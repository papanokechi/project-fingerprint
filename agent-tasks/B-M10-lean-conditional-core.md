# TASK B-M10: Discharge / formalize the M10 conditional core in Lean (Stage 0 only)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. Opens **Thread B**, the only
> unrun thread of the current push and the one that produces **PROVEN** (clean
> axiom cone) rather than VERIFIED/CONFIRMED. It targets **M10** — a deposited
> result that currently rests on an unproven *analytic hypothesis* (a
> "conditional core"). The goal is to lift that hypothesis from assumed to either
> (a) PROVEN in Lean via Mathlib, or (b) honestly STATED as a conditional
> implication `H → result` with `H` named — discharging or tightening the
> analytic hypothesis a deposited paper rests on.
>
> Substrate: **local, checking-only, model-ASSISTED** — operator/Claude authors
> Lean; the machine judges via the axiom cone. The Lean pillar verifies fine on
> CPU; proof *authoring* is the slow, human-in-loop part (per STATE_OF_PLAY:
> "model-assisted, not model-autonomous"). Builds are slow (see timing note).
>
> All standard rules bind: **locate-don't-reconstruct**, no Mathlib lemma names
> from memory (`#check` in-project), PROVEN earned by the cone (not a green
> build), "could not confirm" required, an honest negative is a complete result,
> **no commit/push/tag/move/delete** — ready-state and STOP.

---

## CRITICAL — M10 IS NOT DEFINED IN THIS REPO YET

