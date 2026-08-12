# open_questions.md — Phase 0

Session: 2026-08-12. Discipline: SIARC/AEAL epistemic partition.

Every item below is an **OPERATOR-SUPPLY** request. Per Hard Rule 1 and 2, no
numerical constant, theorem statement, or paper result has been written here
from memory. Where a value would normally be quoted, this document states
**what is needed and in what form**, and nothing else. Anything the operator
supplies will enter the ledger tagged `STRUCTURAL` (cited theorem the operator
has confirmed), never `PROVEN` or `VERIFIED`.

Requests are phrased so that they can be answered with a citation plus a
verbatim statement. Please do not paraphrase the source — paraphrase is where
normalisation conventions get silently dropped, and every one of the items
below is convention-sensitive.

---

## Blocking for Phase 0 closure

### OS-1 — Reference for the sine-kernel (Dyson) constant
**Status: blocks upgrading the Phase 0.3 target from CONJECTURED to STRUCTURAL.**

The task statement supplied the candidate closed form

```
c  =  (1/12) log 2 + 3 zeta'(-1)
```

for the constant term in

```
log det(I - K_s)|_{L^2[-1,1]},   K_s(x,y) = sin(s(x-y)) / (pi (x-y)),
     = a s^2 + b log s + c + O(1/s).
```

This session VERIFIED numerically that `a = -1/2`, `b = -1/4`, and that `c`
agrees with the candidate to the digit count recorded in `ledger.md`. The
identification is nonetheless tagged CONJECTURED because it entered the
session from the prompt, not from a source the session can inspect.

Needed:
1. The bibliographic reference(s) the operator wishes to stand behind
   (attribution given in the task was Dyson / Widom for the identification,
   with rigorous proof due to Krasovsky and to Deift–Its–Krasovsky).
2. The **verbatim theorem statement**, including which interval and which
   kernel normalisation `s` refers to. This matters concretely: the same
   determinant is variously parametrised by the half-length, the full length,
   or the length in units of the mean spacing, and these differ by terms of
   the form `(1/4) log 2`, which is exactly the size of the constant in
   question.
3. Confirmation of whether the `O(1/s)` remainder is known to be a genuine
   asymptotic expansion in `1/s^2` with no odd powers. This session found the
   odd coefficients numerically consistent with zero and the first even one
   equal to `1/32` to the precision available, but that is CONJECTURED.

---

## Needed to begin Phase 1

### OS-2 — Fisher–Hartwig prefactor, exact statement
Needed: the verbatim statement of the (generalised) Fisher–Hartwig asymptotic
formula for Toeplitz determinants `D_n(f)` with symbol carrying both jump and
root-type singularities, in the operator's preferred normalisation. Please
include:
- the precise symbol class and the branch convention for the `beta_j`
  exponents (the `beta_j -> beta_j + integer` ambiguity is the whole content
  of the *generalised* conjecture, and a wrong branch is not detectable
  numerically at low precision);
- the prefactor in terms of the Barnes `G`-function, stated explicitly rather
  than as "the usual Barnes factor";
- which normalisation of `G` is intended (see OS-6);
- the error term and, if known, whether it is uniform in the singularity
  positions;
- whether the operator wants the Szegő–Widom constant `E(f)` in the
  exponential-of-sum form or the Fredholm-determinant form.

### OS-3 — Jin–Korepin XX-chain additive constant
Needed: the verbatim statement of the large-block asymptotics of the Rényi and
von Neumann entanglement entropy for the XX spin chain in the form the
operator wishes to target, specifically:
- the coefficient of `log L` and the **additive constant**, as an expression,
  not a number;
- the definition of the block, the filling / Fermi momentum convention, and
  whether the chain is at half filling;
- the Rényi index convention (`alpha` vs `n`, and whether `S_1` is the
  `alpha -> 1` limit or defined separately);
- the stated error term;
- **the precision to which the constant is given in the source, and how it was
  obtained there** (closed form, numerics, or fit). Phase 1's premise is that
  some of these are low-precision or of unclear provenance; the session cannot
  assess that without knowing what the source actually claims.

### OS-4 — Emptiness formation probability constants
Needed, for whichever model the operator wants targeted (XX free-fermion point
and/or XXZ in a specified regime):
- the verbatim asymptotic form of the EFP `P(n)` including the Gaussian,
  power-law and constant factors;
- the definition of `n` and the normalisation of the ground state;
- the closed form of the constant if one is claimed, together with its
  attribution;
- if only a numerical value is available, the value **with its stated
  uncertainty and the method used**, so that this session can decide whether
  it is a target worth re-deriving.

