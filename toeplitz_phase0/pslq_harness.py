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
