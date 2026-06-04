# Lemma 3.1, general d — in-repo derivation of the slope-1/d Newton edge polynomial

*Deposit note (`pslq/xi0_d3/`). Extends the in-repo d=3 method
(`xi0_d3_scale_test.py :: derive_chi3_symbolic`) to general d, to discharge the
**algebraic** half of the conditionality behind the M9.1⁺ all-d covariance lift.
Forbidden-verb hygiene applied: "PROVEN in-repo for all d≥2" is claimed ONLY for the
algebraic edge polynomial + covariance algebra (carried by the symbolic-in-d
leading-symbol lemma, §2.B), NOT for the analytic Borel-radius step, which stays
cited-conditional. "VERIFIED" is restricted to the actually-computed (d, β_d).*

## 0. Goal and one-line verdict
The all-d lift **M9.1⁺** (`ξ₀(b∘φ)=α⁻¹ξ₀(b)` for `φ(n)=αn+γ`, all d≥2) was previously
*conditional on D2-NOTE Theorem 4.1 / Lemma 3.1*, which are deposit-only
(DOI 10.5281/zenodo.19996689). This note discharges the **algebraic** half of that
conditionality **in-repo** by extending the in-repo d=3 operator method to general d.

> **Verdict.** The **algebraic edge-polynomial fact** (Lemma 3.1's algebra:
> `χ_d(c)=1+(−1)^{d+1}(β_d/d^d)c^d`, only `β_d` on the slope-1/d edge) is **PROVEN
> in-repo for all d≥2** via a symbolic-in-d leading-symbol induction (§2.B), with
> full-operator instance verification for d=2..6 (§2.A). The **covariance law** follows
> from the edge alone, derived in-repo symbolically with **no appeal to D2-NOTE** (§2.C).
> What **remains cited-conditional** is only the **analytic implication** "this edge
> polynomial ⇒ Borel radius `|c|=d/β_d^{1/d}`" — the Wasow §19 / Birkhoff–Trjitzinsky
> content D2-NOTE Thm 4.1 invokes — **not re-derived** here, only numerically
> corroborated for d=2..6 (§2.D).

Reproduce: `python pslq/xi0_d3/lemma31_edge_derivation.py`
(raw: `lemma31_edge_derivation_raw_output.txt`; JSON
`lemma31_edge_derivation_results.json`, sha256
`d0738b5d8a9488667c9b1a18754fa6438098945c5e1b6d4ab5d75469d45e9897`; `ALL_GREEN=True`).

## 0a. Relationship to the deposited M9 writeup (cross-reference, NOT an edit)
This is a **separate companion note**. It does **not** modify the deposited M9 program
statement `pslq/m9_bridge/M9_bridge_stratification.md` (deposited at commit `914c518`),
which remains byte-untouched. It is a **forward reference** that narrows the
conditionality recorded there.

The deposited writeup grounds **Proposition M9.1** (`ξ₀(b∘φ)=α⁻¹ξ₀(b)`) on the in-repo
β_d-only slope-1/d edge fact at d=3 and numerically VERIFIES it at d∈{2,3,4}; the all-d
extension **M9.1⁺** was stated conditional on D2-NOTE Thm 4.1 (deposit-only). This note
supplies the **§4 restatement** to be read alongside that deposit:

> **§4 restatement (M9.1⁺, after this companion note).** The **algebraic core** of M9.1⁺
> — the slope-1/d edge `χ_d(c)=1+(−1)^{d+1}(β_d/d^d)c^d` (only β_d), and the resulting
> covariance `ξ₀(b∘φ)=α⁻¹ξ₀(b)` — is **PROVEN in-repo for all d≥2**, carried by the
> **symbolic-in-d leading-symbol lemma** (§2.B; *not* by the d≤6 numerics, which only
> corroborate). The **analytic edge⇒Borel-radius step** (`ξ₀=|c|=d/β_d^{1/d}`; Wasow §19
> sectorial existence at rank q=(d+2)/2, Birkhoff–Trjitzinsky Borel-summability) **remains
> cited-conditional** on D2-NOTE Thm 4.1 — it is **not** discharged here. "VERIFIED" stays
> restricted to the computed (d, β_d, φ); no d≥7 claim.

