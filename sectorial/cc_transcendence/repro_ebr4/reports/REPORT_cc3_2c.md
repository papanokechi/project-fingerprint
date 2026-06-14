# REPORT — op:cc3-2s2-2 + 2s2-3: H₂ on the PIII(D₈) monodromy manifold, coverage, Barnes battery

**Task:** op:cc-transcendence / cc3-2s2-2 + cc3-2s2-3 · **Stage verdict:** COMPLETE through
op:cc3-2s2-2a → 2b → 2c → 3, **single stage-end HALT**. No mid-stage UNCONDITIONAL HALT fired: the
2a cross-checks all passed (coordinates consistent with rig 0 / SL₂), 2c returned **NOT COVERED**
(no closed-form FIRE), and the 2s2-3 battery returned **ALL-NULL** (no FIRE).
**Discipline:** SIARC four-class (PROVEN=Lean-only / STRUCTURAL / VERIFIED / CONJECTURED), AEAL
ledger, falsification-first, SHA-256 + dps. Nothing committed / minted; all artifacts untracked.

> **CEILING (verbatim, cutting BOTH ways).** Placing κ as a Stokes/monodromy coordinate, a gauge
> dictionary, a coverage verdict, or a PSLQ run prove **NOTHING** about transcendence. A formula
> **MATCH** would prove the **OPPOSITE** — elementarity in an extended (Barnes) class; a **NULL**
> proves neither. **Unconditional transcendence of C / κ is NOT a deliverable of op:cc-3 at any
> grade.** Provenance is exponential (Borel-2 / instanton); the period conjectures see provenance,
> not singularity type.

> **NAMED HAZARD (reproduced).** Tau-function connection constants **≠** Lax-solution Stokes data.
> κ is a **Lax-side** Stokes multiplier; the ILT / Gavrylenko–Lisovyy theorems compute **tau-side**
> objects as Barnes-G / Fredholm functions **of** the monodromy. κ is an **input** to those formulas,
> never their **output**. The line is named in every crossing paragraph of §2–§3.

---

## 1. op:cc3-2s2-2a — Monodromy coordinates of H₂

H₂ reduces (trace-free) to **Y″ = r Y, r = 1/(3t³) − 5/(9t²) − 1/(3t)**, singular set **{0, ∞}
only**, both irregular slope ½ ramification 2 (CC3-2-CORE-LOCAL).

### 1.1 Formal data (exact)
- WKB at t=0: √r ~ t^{−3/2}/√3 ⟹ S(t) ~ −(2/√3)t^{−1/2}, **instanton action a = 2/√3**.
- **Exact reframe cross-check:** the Gevrey-2 (n!)²-Borel kernel ~ exp(−2√(z/t)) places the Borel
  singularity at z₀ with 2√z₀ = a ⟹ **z₀ = (a/2)² = 1/3** (verified to >100 digits). The formal
  exponential factor and the z = 1/3 Borel singularity (2s2-0 reframe) are the **same datum**.
- Wronskian (no Y′ term) ⟹ **α₊ + α₋ = 3/2**; ramification swaps the formal solutions:
  M̂ = [[0, e^{2πiα₊}],[e^{2πiα₋}, 0]], **tr M̂ = 0, det M̂ = −e^{3πi} = +1** (SL₂-consistent).

### 1.2 Topological monodromy — the SL₂ trace coordinate
Taylor-marching analytic continuation of Y″=rY around a loop enclosing t=0:

> **tr(M₀) = −51.06556313995466 22698316746099 45661567920410 33310390833911 0321065718…**

(hyperbolic / loxodromic SL₂, eigenvalue λ ≈ 51.0460, **|tr| ≫ 2 ⟹ irreducible**, off the
reducibility/parabolic locus). This is a **transcendental D₈ character-variety trace coordinate**.

