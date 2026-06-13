# EBR-III reproducibility package

This directory reproduces and verifies every load-bearing computation behind
the paper *The EBR operator at d=2 is not a G-operator and its differential
Galois group is SL(4)* (`paper/ebr3_v1.tex`).

Everything here is **untracked, uncommitted, and unminted**. Nothing in this
package commits, pushes, tags, or deposits anything; see
`../draft/OPERATOR_RUNBOOK.md` for the operator-gated steps.

---

## One-command verification

From this directory:

```sh
python verify.py
```

Exit code `0` ⇔ every check passes. `verify.py` performs two audits:

1. **Embedded self-hash consistency** — for each `results/*.json`, it recomputes
   the canonical SHA-256 of the hash-free object and confirms it equals the hash
   the script itself stored. This proves each frozen artifact is internally
   consistent.
2. **File SHA-256 vs `HASH_MANIFEST.json`** — every script, report, Lean source,
   the paper `.tex`/`.pdf`, and the ledger snapshot is hashed and checked against
   the manifest.

To regenerate the manifest after an intentional change:

```sh
python verify.py --write
```

### Heterogeneous hash conventions (why `verify.py` tries recipes)

The corpus was produced over several sessions and is **not** uniform in how it
canonicalizes JSON before hashing:

* `cc1_L2_structure.py` (the earliest artifact) uses **compact separators**
  `(",", ":")`, appends a **trailing newline**, and excludes a set of
  run-sensitive keys (`timestamp`, `cwd`, paths, …) in addition to the hash key.
* The nine later artifacts (`cc2_*`, `cc4_*`, `ebr3_b`) use **default
  separators** `(", ", ": ")`, **no trailing newline**, and strip only the hash
  key.

The embedded-hash key name also varies: most use
`canonical_sha256_of_hashfree_object`; `cc2_2d` uses `canonical_sha256`;
`cc2_1_twisted_exponent_table` uses `sha256`.

`verify.py` knows both recipes, tries each, and prints which one reproduced each
embedded hash. A run reports, e.g.,
`PASS cc1_... (compact-seps/nl/strip-run-sensitive)` and
`PASS ebr3_b_... (default-seps/no-nl/strip-hashkey)`.

---

## Per-artifact reproduction

### Symbolic / numeric scripts

Each script regenerates its `results/<name>_results.json`. Re-running then
`python verify.py` confirms the embedded self-hash is unchanged.

| run | reproduces | what it establishes |
|-----|-----------|---------------------|
| `python scripts/cc1_L2_structure.py` | `cc1_L2_structure_results.json` | explicit order-4 operator `L_2`, singular set `{0, 4/3, ∞}`, irregular-∞ slope 1/4, exponents |
| `python scripts/cc2_0_arithmetic_gate.py` | `cc2_0_arithmetic_gate_results.json` | not-a-G-function (denominator growth / p-curvature / Katz trichotomy), normalization-scoped |
| `python scripts/cc2_1_2.py` | `cc2_1_2_results.json`, `cc2_1_twisted_exponent_table.json` | twist data `W`, `χ`; Λ²/Sym² rational-solution nulls; twisted exponent table |
| `python scripts/cc2_2d_numerical_monodromy.py` | `cc2_2d_numerical_results.json` | `M_0`, `M_R` semisimple data (audit-corrected) |
| `python scripts/cc4_0_descent.py` | `cc4_0_descent_results.json` | descent/induction NULL ⇒ primitivity (η=√s unique, 4-cycle index-2 closure, both routes agree) |
| `python scripts/cc4_0b_bounds.py` | `cc4_0b_bounds_results.json` | a priori degree bounds `B_2=3`, `B_1=7 ≤ 20` ⇒ the SL₄ theorem is bound-complete |
| `python scripts/cc4_1_connection.py` | `cc4_1_connection_results.json` | connection coefficient to 169 digits (third independent channel) |
| `python scripts/cc4_1_stokes.py` | `cc4_1_stokes_results.json` | Stokes sector layout for slope 1/4 (multipliers out of scope) |
| `python scripts/ebr3_b_pslq.py` | `ebr3_b_pslq_results.json` | integer-relation battery, **ALL-NULL at 169 digits**, positive controls fire |

All scripts call `sys.stdout.reconfigure(encoding="utf-8")` (Windows console
cp1252 cannot print √ / δ / π / −). Numeric scripts use `mpmath`; install with
`pip install mpmath`.

### Lean cores (the only PROVEN items)

```sh
cd lean/cc4_cores
lake build
```

Then inspect `AXIOM_AUDIT.txt`: every declaration's axiom cone must be a subset
of `{propext, Classical.choice, Quot.sound}` with **no** `sorryAx`. Toolchain is
pinned in `lean-toolchain` (`leanprover/lean4:v4.30.0`) and `lake-manifest.json`
(Mathlib rev `c5ea0035`). The `.lake/` build outputs (oleans) are intentionally
**excluded**; `lake build` regenerates them.

### Paper PDF (byte-reproducible)

```sh
# with MiKTeX pdflatex on PATH:
SOURCE_DATE_EPOCH=1718150400 pdflatex -interaction=nonstopmode ebr3_v1.tex
SOURCE_DATE_EPOCH=1718150400 pdflatex -interaction=nonstopmode ebr3_v1.tex
```

The preamble omits embedded timestamps and fixes the trailer `/ID`, so the PDF
byte-hash is stable across builds. Two passes resolve cross-references; there is
no BibTeX step (`thebibliography` is inline). Expected SHA-256 is recorded under
`paper/ebr3_v1.pdf` in `HASH_MANIFEST.json`.

---

## Frozen content hashes (pinned in the paper)

| artifact | SHA-256 |
|----------|---------|
| integer-relation null `results/ebr3_b_pslq_results.json` | `9a3f942def64737dd0bfc00495077f99ea7fe1ae5110982e343d8e12d5f7bcaf` |
| connection coefficient `results/cc4_1_connection_results.json` | `f3400831cc9644641e44de7bcb69e4ec9c8fc69654ab46eb9768067ac2aa13fd` |
| claims-ledger snapshot `claims_cc.jsonl` | `9e6f3fa5a2986cce8edddaad5945e9da4008ea637c1b5c6d5b1fa9691362f6bb` |
| paper `paper/ebr3_v1.pdf` | `32e6f216da6c18daeb6eb7159ec68bc046c366defe33b89a8ab1fb6af8e445f1` |

The full per-file manifest is `HASH_MANIFEST.json`.

---

## Contents

```
verify.py             one-command verifier (recipe-aware)
HASH_MANIFEST.json    canonical hash manifest (all files + embedded self-hashes)
claims_cc.jsonl       AEAL ledger snapshot (45 claims)
scripts/              9 reproducer scripts
results/              10 results JSONs (each self-hashed)
reports/              6 stage reports + the cc-narration erratum
lean/cc4_cores/       Lean 4 project (4 cores / 9 PROVEN decls + AXIOM_AUDIT.txt)
paper/                ebr3_v1.tex + byte-reproducible ebr3_v1.pdf
```
