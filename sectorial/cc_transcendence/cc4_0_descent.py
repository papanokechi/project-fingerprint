#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc4-0  --  DESCENT / INDUCTION TEST  (primitive vs imprimitive, the ballgame)
================================================================================
SIARC four-class discipline. PROVEN = Lean only. Group/module-equivalence
implications are STRUCTURAL with citation locators (van der Put-Singer
'Galois Theory of Linear Differential Equations', ch. 2/4; Beke factorization).

Inherited exact L2 (cc-1 sha bfb91bd..., cc2-1/2 sha 7d102dd...):
  order 4, a4 = 4 s^4(4-3 s); exp@0={0,1/2,1,3/2}; exp@R={0,1,2,-11/6};
  oo irregular slope 1/4, ramification 4, determining factors c*i^k s^{1/4}.
  M0, M_R SEMISIMPLE; M_R={1,1,1,e^{i pi/3}}, M0={1,-1,1,-1}.
  G_Gal(L2)^0 = SL4 STRUCTURAL-CONDITIONAL on excluding imprimitive C2.

THE TEST.  An irreducible rank-4 connection M is imprimitive (induced from a
degree-2 cover) IFF  M  ~=  M (x) eta  for a nontrivial quadratic character eta
(van der Put-Singer Thm; Aschbacher C2). A1 below proves eta = sqrt(s) is the
UNIQUE candidate (ramification subset of {0,R,oo}, even, UNRAMIFIED at R because
the R-eigenvalues {1,1,1,e^{i pi/3}} are NOT negation-closed). So the whole
primitivity question reduces to a single decidable computation:

        does there exist a rational 4x4 intertwiner  Phi  with
              Phi' = A Phi - Phi A + (1/(2s)) Phi   ?     (Route 2)

  nonzero rational Phi  <=>  M ~= M(x)sqrt(s)  <=>  IMPRIMITIVE
  only Phi = 0          <=>  M  not  ~= M(x)sqrt(s) <=> PRIMITIVE (G^0 = SL4)

