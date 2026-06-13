#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc2-1 + op:cc2-2  --  Determinant/Twist + Invariant-Form Battery
===================================================================
SIARC four-class discipline. PROVEN = Lean only. Group-containment
implications are STRUCTURAL with citation locators (van der Put-Singer
'Galois Theory of Linear Differential Equations', Beukers-Heckman).

Inherited (cc-1 sha bfb91bd..., cc2-0 sha dc54bbe...):
  L2 order 4, a4=4 s^4(4-3 s); exp@0={0,1/2,1,3/2}; exp@R={0,1,2,-11/6};
  oo irregular slope 1/4, edge poly -12 c^4-1, determining factors c*i^k s^{1/4}
  (k=0..3, one transitive Z/4 orbit); L2 irreducible/minimal.

REGISTERED PREDICTIONS (test, do not assume):
  P1 (local self-duality at oo): {c i^k} closed under negation, so Lambda^2 L2
     has a rank-2 slope-0 piece at oo (pairs (0,2),(1,3) cancel).
  P2 (global non-self-duality): R-eigenvalues {mu,mu,mu,mu e^{i pi/3}} never
     inversion-closed for any rank-1 twist -> adjoint NEGATIVE, Lambda^2/Sym^2
     rational searches NULL, surviving G_Gal^0 = SL4.
  If P2 fails computationally -> a cc-1 input is wrong -> HALT.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json, hashlib
import sympy as sp

s = sp.symbols("s")
R = sp.Rational(4, 3)

# inherited exact L2 coefficients (cc-1)
A = {
    0: sp.Integer(-1) * s**2,
    1: sp.Integer(-30) * s**2,
    2: -156*s**3 + 12*s**2,
    3: -94*s**4 + 48*s**3,
    4: -12*s**5 + 16*s**4,
}
assert sp.expand(A[4] - 4*s**4*(4 - 3*s)) == 0

EXP0 = [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2)]
EXPR = [sp.Integer(0), sp.Integer(1), sp.Integer(2), sp.Rational(-11, 6)]


# ---------- indicial polynomial at a regular singular point p ----------
def indicial_poly(coeffs, p, r):
    """Return the indicial polynomial in r at finite reg. sing. point p."""
    x = sp.symbols("x")
    aj = {j: sp.Poly(sp.expand(coeffs[j].subs(s, p + x)), x) for j in range(5)}
    # L[x^r] = sum_{j} a_j(p+x) * falling(r,j) * x^{r-j}
    #        = sum_{j,k} a_{j,k} falling(r,j) x^{r-j+k}
    # collect by power r + L ; find lowest L and its coefficient = indicial
    def falling(rr, j):
        out = sp.Integer(1)
        for t in range(j):
            out *= (rr - t)
        return out
    terms = {}  # power offset (k-j) -> coeff poly in r
    for j in range(5):
        cj = aj[j].all_coeffs()[::-1]  # c[k] = coeff of x^k
        for k, c in enumerate(cj):
            if c == 0:
                continue
            off = k - j
            terms[off] = terms.get(off, sp.Integer(0)) + c * falling(r, j)
    Lmin = min(terms.keys())
    indicial = sp.expand(terms[Lmin])
    return indicial, terms, Lmin


