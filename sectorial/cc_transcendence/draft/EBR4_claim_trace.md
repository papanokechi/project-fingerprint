# EBR-IV — claim-trace table (op:ebr4-2)

Every load-bearing statement in the planned paper maps to exactly one `claim_id`
in `claims_cc.jsonl` (MAIN ledger, **92 claims**). **Rule:** any statement with
no `claim_id` either earns a new claim (with evidence) or is cut. This table is
the audit instrument for the ebr4-3 referee pass. Grades: P=PROVEN,
S=STRUCTURAL, V=VERIFIED, C=CONJECTURED.

**Headline grade reminder.** EBR-IV introduces **no new PROVEN item**. The only
machine-checked substrate in the program is the inherited EBR-III Lean cores
(cited in §9, not re-proven here); EBR-IV's own finitary identities are flagged
as Lean-core *candidates* (§11). The headline is a CONDITIONAL theorem (C).

| § | Load-bearing statement | claim_id | grade |
|---|---|---|---|
| 1 | Unconditional transcendence of C/κ is the open problem (CEILING) | CC1-DISCIPLINE | C |
| 1, 9 | The conditional theorem κ∉ℚ̄ under H1–H4 is the program ceiling | CC3-3-CONDITIONAL | C |
| 2.1 | PCF → OGF inhomog. ODE; rank-2 core H₂=3t³D²+10t²D+(t²+5t−1) | CC3-2-CORE-CHAIN | V |
| 2.1 | OGF ODE 3t³y″+10t²y′+(t²+5t−1)y=−1 (verified vs series) | CC3-1-OGF-ODE | S/V |
| 2.2 | Borel-2 Φ=ΣQₙzⁿ/(n!)²; order-4 L; sing {0,1/3}; z=∞ irreg slope 1/4 | CC3-S6-PMAT | S/V |
| 2.2 | Φ holonomic, the order-4 ODE for Φ (θ-form) | CC3-1-PHI | S/V |
| 2.3 | z=1/3 is a Borel-plane singularity; κ a Stokes constant; κ=Γ(4/3)A₀ | CC3-2S2-KAPPA-RES | S |
| 2.3 | κ numeric = Γ(4/3)A₀ = Γ(4/3)C_EBR/√π, channels agree | CC3-2S2-KAPPA-NUM | V |
| 2.3 | κ←K rename (disambiguation; V_quad-K collision noted once) | CC3-2S2-REN | V |
| 3.1 | H₂ formal data: {0,∞} both irregular slope ½ ram 2; r(t) | CC3-2-CORE-LOCAL | V |
| 3.2 | rig(H₂)=0 ⇒ NON-RIGID, moduli dim 2, accessory P=1; controls | CC3-2S2-RIG | V |
| 3.2 | accessory/non-rigidity convention (P=1, reconciles EBR-II) | CC3-2-CONV-1 | V |
| 3.3 | RULE S ⇒ PIII(D₈)=D₈⁽¹⁾ uniquely; Padé screen z=1/3 ~34 d | CC3-2S2-RULES | V |
| 4.1 | G_Gal(H₂)=SL₂, NON-LIOUVILLIAN (Kovacic, 3 cases, ℚ(√3) empty) | CC3-2-KOV | S |
| 4.1 | symmetric-DCHE normal form (two rank-1 irregular pts) | CC3-2-NF | S |
| 4.3, 9 | Discipline line: SL₂/non-rigidity do NOT imply κ transcendental | CC1-DISCIPLINE | C |
| 5.1 | Monodromy spectral projector ⇒ A_Φ=κ to 129 d; witnesses | CC3-S6-PMAT | S/V |
| 5.2 | κ-bridge: scalar gauge ⇒ s\*=A_Φ=Γ(4/3)A₀=κ (S6 → STRUCTURAL) | CC3-S6-CLOSE | S |
| 5.2 | κ=Γ(4/3)A₀ exact (Flajolet–Sedgewick transfer); Channel A 60 d | CC3-2S2-KAPPA-RES | S |
| 5.3 | Integrand chain S1–S6 (I₀ kernel = exp period; Borel-2 summ.) | CC3-2S2-KAPPA-RES | S |
| 6.1 | tr(M₀)=−51.0655631399546… hyperbolic SL₂ irreducible; dim-2 pt | CC3-2S2-2A-COORDS | V |
| 6.1 | integrator-bug methodology (15-dps mpf hazard; range bug) | CC3-2S2-2A-METH | V |
| 6.2 | gauge dictionary H₂→B=[[0,1],[R,0]] (D₈ shape, symmetric DCHE) | CC3-2S2-2B-DICT | S |
| 6.3 | Coverage verdict (iii) NOT COVERED; tau-vs-Lax named hazard | CC3-2S2-2C-VERDICT | V |
| 7.1 | 169-d elementary null: not Γ-quotient/const-combo/algebraic | EBR3-B-GAMMA, EBR3-B-CONST, EBR3-B-ALG | V |
| 7.1 | (κ↔C_EBR identity tying the frozen C-null to κ) | CC3-1B-K-120D | V |
| 7.2 | Barnes-G/Glaisher log-space null; control G(1/2) fires | CC3-2S2-3-BARNES | V |
| 7.3 | NULL-DISCIPLINE rule (tol_dps≫(deg+1)log₁₀H; twice load-bearing) | EBR4-METH-NULLDISC | V |
| 8.1 | Stratum (R) reducible/Riccati EXCLUDED UNCONDITIONALLY (SL₂) | EBR4-1-LOCUS-DIRECT | V/S |
| 8.2 | Stratum (A) q=c√t: tr M₀ PSLQ-NULL deg≤4 @H≤10¹⁰; G5 HARDENED | EBR4-1-LOCUS-DIRECT | V/S |
| 8 | (prior off-locus: |tr M₀|−2=49.07, infinite order) | CC3-3-LOCUS | S/V |
| 9.1 | Named conjecture (Fresán–Jossen exp-period) verbatim, located | CC3-3-CONDITIONAL | C |
| 9.2 | H2⊥H3 verdict (iii); differential→motivic comparison explicit | EBR4-0-HYP | V |
| 9.3 | **THEOREM (CONDITIONAL)** verbatim re-graded ebr4-0 form (②) | CC3-3-CONDITIONAL, EBR4-0-HYP | C |
| 9.4 | G3 two-distinct-facts: κ=A_Φ identified & nonzero (V) vs non-alg (concl.) | EBR4-1-LOCUS-DIRECT | V |
| 9.5 | GAP LIST hardened: G1 + G2/G4 merged + G5 residual | EBR4-0-HYP, EBR4-1-LOCUS-DIRECT | V |
| 9.6 | CEILING box both ways | CC1-DISCIPLINE | C |
| 10 | Four-class grade table | CC3-3-CLOSEOUT | V |
| 11 | Open problems incl. Lean-core candidates, full G5 close, synthesis | CC3-3-CLOSEOUT | V |
| A | Relationship to EBR-II (κ home = exp periods, not classical KZ) | CC3-1B-RESCOPE | V |

