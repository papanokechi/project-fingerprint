# cc3-2 ENTRY DOSSIER — non-rigid branch (op:cc3-1c-3)

**Status:** first-class obstruction record + cc3-2 routing dossier.
**Branch trigger:** op:cc3-1c-2 verdict **rig(L) = 0, NON-RIGID** (derivation
`cc3_1c_rigidity.py`, canonical sha `845ee916336d834a5ee0d7c6cd86eb7c48914e03d8e27733a09affca36ea9d22`).
**Grade of this dossier:** STRUCTURAL where it reports computed local/formal data;
VERIFIED-by-citation where it cites literature theorems; the routing conclusion is
an obstruction report (admissible type (e)) — **no transcendence claim at any grade**.

> **CEILING (reproduced verbatim).** A large G_Gal does NOT imply C transcendental;
> an exponential-period classification does NOT imply C transcendental; only a
> named-conjecture conditional does. Unconditional transcendence of C is NOT a
> deliverable of op:cc-3 at any grade. *Extended (cc3-1c):* relocation to a
> regular-to-regular connection problem does not make K a classical period —
> provenance is exponential; rigidity, if found, sharpens the period home but
> proves no transcendence. Here rigidity is **absent**, which only weakens the
> available machinery further.

---

## 1. The operator and its three-point local data (frozen / computed this stage)

`L = z⁴(1−3z) D⁴ + (4z³−25z⁴) D³ + (2z²−47z³) D² − 15 z² D − z²`
(order 4; Φ(z)=Σ Qₙ zⁿ/(n!)², Qₙ=(3n²+n+1)Qₙ₋₁+Qₙ₋₂, Q₀=1, Q₁=5; radius 1/3).

| point | nature | exponents / formal type | Jordan (eig 1) | dim Z(formal) | source |
|-------|--------|--------------------------|----------------|---------------|--------|
| z = 0 | regular-singular | {0,0,1,1} integer, **LOG-CARRYING** | **[2,2]** | **8** | exact θ-Frobenius `4482b99a…`; monodromy corrob. `1547689b…` (rank(M₀−I)=2) |
| z = 1/3 | regular-singular | {−4/3, 0, 1, 2}; integer block **semisimple** [1,1,1] + isolated e^{−2πi/3} | [1,1,1] | 10 | numerical monodromy `1547689b…` (rank(M_{1/3}−I)=1) |
| z = ∞ | **IRREGULAR** | single slope 1/4, λ⁴ = −256/3, ramification 4 | (irreducible formal type) | 1 | cc3-1b Newton polygon `2d98e76…`; Irr(End)=3 = (12 nonzero pairwise diffs)·¼ |

**Correction logged (CC3-2-ERR-1).** The cc3-1c-0 working hypothesis "z=0 apparent
(M₀=I)" and the cc3-1b *HALT-summary / inherited-state* paraphrase "z=0 block
log-free" are **REFUTED** — z=0 carries logarithms (Jordan [2,2]). *(cc3-1b's report
body, REPORT_cc3_1bc.md §1, correctly anticipated partner logs; the claim
CC3-1B-LOGFREE scopes log-freeness to Φ@0 + the z=1/3 integer block, both confirmed
here. The over-generalization lived only in summary narration.)* The z=1/3 integer
block IS semisimple (cc3-1b correct there). The NON-RIGID verdict is unaffected: it
uses the verified dim Z(M₀)=8 from the exact θ-Frobenius.

## 2. Index of rigidity and accessory count (the obstruction record)

Irregular Euler-characteristic formula (Bloch–Esnault / Arinkin / Jakob–Yun):

```
rig = (2 − #S)·n² + Σ_x dim Z(formal)_x − Σ_x irr_x(End E),   rigid ⟺ rig = 2.
    = (2 − 3)·16 + (8 + 10 + 1) − 3
    = −16 + 19 − 3 = 0.
```

**rig(L) = 0 ⇒ NON-RIGID. Moduli dimension 2P = 2 − rig = 2 ⟹ accessory-parameter
count P = 1** (convention CC3-2-CONV-1: 2P = 2 − rig; reconciles with EBR-II's
P = d − 1 = 1 for L₂ at d = 2, which also has rig = 0 ⟹ P = 1).
Controls (`cc3_1c_rigidity.py`): Airy rig=2, ₂F₁ rig=2, Bessel rig=2 — all PASS.
Internal: L₂ (EBR Borel operator) also rig=0 (same pattern). L is irreducible
(single slope-¼ ramification-4 Galois orbit at ∞ ⇒ no proper global subconnection),
so rig ≤ 2 is the correct ceiling and rig=0 is meaningful (moduli dim 2, P=1 accessory parameter).

