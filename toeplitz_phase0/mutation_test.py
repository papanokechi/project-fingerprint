"""Mutation testing: measure whether the checks are alive, don't inspect it.

MOTIVATION.  Instance 12 (L-049) was a control that could not fail for any
input: it printed PASS three times while measuring nothing.  It was found by
building a tool and reasoning about provenance.  That worked, but it is not
repeatable on demand -- and the second version of that very tool reported 0
findings over 65 guards, a result indistinguishable from a dead audit, which
was only caught because a broken/fixed FIXTURE existed to try it against.

The fixture is the general answer, and it generalises: perturb the thing a
check reads, and require the check to notice.  A check that survives a
mutation of its own inputs is switched off, whatever it prints.

    surviving mutant  ==  a claim nothing actually verifies

This turns liveness from a property someone has to notice into a number.

WHAT IS MUTATED.  Every numeric leaf of every artifact in out/ that the test
suite reads -- both JSON numbers and the decimal STRINGS this project uses to
carry high-precision values (mp.nstr output).  Strings matter more than
numbers here: nearly every VERIFIED quantity in this pipeline is stored as a
string to survive the JSON round trip, so a harness that only mutated JSON
numbers would itself be mostly switched off.

DISCIPLINE.  No file is deleted.  Every mutated file is restored from an
in-memory backup in a finally block, and the harness verifies byte-for-byte
restoration at the end -- a mutation harness that corrupts the artifacts it
tests would be a spectacular own goal.

SELF-CONTROL.  The harness checks its own resolution before reporting: a
mutation that does not change the file cannot test anything, so it is
rejected rather than counted as a survivor.  A survivor produced by a no-op
mutation is exactly the reassuring-direction failure this file exists to find.
"""

from __future__ import annotations

import copy
import io
import json
import math
import os
import random
import re
import subprocess
import sys

# Declared in advance.  None of these is derived from the run they govern.
# A MUTATION HARNESS HAS ITS OWN RESOLUTION, and the first version of this
# file ignored that -- exactly the defect it was written to detect.
#
# Run at a single relative perturbation of 1e-6 it reported 2 kills out of 36
# and called the other 34 unconstrained.  But `assert 0.85 < slope < 0.89`
# cannot possibly notice a 1e-6 nudge: the mutant was below the tolerance of
# the check it was testing.  "Survived" then conflates TWO different states --
# no check exists, and a check exists but is coarser than the probe -- and it
# fails in the reassuring direction, because it makes live checks look dead
# and so invites someone to add redundant ones.
#
# Fixed the same way instance 12 was: escalate until the check responds and
# report the SENSITIVITY THRESHOLD.  A field is unconstrained only if it
# survives a mutation large enough that no honest check could miss it.
PERTURB_LADDER = (1e-6, 1e-3, 1e-1, 1.0)
MAX_MUTANTS = 24        # runtime budget; sampled, and the sample is reported
SEED = 20240607
TEST_CMD = [sys.executable, "-m", "pytest", "test_smoke.py", "-q", "-x",
            "--no-header", "-p", "no:cacheprovider"]

NUM_RE = re.compile(r"^-?\d+\.\d+(?:[eE][-+]?\d+)?$")

# SCOPE.  Mutating every artifact in out/ measures the wrong thing: the
# directory is dominated by PSLQ call logs and superseded snapshots, so a
# uniform sample reports a near-zero kill rate that reflects the sampling,
# not the checks.  Scope instead to the artifacts the test file actually
# opens -- discovered FROM the test source, which is an input to this harness
# and not one of its outputs (L-049).
ART_RE = re.compile(r"out/[A-Za-z0-9_.]+\.json")


def artifacts_under_test(test_file="test_smoke.py"):
    src = io.open(test_file, encoding="utf-8").read()
    return sorted(set(os.path.basename(m) for m in ART_RE.findall(src)))