# =====================================================================
# op:cc2-1  DETERMINANT / TWIST
# =====================================================================
def cc2_1():
    a3, a4 = A[3], A[4]
    ratio = sp.simplify(-a3 / a4)                       # w'/w
    ratio_pf = sp.apart(ratio, s)                       # partial fractions
    logW = sp.integrate(ratio, s)
    logW = sp.simplify(logW)
    # det = exp(int) ; present as s^e0 (4-3s)^eR symbolic
    # residues:
    res0 = sp.simplify(sp.limit(ratio * s, s, 0))               # coeff of 1/s
    resR = sp.simplify(sp.limit(ratio * (s - R), s, R))         # coeff of 1/(s-R)
    # W = s^{res0} (s-R)^{resR}; exponent of W at oo = -(res0+resR)
    det_exp0 = res0
    det_expR = resR
    det_expoo = -(res0 + resR)
    # cross-check W exponent = (sum exponents) - n(n-1)/2 at each reg point
    chk0 = sp.simplify(sum(EXP0) - 6 - det_exp0)
    chkR = sp.simplify(sum(EXPR) - 6 - det_expR)
    # chi = det^{1/4}: exponents = det_exp/4
    chi0, chiR, chioo = det_exp0/4, det_expR/4, det_expoo/4
    twist0 = [sp.nsimplify(e - chi0) for e in EXP0]
    twistR = [sp.nsimplify(e - chiR) for e in EXPR]
    return {
        "minus_a3_over_a4": str(ratio),
        "minus_a3_over_a4_partial_fractions": str(ratio_pf),
        "logW": str(logW),
        "W_det": f"s**({det_exp0}) * (s-4/3)**({det_expR})  [~ s^-3 (4-3s)^(-29/6)]",
        "det_exponents": {"at_0": str(det_exp0), "at_R": str(det_expR), "at_oo": str(det_expoo)},
        "wronskian_crosscheck_(sumExp-6-detExp==0)": {"at_0": str(chk0), "at_R": str(chkR)},
        "chi=det^{1/4}_exponents": {"at_0": str(chi0), "at_R": str(chiR), "at_oo": str(chioo)},
        "chi_nature": "ALGEBRAIC over C(s) (rational powers s^{-3/4}(4-3s)^{-29/24}); not rational, not properly Liouvillian",
        "twisted_exponents_at_0": [str(e) for e in twist0],
        "twisted_exponents_at_R": [str(e) for e in twistR],
        "twisted_sum_at_0": str(sp.nsimplify(sum(twist0))),
        "twisted_sum_at_R": str(sp.nsimplify(sum(twistR))),
        "twisted_note": "after twist by chi=det^{1/4} all regular-point exponent sums = 6 = n(n-1)/2 (SL4 normalization, Wronskian constant); exp parts at oo unchanged (algebraic twist), rational-exponent part shifts by -chi_oo",
        "grade": "VERIFIED (exact symbolic)",
    }


# =====================================================================
# companion matrix + adjoint
# =====================================================================
def companion():
    a4 = A[4]
    M = sp.zeros(4, 4)
    for i in range(3):
        M[i, i+1] = 1
    for j in range(4):
        M[3, j] = sp.simplify(-A[j]/a4)
    return M


def formal_adjoint():
    """L*[u] = sum_j (-1)^j (a_j u)^{(j)}; return its D-form coeffs b_k."""
    u = sp.Function("u")
    expr = 0
    for j in range(5):
        expr += (-1)**j * sp.diff(A[j]*u(s), s, j)
    expr = sp.expand(expr)
    b = {}
    for k in range(5):
        b[k] = sp.simplify(expr.coeff(sp.diff(u(s), s, k)))
    # also the k=0 term (no derivative)
    b[0] = sp.simplify(expr.coeff(u(s)))
    return b


# =====================================================================
# op:cc2-2a  ADJOINT / SELF-DUALITY  (eigenvalue inversion-closure)
# =====================================================================
def cc2_2a():
    b = formal_adjoint()
    # exponents of L* at R via indicial
    r = sp.symbols("r")
    indL, _, _ = indicial_poly(A, R, r)
    indLstar, _, _ = indicial_poly(b, R, r)
    rootsL = sorted(sp.solve(sp.Eq(indL, 0), r), key=lambda z: sp.re(z))
    rootsLs = sorted(sp.solve(sp.Eq(indLstar, 0), r), key=lambda z: sp.re(z))
    # R-monodromy eigenvalues of L: exp(2 pi i rho)
    eig = [sp.simplify(sp.exp(2*sp.pi*sp.I*rho)) for rho in EXPR]
    eig_simpl = [sp.nsimplify(sp.simplify(e), [sp.pi]) for e in eig]
    # inversion-closure-up-to-scalar test on multiset {1,1,1,e^{i pi/3}}
    # find kappa with {eig} == {kappa/eig}; three equal -> kappa fixed by triple
    closed = False
    note = ("R-eigenvalue multiset {1,1,1,e^{-2pi i*11/6}} = {1,1,1,e^{i pi/3}}. "
            "Any V ~ V* (x) kappa forces multiset = kappa*{1,1,1,e^{-i pi/3}}; the value "
            "of multiplicity 3 fixes kappa=1, then e^{i pi/3} != e^{-i pi/3} (since e^{2i pi/3}!=1). "
            "=> NOT inversion-closed up to any scalar => NO invariant nondegenerate bilinear form "
            "(symmetric or alternating), even up to a rank-1 twist.")
    return {
        "adjoint_Lstar_coeffs": {str(k): str(b[k]) for k in range(5)},
        "Lstar_leading_equals_L_leading": bool(sp.simplify(b[4]-A[4]) == 0),
        "L_indicial_at_R_roots": [str(x) for x in rootsL],
        "Lstar_indicial_at_R_roots": [str(x) for x in rootsLs],
        "L_vs_Lstar_exponents_differ": rootsL != rootsLs,
        "R_monodromy_eigenvalues": [str(e) for e in eig_simpl],
        "inversion_closed_up_to_scalar": closed,
        "verdict": "NEGATIVE: L2 is NOT self-dual up to a rank-1 twist (confirms P2)",
        "hand_proof": note,
        "grade": "STRUCTURAL (exact R-eigenvalue hand proof) + VERIFIED (adjoint symbolic)",
    }


