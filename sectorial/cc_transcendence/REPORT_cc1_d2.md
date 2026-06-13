# op:cc-1 (d = 2) — EBR connection-coefficient program, Stage 1 report

**Task.** `op:cc-transcendence/cc-1` — RIGIDITY / MONODROMY SETUP at degree `d = 2`.
**Discipline.** SIARC four-class (PROVEN / STRUCTURAL / VERIFIED / CONJECTURED),
falsification-first, AEAL provenance. *PROVEN is reserved for Lean; nothing here is
Lean-checked, so the ceiling for this stage is VERIFIED (exact symbolic) / STRUCTURAL.*
**Reproducer.** `sectorial/cc_transcendence/cc1_L2_structure.py`
**Canonical hash.** `bfb91bdeef251be00b770f486ec53d2304f4c1064f85d907a82951a49f5f227e`
**Ledger.** `sectorial/cc_transcendence/claims_cc.jsonl` (CC1-OP-L2 … CC1-DISCIPLINE).

---

## Position

Two prompt assumptions were re-verified before computing (per the STATE_OF_PLAY rule
"re-verify the task's own assumptions"):

1. **Family.** The master prompt's objective line equates `C` with "the growth constant
   δ in the running family" and proposes `V(1,0,1)` as the d = 2 anchor. This is
   **corrected here**: `C` is the connection coefficient of the EBR *order-2d* operator
   for the **positive-b family**, whereas `δ = log R∞` of `V(1,0,1)` is a different
   (Fredholm-determinant) object — "same flavour, distinct ODE" exactly as EBR-II §5
   says of `C` vs `σ_conn`. op:cc-1 concerns `L_d` annihilating `G`, so the d = 2 anchor
   used is the repo-canonical EBR object `b(n) = 3n²+n+1` (β₂ = 3), giving `R = 4/3`,
   `γ = 11/6` (matches `sectorial/physical_type_d2.py`, `files/EBR-paper.md`).

2. **EBR-II DOI.** The prompt's placeholder `10.5281/zenodo.20564…` is wrong. Authoritative
   (`program_graph/dois_resolved.md`): EBR-II **concept** `10.5281/zenodo.20566465`,
   latest version `20571232` (v1.2). `20566466` is the superseded v1.0.

## Per-op-code findings (op:cc-1)

**Operator (located, not reconstructed).** From `Q_n = b(n)Q_{n-1}+Q_{n-2}`, `g_n = Q_n/(2n)!`,
the order-4 annihilator of `G` is `L = P₀(θ) − s·P₁(θ+1) − s²`, `θ = s d/ds`, with
`P₀(n)=(2n)(2n-1)(2n-2)(2n-3)`, `P₁(n)=b(n)(2n-2)(2n-3)`. Cleared to D-form:

| k | aₖ(s) | deg |
|---|-------|-----|
| 4 | `16s⁴ − 12s⁵ = 4s⁴(4−3s)` | 5 |
| 3 | `48s³ − 94s⁴` | 4 |
| 2 | `12s² − 156s³` | 3 |
| 1 | `−30s²` | 2 |
| 0 | `−s²` | 2 |

`a₄ = d^d s^{2d}(d^d − β_d s)` ✓ (cross-checks EBR-I Lemma 4.1 / artifact `3e84f22d`).
Finite singular set = `{0, R = 4/3}`; full singular set `{0, 4/3, ∞}`.

**Riemann scheme.** `exp@0 = {0, 1/2, 1, 3/2} = {j/d}`; `exp@R = {0, 1, 2, −γ}`, `γ = 11/6`.
The dominant `−γ` resonates with `{0,1,2}` ⇒ the EBR-II Remark 2.3 log at `s = R`.

**Point at ∞ is IRREGULAR (the load-bearing correction).** The Fuchs bound
`deg aₖ ≤ deg a₄ − (4−k) = 1+k` holds for `k = 1..4` but **fails at `k = 0`**
(`deg a₀ = 2 > 1`) — caused exactly by the `−s²` term. Newton polygon at ∞: a **single**
edge `(0,2)→(4,5)`, slope `3/4`. Exact edge polynomial `−12c⁴ − 1` (i.e. `c⁴ = −1/12`,
`|c| = (1/12)^{1/4} = 0.53728…`): a single Puiseux cycle of length 4 ⇒ **ramification
exactly 4**, one transitive cyclic (order-4) orbit of determining factors `~ exp(C s^{1/4})`.
**Irregular slope 1/4; integer Poincaré rank = 1.** Numerically corroborated at `s = 1e14`
(scaled roots `w·s^{3/4}`: `|·| → 0.53728`, `arg/π → ±1/4, ±3/4`). This **refutes the repo
EBR-II v1.0 "three regular singular points"** and confirms the corrected (erratum) view.

