# Canonical Basis Constants — `basis_canonical.json`

**This file is the SOLE source of truth that basis runs may read constants from.**
The R1, V_quad-S, and M10 threads are GATED on it: a constant may be used by a
basis run **only if its `status` is `VERIFIED`** in `basis_canonical.json`.

## Discipline

Every value in `basis_canonical.json` was **recomputed from its definition** by
`recompute_basis.py` — from mpmath first principles (standard constants) or from
the defining PCF family / formula / recurrence (project constants). **No value was
transcribed** from a deposit abstract, a prior run, or memory. A transcribed
decimal is treated as untrusted until a from-definition recompute confirms it.

## The could-not-confirm rule (applied to numbers)

Any constant whose status is **not `VERIFIED` is BARRED from basis use**:

| status        | meaning                                                            | usable |
|---------------|--------------------------------------------------------------------|--------|
| `VERIFIED`    | recompute matches the latest deposited value                       | ✅ yes |
| `STALE-MATCH` | recompute matches a superseded/retracted value, not claimed latest | ❌ barred — surface |
| `DISCREPANCY` | recompute matches neither deposited version                        | ❌ barred — surface |
| `UNRESOLVED`  | value could not be recomputed from a findable definition           | ❌ barred — surface |

`STALE-MATCH`, `DISCREPANCY`, and `UNRESOLVED` are **stop-and-surface** events:
they signal a provenance defect that the operator must resolve before the value is
used. They are never averaged or auto-resolved.

## This pass

VERIFIED (usable): `pi`, `e`, `log2`, `gamma`, `zeta(3)`, `Catalan G`, `zeta(2)`,
`R1`, `V_quad`, **`S`**.

**`S` (V_quad Stokes constant) — VERIFIED via prefactor identification.**
The discrepancy was the Dingle **prefactor**. The from-definition recompute factors
the late-term amplitude `K = lim|aₙ·ξ₀^{n+β}/((−1)ⁿΓ(n+β))|` (cross-stable to ~84
digits) and applies an explicit prefactor:

- prefactor `Γ(β_exp) = −6.00599` (v1.0, **retracted**) → `S = 0.43770528619…`
  (reproduces the value still hardcoded in the repo scripts and v1.0/P12 deposits);
- prefactor `2π = 6.28319` (v1.1, **corrected**) → `S = 0.4579066231690176361190978…`
  (reproduces the Painlevé-V paper v1.1 value `0.45790662316901763611` to all 20
  deposited digits, stable to ~46 digits).

The two prefactors differ by `2π/|Γ(β_exp)| = 1.04615` (~4.4%), which camouflaged the
v1.0 error. The canonical `S` is recorded under the **2π convention** (v1.1) and
`supersedes` the retracted `0.43770528`.

⚠️ **Repo scripts are STALE:** `pcf-research/vquad/scripts/*` (t2_iter20/22/23/24,
jimbo_final) still carry the retracted `Γ(β_exp)` prefactor and hardcode
`S=0.43770528`. They need the `2π` fix (flagged in the `FLAG_repo_scripts_stale`
block on the `S` entry; **not** modified here — report-and-stop).

## Reproduce

```
python pslq/constants/recompute_basis.py   # recompute all values -> _basis_recompute_raw.json
python pslq/constants/build_canonical.py    # assemble -> basis_canonical.json
```
