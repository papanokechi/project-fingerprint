"""Phase 0.1/0.2 production data: certified log det(I - K_s) on an s-grid.

Certification protocol (this is the whole point of the script):

  For each s we compute three values
      v_base = logdet(s, n0,   dps0)
      v_node = logdet(s, 2*n0, dps0)      <- node doubling
      v_prec = logdet(s, n0,   dps0+20)   <- 20-digit precision increase
  and define
      certified_digits(s) = -log10 max(|v_node - v_base|, |v_prec - v_base|)

  A value is reported as VERIFIED only to that many digits.  This number is
  NOT mp.dps and is generally far below it.

The grid is chosen dense and at large s because the limiting error in the
downstream constant extraction is the truncation of the asymptotic series,
which is governed by the SMALLEST s in the fit window, not by the arithmetic.
"""

from __future__ import annotations

import json
import time
from mpmath import mp

import sinekernel as sk

S_MIN, S_MAX, S_STEP = mp.mpf(30), mp.mpf(45), mp.mpf(1) / 2
N0 = 160
DPS0 = 160
DPS_BUMP = 20
OUTPUT = "out/certified_data.json"


def s_grid():
    out, s = [], S_MIN
    while s <= S_MAX + S_STEP / 10:
        out.append(+s)
        s += S_STEP
    return out


def agreement_digits(a, b):
    d = abs(a - b)
    if d == 0:
        return mp.inf
    return -mp.log10(d)


def main():
    mp.dps = DPS0 + DPS_BUMP + 20
    grid = s_grid()
    rows = []
    t0 = time.time()
    for s in grid:
        t = time.time()
        v_base = sk.log_det(s, N0, DPS0)
        v_node = sk.log_det(s, 2 * N0, DPS0)
        v_prec = sk.log_det(s, N0, DPS0 + DPS_BUMP)
        dn = agreement_digits(v_base, v_node)
        dp = agreement_digits(v_base, v_prec)
        cert = min(dn, dp)
        rows.append({
            "s": mp.nstr(s, 20),
            "n0": N0, "dps0": DPS0,
            "value": mp.nstr(v_prec, DPS0 + 10),
            "node_doubling_digits": mp.nstr(dn, 6),
            "precision_bump_digits": mp.nstr(dp, 6),
            "certified_digits": mp.nstr(cert, 6),
        })
        print(f"s={mp.nstr(s,6):>6}  cert={mp.nstr(cert,6):>10} digits "
              f"(node {mp.nstr(dn,6)}, dps {mp.nstr(dp,6)})  {time.time()-t:6.1f}s",
              flush=True)
    meta = {
        "s_min": mp.nstr(S_MIN, 10), "s_max": mp.nstr(S_MAX, 10),
        "s_step": mp.nstr(S_STEP, 10), "n0": N0, "n1": 2 * N0,
        "dps0": DPS0, "dps1": DPS0 + DPS_BUMP,
        "min_certified_digits": mp.nstr(min(mp.mpf(r["certified_digits"]) for r in rows), 8),
        "wall_seconds": round(time.time() - t0, 1),
    }
    json.dump({"meta": meta, "rows": rows}, open(OUTPUT, "w"), indent=1)
    print("\nmin certified digits over grid:", meta["min_certified_digits"])
    print("wrote", OUTPUT, "in", meta["wall_seconds"], "s")


if __name__ == "__main__":
    main()