## 1. The in-repo d=3 method (extended, not forked)
`xi0_d3_scale_test.py :: derive_chi3_symbolic` forms χ₃ by **direct operator action**:
Euler operator `θ=(u/3)d/du` (`=z d/dz`, `z=u³`), `D:=θ+1`, WKB ansatz `f=exp(c/u)`,
operator `L=1−z·b(θ+1)−z²` (the recurrence `Q_n=b(n)Q_{n-1}+Q_{n-2}` in operator form),
and **χ₃(c) = `[u⁰]`(Lf/f)** — the slope-1/3 edge balance. The d=3 code asserts
`χ₃=1+(β₃/27)c³` and `chi3_only_beta3_on_edge=True`. `lemma31_edge_derivation.py` reuses
this exact construction with `d` generalized, and reuses the **same ξ₀ pipeline**
(`pslq/m9_bridge/m9_1_covariance_check.py`, which imports `neville_zero` from this
directory) for the numeric leg.

## 2. The general-d derivation (four parts, all reproduced)

### A. Full operator χ_d for d=2..6 (instance-verified, full operator)
`derive_chid_symbolic(d)` (the d=3 construction generalized: `θ=(u/d)d/du`,
`b(θ+1)=Σ_{k=0}^d β_k D^k`, `L=1−u^d·g−u^{2d}`, χ_d=`[u⁰]`):

| d | χ_d(c) derived | only β_d on edge | matches `1+(−1)^{d+1}(β_d/d^d)c^d` |
|---|---|---|---|
| 2 | `1 − β₂c²/4`        | ✓ | ✓ |
| 3 | `1 + β₃c³/27`       | ✓ | ✓ |
| 4 | `1 − β₄c⁴/256`      | ✓ | ✓ |
| 5 | `1 + β₅c⁵/3125`     | ✓ | ✓ |
| 6 | `1 − β₆c⁶/46656`    | ✓ | ✓ |

In every case `β_{d−1..0}` are **absent** from the edge — the load-bearing β_d-only fact.

### B. Symbolic-in-d leading-symbol lemma (the general-d backbone)
Put `w=1/u`; then `θ=−(w/d)d/dw`, `f=exp(cw)`, so `θ[g·f]/f=−(w/d)(g′+c·g)`. Hence
`θ^k f/f=P_k(w)` with `P_{k+1}=−(w/d)(P_k′+c·P_k)`, `P_0=1`.

**Lemma (symbolic in d).** `P_k` is a degree-`k` polynomial in `w` with leading
coefficient `(−c/d)^k`.
*Proof (induction).* `P_0=1`; the highest term of `P_{k+1}=−(w/d)(P_k′+cP_k)` is
`−(w/d)·c·(−c/d)^k w^k=(−c/d)^{k+1}w^{k+1}`. ∎

`leading_symbol_lemma` verifies this **for k=0..8 with `d` kept a free symbol** (all
leading coeffs `(−c/d)^k`, degree `k`). Therefore in `b(θ+1)f/f=Σ_k β_k P_k(1/u)` the
top inverse power is `u^{−d}` with coefficient `β_d(−c/d)^d`; `×z=u^d`, take `[u⁰]`:
```
χ_d(c) = 1 − β_d(−c/d)^d = 1 + (−1)^{d+1}(β_d/d^d)c^d,   only β_d on the edge,  ALL d.
```
This is a **symbolic-in-d** derivation, not a finite set of instances.

