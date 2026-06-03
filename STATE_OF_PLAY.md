# Project Fingerprint — State of Play

*Durable snapshot of what exists, what's validated, and what comes next.*
*Purpose: a fresh session (or a fresh operator) starts from this map, not from
git archaeology or chat history. Update this file at the end of each working
session.*

Last updated: end of the build-and-validation phase (D1 complete).

---

## One-line status

The three-pillar discovery factory is **built and fully validated on known
answers and deliberate failures.** The CONJECTURED→PROVEN seam works end-to-end.
No genuine (unknown-answer) discovery run has been attempted yet — that is the
next phase.

---

## What this project is

A discovery loop where an LLM is the creative/mutation operator and a
deterministic machine is always the judge. Scope is restricted to domains where a
cheap evaluator can be written first. Three pillars, three output classes, each
gated by a machine the model cannot talk past:

| Pillar | Tool | Output class | Gate |
|--------|------|-------------|------|
| Search (evolutionary) | OpenEvolve + local model | **VERIFIED** witness | independent evaluator confirms a valid configuration |
| Integer relations | PSLQ (mpmath) | **CONJECTURED** relation | survives high-precision re-test above the Bailey floor |
| Formal proof | Lean 4 + Mathlib | **PROVEN** theorem | `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}, no sorryAx |

The pillars chain: a CONJECTURED relation (PSLQ) can be carried to a PROVEN
theorem (Lean). That seam is validated (Task D1).

## Host constraints (these shape every decision)

- CPU-only, 16 GB RAM, no usable GPU (Intel UHD 620 integrated only).
- Local model permanently capped at ~7B (qwen2.5-coder:7b via Ollama).
- Consequence: the **search pillar (OpenEvolve) is shakedown-only locally** — a
  7B is too weak to mutate code for genuine discovery. Real search-pillar
  discovery would need a hosted model (a spend + principle decision, not yet made).
- The **PSLQ pillar is NOT capped** — the deterministic engine does the work on
  CPU; the model only proposes constant-sets. This is the pillar that can do real
  discovery on the current host.
- The **Lean pillar** verifies fine on CPU; proof *authoring* is model-assisted
  (operator/Claude writes, machine judges), not model-autonomous.

---

## What is built and validated (all committed + pushed)

Repo: `github.com/papanokechi/project-fingerprint` (private). Working tree at
`C:\LocalWork\project-fingerprint` (local, non-OneDrive). 48 KiB on remote — no
regenerable bulk leaked.

- **Infrastructure (day one):** git on a non-synced path, pushed remote,
  `.gitignore` (unanchored `.lake/`, vendored clones, `output*/`, weights),
  pinned toolchains, epistemic-status convention in README, agent task template.
- **Search pillar — OpenEvolve, validated across two domains:**
  - Tasks 01–03: pinned container (OpenEvolve @80945ed, base digest 93ab4b7f),
    local model via `host.docker.internal`, n=26 circle-packing shakedown.
    Validated end-to-end; graceful failure on weak model confirmed.
  - Task 04: cap-sets in AG(n,3). Independent evaluator self-tested (incl.
    adversarial line-completion + oversized-garbage rejection). Known maxima
    n=3→9, n=4→20 re-derived by exhaustive backtracking. Shakedown reached seed
    sizes (8/16) — chain works, model weak, as expected.
- **PSLQ pillar — B1, fully validated on all four outcome types:**
  - Harness `pslq/pslq_search.py` with Bailey-floor precision gate
    (effective precision = min(dps, −log₁₀ tol) ≥ n·log₁₀(maxcoeff) + margin).
  - Self-test: accepts true 2√2=√8, rejects π/[22,7] artifact.
  - Wild known relation: rediscovered Machin's formula [1,−16,4], rock-solid.
  - Open-target null: Catalan G vs {π, π·log2, log2} — clean null to dps 400
    (expected; G has no known elementary closed form).
- **Lean pillar — C1, validated with the cone gate demonstrably firing:**
  - Pinned project `lean/fingerprint-cores/` (Lean v4.29.0, Mathlib rev
    8a178386…). Warm-ups PROVEN (clean cones); adversarial sorry'd control
    correctly shows `sorryAx` — the gate catches incomplete proofs.
- **Cross-pillar seam — D1, validated end-to-end:**
  - Basel ζ(2)=π²/6 carried CONJECTURED (PSLQ, residual ~1.7×10⁻⁴⁰⁰) →
    STATED (Lean statement + sorry) → PROVEN (`zeta_two_real` and
    `zeta_two_complex`, both cones clean). First result to cross two pillars.
    Both forms proven against native Mathlib lemmas to avoid an unaudited ℂ↔ℝ
    bridge.

## What has NOT been done

- No genuine discovery run (every result so far is a known answer or expected
  null, by design).
- No hosted-model decision (search-pillar discovery is blocked on it).
- No deposit/release (no Zenodo, no tagged version — nothing is claimed as a
  finding yet, so nothing to deposit).

---

## The next move (when a fresh session picks this up)

**Highest leverage: point the PSLQ pillar at the operator's own prior-work
constants** (the PCF/Casoratian envelope values, gate sequences, the "clean
closed form I was sure existed but didn't"). This is the one target that is
(a) novelty-likely, (b) runnable at full strength on the current host, and
(c) able to feed the validated CONJECTURED→PROVEN chain if a relation survives.

Blocker: those numerical values are not yet in the repo. **First step of the next
session: get those constants onto disk** (a values file with provenance), then
scope a D-series task: PSLQ search over a basis including them → if a relation
survives the precision gate, hand to Lean for a PROVEN formalization.

Honest expectation: most bases yield nulls, and a null on the operator's own
constant is still informative ("no low-complexity relation to π/ζ(3)/Catalan to
N digits"). A surviving hit would be the first genuine candidate and worth a
serious novelty/literature check before any claim.

Lower-priority alternatives: continue Catalan widenings (π², ζ(3)) — documented
nulls, low information; or make the hosted-model decision to unlock real
search-pillar discovery (cap sets above known dimensions).

## Operating reminders (carried from lessons-learned)

- A claim's label is set by a machine gate, never by confidence. PROVEN = clean
  cone, not a green build.
- No Mathlib lemma names or citations from memory — `#check`/verify in-project.
- Null results are complete, successful answers; design so the agent never feels
  pressure to fabricate a hit.
- Commit + push the same session; the remote is the durable state. Update THIS
  file at each session end so state never lives only in chat.
- Beware activity substituting for verified progress (a string of expected nulls
  can feel like work while teaching little).