**Validation — and a methodology correction worth recording.** The accuracy witness is
**cross-(J, nsteps, radius) agreement plus path-invariance**, NOT det = 1:
- **det = 1 is structural, not an accuracy proof.** For the trace-free Y″=rY the Wronskian is
  conserved by any structure-respecting flow, so det = 1 holds to ~157 digits *regardless of
  trajectory accuracy*. The **trace** is the accuracy-sensitive coordinate.
- **Topological invariance (strongest check):** the singular set is {0, ∞} only, so every circle
  |t|=ρ>0 encloses just t=0 ⟹ tr(M₀) is ρ-independent. Confirmed to **~157 digits** across
  ρ ∈ {0.7, 1.0, 1.7, 2.5}.
- **Path/discretization invariance:** tr(M₀) is invariant to the loop start angle φ₀ (to ~177
  digits, φ₀ ∈ {0,0.3,0.7,1.1,1.9}) and to **irregular (random) node layouts** (to ~80–91 digits) —
  properties only the genuine monodromy trace can have.
- **Two integrator pitfalls were caught and fixed** (see CC3-2S2-2A-METH): (i) an asymmetric Taylor
  truncation `range(J+2)` (dropped the top coefficient); (ii) — the load-bearing one — module-level
  `mpf` constants (ONE3=1/3, FIVE9=5/9) evaluated at the **default 15-digit precision** because
  `mp.dps` was set later inside `main()`. Both produced a **false-stable, ~14-digit-wrong** trace
  (−51.0655631399546**656…**) that agreed with itself to 141 digits. Setting `mp.dps` **before** the
  constants gives the invariance-proven value above. *Lesson: cross-config self-agreement of
  precision-contaminated constants is not a correctness witness.*

### 1.3 Cross-checks (a failure would be an UNCONDITIONAL HALT) — ALL PASS
| check | result |
|-------|--------|
| tr(M₀) converged ≥ 90 d (cross-J, cross-nsteps, cross-radius, phase, irregular nodes) | **PASS** (~141 d) |
| tr(M₀) real (\|Im tr\| < 10⁻⁶⁰) | **PASS** (3.4e-158) |
| \|tr(M₀)\| ≠ 2 (irreducible, off reducibility locus) | **PASS** |
| κ ≠ 0 (nontrivial Stokes ⟹ not formally split) | **PASS** |
| z₀ = (a/2)² = 1/3 (formal ↔ Borel reframe) | **PASS** |
| det(M₀) = 1 (SL₂; structural note, not accuracy witness) | holds to ~157 d |

⟹ coordinates **consistent with rig 0 / G_Gal = SL₂**. The dim-2 D₈ point is reported as
**(tr(M₀), κ)** = (the trace coordinate above; the off-diagonal Stokes constant κ, §2).
Certificate `cc3_2s2_2a_monodromy_results.json` SHA-256 **b1fea3ed…**.

---

## 2. op:cc3-2s2-2b — Gauge dictionary H₂ → standard D₈ Lax form

Every algebraic step is a sympy-checked identity (residual 0):

| step | map | result |
|------|-----|--------|
| (i) scalar gauge | y = t^{−5/3} u | u″ = r u, r = 1/(3t³) − 5/(9t²) − 1/(3t) |
| (ii) ramified pullback + gauge | t = x², Ỹ = x^{1/2} w | w″ = R w, **R = 4/(3x⁴) − 53/(36x²) − 4/3** |
| (iii) companion | W = (w, w′)ᵀ | dW/dx = B W, **B = [[0,1],[R,0]]** |

B has irregular singular points of **Poincaré rank 1 at x=0 and x=∞** — the standard **PIII(D₈) Lax
shape** (2×2, two rank-1 irregular points = the symmetric DCHE of CC3-2-NF). Composite gauge from the
original H₂ solution: **y = x^{−17/6} w** (t = x²).

**Dictionary statement.** A meromorphic scalar gauge multiplies both formal solutions at an irregular
point by the same factor and hence leaves the **Stokes matrices invariant**. Therefore the
off-diagonal Stokes multiplier of B at x=0 equals the Stokes multiplier of H₂ at t=0, and (2s2-1)