## 3. What NON-RIGIDITY forecloses (the routing consequence)

A **rigid** irregular connection can be *identified* inside a finite classified
catalogue and inherits that catalogue's period theorems. **L is not rigid**, so the
following identification routes are **CLOSED**:

- **Katz middle-convolution / hypergeometric catalogue** (Katz, *Rigid Local
  Systems*, Ann. Math. Stud. 139, 1996; and *Exponential Sums and Differential
  Equations*, Ann. Math. Stud. 124, 1990, for the irregular Kloosterman/Airy
  sheaves). These classify **rigid** objects up to middle convolution and twist.
  *Inapplicable:* a positive-dimensional accessory family (moduli dim 2, P=1) is not a single rigid orbit.
- **Jakob–Yun classification of rigid irregular connections.** Same obstruction:
  the classification is of the rigid locus only.
- **Group guard (moot here):** even had L been rigid, the Kloosterman sheaf Kl₄
  carries Sp₄, so an SL₄-monodromy target would have excluded Kl₄ — but L↔L₂ is
  **NOT EQUIVALENT** (cc3-1c-1, `90cdaed3…`), so cc4's SL₄ does not transfer and
  there is no group target to match anyway.

## 4. What Bessel-moment period theory WOULD apply to (and why not here)

Fresán–Sabbah–Yu develop *quadratic relations between Bessel moments* and period
structures for **specific rigid connections of Kloosterman/Bessel type** (J. Fresán,
C. Sabbah, J.-D. Yu, *Quadratic relations between Bessel moments*, Algebra & Number
Theory **17** (2023); and *Quadratic relations between periods of connections*).

- **THEOREM (literature, VERIFIED-by-citation):** for the symmetric-power Kloosterman
  connections, the periods (Bessel moments) satisfy explicit quadratic period
  relations and lie in a controlled period algebra.
- **ASSERTED-HERE (why it does not transfer):** L is (i) NON-RIGID and (ii) NOT
  equivalent to a Kloosterman/L₂ pullback (cc3-1c-1). The Broadhurst–Mellit
  Bessel-moment constants therefore do not provide an identification target; the
  cc3-4a Bessel-moment tier was **skipped by argument** for exactly this reason.

## 5. cc3-2 routing: the generic exponential-motives track

> **UPDATE (op:cc3-2 stage 1, CC3-2-NF — sharpens this section).** The rank-2 core
> H₂ (from CC3-1-OGF-ODE) is now classified: **G_Gal(H₂) = SL₂, non-Liouvillian**
> (CC3-2-KOV) and the normal form is **case (b): the symmetric doubly-confluent Heun
> equation (DCHE)** (CC3-2-NF, REPORT_cc3_2a.md). This gives the period construction a
> **concrete named target** — the DCHE rank-2 connection — so stage 2 is a *worked-example*
> **Hien rapid-decay pairing for rank 2**, not the open-ended generic build anticipated
> below. **Non-rigidity (rig L = 0) is unchanged**, so everything in §3–§4 (closed
> identification routes) still holds; what improves is only the explicitness of the object
> whose pairing must be built and numerically confirmed (≥100 digits, hashed) at cc3-2 stage 2.

