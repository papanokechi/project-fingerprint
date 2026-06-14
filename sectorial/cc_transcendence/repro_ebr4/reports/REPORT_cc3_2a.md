# REPORT — op:cc3-2 (stage 1): hygiene closure + rank-2 core H₂ classification

**Task:** op:cc-transcendence / cc3-2 · **Stage verdict:** COMPLETE, single stage-end HALT
(no mid-stage HALT: the Kovacic verdict is **non-Liouvillian**).
**Discipline:** SIARC four-class (PROVEN=Lean-only / STRUCTURAL / VERIFIED / CONJECTURED),
AEAL ledger, falsification-first, SHA-256 + dps. Nothing committed / minted; all artifacts untracked.

> **CEILING + discipline line (verbatim).** A large G_Gal does NOT imply C transcendental;
> an exponential-period classification does NOT imply C transcendental; only a named-conjecture
> conditional does. **Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.**
> *Extended (cc3-2):* a constructive exponential-period membership, if stage 2 achieves it, is
> type (c) — it proves **NOTHING** about transcendence.

**Centerpiece input (this op).** The OGF y(t)=Σ Qₙtⁿ (Qₙ=(3n²+n+1)Qₙ₋₁+Qₙ₋₂, Q₀=1, Q₁=5)
satisfies the inhomogeneous order-2 ODE `3t³y″ + 10t²y′ + (t²+5t−1)y = −1` (CC3-1-OGF-ODE).
Define the rank-2 homogeneous core **H₂ := 3t³D² + 10t²D + (t²+5t−1)**. This stage classifies H₂.

---

## 0. Hygiene confirmations (op:cc3-2-0) — DONE before any mathematics

- **CC3-2-ERR-1 (log-free supersession).** The cc3-1c-0 *working hypothesis* "z=0 apparent, M₀=I"
  and the cc3-1b *HALT-summary / inherited-state* paraphrase "z=0 block log-free" are **REFUTED**
  (z=0 carries logs, Jordan [2,2], CC3-1C-Z0-JORDAN). The cc3-1b *report body* (REPORT_cc3_1bc.md §1)
  and the claim **CC3-1B-LOGFREE** were narrowly **correct** (log-freeness scoped to Φ@0 + the z=1/3
  integer block); the over-generalization lived only in summary narration. Patched in REPORT_cc3_1c.md
  and cc3_2_entry_dossier.md (non-destructive correction, CC2-2D-JORDAN precedent).
- **CC3-2-CONV-1 (accessory convention).** Moduli dimension 2P = 2 − rig = 2 ⟹ **P = 1 accessory
  parameter**, reconciling with EBR-II's P = d−1 = 1 for L₂ at d=2 (L₂ also rig=0). "Accessory count 2"
  denoted the moduli dimension 2P, not P. Patched throughout REPORT_cc3_1c.md and the dossier.
- **Standing rule → repository memory.** Log content at resonant/repeated Frobenius exponents is
  asserted **only** with the θ-Frobenius obstruction computation attached at claim time — never
  inferred from exponent arithmetic (incidents: cc-1, cc3-1b).

---

## 1. H₂ formal data (op:cc3-2-1) — singular set {0, ∞}, both IRREGULAR slope ½

Reduced invariant (remove the first-order term: y″ = r y, p = 10/(3t), q = (t²+5t−1)/(3t³)):

```
r(t) = ¼p² + ½p′ − q = (−3t² − 5t + 3)/(9t³) = 1/(3t³) − 5/(9t²) − 1/(3t).
```

| point | pole order of r | slope | ramification | nature |
|-------|-----------------|-------|--------------|--------|
| t = 0 | 3 (odd) | **1/2** | **2** | irregular |
| t = ∞ | o(∞)=1; R(v)=(3v²−5v−3)/(9v³), pole order 3 | **1/2** | **2** | irregular |

**Correction logged.** slope = **1/2** (ramification 2) at both points — this **CORRECTS the earlier
"3/2" paraphrase** in transit notes. Two irregular points, no finite regular-singular point.

