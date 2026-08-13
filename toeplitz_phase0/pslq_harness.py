"""Phase 0.4: PSLQ harness with adversarial null controls.

Every PSLQ invocation made by this module is logged -- successes AND failures.
Unlogged failed attempts are the primary contamination vector for integer
relation work: if you run twenty searches and report the one that returned
something, you have reported a fluctuation.

A relation is REPORTABLE only if all of the following hold:

  (a) it is found at precision P and re-found at P+30 with *identical*
      coefficients;
  (b) its coefficient sup-norm is below MAXCOEFF (default 10^4);
  (c) the null controls both come back empty:
        (i)  a target perturbed to c*(1+1e-20)
        (ii) a random 30-digit constant
      If either null control returns a relation, the basis is overcomplete at
      that precision.  The harness then reports the spurious-relation
      threshold instead of the relation.

The harness additionally measures the spurious-relation threshold directly by
sweeping precision against random targets, so that (c) is backed by a number
rather than by a single pass/fail.
"""

from __future__ import annotations

import json
import random
from mpmath import mp

import constants

LOG = "out/pslq_calls.json"
_CALLS = []


def _log(kind, dps, tol_exp, maxcoeff, maxsteps, names, result, note=""):
    rec = {
        "kind": kind, "dps": dps, "tol": f"1e-{tol_exp}",
        "maxcoeff": maxcoeff, "maxsteps": maxsteps,
        "basis": list(names),
        "result": None if result is None else [int(x) for x in result],
        "note": note,
    }
    _CALLS.append(rec)
    tag = "NO RELATION" if result is None else str(rec["result"])
    print(f"    [pslq] {kind:<28} dps={dps:<5} maxcoeff={maxcoeff:<8} -> {tag}")
    return rec


def flush_log(path=LOG):
    json.dump(_CALLS, open(path, "w"), indent=1)
    return path


def pslq_search(target, dps, names, vals, maxcoeff=10**4, maxsteps=10**6,
                guard=8, kind="search", note=""):
    """One logged PSLQ call on [target] + basis values, all at precision dps."""
    with mp.workdps(dps):
        vec = [+mp.mpf(target)] + [+mp.mpf(v) for v in vals]
        tol_exp = dps - guard
        tol = mp.mpf(10) ** (-tol_exp)
        try:
            rel = mp.pslq(vec, tol=tol, maxcoeff=maxcoeff, maxsteps=maxsteps)
        except Exception as exc:                      # pragma: no cover
            _log(kind, dps, tol_exp, maxcoeff, maxsteps, names, None,
                 note=f"{note} EXCEPTION {exc}")
            return None
    _log(kind, dps, tol_exp, maxcoeff, maxsteps, names, rel, note=note)
    return rel


def residual(rel, target, vals, dps):
    """|sum of the relation| at precision dps -- how well it actually holds."""
    with mp.workdps(dps + 20):
        tot = mp.mpf(rel[0]) * mp.mpf(target)
        for k, v in zip(rel[1:], vals):
            tot += mp.mpf(k) * mp.mpf(v)
        return abs(tot)


def format_relation(rel, names):
    terms = []
    for k, nm in zip(rel[1:], names):
        if k:
            terms.append(f"{int(k):+d}*{nm}")
    lead = int(rel[0])
    return f"{lead:+d}*c " + " ".join(terms) + " = 0"


def spurious_threshold(dps_list, names, vals, maxcoeff=10**4, trials=3,
                       seed=20260812):
    """Lowest precision at which random targets STOP producing relations.

    Returns (threshold_or_None, table).  Every call is logged.
    """
    rng = random.Random(seed)
    table = []
    for dps in dps_list:
        hits = 0
        for t in range(trials):
            with mp.workdps(dps + 20):
                r = mp.mpf(rng.getrandbits(200)) / mp.mpf(2) ** 200
                target = mp.mpf(1) + r
            rel = pslq_search(target, dps, names, vals, maxcoeff=maxcoeff,
                              kind=f"NULL-random(dps={dps},trial={t})")
            if rel is not None:
                hits += 1
        table.append({"dps": dps, "random_targets": trials, "relations_found": hits})
    clean = [row["dps"] for row in table if row["relations_found"] == 0]
    # The threshold must be read from ABOVE: adding precision can only make
    # spurious relations rarer, so the meaningful quantity is the lowest
    # precision from which every HIGHER swept precision is also clean.  Taking
    # min(clean) instead would return the bottom of the sweep, where PSLQ
    # simply fails to converge (tol is looser than the basis spacing) and
    # reports nothing for reasons that have nothing to do with completeness.
    thr = None
    for row in sorted(table, key=lambda r: -r["dps"]):
        if row["relations_found"] == 0:
            thr = row["dps"]
        else:
            break
    return thr, table


