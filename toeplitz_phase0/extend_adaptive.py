"""Adaptive certified-grid generation, targeting a CERTIFICATION LEVEL.

Why this exists (all of the following was measured, not assumed).

The first generator fixed n = 3.7*s and dps = 120 + 0.866*s + 15.  Inspecting
the resulting grid shows those two rules are badly mismatched to each other:

  * at s = 30 the NODE channel binds: certified digits 98.8, while the
    precision-bump channel reports ~139;
  * at s >= 47 BOTH channels report ~139, i.e. the node error has fallen far
    below the arithmetic floor and the certification is limited purely by the
    design target of 120 digits.

So at large s the nodes are massively oversupplied.  That matters because the
certification protocol requires a run at 2n, whose cost is 8x, and that 8x run
is what makes extending the grid to larger s expensive.  Fitting the measured
node-convergence data gives

        node_digits(n, s)  ~  A*n - B*s + C,   A = 1.767, B = 3.372, C = 2.88

(1.848 digits gained per 0.5 step in s at +2 nodes, and 1.686 digits LOST per
0.5 step in s at fixed n, which pins A and B separately).  Inverting it lets
us ask for a target certification level directly and pay only for that.

The model is an extrapolation when pushed to large s, so it is not trusted:
the certification protocol is still run in full, and if the achieved level
falls short the point is RETRIED with more nodes/precision.  The model only
sets the starting guess; the protocol, not the model, decides what is
certified.
"""

from __future__ import annotations

import json
import math
import sys
import time
from mpmath import mp

import sinekernel as sk
from certify_data import agreement_digits

# 2/ln(10): honest digits gained per unit of s, set by the
# beyond-all-orders remainder exp(-2s) (L-053).  COMPUTED, never
# transcribed: rounding it to 0.866 understated the budget by 0.65
# digits at s=250, and a transcribed rounding of this very constant
# is what produced the L-050 artifact.
DIGITS_PER_S = 2.0 / math.log(10.0)


TARGET = 165          # certification level we are buying
FLOOR = 150           # a point is unacceptable below this
DPS_BUMP = 20
MAX_TRIES = 3
BASE = "out/certified_data.json"

A, B, C = mp.mpf("1.767"), mp.mpf("3.372"), mp.mpf("2.88")


def n_for(s, target=TARGET):
    """Invert the measured node-convergence law, with a floor for small s."""
    n = (mp.mpf(target) + B * mp.mpf(s) - C) / A
    n = max(float(n), 2.2 * float(s))
    return 2 * int(math.ceil(n / 2))


def dps_for(s, target=TARGET):
    """Arithmetic requirement: measured digit loss 0.866*s plus headroom."""
    return int(target + math.ceil(DIGITS_PER_S * float(s)) + 20)


def certify(s, n0, dps0):
    """The full protocol: node doubling AND a +20-digit precision increase."""
    mp.dps = dps0 + DPS_BUMP + 20
    v_base = sk.log_det(s, n0, dps0)
    v_node = sk.log_det(s, 2 * n0, dps0)
    v_prec = sk.log_det(s, n0, dps0 + DPS_BUMP)
    dn = agreement_digits(v_base, v_node)
    dp = agreement_digits(v_base, v_prec)
    return v_prec, dn, dp, min(dn, dp)


