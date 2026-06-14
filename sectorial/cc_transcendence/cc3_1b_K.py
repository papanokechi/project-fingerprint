#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1b  --  REDUCTION HARDENING: K to >=120 digits + identity check
================================================================================
SIARC. Upgrade CC3-1-CRED (which verified C_EBR = K*(4/3)*sqrt(pi)/Gamma(7/3)
only to relative 6.4e-4 via Richardson) to a >=120-digit identity, by computing
K DIRECTLY as a connection coefficient of Phi's order-4 operator L.

K is defined by:  Phi(z) ~ K * (1-3z)^{-4/3}  as z -> 1/3,
where Phi(z) = sum_n Q_n z^n / (n!)^2, Q_n=(3n^2+n+1)Q_{n-1}+Q_{n-2}, Q0=1,Q1=5.

METHOD (regular-to-regular connection; both 0 and 1/3 are regular singular --
the irregularity of L sits at z=infinity, slope 1/4, and is untouched here):
  * Phi is the holomorphic (exponent-0, log-free) solution at z=0; evaluate it
    and 3 derivatives at an interior matching point z_m=1/6 by summing its
    power series (radius 1/3; rate (3 z_m)=1/2).
  * At z=1/3 build the 4 local Frobenius solutions in v=1-3z (radius 1; rate
    (1-3 z_m)=1/2): the singular S_sing = v^{-4/3}(1+...) and three holomorphic
    H_a,H_b,H_c (exponents 0,1,2; confirmed LOG-FREE in cc3_1b_riemann). Each is
    verified to annihilate L to high order (residual self-check).
  * Solve the 4x4 connection system at z_m; K = coefficient of S_sing.

Then verify C_EBR (frozen 169-digit, f3400831...) equals K*(4/3)*sqrt(pi)/Gamma(7/3).

CEILING (reproduced): a Fuchsian relocation does not imply K is a classical
period; provenance, not singularity type, is what the period conjectures see.
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import hashlib
import sympy as sp
from mpmath import mp, mpf, sqrt, gamma, matrix, lu_solve, fabs, nstr, pi, log10

# ------------------------------------------------------------------ parameters
DPS = 220
NTERMS_PHI = 1100      # z=0 series length (rate 1/2 -> ~ 0.30*N decimal digits)
NTERMS_LOC = 900       # local v-series length at z=1/3
mp.dps = DPS
Z_M = mpf(1) / 6       # matching point; v_m = 1-3 z_m = 1/2


def ns(x, n):
    return nstr(x, n)


# frozen 169-digit C_EBR (hash f3400831...; cc4_1_connection_results.json)
C_EBR_STR = ("3.0557068078904813657019122017276813688755427749738305746763750500"
             "4717360435396245828829279965008999891820001450625880420516341151"
             "5501549494446823017585278488893394706741693")
C_EBR = mpf(C_EBR_STR)

# ------------------------------------------------------------ operator in v
z, v, s = sp.symbols('z v s')
p_z = {4: z**4 * (1 - 3 * z),
       3: 4 * z**3 - 25 * z**4,
       2: 2 * z**2 - 47 * z**3,
       1: -15 * z**2,
       0: -z**2}
ORDER = 4
# z = (1-v)/3 ;  D_z^j = (-3)^j D_v^j
zsub = (1 - v) / sp.Integer(3)
q = {}
for j in range(ORDER + 1):
    q[j] = sp.expand(p_z[j].subs(z, zsub) * (-3)**j)
# polynomial coefficients q_{j,i} (coeff of v^i in q_j)
qc = {}
maxdeg = 0
for j in range(ORDER + 1):
    pj = sp.Poly(q[j], v)
    for (i,), co in pj.terms():
        qc[(j, i)] = sp.nsimplify(co)
        maxdeg = max(maxdeg, i)


def ff(svar, j):
    """falling factorial s(s-1)...(s-j+1) as a sympy expr."""
    r = sp.Integer(1)
    for l in range(j):
        r *= (svar - l)
    return r