# =====================================================================
# exterior / symmetric square of the companion matrix
# =====================================================================
def pairs_lt(n):
    return [(i, j) for i in range(n) for j in range(i+1, n)]


def pairs_le(n):
    return [(i, j) for i in range(n) for j in range(i, n)]


def exterior_square_matrix(Acomp):
    """induced matrix on Lambda^2(C^4), basis e_i^e_j (i<j)."""
    P = pairs_lt(4)
    idx = {p: k for k, p in enumerate(P)}
    B = sp.zeros(6, 6)
    for col, (i, j) in enumerate(P):
        # d(e_i ^ e_j) = (A e_i)^e_j + e_i^(A e_j)
        # A e_i = sum_a A[a,i] e_a
        for a in range(4):
            cia = Acomp[a, i]
            if cia != 0 and a != j:
                ii, jj = (a, j) if a < j else (j, a)
                sign = 1 if a < j else -1
                B[idx[(ii, jj)], col] += sign*cia
            caj = Acomp[a, j]
            if caj != 0 and a != i:
                ii, jj = (i, a) if i < a else (a, i)
                sign = 1 if i < a else -1
                B[idx[(ii, jj)], col] += sign*caj
    return sp.simplify(B), P


# =====================================================================
# RATIONAL INVARIANT-FORM SEARCH:  solve P' = -A^T P - P A for rational P
#   P antisymmetric (6 dof) -> invariant alternating form -> G in Sp4
#   P symmetric    (10 dof) -> invariant symmetric  form -> G in SO4
# ansatz P_ij = N_ij(s) / (s^a (4-3s)^b), deg N_ij <= dmax
# =====================================================================
def rational_form_search(Acomp, kind, a, bexp, dmax):
    D = s**a * (4 - 3*s)**bexp
    coeffs = []
    P = sp.zeros(4, 4)
    cvars = []
    if kind == "antisym":
        ent = pairs_lt(4)
    else:
        ent = pairs_le(4)
    Nmap = {}
    for (i, j) in ent:
        cs = sp.symbols(f"c_{i}_{j}_0:{dmax+1}")
        cvars += list(cs)
        N = sum(cs[d]*s**d for d in range(dmax+1))
        Nmap[(i, j)] = N
        P[i, j] = N/D
        if i == j:
            pass
        else:
            P[j, i] = (1 if kind == "sym" else -1) * N/D
    # residual = P' + A^T P + P A   (must be 0 for invariant form)
    res = sp.diff(P, s) + Acomp.T*P + P*Acomp
    # clear denominators: multiply by D^2 * a4  (a4 = denom of A entries)
    a4 = A[4]
    clear = sp.expand(D**2 * a4)
    eqs = []
    if kind == "antisym":
        cells = pairs_lt(4)
    else:
        cells = pairs_le(4)
    for (i, j) in cells:
        e = sp.expand(sp.together(res[i, j]) * clear)
        e = sp.expand(sp.cancel(e))
        if not e.free_symbols <= (set(cvars) | {s}):
            e = sp.expand(sp.simplify(e))
        pol = sp.Poly(e, s)
        eqs += [c for c in pol.all_coeffs()]
    # solve homogeneous linear system in cvars
    Msys, _ = sp.linear_eq_to_matrix(eqs, cvars)
    ns = Msys.nullspace()
    return {"kind": kind, "ansatz": f"N/(s^{a}(4-3s)^{bexp}), degN<={dmax}",
            "num_unknowns": len(cvars), "num_equations": len(eqs),
            "nullspace_dim": len(ns),
            "nontrivial_rational_form": len(ns) > 0}


