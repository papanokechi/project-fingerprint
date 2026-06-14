# REPORT — op:cc3-2s2 (stage 2): H₂ rigidity, RULE S, and the resurgence construction of κ

**Task:** op:cc-transcendence / cc3-2s2 · **Stage verdict:** COMPLETE through op:cc3-2s2-1,
**single stage-end HALT** before op:cc3-2s2-2 (the ILP/Barnes formula hunt — operator clearance
required, per the START block). No mid-stage HALT fired: P5 holds (not rigid), P6 holds (RULE S
passes), and the Kovacic verdict from stage 1 is non-Liouvillian.
**Discipline:** SIARC four-class (PROVEN=Lean-only / STRUCTURAL / VERIFIED / CONJECTURED),
AEAL ledger, falsification-first, SHA-256 + dps. **RULE S in force verbatim** (below). Nothing
committed / minted; all artifacts untracked.

> **RULE S (reproduced verbatim).** No Painlevé / Sakai surface label reaches VERIFIED without
> computed selectors **plus** the Padé convergence screen.

> **CEILING + discipline line (verbatim, now cutting both ways).** A Stokes reframing, a RULE S
> pass, even an ILP-class formula match would **NOT** prove transcendence; a match would prove the
> **OPPOSITE** direction — elementarity in an extended Barnes class. **Unconditional transcendence
> of C / κ is NOT a deliverable of op:cc-3 at any grade.** Relocation to a regular-to-regular /
> Stokes connection problem does not make κ a classical period — provenance is exponential
> (Borel-2 / instanton), and the period conjectures see provenance, not singularity type.

---

## 0. Rename K → κ (op:cc3-2s2 · CC3-2S2-REN)

The running constant `K = 1.539494848576641034843781903384069038219…` is **renamed κ** throughout
this report and all new ledger entries, to remove the corpus collision with the V_quad Stokes
constant `K`. This rename is **annotation only**: frozen artifacts (`cc3_1b_K.py`,
`cc3_1b_K_results.json`, hash `2ff9da32…`) keep their recorded name `K` with this rename note; no
frozen hash is mutated. Where this report cites a frozen value it writes `κ (frozen as K_130)`.

---

## 1. Rigidity of H₂ (op:cc3-2s2-0 · part A) — rig(H₂) = 0, P5 HOLDS