def build_point(s, target=TARGET, floor=FLOOR):
    n0, dps0 = n_for(s, target), dps_for(s, target)
    for attempt in range(MAX_TRIES):
        v, dn, dp, cert = certify(s, n0, dps0)
        if cert >= floor:
            return {
                "s": mp.nstr(s, 20), "n0": n0, "dps0": dps0,
                "value": mp.nstr(v, dps0 + 10),
                "node_doubling_digits": mp.nstr(dn, 6),
                "precision_bump_digits": mp.nstr(dp, 6),
                "certified_digits": mp.nstr(cert, 6),
                "attempts": attempt + 1,
            }
        # Grow whichever channel is actually binding.  Guessing wrong here
        # only costs time; the protocol is re-run either way.
        if dn <= dp:
            n0 = 2 * int(math.ceil(n0 * 1.2 / 2))
        else:
            dps0 += 30
        print(f"       retry s={mp.nstr(s,6)}: cert {mp.nstr(cert,6)} < {floor}"
              f" -> n0={n0}, dps0={dps0}", flush=True)
    v, dn, dp, cert = certify(s, n0, dps0)
    return {
        "s": mp.nstr(s, 20), "n0": n0, "dps0": dps0,
        "value": mp.nstr(v, dps0 + 10),
        "node_doubling_digits": mp.nstr(dn, 6),
        "precision_bump_digits": mp.nstr(dp, 6),
        "certified_digits": mp.nstr(cert, 6),
        "attempts": MAX_TRIES + 1,
        "below_floor": True,
    }


def main(argv):
    """usage: extend_adaptive.py s_start s_end s_step [--refit]

    Without --refit, existing grid points are left alone and only new s values
    are computed.  With --refit, an existing point is RECOMPUTED whenever its
    current certification is below TARGET-10; the improved row replaces the
    old one in the working grid file.  The superseded grid is never deleted --
    snapshots are kept alongside -- because a later analysis may need to show
    that the answer did not move when the data got better.
    """
    args = [a for a in argv[1:] if not a.startswith("--")]
    refit = "--refit" in argv
    s_start, s_end, s_step = (mp.mpf(x) for x in args[:3])

    try:
        d = json.load(open(BASE))
    except FileNotFoundError:
        # Full rebuild from nothing: `make verify` must not depend on an
        # artifact left over from a previous session.
        d = {"meta": {"kernel": "sin(s(x-y))/(pi(x-y)) on [-1,1]^2",
                      "protocol": "node doubling AND +20 dps",
                      "created_by": "extend_adaptive.py"},
             "rows": []}
    rows = {r["s"]: r for r in d["rows"]}

    grid, s = [], s_start
    while s <= s_end + s_step / 10:
        grid.append(+s)
        s += s_step

    t0 = time.time()
    for s in grid:
        key = mp.nstr(s, 20)
        old = rows.get(key)
        if old is not None:
            mp.dps = 60
            if not refit or mp.mpf(old["certified_digits"]) >= TARGET - 10:
                print(f"s={mp.nstr(s,6):>7} present at "
                      f"{old['certified_digits']} digits, keeping", flush=True)
                continue
        t = time.time()
        row = build_point(s)
        rows[key] = row
        flag = "  BELOW FLOOR" if row.get("below_floor") else ""
        print(f"s={mp.nstr(s,6):>7} n0={row['n0']:<5} dps0={row['dps0']:<5} "
              f"cert={row['certified_digits']:>9} digits "
              f"(node {row['node_doubling_digits']}, "
              f"dps {row['precision_bump_digits']})  "
              f"{time.time()-t:7.1f}s{flag}", flush=True)
        _save(d, rows, t0)

    _save(d, rows, t0)
    print("\ngrid now", len(rows), "points; min certified digits",
          d["meta"]["min_certified_digits"])


def _save(d, rows, t0):
    """Written after every point: a two-hour run must not lose work."""
    mp.dps = 60
    out = sorted(rows.values(), key=lambda r: float(r["s"]))
    d["rows"] = out
    d["meta"]["s_max"] = mp.nstr(max(mp.mpf(r["s"]) for r in out), 10)
    d["meta"]["s_min"] = mp.nstr(min(mp.mpf(r["s"]) for r in out), 10)
    d["meta"]["grid_points"] = len(out)
    d["meta"]["certification_target"] = TARGET
    d["meta"]["min_certified_digits"] = mp.nstr(
        min(mp.mpf(r["certified_digits"]) for r in out), 8)
    d["meta"]["wall_seconds_adaptive"] = round(time.time() - t0, 1)
    json.dump(d, open(BASE, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv)
