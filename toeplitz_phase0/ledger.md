# LEDGER — Phase 0, sine-kernel / Fredholm determinant calibration

APPEND-ONLY. Entries are never edited or deleted. If a later entry supersedes
an earlier one, the earlier one stays and the later one says so explicitly.

Every claim carries exactly one tag:

- **PROVEN** — derived symbolically in this session, derivation shown
- **VERIFIED** — computed numerically in this session, with stated precision
  and convergence evidence
- **STRUCTURAL** — follows from a cited theorem the OPERATOR has confirmed
- **CONJECTURED** — pattern, guess, numerical coincidence, or anything
  recalled from literature

Note on the tag `STRUCTURAL`: **no entry in this ledger carries it.** No
theorem statement has been confirmed by the operator in this session, so
nothing qualifies. Statements that would ordinarily be justified by citation
are tagged CONJECTURED and listed in `open_questions.md` as OPERATOR-SUPPLY
items. This is the intended behaviour of the partition, not an omission.

---

## L-000 — Object under study and normalisation

**PROVEN** (definition, fixed by us; recorded so every later number is
unambiguous). The kernel is

    K_s(x, y) = sin(s(x - y)) / (pi (x - y)),    (x, y) in [-1, 1]^2

with the removable singularity at x = y assigned the value s/pi. The quantity
computed throughout is

    F(s) = log det(I - K_s)  on  L^2([-1,1]).

By the substitution x -> x/s this is the sine-kernel gap probability on the
interval (-s, s) with the standard density-one sine kernel
sin(pi u)/(pi u) rescaled; the operator is asked in `open_questions.md`
(OS-1) to confirm which normalisation the reference constant is quoted in,
because a factor of 2 in the interval length shifts `b*log s` into `c`.
**Until OS-1 is answered, all comparisons to literature are internal to this
normalisation.**

---

## L-001 — Discretisation: Nystrom with Gauss-Legendre nodes

**VERIFIED.** `sinekernel.py` builds the Nystrom matrix
`M_ij = sqrt(w_i) K_s(x_i, x_j) sqrt(w_j)` on n Gauss-Legendre nodes of
[-1,1] and returns `log det(I - M)`.

Gauss-Legendre nodes and weights are computed from scratch (Newton iteration
on the Legendre three-term recurrence, 25 guard digits, node symmetry
`x_{n+1-i} = -x_i` imposed exactly rather than obtained by convergence), so
no node table is taken from memory or from a library.

Correctness evidence, all recomputed by `verify_kernel.py`:

- GL exactness: the rule integrates all monomials of degree < 2n exactly;
  the measured worst-case residual at n=12, dps=40 is reported in
  `out/convergence.json` under `cross.gl_exactness`.
- Parity factorisation agrees with the unfactored determinant.
- The two independent arithmetic backends (mpmath `mpf`, gmpy2 MPFR) agree.

---

## L-002 — Three structural facts exploited, each verified numerically

**PROVEN** (1) *Parity.* `K_s(-x,-y) = K_s(x,y)`, and the GL rule is
symmetric, so in the basis of even/odd combinations of the node pairs
(x_i, -x_i) the matrix `I - M` is exactly block-diagonal with two blocks of
size n/2. Hence `det = det(A_+) det(A_-)`. Cost drops by 4x.
**VERIFIED**: factored and unfactored determinants agree (recorded in
`out/convergence.json`, `cross.parity_factorisation`).

**PROVEN** (2) *Positivity.* `sin(s x)/(pi x)` is the Fourier transform of the
indicator of [-s, s], hence a positive-definite function, hence
`[K_s(x_i, x_j)]_{ij}` is positive semidefinite for ANY choice of nodes, and
`M` is PSD because the GL weights are positive. Since the eigenvalues of the
sine kernel on an interval lie strictly in (0,1), `I - M` is symmetric
positive definite. Consequences used operationally:

- Cholesky needs no pivoting;
- a non-positive pivot cannot occur in exact arithmetic on a resolved grid,
  so it is a genuine *diagnostic* of breakdown rather than a normal event.
  The code raises on it instead of returning a plausible number.

**VERIFIED** (3) *Rank-2 trigonometric structure.*
`sin(s(x_i - x_j)) = sin(s x_i) cos(s x_j) - cos(s x_i) sin(s x_j)`, so the
whole matrix is built from O(n) transcendental evaluations rather than O(n^2).

---

## L-003 — The breakdown diagnostic fires, and is recorded rather than hidden

**VERIFIED.** At s=30 with n=40 (n/s = 1.33) the Cholesky pivot 19 is
negative (~-3.06e-23) and `log_det` raises `ArithmeticError`. This is the L-002
positivity diagnostic firing on an under-resolved grid: n is below the
resolution threshold set by the kernel bandwidth ~2s/pi.

Recorded because it is evidence *for* the implementation: on a grid too coarse
to represent the operator, the code refuses rather than returning a
well-formed wrong number. `verify_kernel.py` now tabulates such rows as
diagnostics instead of aborting the table.

---

## L-004 — Measured digit-loss law

**VERIFIED.** The arithmetic accuracy of `log det(I - K_s)` at working
precision `dps` is `dps - loss(s)` digits, with

    loss(s) = 0.866 * s   digits,     0.866 = 2 / ln(10).

Measured, not assumed: it is read off the plateau of the node-convergence
sweep at fixed dps, across s = 10, 20, 30, 40 (`out/convergence.json`).

**CONJECTURED.** The implied condition number of `I - K_s` is ~ exp(2 s), and
the exponent 2 is a fit to four values of s, not a derivation. The *law* is
used only to size `dps`; every value is separately certified by L-005, so an
error in the law costs time, not correctness.

---

## L-005 — Certification protocol for a single grid point

**VERIFIED** (protocol definition + execution). For each s, three independent
evaluations are made:

    v_base = F(s; n0,   dps0)
    v_node = F(s; 2*n0, dps0)          <- node doubling
    v_prec = F(s; n0,   dps0 + 20)     <- 20-digit precision increase

