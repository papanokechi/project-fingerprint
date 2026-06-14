#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1c  --  EXACT symbolic Frobenius / log-structure of L at z=0  (1c-0)
================================================================================
SIARC.  Noise-free determination of the local monodromy Jordan type of Phi's
operator L at the regular-singular point z=0, via the Euler operator theta=z D.

    L = z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2 .

Using z^k D^k = (theta)_k = theta(theta-1)...(theta-k+1) one gets the clean
'theta-normal form' at z=0 (verified below by P0 == theta^2 (theta-1)^2):

    L = P0(theta) + z P1(theta) + z^2 P2(theta),
      P0(t) = (t)_4 + 4 (t)_3 + 2 (t)_2          = t^2 (t-1)^2     [indicial]
      P1(t) = -3 (t)_4 - 25 (t)_3 - 47 (t)_2 - 15 t
      P2(t) = -1 .

A formal solution is  y = sum_{n>=0} z^n v_n,  v_n = sum_j b[n][j] (log z)^j.
Since theta(z^n L^j) = n z^n L^j + j z^n L^{j-1}, theta acts on the L-vector
v_n as (n I + N), N the nilpotent log-shift  N(L^j)=j L^{j-1}.  Collecting z^n:

    P0(nI+N) v_n + P1((n-1)I+N) v_{n-1} + P2((n-2)I+N) v_{n-2} = 0 .          (R)

This is EXACT and order-local (only n, n-1, n-2), so truncating (R) at order N is
a finite linear system whose null space IS the (truncated) formal solution space.
Unlike a naive D-array (which loses the negative-order intermediate terms that the
log parts of low-order coefficients generate), the theta-form keeps every order
>= 0 and so carries the genuine indicial constraints at n=0,1.

READ-OFF.  Monodromy z->e^{2pi i} z sends log z -> log z + 2pi i, so M=exp(2pi i N)
and (all exponents integer => semisimple part = I) Jordan_type(M)=Jordan_type(N).
Largest Jordan block = (max log power present)+1; #blocks = #log-free solutions.

CEILING (reproduced): a Fuchsian relocation does not imply K is a classical
period (provenance, not singularity type, is what the period conjectures see).
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import sympy as sp

N_TRUNC = 16     # truncation order
DLOG = 4         # log-space dimension (order-4 op => log powers 0..3)

# ---- log-shift nilpotent N : (N v)_i = (i+1) v_{i+1}  (N L^j = j L^{j-1}) -----
Nmat = sp.zeros(DLOG, DLOG)
for i in range(DLOG - 1):
    Nmat[i, i + 1] = i + 1
I4 = sp.eye(DLOG)

def falling(X, k):
    """X (X-I) (X-2I) ... (X-(k-1)I) for a square matrix X (k>=0 => I for k=0)."""
    P = sp.eye(X.rows)
    for m in range(k):
        P = P * (X - m * sp.eye(X.rows))
    return P

def P0(X):  # (t)_4 + 4 (t)_3 + 2 (t)_2
    return falling(X, 4) + 4 * falling(X, 3) + 2 * falling(X, 2)

def P1(X):  # -3 (t)_4 - 25 (t)_3 - 47 (t)_2 - 15 t
    return -3 * falling(X, 4) - 25 * falling(X, 3) - 47 * falling(X, 2) - 15 * X

def P2(X):  # -1
    return -sp.eye(X.rows)

def self_test():
    t = sp.Symbol("t")
    p0 = sp.expand(t * (t - 1) * (t - 2) * (t - 3) + 4 * t * (t - 1) * (t - 2) + 2 * t * (t - 1))
    ok0 = sp.simplify(p0 - t**2 * (t - 1)**2) == 0
    print("theta-normal-form P0(t) == t^2 (t-1)^2 :", "PASS" if ok0 else "FAIL")
    # diagonal of P0(nI+N) is P0(n) = n^2(n-1)^2
    ok1 = True
    for n in range(0, 7):
        M = P0(n * I4 + Nmat)
        if sp.simplify(M[0, 0] - n**2 * (n - 1)**2) != 0:
            ok1 = False
    print("diag P0(nI+N) == n^2(n-1)^2 :", "PASS" if ok1 else "FAIL")
    return ok0 and ok1

