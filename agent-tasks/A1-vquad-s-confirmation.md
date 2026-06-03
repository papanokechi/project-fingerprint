# TASK A1: V_quad–S confirmation run — reproduce the paper's documented null

> Filled-in instance of `agent-tasks/TEMPLATE.md`. Opens **Thread A**, gated until
> now on the Stokes constant `S` being VERIFIED. That gate is **CLEARED**: the basis
> re-verification pass recomputed `S` from definition and recorded it VERIFIED under
> the 2π Dingle convention in `pslq/constants/basis_canonical.json`.
>
> This is a **CONFIRMATION** run, not a discovery run. The Painlevé-V paper documents
> a **null** (no clean integer relation across its stated variant sweep against a
> Gamma/period basis). The job is to reproduce that null with the freshly-VERIFIED
> constants — does our harness, fed the canonical S and V_quad, reproduce the paper's
> documented "no-relation" outcome across the same variant set? A reproduced null is
> the wanted result.
>
> All standard rules bind: bounded scope, ground-truth + transcription gate,
> independent re-verification, no commit/push without go-ahead, "could not confirm"
> required, **null result = success**.

---

## The constant source is FIXED — read only from the canonical file

`pslq/constants/basis_canonical.json` is the **SOLE** source of constant values for
this run. Any constant not marked `VERIFIED` there is **barred** from use. Do NOT
transcribe a value from the paper, an abstract, a prior run, or memory; do NOT
recompute S/V_quad ad hoc inside the harness — load them from the canonical file and
confirm their `status == "VERIFIED"` before use.

Ground-truth values you must read from the file (gate: confirm these prefixes match
the file before proceeding; if they differ, STOP):

- **S** (V_quad Stokes constant) = `0.4579066231690176361190978425482258379624`
  - convention: **2π Dingle prefactor** (v1.1 corrected). dps 240, 46 stable digits.
  - value-string sha256 prefix `45db2f07d633fb6e…`
  - ⚠️ The retracted v1.0 value `0.43770528…` (Γ(β_exp)=−6.00599 prefactor) is
    **BARRED**. If your basis or any input carries `0.437705…`, you are using a
    superseded value — STOP.
- **V_quad** = `1.19737399068835760244…` (dps 320, 250 stable). sha256 prefix
  `aef85cbeb117b5db…`

## Scope — do exactly this

1. **Locate the paper's variant definition — do NOT reconstruct it.** Find the exact
   specification of the "245-variant" (or however-many) sweep and the Gamma/period
   **basis** the Painlevé-V paper used to assert the null: which constants enter the
   basis, which products/powers, the precision and tol, and what "null" meant
   (None returned, or coefficients above a stated floor). Sources in order:
   `pcf-research` (vquad/ scripts and any results/ JSON), then the deposited
   Painlevé-V PDF. **Report exactly which source gave the variant/basis definition.**
   If you cannot find the DEFINITION of the variant set and basis (not just the
   word "null"), **STOP and surface it** — do not invent a 245-variant sweep from
   memory or from the decimal.

2. **Run the confirmation** using the existing PSLQ harness (`pslq/pslq_search.py`,
   the B1 harness with the Bailey-floor guard) — feed it the canonical VERIFIED
   S and V_quad plus the paper's stated Gamma/period basis, at the paper's stated
   precision (or higher), strict tol. Enforce the Bailey floor n·log₁₀(maxcoeff);
   a "relation" found below floor is NOT a finding.

3. **Compare to the paper's documented outcome.**
   - Harness reproduces the null (no relation, or all candidates below floor)
     across the variant set → **CONFIRMED**: report the null, the variant count
     actually run, precision/tol/floor, and that it matches the paper.
   - Harness returns a surviving relation the paper did not report → **DISCREPANCY**:
     re-verify at higher precision (dps ×2, ×4). If it survives, STOP and surface
     both (ours vs paper's documented null) — do NOT silently declare a discovery.
   - Variant count or basis cannot be matched to the paper → report the partial
     coverage honestly; a subset-null is a subset-null, not the paper's full null.

4. **Save** the run log (variants run, basis, per-variant outcome, precision/tol/
   floor) with SHA-256. A reproduced null is a complete, successful deliverable.

## OUT OF SCOPE — do NOT attempt

- Do NOT re-derive or re-verify S or V_quad here — that was Thread "basis
  re-verification" and is DONE. Read them from `basis_canonical.json`; if you reach
  to recompute a constant, you've left scope.
- Do NOT use the retracted `0.43770528` S value under any convention.
- Do NOT loosen tol, lower precision, or raise maxcoeff to manufacture a relation
  (or to manufacture a null). The paper's parameters (once found) are the target.
- Do NOT claim a discovery from a sub-floor or unreplicated relation. Do NOT prove
  anything (no Lean, no convergence arguments).
- Do NOT modify `basis_canonical.json`, `pslq_search.py`, or any deposited script.
- Do NOT touch the stale `pcf-research/vquad/scripts` (see sibling to-do
  `agent-tasks/A2-pcf-research-stale-prefactor.md`). No commit/push/tag/move/delete —
  ready-state and STOP.

## Ground truth / transcription gate

- Constant source: `pslq/constants/basis_canonical.json`, entries with
  `status=="VERIFIED"` only. S = `0.4579066231690176361190978425482258379624`
  (2π convention); V_quad = `1.19737399068835760244…`.
- Retracted/barred: S = `0.43770528…` (Γ(β_exp) prefactor, v1.0).
- Bailey floor: digits ≥ n·log₁₀(maxcoeff), with margin.
Confirm these before relying; if your notes differ, STOP and re-read.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>

**Constant-source gate:** loaded S, V_quad from `basis_canonical.json`; confirmed
`status==VERIFIED` and value-string SHA-256 match: <shown>. Confirmed retracted
`0.43770528` does NOT appear in any basis entry.

**Variant/basis definition source:** <repo/file or paper+page that gave the exact
sweep and Gamma/period basis — or "COULD NOT FIND, stopped">

**Confirmation result:**
- variants run: <n of the paper's m> · basis: <listed> · precision/tol/Bailey floor.
- outcome: <NULL reproduced / DISCREPANCY (relation found) / partial coverage>.
- vs paper: <CONFIRMED matches documented null / DISCREPANCY with both values / N/A>.

**Lean / axiom cones:** N/A — this is a numerical confirmation, never PROVEN.

**Honest claim (one sentence):** <e.g. "Harness reproduces the Painlevé-V paper's
documented null across <n> variants against the Gamma/period basis using the
VERIFIED 2π-convention S — confirmed, no clean relation to dps=<…>.">

**What I could NOT confirm (REQUIRED — never empty):** <whether the variant set
fully matches the paper's; whether higher precision than tested would change the
outcome; any basis entry whose definition wasn't source-found.>

**Ready-but-not-done (awaiting operator):** <git add/commit for the run log +
SHA-256; save this task file's audit trail. Operator runs by hand.>
