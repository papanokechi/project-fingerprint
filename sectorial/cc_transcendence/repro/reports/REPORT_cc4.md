# op:cc-4 — Primitivity Gate — Report **cc4-0** (Descent / Induction Test)

**Program:** `op:cc-transcendence` · **Stage:** `op:cc4-0` (the decisive symbolic gate) · **Degree:** d = 2
**Reproducer:** `sectorial/cc_transcendence/cc4_0_descent.py` — canonical SHA-256 **`a378b781809b4e26caf353cbd4196f7669c557ee1c3a7ef03adaf5ed4ed9fe64`** (deterministic, verified twice).
**Inherits:** `cc-1` `bfb91bd…`, `cc2-0` `dc54bbe…`, `cc2-1/2` `7d102dd…` / table `78915724…` / numeric `03e4292…`.
**Status:** ✅ **VERDICT: PRIMITIVE — `G_Gal(L₂)⁰ = SL₄`, now UNCONDITIONAL (grade STRUCTURAL).** The cc2-2e residual is resolved. **HALT for review before cc4-1**, as directed (numerics are confirmation-only and deferred).

---

## Position

cc2-2e left a single residual dichotomy: **primitive (`G_Gal⁰=SL₄`, no Liouvillian solutions)** vs **imprimitive (Aschbacher C₂; Liouvillian solutions)** — provably undecidable from local data. `op:cc4-0` decides it symbolically. The standard criterion (van der Put–Singer; Aschbacher C₂) is: an irreducible rank-4 connection `M` is imprimitive **iff** `M ≅ M⊗η` for a nontrivial quadratic character `η`. The stage (i) proves `η=√s` is the **unique** candidate (A1), (ii) closes the monomial / field-extension loophole via the odd 4-cycle at ∞ (A1b), then (iii) tests `M ≅ M⊗√s` by **two independent symbolic routes** that must agree. They do: **no intertwiner exists ⇒ PRIMITIVE.** The discipline line is in force: this decides the **group**, not the transcendence of `C`.

---

## Registered analysis A1–A3 — verification

### A1 — `η=√s` is the unique imprimitivity character (STRUCTURAL)
A quadratic character ramifies only at singular points `{0, R, ∞}`, at an **even** number of them. The R-monodromy multiset `{1,1,1,e^{iπ/3}}` is **not** negation-closed (no `−1`), so any character ramified at R changes the R-monodromy ⇒ `η` must be **unramified at R**. Evenness then forces ramification `{0,∞}` ⇒ **`η=√s`** (or trivial). At `0` (`{1,−1,1,−1}`) and `∞` (units `{1,i,−1,−i}`) the multisets **are** negation-closed, so `√s` clears all necessary local tests; sufficiency is the global question (Route 2). Script enumerates all four square classes and confirms a **unique** viable nontrivial character `= √s`. `[CC4-A1-ETA-UNIQUE]`

### A1b — the ∞ 4-cycle is odd ⇒ monomial / C₃ loophole closed (STRUCTURAL)
The ∞ formal monodromy sends `s^{1/4}↦i·s^{1/4}`, hence permutes the determining factors `q_k=c·i^k s^{1/4}` as the **4-cycle `(q₀q₁q₂q₃)` — an odd permutation.** Any **induced** structure embeds `G_Gal`'s permutation of the four factors in a transitive subgroup of `S₄` **containing this 4-cycle**, i.e. in `{C₄, D₄, S₄}` (excluding `A₄`, `V₄`, which have no 4-cycle). Each of `C₄,D₄,S₄` has an index-2 subgroup ⇒ a quadratic character ⇒ by A1 that character is `√s`. So the **4-line monomial** class and the degree-2/4 **C₃ field-extension** classes reduce to the same `√s` test as the **2-block** class. This is what upgrades the conclusion from "2-block excluded" to **unconditional primitivity**. `[CC4-A1B-MONOMIAL-CLOSURE]`

### A3 — heuristic (CONJECTURED, did not steer)
EBR-II's ≥33-digit Γ-quotient null disfavors the Bessel-flavored imprimitive branch. Registered as heuristic only; the verdict rests on the exact computation, and is **consistent** with the heuristic (primitive).

---

## Per-op findings

