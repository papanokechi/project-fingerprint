#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1c-1  --  L <-> L2 RELATION TEST  (projective equivalence under z = s/4)
================================================================================
SIARC.  Decides whether Phi's operator L (radius 1/3) is projectively equivalent
to the pullback of the EBR Borel operator L2 (radius 4/3) under the affine change
s = 4 z, i.e. whether the cc4 result (irreducibility, G_Gal^0 = SL4) TRANSFERS to L.

Invariant used (NECESSARY condition for projective equivalence + affine pullback):
  * an affine change of variable s = 4 z is a biholomorphism near each finite
    singular point and at infinity preserves slopes/ramification; it does NOT
    change local exponents;
  * a projective (gauge) equivalence  y -> g(z) y  shifts ALL exponents at a given
    singular point by ONE common constant alpha_x = ord_x(g);
  * hence the multiset of exponents MODULO Z at each corresponding singular point
    is invariant UP TO a single uniform shift.  If at some point no uniform shift
    matches the two residue-multisets, the operators are NOT equivalent.

Local data (frozen inputs):
  L2 :  s=0   exponents {0, 1/2, 1, 3/2}              (cc1/cc2)
        s=4/3 exponents {0, 1, 2, -11/6}              (dominant -11/6)
        s=inf slope 1/4, ramification 4, edge c^4 = -1/12
  L  :  z=0   exponents {0, 0, 1, 1}                  (cc3-1b; Jordan [2,2])
        z=1/3 exponents {-4/3, 0, 1, 2}               (dominant -4/3)
        z=inf slope 1/4, ramification 4, edge lambda^4 = -256/3
Correspondence under s = 4 z :  s=0 <-> z=0,  s=4/3 <-> z=1/3,  s=inf <-> z=inf.

CEILING (reproduced): a Fuchsian relocation does not make K a classical period;
provenance, not singularity type, is what the period conjectures see.
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from fractions import Fraction as Fr

