# EBR-IV reproducibility package

This directory reproduces and verifies every load-bearing computation behind the
paper *The EBR connection coefficient on the Painlevé III(D₈) surface: a
constructive exponential period and a conditional transcendence theorem*
(`paper/ebr4_v0.tex`).

Everything here is **untracked, uncommitted, and unminted**. Nothing in this
package commits, pushes, tags, or deposits anything; see
`../draft/OPERATOR_RUNBOOK_ebr4.md` for the operator-gated steps.

The companion EBR-III package (`../repro/`, 45 claims, frozen) is **separate and
not modified**. The 169-digit connection coefficient `C_EBR` and the elementary
Γ-quotient null (`EBR3-B-*`) live there and are **cited, not recomputed** here.

---

## One-command verification

From this directory:

```sh
python verify.py
```

Exit code `0` ⇔ every check passes. `verify.py` (the same recipe-aware tool
audited for EBR-III) performs two audits:

1. **Embedded self-hash consistency** — for each `results/*.json`, it recomputes
   the canonical SHA-256 of the hash-free object and confirms it equals the hash
   the script itself stored (`canonical_sha256_of_hashfree_object`). This proves
   each frozen artifact is internally consistent.
2. **File SHA-256 vs `HASH_MANIFEST.json`** — every script, report, the paper
   `.tex`/`.pdf`, and the ledger snapshot is hashed and checked against the
   manifest.

To regenerate the manifest after an intentional change:

```sh
python verify.py --write
```

Unlike the heterogeneous EBR-III corpus, **all 14 EBR-IV results JSONs use one
convention** — key `canonical_sha256_of_hashfree_object`, default separators, no
trailing newline, strip only the hash key (recipe
`default-seps/no-nl/strip-hashkey`). `verify.py` reports the matched recipe per
file for auditability.

All scripts call `sys.stdout.reconfigure(encoding="utf-8")` (Windows console
cp1252 cannot print √ / κ / π / −). Numeric scripts use `mpmath` and `sympy`;
install with `pip install mpmath sympy`. **mpmath precision hazard:** every
script sets `mp.dps` *before* any module-level `mpf(...)` (a context set inside
`main()` silently caps module-level constants at 15 digits — a named hazard in
this corpus).

---

## The three independent κ channels

The constant κ = 1.539494848576641… is computed by **three channels with
disjoint inputs**; their agreement is the cross-check, not a single pipeline.

| channel | script | input | precision |
|---------|--------|-------|-----------|
| **A** — large-order asymptotics | `scripts/cc3_2s2_1_resurgence.py` | the integer sequence Qₙ only (Nmax=60000), κ = Γ(4/3)·A₀, A₀ = lim Qₙ/((n!)²3ⁿn^{1/3}) | ~60 digits |
| **B** — frozen composition | `scripts/cc3_2s2_1_resurgence.py` | the 169-digit `C_EBR` (cited from EBR-III), κ = Γ(4/3)·C_EBR/√π | ~129 digits |
| **C** — monodromy spectral projector | `scripts/cc3_s6_1_period_matrix.py` | analytic continuation of Φ over 3 loops, projector P_μ=(M−I)³/(μ−1)³, μ=e^{−2πi/3} | 129 digits |

Channels A and C take **no** input from the frozen `C_EBR`; channel B is the
only one that does. Re-running any script regenerates its results JSON; `python
verify.py` then confirms the embedded self-hash is unchanged.

---

## Per-artifact reproduction

| run | reproduces | what it establishes |
|-----|-----------|---------------------|
| `python scripts/cc3_2_1_h2_classify.py` | `cc3_2_1_h2_classify_results.json` | the rank-2 core H₂; {0,∞} both irregular slope ½; **G_Gal(H₂)=SL₂** (exact Kovacic, ℚ(√3)-emptiness), non-Liouvillian |
| `python scripts/cc3_2s2_0_rigidity_ruleS.py` | `cc3_2s2_0_rigidity_ruleS_results.json` | rig(H₂)=0 (non-rigid, moduli dim 2); **RULE S ⇒ PIII(D₈)=D₈⁽¹⁾**; Padé z=1/3 to ~34 d |
| `python scripts/cc3_2s2_1_resurgence.py` | `cc3_2s2_1_resurgence_results.json` | **κ = Γ(4/3)·A₀ exact** (Flajolet–Sedgewick transfer); κ channels A (~60 d) and B (~129 d); corrections pure 1/n |
| `python scripts/cc3_2s2_2a_monodromy.py` | `cc3_2s2_2a_monodromy_results.json` | the monodromy point: **tr M₀ = −51.0655631399546…** (hyperbolic ⇒ irreducible, off reducibility locus) |
| `python scripts/cc3_2s2_2b_dictionary.py` | `cc3_2s2_2b_dictionary_results.json` | gauge dictionary H₂ → companion B (D₈ shape, symmetric DCHE); κ = s*(B;x=0)×Γ-factor, Lax-side |
| `python scripts/cc3_2s2_2c_coverage.py` | `cc3_2s2_2c_coverage_results.json` | coverage verdict **(iii) NOT COVERED** (tau-side vs Lax-side); ILP/GL compute tau-side, κ is input |
| `python scripts/cc3_2s2_3_barnes_battery.py` | `cc3_2s2_3_barnes_battery_results.json` | Barnes–Glaisher log-space null (ALL-NULL, H≤10¹², 150 d); positive control G(1/2) fires |
| `python scripts/cc3_s6_1_period_matrix.py` | `cc3_s6_1_period_matrix_results.json` | the order-4 operator L (slope-¼ ∞ ⇒ exp periods); κ channel C **A_Φ=κ to 129 d** (spectral projector) |
| `python scripts/cc3_s6_2_bridge.py` | `cc3_s6_2_bridge_results.json` | the **κ-bridge** s*=A_Φ=κ=Γ(4/3)A₀ (S6 STRUCTURAL): κ a constructive exponential period |
| `python scripts/cc3_3_1_locus.py` | `cc3_3_1_locus_results.json` | off the classical PIII(D₈) locus: SL₂ irreducible (R); tr M₀ not algebraic deg≤8 + infinite order (A) |
| `python scripts/cc3_3_2_conditional_theorem.py` | `cc3_3_2_conditional_theorem_results.json` | the conditional theorem κ∉ℚ̄ under H1–H4; the gap list G1–G5 |
| `python scripts/cc3_3_3_closeout.py` | `cc3_3_3_closeout_results.json` | the program four-class table and readiness inventory |
| `python scripts/ebr4_0_hypothesis_audit.py` | `ebr4_0_hypothesis_audit_results.json` | **H2⊥H3 verdict (iii)**, no collapse (honest count 4); the verbatim re-graded theorem; drop-one backbone |
| `python scripts/ebr4_1_locus_hardening.py` | `ebr4_1_locus_hardening_results.json` | **direct locus hardening** (stratum A deg≤4 @H≤10¹⁰); G5 hardened, G3 tightened; the null-discipline catch |