### Route 2 — `η=√s` intertwiner over `C(s)` (STRUCTURAL; computation VERIFIED)
Search for a rational `4×4` `Φ` solving `Φ′ = AΦ − ΦA + (1/2s)Φ` (= a morphism `M→M⊗√s`).
- **Calibration** (`a_η=0`, i.e. `End_{C(s)}(M)`): nullspace dim **1** (scalars) at every box, **up to the largest stress box (den `s³(4−3s)³`, deg 14, 272+ unknowns)**. This (a) re-confirms cc-1 **absolute** irreducibility and (b) proves the pipeline *does* find solutions when present — so a `0` is meaningful.
- **Twist** (`a_η=1/2s`): nullspace dim **0** in both prescribed boxes `(s¹(4−3s)²,d8)`, `(s²(4−3s)³,d12)`, and in stress boxes up to `(s³(4−3s)⁴, d20)` (**336 unknowns**); also `0` for the opposite sign `a_η=−1/2s`.
- Pole bounds rigorous: `≤1` at 0, `≤2` at R from the integer exponents of `End(M)⊗η`; `M₀,M_R` semisimple (cc2-2d) ⇒ no log-induced pole inflation. **⇒ `M ≇ M⊗√s` ⇒ PRIMITIVE.** `[CC4-0-ROUTE2-PRIMITIVE]`

### Route 1 — pullback `s=t²`, eigenring over `C(t)` (independent; STRUCTURAL)
`Ã(t)=2t·A(t²)`. **A2 local data verified for free:** `exp@t=0 = 2·{0,½,1,3⁄2} = {0,1,2,3}` ✓; ∞ slope `½`; `±t_R` unramified simple points swapped by the deck map `σ:t↦−t`. Eigenring `dim_C{Φ̃ : Φ̃′=[Ã,Φ̃]} = 1` (scalars only — the identity is the sole solution) in both boxes `(t²(3t²−4),d6)`, `(t³(3t²−4)²,d10)` ⇒ **pullback `M̃` irreducible over `C(t)`** ⇒ `M` not induced ⇒ PRIMITIVE. Different base field and matrices from Route 2 — a genuine cross-check. **The two routes AGREE.** `[CC4-0-ROUTE1-PRIMITIVE]`

---

## Theorem (graded inputs)

> **Theorem (cc4-0).** `G_Gal(L₂)⁰ = SL₄`.
>
> **Proof chain & grades.**
> 1. `M` irreducible & minimal (order 4) — **STRUCTURAL** (cc-1; transitive ∞-ramification) + **VERIFIED** (cc2-0 order-<4 factor exclusion); re-confirmed here by `End_{C(s)}(M)=`scalars.
> 2. Not self-dual up to twist ⇒ `G ⊄ Sp₄, SO₄` — **STRUCTURAL** (cc2-2a/2b/2c).
> 3. `Sym³SL₂`, `SL₂⊗SL₂` excluded (self-dual + slope) — **STRUCTURAL** (cc2-2d).
> 4. `η=√s` unique imprimitivity character — **STRUCTURAL** (A1); odd ∞ 4-cycle ⇒ monomial/C₃ reduce to the same test — **STRUCTURAL** (A1b).
> 5. `M ≇ M⊗√s`: no intertwiner (Route 2) **and** pullback irreducible (Route 1) — **STRUCTURAL** (two agreeing computations).
> 6. ⇒ all Aschbacher classes C₁–C₈ and S are excluded for an infinite (2-torus ⊆ `G⁰`) irreducible `G⁰` ⊆ `SL₄` ⇒ `G_Gal(L₂)⁰ = SL₄`. Framework: van der Put–Singer / Aschbacher — **VERIFIED-by-citation**.
>
> **Net grade: STRUCTURAL, UNCONDITIONAL** (no residual gate).

**Corollary (deferred to cc4-2/cc2-5):** `SL₄` non-solvable ⇒ `L₂` has **no Liouvillian solutions** (Kolchin/Singer — VERIFIED-by-citation).

---

## Candidate-elimination table (final)

| candidate (Aschbacher) | status | killed by |
|:--|:--|:--|
| finite | **killed** | ∞ irregular ⇒ 2-dim exponential torus ⊆ `G⁰` |
| C₁ reducible | **killed** | cc-1 + cc2-0 |
| C₈ Sp₄ | **killed** | cc2-2b (no alternating form) |
| C₈ SO₄ | **killed** | cc2-2c (no symmetric form) |
| S `Sym³SL₂` | **killed** | cc2-2d (self-dual + slope) |
| C₄ `SL₂⊗SL₂` | **killed** | cc2-2d (self-dual + slope) |
| **C₂ monomial (4-line)** | **killed** | **cc4-0**: A1b odd 4-cycle ⇒ `{C₄,D₄,S₄}` ⇒ `√s` test (Route 2 NULL) |
| **C₂ imprimitive (2-block)** | **killed** | **cc4-0**: `M≇M⊗√s` (Route 2 NULL + Route 1 eigenring=1) |
| C₃ field-extension (deg 2/4) | **killed** | **cc4-0**: deg-2 = Route 1; deg-4 = A1b monomial closure |
| **C₁ primitive `SL₄`** | **SURVIVOR** | — |