def leaves(obj, path=()):
    """Yield (path, kind) for every mutable numeric leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, path + (i,))
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, float):
        yield path, "float"
    elif isinstance(obj, int):
        yield path, "int"
    elif isinstance(obj, str) and NUM_RE.match(obj.strip()):
        yield path, "numstr"


def get(obj, path):
    for p in path:
        obj = obj[p]
    return obj


def setp(obj, path, val):
    for p in path[:-1]:
        obj = obj[p]
    obj[path[-1]] = val


def mutate(val, kind, rel=None):
    """Perturb by a relative amount large enough to be visible, small enough
    to be a plausible transcription slip rather than obvious garbage."""
    rel = PERTURB_LADDER[0] if rel is None else rel
    if kind == "float":
        return val * (1 + rel) if val else rel
    if kind == "int":
        return val + max(1, int(abs(val) * rel))
    s = val.strip()
    # Perturb a digit late in the mantissa, preserving the exact format so
    # that nothing can notice the mutation by shape alone.
    m = re.match(r"^(-?\d+\.)(\d+)((?:[eE][-+]?\d+)?)$", s)
    if not m:
        return None
    head, frac, tail = m.groups()
    # Digit position chosen so the perturbation is ~rel in relative size.
    i = max(0, min(len(frac) - 1, int(round(-math.log10(rel))) - 1))
    d = frac[i]
    frac = frac[:i] + ("7" if d != "7" else "3") + frac[i + 1:]
    return head + frac + tail


def run_tests():
    r = subprocess.run(TEST_CMD, capture_output=True, text=True)
    return r.returncode == 0


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    outdir = "out"
    files = artifacts_under_test()
    print(f"  artifacts referenced by the test suite: {files}")

    print("=" * 74)
    print("MUTATION TEST -- does any check notice when an artifact changes?")
    print("=" * 74)

    baseline = run_tests()
    print(f"  baseline suite passes: {baseline}")
    if not baseline:
        print("  ABORT: suite already failing, mutation results would be "
              "meaningless (a check cannot be shown alive by a failure it "
              "was going to produce anyway).")
        return 1

    cand = []
    for f in files:
        p = os.path.join(outdir, f)
        try:
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for path, kind in leaves(doc):
            cand.append((f, path, kind))

    # Stratify by FIELD NAME so the sample is not swallowed by whichever
    # field happens to have the most rows.  Reporting a kill rate over an
    # unstratified sample would measure the shape of the artifact.
    rng = random.Random(SEED)
    by_field = {}
    for f, path, kind in cand:
        key = (f, str(path[-1]) if not isinstance(path[-1], int)
               else str(path[-2]) if len(path) > 1 else "?")
        by_field.setdefault(key, []).append((f, path, kind))
    for v in by_field.values():
        rng.shuffle(v)
    order, i = [], 0
    while len(order) < len(cand):
        added = False
        for k in sorted(by_field):
            if i < len(by_field[k]):
                order.append(by_field[k][i])
                added = True
        if not added:
            break
        i += 1
    cand = order
    print(f"  distinct fields: {len(by_field)}")
    print(f"  mutable numeric leaves found: {len(cand)} across {len(files)} "
          f"artifacts")
    print(f"  sampling {min(MAX_MUTANTS, len(cand))} (seed {SEED})\n")

    killed, survived, skipped = [], [], []
    backups = {}
    try:
        for f, path, kind in cand[:MAX_MUTANTS]:
            p = os.path.join(outdir, f)
            if p not in backups:
                backups[p] = io.open(p, encoding="utf-8").read()
            label = f"{f}:{'.'.join(str(x) for x in path)}"
            thresh = None
            tried = 0
            for rel in PERTURB_LADDER:
                doc = json.loads(backups[p])
                old = get(doc, path)
                new = mutate(old, kind, rel)
                if new is None or new == old:
                    continue
                setp(doc, path, new)
                txt = json.dumps(doc, indent=2)
                if txt == backups[p]:
                    continue
                tried += 1
                io.open(p, "w", encoding="utf-8").write(txt)
                ok = run_tests()
                io.open(p, "w", encoding="utf-8").write(backups[p])
                if not ok:
                    thresh = rel
                    break
            if tried == 0:
                skipped.append((f, path, "no effective mutation available"))
                print(f"  skipped   {label}  (no-op at every ladder rung)")
            elif thresh is None:
                survived.append(label)
                print(f"  SURVIVED  {label}  (unmoved up to rel=100%)")
            else:
                killed.append((label, thresh))
                print(f"  killed    {label}  at rel={thresh:g}")
    finally:
        for p, txt in backups.items():
            io.open(p, "w", encoding="utf-8").write(txt)

    # Restoration check.  A harness that leaves the artifacts perturbed would
    # silently poison every downstream claim.
    bad = [p for p, txt in backups.items()
           if io.open(p, encoding="utf-8").read() != txt]
    print(f"\n  artifacts restored byte-for-byte: {len(backups) - len(bad)}"
          f"/{len(backups)}")
    if bad:
        print(f"  RESTORATION FAILED: {bad}")
        return 1

    per = {}
    for lab, _t in killed:
        per.setdefault(lab.split(":")[0], [0, 0])[0] += 1
    for lab in survived:
        per.setdefault(lab.split(":")[0], [0, 0])[1] += 1
    print("\n  kill rate per artifact:")
    for a in sorted(per):
        k, sv = per[a]
        print(f"    {a:34s} killed {k:3d} / survived {sv:3d}")

    n = len(killed) + len(survived)
    print(f"\n  mutants run ....... {n}")
    print(f"  killed ............ {len(killed)}")
    print(f"  SURVIVED .......... {len(survived)}")
    print(f"  skipped ........... {len(skipped)} (no-op mutations, "
          f"rejected rather than scored)")
    if killed:
        print("\n  sensitivity thresholds (smallest relative change detected):")
        for lab, t in killed:
            print(f"    {lab:52s} rel={t:g}")
    if survived:
        print("\n  Survivors are artifact fields NO TEST CONSTRAINS.  That is")
        print("  not automatically a defect -- much of out/ is diagnostic --")
        print("  but any field carrying a VERIFIED claim must be killed.")
        for s in survived:
            print(f"    {s}")

    final = run_tests()
    print(f"\n  suite still passes after restoration: {final}")
    json.dump({"killed": [[a, b] for a, b in killed],
               "survived": survived,
               "skipped": [[a, '.'.join(str(x) for x in b), c]
                           for a, b, c in skipped],
               "restored_ok": not bad, "baseline": baseline,
               "final": final, "seed": SEED,
               "perturb_ladder": list(PERTURB_LADDER)},
              open("out/mutation_test.json", "w"), indent=2)
    print("[out] out/mutation_test.json")
    return 0 if (final and not bad) else 1


if __name__ == "__main__":
    sys.exit(main())
