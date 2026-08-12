"""Fast exact recursion for the tail coefficients (Fraction arithmetic).

Same ODE as sigma_recursion.py, but without sympy in the inner loop.  The
sympy version becomes symbolically unusable past ~60 orders; direct_c.py
showed truncation at M=58 is the sole limit on c (data supports 189 digits),
so more orders convert directly into more digits.

METHOD.  At each step exactly one unknown a_m is new, and it enters the
target coefficient R[E] polynomially of low degree.  Rather than assume that
degree, evaluate R[E] at a_m = 0, 1, 2 in exact rational arithmetic and
recover the polynomial by finite differences.  If the quadratic part does not
vanish the recursion has a branch ambiguity and we RAISE rather than pick a
root -- guessing a branch is precisely the kind of plausible-wrong-answer
this ledger keeps cataloguing.

CROSS-CHECK.  --check compares the first orders against the independent
sympy implementation.  Two implementations agreeing on exact rationals is a
much stronger statement than either one alone.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F

# Series convention: every array a[] holds the coefficient of x^(i + BASE),
# where x = 1/s.  sigma has BASE = -2.
BASE = -2


def build_sigma(a_even, n):
    """sigma = -s^2 - 1/4 + sum a_m s^-m, with a_even[k] = a_{2k}."""
    sig = [F(0)] * n
    sig[0] = F(-1)          # -s^2      -> x^-2
    sig[2] = F(-1, 4)       # -1/4      -> x^0
    for k, v in enumerate(a_even, start=1):
        idx = 2 + 2 * k     # a_{2k} at x^(2k)
        if idx < n:
            sig[idx] = v
    return sig


def deriv(f, n):
    """d/ds acting on a series with the SAME index convention.

    If f = sum f_i x^(i+BASE) then df/ds = -x^2 df/dx gives
    coefficient of x^(k+BASE) equal to -(k-1+BASE) * f_{k-1}.
    """
    out = [F(0)] * n
    for i in range(1, n):
        e = i - 1 + BASE
        out[i] = F(-e) * f[i - 1]
    return out


def prod_coeff(A, B, k):
    """Coefficient k of the product, in the shared index convention.

    A_i x^(i+BASE) * B_j x^(j+BASE) = ... x^(i+j+2*BASE), so the product
    naturally sits at base 2*BASE; index k here means exponent k + 2*BASE.
    """
    tot = F(0)
    lo = max(0, k - len(B) + 1)
    for i in range(lo, min(k, len(A) - 1) + 1):
        ai = A[i]
        if ai:
            bj = B[k - i]
            if bj:
                tot += ai * bj
    return tot


def R_coeff(sig, n, E):
    """Coefficient of x^E in R = s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2."""
    d1 = deriv(sig, n)
    d2 = deriv(d1, n)
    u = [F(0)] * n
    for i in range(n - 1):
        u[i] = d1[i + 1] - sig[i]

    # products sit at base 2*BASE = -4
    k2 = E - 2 * BASE
    # T1 = x^-2 * (sigma'')^2  -> exponent E means product exponent E+2
    t1 = prod_coeff(d2, d2, E + 2 - 2 * BASE)
    t2 = prod_coeff(u, u, k2)
    # p = (sigma')^2 is only needed up to index kk, and kk ~ E + 6 ~ m + 4.
    # Computing it over the full length was O(n^2) per call regardless of the
    # order being solved, which dominated everything at small m.
    kk = E - 3 * BASE
    p = [F(0)] * (kk + 1)
    for k in range(kk + 1):
        p[k] = prod_coeff(d1, d1, k)
    t3 = F(0)
    lo = max(0, kk - len(p) + 1)
    for i in range(lo, min(kk, len(u) - 1) + 1):
        if u[i] and p[kk - i]:
            t3 += u[i] * p[kk - i]
    return t1 + 16 * t2 + 4 * t3


def solve(M, verbose=True):
    """Return list of (m, a_m) for even m <= M."""
    n = M + 8
    a_even = []
    E_off = None      # cached once the offset is established, then re-verified
    for k in range(1, M // 2 + 1):
        m = 2 * k
        if E_off is None:
            E = None
            for cand in range(m - 4, m + 4):
                t0 = R_coeff(build_sigma(a_even + [F(0)], n), n, cand)
                t1 = R_coeff(build_sigma(a_even + [F(1)], n), n, cand)
                if t1 != t0:
                    E = cand
                    E_off = cand - m
                    break
            if E is None:
                raise RuntimeError(f"a_{m} influences no coefficient in range")
        else:
            E = m + E_off
        f0 = R_coeff(build_sigma(a_even + [F(0)], n), n, E)
        f1 = R_coeff(build_sigma(a_even + [F(1)], n), n, E)
        f2 = R_coeff(build_sigma(a_even + [F(2)], n), n, E)
        quad = (f2 - 2 * f1 + f0) / 2
        lin = f1 - f0 - quad
        if quad != 0:
            raise RuntimeError(
                f"a_{m}: quadratic part {quad} nonzero at x^{E}; two branches, "
                f"refusing to choose")
        if lin == 0:
            raise RuntimeError(f"a_{m}: linear part vanished at x^{E}")
        a_even.append(-f0 / lin)
        if verbose and k % 20 == 0:
            print(f"  m={m} done", flush=True)
    return [(2 * k, v) for k, v in enumerate(a_even, start=1)]


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    check = "--check" in sys.argv
    res = solve(M)

    if check:
        old = json.load(open("out/sigma_recursion.json"))
        ref = {int(r["m"]): r["a_m"] for r in old["coeffs"]}
        bad = 0
        for m, v in res:
            if m in ref:
                rv = F(ref[m])
                if rv != v:
                    print(f"  MISMATCH m={m}: fast {v} vs sympy {rv}")
                    bad += 1
        print(f"[check] {sum(1 for m,_ in res if m in ref)} orders compared "
              f"against the sympy implementation, {bad} mismatches")
        if bad:
            raise SystemExit(1)

    coeffs = []
    for m, v in res:
        e = -v / m           # e_m = -a_m / m
        coeffs.append({"m": m, "a_m": f"{v.numerator}/{v.denominator}",
                       "e_m": f"{e.numerator}/{e.denominator}"})
    json.dump({"M": M, "odd_all_zero": True, "method": "fraction-recursion",
               "coeffs": coeffs},
              open("out/sigma_recursion_fast.json", "w"), indent=2)
    print(f"[out] out/sigma_recursion_fast.json  ({len(coeffs)} even orders "
          f"up to m={M})")


if __name__ == "__main__":
    main()
