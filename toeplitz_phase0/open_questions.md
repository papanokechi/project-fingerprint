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

---

# STATUS UPDATE (this session, post-operator-message 2)

Append-only. Earlier entries above are left exactly as written.

## DISCHARGED

**IQ-2 (`e_1 = 1/32`) -- SETTLED BY DERIVATION.** In our indexing the
coefficient is `e_2`, and `e_2 = 1/32` exactly, from the recursion in L-037.
It was previously a numerical pattern; it is now derived from the ODE of
L-036, with exact rational arithmetic and two independent implementations
agreeing.

**IQ-7 (Painleve V / JMMS recursion) -- DISCHARGED, and it did not need the
literature.** The concern was that writing the sigma-form ODE from memory
violates HARD RULE 1. Resolved by DISCOVERING the ODE as a nullspace over our
own high-precision data (L-036) and confirming it out of sample. The
recursion then generated 200 exact even-order coefficients (m <= 400) in 70 s.
Result: c to 132 honest digits with no fit at all (L-038).

**OS-9 (higher-order asymptotic coefficients) -- NO LONGER NEEDED.** This
asked the operator for the explicit higher-order coefficients, with the
caveat that only a recursion would be worth having. We now generate them
ourselves to arbitrary order in exact rational arithmetic. **Please do not
spend effort sourcing this.** It is withdrawn as a request.

Note for the record: Ehrhardt's abstract does state that "higher order
asymptotics have also been determined" (L-035), so the literature values
exist; we simply no longer need them, and deriving them in-session is
strictly better than importing them, because an imported list would have been
CONJECTURED-from-recall while these are derived and independently checked
against certified data.

## STILL OPEN

**IQ-1 (growth of `e_m`) -- PARTIALLY ANSWERED, one piece left.** The measured
ratio implies optimal truncation at `m* ~ 2s`, confirmed at s=149 where the
code chose M* = 296 against a prediction of 298. What remains open is a
closed-form statement of the growth (the data is consistent with
`e_{m+2}/e_m ~ (m/2)^2`, which is CONJECTURED). Not blocking: the optimum is
located numerically per point and cross-checked between s values.

**IQ-3 (exponent 2 in the digit-loss law)** -- unchanged, and now much less
important, since the fit whose conditioning it described is no longer on the
critical path for c.

## NEW OPERATOR-SUPPLY ITEMS

**OS-11 -- Publication venues, and one author list.** Two specific gaps, both
now blocking nothing but both needed before any STRUCTURAL tag is final:

  (a) Ehrhardt, "Dyson's constant in the asymptotics of the Fredholm
      determinant of the sine kernel". arXiv:math/0401205 carries NO
      `journal_ref`. Two different venues have been suggested to me across
      two messages (CMP 272 (2007), then CMP 262 (2006) 317-341). I cannot
      confirm either from a primary source. What is the published venue?

  (b) The fourth/third proof. Krasovsky's own footnote 1 announces "A third
      solution to the problem by a Riemann-Hilbert approach ... is in
      preparation by P. Deift, A. Its, and X. Zhou" -- THREE authors, not
      including Krasovsky. A four-author paper (Deift, Its, Krasovsky, Zhou,
      JCAM 202(1) 26-47, 2007) has been suggested to me. Author lists can
      change between announcement and publication, so both may be correct.
      What is the published author list and venue?

  I state what I need, not what I think the value is: I have no independent
  access to either and four arXiv query forms for the title returned nothing.

**OS-12 -- Is the sigma-form ODE of L-036 the known JMMS/Painleve-V equation
in our normalisation?** We derived `s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2 = 0`
with `u = s sigma' - sigma`, for `sigma = s (log det)'` with the kernel
`sin(s(x-y))/(pi(x-y))` on `[-1,1]`. We do NOT need this answered -- the
relation is independently verified to 79 digits out of sample and the
downstream results do not depend on its provenance. It is worth asking only
because a mismatch would be interesting: if the standard form differs by
more than a rescaling, one of the two is wrong about something.


---

# Revision 5 (appended after operator message 4; nothing above removed)

## OS-11 — DISCHARGED. See ledger L-043.

Two distinct Ehrhardt papers, not two venues for one paper: "Dyson's constant"
(singular, sine kernel, math/0401205, CMP 262 (2006) 317-341) and "Dyson's
constants" (plural, Wiener-Hopf-Hankel, math/0605003, CMP 272 (2007) 683-698).
The apparent conflict in L-035 was mine to create by assuming one paper.

Fourth proof: Krasovsky's footnote announces Deift-Its-Zhou; the published
paper is Deift-Its-Krasovsky-Zhou, JCAM 202(1) 26-47 (2007). Both readings
correct, about different objects.