---

## Paper PDF (byte-reproducible)

```sh
# with MiKTeX pdflatex on PATH:
SOURCE_DATE_EPOCH=1718150400 pdflatex -interaction=nonstopmode paper/ebr4_v0.tex
SOURCE_DATE_EPOCH=1718150400 pdflatex -interaction=nonstopmode paper/ebr4_v0.tex
```

The preamble omits embedded timestamps (`\pdfinfoomitdate=1`,
`\pdftrailerid{}`, `\pdfsuppressptexinfo=-1`) and fixes the trailer `/ID`, so the
PDF byte-hash is stable across builds and across build directories (verified: 3
in-place builds + 1 pristine-temp-dir build, all identical). Two passes resolve
cross-references; there is no BibTeX step (`thebibliography` is inline).

---

## Frozen content hashes (pinned in the paper)

| artifact | SHA-256 |
|----------|---------|
| κ channel C — period matrix `results/cc3_s6_1_period_matrix_results.json` | `56adcb100d841756d24babb9017bbbb718887a6fc48d301ac45ba1594b3e7fb4` |
| κ channels A/B — resurgence `results/cc3_2s2_1_resurgence_results.json` | `8f52843c2e389609c932d25a76b79cfcc422782fc31a0c87392edeb1e8c653f9` |
| κ-bridge `results/cc3_s6_2_bridge_results.json` | `2cc2f6fb8f0c710496d021a321f710f8a15753f66bbeaf2e1d321beb5a73d9d3` |
| conditional theorem `results/cc3_3_2_conditional_theorem_results.json` | `1b15e7ac9a503c30e1cdae8a736677b401c2f1d8c815a2e02a2e0f18908fbfdd` |
| hypothesis audit `results/ebr4_0_hypothesis_audit_results.json` | `d86256cc460e0a45b3c67e2a43b101bcd84402609c06bf1e2c2ecc239156bc87` |
| locus hardening `results/ebr4_1_locus_hardening_results.json` | `dae56db4215caf40bd5edde4e976280206a295bab142cd056d73f6c7d0d948da` |
| claims-ledger snapshot `claims_cc.jsonl` (92 claims) | `a168f2f791883fc6aaf7144154c6436d852cbed7cad405e039930f682680297f` |
| paper `paper/ebr4_v0.pdf` | `afa69197ce7b53003c561ca717dd6365ac021e869c9f692ce1c293e07c22382b` |

The full per-file manifest is `HASH_MANIFEST.json`.

---

## What is NOT here (cited, frozen in EBR-III)

- The 169-digit `C_EBR` (`../repro/results/cc4_1_connection_results.json`,
  `f3400831…`) and the elementary Γ-quotient / constant / algebraic null
  (`../repro/results/ebr3_b_pslq_results.json`, `9a3f942d…`). κ channel B
  consumes `C_EBR` as a fixed input.
- The four PROVEN Lean cores (`../repro/lean/cc4_cores/`). **EBR-IV adds no
  machine-checked core**; its finitary identities are flagged as Lean-core
  candidates in the paper's open-problems section.

---

## Contents

```
verify.py             one-command verifier (recipe-aware; inherited from EBR-III)
HASH_MANIFEST.json    canonical hash manifest (all files + embedded self-hashes)
claims_cc.jsonl       AEAL ledger snapshot (92 claims)
scripts/              14 reproducer scripts (cc3-2 … ebr4-1)
results/              14 results JSONs (each self-hashed)
reports/              4 stage reports (cc3-2a/2b/2c + cc3-final)
paper/                ebr4_v0.tex + byte-reproducible ebr4_v0.pdf
```