and

    certified_digits(s) = -log10( max( |v_base - v_node|, |v_base - v_prec| ) ).

A value is treated as VERIFIED only through this number. Both channels are
required, because they fail in different directions: node doubling cannot see
arithmetic error (both runs share the same roundoff), and a precision bump
cannot see quadrature error (both runs share the same nodes).

Achieved on the production grid: see L-010 and L-013.

---

## L-006 — The asymptotic model and what is fitted

**CONJECTURED** (the *form*; it is taken as an ansatz here, not derived):

    F(s) = a s^2 + b log s + c + sum_{m>=1} e_m s^(-2m) + ...

**VERIFIED** (the coefficients, within this ansatz):

    a = -1/2      recovered to display precision at every order K tested
    b = -1/4      recovered to display precision at every order K tested

**CONJECTURED** — the correction series is even in 1/s. Evidence: an
unrestricted fit including odd powers returns odd coefficients consistent
with zero while `e_1 = 0.0312505... = 1/32` comes out clean; the measured
odd/even amplitude ratio is 0.074 (`odd_even_ratio` in `out/constant.json`).
Adopting `step=2` roughly doubles the number of usable orders for a given
grid size. This is a *modelling* choice and it is falsifiable: it is checked
by held-out prediction (L-008), not assumed.

**CONJECTURED** — `e_1 = 1/32` exactly.

---

## L-007 — Extraction of c, and the honest error budget

**VERIFIED.**

    c = -0.438501166054690678523656303940160547618114829057...
    sigma_c = 5.10e-40
    HONEST DIGITS IN c = 39

The working precision at which this was computed was **318 dps**. *These are
different numbers.* 318 is what mpmath was told to carry; 39 is what the
extraction actually determines. Reporting 318, or any number derived from it,
as the accuracy of c would be a session failure. The ledger records 39.

sigma_c is the max of three independently measured sources:

| source | meaning | value | digits |
|---|---|---|---|
| E1 | order truncation: spread of c over a plateau of successive orders K | 5.10e-40 | 39.3 |
| E2 | window sensitivity: change of c when the fitting window is moved | 1.58e-41 | 40.8 |
| E3 | data noise amplified through the fit, from the certified digits per point | 5.29e-51 | 50.3 |

The binding constraint is **E1**, i.e. truncation of the asymptotic series,
not arithmetic. E3 sits 11 digits below E1, which is the quantitative
statement that this is not a precision-limited computation. Buying more
digits therefore requires more *orders* (more grid points, and a wider
s-range), not more dps.

Selected order K = 79 (even powers only), chosen by scoring each K by the
worst successive difference over a 3-order window, so that a lucky single-order
dip cannot be selected.

---

## L-008 — Falsification test (held out, not fitted)

**VERIFIED.** The grid point s = 40.25 was excluded from the fit and then
predicted from the fitted model:

    | prediction - independently computed value |  =  1.65e-90

This is a prediction, not a residual: the point contributed nothing to the
coefficients. It tests the model form of L-006 (including the even-series
conjecture) rather than the arithmetic.

---

## L-009 — Two bugs that produced plausible wrong answers

Recorded in full because both were silent, both looked like ill-conditioning,
and either could have propagated a confident wrong constant.

**VERIFIED (bug 1: fitting-window collapse).** Point selection originally took
the K+3 *largest* s values available. For large K this collapses the fit onto
a narrow window at the top of the grid, where the columns `s^2`, `log s`, `1`,
`s^-2`, ... are nearly linearly dependent. Symptom: the order sweep diverged
past K=4 with a and b running away by many orders of magnitude. Fix:
`select_points()` spreads points evenly by index across the whole grid.

**VERIFIED (bug 2: precision truncation at parse time).** `load()` parsed the
stored decimal strings into `mp.mpf` *before* raising `mp.dps`. Every one of
the 124-digit data values was therefore silently truncated to mpmath's
15-digit default, and the fit was run on 15-digit data. Symptom: identical to
bug 1 — divergence past low K. Diagnosed by reproducing the fit in a
standalone script on the same file, which reached 8.1e-38. Fix: `mp.dps` is
now set inside `load()` before any parsing, with the failure mode documented
in the docstring.

**This is the most dangerous error class in this pipeline**: `mp.mpf(str)`
silently truncates, so high-precision data can be destroyed with no exception,
no warning, and a plausible-looking result at the far end. Any future addition
that parses stored constants must set precision first.

---

## L-010 — Production grid, revision 1 (53 points)

**VERIFIED.** s in [30, 89]: step 0.5 on [30,45], step 2 on [47,89].
Minimum certified digits over the grid: 124.263. Extraction on this grid gave
36 honest digits in c. Superseded by L-013 (kept per the append-only rule; the
constant did not move, only its error bar).

---

## L-011 — CALIBRATION GATE (task 0.3): PASSED

**CONJECTURED** (the target form — recalled, therefore CONJECTURED by rule 2,
and listed as OS-1 in `open_questions.md`):

    c  =?=  (1/12) log 2 + 3 zeta'(-1)

**VERIFIED** (the comparison). Both sides were computed in-session; nothing
was taken from memory except the *form* of the right-hand side. On the
revision-1 grid:

    c          = -0.43850116605469067852365630394016054834
    candidate  = -0.43850116605469067852365630394016054762
    |c - candidate| = 7.196e-37
    agreement  = 36.14 digits          (gate threshold: 12 digits)

**GATE PASSED**, exceeding the required 12 digits by 24.

The result that matters more than the pass: at that revision sigma_c was
6.55e-37 and the observed discrepancy was 7.20e-37. The error bar is
**calibrated** — it predicted the actual deviation to within 10%, rather than
being conservative by orders of magnitude. An error bar that is merely large
enough proves nothing; one that lands on the observed error is evidence the
budget of L-007 is modelling the right things.