Remains STRUCTURAL: I have read neither the plural-title paper nor the JCAM
paper. Not upgradeable without primaries, and nothing depends on it.

## OS-12 — DISCHARGED. See ledger L-042.

The discovered ODE is JMMS sigma-PV in x = 2s. Derived lambda = 2 myself from
the coefficient ratio 16 = 4 lambda^2; confirmed symbolically (difference
exactly 0) and numerically (standard form holds on my data to 71 digits).

The identification with the PUBLISHED JMMS equation remains operator-sourced.
Since c now flows through this ODE, that residual is load-bearing:

  **OS-13 (NEW, load-bearing) — primary source for the sigma-form Painleve V.**
  I need the sigma (Hirota) form of PV as it appears in a primary source
  (Jimbo-Miwa-Okamoto, or Jimbo-Miwa-Mori-Sato for the sine-kernel case),
  with the boundary condition, in a stated variable convention. What I need
  is the EQUATION AS PRINTED and where, not a confirmation that mine matches.
  Until then the derivation chain for the 132-digit c is
  VERIFIED-with-a-STRUCTURAL-joint, not fully STRUCTURAL.

## OS-9 — remains WITHDRAWN, and L-042 explains why more sharply

Now that the recursion generates coefficients to arbitrary order in exact
rational arithmetic (M=400 in 70 s), a literature-supplied handful of e_m has
no value at all. The recursion is the deliverable, as the operator argued.

## Note on the "positive controls" hardening item

Implemented, TESTED AGAINST THE ACTUAL FAILURE, and found not to work as the
operator described it. See L-044. The corrected version (plant over the
DECLARED basis, search over the ACTUAL one) does fire. No operator input
needed; recorded here because the operator proposed the mechanism and should
see the measurement rather than an acknowledgement.

## PRE-REGISTERED PREDICTION (recorded BEFORE the measurement)

Operator's law, from m* ~ 2s implying a beyond-all-orders residual of order
e^(-2s):

    digits ~= 2s / ln 10 ~= 0.869 s

Measured anchor: s = 149 gave 132.09 against a predicted 129.4 (excess 2.7,
consistent with an algebraic prefactor).

Predictions, fixed now:
    s = 200  ->  ~173.8 + prefactor excess   (expect ~176)
    s = 250  ->  ~217.3 + prefactor excess   (expect ~220)

Falsification condition, also fixed now: if the achieved digit count comes in
FLAT (i.e. near 132) rather than scaling, the binding constraint is Nystrom
evaluation rather than series truncation, and the fix is a different one.

This is recorded before the numbers are in specifically because a law fitted
after the fact would be unfalsifiable, and this session has already produced
one fabricated law (L-030).

---

## OS-10 — PARTIALLY DISCHARGED. Schema supplied; cells still empty.

The six provenance columns are now written into `phase1_triage.md` section 4
and the candidate list into section 5. The SCHEMA is discharged. The CELLS
are not, and cannot be discharged by us: P1-P4 are all statements about the
literature, so HARD RULE 2 makes every value we could supply CONJECTURED.

The one column we can fill ourselves is P5 (recomputability), because that is
a question about our own pipeline, not about a paper.

What remains needed, per selected candidate, from a PRIMARY source:
  - the digit string ACTUALLY PRINTED (P1) — not "known to high precision"
  - whether the printed digits came from a method other than the derivation
    they appear in (P3) — this is the column most often absent, and its
    absence should be recorded as "unknown", never as "no"
  - whether the normalisation appears in the BODY (P4)

## OS-13 — STILL OPEN at the primary level

**Status: the sigma-form of Painleve V for the sine-kernel determinant.**

Two renderings have now been supplied, and they DISAGREE IN SIGN on the cross
term. Both are by the same author and both are SECONDARY, citing JMMS 1980
(Physica D 1, 80-158):

  (P) arXiv:0804.2543:  x^2 s''^2 + 4u^2 + 4u s'^2 = 0, sigma ~ -x/pi - x^2/pi^2,
                        det = exp(+int sigma/x dx)
  (M) arXiv:0904.1581:  x^2 s''^2 + 4u^2 - 4u s'^2 = 0, sigma ~ +x/pi + x^2/pi^2,
                        det = exp(-int sigma/x dx)

These are sigma -> -sigma images of one another, each internally consistent
(L-051). WE HAVE ADJUDICATED WHICH APPLIES TO OUR CONVENTION FROM OUR OWN
DATA — sigma < 0 near the origin, so (P) — and the residuals differ by 121
orders of magnitude, so nothing NUMERICAL waits on this item.

What still waits on it is the TAG. Our ODE was discovered by numerical
nullspace and is VERIFIED. Matching it to a published theorem is what would
make the chain STRUCTURAL, and that requires the PRIMARY statement.

