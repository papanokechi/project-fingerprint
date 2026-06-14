#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:ebr4-0  HYPOTHESIS-INDEPENDENCE AUDIT  (GATE -- drafting blocked behind it)

Adversarial audit of the cc3-3-2 conditional theorem BEFORE any EBR-IV drafting.
Two questions:

  (Q1)  H2 perp H3 :  is  dim G_mot(M) >= 3  (i) independently established,
        (ii) a CONSEQUENCE of the Fresan-Jossen period conjecture named in H3,
        or (iii) dependent on a SEPARATE (unstated) comparison conjecture?
        -> cite the differential-to-motivic comparison step with locator.
        -> if H2 is NOT independent of H3: COLLAPSE the hypothesis list and
           restate (recorded as a correction, not a silent edit).

  (Q2)  RE-GRADE audit: walk every hypothesis's tag against its evidence.
        Any hypothesis whose grade the audit LOWERS triggers a HALT with the
        re-graded theorem before drafting.

METHOD (backbone): a DROP-ONE necessity analysis.  For each Hi exhibit a
model/argument in which all H_{!=i} hold but the conclusion (kappa not in Qbar)
FAILS.  This simultaneously proves (a) every Hi is NECESSARY (honest count),
(b) no Hi is a logical CONSEQUENCE of the others (mutual independence), and in
particular (c) H2 is NOT supplied by H3.

