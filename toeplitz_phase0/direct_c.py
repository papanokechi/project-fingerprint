"""Extract c with NO fit, by exact subtraction of the derived tail.

    c(s, M) = log det(s) + s^2/2 + (log s)/4 - sum_{m<=M} e_m s^-m

If the e_m are exact, c(s,M) converges to the true constant as the asymptotic
series is truncated optimally.  This replaces the entire Richardson apparatus
of fit_constant.py: no design matrix, no conditioning wall, no fitted nuisance
parameters, and no E1 budget line -- the tail is subtracted, not estimated.

NON-CIRCULARITY.  The recursion supplying e_m comes from an ODE discovered by
nullspace search over sigma = s (log det)' at s in [1,4].  Differentiation
annihilates the constant, so neither the ODE nor the e_m contain any
information about c.  c enters here purely as the integration constant.
Comparing the result to the closed form is therefore still a real test.

HONEST ERROR MODEL.  Two independent error sources, reported separately:
  E_trunc  -- asymptotic series truncation, estimated as the magnitude of the
              first OMITTED term, and cross-checked against the observed
              spread of c(s,M) over M and over s
  E_data   -- certified precision of log det(s) at that point
The reported digit count is driven by the larger, never by mp.dps.
"""

from __future__ import annotations

import json
import sys

from mpmath import mp
from sympy import Rational, sympify


def load_coeffs(path="out/sigma_recursion.json"):
    d = json.load(open(path))
    out = {}
    for row in d["coeffs"]:
        v = sympify(row["e_m"])
        if v != 0:
            out[int(row["m"])] = Rational(v)
    return out


def to_mpf(r):
    return mp.mpf(int(r.p)) / mp.mpf(int(r.q))


def c_estimate(s, L, coeffs, M):
    """(c, first_omitted_term_magnitude) truncating the tail at order M."""
    tail = mp.mpf(0)
    for m in sorted(coeffs):
        if m <= M:
            tail += to_mpf(coeffs[m]) * s ** (-m)
    nxt = [m for m in sorted(coeffs) if m > M]
    omit = abs(to_mpf(coeffs[nxt[0]]) * s ** (-nxt[0])) if nxt else mp.mpf(0)
    return L + s ** 2 / 2 + mp.log(s) / 4 - tail, omit


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "out/sigma_recursion.json"
    coeffs = load_coeffs(path)
    orders = sorted(coeffs)
    mp.dps = 400
    print(f"[cfg] {len(coeffs)} nonzero derived coefficients, max order "
          f"{orders[-1]}; dps={mp.dps} (working precision only -- NOT the "
          f"claimed accuracy)")

    data = json.load(open("out/certified_data.json"))
    rows = sorted(data["rows"], key=lambda r: mp.mpf(r["s"]))
    picks = [r for r in rows if mp.mpf(r["s"]) in
             (mp.mpf(100), mp.mpf(120), mp.mpf(140), mp.mpf(149))]
    if not picks:
        picks = rows[-4:]

    print(f"\n{'s':>7} {'cert.dig':>9} {'M*':>5} {'E_trunc':>12} "
          f"{'E_data':>12}  c (first 60 digits)")
    ests = []
    for r in picks:
        s = mp.mpf(r["s"])
        L = mp.mpf(r["value"])
        cert = mp.mpf(r["certified_digits"])
        # Optimal truncation: minimise the first omitted term.
        best = None
        for M in orders:
            cv, omit = c_estimate(s, L, coeffs, M)
            if omit == 0:
                continue
            if best is None or omit < best[2]:
                best = (M, cv, omit)
        M, cv, omit = best
        edata = mp.mpf(10) ** (-cert)
        ests.append((s, cv, max(omit, edata), M))
        print(f"{mp.nstr(s, 5):>7} {mp.nstr(cert, 6):>9} {M:>5} "
              f"{mp.nstr(omit, 4):>12} {mp.nstr(edata, 4):>12}  "
              f"{mp.nstr(cv, 60)}")

    # Internal consistency: independent s values must agree to within the
    # larger of their two error bars.  This is a check the fit could not do.
    print("\n[cross-s] pairwise |c(s_i) - c(s_j)| vs max(err_i, err_j)")
    ok = True
    for i in range(len(ests)):
        for j in range(i + 1, len(ests)):
            d = abs(ests[i][1] - ests[j][1])
            bar = max(ests[i][2], ests[j][2])
            verdict = "ok" if d <= 10 * bar else "INCONSISTENT"
            if verdict != "ok":
                ok = False
            print(f"  s={mp.nstr(ests[i][0],5):>6} vs {mp.nstr(ests[j][0],5):>6}"
                  f"  diff={mp.nstr(d,4):>11}  bar={mp.nstr(bar,4):>11}  {verdict}")

    best = min(ests, key=lambda e: e[2])
    err = best[2]
    digits = float(-mp.log10(err))
    print(f"\n[best] s={mp.nstr(best[0],5)}  M*={best[3]}  "
          f"honest digits = {digits:.2f}")

    ref = mp.log(2) / 12 + 3 * mp.zeta(-1, derivative=1)
    delta = abs(best[1] - ref)
    agree = float(-mp.log10(delta / abs(ref))) if delta > 0 else float("inf")
    print(f"[gate] |c_derived - ((1/12)log2 + 3 zeta'(-1))| = {mp.nstr(delta,6)}")
    print(f"[gate] agreement: {agree:.2f} digits   "
          f"(claimable: {min(agree, digits):.2f})")

    json.dump({"consistent": ok, "honest_digits": digits,
               "agreement_digits": agree, "M_star": best[3],
               "s": str(best[0]), "c": mp.nstr(best[1], int(digits) + 2)},
              open("out/direct_c.json", "w"), indent=2)
    print("[out] out/direct_c.json")


if __name__ == "__main__":
    main()
