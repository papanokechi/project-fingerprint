# op:cc-4 — Group-Program CLOSE — Report **cc4-CLOSE**

**Program:** `op:cc-transcendence` · **Stage:** `op:cc4-CLOSE` = `cc4-0b` + `cc4-1` + `cc4-2` + `cc4-3` · **Degree:** d = 2
**Discipline:** SIARC four-class (PROVEN = Lean only / STRUCTURAL / VERIFIED / CONJECTURED), falsification-first, SHA-256 + dps per artifact, AEAL ledger `claims_cc.jsonl`. **Standing meta-rule:** nothing committed/pushed/moved/deleted; all artifacts untracked in `sectorial/cc_transcendence/`.

**Inherits:** `cc-1 bfb91bd…`, `cc2-0 dc54bbe…`, `cc2-1/2 7d102dd…`/`78915724…`/`03e4292…`, `cc4-0 a378b781…`.

**Status:** ✅ **STAGE COMPLETE. `B ≤ 20` confirmed at cc4-0b ⇒ proceeded cc4-1 → cc4-2 → cc4-3 without halt, as directed.** The group program is **CLOSED**: `G_Gal(L₂)⁰ = SL₄` is now **STRUCTURAL, UNCONDITIONAL, bound-complete**. `C` recomputed to **169 digits** (third channel). Four Lean cores **PROVEN**. Two errata executed. **Transcendence of `C` is untouched — still CONJECTURED — and is handed to `op:cc-3` (periods).**

---

## Position

cc4-0 settled PRIMITIVE (`G_Gal⁰=SL₄`) by two agreeing routes but left **one open audit item**: the rational-solution search ansatz bounds (deg 8 / 10) were *empirical*. cc4-CLOSE (i) **rigorizes those bounds**, (ii) acquires the high-precision **connection/Stokes corpus** that `op:cc-3` will need, (iii) writes the graded **bridge** and executes the queued **errata**, and (iv) lands the **Lean finitary cores**. After this stage the differential-Galois question on `L₂` is finished; the only surviving lever on `C` is period theory.

---

## 1 · cc4-0b — degree-bound rigorization  `[CC4-0B-BOUNDS]` (STRUCTURAL)

**Reproducer:** `cc4_0b_bounds.py` — canonical SHA `b37fb6ead7064b7454670ca3431903a1993f277ad0878e3badf78916b3ce1509` (deterministic, verified twice).

