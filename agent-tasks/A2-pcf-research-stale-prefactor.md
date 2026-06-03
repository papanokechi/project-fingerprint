# TO-DO A2 (external, by-hand): pcf-research vquad scripts carry the RETRACTED S prefactor

> Not a Fingerprint task — a **provenance defect in deposited work**, surfaced by the
> basis re-verification pass. Recorded here as a real to-do; the fix is a separate,
> deliberate, by-hand action on the **`pcf-research`** repo, NOT folded into any
> Fingerprint commit.

## The defect

The basis re-verification recompute (factor late-term amplitude K once, apply the
Dingle prefactor explicitly) showed:

| convention | prefactor | S |
|---|---|---|
| v1.0 **RETRACTED** | `Γ(β_exp) = −6.00599` | `0.43770528619…` |
| v1.1 **CORRECT** | `2π = 6.28319` | `0.4579066231690176361190978…` |

Ratio `2π/|Γ(β_exp)| = 1.04615` (~4.4%) — the exact camouflage the Painlevé-V v1.1
correction named.

These scripts in `pcf-research/vquad/scripts/` still hardcode `S = 0.43770528` with
the retracted `Γ(β_exp)` prefactor:

- `t2_iter20_stokes_constant_v2.py`
- `t2_iter22_s_precision.py`
- `t2_iter23_jimbo.py`
- `t2_iter24_sigma_conn.py`
- `jimbo_final.py`

**Anyone running these "reproducibility" scripts gets the value the authors' own v1.1
explicitly retracted.** The paper is correct; the deposited code is stale.

## Two options (operator's call — do NOT auto-pick)

1. **Fix the scripts.** Replace the `Γ(β_exp)` prefactor with `2π`, update the
   hardcoded `0.43770528 → 0.45790662316901763611`, and commit with a message
   pointing at the v1.1 correction so the history records *why*. Caveat: these are
   artifacts tied to a specific Zenodo deposit — changing them needs deliberate
   versioning, not a silent overwrite.

2. **Lighter touch:** add a `KNOWN_ISSUE` note in the `pcf-research` repo directing
   reproducers to the corrected `2π` prefactor and the v1.1 value, leaving the
   deposited scripts intact.

## Verification reference (from Fingerprint)

- Correct S, recomputed from definition: `0.4579066231690176361190978425482258379624`
  (2π convention; 46 stable digits) — see
  `project-fingerprint/pslq/constants/basis_canonical.json` (entry `S`,
  `status=VERIFIED`) and `recompute_basis.py::recompute_S` (prefactor-explicit).

## Status

OPEN. External to `pcf-research`. Not blocking any Fingerprint thread (Fingerprint
reads S from its own canonical file, not from these scripts).