> **UPDATE (op:cc3-2s2 stage 2, CC3-2S2-RULES / CC3-2S2-KAPPA-RES — supersedes the
> "rapid-decay pairing not yet built" line of §5 below).** Two refinements landed.
> **(i) RULE-S identification.** H₂ has singular set {0,∞} ONLY, **both irregular slope ½
> ramification 2**, so z=1/3 is NOT a singularity of H₂ — it is a **Borel-plane singularity
> (instanton action)** of the Gevrey-2 series y, and **κ (renamed from K, CC3-2S2-REN) is a
> Stokes-type constant**, not a two-point connection coefficient. The (ramified, ramified)
> local type uniquely selects **PIII(D₈) = Sakai surface D₈⁽¹⁾** among the rank-2 two-irregular-
> point Painlevé surfaces (D₆⁽¹⁾=(1,1), D₇⁽¹⁾=(2,1), D₈⁽¹⁾=(2,2)); this reaches **VERIFIED per
> RULE S** (computed selectors **+** the Padé screen reproducing z=1/3 to ~34 digits).
> rig(H₂)=0, moduli dim 2 (= Painlevé phase space). Cert `6c8dd5ee…`.
> **(ii) Exponential-period architecture (replaces "not yet built").** The pairing target is now
> explicit as the **S1–S6 integrand chain**: y Gevrey-2 (S1) → I₀-normalized Borel-2 transform
> Φ=y⊙I₀(2√z) (S2) → I₀(2√z)=(1/2πi)∮e^{x+z/x}dx/x is an **exponential period** (S3, THEOREM
> DLMF 10.9.19) → Hadamard contour pairing, divergent-y leg = Borel-2 summability (S4) →
> **κ = coeff of (1−3z)^{−4/3} in Φ = Γ(4/3)·A₀** (S5, the **bridge identity**, STRUCTURAL/exact
> via Flajolet–Sedgewick transfer) → "κ is an exponential period / Stokes constant" (S6,
> **CONJECTURED-with-architecture**; the rapid-decay-cycle pairing for the divergent-y leg is the
> remaining stage-2 Hien work). The bridge κ=Γ(4/3)A₀ is confirmed **independently to ~60 digits**
> (large-order channel A, uses only the Qₙ recurrence) and to ~129 digits via the frozen
> composition (channel B). Cert `8f52843c…`. **Non-rigidity is unchanged**: the PIII(D₈) label
> sharpens the *period home*, it does not open an identification-based transcendence route —
> consistent with the §6 169-digit nulls.

With identification routes closed, cc3-2 proceeds on the **generic** track:

- **Home (STRUCTURAL framing, not a theorem about C):** K is a connection
  coefficient of an **irregular** holonomic connection (slope ¼ at ∞), regular at
  the matched pair 0 → 1/3. By Katz, regular-singular geometric provenance fails,
  so the *classical* Kontsevich–Zagier period route is unavailable; the candidate
  home is **exponential periods / exponential motives** (Fresán–Jossen,
  *Exponential Motives*, manuscript).
- **THEOREM vs ASSERTED-HERE, per step:**
  - *THEOREM:* exponential motives form a Tannakian category with a period pairing;
    connection coefficients of algebraic-de-Rham / rapid-decay pairings are
    exponential periods (Fresán–Jossen, ch. on period pairing). VERIFIED-by-citation.
  - *ASSERTED-HERE (degrades to CONJECTURED-with-architecture):* that **K specifically**
    is realized as such a pairing for L requires building the rapid-decay cycle and
    the algebraic de Rham class for L explicitly — **not yet done**. This is the
    cc3-2 work item, and until the pairing is constructed and numerically confirmed
    (≥100 digits, hashed, à la cc3-1), the membership claim stays CONJECTURED.
- **Honest note (the headline obstruction):** because L is non-rigid, **no
  identification-based theorem route exists** — there is no finite catalogue whose
  period theorems K can inherit. Any period statement about K must be *constructed*
  for L itself (exponential-motive pairing), then made conditional under a named
  period conjecture (KZ / Grothendieck / André motivated cycles) at cc3-3. The
  moduli dimension 2 (accessory count P=1, CC3-2-CONV-1) is the precise measure of how far L sits from the theorem-rich
  rigid locus.

## 6. Reconnaissance result already in hand (cc3-4a)

`cc3_1c_kpslq.py` (sha `94c3eb91…`): K is, to **169 digits**, **NOT** polylog-elementary
(weight ≤ 3, height ≤ 10¹²) and **NOT** a low-height mixed Γ×polylog combination
(height ≤ 10⁹); positive controls (Li₂(½), √2, ζ(2)) all fired. Pure-Γ tiers skipped
by argument (≡ already-nulled C tiers, ebr3-b `9a3f942d…`). This is consistent with —
and sharpens — the non-rigid/exponential-provenance picture: no elementary closed form
for K is detectable, matching "no rigid-catalogue identification."

## 7. cc3-2s2-2/3 routing result (D₈ monodromy point, coverage, Barnes battery)

Stage cc3-2s2-2 placed H₂ on the **PIII(D₈)=D₈⁽¹⁾** monodromy manifold at an explicit point and
ran the coverage + Barnes legs (REPORT_cc3_2c.md):

- **Monodromy point (2a, `b1fea3ed…`):** topological monodromy of the trace-free reduction
  Y″=rY around t=0 has **tr(M₀) = −51.0655631399546622698316746099456615679204…** (hyperbolic SL₂,
  \|tr\|≫2 ⟹ **irreducible**, off the reducibility locus) — a transcendental D₈ trace coordinate;
  the dim-2 point is **(tr(M₀), κ)**. Reframe cross-check **z₀=(a/2)²=1/3** exact (a=2/√3).
  Consistent with rig 0 / SL₂. *(Methodology note: the accuracy witness is path/radius/node
  invariance, not det=1; a dps-ordering integrator bug that faked 141-digit stability was caught.)*