H₂ has rank n = 2 and singular set {0, ∞} (#S = 2), **both irregular, slope ½, ramification 2,
single ℤ/2 orbit** (from the reduced invariant r = (−3t²−5t+3)/(9t³), CC3-2-CORE-LOCAL). Irregular
index of rigidity (Bloch–Esnault / Arinkin; same pipeline as cc3-1c-2, rank-2 instance):

```
rig = (2 − #S)·n²  +  Σ_p dim Z(formal type)_p  −  Σ_p irr_p(End)
    = (2 − 2)·4     +  (1 + 1)                    −  (1 + 1)
    = 0.
```

- Each point: a single slope-½ ramification-2 orbit ⟹ **dim Z(formal type) = 1**; the two distinct
  exponential characters give 2 nonzero pairwise differences at slope ½ ⟹ **irr(End) = 1** per point.
- **Verdict: rig(H₂) = 0 ⟹ NON-RIGID.** Moduli dimension 2P = 2 − rig = **2** (= the Painlevé
  phase-space dimension), accessory **P = 1**.

> **P5 — `rig(H₂)=0, moduli dim 2` — HOLDS.** A rigid verdict would have been an unconditional HALT
> (it would kill the PIII(D₈) candidacy). It did not fire.

**Controls (same battery as cc3-1c).** Airy, Gauss ₂F₁, Bessel each return **rig = 2** (the
classical rigid value) — the formula separates rigid from non-rigid correctly.

---

## 2. RULE S gate (op:cc3-2s2-0 · part B) — PIII(D₈) VERIFIED, P6 HOLDS

**REFRAME validated.** H₂ has **no finite nonzero singularity** (only 0 and ∞, both irregular).
Therefore **z = 1/3 is a Borel-plane singularity** of the Gevrey-2 formal solution y — an instanton
action — and **κ is a Stokes-type constant of H₂**, not a two-point connection coefficient. Stage 2
is thus *resurgence analysis of H₂* (§3).

**Leg 1 — computed selectors.** For rank-2 connections with two irregular singular points the Sakai
surface is fixed by the (ramification at point A, ramification at point B) datum:

| surface | local type (ram, ram) |
|---------|------------------------|
| PIII(D₆) = D₆⁽¹⁾ | (1, 1) — both unramified, slope 1 |
| PIII(D₇) = D₇⁽¹⁾ | (2, 1) — one ramified |
| **PIII(D₈) = D₈⁽¹⁾** | **(2, 2) — both ramified, slope ½** |

H₂ computes to **(2, 2)** (both points slope-½ ramification-2). **Unique match: PIII(D₈) = D₈⁽¹⁾.**
D₆/D₇ are excluded by the ramification count. Leg 1 **PASSES**.

**Leg 2 — Padé convergence screen.** The screen must reproduce z = 1/3 as the dominant Borel-plane
singularity (this simultaneously validates the reframe):
- Ratio-test radius of Φ(z)=ΣQₙzⁿ/(n!)² (geometric-node Richardson): **0.3333333333…33** matching
  1/3 to **34 digits** (err 1.4e-35).
- Padé pole table (orders 20→60): nearest pole **monotonically converges** to 1/3
  (0.333105 → 0.333231 → 0.333277 → 0.333297 → 0.333308). Converging. Leg 2 **PASSES**.

> **Both legs pass ⟹ PIII(D₈) = Sakai surface D₈⁽¹⁾ reaches VERIFIED per RULE S.**
> **P6 — `PIII(D₈) passes RULE S` — HOLDS.** (A failure would have rerouted op:cc3-2s2-2 to an
> obstruction report; it was not a halt trigger either way.)

**Certificate (canonical SHA-256, hash-free object):**
`6c8dd5ee9106abbcfadf4c497d154aac80dc0e1b1b10d7592c56a3a14f458a14` — `cc3_2s2_0_rigidity_ruleS.py`.

---

## 3. Resurgence construction of κ (op:cc3-2s2-1) — the bridge identity

### 3.1 The bridge identity (centerpiece)

The frozen κ is **defined** (cc3_1b_K_results.json) as *"the coefficient of (1−3z)^{−4/3} in the
analytic continuation of Φ(z) to z = 1/3"* — i.e. the **singular amplitude A_Φ**. By the
Flajolet–Sedgewick transfer theorem (Analytic Combinatorics, Thm VI.1),

```
[zⁿ] A_Φ (1 − 3z)^{−4/3}  ~  A_Φ · 3ⁿ · n^{1/3} / Γ(4/3),
```

so, defining the large-order amplitude **A₀ := limₙ Qₙ / ((n!)² · 3ⁿ · n^{1/3})**, the exact bridge is

> **κ = Γ(4/3) · A₀.**   *(STRUCTURAL — exact, not merely numerical.)*

This is consistent with the frozen reduction `C_EBR = κ·(4/3)√π/Γ(7/3)`, which collapses via
**Γ(7/3) = (4/3)Γ(4/3)** to `κ = Γ(4/3)·C_EBR/√π`, giving the cross-equivalence **A₀ = C_EBR/√π**.
In the resurgence reading, **A₀ is the Borel-plane singularity amplitude at z = 1/3 (the instanton)**
and κ its associated Stokes constant.

### 3.2 Two-channel numerical confirmation (honest precision accounting)

| channel | what it uses | independent? | agreement vs frozen κ₁₃₀ |
|---------|--------------|--------------|---------------------------|
| **A — large-order** | only the Qₙ recurrence + exponent 4/3, Nmax=60000, Richardson on a geometric node ladder | **YES, fully independent** of the cc3-1b Fuchsian continuation | **~60 digits** |
| **B — frozen composition** | κ = Γ(4/3)·C_EBR/√π with the frozen 169-digit C_EBR | NO (restates the frozen 171-digit identity) | **~129 digits** |

- **Channel A** is the genuinely new cross-check: it confirms that A₀ — extracted purely from the
  coefficient asymptotics — **is** the bridge amplitude, to ~60 digits. The wall at ~60 is the
  asymptotic-extrapolation limit at Nmax=60000, not roundoff (dps 340).
- **Channel B** reaches ~129 digits but adds **no new content** beyond the already-frozen
  C_EBR↔κ identity; it confirms only the Γ-algebra Γ(7/3)=(4/3)Γ(4/3). The bridge being **exact
  (STRUCTURAL)**, it holds to the full frozen precision; the ≥100-digit numerical confirmation asked
  for by the op is met here, while the **independent** verification stands at ~60 digits — stated
  plainly, not inflated.
- **Consistency:** A₀ from channel A and A₀ = C_EBR/√π agree to all displayed digits
  (1.72399795138777440647669074957976629134161…).

### 3.3 Key numerical finding — PURE 1/n corrections (corroborates the reframe)

The corrections to rₙ = Qₙ/((n!)²·3ⁿ·n^{1/3}) are **pure integer powers of 1/n**: **no n^{−1/3}
terms, no logs.** This is exactly what a *single dominant log-free Borel singularity* of type
(1−3z)^{−4/3} predicts (the only non-analytic factor is (1−3z)^{−4/3}, times a function analytic in
u=1−3z). Extrapolating on the x=1/n grid lifts channel A from ~19 digits (the wrong n^{−1/3} grid)
to ~60. The clean 1/n structure independently corroborates the **log-free semisimple** z=1/3
monodromy established in cc3-1c.

---

## 4. The integrand chain (op:cc3-2s2-1) — exponential-period architecture, graded per step

| step | statement | grade |
|------|-----------|-------|
| **S1** | y(t)=ΣQₙtⁿ is **Gevrey-2**: \|Qₙ\| ~ A₀(n!)²3ⁿn^{1/3} ⟹ \|Qₙ\| ≤ C·Hⁿ(n!)² | STRUCTURAL |
| **S2** | I₀-normalized Borel-2 transform Φ(z)=ΣQₙzⁿ/(n!)² = y ⊙ I₀(2√z) (Hadamard product), radius 1/3 | STRUCTURAL |
| **S3** | I₀(2√z) = (1/2πi)∮ e^{x+z/x} dx/x — the Borel kernel **is an exponential period** | **THEOREM (cited, DLMF 10.9.19)** |
| **S4** | Φ = Hadamard contour pairing of Borel-summed y against the I₀ kernel; the **divergent-y leg** needs Borel-2 summability off the singular ray arg=0 (which carries z=1/3) | STRUCTURAL (summability cited) |
| **S5** | κ = coeff of (1−3z)^{−4/3} in Φ = Stokes datum = discontinuity amplitude across arg=0 = **Γ(4/3)·A₀** | STRUCTURAL |
| **S6** | ⟹ "**κ is an exponential period / a Stokes constant of L**"; full exponential-**motive** membership (Fresán–Jossen) | **CONJECTURED-with-architecture** |

The grade lives or dies at **S4/S6**: the rapid-decay-cycle pairing for the divergent-y leg is
**not constructed here** — it is the stage-2 Hien rank-2 worked example. What S1–S6 deliver is the
explicit *architecture* and the exact *bridge* (S5), not a membership theorem.

---

## 5. Routing → stage 2 (Hien rapid-decay pairing for the DCHE / PIII(D₈) rank-2 connection)

This report **supersedes** the dossier's "rank-2 rapid-decay pairing not yet built" line with the
explicit S1–S6 architecture. The period home is now sharp on three axes — (i) **named surface**
PIII(D₈) = D₈⁽¹⁾ (VERIFIED per RULE S), (ii) **named normal form** symmetric DCHE (CC3-2-NF), (iii)
**explicit bridge** κ=Γ(4/3)A₀ — so stage 2 is a concrete worked-example Hien pairing, not an
open-ended generic build. **Non-rigidity (rig H₂ = 0) is unchanged**, so no identification-based
*transcendence* route opens; the sharpening is of provenance and of the object whose pairing must be
constructed and numerically confirmed. **op:cc3-2s2-2** (mapping κ onto the Its–Lisovyy–Prokhorov /
Gavrylenko–Lisovyy D₈ connection-problem coordinates, then the Barnes-G/Glaisher PSLQ tier) is the
next step and **requires operator clearance** — a closed-form FIRE there would be an unconditional
HALT and (per the ceiling) would argue *elementarity*, not transcendence.

---

## Four-class ledger (this stage)

| # | statement | class | basis |
|---|-----------|-------|-------|
| CC3-2S2-REN | rename K → κ (annotation only; frozen artifacts keep name K + rename note) | VERIFIED | bookkeeping |
| CC3-2S2-RIG | rig(H₂)=0 ⟹ NON-RIGID, moduli dim 2, accessory P=1; P5 holds; controls Airy/₂F₁/Bessel=2 | VERIFIED | irregular index pipeline `6c8dd5ee…` |
| CC3-2S2-RULES | H₂ local type (ram2,ram2) ⟹ **PIII(D₈)=D₈⁽¹⁾**, unique; Padé screen reproduces z=1/3 to ~34 dig ⟹ **VERIFIED per RULE S**; P6 holds | VERIFIED | computed selectors + Padé screen `6c8dd5ee…` |
| CC3-2S2-KAPPA-RES | **bridge κ = Γ(4/3)·A₀** (A₀=lim Qₙ/((n!)²3ⁿn^{1/3})); exact via Flajolet–Sedgewick transfer; A₀=C_EBR/√π | STRUCTURAL | transfer theorem + cc3-1b def `8f52843c…` |
| CC3-2S2-KAPPA-NUM | κ=Γ(4/3)A₀ confirmed **independently to ~60 digits** (channel A, Qₙ-only) and ~129 digits (channel B, frozen C_EBR); corrections PURE 1/n (no n^{−1/3}, no logs) | VERIFIED | numerical `8f52843c…` |
| CC3-2S2-EXPPER | integrand chain S1–S6: κ = exponential period / Stokes constant of L; I₀ kernel exponential period (S3 THEOREM); membership architecture only | CONJECTURED-with-architecture | `8f52843c…` |

**Epistemic delta (this stage).** The rank-2 core's place is pinned: **rig(H₂)=0 (non-rigid, moduli
dim 2)** and, per RULE S, **PIII(D₈)=D₈⁽¹⁾** (computed selectors + Padé screen both pass) — the first
VERIFIED Painlevé-surface label in the cc-3 line. The reframe is validated (z=1/3 is the instanton
action, κ a Stokes constant). The centerpiece is the **exact bridge κ=Γ(4/3)·A₀** (STRUCTURAL),
confirmed **independently to ~60 digits** and to ~129 via the frozen composition; the pure-1/n
correction structure independently corroborates the log-free single-dominant Borel singularity. The
exponential-period **architecture** S1–S6 supersedes the dossier's "pairing not yet built", with
membership honestly **CONJECTURED-with-architecture**. **No transcendence claim at any grade**
(CEILING in force; a match would argue the opposite).