### OS-5 — Which Phase 1 target is primary
Phase 1 was described as targeting constants "where the literature value is
low-precision or provenance-unclear". Needed: the operator's ranked choice of
target, since the pipeline extensions differ substantially —
- Toeplitz with FH singularities needs a symbol-evaluation and
  Toeplitz-determinant path (not the Nyström path built here);
- EFP and XX entropy need a different kernel discretisation;
- a continuum Fredholm target reuses the Phase 0 machinery almost unchanged.

### OS-6 — Barnes G normalisation
Needed: confirmation of the intended normalisation/functional equation for the
Barnes `G`-function and, if used, for the Glaisher–Kinkelin constant, so that
the session computes the same object as the source. The session can compute
either once told which. (Note: this session used `zeta'(-1)` computed directly
by mpmath and cross-checked it against mpmath's Glaisher constant; that check
is internal consistency, not agreement with any source's convention.)

### OS-7 — Acceptance standard for a Phase 1 claim
Needed: the operator's declared standard for what counts as "beating" a
literature value — e.g. digit count, agreement window, whether a PSLQ
identification with passing null controls is acceptable as a *claim* or only
as a *conjecture*. Phase 0 deliberately does not decide this.

---

## Internal open questions (no operator input required, recorded for honesty)

### IQ-1 — Truncation floor of the order sweep
The order sweep's successive differences stop improving at a level set by the
growth of the asymptotic coefficients `e_m` and by the smallest `s` in the fit
window. The observed growth is consistent with factorial-type growth but the
session has not derived the growth rate, so the optimal `(K, s_min)` trade-off
is chosen empirically, not optimally. CONJECTURED: `e_{m+1}/e_m` grows roughly
linearly in `m`.

### IQ-2 — Even-only correction series
The unrestricted fit gives odd coefficients small compared with even ones, and
`e_1` numerically equal to `1/32`. Both are CONJECTURED. See OS-1 item 3.

### IQ-3 — Digit-loss law
The measured arithmetic digit loss is `0.866 * s`, i.e. `2s/ln 10`,
consistent with a condition number growing like `exp(2s)`. This is VERIFIED as
a measurement over the swept range but the exponent `2` is not derived here;
it is CONJECTURED that it reflects `1 - lambda_max(K_s) ~ exp(-2s)`.

### IQ-4 — Basis overcompleteness
Whether the Phase 0.4 eight-element basis is usable at the precision this
pipeline delivers is determined empirically by the measured spurious-relation
threshold recorded in `ledger.md`. If Phase 1 wants a larger basis, the
precision requirement grows roughly linearly in the basis size, and the
pipeline cost grows steeply because the arithmetic digit loss is linear in `s`
while the truncation floor improves only slowly with `s`.

---

## Revision after the revision-3 grid (appended, nothing above removed)

### OS-8 — Declared precision budget for Phase 1 identifications
Phase 0 measured, rather than assumed, what precision an integer-relation
claim actually costs. For a basis B with measured spurious-relation threshold
`T(B)`, a relation satisfying the Phase 0.4 criteria requires the target
constant to be known to

```
D  >=  max( T(B),  20 + GUARD + log10|target| )  +  30  +  margin
```

digits, where `GUARD` is the harness's tolerance guard (8 here) and the `20`
is the null-control perturbation exponent. Measured thresholds were
`T = 25, 30, ~50` for bases of 3, 4 and 8 elements at `maxcoeff = 1e4`.

Needed from the operator: confirmation that this is the standard Phase 1 will
be held to, since it sets the compute budget. Concretely, an 8-element basis
needs ~83 honest digits in the target, and for this pipeline the cost of
honest digits is set by asymptotic-series truncation, not by arithmetic — see
IQ-1. If the operator wants an 8-element basis in Phase 1, the target must
admit either much larger `s` or a convergent (not asymptotic) representation.

### IQ-1 (updated) — the sweep is order-limited, not s_min-limited
Directly tested this session by refitting on `s >= s_min` for increasing
`s_min`: the result got monotonically WORSE, because `K` is capped at
`(points - 4)` and dropping low-s points destroys orders faster than it
improves per-order truncation. So within the range reachable here the binding
resource is the number of grid points, and the `(K, s_min)` trade-off is not
in the regime where the asymptotic-coefficient growth rate matters. The growth
rate of `e_m` remains underived and is still CONJECTURED. Note this also means
the session has never observed the true optimal-truncation floor at any
`s_min`, so nothing is known about where it lies.

### IQ-5 — Certification level feeds back into the extraction rate
Raising the per-point certification from ~99 to ~166 digits did not merely
lower the data-noise term E3 (which fell 85 digits below the binding term). It
raised the rate at which additional correction orders convert into digits of
`c`, from ~0.07 to ~0.26 digits per order, because orders whose contribution
had been sitting below the old noise floor became usable. CONJECTURED that
this saturates once E3 is well below E1; not tested.

### IQ-6 — Two protocol bugs found by adversarial controls, not by tests
Both are recorded in the ledger (L-012, L-018). Both would have produced a
confident wrong verdict rather than an obvious failure:
1. a spurious-relation threshold read from below returns the precision at
   which PSLQ merely fails to converge;
2. a null control run below its own resolution "fails" for reasons unrelated
   to the hypothesis it is supposed to test.
Recorded here because the same two failure modes will recur in Phase 1 with a
different basis and a different target, and neither is detectable from the
output of a single run.

---

# REVISION 3 — after operator message discharging OS-1 (2026-08-12)

## OS-1 — DISCHARGED. See ledger L-026.

The operator supplied the attribution, and this session verified it against
primary text (arXiv API records; PDFs fetched and text-extracted locally).
Both Krasovsky (arXiv:math/0401258v2) and Ehrhardt (arXiv:math/0401205v2)
were quoted verbatim in L-026, the normalisation was checked term by term and
matches this session's convention exactly, and the target form is upgraded
CONJECTURED -> STRUCTURAL.

Residual items from the discharge, NOT blocking:
  * The operator cited Krasovsky as "CMP 262, 2006"; the arXiv record gives
    Int. Math. Res. Not. 2004, no. 25, 1249-1272. The mathematics is
    confirmed, the citation is not. Which does the operator wish to stand
    behind?
  * "Deift-Its-Krasovsky" as a third independent proof was not confirmed by
    either primary consulted. Reference requested if it is to be cited.
  * Ehrhardt's venue ("CMP 272, 2007") is uncontradicted but unconfirmed (no
    journal_ref in the arXiv record).