- **Gauge dictionary (2b, `87be6028…`, STRUCTURAL):** H₂ → companion **B=[[0,1],[R,0]]**,
  R=4/(3x⁴)−53/(36x²)−4/3 (t=x²), the 2×2 two-rank-1-irregular-point **D₈ shape** (symmetric DCHE).
  **κ = s\*(B;x=0)×Γ-factor**, a **Lax-side** Stokes multiplier. Published-parametrized-Lax match is
  **OBSTRUCTED** (isomonodromy-time inverse problem, transcendental) ⟹ 2c ran in **survey mode**.
- **Coverage verdict (2c, `c72bec88…`):** **(iii) NOT COVERED.** ILT / Gavrylenko–Lisovyy compute
  **tau-side** objects (connection constant χ as Barnes-G(monodromy); τ as Fredholm-det(monodromy));
  κ is an **input** to those, never an output. H₂ non-rigid ⟹ outside the rigid (hypergeometric/
  Bessel/Airy) closed-form catalogue. Only known closed form κ=Γ(4/3)C_EBR/√π is **circular**.
  **[tau-vs-Lax hazard named throughout.]** No FIRE.
- **Barnes battery (2s2-3, `1887c410…`):** **ALL-NULL** — log κ, log A₀ are not integer-linear in
  the Barnes-G/Glaisher-extended basis (m∈{2,3,4,6,12}, H≤10¹², 150 digits); positive control
  G(1/2) fired; pure-Γ tier skipped (≡ frozen C-null). **No FIRE.**

**Net for cc3-2/cc3-3:** the **named target stays the Hien rapid-decay rank-2 pairing for the
symmetric-DCHE / D₈⁽¹⁾ connection** (the S6 CONJECTURED-with-architecture leg). The monodromy point is
now explicit, but no THEOREM-grade closed form covers κ's Lax-side coordinate, and no elementary
(polylog / Γ / Barnes) form is detectable. cc3-2 proceeds on the **generic exponential-motives track**
(Fresán–Jossen) with the Hien construction as the concrete instrument; cc3-3 supplies the
named-conjecture conditional. **CEILING (both ways): NOT COVERED / NULL prove nothing about
transcendence; a match would have argued the opposite.**

## 8. SUMMIT result (op:cc3-S6 + cc3-3, REPORT_cc3_final.md) — **branch CLOSED to its ceiling**

The Hien rapid-decay leg was **realised** and the named-conjecture conditional **assembled**:

- **S6 CLOSED → STRUCTURAL (`56adcb10…` / `2cc2f6fb…`).** κ realised **constructively** as the
  connection coefficient **A_Φ** of the order-4 Borel operator L (sing {0,1/3}, z=∞ irregular
  slope ¼), extracted by the monodromy spectral projector P_μ=(M−I)³/(μ−1)³ (μ=e^{−2πi/3}):
  **A_Φ = κ to 129 digits**, witnesses 208/204 (a **third independent channel**). The dim-2 point
  **(tr M₀, κ)** is now fully computed. Stokes-from-periods bridge κ=Γ(4/3)A₀=A_Φ=s\*(B;x=0), every
  factor explicit. **Supersedes the "pairing not yet built" / CC3-2S2-EXPPER line.** Full
  exponential-**MOTIVE** membership stays CONJECTURED-with-architecture.
- **OFF the classical PIII(D₈) locus (`a6b8d588…`).** (R) reducible/Riccati excluded by SL₂
  irreducibility; (A) algebraic excluded by |tr M₀|−2=49.07 (infinite-order) + tr M₀ not algebraic
  deg≤8 (PSLQ null). No HIT.
- **CONDITIONAL THEOREM (`1b15e7ac…`).** Under H1 (κ exp-period, STRUCTURAL) + H2 (G_mot⊇SL₂,
  CONJECTURED H-aux) + H3 (Fresán–Jossen period conjecture, external) + H4 (period-count, VERIFIED):
  **κ ∉ ℚ̄**, hence C transcendental. **Strongest licensed form, not rounded up**; 5-item graded
  **GAP LIST** is the EBR-IV open-problems section.
- **Close-out (`7c5d38e9…`).** Program four-class table (89 claims: 4 PROVEN / 34 STRUCTURAL /
  48 VERIFIED / 3 CONJECTURED); readiness inventory for **op:ebr4-assemble** with Lean-core
  candidates flagged.