**Borel-2 / Hadamard chain (the rank-4 shell is DERIVED, not asserted).**
- Bessel kernel B(z) = I₀(2√z) = Σ zⁿ/(n!)² is annihilated by **(θ² − z)** (θ = zD), rank 2 — verified.
- Φ(z) = Σ Qₙ zⁿ/(n!)² = (y ⊙ B)(z) is the coefficient-wise (Hadamard) product of the OGF with B.
- The rank-4 operator **L = (rank-2 H₂-recurrence) ⊙ (θ²−z)** (Hadamard product of operators; order ≤ 2·2 = 4).
  Its leading indicial symbol **θ²(θ−1)²** (double root) is the source of the z=0 Jordan **[2,2]**;
  the double Borel weight (n!)² is what raises the order to 4.
- Frozen L = `z⁴(1−3z)D⁴ + (4z³−25z⁴)D³ + (2z²−47z³)D² − 15z²D − z²` **annihilates Φ to 40 terms,
  residual 0**; Q₀..Q₃ = 1, 5, 76, 2361 confirmed.

## 2. Kovacic verdict (op:cc3-2-1) — **G_Gal(H₂) = SL₂, NON-LIOUVILLIAN** (no HALT)

Order-2 dichotomy via the Riccati / quadratic-reducibility criterion (van der Put–Singer, *Galois
Theory of Linear Differential Equations*, GMW 328, 2003, §4.3.4 + §1.3–1.4). **Three rigorous
exclusions:**

1. **Case 1 (reducible) — EXCLUDED.** No rational solution of u′+u²=r over ℂ(t). *Rigorous,
   search-independent:* r ~ 1/(3t³) at t=0 (pole order 3) forces any Riccati solution to behave as
   u ~ ±(1/√3)·t^(−3/2), a **half-integer pole order**, impossible for a rational function. Bounded
   search corroborates (empty).
2. **Case 3 (finite primitive) — EXCLUDED.** t=0 is irregular (slope ½ > 0) ⟹ solutions carry a
   genuine essential singularity exp(±(2/√3)t^(−1/2)) ⟹ G is **infinite**.
3. **Case 2 (imprimitive / dihedral D∞) — EXCLUDED.** *This is the subtle one.* The slope-½
   **ramification-2** structure makes the formal monodromy at 0 (and at ∞) **swap** the two solutions
   exp(±(2/√3)t^(−1/2)) — the dihedral signature. **An SL₂-realized infinite dihedral group has NO
   rational Sym² invariant** (the weight-0 line y₁y₂ is anti-invariant under the SL₂ swap
   antidiag(1,−1)), so a rational-Sym²-over-ℂ(t) search is **not** a sound Case-2 test. The sound test:
   imprimitivity ⟺ L becomes **reducible over a quadratic extension ℂ(√f)** with √f ramified only
   within the singular set {0,∞}. A double cover of ℙ¹ has an **even** branch divisor, so {0} or {∞}
   alone is impossible — the **unique** candidate is **x² = t**. The pullback Y″ = R(x)Y has
   ```
   R(x) = 4/(3x⁴) − 53/(36x²) − 4/3 ,   only finite pole x=0 (order 4),
   ```
   so any rational Riccati solution is forced to the shape a/x² + b/x + c with a² = 4/3; the search
   over ℚ(√3) is **EXHAUSTIVE** and returns **EMPTY**. Hence L is **not** reducible over the only
   admissible quadratic extension ⟹ **not imprimitive**.

Irreducible (1) + infinite (2) + primitive (3) ⟹ **G_Gal(H₂) = SL₂. NON-LIOUVILLIAN.**
The registered expectation (SL₂, non-Liouvillian, consistent with every null so far) **holds**; the
Liouvillian HALT trigger does **not** fire.

**Positive controls (validating the detectors + the pullback machinery):**

| control | Riccati/ℂ(t) | pullback-Riccati/ℂ(x) | reads as |
|---------|--------------|------------------------|----------|
| Airy r=t (SL₂ primitive) | empty | empty | no false positive on either detector |
| r=2/t² (Case 1 reducible) | **fires** (−1/t, 2/t) | **fires** (−5/2x, 7/2x) | reducibility preserved by pullback ⟹ pullback detector FIRES on a genuine reducible |
| pullback formula (Airy) | — | — | Y=Ai(x²)/√(2x) solves Y″=R(x)Y, residual **1.8e-18** |