`zeta'(-1)` is additionally cross-checked in-session against
`1/12 - log A` (Glaisher), so it is not a single-source value.

---

## L-012 — PSLQ harness (task 0.4), revision 1: relation found, CORRECTLY REJECTED

**VERIFIED (the search).** With the full 8-element basis
`{1, log2, logpi, gamma, zeta'(-1), zeta(3)/pi^2, Catalan, log(1+sqrt2)}`
at P = 33 and maxcoeff 1e4, PSLQ returned

    [-12, 1, 0, 0, 36, 0, 0, 0]   i.e.   c = (1/12) log 2 + 3 zeta'(-1)

residual 8.6e-36, coefficient sup-norm 36 (<= 1e4, criterion (b) satisfied).

**VERIFIED (the rejection).** The mandated null controls FAILED: the identical
harness run against random targets also returns relations at dps 15-40 with
this basis. Therefore the relation above is **NOT REPORTABLE**. It agrees with
the gate, which is exactly why it must not be reported: agreeing with the
expected answer is not evidence when the harness would have agreed with
anything.

Reporting this rejection is the deliverable. A harness that returned the right
answer here and stopped would have been indistinguishable from a broken one.

**VERIFIED (spurious-relation threshold).** With 9 vector entries and
maxcoeff 1e4 the measured threshold sits near 50 digits: random targets stop
producing relations only above ~dps 50. The heuristic
`threshold ~ (#entries) * log10(maxcoeff)` = 9 * 4 = 36-50 is consistent with
the measurement. Hence 36-39 honest digits is **overcomplete** for the full
8-element basis.

**VERIFIED (a bug in the threshold statistic, found and fixed).** The
threshold must be read from ABOVE: the lowest precision such that every
higher swept precision is also clean. Taking `min(clean_dps)` returned dps=10,
which is meaningless — at very low precision PSLQ reports nothing because it
fails to converge, not because the basis is complete. The original code made
exactly this error and would have reported a threshold of 10.

---

## L-013 — Production grid, revision 2 (83 points); c to 39 honest digits

**VERIFIED.** The grid was densified on [30.25, 44.75] (step 0.5, offset from
the existing points), giving 83 points, minimum certified digits 98.78.

    c = -0.438501166054690678523656303940160547618114829057222528360990...
    sigma_c = 5.10e-40   ->   39 honest digits    (working precision 318 dps)
    E1 = 5.10e-40 (binding), E2 = 1.58e-41, E3 = 5.29e-51
    held-out residual at s = 40.25: 1.65e-90

Supersedes L-010's error bar. The digits of c agree with revision 1 throughout
revision 1's stated 36-digit range — i.e. **the constant did not move when the
error bar shrank**, which is the behaviour a correct error bar must have.

Cost/benefit measured: +30 points bought +3 digits. Compare L-010, where +22
points that *extended s_max* from 45 to 89 bought +11 digits. **Extending the
range dominates densifying it**, consistent with the extrapolation to
1/s^2 -> 0 being conditioning-limited rather than sample-limited.

---

## L-014 — The precision budget the 0.4 protocol actually requires

**PROVEN** (arithmetic on the protocol as specified; no numerics involved).
Let D be the honest digit count of the target. Task 0.4 imposes two
constraints that are not independent of D:

1. Criterion (a) requires the relation to be re-found at P+30 with identical
   coefficients. A PSLQ run at P+30 consumes P+30 digits of the target, so
   `P + 30 <= D`, i.e. `P <= D - 30` (we use `P = D - 33` for margin).
   Running the search at P = D-3 and "reconfirming" at D+27 feeds PSLQ 27
   digits of pure noise; it will always return NO RELATION. That is a
   guaranteed-fail protocol, not a test, and its failure is not evidence
   against the relation.

2. Null control (i) perturbs the target at the 20th digit. For the control to
   have any discriminating power the search must resolve that digit: `P > 20`.

Combining with the measured spurious threshold T(basis) of L-012, a
REPORTABLE positive result requires

    D  >=  max( T(basis), 20 )  +  33.

For the 8-element basis (T ~ 50) that is D >= 83. For the 3-element basis
`{1, log2, zeta'(-1)}` (4 vector entries, expected T ~ 16-25) it is
D >= 53-58.

**Consequence, stated plainly:** at D = 39 the specified protocol *cannot*
return a positive result for any basis in the nesting. This is a property of
the protocol and the available precision, not of the constant. This is the
motivation for the revision-3 data campaign (L-015).

---

## L-015 — Revision-3 data campaign (in progress at time of writing)

**Method, recorded before the result is known** (so the target cannot be
adjusted after the fact):

Two mismatches were found in the revision-2 grid parameters by inspection:

- at s ~ 30 the NODE channel binds (98.8 certified digits) while the
  precision channel reports ~139;
- at s >= 47 BOTH channels report ~139, meaning the node error has fallen far
  below the arithmetic floor: nodes are massively oversupplied, and since the
  certification protocol requires a run at 2n costing 8x, that oversupply is
  precisely what made extending to large s expensive.

**VERIFIED** (measured node-convergence law, from the revision-2 certification
data): `node_digits(n, s) ~ A n - B s + C` with A = 1.767, B = 3.372, C = 2.88.
A and B are separately pinned by two independent measured slopes: +1.848
digits per 0.5 step in s at +2 nodes, and -1.686 digits per 0.5 step in s at
fixed n. Check: at s=42.75, n=160 it predicts 140.2 digits against 140.19
measured.

Inverting the law lets a *certification level* be requested directly.
`extend_adaptive.py` targets 165 certified digits with a hard floor of 150 and
retries with more nodes or more precision if the protocol falls short — the
model only sets the starting guess; the protocol still decides.

**VERIFIED** (first adaptive point): s = 91 certified to 173.3 digits using
n = 266, versus n = 337 under the old fixed rule, in 57.6 s.

