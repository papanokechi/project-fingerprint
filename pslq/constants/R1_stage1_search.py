#!/usr/bin/env python3
"""Stage 1 — PSLQ reach for R1 against untested bases.

Runs each proposed basis with R1 as the target limit L (index 0) and the
mandatory phantom L-filter active. Any survivor (non-phantom relation clearing
the Bailey floor) is re-tested at dps 200 -> 300 -> 400 before being called a
candidate. Expected outcome: documented nulls.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pslq_search import run_pslq

HERE = Path(__file__).parent
OUT = HERE / "R1_stage1_results.json"

# Untested bases (April-26 already ruled out bounded-degree algebraicity, the
# bilinear-pi ladder, RIES, OEIS). R1 is entry 0 in every basis -> l_index=0.
BASES = [
    ["R1", "pi", "zeta3"],
    ["R1", "catalan", "log2"],
    ["R1", "pi", "log2", "gamma"],
    ["R1", "zeta3", "catalan"],
    ["R1", "pi_ln2", "zeta3", "one"],
    ["R1", "pi", "pi2", "log2"],          # operator phantom-guard basis
]

MAXCOEFF = 1000
PRIMARY_DPS = 220
RETEST_DPS = [200, 300, 400]


def summarize(r):
    return {
        "basis": r.basis_names,
        "n_entries": r.n_entries,
        "dps": r.dps,
        "maxcoeff": r.maxcoeff,
        "coeffs": r.coeffs,
        "bailey_floor": round(r.floor, 3),
        "eff_digits": round(r.eff_digits, 3),
        "clears_floor": r.clears_floor,
        "l_index": r.l_index,
        "passes_l_filter": r.passes_l_filter,
        "is_candidate": r.is_candidate,
    }


def main():
    results = []
    print("=" * 72)
    print("STAGE 1 — R1 PSLQ reach (l_index=0, L-filter mandatory)")
    print("maxcoeff=%d, primary dps=%d, default (strict) tol" % (MAXCOEFF, PRIMARY_DPS))
    print("=" * 72)
    for basis in BASES:
        t0 = time.time()
        r = run_pslq(basis, dps=PRIMARY_DPS, tol=None, maxcoeff=MAXCOEFF, l_index=0)
        dt = time.time() - t0
        print()
        print(r.report())
        print("  (%.1fs)" % dt)
        entry = {"primary": summarize(r), "retests": []}

        if r.coeffs and r.passes_l_filter and r.clears_floor:
            # A non-phantom, floor-clearing relation -> escalate before claiming.
            print("  >> SURVIVOR at primary dps; escalating 200->300->400 ...")
            for d in RETEST_DPS:
                rr = run_pslq(basis, dps=d, tol=None, maxcoeff=MAXCOEFF, l_index=0)
                print("     dps=%d -> coeffs=%s candidate=%s" % (d, rr.coeffs, rr.is_candidate))
                entry["retests"].append(summarize(rr))
        results.append(entry)

    payload = {
        "stage": 1,
        "target": "R1 (degree-(4,2) PCF limit)",
        "engine": "mpmath %s" % mp.__version__,
        "l_filter": "mandatory; relations with coeff on R1 (index 0) == 0 rejected as phantoms",
        "maxcoeff": MAXCOEFF,
        "primary_dps": PRIMARY_DPS,
        "retest_dps": RETEST_DPS,
        "results": results,
    }
    blob = json.dumps(payload, indent=2)
    OUT.write_text(blob, encoding="utf-8")
    sha = hashlib.sha256(blob.encode("utf-8")).hexdigest()

    n_cand = sum(1 for e in results if e["primary"]["is_candidate"])
    print()
    print("=" * 72)
    print("SUMMARY: %d/%d bases -> NULL; %d candidate(s)"
          % (len(results) - n_cand, len(results), n_cand))
    print("wrote %s" % OUT)
    print("results SHA-256: %s" % sha)


if __name__ == "__main__":
    main()