### C. Covariance from the edge alone (symbolic, no D2-NOTE)
`symbolic_covariance(d)` confirms for d=2..6: `b(αn+γ)` has degree `d` and **leading
coefficient `β_d·α^d`** (γ in lower-order terms only). χ_d depends only on `(d,β_d)`, so
the root modulus `d/β_d^{1/d}` maps to `d/(β_dα^d)^{1/d}=α⁻¹·d/β_d^{1/d}` (positive real
d-th root, `α,β_d>0`): `ratio=1/α`, **γ-free**. This reproduces **M9.1⁺ from the in-repo
edge derivation alone**.

### D. Numeric cross-check vs the trusted in-repo pipeline (d=2..6)
The symbolic edge predicts `ξ₀=d/β_d^{1/d}`; the in-repo pipeline measures ξ₀ from `Q_n`
(Neville, dps=160). Ten families, β_d∈{1,2,3,7}, agreement **40.1–45.7 digits**:

| family | d | β_d | ξ₀ edge | pipeline ξ₀ | digits |
|---|---|---|---|---|---|
| d2_b3 | 2 | 3 | 1.15470053838 | 1.15470053838 | 42.7 |
| d2_b1 | 2 | 1 | 2.0 | 2.0 | 40.1 |
| d3_b2 | 3 | 2 | 2.38110157795 | 2.38110157795 | 42.6 |
| d3_b1 | 3 | 1 | 3.0 | 3.0 | 41.5 |
| d4_b1 | 4 | 1 | 4.0 | 4.0 | 42.4 |
| d4_b7 | 4 | 7 | 2.45915261181 | 2.45915261181 | 45.7 |
| d5_b1 | 5 | 1 | 5.0 | 5.0 | 43.4 |
| d5_b2 | 5 | 2 | 4.35275281648 | 4.35275281648 | 44.1 |
| d6_b1 | 6 | 1 | 6.0 | 6.0 | 44.0 |
| d6_b3 | 6 | 3 | 4.99609906593 | 4.99609906593 | 44.8 |

This **corroborates** the analytic edge⇒radius implication for d=2..6 (does not prove it).

## 3. Honest scope — algebraic vs analytic
- **Algebraic edge polynomial (Lemma 3.1's algebra): PROVEN in-repo for all d≥2.**
  §2.B is a general-d induction (verified symbolically, d free); §2.A instance-verifies
  the full operator d=2..6. No D2-NOTE dependence.
- **Covariance law: derived in-repo (symbolic, §2.C)** — `1/α` ratio and γ-independence.
- **Analytic edge⇒radius step: RESIDUAL, cited-conditional.** "Slope-1/d edge ⇒ Borel
  singularity at `|c|=d/β_d^{1/d}`" is Wasow §19 sectorial existence (rank `q=(d+2)/2`,
  §19.3 half-integer for odd d) + Birkhoff–Trjitzinsky Borel-summability, cited by
  D2-NOTE Thm 4.1. **NOT** re-derived here (analysis, not elementary algebra); only
  numerically corroborated d=2..6 (§2.D).
- **Parity / half-integer rank.** The sign `(−1)^{d+1}` only flips which real root is
  picked; ξ₀ is the **modulus** `d/β_d^{1/d}` (parity-blind), and §2.C uses only the
  positive real d-th root. Verified across even (2,4,6) and odd (3,5) d.

Net: the conditionality of M9.1⁺ **shrinks** from "all of D2-NOTE Thm 4.1 + Lemma 3.1"
to **"only the analytic Borel-radius implication (Wasow §19 / B–T)."**

## 4. Could-not-confirm (required)
- The **analytic** edge⇒radius implication is not re-derived in-repo (genuine analytic
  content; only corroborated numerically d=2..6).
- §2.B checks the induction for k=0..8 (d symbolic); the general-k step is the hand proof
  of §2.B, not a machine-closed induction.
- No d≥7 evidence; d=2..6 is the computed range. The all-d support is the symbolic-in-d
  lemma (B), not the d≤6 instances.