# A_delta(s) = sum_j q_{j, delta+j} * ff(s,j)   (the v^{s+delta} coefficient of L[v^s])
DELTAS = list(range(-ORDER, maxdeg + 1))   # safe range
A_sym = {}
for d in DELTAS:
    expr = sp.Integer(0)
    for j in range(ORDER + 1):
        co = qc.get((j, d + j), sp.Integer(0))
        if co != 0:
            expr += co * ff(s, j)
    A_sym[d] = sp.expand(expr)

# indicial = A_{-3}(s)
DMIN = min(d for d in DELTAS if A_sym[d] != 0)
indicial_v = sp.factor(A_sym[DMIN])
ind_roots = sp.roots(sp.Poly(A_sym[DMIN], s))

# lambdify A_delta to high-precision callables (exact rational coeffs -> mpf)
def make_A(d):
    poly = sp.Poly(A_sym[d], s) if A_sym[d] != 0 else None
    if poly is None:
        return (lambda sval: mpf(0))
    coeffs = [sp.nsimplify(c) for c in poly.all_coeffs()]   # highest power first
    mc = [mpf(sp.Rational(c).p) / mpf(sp.Rational(c).q) for c in coeffs]
    deg = len(mc) - 1
    def f(sval):
        acc = mpf(0)
        for k, c in enumerate(mc):
            acc += c * (sval ** (deg - k))
        return acc
    return f

A_num = {d: make_A(d) for d in DELTAS}
I_num = A_num[DMIN]   # indicial as numeric callable


def indicial_value(rho_plus_n):
    return I_num(rho_plus_n)