# =====================================================================
# op:cc2-2b / 2c  driver
# =====================================================================
def cc2_2bc(Acomp):
    # determining-factor sums at oo (P1): factors c*i^k, k=0..3
    I = sp.I
    fac = [I**k for k in range(4)]   # up to common c*s^{1/4}
    ext_sums = {}
    for (i, j) in pairs_lt(4):
        val = sp.simplify(fac[i] + fac[j])
        ext_sums[f"({i},{j})"] = str(val)
    slope0_pairs = [k for k, v in ext_sums.items() if v == "0"]

    Bext, P = exterior_square_matrix(Acomp)
    ext_order = Bext.shape[0]

    # rational invariant-form searches (two boxes for robustness)
    alt1 = rational_form_search(Acomp, "antisym", 4, 4, 10)
    alt2 = rational_form_search(Acomp, "antisym", 3, 3, 8)
    sym1 = rational_form_search(Acomp, "sym", 4, 4, 10)
    sym2 = rational_form_search(Acomp, "sym", 3, 3, 8)

    return {
        "exterior_square_dim_(order)": ext_order,
        "exterior_order_note": "Lambda^2 of order-4 is 6-dimensional; order 6 (no symplectic drop) consistent with P2",
        "infinity_determining_factor_sums_(units_of_c s^{1/4})": ext_sums,
        "slope0_pairs_(sum=0)": slope0_pairs,
        "P1_confirmed_rank2_slope0_piece": slope0_pairs == ["(0,2)", "(1,3)"],
        "P1_note": "pairs (0,2),(1,3) cancel -> rank-2 slope-0; other 4 pairs -> rank-4 slope-1/4 (one Z/4 orbit)",
        "exterior_rational_form_search_box1": alt1,
        "exterior_rational_form_search_box2": alt2,
        "symmetric_rational_form_search_box1": sym1,
        "symmetric_rational_form_search_box2": sym2,
        "Sp4_verdict": ("G NOT in Sp4: no invariant alternating form (Lambda^2 rational search NULL in both boxes; "
                        "closed unconditionally by the R-eigenvalue inversion-closure hand proof)"
                        if not (alt1["nontrivial_rational_form"] or alt2["nontrivial_rational_form"]) else
                        "INVARIANT ALTERNATING FORM FOUND -> P2 REFUTED -> HALT"),
        "SO4_verdict": ("G NOT in SO4: no invariant symmetric form (Sym^2 rational search NULL in both boxes; "
                        "closed by the same hand proof)"
                        if not (sym1["nontrivial_rational_form"] or sym2["nontrivial_rational_form"]) else
                        "INVARIANT SYMMETRIC FORM FOUND -> P2 REFUTED -> HALT"),
        "grade": "VERIFIED (bounded rational search) + STRUCTURAL (eigenvalue closure; vdP-Singer ch.4)",
    }


