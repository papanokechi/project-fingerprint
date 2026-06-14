#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-3-3  EPISTEMIC CLOSE-OUT

Final four-class table for the entire cc program (cc-1 -> cc3-3), the discipline
line in its final form, and the readiness paragraph for op:ebr4-assemble.

Reads the MAIN ledger claims_cc.jsonl (read-only) and injects the five new
cc3-S6/cc3-3 claims of THIS stage, then buckets every claim into exactly one
headline class for the program table.  Reproducible: emits a hash.
"""
import sys, json, hashlib, collections
sys.stdout.reconfigure(encoding="utf-8")

def canon_sha(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

# the five new claims appended by this summit stage (cc3-S6 + cc3-3)
NEW_CLAIMS = [
    ("CC3-S6-PMAT", "STRUCTURAL+VERIFIED"),
    ("CC3-S6-CLOSE", "STRUCTURAL"),
    ("CC3-3-LOCUS", "STRUCTURAL+VERIFIED"),
    ("CC3-3-CONDITIONAL", "CONJECTURED (conditional theorem)"),
    ("CC3-3-CLOSEOUT", "VERIFIED"),
]

def bucket(grade):
    g = grade.upper()
    if "PROVEN" in g:
        return "PROVEN"
    if g.startswith("CONJECTURED"):
        return "CONJECTURED"
    if "STRUCTURAL" in g:
        return "STRUCTURAL"
    return "VERIFIED"

def main():
    print("=== op:cc3-3-3  epistemic close-out ===\n")
    rows = []
    with open("claims_cc.jsonl", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            rows.append((o.get("claim_id", ""), o.get("grade", "")))
    n_ledger = len(rows)
    rows_all = rows + NEW_CLAIMS

    table = collections.OrderedDict([("PROVEN", []), ("STRUCTURAL", []),
                                     ("VERIFIED", []), ("CONJECTURED", [])])
    for cid, gr in rows_all:
        table[bucket(gr)].append({"claim_id": cid, "grade": gr})

    print(f"ledger claims read: {n_ledger}; + {len(NEW_CLAIMS)} new = {len(rows_all)} total\n")
    print("PROGRAM FOUR-CLASS TABLE (cc-1 -> cc3-3):")
    for cls, items in table.items():
        print(f"  {cls}: {len(items)}")
    print()
    print("  PROVEN (Lean v4.30.0 + Mathlib finitary cores):")
    for it in table["PROVEN"]:
        print(f"    - {it['claim_id']}")

    discipline_final = (
        "DISCIPLINE LINE (FINAL FORM): the transcendence of the EBR connection coefficient C, "
        "equivalently of the Stokes constant kappa = Gamma(4/3) C / sqrt(pi), remains CONJECTURED "
        "UNCONDITIONALLY -- it is NOT established at any grade by this program.  The op:cc3-3-2 "
        "conditional theorem (kappa not in Qbar under the Fresan-Jossen exponential period "
        "conjecture + the SL2 motivic-Galois identification + non-degeneracy) is the PROGRAM'S "
        "CEILING and says so.  The ceiling cuts both ways: the NOT-COVERED coverage verdict and "
        "the two extended PSLQ nulls prove nothing about transcendence, and a closed form (had one "
        "fired) would have argued ELEMENTARITY-in-extended-class, not transcendence."
    )

    readiness = {
        "target": "op:ebr4-assemble (EBR-IV paper)",
        "result_inventory": [
            "(1) REDUCTION: EBR generating function G / connection coefficient C reduces, via the OGF "
            "y(t) (3t^3 y''+10t^2 y'+(t^2+5t-1)y=-1) and its Borel-2 transform Phi (radius 1/3), to the "
            "rank-2 core H2 = 3t^3 D^2 + 10t^2 D + (t^2+5t-1) [cc3-1/1b/1c/2].",
            "(2) D8(1) SURFACE IDENTIFICATION under RULE S (selectors + Pade screen): VERIFIED, first "
            "VERIFIED Painleve-surface label in cc-3 [CC3-2S2-RULES, 6c8dd5ee].",
            "(3) SL2 / RIG-0: G_Gal(H2)=SL2 non-Liouvillian (exact Kovacic) [CC3-2-KOV]; rig(H2)=0 "
            "non-rigid, moduli dim 2 (Painleve phase space) [CC3-2S2-RIG].",
            "(4) RESURGENCE BRIDGE: kappa = Gamma(4/3) A0, A0 = C/sqrt(pi) (transfer theorem), exact "
            "[CC3-2S2-KAPPA-RES]; Channel A independent 60 d [CC3-2S2-KAPPA-NUM].",
            "(5) MONODROMY POINT on the dim-2 D8 character variety: (tr M0, kappa), tr M0 = -51.0655... "
            "hyperbolic/irreducible [CC3-2S2-2A-COORDS], kappa now computed to 129 d as the connection "
            "coefficient [CC3-S6-PMAT].",
            "(6) NOT-COVERED coverage verdict (ILT tau / GL Fredholm are tau-side; kappa is a Lax-side "
            "input never output) [CC3-2S2-2C-VERDICT].",
            "(7) TWO EXTENDED NULLS: 169-digit elementary/Gamma-quotient null on C [EBR3-B-*, 9a3f942d]; "
            "Barnes-G/Glaisher log-space null on log kappa, log A0 [CC3-2S2-3-BARNES, 1887c410].",
            "(8) S6 CLOSURE to STRUCTURAL: kappa is a CONSTRUCTIVE exponential period -- the connection "
            "coefficient A_Phi of the order-4 Borel operator L, computed to 129 d with 208/204 witnesses "
            "[CC3-S6-PMAT 56adcb10, CC3-S6-CLOSE 2cc2f6fb].",
            "(9) CONDITIONAL THEOREM + GAP LIST: kappa not in Qbar under the named conjecture + SL2 "
            "motivic identification + non-degeneracy; five-item graded gap list [CC3-3-CONDITIONAL "
            "1b15e7ac]; off-locus exclusion [CC3-3-LOCUS a6b8d588].",
        ],
        "lean_core_candidates_flagged": [
            "L-OPERATOR DATA: the explicit order-4 operator L (p0..p4) annihilating Phi, its singular "
            "set {0,1/3, inf-irregular slope 1/4}, and the indicial polynomials at 0 and 1/3 "
            "({0,0,1,1} / {-4/3,0,1,2}) -- a finitary symbolic identity, Lean-formalizable.",
            "GAUGE-CHAIN IDENTITY: the residual-0 chain H2 -> u''=ru -> (t=x^2) w''=Rw -> companion B, "
            "an exact rational-function identity [CC3-2S2-2B-DICT, 87be6028].",
            "KOVACIC CASE ARITHMETIC: the exhaustive emptiness of the Riccati polynomial system over "
            "Q(sqrt 3) (Case-2 imprimitive exclusion) -- a finite arithmetic certificate [CC3-2-KOV].",
            "DIM COUNTS: dim H^1_dR(H2)=2, dim H^1_dR(L)=5 (Deligne-Malgrange index) -- integer "
            "identities [CC3-2-DIM].",
            "TEMPLATE: the four cc4 Lean cores (CC4-LEAN-BOUNDS/PULLBACK/PARITY/A1B, PROVEN, Lean "
            "v4.30.0 + Mathlib rev c5ea0035) are the formalisation template.",
        ],
        "epistemic_delta_this_stage": "S6 moved CONJECTURED-with-architecture -> STRUCTURAL (constructive "
            "exponential-period realisation of kappa, 129 d); the program acquired its CEILING artifact "
            "(the conditional theorem) and its off-locus exclusion. No grade was upgraded to PROVEN "
            "(PROVEN remains the four cc4 Lean cores only). Unconditional transcendence unchanged: OPEN.",
    }

    obj = {
        "op": "cc3-3-3-epistemic-closeout",
        "task_id": "op:cc-transcendence/cc3-3",
        "claim_id": "CC3-3-CLOSEOUT",
        "grade": "VERIFIED",
        "ledger_claims_read": n_ledger,
        "new_claims_this_stage": NEW_CLAIMS,
        "program_four_class_table": {cls: {"count": len(items), "claim_ids": [it["claim_id"] for it in items]}
                                     for cls, items in table.items()},
        "discipline_line_final": discipline_final,
        "readiness_for_ebr4_assemble": readiness,
    }
    obj["canonical_sha256_of_hashfree_object"] = canon_sha(obj)
    with open("cc3_3_3_closeout_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

    print("\n" + discipline_final)
    print("\n  canonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("  wrote cc3_3_3_closeout_results.json")

if __name__ == "__main__":
    main()