**Hand proof (the theorem's last gap).** Let `f` be a rational horizontal section of the connection `N` whose rational solutions each search enumerates (`N = End(M)⊗√s`, Route 2; `N = End(M̃)`, Route 1). `N` is regular-singular at the finite points, with **End-exponents = pairwise differences of the `M`-exponents** there (residue of `End` = `ad` of residue of `M`), shifted by the η-exponent. Since `M₀`, `M_R` are **SEMISIMPLE** (CC2-2D-JORDAN ⇒ no logs), near a finite singular point `p` we have `f = Σ cᵢ (s−p)^{ρᵢ} hᵢ` with `hᵢ` holomorphic units; single-valuedness (rationality) forces `cᵢ = 0` whenever `ρᵢ ∉ ℤ`. Hence

> **pole order of `f` at `p` ≤ −min{ End-exponents at `p` that lie in ℤ }.**

At `∞`, a rational `f` has slope 0, so its leading `u=1/s` exponent lies in the slope-0 spectrum of `N` (the rank-`(deg)` cyclic piece of the ramified formal monodromy, exponents `{0,1/r,…,(r−1)/r}`, `r=4` Route 2 / `r=2` Route 1, η-shifted) **and must be an integer** ⇒ the growth bound.

**Result.**

| Route | pole bounds | ∞ growth | **B** |
|:--|:--|:--:|:--:|
| 2 — `End(M)⊗√s` over ℂ(s) | ≤1 at `s=0`, ≤2 at `s=R` | 0 | **B₂ = 3** |
| 1 — `End(M̃)` eigenring over ℂ(t) | ≤3 at `t=0`, ≤2 at each `t=±t_R` | 0 | **B₁ = 7** |

Both **≤ 20**. The bound-complete boxes actually executed in cc4-0 — `[s(4−3s)², deg≤8]` (Hom dim **0**) and `[t³(3t²−4)², deg≤10]` (eigenring dim **1**) — **strictly contain** `B₂, B₁` and match the pole bounds. **No rerun triggered.** ⇒ `CC4-0-ROUTE2/1-PRIMITIVE` upgrade to **bound-complete**; **`G_Gal(L₂)⁰ = SL₄` is citable as UNCONDITIONAL STRUCTURAL.**

---

## 2 · cc4-1 — numerical corpus (confirmation + cc-3 inputs)

### 2a · THE CENTERPIECE — connection coefficient, third channel  `[CC4-1-C-120D]` (VERIFIED)
**Reproducer:** `cc4_1_connection.py` — canonical SHA `f3400831cc9644641e44de7bcb69e4ec9c8fc69654ab46eb9768067ac2aa13fd`, dps 170.

Computed via the connection-matrix/Frobenius pipeline at `R` (independent of the EBR-I prefactor and the EBR-II continuation):

- **Amplitude** `A` (coeff. of the dominant `(1−s/R)^{−γ}`, `γ=11/6`):
  `A = 2.8743685099572807503479558203980600569919284184312…`
- **Prefactor** `C_EBR = A/Γ(11/6) = 3.0557068078904813657019122017276813688755427749738…`
- **≥ 169 stable digits** (target 120 **exceeded**), self-validated by **multi-point** (`s*=1.0` vs `0.9` → 169-digit agreement) ∧ **multi-precision** (dps 170 vs 210 → 169). Channel I (Richardson on the coefficient asymptotics, widely-spaced Neville) **independently confirms to 77 digits.**
- **Honest interval note:** mpmath `mpf`, **not** formal Arb intervals — VERIFIED, not PROVEN. This 169-digit value is the primary **`op:cc-3` PSLQ ammunition.**

### 2b · no-log / semisimplicity, to 169 digits  `[CC4-1-NOLOG]` (VERIFIED)
The Frobenius solve's free coefficients at the integer-exponent resonances `{0→1, 0→2, 1→2}` are forced with residual `≈ 0` **to 169 digits** ⇒ **no logarithm at `R`** ⇒ `M_R` semisimple. This **deepens the dps-40 CC2-2D-JORDAN finding by ~129 digits** and is the exact-arithmetic basis of CC4-ERR-1.

### 2c · local monodromy, exact  `[CC4-1-MONODROMY]` (VERIFIED)
In the semisimple Frobenius bases `M₀ = diag(1,−1,1,−1)` (exps `{0,½,1,3/2}`), `M_R = diag(1,1,1,e^{iπ/3})` (exps `{0,1,2,−11/6}`) — **exact** from the Riemann scheme, so the "dps ≥ 120 monodromy" request is met **symbolically**; numerical confirmation at dps 40 (cc2-2d) + the 169-digit residuals above. `det M₀ = 1`, `det M_R = e^{iπ/3}`.

### 2d · Stokes / formal structure at ∞  `[CC4-1-STOKES]` (VERIFIED layout; numerical multipliers honestly DEFERRED)
**Reproducer:** `cc4_1_stokes.py` — canonical SHA `c5d943d4b3b415cbe4320e3a3e07e61eaffb66d06d4f31e317b867f402f16c88`.

- **Determining factors** `q_k = γ_k s^{1/4}`, `γ_k⁴ = −1/12` (`|γ|=(1/12)^{1/4}`, args **odd·π/4**).
- **Singular directions:** 8 in the `w=s^{1/4}` plane (spaced `π/4`); a single `s`-loop = quarter-turn in `w`, cycling the four `q_k`.
- **Formal monodromy** = a single **4-cycle** (perm sign `−1`) × `diag(e^{2πi μ_k})`.
- **Determinant consistency** of `M₀ M_R M_∞ = I` forces **`det M_∞ = e^{−iπ/3}` ⇒ `Σμ_k ≡ 1/3 (mod 1)`** — a rigorous constraint any Stokes computation must satisfy.
- **HONEST SCOPE:** the explicit **numerical Stokes multipliers** at ramified slope 1/4 require Borel–Laplace multisummation and were **NOT completed on host.** Per the stage prompt this is stated openly; the cyclic-identity check is **not** replaced by a weaker proxy. The det-constraint above is the partial, rigorous check delivered in its place.

---

## 3 · cc4-2 — bridge + errata

### Bridge statement (graded)  `[CC4-2-BRIDGE]`
1. **`G_Gal(L₂)⁰ = SL₄`** — **STRUCTURAL**, now **bound-complete** (§1), unconditional.
2. **Corollary:** `L₂` has **no Liouvillian solutions** (`SL₄` non-solvable) — **VERIFIED-by-citation** (Kolchin; Singer; van der Put–Singer ch. 4) + STRUCTURAL application.
3. **NON-IMPLICATION (verbatim):** connection coefficients are **not** differential-Galois invariants; **transcendence of `C` remains CONJECTURED**, and its **sole** route is `op:cc-3` (periods, post-André per CC2-0-CC3-AMEND).

> **Discipline line (verbatim, in force):** Non-rigidity (P = d−1 > 0) does NOT imply C transcendental; a large G_Gal does NOT imply C transcendental. `op:cc-2/4` targets the GROUP only; C's transcendence is `op:cc-3`'s burden via periods.

### Errata log
- **`[CC4-ERR-1]`** (VERIFIED) — "unipotent / resonance log at R" → **"semisimple pseudo-reflection `{1,1,1,e^{iπ/3}}`, no log"** (`γ=11/6 ∉ ℤ`). Inline `[ERRATUM CC4-ERR-1]` markers applied to **`OP_CC2_PROMPT.txt`** (local-monodromy block) and **`REPORT_cc1_d2.md`** (open-problems item 2); the cc-2 report already states it. cc-1 load-bearing claims unaffected. Evidence: CC2-2D-JORDAN (2 channels) + CC4-1-NOLOG (169 digits). Patch artifact: **`ERRATUM_cc4_narration.md`**.
- **`[CC4-ERR-2]`** (VERIFIED) — CC2-0-GFUNC scope audit **CONFIRMED**: the ledger entry is already `NORMALIZATION-SCOPED` to `g_n=Q_n/(2n)!` with the explicit "does not extend to rescalings" caveat, and CC2-0-QINT makes "no collapse" precise. **No conflicting shared-memory entry found** ⇒ nothing to downvote/rewrite. Disposition: CONFIRMED, no patch required.

---

## 4 · cc4-3 — Lean finitary cores (PROVEN)

**Project:** `sectorial/cc_transcendence/lean/cc4_cores/` — `leanprover/lean4:v4.30.0` + Mathlib `v4.30.0` (rev `c5ea0035`). `lake build` **succeeds**; `Cc4Cores.lean` SHA `cfcbd647cad1c1892ee4639665fb992551b8c33d5fa2a625794b1e0ff54a5222`. Audit log: `AXIOM_AUDIT.txt`.

| Core | Declarations | Content | `#print axioms` | Claim |
|:--|:--|:--|:--|:--|
| 1 (cc4-0b) | `Bound.{B2_eq, B1_eq, bounds_le_twenty}` | `B₂=3, B₁=7, both ≤20` | **no axioms** | `CC4-LEAN-BOUNDS` |
| 2 (A2) | `Pullback.{pulled_values, pulled_all_integral}` | `s=t²` doubles `{0,½,1,3/2}→{0,1,2,3}⊂ℤ` | `{propext, Classical.choice, Quot.sound}` | `CC4-LEAN-PULLBACK` |
| 3 (A1) | `Parity.{angles0_neg_closed, anglesR_not_neg_closed}` | exp@0 negation-closed; exp@R **not** | `{propext, Classical.choice, Quot.sound}` | `CC4-LEAN-PARITY` |
| 4 (A1b) | `FourCycle.{c4_sign, c4_not_mem_alternating}` | 4-cycle `sign=−1` ⇒ ∉ `A₄` | `{propext, Classical.choice, Quot.sound}` | `CC4-LEAN-A1B` |

All cones ⊆ `{propext, Classical.choice, Quot.sound}`, **no `sorryAx`** ⇒ all four **PROVEN**. (Eigenvalue negation `λ↦−λ` is correctly encoded as the angle shift `k↦k+3` in `ZMod 6`, since `−1 = e^{2πi·3/6}`.)

---

## 5 · Four-class grade table (stage)

| Claim | Grade |
|:--|:--|
| cc4-0b bounds `B₂=3, B₁=7 ≤ 20` ⇒ SL₄ bound-complete | **STRUCTURAL** |
| `C`: `A`, `C_EBR` to 169 digits (third channel) | **VERIFIED** |
| no-log at `R` to 169 digits (`M_R` semisimple) | **VERIFIED** |
| `M₀, M_R` exact; det consistency `det M_∞=e^{−iπ/3}` | **VERIFIED** |
| Stokes symbolic layout (numerical multipliers **deferred, honest**) | **VERIFIED (partial)** |
| **`G_Gal(L₂)⁰ = SL₄`** (unconditional, bound-complete) | **STRUCTURAL** |
| `L₂` no Liouvillian solutions | **VERIFIED-by-citation** + STRUCTURAL |
| CC4-ERR-1 narration erratum; CC4-ERR-2 scope audit | **VERIFIED** |
| Lean cores ×4 (bounds, pullback, parity, A1b) | **PROVEN** |
| **transcendence of `C`** | **CONJECTURED** (unchanged) |

---

## 6 · Epistemic-status delta

cc4-CLOSE **closes the differential-Galois program** on `L₂`. The last empirical gap (cc4-0 ansatz bounds) is **rigorized** (`B₂=3, B₁=7 ≤ 20`, hand-proved from semisimplicity + single-valuedness), so **`G_Gal(L₂)⁰ = SL₄` is now unconditional STRUCTURAL.** The connection coefficient is recomputed through a **genuinely independent third channel to 169 digits** (≫ the 120 target, ≫ EBR-II's 33), with an exact-arithmetic 169-digit confirmation that `M_R` carries **no log** (retiring the EBR-II "log at R" narration via CC4-ERR-1). Four finitary cores are **PROVEN** in Lean v4.30.0 with clean axiom cones. The Stokes-multiplier leg is **honestly incomplete** (ramified slope-1/4 multisummation beyond host scope), delivered instead as a closed-form layout + a rigorous determinant constraint — no silent proxy. **Nothing moved toward transcendence of `C`; it remains CONJECTURED**, now with a single clearly-identified route.

---

## 7 · Readiness assessment for the two successor ops

**`op:ebr3-assemble` (paper extraction) — READY.** The group story is complete and self-consistent: a graded theorem (`G_Gal⁰=SL₄`, bound-complete), an 8/8 Aschbacher elimination table (REPORT_cc4.md), corrected narration (no "log at R"; semisimple pseudo-reflection), and a 38-entry AEAL ledger with reproducer hashes. Loose ends are cosmetic: (a) propagate the EBR-II irregular-∞ erratum to the public record; (b) the deposited EBR-II "three regular singular points / `N_acc=(2d−1)(d−1)`" needs the `P=d−1` correction landed. No mathematical gap blocks extraction of the **group** results.

**`op:cc-3` (period rebuild, post-André) — READY, with inputs in hand.** The André G-function clause is retired (CC2-0-CC3-AMEND); cc-3 must argue **period-first**. It now has: the **169-digit `C` / `C_EBR`** (PSLQ target against period/Γ bases), the **exact local monodromy** and the **det-consistency `Σμ_k≡1/3`** constraint, and the **Stokes layout** (the one genuinely-hard numeric — the slope-1/4 multipliers — is flagged as the first technical task if the cyclic identity is needed). Central question to pose: **is `C` a Kontsevich–Zagier period of the order-4 connection** (a period/Stokes quantity of the second kind), and do any *unconditional* transcendence results apply? `SL₄` gives "no Liouvillian solutions" but, by the discipline line, **no** transcendence of `C` — that remains entirely cc-3's burden.

---

## Artifact inventory (all untracked, `sectorial/cc_transcendence/`)

| Artifact | Canonical SHA-256 |
|:--|:--|
| `cc4_0b_bounds.py` (+`_results.json`) | results `b37fb6ea…` |
| `cc4_1_connection.py` (+`_results.json`) | results `f3400831…` |
| `cc4_1_stokes.py` (+`_results.json`) | results `c5d943d4…` |
| `lean/cc4_cores/Cc4Cores.lean` (+`Audit.lean`, `AXIOM_AUDIT.txt`) | source `cfcbd647…` |
| `ERRATUM_cc4_narration.md` | — |
| `claims_cc.jsonl` | **38 claims** (12 new: CC4-0B/CC4-1×4/CC4-2-BRIDGE/CC4-ERR×2/CC4-LEAN×4) |

**STAGE HALT — group program CLOSED. Next: `op:ebr3-assemble` and/or `op:cc-3`.**
