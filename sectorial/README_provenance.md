# Reproducibility provenance — EBR (positive-b) preprint

> **Source note.** This table is cross-checked against the finalized
> `EBR-paper.md` §8 provenance (now present). All 7 §8 shas match the actual files.
>
> **✓ DRIFT RESOLVED (paper §8 ↔ propagation edit-text).** Both documents now
> state the precise **five-way** Lean granularity verbatim: positivity all-d /
> factorization d=2–5 / **exhaustive root-set {0,R} classification at degree 2** /
> **no-negative-root content at degrees 2–3** / γ-arithmetic at instances d=2,3,5.
> The earlier, looser phrasings (which collapsed the root-set coverage into a
> single degree range) are superseded: the exhaustive root-set classification
> (`L2_root_imp`) is machine-checked at d=2 ONLY; only the no-negative-root content
> extends to d=3.
>
> **Sha convention.** "sha" below is the **sha256 of the script/lean file** (the
> task-listed identifiers). The `_results.json` files additionally embed a
> `canonical_sha256_of_hashfree_object` (the hash of the run-insensitive result
> object) — a DIFFERENT, complementary identifier. Both are legitimate; do not
> conflate them (e.g. amplitude_F_scope: file sha `1c89aa01`, results-canonical
> `cc610bfa`).

## Lemma → artifact → grade

| Paper component | Artifact (script) | file sha256 (short) | Grade |
|---|---|---|---|
| (i) Location: positivity lift, Q_n>0, radius R=d^d/β_d, all positive-b d | `positivity_lift_general_d.py` | `ed833f11` | PROVEN (positive-b, symbolic+verified-d6) |
| (i) Location: single-valued cover / other-sheet clearance d=2 | `bridge2_othersheet_d2.py` | `28105561` | PROVEN (d=2 unconditional; general-d by same cover) |
| (i)+(ii): exact order-2d ODE, leading coeff a_{2d}(s)=d^d s^{2d}(d^d−β_d s), roots {0,R}, |s|=R uniqueness | `transfer_hypothesis.py` | `3e84f22d` | PROVEN (exact symbolic; verified d=2..6) — the airtight core |
| (ii) Type/exponent law γ=(d+1)/2+b_{d−1}/β_d, general d | `physical_type_general_d.py` | `d50d3f54` | PROVEN (symbolic+verified-d6) |
| (ii)/(iii) d=2 physical type instance (BRANCH-N, γ=11/6) | `physical_type_d2.py` | `fa0574e2` | PROVEN (d=2) |
| (F) Amplitude scope: F-CLOSED-BY-SCOPING (no deposit needs physical-G amplitude) | `amplitude_F_scope.py` | `1c89aa01` | CLOSED-BY-SCOPING |
| Lean uplift (machine-checked algebraic layer, clean axiom cone) | `lean/EBR_uplift.lean` | `7acb1a58` | see Lean granularity below |
| AEAL ledger (all claims, methods, verdicts) | `claims_sectorial.jsonl` | (see manifest) | — |

## Lean machine-checked granularity (five-way — state ALL five, do not collapse)

The Lean file `EBR_uplift.lean` (clean axiom cone `[propext, Classical.choice,
Quot.sound]`, zero sorry, zero project axioms) machine-checks, at the stated scope:

1. **Positivity — ALL degrees** (`Qval_pos`, degree-independent).
2. **Leading-coeff factorization a_{2d}=d^d s^{2d}(d^d−βs) — d = 2,3,4,5**
   (`L2/L3/L4/L5_factor`).
3. **Exhaustive root-set {0,R} classification — d = 2 ONLY** (`L2_root_imp`:
   L=0 ⟹ s∈{0,R}; with `L2_zero_root`, `L2_R_root`). No `L3/L4/L5_root_imp`.
4. **No-negative-real-root (Corollary 4.2 content) — d = 2,3** (`L2_no_neg_root`
   even; `L3_no_neg_root` odd).
5. **γ arithmetic — instances d = 2,3,5** (`gamma_d2_vquad=11/6` branch;
   `gamma_d3_pole=2`, `gamma_d5_pole=3` poles; branch/pole split).

**NOT machine-checked (characterized, NOT axiomatized):** the symbolic-ALL-d steps
(a_{2d} form / γ-law quantified over d — variable exponent `d^d s^{2d}` is not a
Lean polynomial); that L_d IS the ODE leading coefficient (the Weyl/Stirling
derivation, referenced from `transfer_hypothesis.py`); the analytic bridges
(Pringsheim, D-finite localization — absent from Mathlib, supplied as explicit
hypotheses, not axioms).

## Overall grade (must appear in the public Zenodo description)

**EBR (positive-b) PROVEN for all positive-b degrees**, the general-d steps resting
on EXACT SYMBOLIC arguments with exact/numeric verification to degree 6 and a
Lean-machine-checked algebraic layer (granularity above); **NOT a
symbolic-degree-quantified formal proof**. Load-bearing qualifiers (drop none):
positive-b; PHYSICAL generating-function object (not the WKB fluctuation, scale
2ξ₀); amplitude SCOPED OUT; character is a branch/pole SPLIT on the integer-γ
subvariety.