---

## Artifacts (untracked / uncommitted / unminted)

- `cc3_2s2_0_rigidity_ruleS.py` — rigidity (Part A, controls) + RULE S battery (Part B: leg-1
  computed selectors → D₆/D₇/D₈ map; leg-2 ratio-radius + Padé pole table).
- `cc3_2s2_0_rigidity_ruleS_results.json` — canonical SHA-256
  `6c8dd5ee9106abbcfadf4c497d154aac80dc0e1b1b10d7592c56a3a14f458a14`.
- `cc3_2s2_1_resurgence.py` — bridge identity, two-channel numerical confirmation (channel A
  large-order independent / channel B frozen composition), integrand chain S1–S6.
- `cc3_2s2_1_resurgence_results.json` — canonical SHA-256
  `8f52843c2e389609c932d25a76b79cfcc422782fc31a0c87392edeb1e8c653f9`.
- Ledger: CC3-2S2-REN, -RIG, -RULES, -KAPPA-RES, -KAPPA-NUM, -EXPPER appended to MAIN
  `claims_cc.jsonl` (73 → 79). `repro/` (FROZEN EBR-III, 45 claims) untouched.
- `cc3_2_entry_dossier.md` §5 patched (UPDATE box: PIII(D₈) + S1–S6 architecture supersede "pairing
  not yet built").

### Literature locators (VERIFIED-by-citation; never silently load-bearing above CONJECTURED)
- H. Sakai, *Rational surfaces associated with affine root systems and geometry of the Painlevé
  equations*, Comm. Math. Phys. **220** (2001) 165–229. [surface D₈⁽¹⁾ classification]
- M. van der Put, M.-H. Saito, *Moduli spaces for linear differential equations and the Painlevé
  equations*, Ann. Inst. Fourier **59** (2009) 2611–2667. [singularity-type ↔ Painlevé dictionary]
- Y. Ohyama, H. Kawamuko, H. Sakai, K. Okamoto, *Studies on the Painlevé equations V, third
  Painlevé equations of special type PIII(D₇) and PIII(D₈)*, J. Math. Sci. Univ. Tokyo **13** (2006)
  145–204. [PIII(D₈) Lax pair / degeneration]
- D. Arinkin, *Rigid irregular connections on ℙ¹*, Compositio Math. **146** (2010) 1323–1338;
  S. Bloch, H. Esnault, *Local Fourier transforms and rigidity for 𝒟-modules*, Asian J. Math. **8**
  (2004) 587–606. [irregular index of rigidity]
- P. Flajolet, R. Sedgewick, *Analytic Combinatorics*, CUP 2009, Thm VI.1. [singularity-amplitude
  ⇔ coefficient-asymptotics transfer — the bridge identity]
- R. B. Dingle, *Asymptotic Expansions: Their Derivation and Interpretation*, Academic Press 1973;
  M. Loday-Richaud, *Divergent Series, Summability and Resurgence II*, LNM 2154, Springer 2016.
  [late-terms = singularity amplitude; Borel–Laplace summability, Stokes constants]
- DLMF 10.9.19 / G. N. Watson, *Theory of Bessel Functions*, §6.2. [I₀ contour integral —
  exponential period]
- J. Fresán, P. Jossen, *Exponential Motives* (manuscript). [the period home for stage 2 — used as
  architecture, NOT a closed theorem here]
- M. Hien, *Periods for flat algebraic connections*, Invent. Math. **178** (2009) 1–22. [rapid-decay
  pairing — the concrete stage-2 construction for the rank-2 DCHE / PIII(D₈) target]
- O. Lisovyy et al. (Its–Lisovyy–Prokhorov; Gavrylenko–Lisovyy), connection problems for irregular
  Painlevé III. [op:cc3-2s2-2 entry — NOT executed this stage; operator clearance required]