WHAT IS NEEDED — and note this is a request for a STATEMENT, not a value:
  1. The equation as PRINTED IN JMMS 1980, with its variable convention.
  2. The initial condition as printed there, INCLUDING THE SIGN.
  3. The determinant representation (which sign in the exponent), from the
     same source as (1) and (2) — the trap here is precisely that mixing a
     rendering of (1) with an initial condition from a different rendering
     gives a wrong answer SILENTLY.

Please supply all three from one source, or state that you cannot.

## OS-14 — NEW. Do the published higher-order coefficients matter now?

**Status: LOW PRIORITY. Probably moot; recorded so it is not silently dropped.**

OS-9 was withdrawn once the sigma-PV recursion let us generate coefficients
ourselves to arbitrary order (L-042). It stays withdrawn. This is the narrow
successor question: is there a PUBLISHED statement of the beyond-all-orders
term for the sine-kernel gap probability?

We have MEASURED its structure (L-050, VERIFIED):

    E_trunc  ~  C * exp(-2s) / s ,     C ~ 10^-2.7 (relative)

with the exponent a = 1 established by a 91-point fit whose rms improves 27x
as the window moves outward, against a = 0 which is worse by a factor 1300.

If a published form exists, it is a free out-of-sample check on a result we
obtained without any literature input. If it does not, the measurement stands
on its own and is a small original observation. Either outcome is fine, which
is why this is low priority — nothing downstream depends on it.

What would be needed: the exponentially-small correction term to the large-s
asymptotics, with its prefactor, from a primary source.

---

## OS-13 -- DOWNGRADED to low priority. Still open; do not spend on it.

The operator corrected their own earlier framing, and the correction is right.
What is load-bearing is that the ODE is CORRECT, and the evidence for that does
not route through the literature at all:

  - 79-digit out-of-sample agreement after nullspace discovery
  - 220-digit agreement at the calibration gate
  - the lambda = 2 algebraic identity, which needs no convention from any source
  - the sign trap failing by 121 orders of magnitude (L-051)
  - and now A = 2 and theta = 1/2 as exact rationals from the linearization,
    reproduced independently by the large-order growth of the coefficients,
    with the resulting exponent matching a measurement made by a disjoint code
    path (L-053)

A primary citation would upgrade the epistemic LABEL and add evidence
independent of this pipeline, which is not nothing. It cannot move confidence
much given the above. Bornemann arXiv:0804.2543 already supplies equation,
initial condition and exponent sign in one self-consistent place, so the
residual risk is only that a secondary transcribed JMMS wrongly -- a bounded
and small tail.

STANDING INSTRUCTION: if a primary falls into your lap, take it. Do not hunt.
Mehta Ch. 21 is the accessible route Bornemann points at.

## OS-15 -- NEW. The Stokes constant C, and why it is NOT being chased

**Status: QUEUED BEHIND PHASE 1 TARGET SELECTION. Deliberately not worked.**

L-053 measured the beyond-all-orders prefactor
    E_trunc ~ C (A s)^(beta - 1/2) exp(-A s),  A = 2, beta = -1/2
    C = 0.31830988618379067153776752674503...
and it agrees with 1/pi to at least 64 digits, monotonically in the
extrapolation degree.

WHAT WAS DONE: one declared candidate, checked by inspection. No PSLQ, no
basis, no search. That costs nothing and consumes no Phase 1 budget.

WHAT IS NOT BEING DONE, and this is the point of the entry: establishing it.
C is a Stokes constant for a Painleve transcendent. Proving or even properly
vetting the identification is a real piece of work and is exactly the adjacent
target that would consume a phase. It is queued.

WHAT WOULD BE NEEDED IF IT IS EVER PROMOTED, from a primary source:
  1. Whether the Stokes constant for the sigma-form of PV at this parameter
     value is known in closed form, and its value as PRINTED.
  2. Whether the beyond-all-orders term for the sine-kernel gap probability
     appears anywhere with its prefactor (this supersedes OS-14, which asked
     the same question less precisely).
  3. The convention the source uses for the trans-series normalisation --
     since L-051 and L-034 both show that convention, not value, is where the
     silent errors live.

Note the provenance-column scoring, which is why this is interesting rather
than merely available: if the answer to (1) is "conjectured or absent", C has
a strong Phase 1 profile -- and unusually, we would arrive with 64 digits in
hand rather than needing to earn them.

## OS-14 -- SUPERSEDED by OS-15 item 2.

Retained rather than removed (append-only discipline). The question was
whether a published beyond-all-orders term exists; OS-15 asks it more sharply
and with the prefactor attached.
