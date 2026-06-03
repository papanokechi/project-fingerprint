# TASK D1: Pillar-chain integration shakedown (PSLQ → Lean on ζ(2)=π²/6)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. This is the FIRST task that
> spans two pillars. Each pillar is individually validated; the SEAM between them
> never has been. D1 validates the handoff: a result travels
> **CONJECTURED (PSLQ/B1) → PROVEN (Lean/C1)** on a KNOWN, provable identity, so
> the answer is certain and the focus is the integration, not the mathematics.
>
> Target: ζ(2) = π²/6 (the Basel problem; Euler 1735; in Mathlib). Chosen because
> it is exactly true, PSLQ should find it rock-solid (like Machin, unlike the
> Catalan null), AND Mathlib already has the theorem — so the Lean step is
> lookup-and-apply, keeping the focus on the chain rather than a hard proof.
>
> Substrate: B1 step local-only (PSLQ, full strength on CPU). C1 step local,
> checking-only, model-ASSISTED (operator/Claude authors Lean; machine judges via
> the cone). All prior rules bind for both pillars.

---

## The chain, stated as three gated stages

```
Stage 1 (B1):  PSLQ finds the relation among [ζ(2), π²]  → CONJECTURED
                 gate: survives dps 100→200→400 re-test (genuine, not artifact)
Stage 2 (handoff): the CONJECTURED relation is written as a Lean theorem STATEMENT
                 gate: statement type-checks; NOT yet proven (sorry placeholder OK here)
Stage 3 (C1):  the theorem is PROVEN in Lean via Mathlib                → PROVEN
                 gate: #print axioms = subset {propext, Classical.choice,
                       Quot.sound}, NO sorryAx, 0 sorry, 0 errors
```

The deliverable is the chain working: a relation that is CONJECTURED after Stage 1
and PROVEN after Stage 3, with both labels earned by their respective machine
gates — not asserted.

## Pre-flight gates (every run)

- B1 stage: `pslq_search.py` SELFTEST still PASS (regression).
- C1 stage: the pinned `lean/fingerprint-cores/` project still builds clean
  (`lake build`, exit 0); confirm `lean-toolchain` + `lake-manifest.json` unchanged
  from the committed C1 pins (rev 8a178386…). If the build is dirty, STOP.

## Stage 1 — PSLQ (B1): rediscover ζ(2) = π²/6

1. Basis: `x = [zeta(2), pi**2]` computed to mp.dps ≥ 100 (use 400 for re-test).
   `zeta(2)` via `mpmath.zeta(2)`; confirm it ≈ 1.6449340668482264... before use.
2. Expected: PSLQ returns `[6, -1]` (i.e. 6·ζ(2) − π² = 0 ⇔ ζ(2) = π²/6), or an
   integer multiple/sign variant. Small coefficients ⇒ Bailey floor trivially low
   ⇒ a miss would be a bug, not a precision limit.
3. Re-test at dps 100→200→400: coefficients must be IDENTICAL and the residual
   must vanish to working precision (the Machin-style "genuine relation" signature
   you calibrated). Save the candidate (basis, coeffs, precisions, residual) with
   SHA-256.
4. Label: "found; CONJECTURED-class numerical match." (It is well-known — the
   Basel problem — so novelty is N/A; this is a rediscovery by design.)

## Stage 2 — Handoff: state the theorem in Lean

5. In a new module `lean/fingerprint-cores/FingerprintCores/Basel.lean`, write the
   theorem STATEMENT corresponding to the PSLQ relation, e.g.
   `theorem zeta_two_eq : ∑' n : ℕ, (1 : ℝ) / (n+1)^2 = Real.pi^2 / 6 := by sorry`
   — or whatever statement form matches the available Mathlib lemma (see Stage 3).
   At this stage a `sorry` is ALLOWED as a placeholder; confirm the statement
   type-checks (builds with only the expected `sorry` warning). This is the
   honest "stated but not proven" intermediate — do NOT label it PROVEN.

## Stage 3 — Lean (C1): prove it via Mathlib, confirm the cone