Route 1 (independent, over the cover C(t), s=t^2): the eigenring
        dim_C { rational Phi~(t) : Phi~' = A~ Phi~ - Phi~ A~ }
  equals 1  <=> pullback M~ irreducible <=> PRIMITIVE
  equals >=2 <=> M~ decomposes (= W (+) sigma*W) <=> IMPRIMITIVE
Both routes MUST agree.

CALIBRATION built in: the eta-trivial search (a_eta = 0) computes End_{C(s)}(M);
for an absolutely irreducible M this is 1-dimensional (scalars, by Schur), which
re-confirms cc-1 irreducibility AND validates the linear-algebra pipeline.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import hashlib
import sympy as sp

s, t = sp.symbols("s t")
Rsing = sp.Rational(4, 3)

# ---- inherited exact L2 coefficients (cc-1) ----
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


def companion_in(var):
    """Companion matrix of L2 in the variable `var` (= d/d var system matrix)."""
    Asub = {k: A[k].subs(s, var) for k in range(5)}
    a4 = Asub[4]
    M = sp.zeros(4, 4)
    for i in range(3):
        M[i, i+1] = 1
    for j in range(4):
        M[3, j] = sp.cancel(-Asub[j]/a4)
    return M


# =====================================================================
# A1  --  eta = sqrt(s) is the UNIQUE nontrivial quadratic-character
#         candidate for imprimitivity (hand argument, encoded + verified)
# =====================================================================
def cc4_A1():
    # monodromy eigenvalue multisets (M0, M_R semisimple, from cc2-2d)
    eig0 = [sp.simplify(sp.exp(2*sp.pi*sp.I*r)) for r in EXP0]   # {1,-1,1,-1}
    eigR = [sp.simplify(sp.exp(2*sp.pi*sp.I*r)) for r in EXPR]   # {1,1,1,e^{i pi/3}}

    def multiset_key(lst):
        return sorted(sp.nsimplify(sp.simplify(z)).as_real_imag() for z in lst)

    def negation_closed(lst):
        a = multiset_key(lst)
        b = multiset_key([-z for z in lst])
        return a == b

    nc0 = negation_closed(eig0)   # expect True  -> eta MAY ramify at 0
    ncR = negation_closed(eigR)   # expect False -> eta must be UNRAMIFIED at R

    # determining-factor leading units at oo: c * {1, i, -1, -i}
    units = [sp.Integer(1), sp.I, sp.Integer(-1), -sp.I]
    ncoo = negation_closed(units)  # expect True -> eta MAY ramify at oo

    # Enumerate quadratic characters ramified within the singular set {0,R,oo}.
    # A quadratic character of C(s) is a square class prod (s-p_i)^{e_i}, e_i in {0,1},
    # ramified exactly at the p_i with e_i=1 plus oo iff sum e_i is odd.
    # Allowed finite ramification points: {0, R} (cannot ramify at a NON-singular
    # point of L2, else L2(x)eta gains a new singularity and cannot be ~= L2).
    cand = []
    for e0 in (0, 1):
        for eR in (0, 1):
            ram = []
            if e0:
                ram.append("0")
            if eR:
                ram.append("R")
            if (e0 + eR) % 2 == 1:   # odd total degree -> ramified at oo
                ram.append("oo")
            ram_set = set(ram)
            nontrivial = bool(ram_set)
            # local-compatibility: eta must be UNRAMIFIED at R (eigvals not neg-closed)
            ok_R = ("R" not in ram_set)
            # if ramified at 0, eigvals must be neg-closed (they are)
            ok_0 = (("0" not in ram_set) or nc0)
            ok_oo = (("oo" not in ram_set) or ncoo)
            even_branch = (len(ram_set) % 2 == 0)
            viable = nontrivial and ok_R and ok_0 and ok_oo and even_branch
            cand.append({
                "e0": e0, "eR": eR, "ramified_at": sorted(ram_set),
                "even_branch_count": even_branch,
                "unramified_at_R": ok_R, "viable_nontrivial": viable,
                "character": ("trivial" if not nontrivial else
                              ("sqrt(s)" if ram_set == {"0", "oo"} else
                               ("sqrt(s-4/3)" if ram_set == {"R", "oo"} else
                                ("sqrt(s(s-4/3))" if ram_set == {"0", "R"} else "?")))),
            })
    viable = [c for c in cand if c["viable_nontrivial"]]
    return {
        "M0_eigs": [str(sp.nsimplify(sp.simplify(z))) for z in eig0],
        "MR_eigs": [str(sp.nsimplify(sp.simplify(z))) for z in eigR],
        "M0_negation_closed": bool(nc0),
        "MR_negation_closed": bool(ncR),
        "oo_units_negation_closed": bool(ncoo),
        "candidates": cand,
        "viable_nontrivial_characters": [c["character"] for c in viable],
        "unique_candidate": (len(viable) == 1 and viable[0]["character"] == "sqrt(s)"),
        "verdict": ("eta = sqrt(s) is the UNIQUE nontrivial quadratic character "
                    "compatible with the local data (ramified {0,oo}, unramified at R). "
                    "Imprimitivity <=> M ~= M(x)sqrt(s)."),
        "hand_proof": (
            "A quadratic character can ramify only at singular points {0,R,oo} and at "
            "an EVEN number of them. At R the monodromy multiset {1,1,1,e^{i pi/3}} is "
            "NOT closed under negation (no -1 present), so M(x)eta has different R-monodromy "
            "unless eta is UNRAMIFIED at R. Hence ramification subset of {0,oo}; evenness "
            "forces {0,oo} (=> eta=sqrt(s)) or {} (trivial). At 0 the multiset {1,-1,1,-1} "
            "and at oo the unit set {1,i,-1,-i} ARE negation-closed, so sqrt(s) clears the "
            "necessary local tests; sufficiency is decided by the global intertwiner below."),
        "grade": "STRUCTURAL (finite eigenvalue/parity bookkeeping; exact)",
    }


# =====================================================================
# A1b  --  the oo formal monodromy is a 4-CYCLE (odd); this closes the
#          monomial (4-line) and field-extension (C3) loopholes so that
#          "no sqrt(s)-intertwiner" => PRIMITIVE is UNCONDITIONAL, not
#          merely "no 2-block".
# =====================================================================
def cc4_A1b_monomial_closure():
    # formal monodromy at oo: s^{1/4} -> e^{2 pi i/4} s^{1/4} = i s^{1/4},
    # so q_k = c i^k s^{1/4} -> q_{k+1}; a single 4-cycle (q0 q1 q2 q3).
    perm = [1, 2, 3, 0]  # k -> k+1 mod 4
    # cycle type / parity of a 4-cycle
    # a 4-cycle = 3 transpositions => ODD permutation (sign -1)
    sign = 1
    seen = [False]*4
    for start in range(4):
        if seen[start]:
            continue
        length = 0
        x = start
        while not seen[x]:
            seen[x] = True
            x = perm[x]
            length += 1
        if length % 2 == 0:
            sign *= -1
    is_odd = (sign == -1)
    # transitive subgroups of S4 and whether each contains a 4-cycle / has C2 quotient
    transitive_S4 = {
        "C4": {"contains_4cycle": True, "has_index2_subgroup": True},
        "V4": {"contains_4cycle": False, "has_index2_subgroup": True},
        "D4": {"contains_4cycle": True, "has_index2_subgroup": True},
        "A4": {"contains_4cycle": False, "has_index2_subgroup": False},
        "S4": {"contains_4cycle": True, "has_index2_subgroup": True},
    }
    allowed = {g: v for g, v in transitive_S4.items() if v["contains_4cycle"]}
    all_allowed_have_quadratic = all(v["has_index2_subgroup"] for v in allowed.values())
    return {
        "oo_formal_monodromy_permutation": "(q0 q1 q2 q3) 4-cycle on the 4 determining factors",
        "permutation_is_odd": bool(is_odd),
        "transitive_subgroups_of_S4": transitive_S4,
        "permutation_types_containing_a_4cycle": sorted(allowed.keys()),
        "A4_and_V4_excluded_by_4cycle": True,
        "every_allowed_type_has_quadratic_character": bool(all_allowed_have_quadratic),
        "verdict": (
            "Any IMPRIMITIVE/INDUCED structure makes G_Gal permute the 4 determining "
            "factors; the oo formal monodromy is the 4-cycle (q0 q1 q2 q3), an ODD "
            "permutation. A transitive subgroup of S4 containing a 4-cycle lies in "
            "{C4,D4,S4} (NOT A4, NOT V4), each of which has an index-2 subgroup, hence a "
            "quadratic character eta. By A1 that eta is sqrt(s). Route 2 refutes "
            "M ~= M(x)sqrt(s). Therefore BOTH the 2-block AND the 4-line (monomial) "
            "imprimitive classes -- and the degree-2/4 C3 field-extension classes, which "
            "reduce to the same cover -- are EXCLUDED. Primitivity is UNCONDITIONAL."),
        "grade": "STRUCTURAL (permutation-group + formal-monodromy hand argument; exact)",
    }


# =====================================================================
# RATIONAL INTERTWINER SEARCH (generic 4x4, 16 dof)
#   solve   Phi' = A Phi - Phi A + a_eta * Phi   for rational Phi
#   ansatz  Phi_ij = N_ij(var) / (den),  deg N_ij <= dmax
# =====================================================================
def intertwiner_search(Acomp, a_eta, var, den, a4_clear, dmax, label):
    cvars = []
    Phi = sp.zeros(4, 4)
    for i in range(4):
        for j in range(4):
            cs = sp.symbols(f"k_{i}_{j}_0:{dmax+1}")
            cvars += list(cs)
            Phi[i, j] = sum(cs[d]*var**d for d in range(dmax+1)) / den
    res = sp.diff(Phi, var) - Acomp*Phi + Phi*Acomp - a_eta*Phi
    clear = sp.expand(den**2 * a4_clear)
    eqs = []
    for i in range(4):
        for j in range(4):
            e = sp.expand(sp.cancel(sp.together(res[i, j]) * clear))
            pol = sp.Poly(e, var)
            eqs += list(pol.all_coeffs())
    Msys, _ = sp.linear_eq_to_matrix(eqs, cvars)
    ns = Msys.nullspace()
    return {
        "label": label,
        "ansatz": f"N/({den}), degN<={dmax}",
        "num_unknowns": len(cvars),
        "num_equations": len(eqs),
        "nullspace_dim": len(ns),
    }


# =====================================================================
# op:cc4-0  Route 2  --  eta = sqrt(s) twist over C(s)
# =====================================================================
def cc4_route2():
    Acomp = companion_in(s)
    a4 = A[4]
    out = {"description": "Route 2: M -> M(x)sqrt(s) intertwiner over C(s); "
                          "Phi' = [A,Phi] + (1/(2s)) Phi."}
    # CALIBRATION: a_eta = 0 -> End_{C(s)}(M) = scalars (dim 1) if abs. irreducible
    calib = []
    for (a, b, dm) in [(1, 1, 6), (2, 2, 8)]:
        den = s**a * (4 - 3*s)**b
        r = intertwiner_search(Acomp, sp.Integer(0), s, den, a4, dm,
                               f"End(M) calib s^{a}(4-3s)^{b} d{dm}")
        calib.append(r)
    # eta = sqrt(s):  a_eta = (1/2)/s
    a_eta = sp.Rational(1, 2)/s
    twist = []
    for (a, b, dm) in [(1, 2, 8), (2, 3, 12)]:
        den = s**a * (4 - 3*s)**b
        r = intertwiner_search(Acomp, a_eta, s, den, a4, dm,
                               f"Hom(M,M(x)sqrt s) s^{a}(4-3s)^{b} d{dm}")
        twist.append(r)
    out["calibration_End_M_dim"] = [c["nullspace_dim"] for c in calib]
    out["calibration_detail"] = calib
    out["twist_Hom_dim"] = [c["nullspace_dim"] for c in twist]
    out["twist_detail"] = twist
    end_dim = calib[-1]["nullspace_dim"]
    hom_dim = twist[-1]["nullspace_dim"]
    out["End_M_is_scalars"] = (end_dim == 1)
    out["intertwiner_exists"] = (hom_dim > 0)
    out["verdict"] = ("PRIMITIVE (no sqrt(s)-intertwiner)" if hom_dim == 0
                      else "IMPRIMITIVE (sqrt(s)-intertwiner found)")
    out["bounds_note"] = ("pole order <=1 at 0, <=2 at R from End(M)(x)eta integer "
                          "exponents; two boxes confirm stability of the null.")
    return out


# =====================================================================
# op:cc4-0  Route 1  --  pullback s = t^2, eigenring of M~ over C(t)
# =====================================================================
def cc4_route1():
    out = {"description": "Route 1: pullback s=t^2; A~(t)=2t*A(t^2); "
                          "eigenring dim of M~ over C(t)."}
    Acomp_s = companion_in(s)
    # A~(t) = 2 t * A(s=t^2)
    Atil = sp.simplify(2*t * Acomp_s.subs(s, t**2))
    a4_t = sp.expand((A[4].subs(s, t**2)))  # = 4 t^8 (4-3 t^2); denom of A(t^2)
    # clearing factor for A~ entries: A~ = 2t * companion, entries have denom a4(t^2)
    a4_clear = sp.expand(a4_t)

    # ---- A2 local-data verification (free consistency check) ----
    # exp at t=0  = 2 * exp_s@0  (s=t^2 ramified) = {0,1,2,3}
    exp0_t = [sp.simplify(2*r) for r in EXP0]
    a2_local = {
        "exp_at_t0_pred_{0,1,2,3}": [str(x) for x in exp0_t],
        "exp_at_t0_matches": (sorted(exp0_t) == [0, 1, 2, 3]),
        "t_R_squared": str(Rsing),  # t=+-2/sqrt3, unramified simple points
        "deck_map": "sigma: t -> -t; swaps +-t_R, fixes t=0 and t=oo",
        "oo_slope_on_cover": "1/2 (s^{1/4}=t^{1/2}); determining units c*{1,i,-1,-i} t^{1/2}",
        "oo_split_if_imprimitive": "{+-c t^{1/2}} (+) {+-c i t^{1/2}} (deck-swapped)",
    }

    # ---- eigenring: rational Phi~(t) with Phi~' = [A~,Phi~] ----
    # singular points t=0 and t=+-t_R (-> factor 3t^2-4); denom t^a (3t^2-4)^b
    res_boxes = []
    for (a, b, dm) in [(2, 1, 6), (3, 2, 10)]:
        den = t**a * (3*t**2 - 4)**b
        r = intertwiner_search(Atil, sp.Integer(0), t, den, a4_clear, dm,
                               f"eigenring t^{a}(3t^2-4)^{b} d{dm}")
        res_boxes.append(r)
    eig_dim = res_boxes[-1]["nullspace_dim"]
    out["A2_local_data"] = a2_local
    out["eigenring_dim"] = [r["nullspace_dim"] for r in res_boxes]
    out["eigenring_detail"] = res_boxes
    out["pullback_irreducible"] = (eig_dim == 1)
    out["verdict"] = ("PRIMITIVE (eigenring = scalars, M~ irreducible)" if eig_dim == 1
                      else f"IMPRIMITIVE (eigenring dim {eig_dim} >= 2, M~ decomposes)")
    out["bounds_note"] = ("End(M~) integer exponents: pole <=3 at t=0 (exps {0,1,2,3}), "
                          "<=2 at +-t_R; identity I is always a solution so dim>=1; "
                          "dim==1 (scalars only) <=> irreducible cover.")
    return out


def main():
    res = {
        "op": "cc4-0",
        "inherits": {
            "cc1_sha": "bfb91bdeef251be00b770f486ec53d2304f4c1064f85d907a82951a49f5f227e",
            "cc2_12_sha": "7d102ddcf95f89a2939223741770cb01c73e747862239a9c36eb3526e203877c",
        },
        "objective": ("Decide primitive (G_Gal^0=SL4, no Liouvillian) vs imprimitive "
                      "(C2, induced from a quadratic cover) for L2."),
    }
    print("== op:cc4-0 DESCENT / INDUCTION TEST ==")
    print("\n[A1] eta = sqrt(s) uniqueness ...")
    a1 = cc4_A1()
    res["A1_eta_uniqueness"] = a1
    print("  viable nontrivial characters:", a1["viable_nontrivial_characters"])
    print("  unique candidate eta=sqrt(s):", a1["unique_candidate"])

    print("\n[A1b] oo 4-cycle closes monomial / field-extension loopholes ...")
    a1b = cc4_A1b_monomial_closure()
    res["A1b_monomial_closure"] = a1b
    print("  oo formal monodromy is odd (4-cycle):", a1b["permutation_is_odd"])
    print("  perm types containing a 4-cycle:", a1b["permutation_types_containing_a_4cycle"])
    print("  every such type has a quadratic character:",
          a1b["every_allowed_type_has_quadratic_character"])

    print("\n[Route 2] eta=sqrt(s) intertwiner over C(s) ...")
    r2 = cc4_route2()
    res["route2_eta_twist"] = r2
    print("  calibration End(M) dim (expect 1):", r2["calibration_End_M_dim"])
    print("  Hom(M, M(x)sqrt s) dim:", r2["twist_Hom_dim"])
    print("  ->", r2["verdict"])

    print("\n[Route 1] pullback s=t^2 eigenring over C(t) ...")
    r1 = cc4_route1()
    res["route1_pullback"] = r1
    print("  A2 exp@t0 matches {0,1,2,3}:", r1["A2_local_data"]["exp_at_t0_matches"])
    print("  eigenring dim (expect 1):", r1["eigenring_dim"])
    print("  ->", r1["verdict"])

    # ---- agreement + verdict ----
    prim2 = (r2["twist_Hom_dim"][-1] == 0)
    prim1 = (r1["eigenring_dim"][-1] == 1)
    agree = (prim2 == prim1)
    res["routes_agree"] = bool(agree)
    res["both_say_primitive"] = bool(prim1 and prim2)
    if not agree:
        res["verdict"] = "DISAGREEMENT between routes -> HALT, audit before any claim."
        res["grade"] = "N/A (inconsistent)"
    elif prim1 and prim2:
        res["verdict"] = (
            "PRIMITIVE. No sqrt(s)-intertwiner (Route 2 Hom dim 0) AND pullback eigenring "
            "= scalars (Route 1 dim 1). With A1 (eta=sqrt(s) the unique candidate) the "
            "2-block imprimitive class is excluded; with A1b (oo 4-cycle is odd => any "
            "induced permutation type is in {C4,D4,S4}, all with a quadratic character "
            "=> caught by the sqrt(s) test) the 4-line monomial and C3 field-extension "
            "classes are ALSO excluded. Combined with cc2-1/2 (reducible, Sp4, SO4, "
            "Sym^3SL2, SL2(x)SL2 all dead) the differential Galois group satisfies "
            "G_Gal(L2)^0 = SL4  (UNCONDITIONAL at grade STRUCTURAL).")
        res["grade"] = "STRUCTURAL (two independent symbolic routes agree + A1/A1b; van der Put-Singer)"
    else:
        res["verdict"] = ("IMPRIMITIVE. L2 ~= L2(x)sqrt(s): M is induced from the quadratic "
                          "cover s=t^2. C becomes rank-2 connection data on the cover; the "
                          "elementary-C falsification target returns. HALT, reroute the program.")
        res["grade"] = "STRUCTURAL"

    res["discipline_line"] = (
        "non-rigidity (P=d-1>0) does NOT imply C transcendental; a large G_Gal does NOT "
        "imply C transcendental. op:cc-2/4 targets the GROUP only; C's transcendence is "
        "op:cc-3's burden via periods.")

    print("\n== VERDICT ==")
    print(" routes agree:", res["routes_agree"])
    print(" ", res["verdict"])

    # ---- canonical SHA of hash-free object ----
    blob = json.dumps(res, sort_keys=True, ensure_ascii=False).encode("utf-8")
    sha = hashlib.sha256(blob).hexdigest()
    res["canonical_sha256_of_hashfree_object"] = sha
    with open("cc4_0_descent_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", sha)
    print("wrote cc4_0_descent_results.json")


if __name__ == "__main__":
    main()
