<!--
PROVENANCE NOTE (read before relying on this file):
This is the Task 04 SPECIFICATION as handed to the agent -- the record of what was
*specified*, not what *happened*. Saved to disk (per the Task 03 audit-trail lesson:
the executed task's authority must not live only in chat). The agent's final report
is the authority for what actually occurred. Do NOT treat this spec as a substitute
for the run report.
-->

# TASK 04: Cap-sets evaluator shakedown (local-only, replicate known dimensions)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. First task in a NEW domain
> (cap sets in AG(n,3)), reusing the validated pipeline from Tasks 02–03.
>
> SUBSTRATE DECISION (operator, grounded in measured host facts): **local-only.**
> Host is CPU-only, 16 GB RAM, no usable GPU → permanently capped at ~7B, which
> Task 03 proved is too weak to mutate code for discovery. Therefore Task 04 is
> **explicitly a SHAKEDOWN, not a discovery run**: it validates the cap-sets
> evaluator and the search wiring in a new domain by replicating KNOWN-EXACT
> maximal cap sizes. It is NOT expected to discover anything, and must not be
> labelled or reported as if it did.
>
> All prior hard rules bind: container isolation, ground-truth + transcription
> gate, independent evaluator, no commit/push without operator go-ahead, bounded
> budget, "could not confirm" required, null result = success.

---

## Pre-flight gates (do all, every run — not waived by prior success)

1. `docker run --rm hello-world` → Docker success message, else STOP.
2. host `curl http://localhost:11434/v1/models` → lists the model, else STOP.
3. container→host `docker run --rm curlimages/curl http://host.docker.internal:11434/v1/models`
   → returns the model list from inside a container, else STOP.

Same local Ollama substrate as Task 03 (qwen2.5-coder:7b via
host.docker.internal:11434/v1, dummy api_key "ollama", not a secret).

## The domain (precise definitions — do NOT reconstruct from memory)

- A **cap** in AG(n,3) = (ℤ/3ℤ)ⁿ = a set of points with **no three collinear**.
- Over ℤ/3ℤ, three DISTINCT points a, b, c are collinear **iff**
  `a + b + c ≡ 0 (mod 3)` componentwise. Equivalently, for any two distinct
  points a, b the unique third point completing the line is `c = (−a − b) mod 3`
  ` = (2a + 2b) mod 3`. A set is a cap iff for every pair a≠b in the set, that
  third point c is NOT also in the set (when c ∉ {a,b}).
- Cap size = number of points. The cap-set problem asks the MAX size.

## Ground truth — verified known-EXACT maximal cap sizes (transcription gate)

The cap-set problem is solved for n ≤ 6. Maximal cap size by dimension:

| n | max cap size |
|---|---|
| 1 | 2 |
| 2 | 4 |
| 3 | **9** |
| 4 | **20** |
| 5 | 45 |
| 6 | 112 |

**Transcription gate / known trap:** the AG(4,3) maximal cap is **20**, NOT 18.
(Some literature counts "size-18 caps up to isomorphism" — a DIFFERENT quantity;
do not mistake it for the maximum.) Confirm n=3→9 and n=4→20 before relying on
this table; if your notes say otherwise, STOP and re-read.

## Scope — do exactly this

1. **Write the independent cap-sets evaluator** (`cap_set_evaluator.py`, SEPARATE
   from any evolved program), taking n and a list of points in (ℤ/3ℤ)ⁿ and:
   - validates each point is in {0,1,2}ⁿ with correct length n;
   - checks the cap property via the `a+b+c ≡ 0 mod 3` test;
   - reports: is_valid_cap (bool), size, and on failure the first violating triple.
   **Self-test it** before any search. Required self-test cases:
     - a known 9-cap in AG(3,3) → valid, size 9;
     - that same set plus a point that completes a line → INVALID, names the triple;
     - the full AG(2,3) space (all 9 points) → INVALID;
     - a known 4-cap in AG(2,3) → valid, size 4.
   Report `SELFTEST PASS/FAIL` with the cases.

2. **Set up the OpenEvolve cap-sets example** targeting **n=3 then n=4**. Seed may
   be a trivial/greedy cap constructor; evolved program proposes larger caps;
   in-container evaluator scores = cap size if valid, else 0.

3. **Run inside the container** at a BOUNDED budget (operator default: **50
   iterations per dimension**, n=3 and n=4). State actual iterations/wall-clock.

4. **Independently evaluate** the best cap per dimension with
   `cap_set_evaluator.py`; save each best cap to a file; confirm the evaluator
   passes it standalone.

## OUT OF SCOPE — do NOT attempt

- NOT a discovery run. Do NOT target n=5 or n=6 as pass conditions (n=5 MAY be
  attempted as a stretch and is ALLOWED to fall short). NEVER imply a discovery.
- Do NOT claim any result above a known maximum. Exceeding a proven exact maximum
  is impossible → it can ONLY be an evaluator defect; treat as a bug, STOP, report.
- Do NOT edit the evaluator to make a set pass.
- No host execution of evolved code. No hosted-API fallback (local-only task).
- No optimality proof, no Lean. VERIFIED witnesses only.
- No commit/push/tag/move/delete. Prepare to ready-state and STOP.

## A null result is a COMPLETE, SUCCESSFUL answer

Pass condition: the evaluator self-tests pass, AND the search reaches the known
maximum for n=3 (9) and n=4 (20) — OR, if it falls short, the run completed
end-to-end and the evaluator correctly scored what was found. "Reached 9 and 20"
validates the new-domain pipeline; "reached 9 but only 16 at n=4 in 50 iters on a
weak model" is ALSO a successful shakedown. Do not extend budget or tweak the
evaluator to hit a number.

## Sandbox / file-ops rules

Container-only execution. Copy-first for any file op; SHA-256 every saved
artifact; originals stay. Vendored clone and outputs remain git-ignored.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>
**Pre-flight gates this session:** docker / host-curl / container→host — <pass/fail each>
**Evaluator self-test:** `cap_set_evaluator.py` SELFTEST <PASS/FAIL> + the four cases.
**Domain check:** cap test = `a+b+c ≡ 0 mod 3`. Transcription gate: n=3→9, n=4→20 (NOT 18).
**Container / provenance:** OpenEvolve @80945ed in pinned image (digest 93ab4b7f…); local qwen2.5-coder:7b via host.docker.internal.
**Result (per dimension):** n=3 vs 9; n=4 vs 20; (n=5 only if stretch); evaluator agreed valid.
**Sandbox confirmation:** evolved code ran ONLY in container.
**Lean / axiom cones:** N/A — VERIFIED domain, not PROVEN.
**Honest claim (one sentence).**
**What I could NOT confirm (REQUIRED — never empty).**
**Ready-but-not-done (awaiting operator):** exact git add/commit; staged files; operator runs by hand.