Campaign: refit s in [30,45] step 0.25 and s in [45,89] step 2 to the 165-digit
target, then extend to s in [93,149] step 2. Expected effect: E3 drops by
~26 digits (removing it as a future constraint), and the added range attacks
E1, which is the binding term.

**Predicted outcome, stated in advance:** D rises from 39 to somewhere in the
range 48-58. If D >= 53 the 3-element basis can satisfy the 0.4 protocol
cleanly; if not, the honest Phase 0 result for 0.4 remains the quantified
shortfall of L-014. Both outcomes are reportable; only the second requires no
further work.

---

## L-016 — Revision-3 grid (113 points); c to 58 honest digits

**VERIFIED.** The campaign of L-015 completed:

- s in [30, 45] step 0.25 and s in [45, 89] step 2 REFIT to the 165-digit
  certification target (no new points; data quality only);
- s in [93, 149] step 2 added (29 new points).

Grid: **113 points, s in [30, 149], minimum certified digits 165.792**
(was 98.78). Snapshot kept at `out/certified_data.rev3.json`.

    c = -0.438501166054690678523656303940160547619150796475584079822875
    sigma_c = 7.67e-59   ->   58 honest digits
    working precision 515 dps   -- again, a DIFFERENT number
    E1 = 7.67e-59 (binding), E2 = 1.51e-59, E3 = 9.63e-136
    selected K = 108 (even powers only, sweep stride 2)
    held-out residual at s = 44.0: 1.98e-83

The refit moved E3 from 5.29e-51 to 9.63e-136, i.e. 85 digits below the
binding term. Data noise is now irrelevant to this measurement by a wide and
measured margin; the entire error is truncation of the asymptotic series.

Every digit of the revision-2 value (L-013, 39 digits) is reproduced. The
constant has now survived three independent grids without moving.

---

## L-017 — Which lever actually buys digits (measured, and it overturned the guess)

**VERIFIED.** Truncation of an asymptotic series is governed by the smallest s
in the fitting window, so raising s_min ought to help. It was tested directly
by refitting the revision-2 grid restricted to s >= s_min:

| s_min | points | chosen K | E1 |
|---|---|---|---|
| 30 | 83 | 79 | 5.10e-40 |
| 35 | 63 | 59 | 1.11e-38 |
| 40 | 43 | 39 | 3.41e-37 |
| 45 | 23 | 19 | 1.13e-34 |
| 51 | 20 | 16 | 1.36e-32 |
| 61 | 15 | 11 | 8.53e-27 |

Raising s_min makes the answer WORSE, monotonically, because every
configuration available here is **order-limited, not s_min-limited**: K is
capped at (points - 4), so discarding low-s points discards orders faster than
it improves the per-order truncation. The lever that matters is the number of
correction orders, i.e. the number of grid points.

