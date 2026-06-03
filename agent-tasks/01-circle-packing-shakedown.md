# TASK 01: Circle-packing pipeline shakedown (n=26 in unit square)

> Filled-in instance of `agent-tasks/TEMPLATE.md`.
> This is a **pipeline validation task, not a discovery task.** The goal is to
> prove the whole OpenEvolve → sandbox → evaluator → labelling chain works
> against a KNOWN answer, before any novel search is trusted. Treat a
> record-beating number with suspicion, not celebration — see pass condition.

---

## Scope — do exactly this

1. Pin the OpenEvolve dependency: clone ONE specific repo at ONE specific commit
   SHA. Use `codelion/openevolve` (the original) unless the operator names
   another. Record the exact clone URL and the checked-out commit SHA in the
   final report. (There are ≥6 forks under the name "openevolve" — ambiguity
   here is a provenance defect.)
2. Stand up the n=26 circle-packing example: pack 26 non-intersecting circles
   in a unit square to **maximize the sum of radii**.
3. Write an **independent evaluator** (separate file, NOT the one OpenEvolve
   evolves) that takes a configuration (26 centers + 26 radii) and checks:
   - every circle lies fully inside the unit square: `x-r ≥ 0, x+r ≤ 1,
     y-r ≥ 0, y+r ≤ 1` (small numeric tolerance, e.g. 1e-9, stated explicitly);
   - no two circles overlap: for all i<j, `dist(c_i,c_j) ≥ r_i + r_j - tol`;
   - all radii ≥ 0;
   - reports the sum of radii.
4. Run OpenEvolve in the container sandbox (see sandbox rule below) for a
   bounded budget. Report the best valid configuration found and its
   independently-checked sum of radii.

## OUT OF SCOPE — do NOT attempt

- Do NOT chase a record. Beating 2.6359 is not the goal and is not success.
- Do NOT attempt to PROVE optimality or any general bound. This domain yields
  VERIFIED witnesses, never PROVEN theorems. No Lean here.
- Do NOT modify the independent evaluator to make a configuration pass. If a
  configuration fails the evaluator, that is a finding to report, not a bug to
  edit around.
- Do NOT run evolved code on the host. If the sandbox isn't ready, STOP.
- Do NOT raise the budget to manufacture a better number. Stay at the stated
  budget; report what that budget produced.

## Ground truth (use these — do NOT reconstruct from memory)

Source-verified values for n=26, sum-of-radii, unit square:

- Prior best-known: **2.634** (pre-AlphaEvolve).
- AlphaEvolve (Google DeepMind, 2025): **~2.635**.
- Later improved (FICO Xpress solver): **2.63591551**.
- An OpenEvolve user reported reproducing **~2.635977** and explicitly asked
  whether it was *valid* — i.e. even the original reporter did not assume their
  own number was correct. Mirror that posture.

Sources to cite in the report (operator confirmed these resolve):
- AlphaEvolve 26/32-circle improvement: DeepMind AlphaEvolve paper (2025).
- FICO 2.63591551 figure: 36kr coverage of the FICO Xpress result.
- ~2.635977 reproduction: codelion/openevolve issue #156.

**Transcription gate:** before relying on any of the above, confirm you have
them as: prior 2.634, AlphaEvolve 2.635, FICO 2.63591551. If your notes show
different figures, STOP and re-read this section.

## A null result is a COMPLETE, SUCCESSFUL answer

"At the stated budget, the run reached sum-of-radii X (valid per independent
evaluator), below the 2.635 reference" is a fully successful shakedown outcome.
The pipeline working is the deliverable; the number is secondary. Do not extend
the run, relax tolerances, or tweak the evaluator to reach a target figure.

## Sandbox rule (non-negotiable for this project)

OpenEvolve EXECUTES LLM-generated code to score it, and defaults to running it
on the host with no isolation. All evolved code runs in a container sandbox
(e.g. OpenEvolve's `--sandbox-type ContainerSandbox`, or Docker/Podman) on a
non-synced path. If isolation cannot be confirmed, STOP and report — do not
proceed on the host "just for the shakedown."

## Irreversible actions → prepare, then STOP for operator confirmation

Prepare to the ready state and STOP before: commit · push · tag · delete ·
move/overwrite originals · create accounts · modify permissions · publish.
Surface the ready state and the exact command; wait for an explicit operator
"yes". The pinned-SHA record and any results file are prepared for commit but
NOT committed by the agent.

## File operations → copy-first, never move/delete originals

survey → manifest to a safe path → STOP for approval → copy → hash-verify
(record SHA-256) → leave originals as fallback. The cloned OpenEvolve tree is a
dependency, not a canonical artifact — do not edit it in place; copy the example
out before adapting.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>

**OpenEvolve provenance (REQUIRED):**
- Clone URL: <...>
- Commit SHA checked out: <...>
- Install method + Python/env versions: <...>

**Sandbox confirmation (REQUIRED):**
- Isolation mechanism used: <ContainerSandbox / Docker / Podman / ...>
- Confirmed evolved code did NOT run on host: <yes — how verified>

**Result:**
- Budget actually run: <stages / iterations / wall time>
- Best valid configuration's sum of radii (per INDEPENDENT evaluator): <X>
- Reference comparison: <X vs 2.635 AlphaEvolve / 2.634 prior>
- Independent evaluator agreed configuration is valid: <yes/no + which checks>

**Lean / axiom cones:** N/A — no formalization in this task. (PROVEN is not
reachable here; this domain produces VERIFIED witnesses at most.)

**Honest claim (plain language, one sentence):**
<e.g. "Pipeline validated: OpenEvolve at <commit> produced a valid 26-circle
configuration scoring X, independently confirmed; X is CONSISTENT WITH / BELOW
the 2.635 reference." Pick the true one. Do NOT write 'record' anywhere unless
the independent evaluator confirms a valid config strictly above 2.63591551,
in which case label it VERIFIED and flag for operator scrutiny, not celebration.>

**What I could NOT confirm (REQUIRED — never empty):**
<e.g. lemmas/tools/figures I could not verify; whether the reproduced ~2.635977
is itself valid; any source that didn't resolve. If genuinely nothing, say so
and say how it was checked.>

**Ready-but-not-done (awaiting operator confirmation):**
<the exact `git add` / commit command for the provenance record + results file;
the manifest path; files staged. Operator runs these by hand.>