*(The earlier 2F1 "dihedral via rational Sym²" fixture was retired: it tested an unsound criterion.
A genuinely SL₂-dihedral group has no rational Sym² invariant, so that fixture could never validate
the correct Case-2 test. The pullback-reducibility detector is instead validated by the
reducibility-preservation control above.)*

**Certificate hash (canonical SHA-256, hash-free object):**
`e71e915fe616f9447668adf30fd5bd83eede5fcccb122d2c3dc0c131f80f1672` — script `cc3_2_1_h2_classify.py`.

## 3. Normal-form verdict (op:cc3-2-1) — **(b) symmetric doubly-confluent Heun (DCHE)**

Ramified pullback t = x² gives R(x) = 4/(3x⁴) − 53/(36x²) − 4/3:
**pole order 4 at x=0 (slope 1, unramified rank-1 irregular)** and **R → −4/3 as x→∞ (rank-1 irregular)**
— i.e. **two rank-1 irregular points** on the x-line and no finite regular-singular point.

This is the defining configuration of the **symmetric doubly-confluent Heun equation**. It is
**NOT** classical-confluent: Bessel / Kummer–Whittaker each have exactly **one** irregular + **one**
regular-singular point. The number/type of irregular points is a gauge + Möbius invariant and is
**not** reduced by the ramified pullback (a slope>0 point cannot become regular). Therefore:

> **Verdict: case (b) Heun-class.** Stage 2 builds the **Hien rapid-decay pairing for rank 2 directly**,
> with the concrete named target = **symmetric DCHE**. (This is *richer* than the cc3-1c dossier's
> generic-Fresán–Jossen-only anticipation, which predated having the OGF ODE — see §5.)

## 4. de Rham dimension counts (op:cc3-2-2) — feeds cc3-3 regardless of branch

Deligne–Malgrange Euler–Poincaré: χ_dR(U,M) = rank·χ(U) − Σ_x irr_x(M), dim H¹_dR = −χ
(H⁰=H²=0 for irreducible nonconstant); single-slope irr_x = rank·slope.

| object | rank | U | χ(U) | Σ irr_x | χ_dR | **dim H¹_dR** |
|--------|------|---|------|---------|------|----------------|
| **H₂** | 2 | 𝔾_m = ℙ¹∖{0,∞} | 0 | irr₀+irr_∞ = 1+1 = 2 | −2 | **2** |
| **L** | 4 | ℙ¹∖{0,1/3,∞} | −1 | irr_∞ = 4·¼ = 1 | −5 | **5** |

EP controls pass: trivial d/dz on 𝔾_m gives χ=0; Bessel (rank 2, irr_∞=2) gives dim H¹=2. ✓

## 5. Routing consequence (sharpens the cc3-1c dossier)

The dossier (`cc3_2_entry_dossier.md`, non-rigid branch) anticipated the **generic** exponential-motives
track (Fresán–Jossen) with K-as-exp-period only **CONJECTURED-with-architecture** and *no concrete
named target*. The H₂ classification **sharpens** this: the period construction now has a **concrete
named target — the symmetric DCHE rank-2 connection** — so stage 2 is a *worked-example* Hien
rapid-decay pairing for rank 2, not an open-ended generic build. **Non-rigidity (rig L = 0) is
unchanged**, so the identification-based theorem routes remain closed; what improves is the
explicitness of the object whose pairing must be built and numerically confirmed (≥100 digits, hashed)
at the next stage.

---

## Four-class ledger (this stage)

