"""Phase 0 closure status.  The stopping rule as an invariant, not a paragraph.

WHY THIS FILE EXISTS.  Four consecutive rounds have closed the outstanding
items and opened more, and every round was worth doing.  That is the problem:
the work being genuinely good is exactly what makes an indefinitely expanding
Phase 0 hard to notice from inside.  Calibration was meant to earn the right
to make a Phase 1 claim; it has since produced a rediscovered sigma-PV form,
derived trans-series exponents, a 60x precision improvement and a reusable
verification toolchain, and Phase 1 still has not started.

L-036 established that promoting a rule to the spec does not make anyone
follow it -- the rule was broken inside the file that cited it.  So the
stopping rule is written here as something that RUNS and prints a verdict,
with the queue as the DEFAULT DESTINATION for anything new rather than a
judgement call each time.

THE RULE.
  Phase 0 CLOSES when the mechanical conditions below pass AND the triage
  table's provenance cells are filled from primaries for at least one
  candidate (entry condition #11, operator-gated).

  After the mechanical conditions pass, EVERY NEW FINDING GOES TO THE QUEUE,
  including findings that are interesting, cheap, and would obviously work.
  "It is only hours" is the argument that has kept Phase 0 open for four
  rounds; it is therefore not an argument, it is the symptom.

  The queue is open_questions.md.  Items may be worked only after Phase 1
  target selection, or on explicit operator instruction.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

PY = sys.executable


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def check_tests():
    rc, _ = _run([PY, "-m", "pytest", "test_smoke.py", "-q", "--no-header",
                  "-p", "no:cacheprovider"])
    return rc == 0, "smoke suite passes"


def check_audit():
    rc, out = _run([PY, "assertion_audit.py"])
    m = re.search(r"CIRCULAR-COMPARISON \.+ (\d+)", out)
    t = re.search(r"TRANSCRIBED NUMERICS \.+ (\d+)", out)
    n = int(m.group(1)) if m else -1
    k = int(t.group(1)) if t else -1
    return rc == 0, f"assertion audit clean (circular={n}, transcribed={k})"


def check_mutation():
    """Every field carrying a VERIFIED claim must be killable."""
    p = "out/mutation_test.json"
    if not os.path.exists(p):
        return False, "mutation_test.json absent -- liveness unmeasured"
    d = json.load(open(p))
    claim_fields = ("value", "honest", "predicted", "measured_slope",
                    "certified_digits")
    surv = [s for s in d["survived"]
            if s.rsplit(".", 1)[-1] in claim_fields]
    killed = {k[0] for k in d["killed"]}
    return (not surv,
            f"no VERIFIED-claim field survives mutation "
            f"({len(killed)} killed, {len(surv)} claim-fields surviving"
            + (f": {surv}" if surv else "") + ")")


def check_gate():
    p = "out/gate.json"
    if not os.path.exists(p):
        return False, "gate.json absent"
    d = json.load(open(p))
    ok = bool(d.get("passed"))
    return ok, f"calibration gate passes ({d.get('agreement_digits')} digits)"


def check_trans():
    p = "out/trans_series.json"
    if not os.path.exists(p):
        return False, "trans_series.json absent"
    d = json.load(open(p))
    return bool(d.get("consistent")), \
        "trans-series exponents derived and consistent with measurement"


TAGS = ("PROVEN", "VERIFIED", "STRUCTURAL", "CONJECTURED")


def check_untagged_claims():
    """Every ledger section must carry an epistemic tag.

    The first version of this check demanded a literal `Tag:` line and
    reported 43 of 59 entries untagged.  They are tagged -- the early ones use
    a bolded **PROVEN** / **VERIFIED** marker at the head of the body, the
    later ones a `Tag:` line.  The check fired, was sensitive, and asserted
    the WRONG THING: L-057's third category, appearing within minutes of
    L-057 being written.  Kept as a comment rather than silently corrected,
    because a checker that has never been wrong is a checker nobody has
    tested.
    """
    src = open("ledger.md", encoding="utf-8").read()
    # HARD RULE 3 is append-only, so entries written before the tagging
    # convention settled are tagged by an appended RETROTAG line, not by
    # editing them.  L-061.
    retro = set(re.findall(r"RETROTAG (L-\d+):", src))
    secs = re.split(r"^## ", src, flags=re.M)[1:]
    missing = []
    for sec in secs:
        title = sec.splitlines()[0]
        head = "\n".join(sec.splitlines()[:8])
        ident = re.match(r"(L-\d+)", title)
        if ident and ident.group(1) in retro:
            continue
        if not any(t in head for t in TAGS):
            missing.append(title[:52])
    return not missing, (f"all {len(secs)} ledger entries carry an epistemic "
                         f"tag" + (f" -- MISSING: {missing}" if missing else ""))


MECHANICAL = [check_tests, check_audit, check_mutation, check_gate,
              check_trans, check_untagged_claims]


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 74)
    print("PHASE 0 CLOSURE STATUS")
    print("=" * 74)
    results = []
    for fn in MECHANICAL:
        try:
            ok, msg = fn()
        except Exception as e:
            ok, msg = False, f"{fn.__name__} raised {e!r}"
        results.append(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}]  {msg}")

    mech = all(results)
    print(f"\n  mechanical conditions: {'ALL PASS' if mech else 'INCOMPLETE'}")

    # Entry condition #11 requires PRIMARY provenance.  I originally wrote
    # this as operator-gated and unreachable in-session.  That was WRONG, and
    # the operator caught it: HARD RULE 2 forbids taking provenance from
    # RECALL (mine or the operator's), but READING a primary is not recall.
    # Provenance columns are facts printed in a body -- how many digits are
    # shown, whether a second proof is cited, where the normalisation is
    # stated -- and bodies are fetchable.  The condition is discharged by
    # reading, and was.
    tri = open("phase1_triage.md", encoding="utf-8").read()
    # Only the ACTIVE table counts.  Superseded revisions are retained
    # verbatim (nothing in this project is deleted), and their unfilled
    # cells are history, not outstanding work.
    marker = "<!-- ACTIVE-TRIAGE -->"
    active = tri.split(marker, 1)[1] if marker in tri else tri
    unfilled = active.count("| ? |")
    print(f"\n  [#11]  provenance cells filled from primaries")
    print(f"         unfilled cells in the ACTIVE triage table: {unfilled}")
    if unfilled:
        print("         Fill them by READING primaries.  Recall is barred;")
        print("         reading is not.  Any row that cannot be filled from a")
        print("         primary is marked UNFILLABLE and the candidate drops.")

    closed = mech and unfilled == 0
    print("\n" + "-" * 74)
    if closed:
        print("  PHASE 0: CLOSED.  Phase 1 target selection may proceed.")
    else:
        print("  PHASE 0: OPEN, blocked on operator-supplied primary")
        print("           provenance.  Mechanical work is "
              + ("COMPLETE." if mech else "incomplete."))
        if mech:
            print("\n  => Because the mechanical conditions pass, THE QUEUE IS")
            print("     NOW THE DEFAULT DESTINATION for every new finding.")
            print("     Interesting, cheap and obviously-correct are not")
            print("     exceptions -- they are the symptom.  See OS-13/14/15.")
    print("-" * 74)

    json.dump({"mechanical_all_pass": mech,
               "unfilled_triage_cells": unfilled,
               "phase0_closed": closed,
               "checks": [f.__name__ for f in MECHANICAL],
               "results": results},
              open("out/phase0_status.json", "w"), indent=2)
    print("\n[out] out/phase0_status.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