> **κ = s\*(B; x=0) × F**, with **F a Γ-quotient in the formal exponents α±** (α₊+α₋=3/2), from the
> Borel-amplitude ↔ Stokes-multiplier normalization. **[tau-vs-Lax: κ is the Lax-side multiplier.]**

Grade: **STRUCTURAL** for the gauge chain (i)–(iii) (symbolic, residual 0); F is derivable.

**Obstruction (documented; routes 2c to SURVEY mode).** Matching B(x) to a *specific published
parametrized* PIII(D₈) Lax A(λ,s) (Ohyama–Kawamuko–Sakai–Okamoto; FIKN) requires fixing the
isomonodromy **time s** and the transcendent value for which the isomonodromic A(λ,s) equals our
**frozen, non-deforming** B(x) — an **inverse-monodromy (Riemann–Hilbert) determination,
transcendental, not a finite symbolic gauge**. So the dictionary lands rigorously at the
companion-system (D₈-shape) level; the named-published-coordinate match is **not closed symbolically**.
Certificate `cc3_2s2_2b_dictionary_results.json` SHA-256 **87be6028…**.

---

## 3. op:cc3-2s2-2c — Formula coverage (hazard leg, SURVEY mode)

Per the 2b obstruction, 2c is a literature **survey** (no parametrized match asserted; no formula
instantiated numerically). Inventory, THEOREM/conjecture/folklore separated, locators in §refs:

| solved problem | what the theorem computes | coordinates | grade | vs κ |
|----------------|---------------------------|-------------|-------|------|
| **ILT connection constant** (Its–Lisovyy–Prokhorov, CMP 363 (2018)) | the tau-function **connection constant χ** (t→0 / t→∞ prefactor ratio) as a **Barnes-G/Γ** product | monodromy data as **arguments** | THEOREM | **tau-side**; κ is an **input**, not the output |
| **Gavrylenko–Lisovyy Fredholm/Nekrasov** (CMP 2018; Cafasso–G.–L.) | the isomonodromic **tau function** as det(1−K), K built **from** the monodromy | monodromy → tau | THEOREM | **tau-side**; κ-analog is **input** |
| **forward ODE connection problem** (Sibuya; FIKN; Katz *Rigid Local Systems*) | Stokes/connection matrix in closed form **only for RIGID local data** (hypergeometric/Bessel/Airy) | local data → Stokes | THEOREM (rigid) / OPEN (general) | **Lax-side** but H₂ is **non-rigid** (rig=0) ⟹ outside the catalogue |

**Three-way verdict: (iii) NOT COVERED.**
- The solved D₈ problems all compute a **tau-side** quantity as a Barnes-G/Fredholm function **of** the
  monodromy; κ is a **Lax-side** Stokes multiplier that is an **input** to those formulas, never an
  output. **[tau-vs-Lax: named.]**
- No theorem outputs a closed form for a Stokes multiplier of a **non-rigid** 2nd-order ODE; H₂ is
  non-rigid, so it is outside the rigid (hypergeometric/Bessel) closed-form catalogue.
- Even **ADJACENT** use of ILT is blocked: instantiating the connection-constant formula at our point
  needs the **member identification** = the 2b obstruction (transcendental); and even instantiated it
  would output the **tau connection constant**, a different coordinate than κ.
- κ's only known closed form is **κ = Γ(4/3)·C_EBR/√π** (re-confirmed here to ~129 digits) —
  **circular** (C_EBR is the open constant), not an independent elementary/Barnes reduction.

No candidate closed form ⟹ **no numerical evaluation, no FIRE, no HALT.** Certificate
`cc3_2s2_2c_coverage_results.json` SHA-256 **c72bec88…**.

---

## 4. op:cc3-2s2-3 — Log-space Barnes battery (PSLQ)

**Targets:** log κ and log A₀ (κ = Γ(4/3)A₀). **Question:** is log κ a ℤ-combination of
{ log G(j/m) (m∈{2,3,4,6,12}), log Γ(j/m), log π, log 2, log 3, log A_Glaisher, 1 }? A relation = κ
**elementary in the extended Barnes class**. Settings: dps 200, detection 150 digits, height ≤ 10¹².