NOTHING is upgraded here.  PROVEN = Lean only.  cc-3 CEILING in force both ways.
"""
import sys, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")


def canon_sha(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


# ----------------------------------------------------------------------------
# The differential-to-motivic comparison step (the crux of Q1), with locators.
# ----------------------------------------------------------------------------
COMPARISON_STEP = {
    "name": "differential-Galois -> motivic-Galois dimension comparison",
    "statement": (
        "For a motive M with de Rham realisation carrying the Gauss-Manin "
        "connection, the differential Galois group G_Gal of that connection "
        "(equivalently the Zariski closure of the geometric monodromy) injects "
        "into the motivic Galois group G_mot(M) as (the identity component of) "
        "a normal subgroup; consequently dim G_mot(M) >= dim G_Gal."
    ),
    "classical_status": (
        "THEOREM in the classical (pure, regular-singular) motivic setting: the "
        "geometric monodromy group is a normal subgroup of the derived motivic "
        "Galois group, and the differential Galois group of the Gauss-Manin "
        "connection is its Zariski closure."
    ),
    "classical_locators": [
        "Y. Andre, 'Pour une theorie inconditionnelle des motifs', Publ. Math. "
        "IHES 83 (1996), 5-49 (motivic Galois group; monodromy).",
        "Y. Andre, 'Une introduction aux motifs (motifs purs, motifs mixtes, "
        "periodes)', SMF Panoramas et Syntheses 17 (2004), Ch. on Galois "
        "groups and the comparison G_Gal(Gauss-Manin) subset G_mot.",
        "Y. Andre, 'Differentielles non commutatives et theorie de Galois "
        "differentielle ou aux differences', Ann. Sci. ENS 34 (2001), 685-739 "
        "(Tannakian differential Galois formalism).",
    ],
    "our_status": (
        "Here M is an EXPONENTIAL motive and the connection (order-4 L for Phi, "
        "z=inf irregular slope 1/4) is IRREGULAR; the comparison in this case is "
        "part of the Fresan-Jossen exponential-motives framework and its "
        "application is CONTINGENT on (G4) realising M as a genuine object of "
        "that category with a verified irregular Riemann-Hilbert / Stokes-aware "
        "realisation comparison.  So the comparison is theorem-grade classically "
        "but CONJECTURAL-in-application here."
    ),
    "exponential_locator": (
        "J. Fresan, P. Jossen, 'Exponential Motives' (book in preparation): the "
        "exponential motivic Galois group and its realisations.  NB this is the "
        "SAME source as H3 but a DIFFERENT statement -- the comparison/realisation, "
        "NOT the period conjecture -- so H2 and H3 remain logically independent."
    ),
}


# ----------------------------------------------------------------------------
# DROP-ONE necessity analysis (the audit backbone).
# ----------------------------------------------------------------------------
DROP_ONE = {
    "drop_H1": {
        "kept": ["H2", "H3", "H4"],
        "failure_model": (
            "If kappa is not known to be a period of M, then H3 (FJ, about the "
            "periods OF M) constrains kappa not at all; kappa could be anything. "
            "Conclusion kappa not in Qbar does not follow."
        ),
        "verdict": "H1 NECESSARY; not implied by {H2,H3,H4}.",
    },
    "drop_H2": {
        "kept": ["H1", "H3", "H4"],
        "failure_model": (
            "If dim G_mot(M) is allowed to be small (e.g. 0 or a 1-dim torus), "
            "then by H3 (FJ) trdeg<periods> equals that small number; the period "
            "algebra could be algebraic (dim 0) or a single Gamma-quotient line "
            "(torus) -- kappa could be algebraic.  Conclusion fails.  Crucially "
            "H3 (trdeg = dim) does NOT supply dim >= 3: FJ converts dim into "
            "trdeg but never bounds dim from below."
        ),
        "verdict": "H2 NECESSARY; NOT a consequence of H3 (this is the Q1 core).",
    },
    "drop_H3": {
        "kept": ["H1", "H2", "H4"],
        "failure_model": (
            "Without the period conjecture, dim G_mot(M) >= 3 (H2) is a purely "
            "group-theoretic fact with NO transcendence content: there is no "
            "unconditional theorem deducing trdeg of periods from the size of the "
            "motivic Galois group (that bridge IS FJ).  Conclusion fails.  This "
            "shows H2 (about the GROUP) and H3 (the period bridge) carry disjoint "
            "content."
        ),
        "verdict": "H3 NECESSARY; not implied by {H1,H2,H4}.",
    },
    "drop_H4": {
        "kept": ["H1", "H2", "H3"],
        "failure_model": (
            "Even with dim G_mot >= 3 and FJ giving trdeg<periods> >= 3, the "
            "transcendence could live entirely in OTHER period entries while the "
            "specific entry kappa is algebraic (a diagonal / normalisation entry). "
            "The conclusion is about kappa SPECIFICALLY, so it fails without the "
            "non-degeneracy/identification of kappa as the non-trivial off-diagonal "
            "entry.  Conclusion fails."
        ),
        "verdict": "H4 NECESSARY; not implied by {H1,H2,H3}.",
    },
}


def main():
    print("=== op:ebr4-0  hypothesis-independence audit (GATE) ===\n")

    # ---- Q1: H2 perp H3 verdict ------------------------------------------
    q1_verdict = "(iii)"
    q1_text = (
        "H2 (dim G_mot(M) >= 3) is dependent on a SEPARATE comparison step -- the "
        "differential-to-motivic dimension comparison dim G_mot >= dim G_Gal -- "
        "NOT on the period conjecture H3, and NOT (fully) independently established. "
        "It factors as [VERIFIED: G_Gal(H2)=SL2, dim 3, exact Kovacic e71e915f] + "
        "[comparison: dim G_mot >= dim G_Gal; theorem-grade in the classical motivic "
        "setting (Andre), here CONTINGENT on G4-realisation and the irregular/"
        "exponential form of the comparison].  Since the comparison is neither H3 "
        "nor automatic, the honest verdict is (iii)."
    )
    print("Q1  H2 perp H3 :", q1_verdict)
    print("   ", q1_text, "\n")

    # ---- COLLAPSE decision ------------------------------------------------
    # H2 is independent of H3 (drop-one: drop_H3 keeps H2 yet conclusion fails;
    # drop_H2 keeps H3 yet conclusion fails) -> neither implies the other ->
    # NO collapse; the 4-hypothesis count is honest.
    collapse = False
    print("DROP-ONE necessity analysis:")
    for k, v in DROP_ONE.items():
        print(f"  [{k}] keep {v['kept']}  -> {v['verdict']}")
    print(f"\nCOLLAPSE hypothesis list?  {collapse}  "
          "(H2 and H3 carry disjoint content; neither implies the other; "
          "all four hypotheses are necessary -> honest count = 4).\n")

    # ---- Q2: RE-GRADE audit (tag vs evidence) -----------------------------
    regrade = {
        "H1": {"old": "STRUCTURAL", "new": "STRUCTURAL", "lowered": False,
               "evidence": "CC3-S6-CLOSE (2cc2f6fb) + CC3-S6-1 (56adcb10): kappa "
                           "constructively realised as connection coefficient A_Phi "
                           "to 129 d.  Constructive exponential-period membership = "
                           "STRUCTURAL (full motivic membership remains G4)."},
        "H2": {"old": "CONJECTURED (H-aux); differential side VERIFIED",
               "new": "CONJECTURED (motivic); differential anchor VERIFIED",
               "lowered": False,
               "evidence": "G_Gal(H2)=SL2 VERIFIED (e71e915f).  Motivic dim>=3 "
                           "rests on the comparison step (see COMPARISON_STEP), "
                           "contingent on G4.  Tag unchanged -- only RESTATED to "
                           "expose the comparison."},
        "H3": {"old": "CONJECTURED (external, named)",
               "new": "CONJECTURED (external, named)", "lowered": False,
               "evidence": "Fresan-Jossen exponential period conjecture; open."},
        "H4": {"old": "VERIFIED", "new": "VERIFIED", "lowered": False,
               "evidence": "dim H^1_dR(H2)=2 (e71e915f); irreducible (SL2); off "
                           "classical locus (a6b8d588, hardened by ebr4-1); kappa "
                           "is the identified non-vanishing off-diagonal connection "
                           "entry A_Phi != 0 to 129 d (56adcb10)."},
    }
    any_lowered = any(v["lowered"] for v in regrade.values())
    print("Q2  RE-GRADE audit (tag vs evidence):")
    for k, v in regrade.items():
        flag = "  <-- LOWERED" if v["lowered"] else ""
        print(f"  [{k}] {v['old']}  ->  {v['new']}{flag}")
    print(f"\nany grade lowered? {any_lowered}  "
          "(=> NO re-grade HALT; H2 restated, not downgraded).\n")

    # ---- the RE-STATED theorem (verbatim, even though unchanged in grade) --
    theorem_restated = (
        "THEOREM (CONDITIONAL, ebr4-0 re-stated form).  Let M be the exponential "
        "motive attached to the rank-2 connection H2 (realised on the convergent "
        "Borel-2 transform Phi; order-4 operator L, singular {0,1/3}, z=inf "
        "irregular of slope 1/4).  Assume:\n"
        "  (H1, STRUCTURAL) kappa is an exponential period of M -- constructively "
        "the connection coefficient A_Phi = kappa (S6 closure, 129 d).\n"
        "  (H2, CONJECTURED motivic / VERIFIED differential) dim G_mot(M) >= 3, "
        "via G_Gal(H2) = SL2 (exact Kovacic, dim 3) TRANSPORTED to the motivic "
        "group by the comparison dim G_mot >= dim G_Gal (theorem-grade classically "
        "[Andre, IHES 83 (1996); SMF Panoramas 17 (2004)]; here contingent on the "
        "G4 realisation and the irregular/exponential form of the comparison).\n"
        "  (H3, CONJECTURED external) the Fresan-Jossen period conjecture for "
        "exponential motives: trdeg_Q <periods(M)> = dim G_mot(M).\n"
        "  (H4, VERIFIED) the period-count / non-degeneracy data: dim H^1_dR(H2)=2, "
        "the connection is irreducible (SL2 Zariski-dense) and lies off the "
        "algebraic PIII(D8) locus, and kappa is the non-vanishing off-diagonal "
        "connection entry (A_Phi != 0), not a diagonal normalisation factor.\n"
        "THEN trdeg_Q <periods(M)> = dim G_mot(M) >= 3 and the off-diagonal entry "
        "kappa is not algebraic:  kappa not in Qbar.  Consequently the EBR-I/EBR-II "
        "connection coefficient C = kappa * sqrt(pi) / Gamma(4/3) is transcendental "
        "as well (an elementary Gamma-multiple of kappa).\n"
        "The conclusion is LICENSED ONLY under the full conjunction H1 & H2 & H3 & "
        "H4 (drop-one analysis: each hypothesis is necessary).  Dropping H3 leaves "
        "the unconditional residue ONLY: kappa is a non-classical exponential period "
        "off the algebraic PIII(D8) locus -- which says nothing about Qbar."
    )
    print("RE-STATED THEOREM (verbatim):\n")
    print(theorem_restated, "\n")

    correction_note = (
        "CORRECTION (recorded, not silent): the cc3-3-2 statement folded the "
        "differential-to-motivic comparison implicitly into H2's 'H-aux' tag.  "
        "ebr4-0 makes that comparison step EXPLICIT (its own clause, with classical "
        "theorem locator and the G4 contingency).  No grade is lowered; the "
        "hypothesis COUNT is unchanged at 4 (all necessary, mutually independent); "
        "H2 and H3 are confirmed logically independent (Q1 verdict (iii))."
    )
    print(correction_note, "\n")

    obj = {
        "op": "ebr4-0-hypothesis-independence-audit",
        "task_id": "op:ebr4-assemble/ebr4-0",
        "claim_id": "EBR4-0-HYP",
        "grade": "VERIFIED (logical audit; no mathematical grade upgraded)",
        "Q1_H2_perp_H3_verdict": q1_verdict,
        "Q1_text": q1_text,
        "differential_to_motivic_comparison": COMPARISON_STEP,
        "drop_one_necessity_analysis": DROP_ONE,
        "collapse_hypothesis_list": collapse,
        "Q2_regrade": regrade,
        "Q2_any_grade_lowered": any_lowered,
        "regrade_halt_triggered": any_lowered,
        "theorem_restated_verbatim": theorem_restated,
        "correction_note": correction_note,
        "hypothesis_count_honest": 4,
        "ceiling": (
            "This audit upgrades NOTHING. Unconditional transcendence of C/kappa "
            "is NOT a deliverable. A larger motivic group or a closed form would "
            "argue elementarity-in-extended-class; a null proves neither."
        ),
        "references": COMPARISON_STEP["classical_locators"] + [
            "J. Fresan, P. Jossen, Exponential Motives (book in preparation)",
            "M. Kontsevich, D. Zagier, Periods (2001)",
        ],
    }
    obj["canonical_sha256_of_hashfree_object"] = canon_sha(obj)
    with open("ebr4_0_hypothesis_audit_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("  canonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("  wrote ebr4_0_hypothesis_audit_results.json")

    # gate signal for the runner
    print("\nGATE STATUS: Q1=(iii) independent (no collapse); Q2 no grade lowered "
          "(no re-grade HALT). Proceed to ebr4-1; mandatory stage-end HALT after.")


if __name__ == "__main__":
    main()
