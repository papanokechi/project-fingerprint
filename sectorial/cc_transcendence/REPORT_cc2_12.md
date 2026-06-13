# op:cc-2 — Differential Galois Group of L₂ — Gate Report **cc2-1 + cc2-2**

**Program:** `op:cc-transcendence` · **Stage:** `op:cc2-1` (twist) + `op:cc2-2a–2e` (invariant-form battery) · **Degree:** d = 2
**Reproducers:**
- `sectorial/cc_transcendence/cc2_1_2.py` — canonical SHA-256 `7d102ddcf95f89a2939223741770cb01c73e747862239a9c36eb3526e203877c`
- `sectorial/cc_transcendence/cc2_2d_numerical_monodromy.py` — canonical SHA-256 `03e4292669c861ddd3815d3179a876828a83e22702a517de43411a06fe625118` (dps 40)
- Hashed artifact `cc2_1_twisted_exponent_table.json` — SHA-256 `7891572431673b7393f3c2885df9f2604414bf92e417376ef3e00d4c857f31c9`

**Inherits:** `cc-1` sha `bfb91bd…f227e`, `cc2-0` sha `dc54bbe…b5eb`.
**Status:** ⚠️ **HALT after the elimination table**, as directed. The make-or-break verdict (`G_Gal⁰ = SL₄`) is **STRUCTURAL-CONDITIONAL**: the residual *primitive vs imprimitive* dichotomy is **not** decidable from local data and is handed to `op:cc-4`. **One inherited-state claim was REFUTED and corrected** (no log at R). Prediction **P2 was not refuted** (all its computational legs passed); no unconditional early-HALT was triggered.

---

## Position