**Net:** the non-rigid branch is **complete through its conditional ceiling**. Unconditional
transcendence of C/κ remains **OPEN** (it was never a deliverable). Next stage: **op:ebr4-assemble**.

---

## 9. Post-EBR-IV synthesis thread (cc-5 reframed) — **placeholder, flagged at the ebr4 final halt**

A corpus-level object has formed that is **larger than EBR-IV** and should not bloat it. Both
hard constants the program has resolved to date are **Stokes data of rank-2 Painlevé Lax
operators**, but on **different Sakai surfaces**:

| constant | family | operator / role | Sakai surface | grade of the surface label |
|----------|--------|-----------------|---------------|----------------------------|
| **S** (V_quad Stokes constant) | quadratic-growth V-family | rank-2, Painlevé V | **D₅⁽¹⁾** | (V_quad companion, deposited) |
| **κ** (EBR connection coefficient) | EBR d=2, b(n)=3n²+n+1 | H₂, Borel-2 reduction | **D₈⁽¹⁾ = PIII(D₈)** | VERIFIED per RULE S (`6c8dd5ee…`) |

The **old op:cc-5 "dividing-line" conjecture** asked *which connection coefficients are elementary*.
The corpus has quietly sharpened that into a different and crisper question:

> **Surface-type → arithmetic conjecture (SEED, CONJECTURED, not EBR-IV's burden).**
> *Which Sakai surface a positive-coefficient PCF's growth constant lands on — read off the local
> ramification data of the Borel-reduced rank-2 operator by a RULE-S-style selector — and whether
> that surface type predicts the arithmetic class (elementary vs exponential-period vs transcendental)
> of the constant.*

Status and discipline:
- This is recorded in the EBR-IV paper as the final open-problem item ("A surface-type synthesis",
  flagged *a pointer, not a result*) and is **not** load-bearing for the EBR-IV conditional theorem.
- It is the candidate **spine of a post-EBR-IV synthesis paper**, to be opened **only after** the
  EBR-IV (and the live V_quad/D₅⁽¹⁾) deposits resolve, so the two surface anchors are both citable.
- Provenance hooks already in hand: V_quad/D₅⁽¹⁾ on the Painlevé-V side (companion deposit, concept
  DOI `10.5281/zenodo.20455089`); EBR/D₈⁽¹⁾ on the Painlevé-III side (this dossier + `cc3_2s2_0_*`).
  The RULE-S selector (local-type → surface, *computed not pattern-matched*) is the shared instrument
  and the governance point that would carry the synthesis.
- Two data points do **not** make a pattern; the seed needs at least a third surface (a PCF whose
  Borel reduction lands on D₆⁽¹⁾/D₇⁽¹⁾ or a non-D-type surface) before any direction is asserted.

**Flagged for operator judgment at the ebr4 final halt — no action taken here.**

---

### Literature locators (VERIFIED-by-citation; never silently load-bearing above CONJECTURED)
- S. Bloch, H. Esnault, *Local Fourier transforms and rigidity for D-modules*,
  Asian J. Math. **8** (2004), no. 4, 587–605. [irregular index of rigidity]
- D. Arinkin, *Rigid irregular connections on P¹*, Compositio Math. **146** (2010),
  no. 5, 1323–1338. [cohomological rigidity, irregular]
- K. Jakob, Z. Yun, *classification of rigid irregular connections / G-connections.*
- N. Katz, *Rigid Local Systems*, Ann. Math. Stud. **139**, Princeton (1996).
  [middle convolution; Fuchsian — applies to the rigid locus only]
- N. Katz, *Exponential Sums and Differential Equations*, Ann. Math. Stud. **124**
  (1990). [Kloosterman/Airy sheaves, slopes]
- J. Fresán, P. Jossen, *Exponential Motives* (manuscript). [the generic period home]
- M. Hien, *Periods for flat algebraic connections*, Invent. Math. **178** (2009) 1–22;
  *Periods for irregular singular connections on surfaces*, Math. Ann. **337** (2007).
  [rapid-decay pairing — the concrete stage-2 construction for the DCHE rank-2 target]
- J. Fresán, C. Sabbah, J.-D. Yu, *Quadratic relations between Bessel moments*,
  Algebra & Number Theory **17** (2023); *…between periods of connections.*
  [Bessel-moment period theory — Kloosterman/rigid, does NOT apply to L]
- Y. André, *Séries Gevrey arithmétiques*, Ann. Math. **151** (2000). [G-functions]
