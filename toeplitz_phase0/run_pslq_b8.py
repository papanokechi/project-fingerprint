"""PSLQ on the full 8-element basis, using the fit-free constant.

The 8-element basis has always been the interesting one -- it is the only
basis in this project that contains constants with no business being in the
answer (Catalan, log(1+sqrt2), zeta(3)/pi^2, gamma, log pi), so it is the only
basis whose SILENCE is informative.  It was unreachable at 73 digits because
the measured spurious threshold for b=8 is T=44 and the admissible precision
is D >= max(T,31)+33 ~ 77-78.

With the fit-free extraction at 132 digits it is reachable with ~54 digits of
margin.  L-027 still applies: log2 and zeta'(-1) are in the basis by
construction, so a hit on them validates the instrument.  What is NEW is that
six other constants are available to absorb error and must all come back
exactly zero.
"""

from __future__ import annotations

import json

from mpmath import mp

import constants
import pslq_harness as H


def main():
    d = json.load(open("out/direct_c.json"))
    digits = d["honest_digits"]
    # P must satisfy TWO constraints, and my first run respected only one:
    #   lower: P >= max(T,31)+33 ~ 78 for b=8 (spurious-relation threshold)
    #   upper: P + bump <= honest digits, because condition (a) re-runs the
    #          search at P+30 and a search above the honest count tests our
    #          own noise, not the constant.  Getting this wrong produced a
    #          correct relation at P=110 that "failed" reconfirmation at 140.
    BUMP, MARGIN = 30, 10
    P = int(digits) - BUMP - MARGIN
    if P < 78:
        raise SystemExit(f"P={P} below the b=8 spurious threshold; need more digits")
    mp.dps = P + BUMP + 60
    c = mp.mpf(d["c"])
    print(f"[cfg] fit-free c has {digits:.2f} honest digits; P={P}, "
          f"reconfirm at {P + BUMP} <= {int(digits)} (margin {MARGIN})")

    names_wanted = ["log2", "logpi", "gamma", "zeta'(-1)", "zeta(3)/pi^2",
                    "Catalan", "log(1+sqrt2)"]
    names, vals = constants.basis_values(P + 60, names_wanted)
    # basis_values silently drops names it does not recognise.  My first run
    # misspelled four of the seven and got a b=4 basis with zeta'(-1) absent,
    # which returned "NO RELATION" -- a meaningless negative that looked like
    # a clean result.  Never let a basis shrink silently.
    missing = [n for n in names_wanted if n not in names]
    if missing or len(names) != len(names_wanted):
        raise SystemExit(f"basis mismatch, refusing to run: missing={missing} "
                         f"got={names}")
    print(f"[cfg] basis (b={len(names) + 1} incl. 1): {names}")

    res = H.vet_relation(c, P, names, vals, maxcoeff=10 ** 4, bump=BUMP)
    print("\n[vet] found:", res.get("relation_str", res))
    print("[vet] reconfirmed at P+30:", res.get("reconfirmed"))

    ctrl = H.controls(c, P, names, vals, maxcoeff=10 ** 4,
                      declared=list(zip(names, vals)))
    print("[controls]", json.dumps(ctrl, indent=2)[:900])

    H.flush_log("out/pslq_calls_b8.json")
    json.dump({"P": P, "honest_digits": digits, "basis": names,
               "vet": {k: str(v) for k, v in res.items()},
               "controls": {k: str(v) for k, v in ctrl.items()}},
              open("out/pslq_b8.json", "w"), indent=2)
    print("\n[out] out/pslq_b8.json  out/pslq_calls_b8.json")


if __name__ == "__main__":
    main()