def residues_mod1(exps):
    return sorted([Fr(e) - Fr(int(Fr(e) // 1)) for e in exps])  # in [0,1)

def uniform_shift_match(expsA, expsB):
    """Is residue-multiset(B) a single uniform shift of residue-multiset(A)?
    Try every candidate shift = rB - rA[0] and see if it maps A's residues onto B's."""
    rA = residues_mod1(expsA)
    rB = residues_mod1(expsB)
    if len(rA) != len(rB):
        return False, None
    cand = set((rb - rA[0]) % 1 for rb in rB)
    for sh in cand:
        shifted = sorted([(r + sh) % 1 for r in rA])
        if shifted == rB:
            return True, sh
    return False, None

def diffs_multiset(exps):
    e = sorted(Fr(x) for x in exps)
    return sorted([e[j] - e[i] for i in range(len(e)) for j in range(i + 1, len(e))])

def main():
    print("=== cc3-1c-1  L <-> L2 projective-equivalence test (s = 4 z) ===")

    L2 = {
        "s=0":   ["0", "1/2", "1", "3/2"],
        "s=4/3": ["0", "1", "2", "-11/6"],
    }
    L = {
        "z=0":   ["0", "0", "1", "1"],
        "z=1/3": ["-4/3", "0", "1", "2"],
    }
    pairs = [("s=0", "z=0"), ("s=4/3", "z=1/3")]

    point_reports = []
    overall_equiv = True
    for (ps, pz) in pairs:
        eA = [Fr(x) for x in L2[ps]]
        eB = [Fr(x) for x in L[pz]]
        ok, sh = uniform_shift_match(eA, eB)
        rep = {
            "L2_point": ps, "L_point": pz,
            "L2_exponents": [str(x) for x in eA],
            "L_exponents": [str(x) for x in eB],
            "L2_residues_mod1": [str(x) for x in residues_mod1(eA)],
            "L_residues_mod1": [str(x) for x in residues_mod1(eB)],
            "L2_pairwise_diffs": [str(x) for x in diffs_multiset(eA)],
            "L_pairwise_diffs": [str(x) for x in diffs_multiset(eB)],
            "uniform_shift_match": ok,
            "matching_shift": str(sh) if ok else None,
        }
        point_reports.append(rep)
        print(f"\n[{ps} <-> {pz}]")
        print(f"   L2 exps {rep['L2_exponents']}  residues mod 1 {rep['L2_residues_mod1']}")
        print(f"   L  exps {rep['L_exponents']}  residues mod 1 {rep['L_residues_mod1']}")
        print(f"   uniform-shift match? {ok}" + (f" (shift {sh})" if ok else "  => MISMATCH"))
        if not ok:
            overall_equiv = False

    # infinity: slopes/ramification match (1/4, 4) but the edge coefficient does not
    # transform consistently.  Under s = 4 z a slope-1/4 exponential exp(c s^{1/4})
    # becomes exp(c (4z)^{1/4}) = exp(c 4^{1/4} z^{1/4}), so the quartic edge invariant
    # scales by 4: c^4 -> 4 c^4 = 4*(-1/12) = -1/3.  L's actual edge is lambda^4 = -256/3.
    c4_L2 = Fr(-1, 12)
    edge_transported = 4 * c4_L2           # = -1/3
    edge_L = Fr(-256, 3)
    edge_ratio = edge_L / edge_transported  # = 256 = 4^4
    inf_report = {
        "slope_L2": "1/4", "slope_L": "1/4", "ramification": 4, "slopes_match": True,
        "L2_edge_c4": str(c4_L2),
        "edge_after_s=4z_pullback": str(edge_transported),
        "L_edge_lambda4": str(edge_L),
        "edge_ratio_L_over_transported": str(edge_ratio),
        "edge_consistent": (edge_L == edge_transported),
        "note": "slopes match but the quartic edge invariant differs by a factor 4^4=256 => not the affine pullback's edge",
    }
    print("\n[s=inf <-> z=inf]")
    print(f"   slopes 1/4 = 1/4 (match); ramification 4 (match)")
    print(f"   L2 edge c^4 = {c4_L2}; after s=4z -> {edge_transported}; L edge lambda^4 = {edge_L}")
    print(f"   edge ratio = {edge_ratio} (= 4^4)  => edge INCONSISTENT with affine pullback")
    if not inf_report["edge_consistent"]:
        overall_equiv = False

    verdict = "EQUIVALENT" if overall_equiv else "NOT EQUIVALENT"
    print("\n=== VERDICT:", verdict, "===")
    decisive = ("Decisive: at the origin L2 has exponents {0,1/2,1,3/2} (residues mod 1 "
                "{0,1/2,0,1/2}) whereas L has {0,0,1,1} (residues {0,0,0,0}); no uniform "
                "shift maps one multiset to the other, so L is NOT the affine pullback of "
                "L2 up to gauge.  L2 and L are HADAMARD-QUOTIENT partners (g_n=Q_n/(2n)! vs "
                "phi_n=Q_n/(n!)^2, ratio binom(2n,n)), not substitution-related.")
    print(decisive)

    # Consequence: irreducibility of L does NOT transfer from cc4; argue it directly.
    irred_arg = ("L's irreducibility (own argument): at z=inf the formal connection has a "
                 "single slope 1/4 with ramification 4 and the four exponential determinations "
                 "lambda*zeta_4^k (lambda^4 = -256/3) form ONE Galois orbit under the ramified "
                 "Z/4 cover (cyclic permutation of the 4 branches).  A nonzero proper "
                 "subconnection over C(z) would have a formal type at infinity stable under "
                 "this Z/4 action and of rank < 4; but the orbit is transitive on all four "
                 "exponentials, so no proper subset is stable.  Hence the C(z)-connection has "
                 "no proper subobject => L is IRREDUCIBLE.  (Same slope-1/4/ram-4 transitivity "
                 "route as cc-1 used for L2.)  STRUCTURAL.")
    print("\n" + irred_arg)

    obj = {
        "op": "cc3-1c-1",
        "task_id": "op:cc-transcendence/cc3-1c",
        "test": "projective (gauge) equivalence of L vs pullback of L2 under s = 4 z",
        "invariant": "exponents mod Z at each corresponding singular point, up to one uniform shift; slopes/ramification/edge at infinity",
        "finite_points": point_reports,
        "infinity": inf_report,
        "verdict": verdict,
        "equivalent": overall_equiv,
        "decisive_reason": decisive,
        "consequence": ("cc4's irreducibility & G_Gal^0=SL4 do NOT transfer to L by equivalence; "
                        "L's irreducibility is argued directly below."),
        "irreducibility_of_L": irred_arg,
        "relationship": ("L2 and L are Hadamard-quotient partners by binom(2n,n): "
                         "g_n = Q_n/(2n)! (operator L2), phi_n = Q_n/(n!)^2 (operator L), "
                         "g_n = phi_n / binom(2n,n). Hadamard quotient is not a pullback and "
                         "changes local exponents and rank structure."),
        "frozen_inputs": {
            "L2_exponents": L2, "L2_inf": "slope 1/4, ram 4, c^4=-1/12 (cc1/cc2)",
            "L_exponents": L, "L_inf": "slope 1/4, ram 4, lambda^4=-256/3 (cc3-1b)",
        },
        "ceiling": ("A Fuchsian relocation does not make K a classical period; provenance, "
                    "not singularity type, is what the period conjectures see. Unconditional "
                    "transcendence of C is NOT a deliverable of op:cc-3 at any grade."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1c_L_vs_L2_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1c_L_vs_L2_results.json")

if __name__ == "__main__":
    main()