This overturned the working assumption recorded in L-013 ("extending the range
dominates densifying it"), which had been inferred from a revision-1 change
that altered BOTH the point count and s_max and could not separate them.
L-013 is left standing per the append-only rule; **this entry supersedes its
interpretation.** The lesson is that the earlier conclusion was drawn from a
confounded comparison.

**VERIFIED (marginal rate).** Between the 113-point and 83-point grids the
sweep improved from 5.1e-40 (K=79) to 7.7e-59 (K=108): ~0.26 digits per
correction order after the certification refit, against ~0.07 digits/order
before it. Improving the data quality did not merely lower E3, it raised the
RATE at which additional orders convert into digits, because orders whose
contribution sat below the old noise floor became usable.

---

## L-018 — A null control that could not see what it perturbed

**PROVEN** (arithmetic on the harness parameters). Null control (i) perturbs
the target to c*(1+1e-20), an ABSOLUTE change of |c|*1e-20 ~ 4.4e-21. PSLQ is
invoked with tol = 10^-(P - GUARD), GUARD = 8. Discrimination therefore
requires

    |c| * 10^-20  >  10^-(P - GUARD)      i.e.      P  >  20 + GUARD + log10|c|

which for |c| ~ 0.4385 and GUARD = 8 is **P >= 28**, not P >= 20 as recorded
in L-014.

**VERIFIED** (the failure this predicts, observed). At D = 58 the driver chose
P = D - 33 = 25, giving tol = 1e-17 against a perturbation of 4.4e-21. On the
3-element basis {1, log2, zeta'(-1)} the run then gave:

    criterion (a): PASS  -- [12, 0, -1, -36] at P=25, identical at P=55
    criterion (b): PASS  -- sup-norm 36 <= 1e4
    control (ii) random 30-digit constant: PASS -- NO RELATION
    control (i)  perturbed c*(1+1e-20):   FAIL -- same relation returned

Control (i) returned the same relation because at tol = 1e-17 the perturbed
and unperturbed targets are the same number. The control was run below its own
resolution. **Reporting that as evidence that the basis is overcomplete would
have been wrong**, and reporting the relation anyway would have been worse.

Fix: `run_pslq.py` now computes the control-(i) sensitivity floor from |c| and
GUARD, and chooses P per basis as the SMALLEST admissible precision

    P = max( measured spurious threshold T(basis), control-(i) floor )

because every digit spent on the search is a digit denied to the
reconfirmation at P+30. When P + 30 exceeds the available digits the driver
now SKIPS criteria (a) and the controls and says so, rather than running a
protocol whose failure is guaranteed and uninformative.

Corrected budget for a reportable positive result, superseding L-014:

    D  >=  max( T(basis), 20 + GUARD + log10|c| ) + 30 + margin.

For the 3-element basis (measured T = 25, floor 28) that is D >= 61.

---

## L-019 — Measured spurious-relation thresholds (task 0.4 deliverable)

**VERIFIED**, from 3 random targets per precision per basis, maxcoeff = 1e4.
Every one of these calls is logged in `out/pslq_calls.json`.

| basis size | vector entries | spurious relations at dps | threshold T |
|---|---|---|---|
| 8 | 9 | 15-40 | ~50 |
| 4 | 5 | 15-25 | 30 |
| 3 | 4 | 15-20 | 25 |

At dps = 10 no basis returns anything, and this is **not** cleanliness: PSLQ
simply fails to converge when tol is looser than the basis spacing. The
threshold must be read from ABOVE (see L-012). A harness that reported
min(clean dps) would report 10 for every basis.

The heuristic T ~ (#entries) * log10(maxcoeff) predicts 16, 20, 36 against
measured 25, 30, ~50 -- the right ordering and scale, consistently optimistic
by ~40%. Recorded as **CONJECTURED**; the measured column is what the harness
uses.

---

## L-020 — Task 0.1 convergence tables (artifact: out/convergence.json)

**VERIFIED.** Both knobs swept independently, because they control different
errors: node count controls quadrature error, `mp.dps` controls arithmetic
error. Sweeping only one cannot separate them.

**Node-count convergence** (mp.dps fixed at 200, error against n = 6s).
Node counts are taken relative to s, since the kernel bandwidth is ~2s/pi and
a fixed absolute list would mix converged and under-resolved regimes:

| n/s | s=10 | s=20 | s=30 | s=40 |
|---|---|---|---|---|
| 1.0 | — | — | SPD diagnostic | SPD diagnostic |
| 1.5 | | | | 1.90 |
| 2.0 | | | | 25.1 |
| 2.5 | | | | 52.2 |
| 3.0 | | | | 82.6 |
| 3.5 | | | 85.7 | 115.6 |
| 4.0 | | | 114.0 | 151.0 |
| 4.5 | | | 144.1 | 169.1 |

(agreeing digits; the full table for all four s is in `out/convergence.json`).
Convergence is super-exponential in n once n exceeds the bandwidth, and the
rate in digits per node is only weakly dependent on s. Rows marked "SPD
diagnostic" are the L-003 breakdown: at n/s = 1.0 the grid cannot represent
the operator and the code raises rather than returning a number.

**Precision convergence** (n = 6s, error against dps = 180), giving the
digit loss directly as `dps - agreeing digits`:

| s | measured digit loss (mean over dps = 60..140) |
|---|---|
| 10 | 5.50 |
| 20 | 13.72 |
| 30 | 22.73 |
| 40 | 30.49 |

The loss is stable across dps at fixed s (spread < 1 digit), which is what
must happen if it is a conditioning cost rather than an artefact. Linear fit:

    loss(s)  =  0.833 s  -  2.8      (measured)

**CONJECTURED**: this is the same thing as `2 s / ln 10 = 0.8686 s`, i.e. a
condition number `~exp(2s)`; measured slope agrees to ~4% over the swept
range, and the negative intercept is not explained. The pipeline sizes `dps`
using the conservative 0.866 s, so an error here costs time, not correctness —
every value is separately certified by the L-005 protocol regardless.

**Structural cross-checks** (same artifact):

    GL exactness, degree < 24, n=12, dps=40 : 1.148e-41
    parity factorisation vs unfactored det  : 1.497e-48
    mpmath backend vs gmpy2/MPFR backend    : 3.772e-106

---

## L-021 — Revision-4 grid (142 points); c to 71 honest digits

**VERIFIED.** Added s in [92, 148] step 2 (29 points), giving **142 points,
s in [30, 149], minimum certified digits 165.792**. Snapshot:
`out/certified_data.rev4.json`.

    c = -0.43850116605469067852365630394016054761915079647558407982284...
    sigma_c = 1.4105e-72   ->   71 honest digits
    working precision 515 dps   -- still a DIFFERENT number
    E1 = 1.41e-72 (binding), E2 = 7.81e-73, E3 = 3.81e-114
    selected K = 136 (even powers only, sweep stride 2)
    held-out residual at s = 67.0: 3.75e-82

Progression across four independent grids, none of which moved the digits of
the previous one:

| revision | points | s range | min certified | honest digits in c |
|---|---|---|---|---|
| 1 | 53  | [30, 89]  | 124.3 | 36 |
| 2 | 83  | [30, 89]  | 98.8  | 39 |
| 3 | 113 | [30, 149] | 165.8 | 58 |
| 4 | 142 | [30, 149] | 165.8 | 71 |

---

## L-022 — CALIBRATION GATE at 71 digits: PASSED

**VERIFIED.**

    c          = -0.438501166054690678523656303940160547619150796475584079822844
    candidate  = -0.438501166054690678523656303940160547619150796475584079822844
    |c - candidate| = 1.0589e-72
    sigma_c         = 1.4105e-72
    AGREEMENT  = 71.98 digits          (gate threshold: 12 digits)

**GATE PASSED**, exceeding the 12-digit requirement by 60 digits.

For the third time the error bar is **calibrated rather than merely safe**:
|c - candidate| = 1.06e-72 against sigma_c = 1.41e-72, a ratio of 0.75. At
revision 1 the ratio was 1.10 and at revision 3 it was 0.41. An error bar that
tracks the true deviation to within a factor of ~2 across a 36-digit change in
scale is evidence that the E1/E2/E3 budget of L-007 models the right things.

The target form remains **CONJECTURED** (OS-1 unanswered). What is VERIFIED is
the agreement, not the identification.

---

## L-023 — PSLQ HARNESS (task 0.4): REPORTABLE RELATION

**VERIFIED.** With D = 71 the protocol is satisfiable. Per-basis outcome,
with P chosen as the smallest admissible precision per L-018:

| basis size | measured T | P = max(T, 31) | P+30 <= 68? | outcome |
|---|---|---|---|---|
| 8 | 50 | 50 | 80 > 68 — no  | SKIPPED: needs D >= 83 |
| 6 | 40 | 40 | 70 > 68 — no  | SKIPPED: needs D >= 73 |
| 4 | 30 | 31 | 61 <= 68 — yes | **REPORTABLE** |
| 3 | 25 | 31 | —              | not reached (loop stopped at size 4) |

The two larger bases were SKIPPED, not failed. Running criteria (a) and the
controls there would have been a guaranteed-fail protocol (L-018), and a
guaranteed failure is not evidence. The 6-element basis missed by 2 digits.

**Result on the 4-element basis {1, log2, gamma, zeta'(-1)}:**

    -12*c + 1*log2 + 36*zeta'(-1) = 0        i.e.   c = (1/12) log 2 + 3 zeta'(-1)

    (a) found at P = 31, re-found at P+30 = 61 with IDENTICAL coefficients  PASS
    (b) coefficient sup-norm 36 <= 10^4                                     PASS
    (c) null control (i), c*(1+1e-20):  NO RELATION                         PASS
        null control (ii), random 30-digit constant: NO RELATION            PASS
        P = 31 >= measured spurious threshold T = 30                        PASS

    residual at P = 31: 6.68e-52

Note that `gamma` is present in the basis and receives coefficient 0. That is
a small piece of adversarial evidence in its own right: the harness had the
opportunity to use a fourth constant and did not.

**106 PSLQ calls were made in this run and all 106 are logged** to
`out/pslq_calls.json`, including every failure and every null-control call.

**What this does and does not establish.** It establishes that the relation
survives an adversarial protocol that the same harness demonstrably fails on
perturbed and random targets at the same precision and with the same basis.
It does NOT establish the literature identification: the target form entered
this session from the prompt and remains CONJECTURED until OS-1 is answered.
Phase 0 was asked to earn the right to make claims of this kind, and the
content of that right is exactly the null controls, not the relation.

---

## L-024 — Phase 0 closure

All five tasks delivered:

| task | status |
|---|---|
| 0.1 sine-kernel Fredholm determinant, convergence in n AND dps | VERIFIED, L-001..L-005, L-020 |
| 0.2 asymptotic extraction with honest error budget | VERIFIED, L-007, L-021 |
| 0.3 calibration gate | PASSED at 71.98 digits, L-022 |
| 0.4 PSLQ harness with adversarial null controls | REPORTABLE relation, L-023 |
| 0.5 open_questions.md | delivered, 8 OPERATOR-SUPPLY + 6 internal items |

`make verify` / `.\verify.ps1 verify` re-derives every VERIFIED claim from
nothing but mpmath.

**Four bugs were found and fixed, and all four produced plausible-looking
wrong answers rather than errors** (L-009 x2, L-012, L-018). Three of the four
were caught only by a control or a cross-check, not by a test. This is the
main transferable result of Phase 0: in this problem class the default failure
mode is a confident wrong number, so the controls are not overhead, they are
the measurement.

**No Phase 1 constant was attempted.**

## L-025 — Reproducibility defect in the rebuild target, found and fixed post-closure

**Tag: VERIFIED** (set equality checked exactly; see below)

Closing check on the `data` target of `make verify`. `build_grid.BLOCKS`
declared its third block as `s in [91, 149] step 2`, but the grid actually
used for the revision-4 result was built in two passes — an odd sweep
`93..149 step 2`, a smoke-test point at `s = 91`, and a later even sweep
`92..148 step 2` (L-021). The union of those is every integer in `[91, 149]`,
i.e. step 1, not step 2.

Consequence had this not been caught: `verify` would have rebuilt a
**113-point** grid and re-derived c to roughly 58 honest digits, while
`ledger.md` claimed 71. The claim itself was never wrong — the *reproduction
path* for it was. This is the same failure mode as L-009 and L-018: no
exception, no warning, a plausible number that silently disagrees with the
record.

Fix: third block changed to `("91", "149", "1")`. Verified by generating the
point set from `BLOCKS` symbolically and comparing to the certified grid on
disk as sets of decimal strings:

    BLOCKS would build: 142 points
    grid on disk      : 142 points
    in BLOCKS not on disk: []
    on disk not in BLOCKS: []

Exact set equality, both directions. The module docstring was also corrected:
it justified the high-s blocks by "raising s_max/s_min relieves conditioning",
which is the revision-1 reading that L-017 superseded. The measured reason is
that the extraction is **order-limited**, and each additional point buys one
more correction order.

Note the asymmetry this exposes. `verify-fast` was run end to end (EXIT=0) and
proves the analysis chain; the full `verify` has still never been executed,
because it costs hours. What is established here is that its *specification*
now matches the data that produced the claims — not that the run succeeds.
That remains the one untested path in Phase 0, and it is recorded as such
rather than asserted away.

## L-026 — OS-1 DISCHARGED: attribution and normalisation verified against primary sources

**Tag: STRUCTURAL** (operator-confirmed theorem, and the operator's sourcing
independently checked against primary text in-session, per their instruction
that the discipline apply symmetrically to them).

The operator supplied the attribution chain and asked that it be confirmed
rather than taken on their word. It was checked against the arXiv API record
and the paper bodies (PDFs fetched and text-extracted locally; the search-engine
summary channel was NOT used as evidence — see the failure noted below).

**Primary text, Ehrhardt (arXiv:math/0401205v2), verbatim:**

> "log det(I − K_2α) = − α²/2 − log α/4 + log 2/12 + 3ζ′(−1) + o(1), α → ∞."

with `K_α` the integral operator with kernel `sin(x−y)/(x−y)/π` on `[0, α]`.

**Primary text, Krasovsky (arXiv:math/0401258v2), verbatim, eq. (1) and (2):**

> "∆(s) = det[I − K], where K is the integral operator on L²(0, 2s) given by
>  (Kg)(x) = ∫₀^{2s} sin(x−y)/(π(x−y)) g(y) dy"
>
> "ln ∆(s) = − s²/2 − (1/4) ln s + c₀ + O(1/s), s → ∞,  where the constant
>  term c₀ = (1/12) ln 2 + 3ζ′(−1), and ζ′(x) is the derivative of Riemann's
>  zeta function."

**Normalisation now verified, and it was not free.** Krasovsky's ABSTRACT says
the kernel is on "the interval [0,s]", but his BODY defines `K` on `L²(0, 2s)`
— interval length 2s. Taking the abstract at face value would have introduced
a factor-4 error in the leading coefficient (length L gives −L²/8, not −L²/2)
and would have made the two papers appear to contradict each other. The body
is authoritative and the two papers agree. This session's operator
`sin(s(x−y))/(π(x−y))` on `[−1,1]` is, by the substitution `u = sx`, the sine
kernel on `[−s, s]`, length 2s; translation invariance identifies it with
Ehrhardt's `K_{2α}` at `α = s` and with Krasovsky's `∆(s)`. Term for term:
a = −1/2, b = −1/4, c = c₀. The operator's claim of no convention mismatch is
CONFIRMED.

**Independent internal pin on the normalisation (PROVEN, by arithmetic).**
The literature check is not actually load-bearing for the convention. Because
b = −1/4, any error by a factor λ in the interval-length convention shifts the
constant by −(1/4)log λ; for λ = 2 that is 0.1733…, which would destroy
agreement at the FIRST digit. Agreement to 72 digits therefore excludes every
such rescaling on its own. The normalisation is pinned by the arithmetic,
independently of any paper.

**Attribution, per Krasovsky's own introduction (primary, not recalled):**
des Cloizeaux and Mehta — first two terms; Dyson — full asymptotic expansion
via inverse scattering, "partly conjectural"; Widom — rigorous derivation of
the MAIN term; Deift, Its and Zhou — full asymptotics of (d/ds) ln ∆(s), which
"settled the question up to the constant term"; Krasovsky (that paper) and
Ehrhardt (independently) — the constant term.

**Three discrepancies with the operator's message, reported rather than absorbed:**

1. The operator cited Krasovsky as "CMP 262, 2006". The arXiv record gives
   `Int.Math.Res.Not. 2004 (2004), no.25, 1249-1272`. These are different
   venues and years. The MATHEMATICS is confirmed; the CITATION is not.
2. The operator wrote that "Widom proved the first- and second-order
   asymptotics". Krasovsky's introduction assigns Widom the main term, the
   first two terms to des Cloizeaux–Mehta, and the reduction-to-the-constant
   to Deift–Its–Zhou. The operator's chain compresses three contributions.
3. "Deift–Its–Krasovsky" as a third independent proof is NOT confirmed by
   either primary consulted; it would be a separate paper. Left unverified.

Ehrhardt's venue ("CMP 272, 2007") is not contradicted — the arXiv record
simply carries no `journal_ref` — and is left unconfirmed.

**Consequence.** The Phase 0.3 target form is upgraded from CONJECTURED to
STRUCTURAL, and the gate's meaning changes: the pipeline reproduces a PROVED
literature value to 72 digits, not merely a number seeded from the prompt.
This is the first STRUCTURAL entry in this ledger.

**Method note, and it is the same failure genus as L-009/L-018.** A
search-engine summary of Krasovsky returned "[0,s]" together with "−s²/2",
which is internally inconsistent (those two cannot both hold) and would have
propagated a factor-4 normalisation error. It was rejected only because the
inconsistency was checked arithmetically, not because it looked wrong. LLM
search summaries are a second-hand channel and are treated here as CONJECTURED
at best; only fetched primary text is admissible.

---

## L-027 — CORRECTION to the framing of L-023: the PSLQ result is harness validation, not evidence about c

**Tag: PROVEN** (the circularity is a fact about the protocol, not a measurement).

L-023 is append-only and stands as written. Its framing is nonetheless
insufficient and is corrected here.

The relation reported in L-023 is `−12c + log 2 + 36 ζ′(−1) = 0`, which is
algebraically identical to the 0.3 gate target. Both `log 2` and `ζ′(−1)` were
placed in the basis BY CONSTRUCTION. The search therefore had exactly two
possible outcomes: recover that relation, or return nothing. It could not have
produced independent information about `c`.

What L-023 establishes is therefore:
  * the harness RECOVERS a true relation when one is present, at a stated
    precision, with a stated basis, and
  * it returns NOTHING on a perturbed target and on a random target under the
    identical protocol.

That is a validated instrument. It is **not** confirmation of the value of `c`,
and L-023's closing paragraph — which addresses only the weaker point that the
literature identification was unverified — should not be read as claiming
otherwise.

This distinction is recorded now because it becomes load-bearing in Phase 1,
where the basis will be chosen to contain the constants a target is HOPED to
decompose into. In that setting "PSLQ found the relation I was looking for" is
close to uninformative unless the null controls and the spurious threshold do
the work. The instrument is the deliverable; the hit is not.

---

## L-028 — CORRECTION: sigma_c is CONSISTENT WITH calibration, not calibrated

**Tag: VERIFIED** (as a statement about what n = 3 can support).

Earlier entries and the session summary described the error bar as
"calibrated, not merely safe", on the evidence that |Δ|/σ_c took the values
1.10, 0.41, 0.75 across grid revisions 1, 3 and 4.

Three ratios cannot distinguish a correctly scaled σ from one wrong by a
factor of two; with n = 3 the sampling spread of such ratios is wide, and all
three values would sit unremarkably under either hypothesis. The defensible
claim is: **the three observed ratios are consistent with a well-scaled error
bar and show no evidence of systematic over- or under-statement.** They do not
establish the scale factor.

The stronger reading is withdrawn. Note the direction of the risk: it is the
UNDER-statement of σ_c that would corrupt a digit count, and nothing here rules
that out to better than a factor of ~2.

---

## L-029 — The even-only correction series is ALREADY implemented; the proposed gain is already banked

**Tag: VERIFIED** (read directly off the running configuration and artifacts).

The operator proposed, as the highest-value cheap experiment, determining
empirically whether the correction series runs in 1/s or 1/s², on the grounds
that an even-only series would buy roughly twice the digits per Richardson
order and "clears 83 immediately".

That experiment is already in the pipeline and has already been acted on:

  * `fit_constant.main()` calls `order_table(pts, 2, ...)` — `step = 2`, the
    even-only model — and this is what produced every reported result.
  * `odd_coefficient_test()` performs exactly the proposed test: an
    unrestricted `step = 1` fit, reporting max|odd d_k| / max|even d_k|. The
    recorded value in `out/constant.json` is **0.0349**.
  * The selected order is K = 136 at step 2, i.e. the fit already annihilates
    `s^-2 … s^-272`, not ~35 powers.

So the factor-of-two has been banked since before revision 1, and the current
71 digits are the POST-gain figure, not the pre-gain figure. The shortfall to
83 must be closed by some other lever.

Two honest qualifications, neither of which the ratio 0.0349 settles:
  * that ratio is evidence FOR the even-only model, not proof of it, and the
    docstring says so;
  * a genuinely nonzero odd part would bias `c` in a way E1 (an order-to-order
    difference within the even-only model) cannot see. E2, the window
    sensitivity, is the budget line that would catch it, and E2 = 7.8e-73 sits
    essentially at E1 = 1.41e-72 rather than above it — which is mild evidence
    that no unmodelled odd tail is present at that scale.

---

## L-030 — FALSIFIED: my own law T(b) = 5b + 10, and why it looked exact

**Tag: VERIFIED** (step-1 sweep, 3 random targets per precision, maxcoeff 1e4,
threshold read from above; 522 PSLQ calls logged to `out/pslq_calls_Tfine.json`).

Earlier today I recorded in `phase1_triage.md` that the measured spurious-
relation thresholds were "exactly linear", `T(b) = 5b + 10`, fitted to b = 3,
4, 6, 8 with zero residual, and I used it to extrapolate the digits Phase 1
would need at b = 10 and b = 12. I then tested it at the two basis sizes that
had never been measured.

**It is false.** At b = 7 the law predicts 45; the measurement gives 40.

Worse, the apparent exactness was an artefact of my own measurement grid. The
original sweep was `{10,15,20,25,30,40,50,55,60,80}` — spaced by 5 in the
region where T lands — and the fitted slope was also 5. A law with slope
equal to the sampling interval will reproduce quantised data exactly whether
or not it is true. The "zero residual" was carrying no information.

Re-measured on a **step-1** sweep over dps 24..52:

| b | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| T (step 1) | 24 | 27 | 30 | 35 | 39 | 44 |
| 5b+10 | 25 | 30 | 35 | 40 | 45 | 50 |

The true relation is concave, not linear: increments are 3, 3, 5, 4, 5. The
old law over-predicts by up to 6 digits, which is the SAFE direction (it asks
for more precision than needed), but it is wrong, and the b = 10 / b = 12 rows
I derived from it are unsupported.

**Two corrections that follow:**
1. `phase1_triage.md` is amended: the b = 10 and b = 12 requirements are
   withdrawn, and it now records that **T cannot be measured at b > 8 at all
   with the current basis**, which has only 8 entries. A Phase 1 basis of 10
   or 12 requires new constants to be declared first, and T re-measured then.
2. The requirement at b = 8 falls from D >= 83 to **D >= 77** (T = 44, control
   floor 31, so max(44,31) + 33). The current 71-digit result is 6 short of
   the full 8-element basis, not 12.

**Method note.** This is the fourth instance of the session's dominant failure
genus, and the first one I generated myself while writing up: a
quantity read off a grid too coarse to resolve it, presented as exact. It is
the same shape as bug 3 (threshold read from below) and L-018 (control run
below its own resolution). Resolution of the instrument must be checked
before a number taken from it is quoted -- including when the instrument is a
sweep I designed an hour earlier.

---

## L-031 — Densifying the grid hit a CONDITIONING wall, and the wall was precision

**Tag: VERIFIED** (bisection on the largest non-singular K; both runs recorded).

Revision 5 extended the grid 142 -> 224 points by densifying `[30,45]` to step
0.125 and `[45,89]` to step 1 (the cheapest points per certified digit). The
first fit then **failed outright**:

    ZeroDivisionError: matrix is numerically singular   (asympt.fit, K ~ 155+)

This is the honest failure direction and is worth recording as such: the run
aborted rather than returning a fitted value from a numerically singular
solve. Had `lu_solve` merely returned a badly-conditioned answer, this would
have been another plausible-wrong-number.

Diagnosis by bisection on the largest K whose solve is non-singular:

| headroom above certified digits | working precision | max usable K |
|---|---|---|
| 350 | 515 dps | 155 |
| 800 | 965 dps | 221 (no singularity) |

So the wall is **precision, not information**: at headroom 350 the 224-point
grid could not use a third of the orders it had already paid for in Nystrom
time. Densification raises the conditioning demand twice over — the dynamic
range `(s_max/s_min)^(2K)` grows with K, and adjacent rows become
near-duplicates separated only by `Delta_s/s`, which is 0.125/30 ~ 4e-3 at the
bottom of this grid.

Actions: `load()` default headroom 350 -> 800, with the measurement recorded
in its docstring; `order_table` now CATCHES the singular solve, stops the
sweep, and reports `singular_at_K` (also written to `constant.json`), so an
insufficient headroom is loud rather than silent.

**This refines L-017.** L-017 concluded the extraction is order-limited rather
than s_min-limited, and that each additional point buys an order. That holds
only while the working precision can carry the order. There is a third regime,
not previously observed: **precision-limited**, where points are present, the
orders they would buy are unusable, and the binding resource is `mp.dps` in
the FIT — not in the determinant evaluation, where all the certification
effort had been spent.

---