**Reducibility falsification → REFUTED (a positive result).** "L₂ is reducible over C(s)"
is **false**: a single slope with full transitive ramification leaves the formal module at
∞ with no proper sub-module, so `L₂` is **irreducible** and **minimal** (order 4 = 2d).
Independent null: no rational/polynomial solution ≤ deg 6 (no order-1 rational right factor).
This is the prerequisite irreducibility that op:cc-2 needs for a nontrivial `G_Gal`.

**Accessory / rigidity count.** Old `N_acc=(2d−1)(d−1)=3` (EBR-II v1.0 Prop 3.1) is
**inapplicable** (it assumed ∞ regular). Corrected `P = d−1 = 1` (cross-session erratum)
is **cited, not re-derived here** — a from-scratch Katz index with the irregular point +
Jordan data is the residual gap. Robust either way: the count is **positive ⇒ non-rigid at
d = 2**. *Non-rigid does NOT imply `C` transcendental* (the EBR-II discipline line, held).

## Four-class grade table

| Result | Grade |
|--------|-------|
| `L₂` explicit; `a₄ = 4s⁴(4−3s)`; finite singular `{0, 4/3}` | **VERIFIED** (exact symbolic; cross-checks EBR-I) |
| Riemann rows `exp@0={j/2}`, `exp@R={0,1,2,−11/6}` | **VERIFIED** (exact symbolic) |
| ∞ irregular; slope 1/4; ramification 4; Poincaré rank 1 | **VERIFIED** (exact edge poly + numeric) |
| `L₂` irreducible & minimal over C(s) | **STRUCTURAL** (transitive ramification + van der Put–Singer locator) |
| Corrected accessory count `P = d−1` | **VERIFIED-by-citation** (erratum); independent recompute = gap |
| Non-rigidity at d = 2 is robust | **VERIFIED** |
| Transcendence of `C` | **CONJECTURED** (unchanged) |

## Open problems (with op-codes)

1. **`op:cc-2` (next gate).** Identify the differential Galois group `G_Gal(L₂)` over
   `C(s)` for the now-known irreducible order-4 operator with one irregular (slope-1/4,
   rank-1) point. Kovacic (order 2) does not apply directly; use order-4
   Compoint–Singer / van der Put–Singer machinery. **Make-or-break for transcendence.**
2. **`op:cc-1b` / residual.** Independently re-derive `P = d−1` via the Katz rigidity
   index *with* the irregular point and the explicit local data at `{0, R}` (the `s=R`
   semisimple pseudo-reflection `{1,1,1,e^{iπ/3}}` — **[ERRATUM CC4-ERR-1: was "resonance
   log"; M_R is SEMISIMPLE, no log, since γ=11/6∉ℤ — see cc2-2d / cc4-1]**; the
   `{1,−1,1,−1}` eigenvalue multiplicities at `s=0`).
3. **Corpus.** The deposited EBR-II (concept `20566465`) "three regular singular points"
   + `N_acc=(2d−1)(d−1)` needs the irregular-∞ erratum landed on the public record;
   confirm whether v1.2 (`20571232`) already carries it.
4. **`op:cc-6` (Lean).** Finitary cores formalizable now: the `aₖ` extraction and
   `a₄` factorization at fixed d; the Fuchs degree-bound violation at `k=0`; the Newton
   edge `(0,2)→(4,5)` / ramification-4 arithmetic; the resonance condition `γ ∈ ℤ`.
   Only these would earn grade PROVEN.

## Epistemic-status summary (one paragraph)

op:cc-1 at d = 2 moved three things into **VERIFIED** (exact symbolic, hashed): the explicit
order-4 operator `L₂` with `a₄ = 4s⁴(4−3s)`; its Riemann scheme; and the **irregularity of
the point at ∞** (single slope 1/4, ramification 4, integer Poincaré rank 1, caused by the
`−s²` term) — which independently confirms the erratum and refutes the repo EBR-II v1.0
"three regular singular points." It moved one thing into **STRUCTURAL**: the falsification
target "L₂ reducible" is **refuted** — `L₂` is irreducible and minimal over C(s) by transitive
ramification, the prerequisite for op:cc-2. The corrected accessory count `P = d−1` is carried
**by citation** (independent Katz-index recompute is a flagged gap), and non-rigidity at d = 2
is robust to the correction. The **transcendence of `C` remains CONJECTURED**; non-rigidity is
explicitly *not* taken as evidence for it. **HALT for review before op:cc-2.**