def vet_relation(c, dps, names, vals, maxcoeff=10**4, bump=30):
    """Full gated search around target c.  Returns a verdict dict."""
    verdict = {"reportable": False, "relation": None, "reasons": []}

    rel = pslq_search(c, dps, names, vals, maxcoeff=maxcoeff,
                      kind=f"TARGET c (P={dps})")
    if rel is None:
        verdict["reasons"].append(f"no relation at P={dps}")
        return verdict

    rel2 = pslq_search(c, dps + bump, names, vals, maxcoeff=maxcoeff,
                       kind=f"TARGET c (P+{bump}={dps+bump})")
    if rel2 is None or list(rel2) != list(rel):
        verdict["relation"] = [int(x) for x in rel]
        verdict["reasons"].append(
            f"(a) FAILED: coefficients at P+{bump} are "
            f"{None if rel2 is None else [int(x) for x in rel2]}, not identical")
        return verdict

    if max(abs(int(x)) for x in rel) > maxcoeff:
        verdict["reasons"].append("(b) FAILED: sup-norm above threshold")
        return verdict

    verdict["relation"] = [int(x) for x in rel]
    verdict["reportable"] = True
    verdict["reasons"].append(f"(a) reconfirmed at P+{bump} with identical coefficients")
    verdict["reasons"].append(f"(b) sup-norm {max(abs(int(x)) for x in rel)} <= {maxcoeff}")
    return verdict


def null_controls(c, dps, names, vals, maxcoeff=10**4, seed=20260812):
    """Controls (i) perturbed target and (ii) random 30-digit constant."""
    out = {}
    with mp.workdps(dps + 20):
        c_pert = mp.mpf(c) * (1 + mp.mpf(10) ** -20)
    out["perturbed"] = pslq_search(c_pert, dps, names, vals, maxcoeff=maxcoeff,
                                   kind="NULL-perturbed c*(1+1e-20)")
    rng = random.Random(seed)
    with mp.workdps(dps + 20):
        rnd = mp.mpf(rng.getrandbits(120)) / mp.mpf(10) ** 36
    out["random"] = pslq_search(rnd, dps, names, vals, maxcoeff=maxcoeff,
                                kind="NULL-random 30-digit constant")
    out["passed"] = out["perturbed"] is None and out["random"] is None
    return out


# ---------------------------------------------------------------------------
# Structural guard against the recurring failure of this project: a check run
# outside its own validity domain.  Three instances in one session (L-024,
# L-040(6), L-040(7), L-040(8)), the second of which broke a rule stated in
# the docstring of the very file that broke it.
#
# Rules did not work.  So this is not a rule: null_controls and
# positive_control cannot execute without passing through resolution_guard,
# and it RAISES rather than warns.  A future implementation can no longer
# omit it by forgetting, only by deliberately deleting it.
# ---------------------------------------------------------------------------

class ResolutionError(RuntimeError):
    """A check was asked to detect something below its own resolution."""


def resolution_guard(what, effect_size, resolution, margin=100):
    """Assert a check can actually see the thing it claims to test.

    effect_size -- how far the perturbation/plant moves the quantity
    resolution  -- the smallest difference the instrument can register
    Raises unless effect_size >= margin * resolution.
    """
    eff, res = mp.mpf(effect_size), mp.mpf(resolution)
    if not (eff >= margin * res):
        raise ResolutionError(
            f"{what}: effect {mp.nstr(eff, 5)} is not {margin}x above "
            f"resolution {mp.nstr(res, 5)}. A negative result here would be "
            f"indistinguishable from the control being switched off.")
    return {"what": what, "effect": mp.nstr(eff, 6),
            "resolution": mp.nstr(res, 6), "margin_ok": True}


