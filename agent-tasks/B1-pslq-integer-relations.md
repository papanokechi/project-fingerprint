# TASK B1: PSLQ integer-relation search — pillar shakedown (local-only)

> Filled-in instance of `agent-tasks/TEMPLATE.md`. Opens **Pillar B**
> (integer-relation discovery, Ramanujan-Machine lineage), distinct from the
> OpenEvolve pillar. Here the SEARCH is a deterministic algorithm (PSLQ); the LLM
> only proposes which constants to test. Output class is **CONJECTURED** — a
> relation PSLQ returns is a high-precision numerical coincidence, NOT a theorem,
> until separately proven (potentially via Pillar C / Lean).
>
> Substrate: **local-only, full strength.** Unlike cap-sets, this pillar is NOT
> hardware-capped — mpmath + PSLQ are CPU-fine and do the real work; the weak 7B
> only suggests constant-sets, which it can do adequately. No hosted provider.
>
> All standard rules bind: bounded scope, ground-truth + transcription gate,
> independent re-verification, no commit/push without go-ahead, "could not
> confirm" required, null result = success.

---

## The method, stated precisely (do NOT reconstruct from memory)

- API: `mpmath.pslq(x, tol=None, maxcoeff=1000, maxsteps=100)`. Given a real
  vector `x = [x_0,…,x_n]`, finds integers `[c_0,…,c_n]` with
  `|c_0 x_0 + … + c_n x_n| < tol` and `max|c_k| < maxcoeff`; returns `None` if
  none found. Default tol = 3/4 of working precision.
- PSLQ finds **linear** relations among the supplied numbers. Any transcendental
  constants (π, e, ζ(3), …) must be supplied explicitly by the operator/LLM —
  PSLQ does not invent them. (Nonlinear relations only via supplying products/
  powers as additional basis entries.)

## THE central failure mode — false positives from low precision

PSLQ will return a "relation" that is merely a low-accuracy approximation if
precision/tolerance are loose. Canonical illustration: `pslq([-1, pi], tol=0.01)`
→ `[22,7]`; `tol=0.001` → `[355,113]`. Both are FALSE as exact relations — they
are just good rational approximations to π. A returned coefficient vector is
**meaningless without a precision/tolerance justification.**

**Precision floor (Bailey's rule — enforce it):** to trust a relation with
coefficients bounded by G among an n-entry vector, the inputs must be computed to
at least **n · log₁₀(G)** decimal digits, with comfortable margin. A relation
found at precision below this floor is NOT a finding — it is a candidate to
re-test at higher precision.

## Scope — do exactly this

1. **Write the PSLQ harness** (`pslq_search.py`) that, given a named constant
   basis and parameters, computes each constant to a stated `mp.dps`, runs
   `mpmath.pslq`, and reports the coefficient vector (or None) ALONGSIDE:
   the working precision, tol, maxcoeff, and the Bailey floor n·log₁₀(maxcoeff)
   for comparison. It must refuse to report a relation as a candidate unless the
   working precision exceeds the Bailey floor by a stated margin.

2. **Reproduce a KNOWN relation first** (the shakedown gate — this pillar's n=26).
   Use a textbook-true integer relation as the self-test, e.g.:
   - `pslq([sqrt(n) for n in range(2,9)])` → should return `[2,0,0,0,0,0,-1]`
     (i.e. 2·√2 = √8), per mpmath docs;
   - and the deliberate FALSE-POSITIVE check: confirm the harness FLAGS
     `pslq([-1, pi], tol=0.01) → [22,7]` as below-floor / not a real relation.
   Report `SELFTEST PASS/FAIL` with both: it must accept the true relation AND
   reject the π/22-7 false positive.

3. **LLM proposes constant bases to explore** (the only LLM role; local 7B is
   adequate). For each proposed basis, run the harness at high precision
   (e.g. mp.dps ≥ 100, stated), with strict tol. Keep a log of bases tried and
   outcomes. **A basis returning None is a COMPLETE, SUCCESSFUL result** ("no
   relation among these to this precision/maxcoeff") — do not loosen tol or
   lower precision to manufacture a hit.

4. **Re-verify any candidate relation at HIGHER precision** before reporting it.
   A relation real at dps=100 must survive dps=200 (and ideally dps=400) with the
   same small coefficients. A relation that vanishes when precision increases was
   a false positive — report it as such, not as a find. Save each surviving
   candidate (basis, coefficients, precisions tested) with SHA-256.

## OUT OF SCOPE — do NOT attempt

- Do NOT report any relation as PROVEN or as a theorem. PSLQ output is
  **CONJECTURED** — a numerical coincidence pending proof. Proving it is a
  separate Pillar-C/Lean task, out of scope here.
- Do NOT loosen tol or lower precision to produce a relation. Do NOT raise
  maxcoeff to fish for large-coefficient "relations" (large coefficients are the
  signal NO clean relation exists — see the method note).
- Do NOT claim novelty. A found relation may be well-known (e.g. a Machin-like
  formula). Report it as "found; novelty UNVERIFIED" — checking novelty against
  literature is a separate step.
- Do NOT edit the harness to make a candidate pass the floor.
- No hosted provider (local-only). No commit/push/tag/move/delete — ready-state
  and STOP.

## Ground truth / transcription gate

- `mpmath.pslq` returns None when no relation exists within (tol, maxcoeff). 
- True self-test relation: 2√2 − √8 = 0 → `[2,0,0,0,0,0,-1]` for the
  range(2,9) sqrt vector.
- False positive to REJECT: `[22,7]` / `[355,113]` for `[-1, pi]` at loose tol.
- Bailey floor: digits ≥ n·log₁₀(maxcoeff).
Confirm these before relying; if your notes differ, STOP and re-read.

---

## REQUIRED FINAL REPORT (fill every field)

**What I did:** <bounded summary>

**Harness self-test:** `pslq_search.py` SELFTEST <PASS/FAIL> — accepted true
2√2=√8 relation AND rejected the π/22-7 false positive: <both shown>.

**Method confirmation:** mpmath.pslq signature used; working precision (mp.dps)
per run; tol; maxcoeff; Bailey floor n·log₁₀(maxcoeff) and margin.

**Bases explored:** <list of constant-sets tried, LLM-proposed; each → relation
or None, with the precision/tol used>.

**Candidate relations (if any):**
- basis · coefficient vector · precisions tested (dps=100/200/400) · survived? ·
  saved path + SHA-256.
- For each: explicit "CONJECTURED — numerical coincidence to <N> digits, NOT
  proven; novelty UNVERIFIED."
- If NONE survived higher-precision re-test: say so plainly — a clean,
  successful null.

**Lean / axiom cones:** N/A — PSLQ yields CONJECTURED, never PROVEN. (A surviving
candidate is a CANDIDATE for a future Pillar-C proof task.)

**Honest claim (one sentence):**
<e.g. "PSLQ pillar validated: harness accepts a known relation and rejects the
classic π false positive; explored K bases at dps≥100; found J candidate
relations surviving to dps=400, all labelled CONJECTURED + novelty-unverified
(or: found none — a clean null).">

**What I could NOT confirm (REQUIRED — never empty):**
<novelty of any candidate vs literature; whether higher precision than tested
would dissolve a candidate; whether the constant bases are interesting vs
arbitrary; any value not independently recomputed.>

**Ready-but-not-done (awaiting operator):**
<git add/commit for pslq_search.py, the bases log, surviving candidates +
SHA-256; manifest path. Save agent-tasks/B1-…md to disk (audit trail). Operator
runs by hand.>