**Coverage check.** Every planned load-bearing statement maps to a ledger
`claim_id`. New EBR-IV-stage claims used: `EBR4-0-HYP`, `EBR4-1-LOCUS-DIRECT`,
`EBR4-METH-NULLDISC` (defined this op:ebr4-assemble; hashes `d86256cc`,
`dae56db4`, ledger entry resp.). All cc3-* are inherited and frozen-in-content.

**Claims deliberately NOT cited in the body (intentional, with reason).**
- `CC3-2S2-EXPPER` (CONJECTURED-with-architecture) — the **superseded**
  intermediate ("κ exp-period, pairing not yet built"); the paper cites its
  STRUCTURAL replacement `CC3-S6-CLOSE`. Citing the precursor would misstate the
  status. (Mirror of the EBR-III `CC2-2E-VERDICT` disposition.)
- The cc3-0 / cc3-1 / cc3-1c arithmetic-location claims (`CC3-0-P3`,
  `CC3-1-INTREP`, `CC3-1C-RIGIDITY`, `CC3-4A-KPSLQ`, …) — **background corpus**;
  their substance (Φ holonomic, L irregular, κ not polylog-elementary, L
  non-rigid) is folded into §2/§3/§7 wherever load-bearing, but the per-step
  claims are not individually cited (they are the route, not the result). Listed
  here so the omission is explicit, not silent.

**Statements deliberately NOT made (forbidden-string guard).** "κ is
transcendental"; "we prove transcendence"; "κ is a period" / "C is a period"
(unconditional — exp-period membership is STRUCTURAL-constructive, full motivic
membership is CONJECTURED, §9 G2/G4); "SL₂ implies transcendence";
"non-rigidity implies transcendence"; any unqualified ℚ̄ statement. The
unconditional result is **non-membership-pending-conjecture**.
