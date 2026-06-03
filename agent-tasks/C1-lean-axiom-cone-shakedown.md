# TASK C1: Lean formalization pillar — setup + axiom-cone shakedown (local)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. Opens **Pillar C** (machine-
> checked proof, Goedel-Prover/Lean lineage). This is the ONLY pillar that
> produces **PROVEN**, and the gate is the axiom cone — not a green build.
>
> Substrate: **local, checking-only.** Lean + Mathlib build and `#print axioms`
> run fine on CPU — no GPU needed to VERIFY. The weak 7B CANNOT autonomously
> generate Mathlib-level proofs, so this pillar is **model-ASSISTED, not model-
> autonomous**: the operator/Claude authors the Lean; the model helps with lemma
> lookup and boilerplate; the MACHINE is the judge regardless of who wrote the
> proof. That is not a limitation — it is the only configuration in which PROVEN
> means what the convention says.
>
> All standard rules bind: bounded scope, no Mathlib lemma names from memory,
> independent verification (the cone), no commit/push without go-ahead, "could
> not confirm" required.

---

## PROVEN — the gate, stated exactly (official Lean criterion)

A declaration is PROVEN iff `#print axioms <decl>` reports a subset of exactly
`{propext, Classical.choice, Quot.sound}` — **with NO `sorryAx`**, NO user-
defined axioms, AND the file builds with 0 errors and contains 0 `sorry`.

- A green `lake build` is NOT proof. `sorry` compiles; the cone catches it.
- Beware statement-vs-proof confusion: it is trivial to NAME a true-looking
  statement and `sorry` its proof. The cone is what distinguishes "stated" from
  "proven." Always print the cone for the ACTUAL theorem, not a lemma near it.
- A decl whose cone is clean but whose comment says STRUCTURAL/CONJECTURED is a
  defect to FIX (promote the label), not cosmetic.

## Reproducibility — pin the project (official Lean guidance)

Lean + Mathlib move fast with little backward-compatibility; a standalone file
that builds today may not build elsewhere or later. Therefore the Lean work MUST
be a pinned project: commit `lean-toolchain` and `lake-manifest.json`. "Mathlib
prebuilt" is not reproducible; a pinned rev is. Record exact Lean + Mathlib
versions in the report.

## Scope — do exactly this

1. **Stand up a pinned Lean 4 + Mathlib project** under
   `lean/fingerprint-cores/` (or a sibling per the repo topology). Use `lake`;
   pull Mathlib at a specific rev; commit `lean-toolchain` + `lake-manifest.json`.
   Confirm a clean `lake build` of an empty/trivial module before anything else.
   (First build of Mathlib is slow on CPU — expected; report wall-clock.)

2. **Prove three trivially-true warm-up theorems** whose ONLY purpose is to
   validate the cone workflow — this pillar's n=26 shakedown. Suggested ladder
   (operator may swap):
   - a pure-logic tautology that should yield a MINIMAL cone (possibly just
     `[propext]` or empty) — demonstrates a clean minimal cone;
   - a simple arithmetic/Nat lemma proved via Mathlib — likely the full
     `{propext, Classical.choice, Quot.sound}` (fine, still PROVEN);
   - **the adversarial case:** state a true theorem and prove it with `sorry`,
     then run `#print axioms` and CONFIRM it reports `sorryAx`. This proves the
     gate actually catches an incomplete proof. (Then either complete it or
     clearly mark it as the deliberate negative control — do NOT leave a sorry'd
     theorem labelled PROVEN.)

3. **For every theorem, run `#print axioms <decl>` and record the cone VERBATIM**
   in the report. State per-decl: cone contents, sorry count, error count, and
   the resulting class (PROVEN only if the cone is clean + 0 sorry + 0 errors).

4. **No Mathlib lemma names from memory.** Any Mathlib lemma used is `#check`ed
   and its real signature confirmed before use. Maintain a "could-not-confirm-
   exists" list; never use anything on it. (The 7B is especially prone to
   hallucinating plausible-but-nonexistent Mathlib names — treat every suggested
   lemma as unverified until `#check` passes.)

## OUT OF SCOPE — do NOT attempt

- Do NOT attempt a hard/novel theorem yet. This task validates the cone workflow
  on trivial theorems. (A real target — e.g. formalizing a finitary structural
  core, or proving a PSLQ candidate from Pillar B — is a LATER task once the
  workflow is proven.)
- Do NOT report PROVEN on the strength of a green build. Cone or it didn't happen.
- Do NOT use a Mathlib lemma you have not `#check`ed.
- Do NOT leave the sorry'd control theorem mislabelled.
- Do NOT rely on the 7B to author the proofs autonomously; it assists, the
  operator/Claude authors, the machine judges.
- No commit/push/tag/move/delete — ready-state and STOP.

## Ground truth / transcription gate

- PROVEN cone target: subset of `{propext, Classical.choice, Quot.sound}`,
  no `sorryAx`.
- `sorryAx` in the cone ⇒ incomplete proof ⇒ NOT proven (this is the gate working).
- Reproducibility requires committed `lean-toolchain` + `lake-manifest.json`.
Confirm before relying; if your notes differ, STOP and re-read.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>

**Project / toolchain (REQUIRED for reproducibility):**
- Lean version: <...>  · Mathlib rev: <...>
- `lean-toolchain` + `lake-manifest.json` committed-ready: <paths>
- Clean `lake build` of trivial module: <pass/fail + wall-clock>

**Per-theorem axiom cones (VERBATIM — REQUIRED):**
For each of the three warm-ups:
```
#print axioms <decl>
→ <exact output>
```
- sorry count: <n> · error count: <n> · class: <PROVEN / STRUCTURAL / …>

**Gate self-test (the adversarial control):**
- sorry'd theorem → `#print axioms` reported `sorryAx`: <yes/no>. (Must be yes —
  this confirms the gate catches incomplete proofs.) Final disposition of that
  theorem: <completed / clearly marked negative control, NOT labelled PROVEN>.

**Mathlib lemmas used:** <each lemma + confirmed via #check>. Could-not-confirm
list: <names the 7B suggested that #check rejected — never used>.

**Honest claim (one sentence):**
<e.g. "Lean pillar validated: pinned Lean <v>/Mathlib <rev> project builds; two
warm-up theorems are PROVEN (cones verbatim above, clean + 0 sorry); the
adversarial sorry'd control correctly shows sorryAx, confirming the cone gate
catches incomplete proofs.">

**What I could NOT confirm (REQUIRED — never empty):**
<e.g. any Mathlib lemma the 7B suggested that didn't exist; whether the pinned
rev builds on another machine (only verified here); first-build wall-clock as
representative.>

**Ready-but-not-done (awaiting operator):**
<git add/commit for the Lean project (lakefile, lean-toolchain, lake-manifest,
the warm-up .lean file); note: Mathlib build artifacts (.lake/, *.olean) stay
git-ignored. Save agent-tasks/C1-…md to disk (audit trail). Operator runs by hand.>