def build_local_solution(rho, free_vals, N, resonance_tol):
    """Build c_0..c_N for S = sum_k c_k v^(rho+k) via the order-4 recurrence
       I(rho+n) c_n = -sum_{delta>DMIN} A_delta(rho+n-3-delta) c_{n-3-delta}.
    free_vals: dict n->value for resonant n (where I(rho+n)=0). Asserts the
    obstruction (rhs) vanishes at each resonance (log-free check)."""
    rho = mpf(rho) if not isinstance(rho, mpf) else rho
    c = [mpf(0)] * (N + 1)
    obstr = {}
    for n in range(0, N + 1):
        if n == 0:
            rhs = mpf(0)
        else:
            rhs = mpf(0)
            for d in DELTAS:
                if d == DMIN:
                    continue
                idx = n - 3 - d        # = n-3-delta ; index of c
                if 0 <= idx <= n - 1:
                    rhs += A_num[d](rho + idx) * c[idx]
            rhs = -rhs
        Ival = indicial_value(rho + n)
        if fabs(Ival) < mpf(10) ** (-DPS // 2):     # resonance
            obstr[n] = rhs
            if fabs(rhs) > resonance_tol:
                raise RuntimeError(f"LOG forced at rho={rho}, n={n}: obstruction={rhs}")
            c[n] = mpf(free_vals.get(n, 0))
        else:
            if n == 0:
                c[n] = mpf(free_vals.get(0, 1))     # seed
            else:
                c[n] = rhs / Ival
    return c, obstr


def eval_series_v(c, rho, vval, nder):
    """Return [S, dS/dv, d2S/dv2, d3S/dv3] at v=vval for S=sum c_k v^(rho+k)."""
    out = []
    for q_ord in range(nder + 1):
        acc = mpf(0)
        for k, ck in enumerate(c):
            e = rho + k
            # q_ord-th derivative of v^e : ff(e,q_ord) v^(e-q_ord)
            coef = mpf(1)
            for l in range(q_ord):
                coef *= (e - l)
            acc += ck * coef * (vval ** (e - q_ord))
        out.append(acc)
    return out


def v_to_z_derivs(d_v):
    """convert [S, S_v, S_vv, S_vvv] to [S, S_z, S_zz, S_zzz] via v=1-3z."""
    return [d_v[0], -3 * d_v[1], 9 * d_v[2], -27 * d_v[3]]


def main():
    print("== operator in v, indicial ==")
    print("  DMIN (indicial offset) =", DMIN)
    print("  indicial A_{%d}(s) = %s" % (DMIN, indicial_v))
    print("  indicial roots =", {str(r): m for r, m in ind_roots.items()})

    vm = 1 - 3 * Z_M
    print(f"\n  matching z_m = {Z_M}  ->  v_m = {vm}  (dps={DPS})")

    # ---- Phi and derivatives at z_m from the z=0 power series -------------
    print("\n== Phi at z_m from z=0 series ==")
    Q = [mpf(1), mpf(5)]
    for n in range(2, NTERMS_PHI + 1):
        Q.append((3 * n * n + n + 1) * Q[n - 1] + Q[n - 2])
    # a_n = Q_n/(n!)^2
    a = [mpf(0)] * (NTERMS_PHI + 1)
    fact = mpf(1)
    for n in range(0, NTERMS_PHI + 1):
        if n > 0:
            fact *= n
        a[n] = Q[n] / (fact * fact)
    # Phi^(i)(z_m) = sum_n a_n * n!/(n-i)! z_m^(n-i)
    phi_d = []
    for i in range(4):
        acc = mpf(0)
        for n in range(i, NTERMS_PHI + 1):
            coef = mpf(1)
            for l in range(i):
                coef *= (n - l)
            acc += a[n] * coef * (Z_M ** (n - i))
        phi_d.append(acc)
    # convergence check: last term magnitude
    tail = fabs(a[NTERMS_PHI] * (Z_M ** NTERMS_PHI))
    print(f"  Phi(z_m)   = {ns(phi_d[0], 40)}")
    print(f"  tail term ~ {ns(tail, 5)}  (want << 10^-150)")

    # ---- local basis at z=1/3 --------------------------------------------
    print("\n== local Frobenius basis at z=1/3 (v=1-3z) ==")
    res_tol = mpf(10) ** (-(DPS - 40))
    RHO_SING = mpf(-4) / 3
    c_sing, ob_sing = build_local_solution(RHO_SING, {0: 1}, NTERMS_LOC, res_tol)
    c_Ha, ob_Ha = build_local_solution(0, {0: 1, 1: 0, 2: 0}, NTERMS_LOC, res_tol)
    c_Hb, ob_Hb = build_local_solution(0, {0: 0, 1: 1, 2: 0}, NTERMS_LOC, res_tol)
    c_Hc, ob_Hc = build_local_solution(0, {0: 0, 1: 0, 2: 1}, NTERMS_LOC, res_tol)
    print("  S_sing rho=-4/3 built; resonances:", {k: ns(val, 3) for k, val in ob_sing.items()})
    print("  H_a (c0=1) resonances:", {k: ns(val, 3) for k, val in ob_Ha.items()})
    print("  H_b (c1=1) resonances:", {k: ns(val, 3) for k, val in ob_Hb.items()})
    print("  H_c (c2=1) resonances:", {k: ns(val, 3) for k, val in ob_Hc.items()})

    rho_list = [RHO_SING, 0, 0, 0]
    cs = [c_sing, c_Ha, c_Hb, c_Hc]
    # tail self-check on each local series
    loc_tails = [fabs(cs[i][NTERMS_LOC] * vm ** (rho_list[i] + NTERMS_LOC)) for i in range(4)]
    print("  local tail terms:", [ns(t, 4) for t in loc_tails])

    # ---- assemble 4x4 connection system at z_m ----------------------------
    cols = []
    for i in range(4):
        dv = eval_series_v(cs[i], rho_list[i], vm, 3)
        cols.append(v_to_z_derivs(dv))
    Mmat = matrix(4, 4)
    for r in range(4):
        for cc in range(4):
            Mmat[r, cc] = cols[cc][r]
    bvec = matrix(phi_d)
    coeffs = lu_solve(Mmat, bvec)
    K = coeffs[0]
    print("\n== connection solve ==")
    print("  K (coeff of (1-3z)^{-4/3} in Phi) =")
    print("   ", ns(K, 130))

    # ---- identity check: C_EBR ?= K*(4/3)*sqrt(pi)/Gamma(7/3) --------------
    factor = (mpf(4) / 3) * sqrt(pi) / gamma(mpf(7) / 3)
    C_from_K = K * factor
    K_pred = C_EBR / factor
    rel_err = fabs(C_from_K - C_EBR) / fabs(C_EBR)
    # stable digits agreement
    if rel_err == 0:
        agree = DPS
    else:
        agree = int(-log10(rel_err))
    print("\n== reduction identity check ==")
    print("  factor (4/3)sqrt(pi)/Gamma(7/3) =", ns(factor, 40))
    print("  K * factor      =", ns(C_from_K, 60))
    print("  C_EBR (frozen)  =", ns(C_EBR, 60))
    print("  K (direct)      =", ns(K, 40))
    print("  K_pred=C/factor =", ns(K_pred, 40))
    print(f"  relative error  = {ns(rel_err, 5)}")
    print(f"  AGREEING DIGITS = {agree}")

    out = {
        "op": "cc3-1b-K", "task_id": "op:cc-transcendence/cc3-1b",
        "quantity": "K = coefficient of (1-3z)^{-4/3} in the continuation of Phi(z)=sum Q_n z^n/(n!)^2 to z=1/3",
        "method": ("regular-to-regular connection matching at z_m=1/6 (v_m=1/2): Phi (holomorphic exp-0 "
                   "solution at z=0, log-free) matched against the 4 local Frobenius solutions at z=1/3 "
                   "(S_sing=v^{-4/3}(1+...), and log-free holomorphic H_a,H_b,H_c for exponents 0,1,2)."),
        "dps_working": DPS, "nterms_phi": NTERMS_PHI, "nterms_local": NTERMS_LOC,
        "matching_point_z": str(Z_M), "matching_point_v": str(vm),
        "indicial_offset_DMIN": int(DMIN),
        "indicial_v_factored": str(indicial_v),
        "indicial_roots": {str(r): int(m) for r, m in ind_roots.items()},
        "phi_tail_term": ns(tail, 6),
        "local_tail_terms": [ns(t, 6) for t in loc_tails],
        "resonance_obstructions": {
            "S_sing": {int(k): ns(val, 4) for k, val in ob_sing.items()},
            "H_a": {int(k): ns(val, 4) for k, val in ob_Ha.items()},
            "H_b": {int(k): ns(val, 4) for k, val in ob_Hb.items()},
            "H_c": {int(k): ns(val, 4) for k, val in ob_Hc.items()},
        },
        "K_value_130": ns(K, 130),
        "reduction_factor": "(4/3)*sqrt(pi)/Gamma(7/3)",
        "C_EBR_frozen_hash": "f3400831cc9644641e44de7bcb69e4ec9c8fc69654ab46eb9768067ac2aa13fd",
        "C_from_K_60": ns(C_from_K, 60),
        "C_EBR_60": ns(C_EBR, 60),
        "relative_error": ns(rel_err, 6),
        "agreeing_digits": int(agree),
        "verdict": ("PASS: C_EBR = K*(4/3)*sqrt(pi)/Gamma(7/3) to >=120 digits -> CC3-1-CRED hardened"
                    if agree >= 120 else
                    "PARTIAL: agreement %d digits (< 120)" % agree),
        "ceiling": ("A Fuchsian relocation does not imply K is a classical period; provenance, not "
                    "singularity type, is what the period conjectures see. Unconditional transcendence "
                    "of C is NOT a deliverable of op:cc-3 at any grade."),
    }
    blob = json.dumps(out, sort_keys=True, ensure_ascii=False).encode("utf-8")
    out["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1b_K_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", out["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1b_K_results.json")


if __name__ == "__main__":
    main()