## OS-9 — Explicit higher-order coefficients of the sine-kernel expansion

**Status: would remove E1 as the binding error term, IF the answer is a
recursion rather than a finite list.**

Ehrhardt's abstract states that "higher order asymptotics have also been
determined", so explicit coefficients exist in the literature. What is needed
is the coefficients themselves, in closed form, for

```
log det(I - K_s) = -s^2/2 - (1/4) log s + c + sum_{m>=1} e_m s^(-2m).
```

IMPORTANT QUALIFICATION, so that this is not over-valued. The current fit
already annihilates s^-2 ... s^-272 numerically (K = 136, even-only; L-029).
Supplying the first few `e_m` in closed form would therefore save a handful of
orders out of 136 and is worth almost nothing. This item is only valuable if
what is available is a **recursion or generating function for all m**, which
would let the tail be subtracted exactly instead of extrapolated.

State which of the two is available. A finite list of the first few
coefficients should be marked as such, and this item closed as low-value.

## OS-10 — Provenance columns for the Phase 1 triage table

`phase1_triage.md` cannot be completed in-session. For each of the Fisher-
Hartwig prefactor, the Jin-Korepin XX-chain additive constant, and the
emptiness-formation-probability constant, the following are needed BEFORE
target selection:
  * how many digits the published value carries;
  * whether the published value is proved, derived non-rigorously, or
    conjectured;
  * whether an independent second derivation exists;
  * which constants the operator expects to appear in the closed form (this
    fixes the basis size b, hence the required D via T(b) = 5b + 10).

State what is needed, not what the value is believed to be.

---

## IQ-7 — Can the Painleve V representation generate the tail exactly?

**Internal. This is the strongest available lever on E1 and it is untested.**

Both primaries consulted in L-026 record (Ehrhardt, verbatim) that "Jimbo,
Miwa, Mori and Sato showed that the function sigma(alpha) = alpha d/dalpha
log det(I - K_alpha)" satisfies an ODE of Painleve V type. If that ODE admits
a formal large-alpha series solution, its coefficients satisfy a RECURSION,
and the entire correction tail becomes available in closed form to arbitrary
order.

That would change the character of the extraction completely: the correction
series would be SUBTRACTED exactly rather than fitted, `e_m` would stop being
nuisance parameters, and E1 — currently the binding budget line at 1.41e-72 —
would be replaced by an error controlled only by where the asymptotic series
is truncated at optimal order.

It would also settle IQ-2 (`e_1 = 1/32`, currently CONJECTURED from the
numerical fit) by derivation rather than by pattern, which would make it the
session's first PROVEN coefficient.

Not attempted here: deriving and verifying the recursion is a piece of
symbolic work with its own failure modes, and Phase 0 is closed. Flagged as
the first thing to try if Phase 1 is digit-starved.

## IQ-8 — Two sources of truth for the grid

`build_grid.BLOCKS` and `out/certified_data.json` independently encode the
grid, and they silently diverged once already (L-025). A regression test now
makes the divergence loud (`test_smoke.test_grid_spec_matches_data`), but the
duplication itself remains. The structurally correct fix is for one to be
derived from the other. Deferred, not solved.