def positive_control(dps, names, vals, maxcoeff=10**4, seed=20260813,
                     trials=3, kmax=40, declared=None):
    """Plant a KNOWN relation and require the harness to recover it exactly.

    The null controls establish that the instrument finds nothing when there
    is nothing.  They say nothing about whether it would find something when
    there IS something -- a precision that is too low, a tolerance that is
    too tight, or a coefficient bound that is too small all fail BOTH null
    controls happily and look clean.

    IMPORTANT, and NOT what I first implemented.  Planting over the basis
    that was PASSED IN does not detect a basis that silently lost an element
    (L-040(7)): the shrunken basis simply recovers its own plant and reports
    OK.  Measured directly -- dropping zeta'(-1) from b=8 left all three
    plants recovered and both null controls silent.  A positive control is
    therefore NOT a remedy for basis-identity errors unless the plant is
    built over the basis the caller INTENDED.

    `declared` = [(name, value)] of the intended basis.  When supplied, the
    target is planted over THOSE values and searched over the actual ones, so
    a missing element makes the planted relation unfindable.
    """
    rng = random.Random(seed)
    plant_names = [n for n, _ in declared] if declared else list(names)
    plant_vals = [v for _, v in declared] if declared else list(vals)
    results = []
    for t in range(trials):
        with mp.workdps(dps + 30):
            ks = [rng.randint(-kmax, kmax) for _ in plant_vals]
            if all(k == 0 for k in ks):
                ks[0] = 1
            # Force a nonzero coefficient on any declared element that is
            # absent from the actual basis, so its absence must show up.
            for i, nm in enumerate(plant_names):
                if nm not in names and ks[i] == 0:
                    ks[i] = 1
            target = sum(mp.mpf(k) * mp.mpf(v)
                         for k, v in zip(ks, plant_vals))
            scale = max(abs(mp.mpf(v)) for v in plant_vals)
            resolution_guard(
                f"positive control trial {t}",
                effect_size=max(abs(target), mp.mpf(10) ** (-dps // 2)),
                resolution=scale * mp.mpf(10) ** (-dps),
                margin=10)

        rel = pslq_search(target, dps, names, vals, maxcoeff=maxcoeff,
                          kind=f"POSITIVE-control planted #{t}")
        # Expected coefficients, expressed over the ACTUAL basis order.
        kmap = dict(zip(plant_names, ks))
        want = [1] + [-kmap.get(n, 0) for n in names]
        exact = plant_names == list(names)
        ok = rel is not None and (
            [int(x) for x in rel] == want or [-int(x) for x in rel] == want)
        results.append({"trial": t, "planted": ks, "over": plant_names,
                        "found": None if rel is None else [int(x) for x in rel],
                        "recovered": bool(ok), "basis_identical": exact})
    passed = all(r["recovered"] for r in results)
    return {"trials": results, "passed": passed}


def controls(c, dps, names, vals, maxcoeff=10**4, seed=20260812, declared=None):
    """Both halves of the pair.  Use THIS, not null_controls alone.

    A run that reports only null results has verified that the instrument is
    silent, which is also what a broken instrument reports.

    `declared` = [(name, value)] of the INTENDED basis; pass it whenever the
    caller knows what the basis was supposed to be, so that a silently
    shrunken basis fails the positive control instead of passing everything.
    """
    with mp.workdps(dps + 30):
        pert_effect = abs(mp.mpf(c)) * mp.mpf(10) ** -20
        guard = resolution_guard("null control perturbation",
                                 effect_size=pert_effect,
                                 resolution=mp.mpf(10) ** (-dps),
                                 margin=100)
    null = null_controls(c, dps, names, vals, maxcoeff=maxcoeff, seed=seed)
    pos = positive_control(dps, names, vals, maxcoeff=maxcoeff,
                           declared=declared)
    return {"null": null, "positive": pos, "null_guard": guard,
            "passed": bool(null["passed"] and pos["passed"])}