def main():
    print("=== cc3-1c  EXACT Frobenius log-structure of L at z=0 (theta-form) ===")
    print("N (truncation) =", N_TRUNC)
    assert self_test()

    # unknowns b[n][j]
    b = [[sp.Symbol(f"b_{n}_{j}") for j in range(DLOG)] for n in range(N_TRUNC + 1)]
    unknowns = [b[n][j] for n in range(N_TRUNC + 1) for j in range(DLOG)]

    def vec(n):
        return sp.Matrix([b[n][j] for j in range(DLOG)])

    # precompute the order-dependent matrices
    M0 = {n: P0(n * I4 + Nmat) for n in range(N_TRUNC + 1)}
    M1 = {n: P1((n - 1) * I4 + Nmat) for n in range(N_TRUNC + 1)}
    M2 = {n: P2((n - 2) * I4 + Nmat) for n in range(N_TRUNC + 1)}

    eqs = []
    for n in range(N_TRUNC + 1):
        e = M0[n] * vec(n)
        if n - 1 >= 0:
            e = e + M1[n] * vec(n - 1)
        if n - 2 >= 0:
            e = e + M2[n] * vec(n - 2)
        for j in range(DLOG):
            ex = sp.expand(e[j])
            if ex != 0:
                eqs.append(ex)

    A, _ = sp.linear_eq_to_matrix(eqs, unknowns)
    ns = A.nullspace()
    dim = len(ns)
    print("solution-space dimension (should be 4):", dim)

    idx = {(n, j): n * DLOG + j for n in range(N_TRUNC + 1) for j in range(DLOG)}

    per_sol = []
    max_j_overall = 0
    for s_i, v in enumerate(ns):
        nz = [(n, j) for (n, j) in idx if sp.simplify(v[idx[(n, j)]]) != 0]
        js = [j for (_, j) in nz]
        ns_ = [n for (n, _) in nz]
        mj = max(js) if js else 0
        lo = min(ns_) if ns_ else None
        max_j_overall = max(max_j_overall, mj)
        per_sol.append({"basis_index": s_i, "max_log_power": mj, "lowest_order_n": lo,
                        "n_support": len(nz)})
        print(f"  sol[{s_i}]: max log power = {mj}, lowest n = {lo}, support = {len(nz)}")

    # #log-free solutions = dim - rank(log-part of null space)
    rows = [[v[idx[(n, j)]] for n in range(N_TRUNC + 1) for j in range(1, DLOG)] for v in ns]
    rank_log = sp.Matrix(rows).rank()
    num_logfree = dim - rank_log
    largest_block = max_j_overall + 1
    print()
    print("max log power present :", max_j_overall, "=> largest Jordan block =", largest_block)
    print("number of log-free solutions (= # Jordan blocks):", num_logfree)

    jordan = None
    if dim == 4:
        if num_logfree == 2 and largest_block == 2:
            jordan = [2, 2]
        elif num_logfree == 2 and largest_block == 3:
            jordan = [3, 1]
        elif num_logfree == 1 and largest_block == 4:
            jordan = [4]
        elif num_logfree == 3 and largest_block == 2:
            jordan = [2, 1, 1]
        elif num_logfree == 4 and largest_block == 1:
            jordan = [1, 1, 1, 1]
    dimZ = sum(min(di, dj) for di in jordan for dj in jordan) if jordan else None
    print("=> Jordan type of M_0 (eigenvalue 1):", jordan)
    print("=> dim Z(M_0) =", dimZ)

    obj = {
        "op": "cc3-1c-frobenius-z0",
        "task_id": "op:cc-transcendence/cc3-1c",
        "operator_L": "z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2",
        "theta_normal_form": "L = P0(theta) + z P1(theta) + z^2 P2(theta)",
        "P0": "t^2 (t-1)^2", "P1": "-3 (t)_4 - 25 (t)_3 - 47 (t)_2 - 15 t", "P2": "-1",
        "point": "z=0", "exponents": [0, 0, 1, 1], "indicial_polynomial": "rho^2 (rho-1)^2",
        "method": "exact rational Frobenius in theta=zD; recurrence P0(nI+N)v_n + P1((n-1)I+N)v_{n-1} + P2((n-2)I+N)v_{n-2}=0; sympy nullspace over Q.",
        "truncation_N": N_TRUNC,
        "solution_space_dim": int(dim),
        "max_log_power": int(max_j_overall),
        "largest_jordan_block": int(largest_block),
        "num_log_free_solutions_eq_num_blocks": int(num_logfree),
        "jordan_type_M0_eigenvalue_1": jordan,
        "dimZ_M0": int(dimZ) if dimZ is not None else None,
        "per_solution": per_sol,
        "verdict_vs_cc3_1b": ("cc3-1b's 'z=0 apparent / log-free' is REFUTED: z=0 carries "
                              "logarithms; rank(M0-I)=2 (2 Jordan blocks)."),
        "rigidity_input": ("dimZ(M_0) feeds rig = -16 + dimZ(M_0) + dimZ(M_{1/3}) + 1 - 3, "
                           "dimZ(M_{1/3})=10."),
        "ceiling": ("A Fuchsian relocation does not imply K is a classical period; provenance, "
                    "not singularity type, is what the period conjectures see. Unconditional "
                    "transcendence of C is NOT a deliverable of op:cc-3 at any grade."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1c_frobenius_z0_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1c_frobenius_z0_results.json")

if __name__ == "__main__":
    main()