- **Positive control — FIRES:** the Barnes–Glaisher value G(1/2)=2^{1/24}π^{−1/4}e^{1/8}A^{−3/2}
  ⟺ 24 logG(1/2) − log2 + 6 logπ + 36 logA − 3 = 0 is detected exactly (coeffs [24,−1,6,36,−3]).
- **Skip-by-argument:** the pure {log Γ(j/m), log π, log 2, log 3} tier is the log-image of the
  Γ-quotient test, already **nulled for C to 169 digits** (frozen `9a3f942d…`); κ is a Γ-quotient iff
  C_EBR is. Skipped; only Barnes-G/Glaisher-bearing tiers (the new content) are run.
- **Methodology — deflation.** Barnes-G at rational arguments is linearly *dependent* (multiplication
  identities), so raw PSLQ returns basis-internal relations (target coeff 0). The battery **deflates**
  (removes a provably redundant element each time such a relation appears) until either a
  target-bearing relation appears (FIRE) or PSLQ returns None (genuine NULL).

| target | tier | result |
|--------|------|--------|
| log κ | m∈{2,3,4,6} (15-elt) | **NULL** (6 deflations to an independent basis) |
| log κ | m∈{2,3,4,6,12} (19-elt) | **NULL** (8 deflations) |
| log A₀ | m∈{2,3,4,6} | **NULL** (6 deflations) |
| log A₀ | m∈{2,3,4,6,12} | **NULL** (8 deflations) |

> **ALL-NULL** (honest deliverable): log κ and log A₀ are **not** integer-linear in the
> Barnes-G/Glaisher-extended basis (heights ≤ 10¹²) to 150 digits ⟹ κ **not elementary in the
> extended Barnes class** at this height/precision. Consistent with every prior null. **No FIRE.**

Certificate `cc3_2s2_3_barnes_battery_results.json` SHA-256 **1887c410…**.

---

## Four-class ledger (this stage)

