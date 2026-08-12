"""Generate the asymptotic tail of log det(I - K_s) exactly, by recursion.

Uses ONLY the ODE discovered in sigma_ode.py and verified out of sample in
sigma_ode_verify.py:

    s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2 = 0,   u = s sigma' - sigma,
    sigma(s) = s d/ds log det(I - K_s).

WHY THIS MATTERS (operator, this session): fit_constant.py currently spends
K Richardson orders annihilating this tail numerically, and that annihilation
is the E1 budget line.  Coefficients obtained here are exact rationals, so
the tail becomes a subtraction rather than a fit.

WHAT IT CANNOT DO: the constant c is an integration constant of the ODE and
is invisible to this recursion -- sigma = s (log det)' kills it.  That is the
structural reason the constant needed a separate 30-year proof, and it is
also why this module can never be circular about c.  It supplies the tail
and says nothing whatsoever about the constant.

Ansatz, with NO parity assumed:

    sigma(s) = -s^2 - 1/4 + sum_{m>=1} a_m s^-m

If the odd a_m come out identically zero, the even-only model that
fit_constant.py assumes on numerical evidence (L-029) becomes a derived
consequence rather than a fitted one.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def _mul(A, B, lo_a, lo_b, n):
    """Truncated series product.  A,B are coefficient lists from x^lo."""
    out = [sp.Integer(0)] * n
    for i, ai in enumerate(A):
        if ai == 0:
            continue
        for j, bj in enumerate(B):
            if bj == 0:
                continue
            k = i + j
            if k < n:
                out[k] += ai * bj
    return out, lo_a + lo_b


def _align(A, lo_a, lo_target, n):
    """Shift a series to a common lowest exponent."""
    shift = lo_a - lo_target
    out = [sp.Integer(0)] * n
    for i, a in enumerate(A):
        if 0 <= i + shift < n:
            out[i + shift] = a
    return out


def build(M: int):
    """Solve for a_1..a_M.  Returns (a_values, odd_all_zero)."""
    x = sp.symbols("x")  # x = 1/s
    N = M + 12           # series length, with headroom

    a = [sp.Symbol(f"a{m}") for m in range(M + 1)]

    # sigma as a series in x starting at x^-2
    LO = -2
    sig = [sp.Integer(0)] * N
    sig[0] = sp.Integer(-1)                 # -s^2
    sig[2] = sp.Rational(-1, 4)             # -1/4
    for m in range(1, M + 1):
        sig[2 + m] = a[m]                   # a_m s^-m

    # d/ds = -x^2 d/dx.  If f = sum f_j x^j then (df/ds)_k = -(k-1) f_{k-1}
    def dds(F, lo):
        out = [sp.Integer(0)] * N
        for i in range(N):
            j = lo + i           # exponent of source term
            k = j + 1            # exponent of result term
            idx = i + 1          # position in result list (same lo+1 base)
            if idx < N:
                out[idx] = -sp.Integer(j) * F[i]
        # result lowest exponent is lo+1, but out is indexed from lo+1-1... align:
        res = [sp.Integer(0)] * N
        for i in range(N):
            if i + 1 < N:
                res[i] = out[i + 1]
        return res, lo + 1

    sig1, lo1 = dds(sig, LO)          # sigma'  starts at x^-1
    sig2, lo2 = dds(sig1, lo1)        # sigma'' starts at x^0

    # u = s sigma' - sigma = x^-1 sigma' - sigma
    u_a = sig1[:]                      # exponent base lo1 - 1 = -2
    u = [u_a[i] - sig[i] for i in range(N)]
    lo_u = -2

    s2sig2sq, lo_a1 = _mul(sig2, sig2, lo2, lo2, N)   # sigma''^2 at x^0
    lo_a1 -= 2                                        # times s^2 = x^-2
    u2, lo_u2 = _mul(u, u, lo_u, lo_u, N)
    sig1sq, lo_s1s = _mul(sig1, sig1, lo1, lo1, N)
    usig1sq, lo_us = _mul(u, sig1sq, lo_u, lo_s1s, N)

    LOR = min(lo_a1, lo_u2, lo_us)
    T1 = _align(s2sig2sq, lo_a1, LOR, N)
    T2 = _align(u2, lo_u2, LOR, N)
    T3 = _align(usig1sq, lo_us, LOR, N)
    R = [sp.expand(T1[i] + 16 * T2[i] + 4 * T3[i]) for i in range(N)]

    print(f"[series] R starts at x^{LOR}; first two coeffs "
          f"{sp.simplify(R[0])}, {sp.simplify(R[1])}")

    # Rather than assume which R-coefficient introduces a_m (my first guess
    # was off by one and the code correctly refused to proceed), scan the
    # coefficients in order and pick up whichever unknown is newly present.
    sol = {}
    pending = [a[m] for m in range(1, M + 1)]
    for idx in range(N):
        if not pending:
            break
        eq = sp.expand(R[idx].subs(sol))
        if eq == 0:
            continue
        present = [t for t in pending if eq.has(t)]
        if not present:
            raise RuntimeError(
                f"R[{idx}] (x^{LOR + idx}) is nonzero but contains no unknown: "
                f"the ansatz is inconsistent with the ODE")
        if len(present) > 1:
            raise RuntimeError(
                f"R[{idx}] introduces {len(present)} unknowns at once "
                f"({present}); recursion is not triangular")
        unk = present[0]
        roots = sp.solve(sp.Eq(eq, 0), unk, dict=True)
        roots = [r for r in roots if unk in r]
        if len(roots) != 1:
            raise RuntimeError(
                f"order {unk}: {len(roots)} solutions at x^{LOR + idx}, "
                f"expected exactly 1 -- branch ambiguity, do not guess")
        sol[unk] = sp.simplify(sp.together(roots[0][unk]).subs(sol))
        pending.remove(unk)
    if pending:
        raise RuntimeError(f"unresolved after {N} orders: {pending}")
    return [sol[a[m]] for m in range(1, M + 1)]


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    vals = build(M)

    print("\n  m      a_m  (coefficient of s^-m in sigma)        e_m in log det")
    out = []
    odd_zero = True
    for m, v in enumerate(vals, start=1):
        # sigma = s (log det)'  =>  a_m s^-m  <=>  e_m s^-m in log det with
        # a_m = -m e_m, so e_m = -a_m/m.
        e = sp.Rational(-1, m) * v if v != 0 else sp.Integer(0)
        e = sp.simplify(e)
        if m % 2 == 1 and v != 0:
            odd_zero = False
        print(f"{m:>3}  {str(v):>36}   {str(e)}")
        out.append({"m": m, "a_m": str(v), "e_m": str(e)})

    print(f"\n[parity] all odd a_m vanish: {odd_zero}")
    with open("out/sigma_recursion.json", "w") as fh:
        json.dump({"M": M, "odd_all_zero": bool(odd_zero), "coeffs": out},
                  fh, indent=2)
    print("[out] out/sigma_recursion.json")


if __name__ == "__main__":
    main()
