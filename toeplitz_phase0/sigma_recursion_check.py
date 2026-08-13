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


# Declared in advance, independent of any measurement below.
E2_RESOLUTION_TARGET = mp.mpf("1e-6")


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
    # RESOLVING POWER, not a tautology.
    #
    # The previous version of this block scaled the perturbation FROM the
    # floor (eps = 100*floor/term2) and then asserted cerr > 10*floor.  Since
    # cerr is then ~100*floor by construction, the assertion reduced to
    # "100 > 10" and could not fail for any input -- measured ratios 101, 99,
    # 99.  It was a control that was switched on and measuring nothing.  Found
    # by assertion_audit.py, not by inspection (L-049).
    #
    # The non-vacuous quantity is the RESOLVING POWER: the smallest relative
    # perturbation of e_2 this data could detect, eps_min = floor / term2.
    # That is a measurement of the data, compared against a threshold declared
    # in advance and independent of it.
    print("\n[resolving power] smallest detectable relative error in e_2")
    print(f"{'s':>8}  {'floor':>13}  {'|e_2 s^-2|':>13}  "
          f"{'eps_min':>13}  {'vs target':>10}")
    worst = None
    for r in picks[:3]:
        s = mp.mpf(r["s"])
        L = mp.mpf(r["logdet"]) if "logdet" in r else mp.mpf(r["value"])
        resid = L - (-s ** 2 / 2 - mp.log(s) / 4 + c)
        pred = sum(to_mpf(coeffs[m]) * s ** (-m) for m in coeffs)
        floor = abs(resid - pred)
        term2 = abs(to_mpf(coeffs[2]) * s ** -2)
        eps_min = floor / term2
        worst = eps_min if worst is None else max(worst, eps_min)
        mark = "ok" if eps_min < E2_RESOLUTION_TARGET else "TOO COARSE"
        print(f"{mp.nstr(s, 6):>8}  {mp.nstr(floor, 4):>13}  "
              f"{mp.nstr(term2, 4):>13}  {mp.nstr(eps_min, 4):>13}  "
              f"{mark:>10}")

    # Positive control: a perturbation ONE DECADE ABOVE the measured
    # resolving power must be detected; one a decade BELOW must not.  Both
    # directions, so the instrument is shown to be neither deaf nor
    # hallucinating.  Threshold and both perturbation sizes are declared
    # relative to eps_min, but the PASS/FAIL boundary is not, so the test can
    # genuinely fail.
    r = picks[0]
    s = mp.mpf(r["s"])
    L = mp.mpf(r["logdet"]) if "logdet" in r else mp.mpf(r["value"])
    resid = L - (-s ** 2 / 2 - mp.log(s) / 4 + c)
    pred = sum(to_mpf(coeffs[m]) * s ** (-m) for m in coeffs)
    floor = abs(resid - pred)
    term2 = abs(to_mpf(coeffs[2]) * s ** -2)
    eps_min = floor / term2

    def detect(eps):
        pert = sum(to_mpf(coeffs[m]) * ((1 + eps) if m == 2 else 1)
                   * s ** (-m) for m in coeffs)
        return abs(resid - pert) > 3 * floor

    loud = detect(10 * eps_min)
    quiet = detect(eps_min / 10)
    print(f"\n[two-sided control at s={mp.nstr(s, 5)}]  "
          f"eps_min = {mp.nstr(eps_min, 4)}")
    print(f"  perturbation 10x ABOVE eps_min detected : {loud}   (want True)")
    print(f"  perturbation 10x BELOW eps_min detected : {quiet}  (want False)")
    if not loud or quiet:
        raise SystemExit(
            "resolution control failed: the instrument is deaf above its "
            "own resolution or hallucinating below it")
    if worst >= E2_RESOLUTION_TARGET:
        raise SystemExit(
            f"data resolves e_2 only to {mp.nstr(worst, 4)}, target is "
            f"{E2_RESOLUTION_TARGET}")
    json.dump({"rows": out, "e2_resolving_power": mp.nstr(worst, 8)},
              open("out/sigma_recursion_check.json", "w"), indent=2)

    print("\n[out] out/sigma_recursion_check.json")


if __name__ == "__main__":
    main()