| # | statement | class | basis |
|---|-----------|-------|-------|
| CC3-2S2-2A-COORDS | tr(M₀) = −51.0655631399546622698316746099456615679204… (SL₂ trace coordinate of H₂'s topological monodromy; \|tr\|≫2 irreducible); reframe z₀=(a/2)²=1/3 exact; α₊+α₋=3/2; all cross-checks PASS | VERIFIED | `b1fea3ed…` |
| CC3-2S2-2A-METH | accuracy witness = cross-(J,nsteps,radius)+phase+irregular-node invariance, NOT det=1 (structural); two integrator pitfalls fixed (asymmetric truncation; module-level mpf at default dps) | VERIFIED | `b1fea3ed…` |
| CC3-2S2-2B-DICT | gauge chain H₂→u″=ru→(t=x²)→w″=Rw→companion B=[[0,1],[R,0]] (D₈ shape); κ = s\*(B;x=0)×F, F a Γ-quotient in α±; published-Lax match OBSTRUCTED (isomonodromy-time inverse problem) | STRUCTURAL | `87be6028…` |
| CC3-2S2-2C-VERDICT | three-way coverage = **(iii) NOT COVERED**: ILT/GL compute tau-side objects as Barnes-G(monodromy); κ is Lax-side input, never output; H₂ non-rigid ⟹ outside rigid catalogue; κ=Γ(4/3)C_EBR/√π circular | VERIFIED | `c72bec88…` |
| CC3-2S2-3-BARNES | log κ, log A₀ ALL-NULL over Barnes-G/Glaisher-extended basis (m∈{2,3,4,6,12}, H≤10¹², 150 dig), deflation methodology; positive control G(1/2) fired; pure-Γ tier skipped (≡ frozen C-null) | VERIFIED | `1887c410…` |

**Epistemic delta.** H₂ is placed on the PIII(D₈)=D₈⁽¹⁾ monodromy manifold at an explicit point:
the SL₂ trace coordinate **tr(M₀) = −51.0655631399546622698…** (transcendental, irreducible) plus the
off-diagonal Stokes constant κ. The gauge dictionary to the D₈-shape companion Lax form is symbolic
and exact; κ is its x=0 **Lax-side Stokes multiplier** (up to a Γ-amplitude factor), with full
published-Lax matching honestly **obstructed** by the (transcendental) isomonodromy-time inverse
problem. The coverage verdict is **NOT COVERED** — the literature solves the **tau-side** connection
constant / tau function as Barnes-G(monodromy), with κ an **input**, never an output; and H₂'s
non-rigidity excludes the rigid closed-form catalogue. The extended-Barnes PSLQ battery is
**ALL-NULL**. **No transcendence claim at any grade** (CEILING in force; a match would have argued the
opposite). The standing tau-vs-Lax line held at every crossing.

---

## Artifacts (untracked / uncommitted / unminted)

- `cc3_2s2_2a_monodromy.py` + `_results.json` — SHA-256 **b1fea3ed41f87e1a11c2a3743057abdb9e1c242ca7e3d60f471894dc61343c81**.
- `cc3_2s2_2b_dictionary.py` + `_results.json` — SHA-256 **87be6028174634f7253818cbb709ed5ac99199a035cec18160d0bdb21cc5eeff**.
- `cc3_2s2_2c_coverage.py` + `_results.json` — SHA-256 **c72bec8899cf4d2b67cc171935ddf81df22a5f2910c8861e7fda08341503aad7**.
- `cc3_2s2_3_barnes_battery.py` + `_results.json` — SHA-256 **1887c4103ba5e20a54bed3a45fbcea04acc810406b19510eb0b15e4a3aae6e02**.
- Ledger: CC3-2S2-2A-COORDS, -2A-METH, -2B-DICT, -2C-VERDICT, -3-BARNES appended to MAIN
  `claims_cc.jsonl` (79 → 84). `repro/` (FROZEN EBR-III, 45 claims) untouched.
- `cc3_2_entry_dossier.md` §6 routing note appended.

### Literature locators (VERIFIED-by-citation; SHAPE only — exact-matrix transcription deferred to any future numeric use)
- Y. Ohyama, H. Kawamuko, H. Sakai, K. Okamoto, *Studies on the Painlevé equations V: PIII(D₇) and
  PIII(D₈)*, J. Math. Sci. Univ. Tokyo **13** (2006) 145–204. [PIII(D₈) Lax pair]
- A. Fokas, A. Its, A. Kapaev, V. Novokshenov, *Painlevé Transcendents: The Riemann–Hilbert
  Approach*, AMS Math. Surveys Monogr. **128** (2006). [PIII 2×2 linear system, Stokes structure]
- A. Its, O. Lisovyy, A. Prokhorov, *Monodromy dependence and connection constants for Painlevé tau
  functions*, Comm. Math. Phys. **363** (2018) 1–58. [tau connection constant — the tau-side object]
- P. Gavrylenko, O. Lisovyy, *Fredholm determinant and Nekrasov sum representations of isomonodromic
  tau functions*, Comm. Math. Phys. **363** (2018) 1–58; M. Cafasso, P. Gavrylenko, O. Lisovyy,
  irregular Painlevé. [Fredholm/Nekrasov tau — tau-side]
- M. van der Put, M.-H. Saito, Ann. Inst. Fourier **59** (2009) 2611–2667. [moduli of Painlevé linear
  problems; D₈ = both points ramified]
- N. Katz, *Rigid Local Systems*, Ann. Math. Stud. **139** (1996). [rigid ⟹ closed-form Stokes;
  excludes the non-rigid H₂]
- E. W. Barnes (G-function); J. Glaisher / Glaisher–Kinkelin A. [the battery basis; positive-control
  identity G(1/2)=2^{1/24}π^{−1/4}e^{1/8}A^{−3/2}]
