"""Pre-registered test of the operator's digits ~= 0.869*s law.

The prediction, and the falsification condition, were written into
open_questions.md (revision 5) BEFORE this script was run.  If the achieved
digit count comes in flat rather than scaling linearly in s, the binding
constraint is Nystrom evaluation, not series truncation.

Nothing here fits anything.  c is read off the exact recursion at optimal
truncation, exactly as in direct_c.py; the only new quantity is the honest
digit count at each s, compared against a number fixed in advance.
"""
import json
import os
import sys

from mpmath import mp

from direct_c import load_coeffs, c_estimate

PREDICTED = {149: 129.4, 200: 173.8, 250: 217.3}


def rows():
    """Certified points from both builders, keyed by s (larger cert wins)."""
    out = {}
    for path in ("out/certified_data.json", "out/highs_points.json"):
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        for r in d.get("rows", d if isinstance(d, list) else []):
            s = int(mp.mpf(r["s"]))
            cert = mp.mpf(r["certified_digits"])
            if s not in out or cert > out[s][1]:
                out[s] = (r, cert)
    return out


def main():
    coeffs = load_coeffs(sys.argv[1] if len(sys.argv) > 1
                         else "out/sigma_recursion_fast.json")
    orders = sorted(coeffs)
    mp.dps = 600

    have = rows()
    want = [s for s in (149, 200, 250) if s in have]
    print(f"[cfg] {len(coeffs)} coefficients, max order {orders[-1]}; "
          f"points available: {sorted(have)}")

    res = []
    print(f"\n{'s':>5} {'cert':>8} {'M*':>5} {'2s':>5} {'E_trunc':>11} "
          f"{'honest':>8} {'pred':>8} {'excess':>8}")
    for s_int in want:
        r, cert = have[s_int]
        s = mp.mpf(r["s"])
        L = mp.mpf(r["value"])
        best = None
        for M in orders:
            cv, omit = c_estimate(s, L, coeffs, M)
            if omit == 0:
                continue
            if best is None or omit < best[2]:
                best = (M, cv, omit)
        M, cv, omit = best
        # M* at the top of the available range means the truncation minimum
        # was never reached -- the digit count is then a lower bound, not a
        # measurement, and must not be compared against the prediction.
        saturated = M >= orders[-1]
        err = max(omit, mp.mpf(10) ** (-cert))
        honest = -mp.log10(err / max(abs(cv), mp.mpf(1)))
        pred = PREDICTED[s_int]
        res.append((s_int, float(honest), pred, saturated, cv, err, M))
        flag = "  <-- SATURATED, lower bound only" if saturated else ""
        print(f"{s_int:>5} {mp.nstr(cert,6):>8} {M:>5} {2*s_int:>5} "
              f"{mp.nstr(omit,4):>11} {float(honest):>8.2f} {pred:>8.1f} "
              f"{float(honest)-pred:>8.2f}{flag}")

    usable = [x for x in res if not x[3]]
    print("\n[verdict]")
    if len(usable) < 2:
        print("  INCONCLUSIVE: fewer than two unsaturated points. Extend the")
        print("  recursion past M = 2*s_max before comparing against the law.")
        return
    excess = [x[1] - x[2] for x in usable]
    spread = max(excess) - min(excess)
    print(f"  excess over 0.869*s: {['%.2f' % e for e in excess]}")
    print(f"  spread {spread:.2f} digits over s in "
          f"[{usable[0][0]}, {usable[-1][0]}]")
    if spread < 5:
        print("  CONSISTENT with digits = 0.869*s + const (prefactor).")
        print("  Precision is truncation-limited and linear in s.")
    elif usable[-1][1] - usable[0][1] < 5:
        print("  FLAT: digit count did not scale. Nystrom-limited, NOT")
        print("  truncation-limited -- the law is falsified in this regime.")
    else:
        print("  Scales, but not at the predicted rate. Report the measured")
        print("  slope rather than the predicted one.")
    slope = ((usable[-1][1] - usable[0][1])
             / (usable[-1][0] - usable[0][0])) if len(usable) > 1 else 0
    print(f"  measured slope: {slope:.4f} digits per unit s "
          f"(predicted 0.8686)")

    json.dump({"points": [{"s": x[0], "honest": x[1], "predicted": x[2],
                           "saturated": x[3], "M": x[6],
                           "c": mp.nstr(x[4], 40)} for x in res],
               "measured_slope": slope},
              open("out/prediction_test.json", "w"), indent=2)
    print("\n[out] out/prediction_test.json")


if __name__ == "__main__":
    main()