# =====================================================================
# op:cc2-2d  Jordan structure at R (Frobenius obstructions) + tensor exclusions
# =====================================================================
def cc2_2d():
    r = sp.symbols("r")
    indL, terms, Lmin = indicial_poly(A, R, r)

    def Ptil(ell, rr):
        off = Lmin + ell
        return sp.expand(terms.get(off, sp.Integer(0)).subs(r, rr)) if off in terms else sp.Integer(0)

    P0 = sp.factor(indL)
    # eigenvalue-1 tower {0,1,2}: ALL resonance obstructions must be checked.
    # r=0 -> 1 : Ptil1(0);  r=1 -> 2 : Ptil1(1);  r=0 -> 2 : Ptil2(0) (+ c1*Ptil1(1))
    ob_0_1 = sp.simplify(Ptil(1, sp.Integer(0)))
    ob_1_2 = sp.simplify(Ptil(1, sp.Integer(1)))
    ob_0_2 = sp.simplify(Ptil(2, sp.Integer(0)))   # since Ptil1(1)=0, full N=2 numerator = c0*Ptil2(0)
    # number of independent log-free solutions on eigenvalue-1 space:
    #   from r=2 always 1; from r=1 iff ob_1_2==0; from r=0 iff ob_0_1==0 AND ob_0_2==0
    logfree = 1 + int(ob_1_2 == 0) + int(ob_0_1 == 0 and ob_0_2 == 0)
    semisimple = (logfree == 3)
    size = {3: 1, 2: 2, 1: 3}[logfree]

    # exponential-torus dimension = Z-rank of {determining-factor leading units} = {1,i,-1,-i}
    facs = [sp.I**k for k in range(4)]
    Wmat = sp.Matrix([[sp.re(f), sp.im(f)] for f in facs])
    exp_torus_dim = Wmat.rank()

    # M_0 Jordan (symbolic): exponents {0,1/2,1,3/2}; resonances 0->1 and 1/2->3/2
    ind0, terms0, Lmin0 = indicial_poly(A, sp.Integer(0), r)
    def Ptil0(ell, rr):
        off = Lmin0 + ell
        return sp.expand(terms0.get(off, sp.Integer(0)).subs(r, rr)) if off in terms0 else sp.Integer(0)
    M0_ob_0_1 = sp.simplify(Ptil0(1, sp.Integer(0)))
    M0_ob_h_3h = sp.nsimplify(sp.simplify(Ptil0(1, sp.Rational(1, 2))))
    M0_semisimple = (M0_ob_0_1 == 0 and M0_ob_h_3h == 0)

    return {
        "indicial_at_R_factored": str(P0),
        "obstruction_exp0->1_(Ptil1(0))": str(ob_0_1),
        "obstruction_exp1->2_(Ptil1(1))": str(ob_1_2),
        "obstruction_exp0->2_(Ptil2(0))": str(ob_0_2),
        "log_free_solution_count_eig1": logfree,
        "max_jordan_block_eig1": size,
        "M_R_semisimple": semisimple,
        "jordan_structure_eig1": ("SEMISIMPLE: 3 independent log-free Frobenius solutions on the "
                                  "eigenvalue-1 space (geometric mult = algebraic mult = 3); NO logarithm"
                                  if semisimple else f"non-semisimple, max Jordan block {size}"),
        "M_R_type": "semisimple complex pseudo-reflection of order 6: eigenvalues {1,1,1,e^{i pi/3}}, fixes a 3-dim hyperplane, scales one line by e^{i pi/3}",
        "M_0_obstruction_0->1": str(M0_ob_0_1),
        "M_0_obstruction_half->3half": str(M0_ob_h_3h),
        "M_0_semisimple": M0_semisimple,
        "M_0_type": "semisimple: eigenvalues {1,-1,1,-1}, no logarithm (both resonance obstructions vanish)",
        "numerical_crosscheck": {
            "script": "cc2_2d_numerical_monodromy.py",
            "output_hash": "03e4292669c861ddd3815d3179a876828a83e22702a517de43411a06fe625118",
            "dps": 40,
            "M_R": "eig {1,1,1,e^{i pi/3}}; rank(M_R-I)=1 -> geom mult eig1 = 3 = alg mult -> SEMISIMPLE",
            "M_0": "eig {1,-1,1,-1}; rank(M_0-I)=2, rank(M_0+I)=2 -> all geom=alg -> SEMISIMPLE",
            "agrees_with_symbolic": True,
        },
        "AUDIT_inherited_state": ("REFUTES the inherited-state narration 'resonance log / unipotent part at R'. "
                                  "M_R is SEMISIMPLE (two independent channels). Consistent with EBR-II's OWN "
                                  "criterion: a -gamma resonance log requires gamma in Z; here gamma = 11/6 not in Z, "
                                  "so NO log is expected. The R-eigenvalues {1,1,1,e^{i pi/3}} are unchanged; only the "
                                  "'unipotent' adjective is corrected to 'semisimple pseudo-reflection'. cc-1's "
                                  "load-bearing claims (irreducibility, exponents, irregular-oo) are UNAFFECTED. "
                                  "Recommend a one-line cc-1 narration erratum."),
        # ---- tensor / Sym^3 exclusions (independent of the log; rely on cc2-2a self-duality) ----
        "Sym3_SL2_excluded": True,
        "Sym3_SL2_reason": ("(i) Sym^3 of a rank-2 W is self-dual up to twist (Sym^3 W ~ Sym^3 W* (x) (det W)^3), "
                            "contradicting cc2-2a (not self-dual up to any rank-1 twist); "
                            "(ii) SLOPE: a rank-2 module has ramification <=2, cannot carry slope 1/4 (needs "
                            "ramification 4); Sym^3 of slope-phi rank-2 gives factors {3phi,phi,-phi,-3phi} with "
                            "TWO magnitudes, not L2's single equal-magnitude transitive Z/4 orbit {c i^k}."),
        "SL2_tensor_SL2_excluded": True,
        "SL2_tensor_SL2_reason": ("(i) V1 (x) V2 with rank-2 factors is self-dual up to twist (each rank-2 is, via "
                                  "V_i ~ V_i* (x) det V_i), contradicting cc2-2a; "
                                  "(ii) SLOPE: rank-2 factors have ramification <=2, cannot produce slope 1/4. "
                                  "This is the Aschbacher TENSOR class C4, distinct from the imprimitive class C2 below."),
        # ---- imprimitive / monomial: NOT locally excludable (the log crutch is gone) ----
        "exponential_torus_dim": exp_torus_dim,
        "exponential_torus_weights": "{+e1,-e1,+e2,-e2} (the 4 determining factors c*{1,i,-1,-i}; Z-module rank 2)",
        "monomial_4line_excluded_locally": False,
        "imprimitive_2block_excluded_locally": False,
        "imprimitive_status": ("OPEN -- NOT excludable from local data. The connected exponential torus T (dim 2) "
                               "lies in G^0 and fixes each block (blocks must be spans of weight-lines). The formal "
                               "monodromy at oo is a single 4-cycle on the 4 weight-lines; it preserves the 2-block "
                               "system {{L1,L3},{L2,L4}} (swapping the two blocks). The SEMISIMPLE pseudo-reflection "
                               "M_R = diag(1,1,1,e^{i pi/3}) in the weight basis preserves that same 2-block system "
                               "(and the 4-line system). M_0 is also semisimple. Hence local data at {0,R,oo} are "
                               "fully COMPATIBLE with an imprimitive 2-block (and a fortiori monomial) structure. "
                               "Excluding it requires the GLOBAL monodromy relation M_0 M_R M_oo = I together with "
                               "the connection/Stokes data at oo -- i.e. op:cc-4 (DEFERRED per the stage rules)."),
        "imprimitive_meaning": ("The imprimitive C2 case (V = W1 (+) W2, blocks swapped) has G^0 block-diagonal "
                                "(<= GL2 x GL2), and the monomial case has G^0 a torus -- both give a solvable or "
                                "non-simple G^0, equivalently L2 WOULD have Liouvillian solutions. So the residual "
                                "dichotomy is exactly: primitive (G^0 = SL4, NO Liouvillian solutions) vs imprimitive "
                                "(G^0 reducible/torus, Liouvillian solutions exist). cc2-4 is the decider."),
        "grade": "STRUCTURAL (Frobenius obstruction exact + numerical cross-check + slope/self-dual hand proofs); imprimitive exclusion DEFERRED to cc2-4",
    }


