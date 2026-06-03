<!--
PROVENANCE NOTE (read before relying on this file):
This is the Task 03 SPECIFICATION as drafted and handed to the agent — the record
of what was *specified*, not what *happened*. It was reconstructed to disk after
execution because the original lived only in the chat transcript (a §5 gap: the
task that actually ran had the weakest paper trail). The agent's final report is
the authority for what *actually occurred*; this file is the authority for what was
*asked*. They agree for this run (same OpenEvolve SHA 80945ed, same
host.docker.internal endpoint, same model qwen2.5-coder:7b, same 100-iter budget).
Do NOT treat this spec as a substitute for the run report.
-->

# TASK 03: Local provider wiring + build + run (resume of Task 02)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. Resumes
> `agent-tasks/02-containerized-circle-packing.md` with the LLM-provider gate now
> answered: **local Ollama server, OpenAI-compatible endpoint.** All Task 01/02
> rules still bind (pipeline-not-record, independent evaluator, ground-truth +
> transcription gate, container isolation, no commit/push without operator
> go-ahead, no secrets committed).
>
> Operator has completed the two by-hand prerequisites: installed Ollama for
> Windows and pulled the model. Agent does everything from wiring onward.

---

## Pre-flight gates (do BOTH first, every run — not waived by prior success)

1. Docker isolation:
   ```
   docker run --rm hello-world
   ```
   Must print the Docker success message. Else STOP.

2. Local LLM server reachable FROM THE HOST:
   ```
   curl http://localhost:11434/v1/models
   ```
   Must return a model list including the target model. Else STOP and report —
   do not proceed, do not fall back to a hosted API or to host execution.

If either gate fails, STOP. Report which, and the exact output.

## CRITICAL networking note (the most likely failure)

OpenEvolve runs INSIDE the Docker container; Ollama runs on the Windows HOST.
Inside the container, `localhost` means the container, NOT the host. The
OpenEvolve config MUST reach Ollama at:

```
api_base: "http://host.docker.internal:11434/v1"
```

NOT `http://localhost:11434/v1`. A localhost config will connect fine when tested
bare on the host and then silently fail from inside the container. Verify the
container can actually reach the host endpoint before running the search:

```
docker run --rm curlimages/curl http://host.docker.internal:11434/v1/models
```

This must return the model list from inside a container. If it does not, STOP —
the run cannot work until it does. (On Docker Desktop host.docker.internal is
provided automatically; on plain Linux it may need
`--add-host=host.docker.internal:host-gateway`.)

## Scope — do exactly this

1. **Provider config.** Configure OpenEvolve to use the local endpoint:
   - `api_base: "http://host.docker.internal:11434/v1"`
   - `model: "qwen2.5-coder:7b"` (operator default; if the host's
     `/v1/models` shows a different name, use the exact string it reports and
     note the substitution).
   - `api_key`: a dummy value (e.g. `"ollama"`) — required but unused by Ollama.
     This is NOT a secret; it may appear in config. (There is no real key to
     protect in the local path.)

2. **Build the pinned container** from the Task 02 Dockerfile
   (`containers/circle-packing/Dockerfile`, base
   `python:3.12-slim-bookworm@sha256:93ab4b7f…`, OpenEvolve @
   `80945ed82886d5c4ff2f3d22436765d50cb61266`). Capture the frozen dependency
   lock the Dockerfile generates. If the build fails, report the error and STOP
   — do not patch the pin to force it without flagging the change.

3. **Run the n=26 circle-packing search** inside the container at a BOUNDED
   budget (operator default below; do not exceed without go-ahead):
   - **Budget: 100 iterations** (shakedown — enough to prove the loop turns,
     not a record attempt). State actual iterations/wall-clock in the report.
   - The search runs in-container; Ollama is reached via host.docker.internal;
     output is written to a mounted `/work/output` dir the host can read.

4. **Independently evaluate** the best configuration with the Task 02
   `independent_evaluator.py` (already self-tested). Save the best config to a
   file and confirm the evaluator passes it standalone (so it is re-checkable
   without re-running the search).

## OUT OF SCOPE — do NOT attempt

- No record-chasing. Success = a VALID config (independent evaluator passes),
  ideally near 2.634–2.635, at the stated budget. A low number at 100 iters is
  still a successful shakedown. A number > 2.63591551 → suspicion + operator
  scrutiny, never a headline.
- No raising the budget mid-run to reach a figure.
- No optimality proof, no Lean. VERIFIED witnesses only.
- No editing the independent evaluator to make a config pass.
- No host execution of evolved code. No hosted-API fallback.
- No commit/push/tag/move/delete. Prepare to ready-state and STOP.

## Ground truth (use, do NOT reconstruct)

n=26 sum-of-radii unit square: prior **2.634** / AlphaEvolve **~2.635** / FICO
**2.63591551** / community OpenEvolve **~2.635977** (validity unconfirmed).
Transcription gate: confirm 2.634 / 2.635 / 2.63591551 before relying; else STOP.

## A null result is a COMPLETE, SUCCESSFUL answer

"100 iterations, local qwen2.5-coder:7b, best VALID config = Y (evaluator
confirmed), below 2.635 reference" fully validates the pipeline. The end-to-end
chain turning inside the container against a local model is the deliverable.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>

**Pre-flight gates this session:**
- `docker run --rm hello-world`: <pass/fail>
- host `curl …/v1/models`: <pass/fail + models listed>
- container→host `host.docker.internal …/v1/models`: <pass/fail>

**Provider config (REQUIRED):**
- api_base used: <http://host.docker.internal:11434/v1>
- model string used (exact): <...>
- confirmed NOT localhost inside container: <yes>

**OpenEvolve provenance + container (REQUIRED):**
- Clone URL + SHA checked out: <…@80945ed…>
- Base image + digest: <python:3.12-slim-bookworm@sha256:93ab4b7f…>
- Dependency lock path (committed-ready): <...>
- Build result: <success / error text>
- One-command re-run invocation: <docker run … -v …:/work/output … >

**Sandbox confirmation (REQUIRED):**
- Evolved code ran ONLY in container: <yes — how verified>
- Host did only orchestration + read mounted output: <yes/no>

**Result:**
- Budget actually run: <iterations / wall-clock>
- Best VALID config sum of radii (INDEPENDENT evaluator): <Y>
- Saved config path (re-checkable standalone): <...>
- Reference comparison: <Y vs 2.635 / 2.634>
- Evaluator agreed valid: <yes/no + which checks>

**Lean / axiom cones:** N/A — VERIFIED domain, not PROVEN.

**Honest claim (one sentence):**
<"Pipeline validated end-to-end: OpenEvolve @80945ed in pinned container, local
qwen2.5-coder:7b via host.docker.internal, 100 iters → valid 26-circle config
scoring Y, independently confirmed; Y consistent-with/below 2.635 reference.">

**What I could NOT confirm (REQUIRED — never empty):**
<validity of community ~2.635977; whether 100 iters is representative; whether
operator wants a different model/budget/pin; any source not re-verified live.>

**Ready-but-not-done (awaiting operator confirmation):**
<exact git add/commit for: Dockerfile, requirements.lock, config.yaml (no secret),
independent_evaluator.py, saved best config, results summary; manifest path;
files staged. Operator runs by hand.>
