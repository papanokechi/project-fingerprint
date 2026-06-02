# CLI / Tier-2 Agent Task Template

Copy this file, fill every section, hand it to the agent. The structure exists
to make honesty the easy path: an agent over-reaches and fabricates when a null
result feels like failure, so a null result is defined here as success.

---

## TASK: <one line>

### Scope — do exactly this
<the specific, bounded thing: e.g. "run a PSLQ sweep for integer relations
among {1, ζ(3), π³, log2³} at 200-digit precision, degree ≤ 3">

### OUT OF SCOPE — do NOT attempt
<list what to NOT touch. Agents over-reach into adjacent hard problems unless
fenced. e.g. "Do not attempt to PROVE any relation found. Do not formalize
anything. Do not touch the Lean repo. If you reach for a convergence argument,
you've left scope — STOP and report.">

### Ground truth (use these — do NOT reconstruct)
<embed the verified constants/values/coefficients/exact tactic so the agent does
not regenerate them wrong. Include a gate the agent must pass before trusting its
own transcription, e.g. "confirm ζ(3) ≈ 1.2020569031595942854 to the digits
shown before proceeding; if your value differs, STOP.">

### A null result is a COMPLETE, SUCCESSFUL answer
"No relation found at this precision / degree" is a valid, wanted outcome.
Do not lower precision, widen degree, or relax thresholds to manufacture a hit.
If nothing is found at the stated parameters, report that and stop.

### Irreversible actions → prepare, then STOP for operator confirmation
The agent prepares to the ready state and STOPS before any of:
commit · push · tag · delete · move/overwrite originals · create accounts ·
modify permissions · publish. Surface the ready state; wait for an explicit
operator "yes". Per-action, per-session — one approval never generalizes.

### File operations → copy-first, never move/delete originals
survey → write manifest to a safe path → STOP for approval → copy →
hash-verify (record SHA-256) → leave originals as fallback.
Deletion is a separate, later, by-hand step. A reconstructed file is NOT the
canonical file — flag it to diff against the master, don't treat it as ground.

---

## REQUIRED FINAL REPORT (structured — fill every field)

**What I did:** <bounded summary>

**Result:** <the finding, or explicit null result>

**For any Lean work — axiom cones VERBATIM:**
```
#print axioms <decl>
→ <paste exact output>
```
- Build exit code: <0 / nonzero>
- `sorry` count: <n>
- Error count: <n>
- PROVEN? <only "yes" if cone == {propext, Classical.choice, Quot.sound},
  no sorryAx, 0 sorry, 0 errors. Otherwise state the actual class.>

**Honest claim (plain language):** <one sentence; if conditional, name the
hypothesis: "verified CONDITIONAL on H = ...">

**What I could NOT confirm (REQUIRED — never leave empty):**
<lemmas/tools/citations/DOIs I could not verify exist. "Could not confirm X
exists" belongs here, not silently dropped. If genuinely nothing, write
"nothing — all referenced items were source-verified" and say how.>

**Ready-but-not-done (awaiting operator confirmation):**
<any irreversible action prepared but held: the exact commit/push/tag command,
the manifest path, the files staged. Operator runs these by hand.>
