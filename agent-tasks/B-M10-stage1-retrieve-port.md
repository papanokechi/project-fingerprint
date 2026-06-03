# TASK B-M10-S1: Retrieve & port the M10 apparent-singularity core into Fingerprint (Stage 1)

> Follows the confirmed Stage 0 of `B-M10-lean-conditional-core.md`. Stage 0
> resolved the provenance question: the M10 core file **is on the remote** and is
> **self-contained**. This task retrieves it and ports it into
> `lean/fingerprint-cores/`, then records the axiom cone honestly. Character
> (confirmed Stage 0): **CONDITIONAL-FORMALIZATION** — the deliverable is a
> sorry-free build whose theorems are explicitly conditional on named axioms, NOT
> a full PROVEN.
>
> All standard rules bind: locate-don't-reconstruct (here: copy the REAL file, do
> not retype it), no Mathlib lemma names from memory (`#check` in-project),
> PROVEN/CONDITIONAL set by the `#print axioms` cone, "could not confirm"
> required, **no commit/push/tag/move/delete** — ready-state and STOP.

---

## Stage 0 outcome (confirmed — the ground truth this task builds on)

- **Source file:** `papanokechi/wallis-pcf-lean4`, path `lean/Thm66_ApparentSingularity.lean`,
  on branch **`vquad/handoff-2026-04-16`** (NOT on `main`; `main`'s `lean/` has only
  `WallisFamily.lean`, `lakefile.lean`, `lean-toolchain`). 155 lines.
- **Self-contained:** imports are **Mathlib-only** (`Analysis.Calculus.Deriv.{Basic,Add,Pow,Mul}`,
  `Analysis.SpecialFunctions.Pow.Real`, `Data.Matrix.Basic`, `Data.Complex.Basic`);
  `IndicialPoly` and all coefficients/roots are defined IN this file. It needs
  **none** of the sibling modules (WallisFamily, ShiftConsistency, CasoratianPi4,
  proof_targets, LemmaK, CardEvenOfInvolution) — those are NOT on the remote and are
  NOT required for this core. Retrieval scope = **this one file**.
- **Version gap:** source pins `leanprover/lean4:stable` + UNPINNED mathlib HEAD;
  Fingerprint pins `leanprover/lean4:v4.29.0` + mathlib commit `8a178386`. The port
  re-pins to v4.29.0 and must fix any API drift.
- **Conditional footprint (the named axioms in the file):**
  - `frobenius_double_root_at_apparent_singularity` — `mathlib_gap: Frobenius ODE theory` (genuine analytic gap, H₁)
  - `monodromy_unipotent_from_double_root` — `mathlib_gap: Monodromy of linear ODE` (genuine analytic gap, H₂)
  - `root_s1`, `root_s2` (`a_coeff_c sₖ = 0`) and `a_deriv_s1_ne_zero`, `a_deriv_s2_ne_zero`
    — AEAL-tagged "routine"; these are DISCHARGEABLE by computation (optional strengthening).
- **Two `(by sorry)`** at lines 118/120 supply the vestigial `h_exact` param of the
  Frobenius axiom; the documented fix is **"Pattern alpha" — delete `h_exact` from the
  axiom signature** (strictly strengthens it, 3 hyps→2) and remove the two `(by sorry)`
  args ⇒ project sorry-count 2→0.

## ⚠️ STRENGTH CAVEAT — read before deciding the deliverable's honest claim

`IndicialPoly (a : ℂ→ℂ) (s : ℂ) : ℂ→ℂ := fun ρ => ρ ^ 2` (line 86) **ignores `a` and
`s`** — it returns `ρ²` for every input. Consequently `apparent_singularity_thm_i`'s
conclusion `IndicialPoly a_coeff_c sₖ = fun ρ => ρ²` is **definitionally `rfl`**, and
the Frobenius axiom is **decorative at the use site** (the theorem is provable by
`exact ⟨rfl, rfl⟩` with no axiom and no sorry). The formalization therefore does NOT
yet encode the *content* that the indicial polynomial of THIS ODE genuinely equals ρ²;
`IndicialPoly` is a stub. The honest claim must say this plainly. A faithful
formalization (out of scope here unless the operator expands it) would define
`IndicialPoly` to actually compute the indicial polynomial from the ODE coefficients,
at which point the Frobenius axiom becomes load-bearing.

## Scope — do exactly this

1. **Pre-flight:** `lean/fingerprint-cores/` builds clean (`lake exe cache get`
   then `lake build`, exit 0); pins unchanged (toolchain `v4.29.0`, lakefile mathlib
   `rev "v4.29.0"`, manifest mathlib `8a178386…`). If dirty, STOP.