`op:cc2-1+2` normalizes the determinant and then runs the full invariant-form / tensor / imprimitivity battery to pin `G = G_Gal(L₂) ⊆ SL₄` over `C(s)`. The stage tests two registered predictions — **P1** (local self-duality at ∞) and **P2** (global non-self-duality ⇒ survivor SL₄) — *without assuming them*. The discipline line is in force throughout: identifying the **group** says nothing about the **transcendence of C** (that is `op:cc-3`'s burden via periods).

---

## Per-op findings

### op:cc2-1 — determinant / twist (VERIFIED)
- `w′/w = −a₃/a₄ = (24−47s)/(2s(3s−4)) = −3/s + (29/2)/(4−3s)`, so the Wronskian is
  **W = s⁻³(4−3s)^(−29/6)**; det-exponents `{0: −3, R: −29/6}`.
- Cross-check `W_exp = (Σ local exponents) − n(n−1)/2` (n=4 ⇒ 6): residual **0** at both 0 and R. ✓
- The SL₄-normalizing twist **χ = det^{1/4} = s^(−3/4)(4−3s)^(−29/24) is ALGEBRAIC** over `C(s)` (rational powers; not rational, not properly Liouvillian).
- Twisted exponents (load-bearing artifact, hashed): `{3/4, 5/4, 7/4, 9/4}` at 0 and `{29/24, 53/24, 77/24, −5/8}` at R — **each sums to 6** (SL₄ normalization; Wronskian constant). `[CC2-1-TWIST]`

### op:cc2-1 (cont.) — exponential torus at ∞ (STRUCTURAL)
- Determining-factor leading units `c·{1, i, −1, −i}` generate a **ℤ-module of rank 2**, so the formal **exponential torus T at ∞ has dimension 2**, weights `{+e₁, −e₁, +e₂, −e₂}`.
- The weight set is **closed under negation** ⇒ **P1 CONFIRMED**: `Λ²L₂` has a rank-2 slope-0 piece at ∞ (the cancelling pairs (0,2),(1,3)). `[CC2-1-EXPTORUS]`

### op:cc2-2a — adjoint / self-duality (STRUCTURAL, exact)
- R-monodromy eigenvalues `= exp(2πiρ)`, `ρ∈{0,1,2,−11/6}` `= {1, 1, 1, e^{iπ/3}}`.
- Any invariant form, even up to a twist `V ≅ V*⊗κ`, needs the multiset inversion-closed up to κ; the multiplicity-3 value pins **κ = 1**, then `e^{iπ/3} ≠ e^{−iπ/3}`.
- **Verdict: NO invariant symmetric or alternating form, even up to twist ⇒ G ⊄ SO₄ and G ⊄ Sp₄.** Exact, uses only the −11/6 exponent. **Confirms P2.** `[CC2-2A-SELFDUAL]`

### op:cc2-2b / 2c — exterior & symmetric square (VERIFIED)
- `Λ²L₂` has **order 6** (no symplectic order-drop to 5). At ∞: rank-2 slope-0 ⊕ rank-4 slope-1/4 (= P1).
- Rational-form search `P′ = −AᵀP − PA` (A = companion):
  - **antisymmetric P** (→ Sp₄): nullspace dim **0** in both boxes (`s^a(4−3s)^b`, num deg d: box1 a=b=4,d=10; box2 a=b=3,d=8). **NULL ⇒ G ⊄ Sp₄.** `[CC2-2B-SP4]`
  - **symmetric P** (→ SO₄): nullspace dim **0** in both boxes. **NULL ⇒ G ⊄ SO₄.** `[CC2-2C-SO4]`
- Bounds reported so the nulls are auditable; closure to *all* twists is the exact `CC2-2A` argument.

### op:cc2-2d — Jordan structure, tensor & imprimitivity

**🔴 AUDIT CORRECTION — M_R is SEMISIMPLE, not unipotent. `[CC2-2D-JORDAN]`**
Two independent channels:
- **Exact symbolic Frobenius at R:** every resonance obstruction on the eigenvalue-1 tower {0,1,2} **vanishes** — `P̃₁(0)=0`, `P̃₁(1)=0`, `P̃₂(0)=0` — giving **3 independent log-free solutions** ⇒ geom mult = alg mult = 3 ⇒ **no logarithm**.
- **Numerical monodromy (dps 40):** `rank(M_R − I) = 1` (singular values 2.159, then ≤1e-30) ⇒ geom mult of eigenvalue 1 is 3.

So `M_R` is a **semisimple complex pseudo-reflection of order 6**, eigenvalues `{1,1,1,e^{iπ/3}}`; `M_0` is likewise semisimple, `{1,−1,1,−1}`. This **refutes the inherited-state narration "resonance log / unipotent part at R."** It is **consistent with EBR-II's own criterion** (a −γ resonance log needs **γ∈ℤ**; here γ = 11/6 ∉ ℤ). cc-1's load-bearing claims are unaffected; only the *"unipotent"* adjective needs a one-line **cc-1 narration erratum**.

**Tensor / symmetric-power exclusions (STRUCTURAL). `[CC2-2D-TENSOR]`**
- **Sym³SL₂ (class S):** self-dual up to twist (contra `CC2-2A`) **+** slope (rank-2 ⇒ ramification ≤ 2 ≠ 4; factors {3φ,φ,−φ,−3φ} have two magnitudes). Excluded.
- **SL₂⊗SL₂ (class C₄ tensor):** self-dual up to twist (contra `CC2-2A`) **+** slope. Excluded.

**🟡 Imprimitivity NOT excludable from local data — DEFERRED to op:cc-4. `[CC2-2D-IMPRIM]`**
With both `M_0`, `M_R` semisimple, the anticipated "M_R unipotent ⇒ not monomial" route is **void**. Structurally: the connected 2-torus `T ⊆ G⁰` fixes every block (blocks must be weight-line spans); the ∞ formal monodromy is a single 4-cycle that **preserves** the 2-block system `{{L₁,L₃},{L₂,L₄}}` (swapping the blocks); and `M_R = diag(1,1,1,e^{iπ/3})` in the weight basis preserves that same system. So the local data at {0, R, ∞} are **fully compatible** with an imprimitive 2-block (Aschbacher **C₂**) structure (and the monomial degeneration). Excluding it requires the **global** relation `M₀ M_R M_∞ = I` + the ∞ connection/Stokes data = **op:cc-4**.

### op:cc2-2e — candidate elimination table

| candidate (Aschbacher) | status | killed by |
|:--|:--|:--|
| finite | **killed** | ∞ irregular ⇒ `G⁰ ⊇` 2-dim exponential torus (infinite, connected) |
| reducible | **killed** | cc-1 irreducibility (transitive ℤ/4 slope orbit) + cc2-0 order-<4 factor exclusion |
| Sp₄ (C₈ alt form) | **killed** | `CC2-2B`: no invariant alternating form (Λ² search NULL; eigenvalues not inversion-closed) |
| SO₄ (C₈ sym form) | **killed** | `CC2-2C`: no invariant symmetric form (Sym² search NULL) |
| Sym³SL₂ (class S) | **killed** | `CC2-2D-TENSOR`: self-dual up to twist + slope |
| SL₂⊗SL₂ (C₄ tensor) | **killed** | `CC2-2D-TENSOR`: self-dual up to twist + slope |
| monomial (C₂, 4 lines) | **OPEN → cc2-4** | `M₀,M_R` semisimple; torus + pseudo-reflection compatible with the 4-line system |
| imprimitive (C₂, 2+2) | **OPEN → cc2-4** | local data compatible with block system `{{L₁,L₃},{L₂,L₄}}` |
| **SL₄ (C₁ primitive)** | **candidate (pending cc2-4)** | survivor **iff** imprimitive/monomial excluded |

**Verdict (STRUCTURAL-CONDITIONAL).** Six of eight candidates are killed. The residual dichotomy is
> **PRIMITIVE** `[G_Gal(L₂)⁰ = SL₄; no Liouvillian solutions]`  vs  **IMPRIMITIVE** `[C₂: monomial torus or 2-block ⊆ GL₂×GL₂; Liouvillian solutions exist]`,

which is **not** decidable from the local data and is the burden of **op:cc-4** (global monodromy + connection at ∞). Hence `G_Gal(L₂)⁰ = SL₄` is asserted **STRUCTURAL-CONDITIONAL**, not as a clean result. `[CC2-2E-VERDICT]`

---

## Status of the registered predictions

- **P1 (local self-duality at ∞): CONFIRMED.** Determining factors negation-closed; `Λ²` rank-2 slope-0 piece; exp-torus weights `{±e₁,±e₂}`.
- **P2 (global non-self-duality): computational legs ALL CONFIRMED**, conclusion **REFINED not refuted.** Eigenvalues `{1,1,1,e^{iπ/3}}` and both NULL form-searches are exactly as predicted, so **no early-HALT fired**. But P2's *leap* "non-self-dual ⇒ survivor SL₄" is **incomplete**: non-self-duality kills Sp₄/SO₄/tensor/Sym³ but **not** the (generally non-self-dual) imprimitive **C₂** class. Honest survivor set = `{SL₄, imprimitive-C₂}`; cc-4 decides.
- **P1/P2 consistency:** the negation-closed ∞ pairing does **not** globalize to a G-invariant form because `M_R`'s unpaired `e^{iπ/3}` breaks inversion-closure. No contradiction.

---

## Four-class grade table

| Claim | Grade |
|:--|:--|
| Wronskian `W=s⁻³(4−3s)^(−29/6)`; χ=det^{1/4} algebraic; twisted exponents sum 6 | **VERIFIED** |
| exponential torus at ∞ has dim 2; weights `{±e₁,±e₂}` (P1) | **VERIFIED** + **STRUCTURAL** (T⊆G⁰) |
| L₂ not self-dual up to any twist ⇒ G ⊄ SO₄, G ⊄ Sp₄ (exact eigenvalue proof) | **STRUCTURAL** |
| Λ² / Sym² rational-form searches NULL (both boxes) | **VERIFIED** |
| **M_R (and M_0) SEMISIMPLE — corrects inherited "log at R"** (2 channels) | **VERIFIED** + **STRUCTURAL** |
| Sym³SL₂ and SL₂⊗SL₂ excluded (self-dual + slope) | **STRUCTURAL** |
| monomial / imprimitive **not** locally excludable; deferred to cc-4 | **STRUCTURAL** |
| `G_Gal(L₂)⁰ = SL₄` | **STRUCTURAL-CONDITIONAL** (on cc-4 primitivity) |
| transcendence of C | **CONJECTURED** (unchanged) |

Citations are **VERIFIED-by-citation**: van der Put–Singer ch. 3–4 (formal classification, exponential torus, invariant forms, Aschbacher-style maximal subgroups), Beukers–Heckman (reflection methodology, heuristic input only here), Kolchin/Singer (solvable G⁰ ⇔ Liouvillian solutions).

---

## Open problems (with op-codes)

1. **op:cc-4 (now the make-or-break gate):** global monodromy `M₀, M_R, M_∞` (+ connection/Stokes at ∞) to decide **primitive (SL₄) vs imprimitive (C₂)** — equivalently **no Liouvillian solutions vs Liouvillian**. Numerical channel already validated here (`cc2_2d_numerical_monodromy.py`).
2. **cc-1 narration erratum:** replace "unipotent / resonance log at R" with "semisimple pseudo-reflection `{1,1,1,e^{iπ/3}}`" (eigenvalues, exponents, irreducibility, irregular-∞ all stand).
3. **op:cc2-6 (Lean finitary core):** candidates that genuinely formalize now — the Wronskian-exponent computation `−a₃/a₄ → W=s⁻³(4−3s)^(−29/6)`; the indicial polynomials at 0 and R; the resonance-obstruction arithmetic (`P̃₁(0)=P̃₁(1)=P̃₂(0)=0`); the ℤ-rank-2 exp-torus lattice computation.
4. **op:cc-3 (unchanged):** is C a period (Kontsevich–Zagier) of the order-4 operator? (André G-function route already retired in cc2-0.)

---

## Discipline line (verbatim, in force)

> **Non-rigidity (P = d−1 > 0) does NOT imply C transcendental; a large G_Gal does NOT imply C transcendental. `op:cc-2` targets the GROUP only; C's transcendence is `op:cc-3`'s burden via periods.**

Even a *confirmed* `G_Gal⁰ = SL₄` (non-solvable) would license only **"no Liouvillian solutions"** (cc2-5), **not** transcendence of C.

---

## Epistemic-status delta

This stage **moved several claims to VERIFIED/STRUCTURAL** (determinant/twist; algebraic χ; SL₄-normalized twisted exponents; 2-dim exponential torus; non-self-duality ⇒ ⊄ SO₄/Sp₄; Λ²/Sym² nulls; Sym³SL₂ and SL₂⊗SL₂ exclusions) and **corrected one inherited error** (M_R is **semisimple**, not unipotent — refuting "resonance log at R", consistent with EBR-II's γ∈ℤ criterion). The headline `G_Gal⁰ = SL₄` is **STRUCTURAL-CONDITIONAL**: six of eight candidates are eliminated, and the analysis **sharply localizes** the one remaining question to **primitive vs imprimitive (C₂)** — equivalently **non-Liouvillian vs Liouvillian** — which provably needs the **global** monodromy of **op:cc-4**. Prediction **P2's computational content passed** (no early-HALT), while its informal "⇒ SL₄" leap was shown to omit the non-self-dual imprimitive class. **Nothing moved toward transcendence of C; it remains CONJECTURED.** **Halted before cc2-3 / cc2-4** per the START directive.
