"""Extend the certified grid to larger s.

Rationale (measured, not assumed).  With the grid confined to s in [30,45] the
order sweep stalls near 1e-25.  That stall is NOT arithmetic: the measured
noise amplification at that order is ~1e-103, a hundred orders below.  It is
truncation of the asymptotic series, whose size is governed by the smallest s
in the window and by the number of correction orders K the grid can support.

Widening the window upward attacks both at once:
  * more grid points  -> larger K -> more powers of 1/s removed;
  * larger s_max/s_min ratio -> the extrapolation to 1/s^2 = 0 becomes much
    better conditioned (Chebyshev amplification T_m(zeta) with zeta closer to
    1), so the extra orders are actually usable.

n and dps are scaled with s: the node requirement grows with the kernel
bandwidth ~2s/pi, and the arithmetic digit loss was MEASURED in verify_kernel
to be 0.866*s = 2s/ln(10), i.e. condition number ~ exp(2s).
"""

from __future__ import annotations

import json
import math
import sys
import time
from mpmath import mp

import sinekernel as sk
from certify_data import agreement_digits

TARGET_DIGITS = 120
DPS_BUMP = 20
BASE = "out/certified_data.json"


def n_for(s):
    return 2 * int(math.ceil(3.7 * float(s) / 2))


def dps_for(s):
    return int(TARGET_DIGITS + math.ceil(0.866 * float(s)) + 15)


def main(argv):
    """usage: extend_data.py [s_start s_end s_step]

    Each new grid point buys one more correction order K in the downstream
    Richardson sweep.  Points at small s are far cheaper (cost ~ n^3 ~ s^3),
    so filling in the low-s region is the economical way to buy orders; points
    at large s additionally raise s_max/s_min, which improves the conditioning
    of the extrapolation to 1/s^2 = 0.  Both are useful and this script does
    either.
    """
    if len(argv) == 4:
        s_start, s_end, s_step = (mp.mpf(x) for x in argv[1:])
    else:
        s_start, s_end, s_step = mp.mpf(47), mp.mpf(89), mp.mpf(2)

    d = json.load(open(BASE))
    have = {r["s"] for r in d["rows"]}
    rows = list(d["rows"])

    grid, s = [], s_start
    while s <= s_end + s_step / 10:
        grid.append(+s)
        s += s_step

    t0 = time.time()
    for s in grid:
        key = mp.nstr(s, 20)
        if key in have:
            print(f"s={mp.nstr(s,6):>6} already present, skipping")
            continue
        n0, dps0 = n_for(s), dps_for(s)
        mp.dps = dps0 + DPS_BUMP + 20
        t = time.time()
        v_base = sk.log_det(s, n0, dps0)
        v_node = sk.log_det(s, 2 * n0, dps0)
        v_prec = sk.log_det(s, n0, dps0 + DPS_BUMP)
        dn = agreement_digits(v_base, v_node)
        dp = agreement_digits(v_base, v_prec)
        cert = min(dn, dp)
        rows.append({
            "s": key, "n0": n0, "dps0": dps0,
            "value": mp.nstr(v_prec, dps0 + 10),
            "node_doubling_digits": mp.nstr(dn, 6),
            "precision_bump_digits": mp.nstr(dp, 6),
            "certified_digits": mp.nstr(cert, 6),
        })
        print(f"s={mp.nstr(s,6):>6} n0={n0:<5} dps0={dps0:<5} "
              f"cert={mp.nstr(cert,6):>9} digits (node {mp.nstr(dn,6)}, "
              f"dps {mp.nstr(dp,6)})  {time.time()-t:6.1f}s", flush=True)

    mp.dps = 60
    rows.sort(key=lambda r: float(r["s"]))
    d["rows"] = rows
    d["meta"]["s_max"] = mp.nstr(max(mp.mpf(r["s"]) for r in rows), 10)
    d["meta"]["s_min"] = mp.nstr(min(mp.mpf(r["s"]) for r in rows), 10)
    d["meta"]["extended"] = True
    d["meta"]["grid_points"] = len(rows)
    d["meta"]["min_certified_digits"] = mp.nstr(
        min(mp.mpf(r["certified_digits"]) for r in rows), 8)
    d["meta"]["wall_seconds_extension"] = round(time.time() - t0, 1)
    json.dump(d, open(BASE, "w"), indent=1)
    print("\ngrid now", len(rows), "points; min certified digits",
          d["meta"]["min_certified_digits"])


if __name__ == "__main__":
    main(sys.argv)
