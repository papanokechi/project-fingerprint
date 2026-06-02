# project-fingerprint

AI-assisted mathematical discovery pipeline: search-with-evaluator conjecture
generation, finitary structural cores, and Lean 4 machine-verified proofs.

Status: **infrastructure / day-one.** No mathematical claims yet.

---

## What this project is

A discovery loop in which an LLM is the *creative mutation operator* and a
deterministic machine is *always the judge*. Every real system this is built on
(FunSearch/AlphaEvolve, Ramanujan Machine, Goedel-Prover) shares one trait: a
cheap, deterministic evaluator the model cannot talk its way past. So the scope
is deliberately restricted to **domains where the evaluator can be written
first** — integer relations (PSLQ), continued fractions, extremal combinatorics,
finitary identities. Where no cheap evaluator exists, the output is a
*conjecture*, labelled as such, not a discovery.

"Exponential" (if it happens) comes from search throughput against a verifier —
never from the model being clever.

---

## Epistemic status convention (READ BEFORE CLAIMING ANYTHING)

A claim's label is set by what a **machine** confirms, not by how confident
anyone — human or agent — feels. Four classes:

| Class | Meaning | Confirmed by |
|-------|---------|--------------|
| **PROVEN** | Machine-checked, no gaps | Lean axiom cone (see below) |
| **VERIFIED** | Numerically checked to high precision, not yet formalized | mpmath/sympy transcript committed |
| **STRUCTURAL** | Finitary core formalized; rests on explicit hypotheses | Lean build + named hypotheses |
| **CONJECTURED** | Search-generated, plausible, unproven | nothing yet — honest default |

### PROVEN means exactly this — nothing weaker

A declaration is PROVEN **only** when:

```
#print axioms <decl>
```

shows exactly `{propext, Classical.choice, Quot.sound}`, **with no `sorryAx`**,
**AND** zero `sorry` tactics, **AND** zero errors.

A green `lake build` is **NOT** proof. A `sorry` compiles fine. **Always check
the cone.** Source comments must match the cone — a decl commented STRUCTURAL
whose cone is actually clean is a defect to fix, not cosmetic.

### The conditional-core pattern (the workhorse)

When the full theorem needs heavy analysis (limits, Stirling, convergence) that
isn't finitary: formalize the **finitary structural core** and take the hard
analytic fact as an **explicit, clearly-labelled hypothesis**. State plainly:
"verified CONDITIONAL on H." This is honest and still strong.

Do **not** let "verified conditional on H" silently become "verified."

### Numerically verify before formalizing or writing

Every load-bearing identity, coefficient, constant, and gate value gets checked
in mpmath/sympy **first**, and the transcript committed. Last project this
caught a wrong determinant sign, wrong gate values, a wrong leading constant,
two wrong envelope claims, and a false inequality. Cheap check, expensive miss.

---

## Anti-fabrication rules (humans and agents alike)

- **No citations from memory.** Every cited theorem/lemma number is
  source-verified or carries `% FLAG(operator): confirm` until the physical
  edition is checked.
- **No Mathlib lemma names from memory.** Survey installed source, `#check` it,
  paste the real signature. Maintain a "could-not-confirm-exists" list; never
  use anything on it.
- **Survey before wiring.** "No usable lemma/tool exists" is a complete,
  successful answer. Tasks are designed so a null result is not a failure.
- **Verify surprising negatives too.** A clean closed form you're *sure* exists
  may not. Admitting that is the right call.

### Tool reality list

External services named in planning docs are **CONJECTURED to exist** until a
live URL resolves and a repo shows commits. Confirmed real as of project start:
Ramanujan Machine, FunSearch/AlphaEvolve (+ OpenEvolve clone), Goedel-Prover,
Lean 4 + Mathlib, PSLQ, SageMath/SymPy/mpmath. Everything else from the survey
doc stays on the could-not-confirm list until checked.

---

## Repo topology

Per-artifact repos for anything independently depositable (each Zenodo deposit =
one tagged release of one repo), plus this repo as notes/scratch + orchestration.

- `project-fingerprint` (this) — orchestration, search drivers, notes
- `fingerprint-lean-cores` — Lean formalizations (created when first core exists)
- additional per-result repos as discoveries solidify

Each durable claim is SHA-anchored: it points at a commit SHA and a versioned
DOI, never a branch HEAD or a dirty tree. Commit before depositing.

---

## Agent division of labor

- **Claude Desktop** — orchestrator + epistemics keeper. Conjectures, finitary
  cores, numerical pre-verification, task templates, abstracts. *Never* the final
  judge of PROVEN.
- **Copilot CLI agents** — bounded gated executors. Run search loops and file ops
  under the task template (`/agent-tasks/TEMPLATE.md`). Irreversible actions stop
  for operator confirmation.
- **VS Code agents** — in-repo Lean formalization + verification. The **only**
  place PROVEN is earned (the only place the axiom cone is checked).

---

## Sandbox policy for evolved code

FunSearch/OpenEvolve clones **execute LLM-generated code to score it**, and
default to running it on the host with no isolation. All evolved/LLM-generated
code runs in a container sandbox on a non-synced path. No exceptions, no
"just this once on the host."

---

## Day-one checklist

- [x] `C:\LocalWork\project-fingerprint` (non-OneDrive). `git init`.
- [ ] Empty GitHub repo (private), remote added, initial commit **pushed same day**.
- [ ] `.gitignore`, `LICENSE`, `README` committed.
- [ ] Toolchain pinned (`lean-toolchain`, `lake-manifest.json`) once Lean is in.
- [x] Repo topology decided (above).
- [x] Epistemic-status convention written (above).
- [ ] CLI-agent task template saved (`/agent-tasks/TEMPLATE.md`).
- [ ] Sandbox policy decided (above).
- [ ] **Only THEN** start the mathematics.

---

## Wellbeing note

Long, self-driven program. Two guards: (1) the multi-session handoff model only
works if anchors are real (committed + pushed) — infrastructure-first is what
makes the work survivable across sessions without re-deriving state from memory;
(2) beware the "verified/archived" satisfaction outrunning the actual
verification. The discipline above exists to keep the satisfaction attached to
the real thing — clean axiom cone, pushed commit, resolving DOI — not the
appearance of it.