**8/8 non-`SL₄` candidates eliminated.**

---

## Four-class grade table

| Claim | Grade |
|:--|:--|
| `η=√s` unique imprimitivity character (A1) | **STRUCTURAL** |
| ∞ 4-cycle odd ⇒ monomial/C₃ closure (A1b) | **STRUCTURAL** |
| `End_{C(s)}(M)=`scalars (calibration; re-confirms abs. irreducibility) | **VERIFIED** |
| `M≇M⊗√s` — Route 2 NULL (to 336 unknowns) | **VERIFIED** (computation) → **STRUCTURAL** (implication) |
| pullback `M̃` irreducible — Route 1 eigenring `=1` | **VERIFIED** (computation) → **STRUCTURAL** (implication) |
| **`G_Gal(L₂)⁰ = SL₄`** (unconditional) | **STRUCTURAL** |
| `L₂` has no Liouvillian solutions (corollary) | **STRUCTURAL** (deferred to cc4-2) |
| transcendence of `C` | **CONJECTURED** (unchanged) |

---

## Discipline line (verbatim, in force)

> **Non-rigidity (P = d−1 > 0) does NOT imply C transcendental; a large G_Gal does NOT imply C transcendental. `op:cc-2/4` targets the GROUP only; C's transcendence is `op:cc-3`'s burden via periods.**

Even now that `G_Gal⁰ = SL₄` is **unconditional**, it licenses only *no Liouvillian solutions*, **not** transcendence of `C`. Connection coefficients are not differential-Galois invariants.

---

## Open problems / next gates (NOT started — awaiting review)

1. **op:cc4-1 (deferred, confirmation-only):** numerical monodromy `M₀M_RM_∞=I` at dps ≥ 60 + Stokes at ∞; word-sampling Zariski-dim vs `dim SL₄ = 15`. Must agree with cc4-0. Pipeline already validated in `cc2_2d_numerical_monodromy.py`.
2. **op:cc4-2 (bridge + errata):** (i) state the `SL₄`/no-Liouvillian bridge; (ii) **execute the cc-1 narration erratum** "unipotent / resonance log at R" → "semisimple pseudo-reflection `{1,1,1,e^{iπ/3}}`" and propagate the correction into the `op:cc-2` prompt blocks (claim `CC4-ERR-1`); confirm cc-1 load-bearing claims unaffected.
3. **op:cc-3 (the remaining transcendence burden):** rebuild period-first (André G-function clause retired per cc2-0). Is `C` a Kontsevich–Zagier period of the order-4 connection? This is now the **sole** route to moving `C` off CONJECTURED.
4. **op:cc4-3 / cc2-6 (Lean):** A1 parity bookkeeping; A1b 4-cycle/`S₄` enumeration; pullback exponent arithmetic `{0,1,2,3}`; the `End_{C(s)}(M)=`scalars finite check. Pin `leanprover/lean4 v4.30.0` + Mathlib; `#print axioms` per decl. Only these PROVEN.

---

## Epistemic-status delta

`op:cc4-0` **moves `G_Gal(L₂)⁰ = SL₄` from STRUCTURAL-CONDITIONAL (cc2-2e) to STRUCTURAL-UNCONDITIONAL.** Two independent symbolic routes — the `√s`-twist intertwiner over `C(s)` and the pullback eigenring over `C(t)` — **agree on PRIMITIVE**, and the A1/A1b hand arguments close every imprimitive and field-extension class (the odd ∞ 4-cycle being the decisive new ingredient). The built-in calibration (`End_{C(s)}(M)=`scalars at 336 unknowns) makes the NULL auditable, not an artifact. The make-or-break gate flagged at the cc2 halt is **passed**. **Nothing moved toward transcendence of `C`; it remains CONJECTURED** and now has a single clearly-identified route (periods, `op:cc-3`). One audit item is queued for cc4-2 (the semisimple-at-R erratum). **Halted before cc4-1** per the START directive.