| # | statement | class | basis |
|---|-----------|-------|-------|
| CC3-2-ERR-1 | log-free supersession (scope-correct, non-destructive) | VERIFIED | θ-Frobenius CC3-1C-Z0-JORDAN |
| CC3-2-CONV-1 | accessory count P=1 (moduli dim 2P=2); reconciles EBR-II | VERIFIED | rig(L)=0 + EBR-II |
| CC3-2-CORE-LOCAL | H₂ singular set {0,∞} both irregular slope ½ ramif 2; r=(−3t²−5t+3)/(9t³) (corrects "3/2") | VERIFIED | exact symbolic `e71e915f…` |
| CC3-2-CORE-CHAIN | Borel-2/Hadamard: B=I₀(2√z) by (θ²−z); Φ=y⊙B; rank-4 L=H₂-rec ⊙ (θ²−z), symbol θ²(θ−1)² → z=0 [2,2]; L⊨Φ to 40 terms | VERIFIED | symbolic `e71e915f…` |
| CC3-2-KOV | G_Gal(H₂)=SL₂, non-Liouvillian (Case 1 indicial 3/2 + empty Riccati; Case 3 irregular; Case 2 unique-cover √t pullback irreducible over ℚ(√3)); NO HALT | STRUCTURAL | CAS+hand, controls fired, `e71e915f…` |
| CC3-2-NF | normal form (b): symmetric DCHE (two rank-1 irregular pts after t=x²; not classical-confluent) | STRUCTURAL | `e71e915f…` |
| CC3-2-DIM | dim H¹_dR(H₂)=2, dim H¹_dR(L)=5 (Deligne–Malgrange EP) | VERIFIED | `e71e915f…` |

**Epistemic delta (this stage).** rank-2 core H₂ pinned: **SL₂ non-Liouvillian** (every elementary/
Liouvillian closed-form route is now *excluded*, not merely *not-found* — the 169-digit nulls are
confirmed consistent, not contradicted), normal form **(b) symmetric DCHE**. The Case-2 exclusion was
rebuilt on the **correct** criterion (quadratic-extension reducibility via the unique √t cover), not the
unsound rational-Sym² test that the verdict had originally leaned on. cc3-2 stage 2 now has a concrete
named pairing target. **No transcendence claim at any grade** (CEILING in force).

## Artifacts (untracked / uncommitted / unminted)

- `cc3_2_1_h2_classify.py` — script (local analysis, Kovacic three-exclusion, normal form, Borel-2/
  Hadamard chain, de Rham counts, controls).
- `cc3_2_1_h2_classify_results.json` — certificate, canonical SHA-256
  `e71e915fe616f9447668adf30fd5bd83eede5fcccb122d2c3dc0c131f80f1672`.
- Ledger: CC3-2-CORE-LOCAL, CC3-2-CORE-CHAIN, CC3-2-KOV, CC3-2-NF, CC3-2-DIM appended to MAIN
  `claims_cc.jsonl`. `repro/` (FROZEN EBR-III, 45 claims) untouched.

### Literature locators (VERIFIED-by-citation; never silently load-bearing above CONJECTURED)
- M. van der Put, M. Singer, *Galois Theory of Linear Differential Equations*, GMW 328, Springer
  (2003): §4.3.4 (Kovacic / order-2 dichotomy), §1.3–1.4 (algebraic Riccati solutions ⇔ imprimitivity
  over a quadratic extension).
- J. Kovacic, *An algorithm for solving second order linear homogeneous differential equations*,
  J. Symbolic Comput. **2** (1986) 3–43. [the four-case structure; Case-2 algebraic-degree-2 Riccati]
- A. Duval, M. Loday-Richaud, *Kovacic's algorithm and its application to some families of special
  functions*, AAECC **3** (1992) 211–246. [doubly-confluent Heun / irregular reductions]
- B. Dwork, G. Gerotto, F. Sullivan, *An Introduction to G-Functions*, Ann. Math. Stud. **133** (1994).
  [reduced-invariant pullback / Schwarzian transformation of y″=ry]
- P. Deligne, *Équations différentielles à points singuliers réguliers*, LNM 163; Malgrange index
  theorem; C. Sabbah, *Introduction to Stokes structures*, LNM 2060, §5. [de Rham Euler–Poincaré, irr_x]
- J. Fresán, P. Jossen, *Exponential Motives* (manuscript). [the period home for stage 2]
- M. Hien, *Periods for flat algebraic connections*, Invent. Math. **178** (2009) 1–22; and
  *Periods for irregular singular connections on surfaces*, Math. Ann. **337** (2007). [rapid-decay
  pairing — the concrete stage-2 construction for the DCHE rank-2 target]