2. **Retrieve the REAL file** (do not retype): clone `wallis-pcf-lean4` at branch
   `vquad/handoff-2026-04-16` (or `gh api .../contents/lean/Thm66_ApparentSingularity.lean?ref=vquad/handoff-2026-04-16`
   raw) and copy it into a new module `FingerprintCores/M10ApparentSingularity.lean`.
   Record the source commit SHA + the file's SHA-256.
3. **Port to v4.29.0:** add the module to the import graph; `lake build`; fix any
   v(stable/4.30)→v4.29.0 API drift (e.g. renamed `deriv`/`HasDerivAt`/`Matrix.mulVec`
   lemmas) — every replacement lemma `#check`ed in-project, none from memory. Keep the
   mathematical statements byte-faithful to the source; only adapt API names/syntax.
4. **Apply Pattern alpha** (the documented M10 closure): delete the `h_exact` parameter
   from `frobenius_double_root_at_apparent_singularity` and remove the two `(by sorry)`
   args at the use sites. Confirm sorry-count → 0. Do NOT alter the axioms' conclusions.
5. **Record the cone VERBATIM** for the key results:
   `#print axioms apparent_singularity_thm_i` and `#print axioms vquad_monodromy_invariant`.
   Expected: the cone CONTAINS the custom axioms (`frobenius_…`, `monodromy_…`,
   `root_s*`, `a_deriv_s*`) ⇒ **CONDITIONAL, not PROVEN** — the Fingerprint gate
   correctly refusing PROVEN because of the explicit axioms. Report the exact cone.
6. **(Optional strengthening, only if time permits and operator agrees)** discharge the
   "routine" axioms `root_s1/s2` (verify `3sₖ²+sₖ+1 = 0` for `sₖ=(-1±i√11)/6` — a
   `field_simp`/`ring`-style computation with `sqrt_11_sq`) and `a_deriv_s*` by real
   proofs, shrinking the conditional footprint to just the two genuine analytic gaps
   (Frobenius, Monodromy). Keep each as a separate, clearly-labelled lemma.

## OUT OF SCOPE — do NOT

- Do NOT retype/reconstruct the file from memory or from the Stage-0 transcript — copy
  the REAL file from the confirmed branch; flag any byte you had to change (API drift)
  explicitly.
- Do NOT attempt to discharge the Frobenius or Monodromy `mathlib_gap` axioms (that is
  formalizing ODE Frobenius/monodromy theory — a major separate effort). They stay
  axioms; name them in the honest claim.
- Do NOT "fix" the `IndicialPoly` stub into a real indicial-polynomial computation
  unless the operator explicitly expands scope — surface it as the strength caveat, do
  not silently rewrite the deposited content.
- Do NOT label anything PROVEN while the custom axioms are in the cone. The honest class
  is CONDITIONAL (PROVEN-modulo-the-named-axioms).
- Do NOT edit the other Fingerprint cores or the toolchain/Mathlib pins. No commit/push.

## A clean result either way is success

- File ported, builds clean, sorry-free, cone recorded showing the named axioms →
  **CONDITIONAL-FORMALIZATION delivered**, with the IndicialPoly-stub caveat documented.
  This is the wanted outcome.
- v4.29.0 API drift proves unbridgeable without major work → report the specific
  failures (a real version-gap finding) and STOP; do not force it.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <retrieve + port + Pattern-alpha summary>

**Retrieval provenance:** source branch `vquad/handoff-2026-04-16`, commit SHA <…>,
file SHA-256 <…>; bytes changed for v4.29.0 API drift (list each, with the `#check`ed
replacement lemma): <…>.

**Pre-flight:** `lake build` of fingerprint-cores <clean/dirty>; pins unchanged <yes/no>.

**Port result:** builds <exit 0/n>; sorry count after Pattern alpha <0/n>; error count <n>.

**Axiom cones VERBATIM:**
```
#print axioms apparent_singularity_thm_i
→ <exact output>
#print axioms vquad_monodromy_invariant
→ <exact output>
```

**Honest claim (one sentence):** <e.g. "M10 apparent-singularity core ported into
fingerprint-cores and building sorry-free under Lean v4.29.0; `apparent_singularity_thm_i`
and `vquad_monodromy_invariant` are PROVEN CONDITIONAL on the named axioms
{frobenius_double_root_at_apparent_singularity, monodromy_unipotent_from_double_root,
root_s*, a_deriv_s*}; note `IndicialPoly` is a stub (`fun ρ => ρ²`), so the
apparent-singularity statement is definitionally trivial and the Frobenius axiom is not
yet load-bearing.">

**What I could NOT confirm (REQUIRED — never empty):** <which axioms remain undischarged;
whether the v4.29.0 API matched the source; whether the IndicialPoly stub was intended;
any lemma `#check` rejected.>

**Ready-but-not-done (awaiting operator):** <git add/commit for the new
`FingerprintCores/M10ApparentSingularity.lean` + this spec; `.lake/` ignored. By hand.>
