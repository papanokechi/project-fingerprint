"""Trans-series structure of the sine-kernel tail: derive A and b, don't fit them.

L-050 MEASURED  E_trunc ~ C * exp(-2s) / s  by fitting 91 honest-digit counts.
That is a VERIFIED empirical law.  This script derives the two exponents from
the ODE alone -- no digit counts, no fit to the L-050 data -- by two routes
that do not share a mechanism:

  ROUTE 1 (WKB).  Linearize s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2 = 0 about
    the perturbative solution.  The quadratic-in-sigma'' structure gives a
    second-order LINEAR ODE for the perturbation delta, whose WKB solution at
    large s is  C * s^(theta) * exp(-A s)  with A and theta fixed by the
    equation and C left free.  C is a Stokes constant: linearization cannot
    determine it, which is exactly why it must be measured and the exponents
    must not be.

  ROUTE 2 (resurgence / large-order).  The same exponential controls the
    large-order growth of the perturbative coefficients:
        e_m ~ (S/2pi i) * Gamma(m + beta) / A^(m+beta)
    We hold 300 exact rational e_m from the recursion.  Reading A and beta off
    their growth uses no differential-equation manipulation at all.

  RECONCILIATION.  The exponent in the MEASURED law is a third thing again,
    and conflating it with either of the above is the error this file exists
    to avoid.  The honest-digit count measures the OPTIMAL-TRUNCATION error,
    i.e. the least term of the series, and Stirling puts a sqrt between the
    least term and the trans-series term.  Derived below:  a = 1/2 - beta.

Nothing here reads out/prediction_test.json or out/excess_structure.json.
The comparison at the end is therefore out-of-sample in both directions.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as Fr

import sympy as sp
from mpmath import mp, mpf, log, sqrt, pi, loggamma, exp

import sigma_recursion_fast as srf

# Declared in advance, so that no threshold below is derived from the thing it
# judges (L-049).  These are the values the two routes must agree on; they are
# NOT read from the measurement they will be compared against.
N_WKB_ORDERS = 10      # orders of 1/s carried through the Riccati solve
N_SIGMA = 24           # perturbative orders used to build the linearization
NEVILLE_DEG = 16       # degree of the 1/m extrapolation in route 2
BETA_TOL = mpf("1e-15") # declared: how close to a half-integer beta must land


# --------------------------------------------------------------------------
# ROUTE 1 -- linearize the ODE and solve the Riccati equation for the exponent
# --------------------------------------------------------------------------

def route1_wkb(verbose=True):
    s = sp.symbols("s", positive=True)

    coeffs = srf.solve(N_SIGMA, verbose=False)
    sig = -s**2 - sp.Rational(1, 4)
    for m, v in coeffs:
        sig += sp.Rational(v.numerator, v.denominator) * s**(-m)

    d1 = sp.diff(sig, s)
    d2 = sp.diff(d1, s)
    u = s * d1 - sig

    # F(sigma) = s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2 ; delta u = s d' - d.
    # dF = 2 s^2 sigma'' d'' + (32u + 4 sigma'^2)(s d' - d) + 8 u sigma' d'
    Cdd = 2 * s**2 * d2
    W = 32 * u + 4 * d1**2
    Cd = W * s + 8 * u * d1
    C0 = -W

    P = sp.simplify(Cd / Cdd)
    Q = sp.simplify(C0 / Cdd)

    z = sp.symbols("z", positive=True)
    def ser(expr, n):
        e = expr.subs(s, 1 / z)
        return sp.series(sp.together(e), z, 0, n).removeO().expand()

    Pz = sp.Poly(ser(P, N_WKB_ORDERS), z)
    Qz = sp.Poly(ser(Q, N_WKB_ORDERS), z)
    p = [Pz.coeff_monomial(z**k) for k in range(N_WKB_ORDERS)]
    q = [Qz.coeff_monomial(z**k) for k in range(N_WKB_ORDERS)]

    # S0^2 + p0 S0 + q0 = 0.  p0 = 0 below (the leading delta' coefficients
    # cancel), so this is just S0^2 = -q0.
    S0s = sp.solve(sp.Symbol("S0")**2 + p[0] * sp.Symbol("S0") + q[0],
                   sp.Symbol("S0"))
    A = -min(S0s)          # decaying branch S0 = -A, A > 0

    # Riccati: S' + S^2 + P S + Q = 0 with S = sum S_k z^k, d/ds = -z^2 d/dz.
    K = N_WKB_ORDERS - 2
    Sk = [sp.Rational(0)] * (K + 1)
    Sk[0] = -A
    unk = sp.symbols(f"c1:{K+1}")
    Sser = Sk[0] + sum(unk[i - 1] * z**i for i in range(1, K + 1))
    expr = (-z**2 * sp.diff(Sser, z) + Sser**2
            + sum(p[k] * z**k for k in range(N_WKB_ORDERS)) * Sser
            + sum(q[k] * z**k for k in range(N_WKB_ORDERS)))
    expr = sp.expand(expr)
    sol = {}
    for k in range(1, K + 1):
        eq = sp.expand(expr.coeff(z, k)).subs(sol)
        r = sp.solve(eq, unk[k - 1])
        if len(r) != 1:
            raise RuntimeError(f"order {k}: {len(r)} solutions, refusing")
        sol[unk[k - 1]] = sp.nsimplify(r[0])
    theta = sol[unk[0]]        # delta ~ s^theta exp(-A s)

    if verbose:
        print("ROUTE 1 -- WKB linearization of the ODE (exact, symbolic)")
        print(f"  leading delta'  coefficient p0 = {p[0]}   "
              f"(cancellation is what makes A finite)")
        print(f"  leading delta   coefficient q0 = {q[0]}")
        print(f"  => S0 = -A with A = {A}")
        print(f"  => delta_sigma ~ C * s^({theta}) * exp(-{A} s)")
        print(f"  next Riccati orders: "
              f"{[sp.nsimplify(sol[unk[i]]) for i in range(1, min(4, K))]}")
    return sp.Rational(A), sp.Rational(theta)


# --------------------------------------------------------------------------
# ROUTE 2 -- large-order growth of the perturbative coefficients
# --------------------------------------------------------------------------

def route2_largeorder(path="out/sigma_recursion_fast.json", A_route1=None,
                      verbose=True):
    """Read A and beta off the large-order growth of the exact e_m.

    Two passes, kept separate on purpose:
      (a) A FREE.  A^2 = lim m^2 / r_m.  This confirms route 1 without using
          it, at whatever precision the extrapolation supports.
      (b) A IMPOSED from route 1 (exact, symbolic).  Then beta follows in
          closed form from r_m and lands to full precision.
    Pass (b) is NOT an independent check of A -- reporting it as one would be
    the L-039 circularity.  It is a high-precision read of beta GIVEN A.
    """
    mp.dps = 120
    d = json.load(open(path))
    E = {}
    for r in d["coeffs"]:
        n, dn = r["e_m"].split("/")
        E[r["m"]] = mpf(int(n)) / mpf(int(dn))
    ms = sorted(E)
    rows = [(mpf(m), E[m + 2] / E[m]) for m in ms if m + 2 in E]

    # (a) A with beta unknown: beta only enters at order 1/m, so the
    #     extrapolation absorbs it.
    A2_free = neville([(m, m**2 / r) for m, r in rows], NEVILLE_DEG)
    A_free = sqrt(A2_free)

    # (b) A imposed: (m+b)(m+b+1) = A^2 r  =>  b = (sqrt(1+4A^2 r) - 2m - 1)/2
    A = mpf(int(A_route1))
    bpts = [(m, (sqrt(1 + 4 * A**2 * r) - 2 * m - 1) / 2) for m, r in rows]
    beta = neville(bpts, NEVILLE_DEG)

    if verbose:
        print("\nROUTE 2 -- large-order growth of the exact rational e_m")
        print(f"  data: M = {d['M']}  ({len(ms)} even orders), no fit to any"
              f" digit count")
        print(f"  raw beta_m (A imposed) at the top of the range:")
        for m, b in bpts[-3:]:
            print(f"    m={int(m):4d}   {mp.nstr(b, 12)}")
        print(f"  (a) A free      : A = {mp.nstr(A_free, 18)}"
              f"   [independent of route 1]")
        print(f"  (b) A = {A} imposed: beta = {mp.nstr(beta, 25)}")
        for deg in (8, 12, 16, 20):
            print(f"        deg {deg:3d} -> {mp.nstr(neville(bpts, deg), 22)}")
    return A_free, beta, E


def neville(pts, deg):
    """Polynomial extrapolation in x = 1/m to x = 0, using the last deg+1 pts.

    Repeated application of a single 1/m-eliminating Richardson step does NOT
    accelerate past first order -- it removes the 1/m term and then keeps
    removing a term that is already gone.  Neville in 1/m removes 1/m, 1/m^2,
    ... in turn, which is what the sequence actually needs.
    """
    pts = pts[-(deg + 1):]
    xs = [1 / m for m, _ in pts]
    col = [v for _, v in pts]
    n = len(xs)
    for k in range(1, n):
        col = [(col[i + 1] * (0 - xs[i]) - col[i] * (0 - xs[i + k]))
               / (xs[i + k] - xs[i]) for i in range(n - k)]
    return col[0]


def reconcile(A_sym, theta_sym, beta, verbose=True):
    """Three exponents from one beta.  Keeping them apart is the whole point.

    With  e_m ~ K Gamma(m+beta) / A^m, the dispersion relation in w = 1/s
        e_m = (1/2 pi i) int_0^inf Disc f(w) w^(-m-1) dw
    with  Disc f(w) ~ C w^(-beta) exp(-A/w)  gives, after w = A/t,
        e_m = (C/2 pi i) A^(beta-m) Gamma(m + beta).
    So the trans-series term in LOG DET carries s^(+beta), not s^(-beta).
    (Getting that sign backwards is the first thing this script did, and it
    put theta off by exactly 1 -- logged rather than quietly corrected.)

        (i)   log det :  s^(beta)     exp(-A s)
        (ii)  sigma   :  s^(1+beta)   exp(-A s)      [sigma = s d/ds log det]
        (iii) least term of the truncated series, which is what an honest
              digit count measures:
                 m* + beta = A s, and Stirling at m* gives
                 t_m* = K sqrt(2 pi) (A s)^(beta - 1/2) exp(-A s)
              so the MEASURED exponent is a = 1/2 - beta.
    (ii) is the WKB output.  (iii) is L-050.  They differ by sqrt(s) and by
    the derivative -- three different numbers, and the reason a naive
    "check b against the measured a" comparison fails.
    """
    theta_pred = 1 + beta
    a_pred = mpf(1) / 2 - beta
    if verbose:
        print("\nRECONCILIATION")
        print(f"  beta                                  = {mp.nstr(beta, 20)}")
        print(f"  (ii)  theta = 1 + beta  (sigma)       = {mp.nstr(theta_pred, 20)}")
        print(f"        theta from WKB, route 1         = {theta_sym}")
        print(f"  (iii) a     = 1/2 - beta (least term) = {mp.nstr(a_pred, 20)}")
    return a_pred, theta_pred


def least_term_check(E, A, beta, K, verbose=True):
    """Normalization-free test: predict the ACTUAL omitted term at given s.

    This sidesteps every question about what the honest-digit count is
    normalized by.  It compares the closed-form least term against the
    smallest term of the series actually evaluated at that s.
    """
    mp.dps = 60
    ms = sorted(E)
    out = []
    for s_val in (mpf(149), mpf(200), mpf(250)):
        best, bm = None, None
        for m in ms:
            t = abs(E[m]) * s_val**(-m)
            if best is None or t < best:
                best, bm = t, m
        pred = K * sqrt(2 * pi) * (A * s_val)**(beta - mpf(1) / 2) * exp(-A * s_val)
        out.append({"s": int(s_val), "m_star": bm,
                    "least_term": mp.nstr(best, 12),
                    "predicted": mp.nstr(pred, 12),
                    "ratio": mp.nstr(best / pred, 12)})
        if verbose:
            print(f"    s={int(s_val):4d}  m*={bm:4d}  actual {mp.nstr(best,10)}"
                  f"  predicted {mp.nstr(pred,10)}  ratio {mp.nstr(best/pred,10)}")
    return out


def stokes_prefactor(E, A, beta, verbose=True):
    """K = lim e_m A^m / Gamma(m+beta).  MEASURED, NOT IDENTIFIED.

    This is the Stokes constant the linearization cannot fix -- the one
    genuinely free datum in the trans-series.  It is computed here only
    because it makes the PREFACTOR of the measured law checkable, which is
    what turns the exponent agreement into a full check of the law.

    NO PSLQ IS RUN ON IT.  Identifying K is a real mini-target and precisely
    the adjacent one that would eat a Phase 1; it is queued behind target
    selection, deliberately and on the record.
    """
    mp.dps = 60
    ms = sorted(E)
    pts = [(mpf(m), E[m] * exp(mpf(m) * log(A) - loggamma(mpf(m) + beta)))
           for m in ms]
    K = neville(pts, NEVILLE_DEG)
    C = K * sqrt(2 * pi) * A**(beta - mpf(1) / 2)
    if verbose:
        print("\nSTOKES PREFACTOR (measured, not identified)")
        print(f"  K = lim e_m A^m / Gamma(m+beta) = {mp.nstr(K, 20)}")
        print(f"  stability: deg 8 -> {mp.nstr(neville(pts, 8), 15)}, "
              f"deg 20 -> {mp.nstr(neville(pts, 20), 15)}")
        print(f"  => C in  C * s^(1/2-beta) * exp(-A s):  {mp.nstr(C, 20)}")
        print("  NOT submitted to PSLQ: queued behind Phase 1 target selection.")
        # C landed on a value recognisable BY INSPECTION.  Reporting the
        # digits of agreement with the single obvious candidate is not a
        # search and does not consume the Phase 1 budget; it also cannot be
        # suppressed honestly once seen.  One candidate, declared here, no
        # basis, no PSLQ.  The identification stays CONJECTURED: 1/pi is the
        # most prior-heavy constant available and a one-term match against it
        # is weak evidence per digit compared with a vetted PSLQ relation.
        cand = 1 / pi
        print(f"\n  agreement with the single declared candidate 1/pi:")
        for deg in (12, 28, 44, 52):
            Kd = neville(pts, deg)
            Cd = Kd * sqrt(2 * pi) * A**(beta - mpf(1) / 2)
            err = abs(Cd - cand)
            print(f"    deg {deg:3d} -> {mp.nstr(-log(err)/log(10), 6)} digits")
        print("  Monotone in the extrapolation degree, so the limit is the")
        print("  extrapolator, not a discrepancy.  Tag: CONJECTURED.")
    return K, C


def main():
    A_sym, theta_sym = route1_wkb()
    A_free, beta, E = route2_largeorder(A_route1=A_sym)
    a_pred, theta_pred = reconcile(A_sym, theta_sym, beta)
    K, C = stokes_prefactor(E, mpf(int(A_sym)), beta)
    print("\n  normalization-free check of the prefactor:")
    lt = least_term_check(E, mpf(int(A_sym)), beta, K)

    print("\nCROSS-CHECKS")
    dA = abs(A_free - mpf(int(A_sym)))
    print(f"  A     : symbolic {A_sym} vs large-order {mp.nstr(A_free, 18)}"
          f"   |diff| = {mp.nstr(dA, 6)}")
    dth = abs(mpf(sp.Rational(theta_sym)) - theta_pred)
    print(f"  theta : WKB {theta_sym} vs 1+beta {mp.nstr(theta_pred, 18)}"
          f"   |diff| = {mp.nstr(dth, 6)}")
    dhalf = abs(beta + mpf(1) / 2)
    print(f"  beta  : |beta - (-1/2)| = {mp.nstr(dhalf, 6)}"
          f"   (declared tolerance {mp.nstr(BETA_TOL, 3)})")

    ok = dth < mpf("1e-15") and dhalf < BETA_TOL
    print(f"\n  => a (the L-050 exponent) DERIVED from the ODE = "
          f"{mp.nstr(a_pred, 18)}")
    print("     L-050 measured it as 0.9941 (s>=60) -> 0.9964 (s>=140),")
    print("     converging monotonically.  Derivation and measurement were")
    print("     produced by disjoint code paths.")
    print(f"\n  verdict: {'CONSISTENT' if ok else 'MISMATCH -- do not report'}")

    out = {
        "A_symbolic": str(A_sym),
        "theta_symbolic": str(theta_sym),
        "A_largeorder_free": mp.nstr(A_free, 20),
        "beta": mp.nstr(beta, 25),
        "theta_from_beta": mp.nstr(theta_pred, 20),
        "a_derived": mp.nstr(a_pred, 20),
        "K_stokes": mp.nstr(K, 20),
        "C_prefactor": mp.nstr(C, 20),
        "A_agreement": mp.nstr(dA, 6),
        "theta_agreement": mp.nstr(dth, 6),
        "beta_from_half": mp.nstr(dhalf, 6),
        "least_term_check": lt,
        "consistent": bool(ok),
        "C_minus_inv_pi": mp.nstr(abs(C - 1 / pi), 6),
        "C_candidate": "1/pi  (CONJECTURED: inspection, one candidate, no PSLQ)",
        "note": "a_derived comes from the ODE alone; it is NOT fitted to the "
                "honest-digit counts of L-050.",
    }
    os.makedirs("out", exist_ok=True)
    json.dump(out, open("out/trans_series.json", "w"), indent=2)
    print("\n[out] out/trans_series.json")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