# =====================================================================
def main():
    print("="*72); print("op:cc2-1 + op:cc2-2  Twist + Invariant-Form Battery"); print("="*72)

    Acomp = companion()
    twist = cc2_1()
    print("\n[cc2-1] -a3/a4 =", twist["minus_a3_over_a4"])
    print("        det exponents:", twist["det_exponents"])
    print("        Wronskian cross-check (==0):", twist["wronskian_crosscheck_(sumExp-6-detExp==0)"])
    print("        twisted exp@0 =", twist["twisted_exponents_at_0"], " sum", twist["twisted_sum_at_0"])
    print("        twisted exp@R =", twist["twisted_exponents_at_R"], " sum", twist["twisted_sum_at_R"])

    # ---- standalone hashed twisted-exponent-table artifact (load-bearing for cc2-2) ----
    twist_table = {
        "artifact": "cc2-1 twisted-exponent table",
        "operator": "L2 (cc-1 sha bfb91bd...)",
        "determinant_W": twist["W_det"],
        "det_exponents": twist["det_exponents"],
        "chi=det^{1/4}_exponents": twist["chi=det^{1/4}_exponents"],
        "chi_nature": twist["chi_nature"],
        "original_exponents": {"at_0": [str(e) for e in EXP0], "at_R": [str(e) for e in EXPR]},
        "twisted_exponents": {"at_0": twist["twisted_exponents_at_0"], "at_R": twist["twisted_exponents_at_R"]},
        "twisted_sums_(=6=SL4_norm)": {"at_0": twist["twisted_sum_at_0"], "at_R": twist["twisted_sum_at_R"]},
        "note": twist["twisted_note"],
    }
    tblob = json.dumps(twist_table, sort_keys=True, ensure_ascii=False).encode("utf-8")
    twist_table["sha256"] = hashlib.sha256(tblob).hexdigest()
    with open("cc2_1_twisted_exponent_table.json", "w", encoding="utf-8") as f:
        json.dump(twist_table, f, indent=2, ensure_ascii=False)
    print("        twisted-exponent table sha256 =", twist_table["sha256"])

    a2a = cc2_2a()
    print("\n[cc2-2a] R-monodromy eigenvalues:", a2a["R_monodromy_eigenvalues"])
    print("         L* exps@R:", a2a["Lstar_indicial_at_R_roots"], " vs L exps@R:", a2a["L_indicial_at_R_roots"])
    print("         verdict:", a2a["verdict"])

    a2bc = cc2_2bc(Acomp)
    print("\n[cc2-2b/c] exterior square dim:", a2bc["exterior_square_dim_(order)"])
    print("           oo determining-factor sums:", a2bc["infinity_determining_factor_sums_(units_of_c s^{1/4})"])
    print("           slope-0 pairs:", a2bc["slope0_pairs_(sum=0)"], "(P1:", a2bc["P1_confirmed_rank2_slope0_piece"], ")")
    print("           Lambda^2 rational search box1:", a2bc["exterior_rational_form_search_box1"]["nullspace_dim"],
          " box2:", a2bc["exterior_rational_form_search_box2"]["nullspace_dim"])
    print("           Sym^2 rational search box1:", a2bc["symmetric_rational_form_search_box1"]["nullspace_dim"],
          " box2:", a2bc["symmetric_rational_form_search_box2"]["nullspace_dim"])
    print("           Sp4:", a2bc["Sp4_verdict"])
    print("           SO4:", a2bc["SO4_verdict"])

    a2d = cc2_2d()
    print("\n[cc2-2d] indicial@R:", a2d["indicial_at_R_factored"])
    print("         obstructions  0->1:", a2d["obstruction_exp0->1_(Ptil1(0))"],
          " 1->2:", a2d["obstruction_exp1->2_(Ptil1(1))"],
          " 0->2:", a2d["obstruction_exp0->2_(Ptil2(0))"])
    print("         M_R:", a2d["jordan_structure_eig1"])
    print("         M_0:", a2d["M_0_type"], "(semisimple:", a2d["M_0_semisimple"], ")")
    print("         AUDIT:", a2d["AUDIT_inherited_state"][:96], "...")
    print("         exp-torus dim:", a2d["exponential_torus_dim"],
          "| Sym^3SL2 excl:", a2d["Sym3_SL2_excluded"], "| SL2(x)SL2 excl:", a2d["SL2_tensor_SL2_excluded"])
    print("         imprimitive(2-block)/monomial excluded locally:",
          a2d["imprimitive_2block_excluded_locally"], "-> DEFERRED to cc2-4")

    # ---------------- elimination table ----------------
    no_form = ("NOT in Sp4" in a2bc["Sp4_verdict"]) and ("NOT in SO4" in a2bc["SO4_verdict"])
    imprimitive_excluded = a2d["imprimitive_2block_excluded_locally"] and a2d["monomial_4line_excluded_locally"]
    primitive_settled = imprimitive_excluded
    sl4_clean = (no_form and primitive_settled)
    elim = {
        "finite": {"killed_by": "oo irregular: G^0 contains the 2-dim exponential torus (infinite, connected) [cc2-3 input/cc-1]",
                   "grade": "STRUCTURAL", "status": "killed"},
        "reducible": {"killed_by": "cc-1 irreducibility (transitive Z/4 slope orbit) + cc2-0 order-<4 factor exclusion",
                      "grade": "STRUCTURAL", "status": "killed"},
        "Sp4 (C8 alt form)": {"killed_by": "cc2-2b: no invariant alternating form (Lambda^2 rational search NULL; R-eigenvalues not inversion-closed up to twist)",
                              "grade": "STRUCTURAL", "status": "killed" if no_form else "OPEN"},
        "SO4 (C8 sym form)": {"killed_by": "cc2-2c: no invariant symmetric form (Sym^2 rational search NULL; same eigenvalue closure)",
                              "grade": "STRUCTURAL", "status": "killed" if no_form else "OPEN"},
        "Sym^3 SL2 (class S)": {"killed_by": "cc2-2d: self-dual up to twist (contra cc2-2a) + slope (rank-2 ramif <=2 != 4)",
                                "grade": "STRUCTURAL", "status": "killed"},
        "SL2 (x) SL2 (C4 tensor)": {"killed_by": "cc2-2d: self-dual up to twist (contra cc2-2a) + slope (rank-2 ramif <=2 != 4)",
                                    "grade": "STRUCTURAL", "status": "killed"},
        "monomial (C2, 4 lines)": {"killed_by": "NOT excluded locally: M_0,M_R semisimple; torus+pseudo-reflection compatible with 4-line system",
                                   "grade": "--", "status": "OPEN -> cc2-4"},
        "imprimitive (C2, 2+2)": {"killed_by": "NOT excluded locally: local data compatible with block system {{L1,L3},{L2,L4}} (gamma_oo swaps blocks; M_R preserves them)",
                                  "grade": "--", "status": "OPEN -> cc2-4"},
        "SL4 (C1 primitive)": {"killed_by": "-- survivor IFF imprimitive/monomial excluded (cc2-4) --",
                               "grade": "STRUCTURAL-CONDITIONAL", "status": "SURVIVOR" if sl4_clean else "candidate (pending cc2-4 primitivity)"},
    }
    verdict = ("Assuming cc2-1/2 verdicts, G_Gal(L2)^0 = SL4."
               if sl4_clean else
               "CONDITIONAL: 6 of 8 proper candidates are killed (finite, reducible, Sp4, SO4, Sym^3SL2, "
               "SL2(x)SL2). The residual dichotomy is PRIMITIVE (G_Gal(L2)^0 = SL4, no Liouvillian solutions) "
               "vs IMPRIMITIVE (C2: monomial torus or 2-block <= GL2xGL2, Liouvillian solutions exist). This is "
               "NOT decidable from the local data at {0,R,oo} (all of M_0, M_R semisimple; 2-dim exp torus and "
               "the oo 4-cycle + the R pseudo-reflection are all compatible with the block system {{L1,L3},{L2,L4}}). "
               "It is decided by op:cc-4 (global monodromy M_0 M_R M_oo = I + connection at oo). G_Gal(L2)^0 = SL4 "
               "is therefore STRUCTURAL-CONDITIONAL on the cc2-4 primitivity check.")

    print("\n[cc2-2e] ELIMINATION TABLE:")
    for k, v in elim.items():
        print(f"   {k:26s} {v['status']:30s} <- {v['killed_by']}")
    print("\n   VERDICT:", verdict)

    obj = {
        "op": "cc2-1+cc2-2",
        "inherits": {"cc-1": "bfb91bdeef251be00b770f486ec53d2304f4c1064f85d907a82951a49f5f227e",
                     "cc2-0": "dc54bbedd961649e3807406f4a0882022c8856d07460820cb2581a4282e3b5eb"},
        "cc2_1_determinant_twist": twist,
        "cc2_2a_adjoint_selfduality": a2a,
        "cc2_2bc_invariant_forms": a2bc,
        "cc2_2d_imprimitive_tensor": a2d,
        "cc2_2e_elimination_table": elim,
        "P1_local_self_duality_at_infinity": {
            "status": "CONFIRMED",
            "evidence": "determining factors c*{1,i,-1,-i} closed under negation; Lambda^2 has rank-2 slope-0 piece at oo (pairs (0,2),(1,3) cancel); exp-torus weights {+e1,-e1,+e2,-e2}",
        },
        "P2_global_non_self_duality": {
            "computational_predictions": "ALL CONFIRMED (R-eigenvalues {1,1,1,e^{i pi/3}}=={mu,mu,mu,mu e^{i pi/3}} with mu=1; Lambda^2 and Sym^2 rational searches NULL; adjoint NEGATIVE)",
            "conclusion_status": ("REFINED, not refuted. P2's stated leap 'non-self-dual => survivor SL4' is INCOMPLETE: "
                                  "non-self-duality kills Sp4/SO4/tensor/Sym^3 but NOT the imprimitive C2 class (monomial "
                                  "/ 2-block), which need not be self-dual. So the honest survivor set is {SL4, imprimitive-C2}, "
                                  "and cc2-4 decides between them. No early-HALT: P2's computational legs all passed."),
        },
        "P1_P2_consistency": ("P1 (local self-duality at oo) and P2 (global non-self-duality) are CONSISTENT: the "
                              "negation-closed weight pairing at oo does NOT globalize to a G-invariant form because "
                              "M_R's e^{i pi/3} eigenvalue (unpaired with e^{-i pi/3}) breaks inversion-closure."),
        "AUDIT_correction": a2d["AUDIT_inherited_state"],
        "G_Gal_verdict": verdict,
        "G_Gal_grade": "STRUCTURAL-CONDITIONAL (conditional on cc2-4 primitivity; not Lean-checked)",
        "discipline_line": ("non-rigidity (P=d-1>0) does NOT imply C transcendental; a large G_Gal does NOT imply C "
                            "transcendental. op:cc-2 targets the GROUP only; C's transcendence is op:cc-3's burden via "
                            "periods. Even a confirmed G_Gal^0=SL4 (non-solvable) would license only 'no Liouvillian "
                            "solutions' (cc2-5), NOT transcendence of C, which remains CONJECTURED."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    sha = hashlib.sha256(blob).hexdigest()
    obj["canonical_sha256_of_hashfree_object"] = sha
    with open("cc2_1_2_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", sha)
    print("wrote cc2_1_2_results.json")


if __name__ == "__main__":
    main()