`M10` appears in the corpus only as a *named, gated thread* (see
`pslq/constants/basis_canonical.json` and `basis_canonical_README.md`: "SOLE
source basis runs (R1, V_quad-S, **M10** threads) may read from"). Its actual
mathematical content — which deposited paper, which identity/quantity, and which
analytic hypothesis the deposited core is conditional on — **is not on disk in
`project-fingerprint`.** Therefore the FIRST job is to LOCATE what M10 is from
the deposits. **Do NOT invent or reconstruct M10's statement, its hypothesis, or
its proof from memory or from a plausible guess.** A confidently-wrong setup
here yields a confidently-wrong "PROVEN" label, which is worse than a null.

## STAGE 0 — locate M10 AND determine the task's true character
## (do this FIRST, then STOP for operator confirmation before any Lean authoring)

1. **Locate M10's definition** in the deposits / repos — do not reconstruct.
   Sources to check, in order: the GitHub repos `papanokechi/siarc-relay-bridge`
   (session folders — search `gh search code --repo papanokechi/siarc-relay-bridge M10`
   and grep its STATE/handoff notes), `papanokechi/pcf-research`,
   `pcf-casoratian-identities`, `wallis-pcf-lean4`; then the deposit PDFs
   (Channel Theory / D2-NOTE and any paper whose result is tagged M10). Report:
   - **What M10 is:** the exact deposited statement/quantity (e.g. an identity, a
     limit, a closed form, an inequality), with the source (repo/file+line or
     paper+page+DOI) that gave the DEFINITION (not a value).
   - **The conditional core:** the precise analytic **hypothesis H** the deposited
     result currently assumes (e.g. an asymptotic bound, a convergence/transseries
     claim, an analyticity/Borel-summability assumption, a uniqueness lemma).
     Quote it. This is the thing the Lean step is meant to discharge or formalize.
   - **What basis constants M10 needs** (if any) from `basis_canonical.json`, and
     confirm each has `status = VERIFIED` there (the file is the SOLE constant
     source; a non-VERIFIED constant is BARRED — STOP if M10 needs a barred one).

2. **Reproduce a minimal sanity check** that you have the right M10 — e.g. the
   deposited numeric value/identity recomputed at modest precision, or the exact
   proposition restated and checked for internal consistency — so the operator
   can confirm you located the *intended* object before any formalization.

3. **Determine the task's character** and report which it is, with the supporting
   quote/location:
   - **DISCHARGEABLE-IN-MATHLIB** — H (or the whole result) is a known theorem
     already in Mathlib (like Basel ζ(2)=π²/6 in D1): the Lean step is
     lookup-`#check`-apply → **PROVEN** is achievable this pass.
   - **CONDITIONAL-FORMALIZATION** — H is genuinely hard / not in Mathlib: the
     honest deliverable is the **STATED implication `H → result`** type-checking
     in Lean with `H` an explicit hypothesis (PROVEN of the *implication*, with H
     assumed), NOT a PROVEN of the result. Name H precisely.
   - **NOT-YET-FORMALIZABLE** — the statement cannot be expressed against current
     Mathlib without an unaudited bridge: report that and stop; do not force it.

4. If you **cannot locate** M10's definition or its conditional hypothesis from a
   deposit, **STOP and say so plainly** — do NOT reconstruct M10 from its name,
   from the basis_canonical mention, or from a guess at "what M10 probably is."
   `UNRESOLVED: M10 definition not found` is a complete, acceptable Stage-0
   outcome that surfaces a real provenance gap.

**STOP here. Report Stage 0 and await operator confirmation of (i) the located
M10 statement, (ii) the conditional hypothesis H, and (iii) the task character,
before writing any Lean.**

## STAGE 1 — formalize in Lean (ONLY after Stage 0 confirmed; sketch, to be
## re-scoped by the operator from the located object)

5. **Pre-flight (every run):** the pinned `lean/fingerprint-cores/` builds clean
   — `lake build`, exit 0 — and pins are unchanged: `lean-toolchain` =
   `leanprover/lean4:v4.29.0`, `lakefile.toml` mathlib `rev = "v4.29.0"`,
   `lake-manifest.json` mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
   If the build is dirty or pins differ, STOP. (Use `lake exe cache get` first;
   see timing note — first Mathlib-importing build is ~4–6 min, full warm
   `lake build` ~230 s.)
6. **State M10 in a new module** `FingerprintCores/M10.lean` (add to the import
   graph as the other cores are). Write the theorem STATEMENT matching the
   located object; per the character:
   - DISCHARGEABLE → state the result directly.
   - CONDITIONAL → state `theorem m10 (H : <H as a Lean Prop>) : <result> := …`
     with H an explicit hypothesis. A `sorry` placeholder is allowed at this
     intermediate "STATED-not-proven" step; confirm the statement type-checks
     (builds with only the placeholder `sorry` warning). Do NOT label it PROVEN.
7. **Find the real Mathlib lemma(s) — do NOT use any name from memory.** Survey
   the installed Mathlib source/docs, `#check` each candidate, and paste its REAL
   signature before use. Names that `#check` rejects go on the could-not-confirm
   list; find the real one or stop — never fabricate a lemma name.
8. Replace `sorry` with a real proof (DISCHARGEABLE), or complete the proof of
   the *implication* under the explicit `H` (CONDITIONAL). If a real↔complex or
   tsum-form bridge is non-trivial, prove the form Mathlib states DIRECTLY and
   note exactly which statement is proven — honesty about WHICH statement beats a
   prettier statement with a gap.
9. **Run `#print axioms <decl>` and record the cone VERBATIM.** PROVEN only if the
   cone ⊆ `{propext, Classical.choice, Quot.sound}`, **no `sorryAx`**, 0 `sorry`,
   0 errors. For a CONDITIONAL deliverable, PROVEN applies to the *implication*;
   state plainly "PROVEN conditional on H = …", H still assumed.

## OUT OF SCOPE — do NOT

- Do NOT reconstruct M10's statement, its hypothesis H, or any cited result from
  memory or from its name. Located-from-deposit only; STOP if not found.
- Do NOT use any Mathlib lemma name unverified by `#check` in-project.
- Do NOT label anything PROVEN until the cone is clean and `sorryAx`-free; a
  STATED `sorry` is "stated, not proven."
- Do NOT silently discharge H to make the result unconditional — if H is assumed,
  say so. Tightening or discharging H is the *point*; pretending it's gone is the
  failure mode.
- Do NOT modify the pinned toolchain / Mathlib rev, or edit the other cores
  (`Trivial`, `Warmup`, `Basel`, `Control`). No PSLQ here (wrong pillar).
- No commit/push/tag/move/delete — ready-state and STOP.

## A clean result either way is success

- M10 carried to a clean cone → **PROVEN** (or PROVEN-conditional-on-H): the
  wanted outcome, strengthening a deposited paper's analytic footing.
- H not dischargeable in current Mathlib → an honest **CONDITIONAL-FORMALIZATION**
  (the implication proven, H named) is a complete, depositable result.
- M10 not locatable → **UNRESOLVED**, a real provenance gap surfaced. All three
  are complete, honest answers.

---

## REQUIRED FINAL REPORT (fill every field)

**Stage 0 — located M10:**
- What M10 is (exact statement/quantity) + DEFINITION source (repo/file+line or
  paper+page+DOI): <…>
- Conditional hypothesis H (verbatim quote + source): <…>
- Basis constants M10 needs + their `basis_canonical.json` status: <… all VERIFIED?>
- Minimal sanity check that this is the intended M10: <…>

**Task character (REQUIRED):** DISCHARGEABLE-IN-MATHLIB / CONDITIONAL-FORMALIZATION
/ NOT-YET-FORMALIZABLE / UNRESOLVED — with the supporting quote/location.

**Pre-flight (if Stage 1 reached):** `lake build` <clean/dirty>; pins unchanged
(toolchain v4.29.0, mathlib 8a178386…) <yes/no>.

**Stage 1 — Lean (if reached):**
- the exact statement written (paste): <…>
- Mathlib lemma(s) used with REAL `#check` signature(s): <paste>
- could-not-confirm list (names `#check` rejected): <…>
- axiom cone VERBATIM:
```
#print axioms <decl>
→ <exact output>
```
- sorry count: <n> · error count: <n> · class: <PROVEN / PROVEN-conditional-on-H
  / STATED-not-proven / not>.

**Honest claim (one sentence):** <e.g. "M10 (<statement>, deposited in <source>)
PROVEN conditional on H = <hypothesis>: the implication H → M10 formalized in
Lean against Mathlib <lemmas>, cone clean (verbatim above); H itself remains
assumed." OR the located-but-not-formalized / UNRESOLVED finding.>

**What I could NOT confirm (REQUIRED — never empty):** <which deposit gave (or
failed to give) the M10 definition; whether H is the canonical hypothesis or one
of several; any Mathlib lemma not found; whether the proven statement form is the
natural one.>

**Ready-but-not-done (awaiting operator):** <git add/commit for the new
`FingerprintCores/M10.lean` + any sanity-check script + this spec file to disk
(audit trail). `.lake/` stays ignored. Selective staging. Operator runs by hand.>
