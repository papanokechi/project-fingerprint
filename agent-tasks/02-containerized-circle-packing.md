# TASK 02: Containerized circle-packing run (resume of Task 01)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. Resumes
> `agent-tasks/01-circle-packing-shakedown.md` now that a container runtime
> exists (Docker Desktop, WSL2 backend, `docker run --rm hello-world` confirmed
> passing by the operator).
>
> Everything in Task 01 still binds: pipeline-validation-not-record, independent
> evaluator, no record-chasing, no commit/push without operator go-ahead,
> ground-truth figures and transcription gate. This file adds the containerization
> and reproducibility specifics.

---

## Pre-flight gate (do this FIRST, every run — not waived by prior success)

Re-verify isolation yourself before anything else:

```
docker run --rm hello-world
```

If it does not print the Docker success message, STOP and report. Do NOT fall
back to running evolved code on the host under any circumstance. The operator's
confirmation that it worked once does not substitute for your own check now.

## Scope — do exactly this

1. **Pin the dependency.** Clone `https://github.com/codelion/openevolve` and
   check out the SHA selected in the Task 01 report:
   `80945ed82886d5c4ff2f3d22436765d50cb61266`. If that SHA no longer resolves or
   the operator named a different fork/SHA, STOP and confirm before proceeding.
   Treat the cloned tree as a dependency, not a canonical artifact — copy the
   circle-packing example out before adapting; do not edit in place.

2. **Write a pinned, reproducible container.** Author a `Dockerfile` under the
   project (e.g. `containers/circle-packing/Dockerfile`) that:
   - uses a **pinned** base image by digest or exact tag (e.g.
     `python:3.12-slim@sha256:...` — record the digest, not a floating tag);
   - installs OpenEvolve at the pinned SHA and its deps, with versions captured
     (a frozen `requirements.txt` or `uv.lock` committed alongside);
   - runs the search and the evaluator INSIDE the container; the host only
     orchestrates and reads results back out of a mounted output dir.
   The reproducibility target: base-image digest + OpenEvolve SHA + model id +
   config = a re-runnable result. This is also what a later Zenodo deposit needs.

3. **Independent evaluator** (carry over from Task 01, unchanged in intent):
   a SEPARATE file, NOT the program OpenEvolve evolves, that takes 26 centers +
   26 radii and checks: all circles fully inside the unit square (tol 1e-9,
   stated); no overlaps (`dist(c_i,c_j) ≥ r_i+r_j-tol` for all i<j); radii ≥ 0;
   reports sum of radii. The evaluator must be runnable standalone on a saved
   configuration, so a result can be re-checked without re-running the search.

4. **LLM provider for OpenEvolve.** OpenEvolve uses an OpenAI-compatible API.
   Record exactly which model/provider was used (and the endpoint if local).
   Do NOT put any API key in the Dockerfile, the repo, or a committed file —
   pass it via environment at runtime only. If no key/provider is configured,
   STOP and ask the operator rather than guessing.

5. **Run at a bounded budget.** State the budget (iterations/stages/wall-clock)
   before running; do not raise it mid-run to chase a number. Report the best
   VALID configuration found and its independently-checked sum of radii.

## OUT OF SCOPE — do NOT attempt

- No record-chasing. Success = valid config ~2.634–2.635 confirmed by the
  independent evaluator. A number > 2.63591551 is a reason for suspicion and
  operator scrutiny, not a headline.
- No optimality proof, no general bound, no Lean. VERIFIED witnesses only.
- Do not edit the independent evaluator to make a config pass.
- Do not run evolved code on the host. Do not relax the sandbox.
- Do not commit, push, tag, move, or delete. Prepare to ready-state and STOP.
- Do not embed secrets anywhere persistent.

## Ground truth (use these — do NOT reconstruct)

n=26, sum-of-radii, unit square (carried from Task 01, transcription gate applies):
prior best **2.634**; AlphaEvolve **~2.635**; FICO Xpress **2.63591551**;
community-reported OpenEvolve reproduction **~2.635977**, validity unconfirmed.
Before relying on these confirm: prior 2.634 / AlphaEvolve 2.635 / FICO 2.63591551.
If your notes differ, STOP and re-read.

## A null result is a COMPLETE, SUCCESSFUL answer

"At budget X, best valid config = Y < 2.635" fully validates the pipeline. The
chain working end-to-end inside the container is the deliverable. Do not extend
the run or touch tolerances to reach a figure.

## File operations → copy-first, never move/delete originals

survey → manifest to safe path → STOP for approval → copy → hash-verify
(SHA-256) → originals stay as fallback.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>

**Pre-flight gate:** `docker run --rm hello-world` result this session: <pass/fail>

**OpenEvolve provenance (REQUIRED):**
- Clone URL + commit SHA actually checked out: <...>
- Confirmed SHA matches Task 01 selection (80945ed…) or operator-approved change: <...>

**Container reproducibility (REQUIRED):**
- Base image + DIGEST: <python:3.12-slim@sha256:...>
- Dependency lock committed (path): <...>
- LLM model/provider/endpoint used: <...>  (key passed via env, NOT committed: <confirm>)
- One-command re-run invocation: <docker ... >

**Sandbox confirmation (REQUIRED):**
- Evolved code ran ONLY inside the container: <yes — how verified>
- Host involvement limited to orchestration + reading mounted output: <yes/no>

**Result:**
- Budget actually run: <...>
- Best valid config sum of radii (INDEPENDENT evaluator): <Y>
- Reference comparison: <Y vs 2.635 / 2.634>
- Independent evaluator agreed config valid: <yes/no + which checks + saved config path>

**Lean / axiom cones:** N/A — VERIFIED domain, not PROVEN.

**Honest claim (one sentence):**
<"Pipeline validated end-to-end in container at <SHA>/<image digest>: valid
26-circle config scoring Y, independently confirmed; Y is consistent-with/below
the 2.635 reference." Use 'record'/'VERIFIED-record' ONLY if a valid config
strictly exceeds 2.63591551, and then flag for operator scrutiny.>

**What I could NOT confirm (REQUIRED — never empty):**
<e.g. validity of the community ~2.635977; whether base digest is the operator's
intended pin; any source not re-verified against live pages.>

**Ready-but-not-done (awaiting operator confirmation):**
<exact git add/commit commands for: Dockerfile, lockfile, evaluator, saved best
config, results summary; the manifest path; files staged. Operator runs by hand.>
