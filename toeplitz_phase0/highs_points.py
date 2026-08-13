"""Test the operator's falsifiable prediction: digits ~ 2s/ln10 ~ 0.869*s.

If optimal truncation of the asymptotic series sits at m* ~ 2s, the residual
left behind is the beyond-all-orders term ~ exp(-2s), so achievable digits
should be LINEAR in s.  Prediction at s=149 is 129.4 against 132.09 measured,
the excess being an algebraic prefactor.

Two outcomes, both informative:
  - digits track 0.869*s     -> precision is linear in s at ~fixed cost per
                                point, and basis size stops constraining
                                Phase 1 target selection
  - digits come in flat      -> the binding limit is the Nystrom evaluation,
                                not the series truncation, which is a
                                different fix entirely

This builds ONE certified point per s.  There is no grid: the fit-free
extraction needs a single point (L-038).
"""

from __future__ import annotations

import json
import sys
import time

from mpmath import mp

import extend_adaptive as EA
import math

# 2/ln(10): honest digits gained per unit of s, set by the
# beyond-all-orders remainder exp(-2s) (L-053).  COMPUTED, never
# transcribed: rounding it to 0.866 understated the budget by 0.65
# digits at s=250, and a transcribed rounding of this very constant
# is what produced the L-050 artifact.
DIGITS_PER_S = 2.0 / math.log(10.0)


OUT = "out/highs_points.json"


def main():
    ss = [int(v) for v in sys.argv[1:]] or [200]
    try:
        existing = json.load(open(OUT))
    except FileNotFoundError:
        existing = {"rows": []}
    have = {r["s"] for r in existing["rows"]}

    for s_int in ss:
        s = mp.mpf(s_int)
        # Certify comfortably above the predicted requirement so the data
        # never becomes the binding budget (it is currently slack by ~57
        # digits at s=149 and we want to keep it that way).
        target = int(DIGITS_PER_S * s_int) + 60
        floor = int(DIGITS_PER_S * s_int) + 40
        t0 = time.time()
        print(f"[build] s={s_int} target={target} floor={floor}", flush=True)
        row = EA.build_point(s, target=target, floor=floor)
        row["wall_seconds"] = round(time.time() - t0, 1)
        print(f"[build] s={s_int} certified={row['certified_digits']} "
              f"n0={row['n0']} dps0={row['dps0']} "
              f"{row['wall_seconds']}s", flush=True)
        if row["s"] in have:
            existing["rows"] = [r for r in existing["rows"]
                                if r["s"] != row["s"]]
        existing["rows"].append(row)
        json.dump(existing, open(OUT, "w"), indent=2)
        print(f"[out] {OUT}", flush=True)


if __name__ == "__main__":
    main()