6. **Find the real Mathlib lemma — do NOT use a name from memory.** Candidate to
   VERIFY (not to trust): something like `riemannZeta_two`, or a real-valued
   form. Survey the installed Mathlib source / docs, `#check` the candidate, and
   paste its REAL signature before using it. The relevant file is
   `Mathlib.NumberTheory.LSeries.RiemannZeta` (confirmed to exist); the exact
   decl name and whether it is stated over ℂ (`riemannZeta`) vs a real `tsum`
   form must be confirmed in-project. If the lemma you expect does not exist
   under the guessed name, it goes on the could-not-confirm list and you find the
   real one — do NOT fabricate.
7. Replace the `sorry` with a real proof using the confirmed lemma (plus any
   `#check`ed bridging lemmas to convert ℂ↔ℝ or tsum forms as needed). If the
   real-valued bridge is non-trivial, it is acceptable to prove the form Mathlib
   states DIRECTLY and note the exact statement proven — honesty about WHICH
   statement is proven beats forcing a prettier statement with a gap.
8. Run `#print axioms <decl>` and record the cone VERBATIM. PROVEN only if the
   cone is a subset of {propext, Classical.choice, Quot.sound}, no sorryAx, 0
   sorry, 0 errors.

## OUT OF SCOPE — do NOT

- Do NOT label the relation PROVEN until Stage 3's cone is clean. After Stage 1
  it is CONJECTURED; after Stage 2 it is STATED-not-proven; only a clean cone
  earns PROVEN.
- Do NOT use any Mathlib lemma name unverified by `#check`.
- Do NOT loosen PSLQ tol or lower precision in Stage 1.
- Do NOT claim novelty — this is a deliberate rediscovery of a known theorem to
  test the CHAIN. Say so plainly.
- Do NOT leave a sorry'd statement labelled as proven.
- No commit/push/tag/move/delete — ready-state and STOP.

## Ground truth / transcription gate

- ζ(2) = π²/6 (Basel problem, Euler 1735). `mpmath.zeta(2)` ≈ 1.6449340668482264.
- PSLQ on `[zeta(2), pi**2]` should yield `[6, -1]` or equivalent.
- PROVEN cone: subset {propext, Classical.choice, Quot.sound}, no sorryAx.
- Mathlib file `Mathlib.NumberTheory.LSeries.RiemannZeta` exists; exact lemma
  name to be confirmed in-project, NOT assumed.
Confirm before relying; if notes differ, STOP and re-read.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary of the three stages>

**Pre-flight:** PSLQ SELFTEST <PASS/FAIL>; `lake build` of fingerprint-cores
<clean/dirty>; C1 pins unchanged <yes/no>.

**Stage 1 — PSLQ (CONJECTURED):**
- basis, coefficient vector found, precisions tested (100/200/400), residual at
  dps 400, survived? <…> · saved path + SHA-256.

**Stage 2 — Handoff (STATED):**
- theorem statement written; type-checks with only the placeholder sorry: <yes>.

**Stage 3 — Lean (PROVEN):**
- Mathlib lemma used, with REAL signature confirmed via #check: <paste>.
- could-not-confirm list (names tried that #check rejected): <…>.
- the exact statement actually proven: <paste the theorem as proven>.
- axiom cone VERBATIM:
```
#print axioms <decl>
→ <exact output>
```
- sorry count: <n> · error count: <n> · class: <PROVEN / not>.

**Honest claim (one sentence):**
<"Pillar chain validated end-to-end: PSLQ rediscovered 6·ζ(2)−π²=0 (CONJECTURED,
holds to dps 400), the relation was stated in Lean and PROVEN via Mathlib
<lemma>, cone clean (verbatim above) — a known identity (Basel, 1735) carried
CONJECTURED→PROVEN to test the seam, no novelty claimed.">

**What I could NOT confirm (REQUIRED — never empty):**
<e.g. exact Mathlib decl name until #checked; whether the ℂ↔ℝ bridge introduced
any dependency; whether the proven statement form is the "natural" one.>

**Ready-but-not-done (awaiting operator):**
<git add/commit for: the new Basel.lean, the saved PSLQ candidate JSON, and
agent-tasks/D1-…md (save spec to disk — audit trail). .lake/ stays ignored.
Operator runs by hand.>
