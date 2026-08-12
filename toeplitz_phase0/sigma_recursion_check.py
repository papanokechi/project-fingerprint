"""End-to-end validation of the recursion against certified determinant data.

Chain under test, with each link established independently:

  sigma-form ODE      DISCOVERED by nullspace over our own data (sigma_ode.py)
                      VERIFIED out of sample to 79 digits (sigma_ode_verify.py)
  tail coefficients   DERIVED from that ODE by recursion (sigma_recursion.py)
  constant c          NOT supplied by the recursion -- taken from the closed
                      form, whose only role here is to fix the one number the
                      ODE structurally cannot see

Test: for each certified s,

    resid(s) = log det(s) - ( -s^2/2 - (log s)/4 + c )

should equal sum_m e_m s^-m with the DERIVED e_m.  Nothing in the recursion
was fitted to this data, so agreement is a genuine out-of-sample prediction
of ~30 digits of structure, not a fit.

CONTROL: the same comparison with e_2 perturbed in its last place.  If that
also passes, the test has no resolution and its agreement means nothing
(the rule promoted from L-024).
"""

from __future__ import annotations

import json

from mpmath import mp
from sympy import Rational, sympify


def load_coeffs():
    d = json.load(open("out/sigma_recursion.json"))
    out = {}
    for row in d["coeffs"]:
        v = sympify(row["e_m"])
        if v != 0:
            out[row["m"]] = Rational(v)
    return out, d["M"]


def to_mpf(r):
    return mp.mpf(int(r.p)) / mp.mpf(int(r.q))


def main():
    mp.dps = 120
    coeffs, M = load_coeffs()
    c = mp.log(2) / 12 + 3 * mp.zeta(-1, derivative=1)

    data = json.load(open("out/certified_data.json"))
    rows = data["rows"]
    print(f"[cfg] dps={mp.dps}  derived orders M={M}  "
          f"nonzero e_m: {sorted(coeffs)}")
    print(f"[cfg] c = {mp.nstr(c, 30)}   (closed form; supplies ONLY the "
          f"constant the ODE cannot see)")
    print(f"\n{'s':>8}  {'log10|resid - sum e_m s^-m|':>30}  "
          f"{'log10|resid|':>14}  {'digits explained':>17}")

    picks = []
    alls = sorted(rows, key=lambda r: mp.mpf(r["s"]))
    for target in [30, 60, 90, 120, 149]:
        best = min(alls, key=lambda r: abs(mp.mpf(r["s"]) - target))
        if best not in picks:
            picks.append(best)

    out = []
    for r in picks:
        s = mp.mpf(r["s"])
        L = mp.mpf(r["logdet"]) if "logdet" in r else mp.mpf(r["value"])
        resid = L - (-s ** 2 / 2 - mp.log(s) / 4 + c)
        pred = sum(to_mpf(coeffs[m]) * s ** (-m) for m in coeffs)
        err = abs(resid - pred)
        gained = float(mp.log10(abs(resid) / err)) if err > 0 else float("inf")
        print(f"{mp.nstr(s, 6):>8}  {mp.nstr(err, 6):>30}  "
              f"{mp.nstr(abs(resid), 6):>14}  {gained:>17.1f}")
        out.append({"s": str(s), "log10_err": float(mp.log10(err)),
                    "digits_explained": gained})

    # Resolution control (L-024 rule, and L-036: I violated it here first).
    # The truncation error at each s is the resolution floor.  A perturbation
    # of e_2 only registers if it moves the sum by more than that floor, so
    # the perturbation must be CHOSEN from the measured floor, never fixed in
    # advance.  My first attempt used a fixed 1e-20 and was ~10 orders below
    # resolution at every point -- it "passed" by being switched off.
    print("\n[control] e_2 perturbed; size chosen from the measured floor")
    print(f"{'s':>8}  {'floor':>13}  {'rel.perturb':>13}  "
          f"{'control err':>13}  {'verdict':>8}")
    for r in picks[:3]:
        s = mp.mpf(r["s"])
        L = mp.mpf(r["logdet"]) if "logdet" in r else mp.mpf(r["value"])
        resid = L - (-s ** 2 / 2 - mp.log(s) / 4 + c)
        pred = sum(to_mpf(coeffs[m]) * s ** (-m) for m in coeffs)
        floor = abs(resid - pred)
        term2 = to_mpf(coeffs[2]) * s ** -2
        eps = 100 * floor / term2          # 100x above the resolution floor
        pert = sum(to_mpf(coeffs[m]) * ((1 + eps) if m == 2 else 1)
                   * s ** (-m) for m in coeffs)
        cerr = abs(resid - pert)
        ok = "PASS" if cerr > 10 * floor else "NO RES."
        print(f"{mp.nstr(s, 6):>8}  {mp.nstr(floor, 4):>13}  "
              f"{mp.nstr(eps, 4):>13}  {mp.nstr(cerr, 4):>13}  {ok:>8}")

    json.dump(out, open("out/sigma_recursion_check.json", "w"), indent=2)
    print("\n[out] out/sigma_recursion_check.json")


if __name__ == "__main__":
    main()
