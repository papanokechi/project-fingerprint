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

## L-032 — The full `verify` path has now been RUN, from nothing, and it reproduces exactly

**Tag: VERIFIED** (single end-to-end execution; log retained).

Until now the only never-exercised path in Phase 0 was the full rebuild.
L-025 was the argument for running it: a defect had already been found in that
path by inspection, which is direct evidence that an untested path harbours
defects. It was run in a scratch copy of the source containing **no `out/`
directory at all**, so it began from nothing but mpmath and the code.

    .\verify.ps1 verify        EXIT = 0
    grid build complete in 12612 s (3.5 h), 142 points

Reproduced, against the committed state (commit 21cb71c):

| quantity | committed | from-scratch rebuild |
|---|---|---|
| grid points | 142 | 142 |
| min certified digits/point | 165.792 | 165.792 |
| selected order K | 136 | 136 |
| (E1) order truncation | 1.4105e-72 | 1.4105e-72 |
| (E2) window sensitivity | 7.81179e-73 | 7.81179e-73 |
| (E3) data-noise | 3.81039e-114 | 3.81039e-114 |
| honest digits in c | 71 | 71 |
| gate agreement | 71.97515 digits | 71.97515 digits |
| held-out residual (s = 67) | 3.75487e-82 | 3.75487e-82 |
| PSLQ verdict | REPORTABLE at b = 4 | REPORTABLE at b = 4 |
| bases 8 and 6 | SKIPPED | SKIPPED |

**Stronger than a summary-statistics match:** the rebuilt grid was compared to
the canonical snapshot value by value, as decimal strings. All 142 common `s`
values are present in both and **zero values differ**. The determinant
evaluation is therefore deterministic and the certification protocol
reproducible, not merely repeatable in aggregate.

Note what this does and does not cover. It validates the state at commit
21cb71c — the 142-point spec, `load(headroom=350)`. The revision-5 changes
(224 points, headroom 800, the singular-solve guard) were made after this run
started and are NOT covered by it. The scratch tree is retained rather than
deleted, per the no-deletion rule.

---

## L-033 — Revision-5 grid (224 points): c to 73 honest digits, and a costly negative result

**Tag: VERIFIED.** E1 = 1.00398e-74, E2 = 4.2366e-76, E3 = 6.92354e-107,
adopted sigma_c = 1.00398e-74, K = 218, working precision 965 dps (again a
different number). Held-out test at s = 44: 1.59357e-120.

    c = -0.4385011660546906785236563039401605476191507964755840798228440...
        (73 honest digits)

Gate re-run: **AGREEMENT = 74.13 digits**, |c - candidate| = 7.35787e-75
against sigma_c = 1.00398e-74, ratio 0.73. Fourth consistency point; the
sequence of |Delta|/sigma_c is now 1.10, 0.41, 0.75, 0.73 (still only four
points — L-028 stands).

**THE NEGATIVE RESULT, which is the useful part.** Revision 5 added 82 points
and bought 2 digits. Compare:

| step | points added | where | digits gained | digits per point |
|---|---|---|---|---|
| rev3 -> rev4 | +29 | s in [92,148], HIGH s | +13 | **0.448** |
| rev4 -> rev5 | +82 | s in [30,45] at 0.125, s in [46,88], LOW/MID s | +2 | **0.024** |

Points added at high s were worth roughly **19x more per point** than points
added at low s. I chose the low-s points deliberately, on the reasoning that
they were by far the cheapest per certified digit in Nystrom time (~10 s each
versus ~150 s at s = 149). That reasoning optimised **cost per point** when
the objective is **digits per point**, and those are not the same quantity.
The cheap points were cheap because they are nearly redundant.

Two mechanisms, both now measured rather than argued:
  * densely spaced low-s points produce near-duplicate rows in the design
    matrix (relative separation Delta_s/s ~ 4e-3 at the bottom of the grid),
    which is precisely the conditioning failure of L-031;
  * E3 degraded from 3.81e-114 to 6.92e-107 -- seven digits worse -- which is
    the conditioning penalty showing up directly in the noise amplification,
    even though E3 remains 32 digits below binding.

**This supersedes my reading of L-017 and partially reinstates L-013.** L-017
concluded from the s_min experiment that the extraction is order-limited, each
point buying one order. That is true but incomplete: an order bought at low s
is worth far less than an order bought at high s, and past some density it is
worth almost nothing while actively degrading conditioning. L-013's original
instinct -- that extending the range dominates densifying it -- was closer to
right than the correction I applied to it, though for a reason neither entry
identified: it is the s-LOCATION of the new points that matters, not the
count.

**Operational rule for Phase 1:** buy points at the largest s the certification
budget allows. Do not densify a region already sampled. Cost per point is the
wrong figure of merit.

---

## L-034 — PSLQ at D = 73: the SIX-element basis is now REPORTABLE

**Tag: VERIFIED.** 246 PSLQ calls logged this run (`out/pslq_calls.json`),
including every failure and every null-control call.

The threshold sweep in `run_pslq.py` was changed to step 1 across dps 22..55,
following L-030 -- the previous step-5 sweep resolved T only to +/-5, and
since P >= T is spent directly out of the digit budget, a 5-digit
over-estimate of T can skip a basis needlessly.

| basis size | measured T (step-1) | P | P+30 <= 70? | outcome |
|---|---|---|---|---|
| 8 | 45 | 45 | 75 > 70 — no | SKIPPED: needs D >= 78 |
| 6 | 35 | 35 | 65 <= 70 — yes | **REPORTABLE** |

The b = 8 threshold table shows the transition resolved: 3/3 spurious
relations at dps 43, 2/3 at 43, 1/3 at 44, 0/3 from 45 up. That is a
stochastic edge, not a sharp constant, and a standalone measurement an hour
earlier gave 44 rather than 45 for the same basis. T is a small-sample
estimate of the edge of a random phenomenon.

**Result on the 6-element basis {1, log2, logpi, gamma, zeta'(-1), zeta(3)/pi^2}:**

    +12*c - 1*log2 - 36*zeta'(-1) = 0        i.e.   c = (1/12) log 2 + 3 zeta'(-1)

    (a) found at P = 35, re-found at P+30 = 65, IDENTICAL coefficients  PASS
    (b) coefficient sup-norm 36 <= 10^4                                 PASS
    (c) perturbed control c*(1+1e-20): NO RELATION                      PASS
        random 30-digit control:       NO RELATION                      PASS
        P = 35 >= measured spurious threshold T = 35                    PASS

This is a strictly stronger adversarial result than L-023's 4-element hit:
**three** basis elements (`logpi`, `gamma`, `zeta(3)/pi^2`) were available and
all received coefficient exactly 0. The harness had five opportunities to
spend a spurious constant and took none.

**L-027 still applies in full.** `log2` and `zeta'(-1)` remain in the basis by
construction, so this is a stronger validation of the INSTRUMENT, not
independent evidence about `c`. The zero coefficients are evidence about the
instrument's selectivity, which is exactly what Phase 1 will depend on.

---

## L-035  VERIFIED / STRUCTURAL  Citation correction: I was right on Krasovsky, cannot confirm the fourth proof, and the primary announces THREE authors not four

Operator conceded the CMP 262 misattribution and reassigned that venue to
Ehrhardt. Applying the discipline symmetrically, I did not accept the
correction on their word either. Evidence, all from primary PDFs already
downloaded (`ehr.pdf` = arXiv:math/0401205v2, `kras.pdf` = math/0401258v2):

1. **Ehrhardt's venue remains UNCONFIRMED.** The arXiv API returns *no*
   `journal_ref` field for math/0401205. I therefore cannot confirm CMP 262
   (2006) 317-341 any more than I could confirm the operator's earlier CMP
   272 (2007). Both are third-party claims. OPERATOR-SUPPLY item OS-11.
   Note the operator has now given two different venues for Ehrhardt across
   two messages; that is itself a reason to require a primary.

2. **The third proof is announced by the primary, and the author list is
   Deift-Its-Zhou, NOT Deift-Its-Krasovsky-Zhou.** Krasovsky's own
   footnote 1, verbatim:

     "As this paper was being prepared for publication, an announcement by
      T. Ehrhardt claiming the same result as Theorem 1 (by a different
      method) was posted on the internet. A third solution to the problem
      by a Riemann-Hilbert approach (related to the present one) is in
      preparation by P. Deift, A. Its, and X. Zhou."

   So my earlier "unconfirmed by either primary" was too weak -- Krasovsky
   *does* announce it. But the operator's correction ("Four authors, not
   three") is contradicted by the primary announcement, which names three
   and does not include Krasovsky. An author list can of course change
   between announcement and publication, which is precisely why the
   published paper is needed rather than inferred. OS-11 covers this too.
   `arXiv` title/abstract search for "Widom-Dyson constant" returned zero
   entries across four query forms, so I could not resolve it in-session.

3. **What IS now primary-confirmed:** two independent proofs (Krasovsky by
   orthogonal polynomials on an arc; Ehrhardt "by a different method",
   independence attested by Krasovsky himself), plus a third in preparation
   by RHP. That is the structure the operator described; only the fourth
   paper's identity is unsettled.

4. **A convention datapoint that costs nothing and pins everything.**
   Ehrhardt's abstract and eq. (1) verbatim: `K_alpha` on `L^2[0,alpha]`
   with kernel `sin(x-y)/(pi(x-y))` -- note NO `s` parameter, the interval
   length carries it -- and the result is stated for `det(I - K_{2alpha})`,
   i.e. the operator on `[0, 2alpha]`, length `2alpha`. Our kernel is
   `sin(s(x-y))/(pi(x-y))` on `[-1,1]`; the substitution `u = s x` maps it
   to `sin(u-v)/(pi(u-v))` on `[-s,s]`, length `2s`. Hence `alpha = s`
   exactly, with no factor of 2 outstanding, confirming `a=-1/2, b=-1/4`.
   This is the third independent route to the same normalisation (the
   others being Krasovsky eq. (1)-(2) and the self-pinning argument of
   L-026), and it is now derived rather than asserted.

5. **Ehrhardt's abstract independently corroborates OS-9**: "The first and
   second order asymptotics of this formula have already been proved and
   higher order asymptotics have also been determined."

**Standing correction to my own record:** L-026 stated the third proof was
"unconfirmed by either primary". That was wrong -- I had the PDF in hand and
had not searched it for the announcement. Logged as an instance of failing to
interrogate evidence already in my possession, which is cheaper to fix than
any of the compute-bound failures in this ledger and was missed anyway.

---

## L-036  VERIFIED  The sigma-form ODE, DISCOVERED from our own data rather than recalled

The operator proposed subtracting known higher-order terms instead of
extrapolating them away, and pointed out that if the Painleve-V series can
supply everything except the constant, then the whole tail is derivable.
Correct -- but writing the sigma-form ODE down from memory violates HARD
RULE 1, and accepting it from the operator is the same violation one channel
removed. So the ODE was not written down. It was DISCOVERED.

**Method.** sigma(s) = s d/ds log det(I - K_s), with derivatives taken
analytically from the Nystrom matrix, never by finite differences:

    L'   = Tr(A^-1 A'),   L'' = Tr(A^-1 A'') - Tr(X^2),   X = A^-1 A'
    L''' = Tr(A^-1 A''') - 3 Tr(A^-1 A'' X) + 2 Tr(X^3)

exact because d^r/ds^r of sin(s d)/(pi d) is elementary. Validated against a
central difference: agreement 5.4e-19, i.e. at the finite-difference
truncation error, not at a bug.

A design matrix was then built over all 70 monomials in (s, sigma, sigma',
sigma'') of total degree <= 4, sampled at 82 values of s, and its nullspace
taken.

**First attempt failed, and failed informatively.** sigma ~ -s^2, so a
degree-4 monomial spans s^8; sampling s over [0.5,23] gave a design matrix
whose singular values decayed smoothly with NO gap, and the code reported 34
"null directions" -- all conditioning noise. Row and column equilibration
plus a narrow window s in [1,4] fixed it: the spectrum then showed
log10 singular values of -122.06, -76.55, -74.54, ... i.e. ONE genuine null
direction and a 45-order gap beneath the noise.

**Result.** Of 70 monomials, exactly six carry non-noise coefficients, and
all six are exact dyadic rationals; the other 64 sit at ~1e-49:

    -1/2 sigma^2 + 1/8 sigma sigma'^2 + s sigma sigma' - 1/8 s sigma'^3
    - 1/32 s^2 sigma''^2 - 1/2 s^2 sigma'^2  =  0

Multiplying by -32 and grouping with u = s sigma' - sigma:

    s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2 = 0                        (*)

**Out-of-sample confirmation** (sigma_ode_verify.py), at s far outside the
discovery window [1,4], relative residual |R|/max|term|:

    s=6   2.8e-79      s=9   1.6e-77     s=12  4.8e-75
    s=20  5.2e-69      s=30  5.3e-60

**Control, validated against its own resolution before being believed:** the
same functional with 16 -> 16.0000000001 gives 6.2e-12 at both s=9 and s=20,
some 48-65 orders above the unperturbed residual. The test has resolution to
spare, so the near-zero result is evidence rather than an absence of it.

Tag is VERIFIED, not STRUCTURAL: no theorem was cited. (*) is a statement
about our own numerics, established at stated precision with a working
control, and it is used below only to generate a tail that is then checked
against independent data.

---

## L-037  PROVEN (conditional on L-036)  The tail is a recursion; odd orders vanish identically; e_2 = 1/32

Substituting sigma(s) = -s^2 - 1/4 + sum_{m>=1} a_m s^-m into (*) and
matching powers gives a triangular recursion. **No parity was assumed** --
all m were carried.

Implementation refused to guess twice, both times correctly:
  - my first index offset was wrong and the code raised "equation vanished
    identically" rather than solving something else. Replaced by a loop that
    SCANS coefficients and picks up whichever unknown is newly present, and
    raises if two appear at once (non-triangular) or if a quadratic branch
    ambiguity appears.

**Results.**

    a_1 = 0     a_2 = -1/16     a_3 = 0     a_4 = -5/32     a_5 = 0
    a_6 = -131/128    a_8 = -6575/512    a_10 = -1080091/4096   ...

  1. **Every odd a_m vanishes identically, to m=400.** The even-only model
     that fit_constant.py has assumed since revision 1 on numerical evidence
     (ratio 0.035-0.047, L-029) is now a DERIVED consequence of (*), not a
     fitted assumption. This is the one place in the project where an
     evidence-backed modelling choice became a consequence.

  2. **e_2 = 1/32 exactly.** IQ-2 conjectured this from a numerical pattern
     and is hereby settled by derivation. All denominators are exact powers
     of two.

  3. The constant c does NOT appear anywhere in this recursion and cannot.
     sigma = s (log det)' annihilates it. That is the structural reason the
     constant needed a separate proof thirty years after the series, and it
     is also why nothing here can be circular about c.

**Two independent implementations.** sigma_recursion.py (sympy, symbolic)
and sigma_recursion_fast.py (exact Fraction arithmetic, polynomial
reconstruction by finite differences at a_m = 0,1,2 with an explicit raise if
the quadratic part is nonzero) agree on all 30 shared even orders with ZERO
mismatches. The fast path reached m=400 (200 orders) in 70 s after an
optimisation that stopped recomputing (sigma')^2 over the full series length
on every call -- a 400x speedup, from 200 s to 0.48 s at M=60.

---

## L-038  VERIFIED  c extracted with NO FIT at 132 digits; E1 is eliminated, not reduced

With the tail exact, the entire Richardson apparatus becomes unnecessary:

    c(s,M) = log det(s) + s^2/2 + (log s)/4 - sum_{m<=M} e_m s^-m

No design matrix, no extrapolation, no fitted nuisance parameters, no
conditioning wall (L-031), and no E1 budget line. c is read off as the
integration constant of (*).

**Optimal truncation is real and was predicted before it was measured.** The
term ratio implies the series turns around at m* ~ 2s; at s=149 the code
selected M* = 296 against a prediction of 298.

    s      cert.dig   M*    E_trunc      E_data
    100    177.3     198   4.39e-90     5.07e-178
    120    183.7     238   1.56e-107    1.93e-184
    140    189.1     278   5.67e-125    7.45e-190
    149    189.7     296   8.11e-133    2.13e-190

**The error bar is calibrated, and this is checkable in a way the fit's
sigma_c never was.** Independent s values must agree to within the truncation
bar, and they do -- consistently at ~80% of it:

    |c(100)-c(120)| = 3.65e-90   vs bar 4.39e-90
    |c(120)-c(140)| = 1.29e-107  vs bar 1.56e-107
    |c(140)-c(149)| = 4.71e-125  vs bar 5.67e-125

Three independent checks, all landing just inside a slightly conservative
bar. Contrast L-028, where |Delta|/sigma_c over four revisions could not fix
the scale to better than 2x.

**Result: 132.09 honest digits, agreeing with (1/12)log2 + 3 zeta'(-1) to
131.81 digits.**

Previous best was 73 honest digits from a 224-point grid and ~4 h of fitting
(L-033). This is from ONE data point, no fit, and ~70 s of recursion.

**What this says about the entire preceding effort.** Revisions 1-5 bought
36 -> 73 digits by buying grid points, and L-033 concluded the lever was
s-location rather than point count. Both were true and both were the wrong
axis. The binding constraint was never the data -- E_data was already
1e-190 at s=149, some 117 digits better than the answer we were reporting.
It was E1, the numerical annihilation of a tail that was analytically
available the whole time. Every point purchased after revision 3 addressed
the wrong budget line. The operator's instinct to attack E1 before selecting
Phase 1 targets was right, and the honest accounting is that ~6 h of grid
compute in this project bought 2 digits while 70 s of recursion bought 59.

---

## L-039  VERIFIED  The full 8-element basis is REPORTABLE, with five decoys silent

The b=8 basis was the point of the exercise: it is the only basis here
containing constants with no business in the answer, so it is the only basis
whose silence carries information. It needed D ~ 77-78 (L-030) and was
unreachable at 73 digits.

    basis: 1, log2, logpi, gamma, zeta'(-1), zeta(3)/pi^2, Catalan, log(1+sqrt2)
    P = 92   (>= 78 threshold; P+30 = 122 <= 132 honest digits)

    relation at P=92:    [-12, 1, 0, 0, 36, 0, 0, 0]
    relation at P+30:    [-12, 1, 0, 0, 36, 0, 0, 0]   IDENTICAL   (a) PASS
    sup-norm 36 <= 10^4                                            (b) PASS
    null control, perturbed c*(1+1e-20):  NO RELATION              (c) PASS
    null control, random 30-digit:        NO RELATION              (c) PASS

i.e. c = (1/12) log 2 + 3 zeta'(-1), with logpi, gamma, zeta(3)/pi^2,
Catalan and log(1+sqrt2) ALL receiving coefficient exactly zero. Five
opportunities to spend a spurious constant, none taken.

**L-027 still applies and is not weakened.** log2 and zeta'(-1) remain in the
basis by construction, so the hit itself is instrument validation, not
independent evidence about c. What is new is the selectivity: the instrument
now demonstrably declines five wrong answers at 92 digits. That, and not the
hit, is what Phase 1 depends on.

---

## L-040  Bug taxonomy, entries 6-8. All three are mine, all from this segment.

**(6) I violated my own newly promoted rule, in the file that cites it.**
sigma_recursion_check.py compared derived coefficients to certified data and
included a control perturbing e_2 by 1e-20. It printed results IDENTICAL to
the unperturbed run at every point. Reason: at s=30 the truncation floor is
1.3e-15 while a 1e-20 relative perturbation of e_2 moves the sum by 3.5e-25 --
ten orders BELOW resolution. The control was switched off and reported PASS.
This is exactly L-024, which I had promoted to a general rule and written
into that file's own docstring. Fixed by choosing the perturbation FROM the
measured floor (100x above it); it now degrades by ~99x as it should.
Lesson: promoting a rule to the spec does not make you follow it. The control
must compute its own resolution at runtime; a constant chosen by hand will
eventually be below it.

**(7) Silent basis shrink.** run_pslq_b8.py passed seven names to
constants.basis_values, four of them misspelled. The function silently
returns only the names it recognises. The run proceeded on a b=4 basis with
zeta'(-1) ABSENT and reported "NO RELATION" -- a clean-looking negative that
was structurally guaranteed. Caught only because b=4 was printed and looked
wrong. Now guarded with an explicit missing-name check that refuses to run.
Same genus as L-025: a correct-looking result from a silently wrong
configuration.

**(8) Vetting budget off by the bump.** P was chosen as honest_digits - 20 =
110, satisfying P <= digits. But condition (a) re-runs the search at P+30 =
140, which is ABOVE the 132 honest digits, so the reconfirmation searched our
own noise and returned NO RELATION -- reporting "not reportable" for a
relation that was correct and present. The constraint is
P + bump <= honest_digits, not P <= honest_digits. Fixed; P=92 now
reconfirms at 122 with identical coefficients.

Note the direction of failure differs across these three: (6) and (7) fail
REASSURINGLY (a control that cannot fire, a search that cannot hit), while
(8) fails conservatively. Only the first two are dangerous, and both were
invisible to every check except printing the configuration and comparing it
to what was intended.

---

## L-041  Gap-based selection: replacing a misleading artefact with a self-diagnosing one

sigma_ode.py originally selected null directions by a fixed tolerance of
1e-(dps/2), and reported "12 null direction(s) at 1e-60" when exactly ONE is
genuine. The arithmetic was not wrong -- the true vector was in the list, and
L-036 identified it correctly by taking the smallest singular value -- but the
printed artefact was misleading, and `out/sigma_ode.json` recorded n_null=12.
A fixed threshold cannot know where the relation stops and the conditioning
tail starts.

Replaced by selection on the largest spectral gap, which also RAISES if the
largest gap is under 10 decades ("conditioning-limited, not
information-limited"). Re-run reproduces the identical spectrum and now
reports:

    1 genuine null direction(s), selected by a spectral gap of 45.5 decades

This is the same failure genus as L-025 and L-040(7): the result was right
and the reported configuration was wrong, which is invisible to any check
except reading the output and comparing it to what was meant. Recording it
because Phase 1 will run this same nullspace machinery on relations whose
correct rank is NOT known in advance, and there a fixed tolerance would not
merely mislabel -- it would silently manufacture relations.

---

## L-042 -- OS-12 discharged: the discovered ODE is JMMS sigma-PV at x = 2s

Tag: PROVEN (the algebra) + STRUCTURAL (the identification, operator-sourced)

The operator supplied the Jimbo-Miwa-Okamoto sigma (Hirota) form as quoted by
Bornemann,

    x^2 tau''^2 + 4 (x tau' - tau)(x tau' - tau + tau'^2) = 0,

against my nullspace-discovered

    s^2 sigma''^2 + 16 u^2 + 4 u sigma'^2 = 0,   u = s sigma' - sigma.

I did not take the reconciliation on trust. Under x = lambda s with
sigma~(s) = tau(lambda s): u is invariant, sigma~'^2 = lambda^2 tau'^2, and
s^2 sigma~''^2 = lambda^2 x^2 tau''^2. Multiplying the standard form by
lambda^2 therefore moves ONLY the u^2 coefficient, as 4 lambda^2, while the
u sigma'^2 coefficient is scale-invariant. Hence 16 = 4 lambda^2, lambda = 2.

Checked two ways in-session, both independent of the literature:
  - symbolically: the difference of the two equations after substitution is
    EXACTLY 0 (sympy, not a numerical zero);
  - numerically: with tau(x) = sigma(x/2) the STANDARD form holds on my own
    certified data to 71 digits.

Two consequences, and the second is the one that matters.

(1) lambda = 2 is a FOURTH confirmation of the normalisation, and the only
    one that needs no literature convention at all -- it falls out of a
    coefficient ratio.

(2) DEPENDENCY CLASS CAN CHANGE WITHOUT THE ITEM CHANGING. I filed OS-12 as
    curiosity, with the explicit note "nothing depends on it", and that was
    accurate when written: the ODE was VERIFIED out of sample and c still
    came from a fit. It stopped being accurate the moment I read c off the
    recursion in L-038, because from then on all 132 digits rested on an
    equation whose only warrant was a numerical nullspace. Nothing about
    OS-12 changed; its load-bearingness changed underneath it. I did not
    notice, and would not have, absent the operator.

    The general rule, for Phase 1 and for the SIARC spec: an open item's
    priority must be re-derived whenever the dependency graph changes, not
    only when the item does. Filing is not a terminal state.

Note on tagging. The mathematical content here is PROVEN in-session. What
remains operator-sourced is only the IDENTIFICATION of the target equation
with the published JMMS sigma-PV -- i.e. the name, not the algebra. I have
verified my equation IS the equation the operator quoted; I have NOT
independently verified that the equation the operator quoted is the one in
Jimbo-Miwa-Okamoto. That residual stays STRUCTURAL pending a primary source
and is recorded as such, because the derivation chain for c now passes
through it.

---

## L-043 -- OS-11 discharged: two Ehrhardt papers, and DIZ -> DIKZ

Tag: STRUCTURAL (operator-sourced, consistent with my primary reads)

My L-035 flagged an apparent venue conflict for Ehrhardt. The operator
resolves it: there are two papers with near-identical titles.

  "Dyson's constant"   (singular) -- sine kernel        -- math/0401205
                                  -- CMP 262 (2006) 317-341
  "Dyson's constants"  (plural)  -- Wiener-Hopf-Hankel  -- math/0605003
                                  -- CMP 272 (2007) 683-698

I fetched and read the first; the operator's earlier K_{2 alpha} quotation
came from the second. Neither citation was wrong; they were presented as one
paper. arXiv carries no journal_ref for either, which is why my primary check
could neither confirm nor refute and correctly returned "unconfirmed" rather
than adjudicating.

On the fourth proof, both readings were right about different objects.
Krasovsky's footnote 1, which I read in the PDF, announces Deift, Its and
Zhou -- three authors, not including Krasovsky. The operator reports the
published paper as Deift, Its, Krasovsky, Zhou, JCAM 202(1) 26-47 (2007);
Krasovsky joined between announcement and publication. My caveat
"announcement is not publication" was therefore the operative distinction,
and the disagreement was never a disagreement.

Both items remain STRUCTURAL, not VERIFIED: I have not seen the JCAM paper
or the plural-title paper, only reports of them.

---

## L-044 -- Positive controls: the operator's mechanism does NOT work as stated, and why

Tag: VERIFIED (measured, both directions)

The operator's hardening item: I have been running null controls only, which
verify the instrument is silent when nothing is there -- indistinguishable
from an instrument that is switched off. Add positive controls: plant a known
relation and require recovery. Stated consequence: this "would have caught the
missing zeta'(-1) instantly, because a basis that can't find a relation it
contains is switched off."

I implemented it and tested it against the actual L-040(7) failure. THE CLAIM
IS FALSE AS STATED, and the measurement is unambiguous.

Planting over the basis that is PASSED IN cannot detect a basis that lost an
element, because the plant is built from the same shrunken list. Dropping
zeta'(-1) from b=8 and running the full pair:

    NULL-perturbed c*(1+1e-20)      -> NO RELATION      (null passes)
    NULL-random 30-digit constant   -> NO RELATION      (null passes)
    POSITIVE planted #0,#1,#2       -> recovered, recovered, recovered
    verdict                         -> INSTRUMENT OK

That is a clean bill of health issued to the exact configuration the control
was introduced to catch. The positive control is a genuine instrument, but it
measures a different quantity than the operator ascribed to it:

    positive control  -> is the instrument switched on?
                         (precision, tolerance, coefficient bound)
    basis-identity    -> is the instrument pointed at the intended basis?

These are orthogonal, and L-040(7) is entirely the second.

THE FIX. Plant over the DECLARED basis and search over the ACTUAL one, with a
nonzero coefficient forced on any declared element absent from the actual
list. Then a missing element makes the planted relation unfindable by
construction. Re-measured on the identical failure:

    POSITIVE planted #0,#1,#2       -> found=None x3
    verdict                         -> INSTRUMENT FLAGGED

and the intact b=8 basis still passes both halves, so the control is not
merely trigger-happy. Full b=8 driver re-run with the pair wired in:
relation [-12, 1, 0, 0, 36, 0, 0, 0] recovered, sup-norm 36, reconfirmed at
P+30, both controls passed.

The methodological point is larger than the patch. A control inherits its
validity from what it is built out of. Building a positive control out of the
suspect object tests the object against itself -- the same circularity as
L-039's PSLQ hit, which could only ever return the relation its basis
contained. The rule that generalises: A CONTROL MUST BE CONSTRUCTED FROM
SOMETHING THE SUSPECT PATH CANNOT INFLUENCE. Null controls satisfy this
trivially (a random constant is independent of everything). Positive controls
do not satisfy it by default, and the default is the dangerous case, because
it fails in the reassuring direction.

This is now the ninth instance in this session of a check producing a
plausible passing answer rather than an error -- and the first where the
faulty check was one introduced specifically to prevent that failure mode.
Recorded as a caution against treating hardening items as self-validating.

---

## L-045 -- Pre-registered prediction CONFIRMED: digits = 0.869*s + 2.7

Tag: VERIFIED (three points, prediction fixed in writing before measurement)

The operator derived, from my own measured optimal truncation m* ~ 2s, that
the post-truncation residual is the beyond-all-orders term of order e^(-2s),
hence

    digits ~= 2s / ln 10 ~= 0.8686 s

and predicted ~176 at s=200 and ~220 at s=250, with an explicit falsification
condition: a FLAT digit count would mean the binding constraint is Nystrom
evaluation, not series truncation, and would require a different fix.

I wrote the predictions and the falsification condition into
open_questions.md revision 5 BEFORE running prediction_test.py. This matters
because this session has already produced one law fitted after the fact and
then falsified (L-030, the fabricated T(b) = 5b+10); a prediction recorded
only after the numbers are in is not a prediction.

Measured (prediction_test.py, coefficients to M=600, exact rationals):

      s     cert     M*    2s      E_trunc     honest    pred   excess
    149  189.672    296   298   8.108e-133    132.09   129.4    2.69
    200  257.128    398   400   3.043e-177    176.52   173.8    2.72
    250  301.045    498   500   9.059e-221    220.04   217.3    2.74

Excess spread 0.05 digits over 101 units of s. Measured slope 0.8708 against
predicted 0.8686 (0.25% high). The law holds, and the constant offset behaves
exactly as an algebraic prefactor should -- it is an offset, not drift.

Two independent structures fall out and neither was fitted:
  - M* landed at 296, 398, 498 against 2s = 298, 400, 500. The optimal
    truncation tracks 2s with an offset of -2 at every point. Predicted
    before measurement in L-038 at a single s; now confirmed as a law.
  - E_trunc drops by ~44 decades per 51 units of s, i.e. 0.87/unit, the
    same slope from a completely different quantity.

CROSS-s CONSISTENCY, which no fit could supply:

    s=149 vs 200: diff 6.744e-133  bar 8.108e-133  ratio 0.832  ok
    s=149 vs 250: diff 6.744e-133  bar 8.108e-133  ratio 0.832  ok
    s=200 vs 250: diff 2.532e-177  bar 3.043e-177  ratio 0.832  ok

The ratio is 0.832 at all three pairs. The error bar is therefore not merely
conservative, it is CALIBRATED to within 20%, and its scale is derived from
the first omitted term rather than estimated from residuals. Contrast L-028,
where the fit's sigma_c could not be pinned to better than a factor of 2.

CALIBRATION GATE (0.3), restated at the new precision. Against

    c = (1/12) log 2 + 3 zeta'(-1)

    agreement: 219.765 digits, honest budget 220.04 digits.

The agreement sits AT the error bar, not beyond it -- which is the correct
outcome and is itself a check: an agreement exceeding the honest budget would
mean the budget was overstated. Phase 0.3 required 12 digits. We are at 219.8.

Accounting for the session, which is the part worth carrying forward:
    revision 1-3 grid, ~6 h compute ............  +2 digits
    sigma-PV recursion, 70 s ...................  +59 digits
    two extra certified points, ~10 min ........  +88 digits
The binding budget line moved twice, and both times the expensive activity
was addressing a line that had already stopped binding. Measure which term
dominates BEFORE buying more of anything.

Consequence for Phase 1, per the operator: required-basis-size has ceased to
be a constraint. The measured spurious thresholds give D >= max(T,31)+33, so
b=8 needs 77-78; at 220 digits there is 142 digits of headroom, and the law
says another 100 digits costs ~115 units of s at ~7 min each. Target
selection is now governed by literature provenance quality alone.

---

## L-046 -- Near-miss: `git add -A` staged 250+ unrelated files from other projects

Tag: VERIFIED (caught pre-push, reverted)

Recording because it was caught by reading output rather than by any check,
which makes it the same genus as L-025 and L-041, and because the failure
mode is worse than the ones already logged.

`git add -A` from inside toeplitz_phase0 stages from the REPOSITORY ROOT, not
the current directory. This repo hosts several unrelated projects. The commit
that resulted contained ~250 files from sectorial/, lean/, zenodo/,
program_graph/ and files/ -- including `check_prod_token.ps1` and
`set_prod_token.ps1`, i.e. scripts whose names indicate production
credentials. Reverted with `git reset --mixed 59f3830` (working tree
untouched, session rule: no deletion) and re-staged as `git add
toeplitz_phase0/`, giving the correct 15 files.

Three things worth stating plainly.

1. Nothing was pushed, and push is operator-gated by the session rules. The
   gate that would have contained this is a rule I was given, not a property
   of anything I built. That is not a defence; it is luck with a policy
   attached.

2. It was detected ONLY because the command echoed `git status --short` and I
   read it. Had I written `git add -A; git commit` without the status line,
   the commit would have been silent and plausible -- the ledger and code
   changes would all have been present and correct, with the contamination
   invisible in the summary. Once again: a correct-looking result concealing
   a wrong path.

3. The general rule this session keeps rediscovering, now in a tenth
   instance and in a new domain: THE SCOPE OF AN OPERATION IS NOT THE SCOPE
   OF YOUR ATTENTION. `-A` means the repo; the working directory does not
   narrow it. The same error shape as the null control that ran below its own
   resolution and the basis that silently lost an element -- an operation
   whose actual domain is wider or narrower than the one assumed, failing
   quietly in the direction that looks fine.

Standing rule for the remainder of this project: stage by explicit path
(`git add toeplitz_phase0/`), never `-A`, and always print `git diff --cached
--name-only` before committing. Recorded here rather than only in a config
file because L-044 established that promoting a rule does not make it
followed; the check must be in the command that is actually run.

---

## L-047 -- Full `verify` run from scratch: clean, no drift

Tag: VERIFIED (complete rebuild, exit code 0)

The operator's argument for not deferring this was L-025: a defect had been
found in the untested reproduction path BY INSPECTION, which is direct
evidence that the untested path harbours defects. Run now, before Phase 1, so
that the baseline is clean when the interesting numbers arrive.

`.\verify.ps1 verify` -- every stage from an empty out/, ~75 min, exit 0.
Log at out/verify_full.log. Stage results, all matching the incremental runs:

  smoke tests ............ 9/9 passed
  grid spec .............. BLOCKS generates 224 points; data file holds 224;
                           set equality both directions -- the L-025 defect
                           is confirmed fixed on the path that actually runs
  spd diagnostic ......... under-resolved (s=30,n=40) correctly RAISED
  node convergence ....... s=20: 13.7 -> 27.3 -> 42.6 -> 59.2 -> 77.0 -> 95.8
                           agreeing digits at n/s = 2.0 ... 4.5
  factored vs full ....... rel diff 2.3e-50 (s=1), 1.1e-49 (s=5)
  gate.py ................ agreement 74.133 digits vs 12-digit threshold;
                           CONSISTENT with the error bar; GATE PASSED
  run_pslq.py ............ NOT reportable at b=8 at the fit's precision, so
                           it shrank the basis per the pre-declared nesting
                           and reported at b=6. Correct behaviour: the fit
                           route has ~74 digits and b=8 needs 77-78.
  sigma_ode.py ........... 1 genuine null direction, gap 45.5 decades
  recursion .............. a_2 = -1/16, e_2 = 1/32, exact
  direct_c.py ............ agreement 131.81 digits (claimable 131.81)
  run_pslq_b8.py ......... reportable, [-12,1,0,0,36,0,0,0], controls passed

Two things worth noting rather than glossing.

1. The two PSLQ drivers DISAGREE on b=8, and that is correct. run_pslq.py is
   fed the FIT's c (~74 digits) and correctly refuses b=8; run_pslq_b8.py is
   fed the RECURSION's c (131.81 digits) and correctly reports it. A pipeline
   in which both reported would be one in which the digit gate was not doing
   anything. The disagreement is the gate working.

2. The default `verify` target reproduces 131.81 digits, not the 220.04 of
   L-045, because it uses the shipped grid (s <= 149) and M=400. The 220-digit
   result is reproduced by the separate `predict` target, which rebuilds the
   s=200/250 points and the M=600 recursion. Both were run to completion this
   session and both are reproducible from scratch; they are different targets
   with different costs, and the digit counts are not interchangeable.

No stage degraded, no stage was skipped except the two PSLQ searches that are
skipped BY DESIGN (running them at that precision would be a guaranteed-fail
protocol, not a test -- L-020).

---

## L-048 -- The full verify run exposed TWO defects, one of them in the
##          prediction test itself. Eleventh instance of the class.

Tag: VERIFIED (both defects reproduced, both fixed, fixes tested)

This is the strongest argument yet for the operator's insistence on running
the full rebuild before Phase 1: the run did not merely confirm the pipeline,
it FOUND THINGS. Neither defect was visible from any incremental run.

DEFECT 1 -- targets clobber each other's artifacts.
`verify` runs `sigma_recursion_fast.py 400`; `predict` runs it at 600. Both
write out/sigma_recursion_fast.json. Whichever ran last won. The full verify
therefore silently downgraded the artifact 600 -> 400 AFTER the 220-digit
result had been produced and committed.

DEFECT 2 -- and this is the bad one. The saturation guard did not fire.
prediction_test.py already contained a guard for exactly this: a point whose
optimal truncation lies outside the available series is a lower bound, not a
measurement, and must be excluded. It tested `M* >= orders[-1]`. With M=400
and s=250, the search selected M* = 398. 398 >= 400 is FALSE. The point was
scored as usable and the run reported:

    250  ...  M*=398  215.28 digits   excess -2.02
    verdict: CONSISTENT ... measured slope 0.8237

A wrong digit count, a wrong slope, a spread of 4.74 that squeaked under a
threshold of 5, and the word CONSISTENT. No error, no warning. Had I run the
full verify BEFORE producing L-045 rather than after, I would have published
0.8237 against a prediction of 0.8686, called it a near-miss, and gone looking
for physics in an artifact of a truncated coefficient file.

The guard was testing the wrong quantity. `M* >= orders[-1]` asks whether the
search hit the end of the array; the question is whether the MINIMUM was
reachable, i.e. whether 2s <= orders[-1]. Off by exactly the two orders
between 398 and 400.

This is the eleventh instance this session of a check that produces a
plausible passing answer rather than an error, and the SECOND (after L-044)
where the faulty check was one I had written specifically to prevent that
failure mode. The pattern is now unambiguous enough to state as a finding
rather than a caution: WRITING A GUARD IS NOT EVIDENCE THE GUARD WORKS. In
both cases the guard was correct in intent, plausible on inspection, and
wrong in a way that only firing it against a real failure could reveal.
Every guard needs its own positive control -- the same argument the operator
made for PSLQ, applied one level up, to the guards themselves.

FIXES, both tested by reproducing the failure and watching it flip:
  - saturation: `M >= orders[-1] or 2*s > orders[-1]`. Re-run against the
    M=400 file now prints "SATURATED (need M >= 500), lower bound only",
    excludes the point, and reports the honest two-point slope 0.8711.
  - verdict threshold tightened 5 -> 1.0 digits of spread. The true spread is
    0.05, so 1.0 is 20x margin; 5 was loose enough to pass the broken run.
  - sigma_recursion_fast.py now REFUSES to overwrite an artifact of higher M
    and says so, with --out= to write elsewhere. Verified: `600` writes,
    then `400` refuses.

After restoring M=600 the three-point result reproduces exactly: 132.09,
176.52, 220.04, excess 2.69/2.72/2.74, slope 0.8708. 9/9 smoke tests pass.

ALSO RECORDED, and it is the good news: certified_data.json rebuilt from
scratch is BIT-IDENTICAL to the committed file -- 224 rows, zero value
mismatches, no lost s. The expensive part of the pipeline is exactly
reproducible; the defects were both in the cheap orchestration around it.

---

## L-049 -- The assertion audit, and instance 12 exactly where predicted

Tag: PROVEN (the criterion) + VERIFIED (the finding)

The operator's sharpening: L-044 and L-048 are not merely "checks outside
their validity domain", they are checks whose ASSERTIONS ARE WRITTEN IN
TERMS OF QUANTITIES THE PATH UNDER TEST PRODUCES. That is checkable by
inspection rather than by insight, so it can be mechanised -- which matters
because two of the eleven instances were guards written specifically to
prevent the failure they then missed. An audit that depends on the auditor
noticing is the wrong instrument.

Built assertion_audit.py. It required TWO self-corrections, both caught by
running it against the known-broken and known-fixed guards before trusting
it -- i.e. by giving the auditor its own positive control, which is the
lesson of L-044 applied to the auditor.

  Attempt 1: judged each Compare separately. The repaired L-048 guard is
    `M >= orders[-1] or 2*s > orders[-1]`, a disjunction of sufficient
    conditions; judging clauses alone flagged the first and declared the
    FIXED code still broken. Also counted the `-1` in `orders[-1]` as an
    external referent, so it PASSED the broken guard. Both directions wrong.

  Attempt 2: asked "does the guard mention a declared symbol". On real code
    this reported 0 findings over 65 guards, because almost everything
    eventually traces to a parameter. Zero findings from an audit is
    indistinguishable from an audit that does nothing -- the same shape as a
    control that passes by being switched off.

  Attempt 3, the criterion that works: ARE THE TWO SIDES OF THE COMPARISON
    INDEPENDENT? Flag when the measured side and the threshold side share a
    computed ancestor.
        L-048: M <- best <- search(coeffs);  orders <- sorted(coeffs)
        L-044: want <- ks <- vals;           rel <- pslq_search(...) <- vals
    Both repairs severed exactly that link. The tool reports the shared
    ancestor by name, which makes each finding actionable rather than
    advisory.

RESULT over 28 files / 66 guards: 2 findings.

FINDING 1 -- sigma_recursion_check.py, the resolution control. INSTANCE 12,
and it is a tautology. The perturbation was scaled FROM the floor,
`eps = 100*floor/term2`, and then the verdict asserted `cerr > 10*floor`.
Since cerr is ~100*floor by construction, the assertion reduces to
`100 > 10`. Measured ratios: 101, 99, 99. THE CONTROL COULD NOT FAIL FOR ANY
INPUT. It printed PASS three times and told us nothing.

This is worse than the L-024 case it was written to fix. There the control
was below its resolution and silent; here it is above its resolution and
loud, and still measures nothing, because the thing it compares against is
derived from the thing it measures. Being 'validated against its own
resolution' is not sufficient if the validation is circular.

  Replaced with the non-vacuous quantity: the RESOLVING POWER
  eps_min = floor/term2, the smallest relative error in e_2 the data could
  detect, compared against a threshold DECLARED IN ADVANCE
  (E2_RESOLUTION_TARGET = 1e-6). Measured: 4.6e-25, 3.2e-42, 1.4e-52 at
  s = 30, 60, 89. Plus a two-sided control -- a perturbation a decade ABOVE
  eps_min must be detected (True) and one a decade BELOW must not (False).
  Both directions now, so the instrument is shown to be neither deaf nor
  hallucinating, and the test can genuinely fail.

FINDING 2 -- gate.py, `consistent = diff <= 10*sigma`. Real, and it is L-028
rediscovered mechanically: sigma_c is produced by the same fit whose accuracy
it certifies. WAIVED, with the reason written next to the guard, because the
gate DECISION is `agree >= GATE_DIGITS`, which compares against the external
closed form and a declared threshold; `consistent` is diagnostic only.

Waivers are counted and PRINTED, never hidden. Accepting a finding by
deleting the check or loosening the tool would make the audit self-defeating
in precisely the way this ledger keeps documenting.

Wired into test_smoke.py with BOTH halves: the codebase must be clean AND the
auditor must still flag the historical L-048 shape. 10/10 pass.

---

## L-050 -- CORRECTION to L-045: the excess is NOT flat, and the error was mine

Tag: VERIFIED (91-point fit, plus a 3-point confirmation)

L-045 reported "excess spread 0.05 digits over 101 units of s ... an offset,
not drift", and concluded the remainder is a pure prefactor. The operator
built on that, inferring a constant multiplicative factor with no algebraic
correction and bounding any power s^-a by |a| <= 0.22.

BOTH CONCLUSIONS ARE WRONG, AND THE CONTAMINATION ENTERED IN MY CODE.

prediction_test.py compared measurements against a hardcoded dict
    PREDICTED = {149: 129.4, 200: 173.8, 250: 217.3}
These are 2s/ln(10) rounded to one decimal -- but rounded in DIFFERENT
DIRECTIONS: -0.020, +0.082, +0.153. That injected a spurious -0.173 drift
across s in [149, 250], which nearly cancelled the real +0.222 drift and left
a residue of +0.05 that read as flat.

    s      exact 2s/ln10   hardcoded   round err   excess(exact)  excess(hard)
    149      129.419756      129.4      -0.0198       2.67024        2.69
    200      173.717793      173.8      +0.0822       2.80221        2.72
    250      217.147241      217.3      +0.153        2.89276        2.74

With exact predictions the excess drifts by 0.2225 over the range, against
log10(250/149) = 0.2248. Ratio 0.998.

INDEPENDENT CONFIRMATION, and it came first. A 3-parameter fit
    digits(s) = A*s + a*log10(s) + B
over 91 certified points, s in [60, 250]:

    window     n      A            a          rms
    s >=  60   91   0.868599146   0.994141   1.97e-5
    s >=  80   71   0.868596604   0.994979   8.05e-6
    s >= 100   52   0.868595196   0.995505   3.32e-6
    s >= 120   32   0.868594215   0.995908   1.73e-6
    s >= 140   12   0.868593015   0.996430   7.42e-7
                    2/ln10 = 0.868588964

A converges monotonically to 2/ln(10) and a converges monotonically to 1,
with the rms residual falling 27x as the window moves out -- the signature of
an asymptotic law, not a fitted coincidence. Competing hypotheses on 91
points: a free gives rms 1.97e-5; a = 1/4 gives 0.0194; a = 0 gives 0.0259.
The a = 0 hypothesis is worse by a factor of 1300.

CONCLUSION (VERIFIED): the beyond-all-orders remainder is

    E_trunc ~ C * exp(-2s) / s        with a = 1, not 0

So there IS an algebraic prefactor, it is 1/s, and the operator's "clean
structural fact measured for free" was measured off my contaminated numbers.

Three things worth stating.

1. The general rule, and it is new in this session: NEVER COMPARE A
   MEASUREMENT AGAINST A ROUNDED PREDICTION. The rounding here was 0.15
   digits against an effect of 0.22 digits -- the same order as the signal.
   Rounding a prediction for display is fine; storing the rounded value and
   subtracting it is not.

2. It is the aliasing failure of L-030 in a new costume. There, validation
   points sat on the lattice used for fitting. Here, the prediction was
   quantised at a scale comparable to the effect. Both are "the design was
   confounded with the parameter", and both produced a plausible null.

3. On provenance: the operator's inference was sound given the inputs, and
   the inputs were mine. The lesson is not that the operator erred; it is
   that a derived claim inherits the contamination of its inputs silently,
   and that pre-registering a prediction protects against fitting after the
   fact but NOT against a biased comparison baseline. The pre-registration in
   L-045 was genuine and is untouched; what failed was the yardstick.

FIXED: prediction_test.py now computes 2s/ln(10) exactly at full precision;
the verdict reports spread/log10(s_max/s_min) as a direct estimate of a and
names the 1/s prefactor. The smoke test now asserts a ~ 1 rather than
asserting flatness -- the previous assertion would have locked the artifact
in. New: excess_structure.py, run as part of `verify.ps1 predict`.

The slope claim of L-045 survives unchanged and is strengthened: A agrees
with 2/ln(10) to 5 significant figures across 91 points. Only the reading of
the excess is corrected.

---

## L-051 -- The sigma -> -sigma sign trap, resolved by data (2nd instance)

Tag: VERIFIED

The operator supplied a SECOND rendering of the sigma-form, by the same
author, with the opposite sign on the cross term:

  (P) arXiv:0804.2543   x^2 s'' ^2 + 4u^2 + 4u s'^2 = 0,  sigma ~ -x/pi - x^2/pi^2,
                        det = exp(+int_0^{pi s} sigma/x dx)
  (M) arXiv:0904.1581   x^2 s'' ^2 + 4u^2 - 4u s'^2 = 0,  sigma ~ +x/pi + x^2/pi^2,
                        det = exp(-int_0^{pi s} sigma/x dx)
      (u = x sigma' - sigma)

Not a contradiction: (M) is the sigma -> -sigma image of (P). Under that map
u -> -u, so u^2 and x^2 sigma''^2 are invariant while u sigma'^2 flips. Each is
internally consistent. The hazard is entirely in MIXING them: take the ODE
from one paper and the initial condition or the exponent sign from the other
and you get a wrong answer with no error raised.

Both are secondary renderings of JMMS 1980, so OS-13 REMAINS OPEN at the
primary level. But the trap can be disarmed without resolving OS-13, because
the discriminant is observable in our own data: the SIGN OF SIGMA NEAR 0.

sigma_sign_trap.py, with tau(x) = sigma(x/2), x = 2s:

     s      sigma(s)      resid (P)     resid (M)
   0.25    -0.188422       0.0          5.19e-2
   1.00    -1.260270      -7.7e-121      6.67
   8.00   -64.251102      -1.8e-114      3.26e4

sigma < 0 near the origin, because log det is DECREASING. Our convention is
(P) / arXiv:0804.2543, and (P) is satisfied to the ambient precision floor
while (M) fails by 121 orders of magnitude. No source was consulted to decide
this; the residual decided it.

SECOND INSTANCE of the rule from L-036: CONVENTION TRAPS ARE ADJUDICATED BY
THE NUMERICS, NOT BY THE SOURCE. First instance was alpha vs 2*alpha, where a
factor-lambda error shifts c by -(1/4)log(lambda) and the fit refuses the
wrong convention. The pattern now has a general form worth stating: whenever a
target has a KNOWN LOG COEFFICIENT or a known sign structure, the numerics
adjudicate the normalisation, which inverts the usual dependency on the
literature. Carry into Phase 1, where XX-chain and EFP conventions are more
varied than the sine-kernel case.

Consistency check, algebraic and literature-free: multiplying (P) through by
lambda^2 under x = lambda*s sends the u^2 coefficient 4 -> 4 lambda^2 while
leaving the u sigma'^2 coefficient fixed. Our numerically-discovered ODE has 16
and 4, so lambda = 2 exactly -- an independent confirmation of the x = 2s
normalisation requiring no convention from any source.

DEPENDENCY-CLASS NOTE, which is the operator's point and is general: the 132
digits rest on an ODE found by numerical nullspace. That was tagged VERIFIED
and recorded as "nothing depends on it". Reading c off its recursion made it
load-bearing WITHOUT THE ITEM ITSELF CHANGING. AN ITEM'S DEPENDENCY CLASS CAN
CHANGE WHILE THE ITEM DOES NOT, so "nothing depends on this" must be re-checked
whenever anything new is derived, not recorded once.

---

## L-052 -- Credential history check: clean

Tag: VERIFIED

Following L-046 (`git add -A` from a subdirectory stages from the REPO ROOT,
which nearly committed an unrelated token script), the operator asked the
sharper question: was it ever committed in EARLIER history?

    git log --all --oneline -- '*set_prod_token*'   -> empty
    git log --all --oneline -- '*token*'            -> empty
    git ls-files | findstr /i token                 -> empty

Nothing matching was ever tracked, on any branch or ref. The sibling trees in
this repository have history but contain no token files.

The near-miss remains a real defect in procedure even though it caused no
leak. Standing rule, already in force since L-046: stage by explicit pathspec
(`git add toeplitz_phase0/`) and print `git diff --cached --name-only` before
every commit. A miss that happens not to land is still the same miss.

---

## L-053 -- A and the prefactor exponent DERIVED, not fitted; and C = 1/pi

Tag: PROVEN (A and theta, symbolic) + VERIFIED (beta, and the prefactor check)
     + CONJECTURED (the identification C = 1/pi)

L-050 MEASURED E_trunc ~ C exp(-2s)/s by fitting 91 honest-digit counts. The
operator's point: that exponent was derivable a priori from the ODE we already
have, so my "no algebraic prefactor" claim was refutable before either of us
looked at a residual. Correct. Three routes now, deliberately disjoint.

ROUTE 1 -- WKB (symbolic, exact). Linearizing s^2 sigma''^2 + 16u^2 + 4u
sigma'^2 = 0 about the perturbative solution gives a 2nd-order LINEAR ODE for
delta. Result:

    leading delta' coefficient p0 = 0     <- the cancellation that makes A finite
    leading delta  coefficient q0 = -4
    => S0^2 = 4, decaying branch S0 = -2
    => delta_sigma ~ C s^(1/2) exp(-2 s)

so A = 2 and theta = 1/2, both EXACT RATIONALS out of the Riccati solve.
Next Riccati orders 5/16, -5/32, 593/1024 -- all rational, which is a check
in itself. C is a Stokes constant and linearization cannot fix it; that is
precisely why C must be measured and the exponents must not be.

ROUTE 2 -- large-order growth (uses no differential-equation manipulation).
With e_m ~ K Gamma(m+beta)/A^m, r_m = e_{m+2}/e_m = (m+beta)(m+beta+1)/A^2,
so beta = (sqrt(1+4A^2 r_m) - 2m - 1)/2 in closed form. Over the 300 exact
rational e_m we already hold:

    A free (independent of route 1):  A = 2.000000000000000000  (|diff| 8.1e-33)
    A = 2 imposed:                    beta = -1/2 to 1.0e-31

    Neville degree     8        12       16       20
    beta            -0.49999.. -0.5     -0.5     -0.5

The two passes are reported separately ON PURPOSE. Pass (b) imposes route 1's
A and is therefore NOT an independent confirmation of A; calling it one would
be L-039 again.

ROUTE 3 -- the measurement, L-050: a = 0.9941 (s>=60) -> 0.9964 (s>=140).

RECONCILIATION, and this is where I had it wrong first. THREE DIFFERENT
EXPONENTS, and conflating any two is a mistake:

    (i)   trans-series in log det :  s^(beta)      exp(-A s)
    (ii)  trans-series in sigma   :  s^(1+beta)    exp(-A s)
    (iii) least term / optimal truncation, which is what an honest digit
          count measures :          s^(1/2-beta)  exp(-A s)

(ii) is the WKB output. (iii) is L-050. They differ by sqrt(s) AND by the
derivative. The sqrt is Stirling: m* + beta = A s, and
Gamma(m*+beta)/(As)^(m*) = sqrt(2 pi) (A s)^(beta-1/2) exp(-A s). So the
honest-digit count measures something strictly SMALLER than the trans-series
term, and a naive "check b against the measured a" comparison fails by 1/2
for reasons that have nothing to do with either being wrong.

MY ERROR, logged rather than quietly corrected: I first wrote the dispersion
relation with s^(-beta) instead of s^(+beta). That put theta off by exactly 1
(predicted 3/2 against the WKB's 1/2) and produced beta = -0.607 out of a
broken extrapolator, which I nearly read as "beta is not a half-integer". Two
independent defects pointing the same way. The correct relation, from
e_m = (1/2 pi i) int_0^inf Disc f(w) w^(-m-1) dw with w = 1/s and
Disc f ~ C w^(-beta) exp(-A/w), is e_m = (C/2 pi i) A^(beta-m) Gamma(m+beta).

SECOND DEFECT, worth its own note: my Richardson was first-order only.
Repeatedly applying a single 1/m-eliminating step does NOT accelerate -- after
the first pass the 1/m term is gone and the operator keeps removing a term
that is not there. Replaced with Neville extrapolation in 1/m, which removes
1/m, 1/m^2, ... in turn. beta went from -0.607 (unusable) to -0.5 (31 digits)
with no new data. The data was never the limit; the extrapolator was.

RESULT:  a = 1/2 - beta = 1  EXACTLY, derived from the ODE with no reference
to any digit count. Measurement converges to it monotonically from below.

PREFACTOR, normalization-free. Rather than argue about what the honest-digit
count is normalized by, compare the closed-form least term against the
smallest term of the series actually evaluated:

     s     m*    actual         predicted      ratio
    149    298   8.108428e-133  8.126588e-133  0.99777
    200    400   3.043011e-177  3.048087e-177  0.99833
    250    500   9.059205e-221  9.071292e-221  0.99867

Ratio -> 1 monotonically. The law is confirmed including its prefactor.

C = 1/pi (CONJECTURED). K = lim e_m A^m/Gamma(m+beta) = 0.253974543736964,
giving C = K sqrt(2 pi) A^(beta-1/2) = 0.31830988618379067153776752674503.
Agreement with 1/pi, by Neville degree: 26.9, 37.7, 46.8, 54.6, 61.3, 64.2
digits -- MONOTONE IN THE DEGREE, so the limit is the extrapolator, not a
discrepancy. At least 64 digits.

ON THE DISCIPLINE HERE, because this is exactly the adjacent target the
operator warned would eat a Phase 1. I did not go looking for C. It was
computed to check the prefactor of the measured law, which is legitimate
validation, and it then landed on a value recognisable by inspection. NO PSLQ
WAS RUN. No basis was constructed. Reporting the digits of agreement with one
declared candidate is not a search and consumes no Phase 1 budget; suppressing
a 64-digit match once seen would be a different kind of dishonesty.

It stays CONJECTURED, and the reason is not modesty: 1/pi is the most
prior-heavy constant available, so a one-term match against it carries far
less evidential weight per digit than a vetted PSLQ relation with null and
positive controls. What would consume Phase 1 is trying to PROVE it. Queued.

---

## L-054 -- Provenance defects propagate into the OPERATOR's reasoning

Tag: STRUCTURAL (the operator stated the rule about their own inference)

The operator inferred a <= 0.22 from a spread of 0.05. That spread was a
DERIVED COLUMN of prediction_test.py -- an output of the very path under test
(L-050). Their words: "I reasoned from an output-derived quantity as though it
were data, which is the input/output-provenance failure applied one level up,
to me."

Recorded as a rule because it generalises past this session:

  AN OPERATOR'S REASONING INHERITS THE PROVENANCE DEFECTS OF WHATEVER COLUMN
  IT READS. A derived column handed upward carries no marking that it is
  derived, so the recipient cannot apply the classification even if they know
  the rule.

Practical consequence, and it is on ME, not on them: the fix is at the
producing end. Reported tables must mark each column as measured or derived,
because the consumer cannot recover that. prediction_test.py now prints the
prediction formula rather than a bare residual column, for this reason.

This is the eleven-instance bug class escaping the codebase into the
conversation. It is the same failure -- an assertion (here, an inference)
whose constraining term came from the path under test -- and the audit tool
cannot see it, because the tool only reads Python.

---

## L-055 -- Two tool extensions, and both found live defects immediately

Tag: VERIFIED

(A) TRANSCRIBED NUMERIC LITERALS. L-050's root cause was not a circular guard;
it was a value TRANSCRIBED at authoring time rather than computed at runtime.
The special rule was "never subtract a rounded prediction"; the general rule
is NO TRANSCRIBED NUMERICS IN VERIFICATION CODE, and unlike the guard
criterion it is genuinely grep-able.

Discriminant between a SPECIFICATION and a TRANSCRIPTION is precision: a
declared threshold is round by construction (10, 1e-17, 0.5), a transcribed
value carries >= 3 significant digits. Integers are exempted -- they are
overwhelmingly counts, node numbers and precisions, i.e. inputs.

FIVE FINDINGS ON FIRST RUN, and four are the same constant as L-050:

    extend_adaptive.py:61   0.866 * s        precision budget
    extend_data.py:41       0.866 * s        precision budget
    highs_points.py:46,47   0.869 * s        certification target and floor
    sinekernel.py:313       3.3219280948873626 * dps   (= log2(10))

0.866 and 0.869 are transcribed roundings of 2/ln(10) = 0.8685889638065035 --
the SAME constant whose rounding produced L-050, used four more times, in the
code that sizes the precision budget. 0.866 understates the budget by 0.65
digits at s=250. Not fatal, because the margins are +15..+60, but it is the
identical defect sitting in the path that decides how much precision to buy.

All five replaced with computed values (a module-level DIGITS_PER_S = 2.0 /
math.log(10.0), and math.log2(10)). Audit now reports 0. Wired into the exit
code, so it fails the build.

(B) MUTATION TESTING. The broken/fixed fixture is the general answer to "is
this checker switched off", and it mechanises: perturb what a check reads and
require it to notice. A check that survives mutation of its own inputs is
dead, whatever it prints.

THE HARNESS WAS ITSELF BROKEN TWICE, both times in ways it exists to detect.

  (b1) Scope. A uniform sample over out/ reported 0 kills in 36 -- but out/ is
       dominated by PSLQ call logs and superseded snapshots, so the sample
       measured the shape of the directory. Rescoped to the artifacts the test
       file actually opens, discovered FROM the test source.

  (b2) ITS OWN RESOLUTION -- instance 12's lesson, in the tool built to find
       instance 12. Run at a single relative perturbation of 1e-6 it reported
       2 kills of 36. But `assert 0.85 < slope < 0.89` CANNOT notice a 1e-6
       nudge. "Survived" was conflating no-check-exists with
       check-is-coarser-than-the-probe, and it fails in the reassuring
       direction: it makes live checks look dead and invites redundant ones.
       Replaced the fixed perturbation with an ESCALATING LADDER
       (1e-6, 1e-3, 1e-1, 1.0) reporting the SENSITIVITY THRESHOLD. Three of
       the four kills need rel >= 1e-3, so three of four were mis-scored.

THE FINDING THAT MATTERED: certified_data.json rows.N.value SURVIVED A 100%
MUTATION. The most load-bearing field in the project -- the certified
determinant values -- was constrained by nothing in the fast suite. Only
`verify` touched it, at a cost of hours, so between full rebuilds it was
effectively unchecked. This is not a check that failed; it is a check that was
never written, and no amount of inspecting existing guards would have found it.

Closed with test_certified_values_are_constrained_by_the_recursion: each row
compared against -s^2/2 - (1/4)log s + c_closed + sum e_m s^-m, using the
EXTERNAL closed form and the exact rational coefficients. 0.1 s for the whole
grid. Agreement runs 20.8 digits at s=30 to 80+ at s=113, truncation-limited
as it must be. rows.N.value now dies at rel=1e-6.

Stated honestly in the test's own docstring: the sigma-ODE behind those e_m
was discovered from a subset of this same grid, so this is a CONSISTENCY check
and cannot promote the values. What it does is detect corruption of any single
row, because a global smooth relation is violated by a local edit -- which is
exactly the liveness property that was missing.

AND THE AUDITOR CAUGHT MY NEW TEST. On first write it flagged two guards in
test_certified_values_..., correctly: `min(hi) > max(lo)` puts the data under
test on both sides, so a uniformly corrupted grid would satisfy it. In
flagging it, it also exposed a plain `lo`/`hi` VARIABLE SHADOWING BUG two
lines up, where the declared range unpack was clobbering the agreement split.
A tool written to catch a class of bug catching an unrelated bug in code
written the same hour, by static provenance alone, is the strongest evidence
so far that the criterion is tracking something real.

Both fixed by anchoring the constraining side on declared floors.

Remaining survivors, recorded rather than closed: wall_seconds, attempts, n0,
dps0, precision_bump_digits, meta.s_min/s_max/s_step. These are provenance
metadata, not claims. A field carrying a VERIFIED claim must be killed; a
field recording how long something took need not be.

---

## L-056 -- Where the pi in C = 1/pi comes from. Answer: partially my bridge.

Tag: VERIFIED (the discrimination) + CONJECTURED (the identification, still)

The operator's challenge was sharp and cheap: resurgence bookkeeping carries a
1/pi, so a stray factor would produce exactly the observed result -- a constant
reading 1/pi when the truth is 1, or pi when the truth is 1. Which route
produced the 64 digits, and does it contain a pi?

THE HONEST ANSWER IS "PARTIALLY YES", and the two halves must be separated.

HALF 1 -- the amplitude, which has NO bookkeeping freedom.
    K = lim e_m A^m / Gamma(m + beta) = 0.2539745437369638791430532197385...
The e_m are exact rationals; A = 2 and beta = -1/2 are exact rationals from
the linearization. There is no convention to get wrong. Gamma(m-1/2) does
supply a sqrt(pi), but that is what Gamma IS at half-integer argument -- it
means pi genuinely appears in the answer, not that I imported it.

HALF 2 -- the bridge, which DOES contain a sqrt(2 pi).
    C = K sqrt(2 pi) A^(beta - 1/2)
The sqrt(2 pi) is Stirling, from the optimal-truncation step. This is exactly
the step the operator flagged, and the concern is legitimate: a factor slipped
here moves C by 2.5066 and no algebra would complain. DISCLOSED, not defended.

Three defences, all computed, none of which is "1/pi is a nice number".

(D1) THE PI EXPONENT IS PINNED BY THE DATA, NOT CHOSEN BY ME. Scanning
     K * pi^p / sqrt(2) over half-integer p:

       p     K pi^p / sqrt2
      -1/2   0.10132118364233777144
       0     0.17958712212516656169
       1/2   0.31830988618379067154
       1     0.56418958354775628695
       3/2   1.0                        <== EXACTLY 1
       2     1.77245385090551602730
       5/2   3.14159265358979323846
       3     5.56832799683170784528

     K = sqrt(2) pi^(-3/2) to 64.3 digits. The neighbours are not near
     misses; they are unrelated irrationals. Had I lost or gained a
     sqrt(pi), the clean rung would sit at p = 1 or p = 2. It does not.

(D2) THE STIRLING BRIDGE IS VALIDATED, NOT ASSUMED. The least-term check
     compares the closed form against the smallest term of the series
     computed DIRECTLY from the coefficients -- no Stirling on the actual
     side. Ratios 0.99777, 0.99833, 0.99867 at s = 149, 200, 250, rising
     toward 1. A dropped or doubled sqrt(2 pi) would put these at 0.399 or
     2.507. This is the check that actually discriminates.

(D3) THE NAMED RIVALS ARE EXCLUDED BY THE MEASURED K.
       C = 1     requires K = 0.79788456080286535588
       C = pi    requires K = 2.50662827463100050242
       C = 1/pi  requires K = 0.25397454373696387914  <== measured
     Not close. The operator's specific failure mode is falsified, not
     argued away.

A CAVEAT THAT CUTS THE OTHER WAY, recorded because leaving it out would be
the more comfortable choice: THE INVARIANT ACTUALLY MEASURED IS
K = sqrt(2) pi^(-3/2), which nobody would call a clean constant on sight.
"1/pi" is that number times sqrt(2 pi)/2. So part of the apparent simplicity
is manufactured by the normalisation, and the aesthetic pull of the simpler
form is not evidence. The tag stays CONJECTURED.

ON THE UPGRADE PATH. The operator is right that more digits do not help: a
post-hoc-recognised candidate does not improve at 200 digits. What moves it is
a second, structurally different consequence of the same hypothesis -- the
two-instanton coefficient at exp(-4s), which resurgence fixes in terms of C.
We hold 300 exact e_m and the machinery is built, so it is hours not weeks.
NOT RUN. Queued in OS-15 by the operator's own instruction, and the whole
point of the stopping rule below is that "it is only hours" is precisely the
argument that has kept Phase 0 open for four rounds.

---

## L-057 -- The third failure category, and the boundary of automation

Tag: STRUCTURAL (operator-stated), recorded as a known bounded gap

The two tools cover different failures, and it is worth naming that they were
built a week apart for different reasons:

  assertion_audit.py  -- checks that EXIST BUT CANNOT FAIL   (broken guards)
  mutation_test.py    -- checks that WERE NEVER WRITTEN      (absent guards)

THE RESIDUAL THIRD CATEGORY: checks that exist, fire, and assert the WRONG
THING. A mutation kill proves SENSITIVITY, NOT CORRECTNESS. A guard asserting
`slope < 0.89` when it should assert `slope < 0.87` kills mutants happily and
reports green while permitting the error it was written to exclude.

Neither tool can see this, and it is not an implementation gap. Both tools
reason about PROVENANCE and RESPONSIVENESS -- structural properties of the
code. Whether a threshold is the RIGHT threshold is a claim about the
mathematics, which no static or dynamic analysis of the code can supply.

Partial coverage exists: the broken/fixed fixture pins intended behaviour at
one point, and the two-sided control in sigma_recursion_check.py pins it from
both directions. Both work by encoding the correct answer somewhere the tool
can compare against. That generalises only as far as someone is willing to
write the expected behaviour down.

LOGGED AS A BOUNDED, KNOWN GAP rather than left implicit, because an implicit
gap in a verification toolchain is indistinguishable from a claim of coverage.
The tooling reduces the review surface; it does not eliminate it. Every
threshold in this repository remains a human judgement, and the honest
statement of what the toolchain buys is: it guarantees the checks are alive
and non-circular, and says nothing about whether they are right.

---

## L-058 -- Three times the binding constraint was analysis, not data

Tag: VERIFIED (three instances, all in this ledger)

The operator's pattern, and it holds:

  1. E1 (order truncation) was going to be solved by more grid points. It was
     dissolved by the sigma-PV recursion instead -- exact subtraction rather
     than numerical annihilation. No new data (L-042).
  2. Densification bought 0.024 digits per point. The information lives in the
     RANGE of s, not the count; nearly collinear rows add nothing (L-031).
  3. beta came out -0.607 and I nearly read that as "beta is not a
     half-integer". Fixing the extrapolator -- Richardson was first-order
     only -- moved it to -0.5 at 31 digits WITH NO NEW DATA AT ALL (L-053).

Three times the instinct reached for more data; three times the limit was in
the analysis. Instance 3 is the sharpest, because the data had been sitting
there for two sessions already holding 31 digits of an answer I was reading as
0.4 digits.

PRE-COMMIT FOR PHASE 1, adopted: BEFORE BUYING COMPUTE, WRITE DOWN THE
ARGUMENT FOR WHY THE CURRENT LIMIT IS DATA RATHER THAN STRUCTURE. Not a
gesture -- a written argument that can be wrong, recorded before the spend, so
that the fourth instance is caught rather than counted afterwards. On this
track's record the prior is strongly against data being the limit.

Note the connection to L-049's criterion: "we need more data" is itself an
assertion, and its constraining term has consistently been an output of the
analysis under test.

---


---

## L-059 — The Phase 0 stopping rule, written as a check rather than a paragraph

Tag: **STRUCTURAL** (process). Artifact: `phase0_status.py`, `out/phase0_status.json`.

The operator's observation is correct and is the most important thing said
this session: this is the fourth consecutive round in which closing the
outstanding items opened more, every round was worth doing, and *that is
precisely what makes an indefinitely expanding Phase 0 invisible from
inside*. Calibration was meant to earn the right to make a Phase 1 claim. It
has since produced a rediscovered sigma-PV form, derived trans-series
exponents, a 60x precision improvement and a reusable verification
toolchain, and Phase 1 has still not started.

L-036 already established that promoting a rule to the spec does not make me
follow it -- I broke the rule inside the file that cited it. A stopping rule
written as prose is therefore predicted to fail. It is written as an
executable check instead.

THE RULE, as implemented:

  Phase 0 CLOSES when six mechanical conditions pass AND the triage table's
  provenance cells are filled from primaries (entry condition #11).

  Once the MECHANICAL conditions pass, the queue (`open_questions.md`) is
  the DEFAULT DESTINATION for every new finding -- not a judgement call per
  item. "It is only hours" is not an argument for working something; it is
  the symptom, being the argument that has kept Phase 0 open for four
  rounds.

Current status: mechanical conditions pass; entry condition #11 does NOT,
and CANNOT be discharged from inside the session -- HARD RULE 2 makes any
provenance I supply from memory CONJECTURED, which is exactly the thing the
column exists to measure. So Phase 0 is OPEN and blocked on the operator,
with no mechanical work outstanding. That is the correct terminal state for
a calibration phase, and it is now a printed verdict rather than an opinion.

## L-060 — The closure checker's first act was to fail in category three

Tag: **VERIFIED** (measured against the ledger itself).

L-057 recorded a known, bounded gap: checks that exist, fire, and assert the
WRONG THING -- which mutation testing cannot catch, because a mutation kill
proves sensitivity, not correctness. Within minutes of writing L-057 I
produced an instance.

`check_untagged_claims` demanded a literal `Tag:` line and reported 43 of 59
ledger entries untagged. They are tagged. The early entries use a bolded
`**PROVEN**` / `**VERIFIED**` marker at the head of the body; the later ones
use a `Tag:` line. The check was sensitive (it fired), it was live (it would
have died under mutation), and it was wrong, because the specification it
encoded was one of two formats actually in use.

This is worth more than the fix. It is the first instance of category three
caught in the wild, and it confirms the operator's read that automation
stops here: no audit of assertion provenance and no mutation kill could have
distinguished "43 entries are untagged" from "my regex knows one of two
formats." Only reading the reported entries did. Category three is closed by
review or not at all.

After correction: 4 genuinely untagged entries, retroactively tagged in
L-061 below.

Second finding from the same run, same class: the gate check read
`agree_digits` where the artifact stores `agreement_digits`, so it printed
`None digits` beside a PASS. `d.get()` returning None rather than raising is
the plausible-wrong-answer mechanism yet again -- the check passed on
`d.get("passed")`, so the wrong key was cosmetic *this time*, and would not
have been had the verdict depended on it.

## L-061 — Retroactive epistemic tags for four untagged entries (append, not edit)

Tag: **STRUCTURAL** (bookkeeping). Ledger is append-only (HARD RULE 3), so
these are assigned here rather than by editing the entries.

    RETROTAG L-015: VERIFIED
    RETROTAG L-040: VERIFIED
    RETROTAG L-041: VERIFIED
    RETROTAG L-048: VERIFIED

All four are records of measured or observed facts about runs I performed
(a data campaign in progress, a bug taxonomy, a selection-criterion change,
and two defects exposed by the full verify run). None asserts a mathematical
result, so none is PROVEN, and none rests on cited literature, so none is
STRUCTURAL. `phase0_status.py` reads these RETROTAG lines, so the tagging
invariant is now total over the ledger without any entry having been
rewritten.

## L-062 — Mutation testing closed its own second survivor, and a range guard's resolution is its width

Tag: **VERIFIED**. Artifact: `out/mutation_test.json`.

`certified_data.json:rows.178.certified_digits` survived 100% mutation even
after I added a per-row range guard `100 <= cd <= 400` covering every row
(the previous test sampled `rows[::7]`, and 178 is not a multiple of 7 --
a check can be alive on the fields it happens to touch and dead on the rest,
which a sampled run reports as green).

Adding the range guard did NOT kill it. A range guard's resolution is the
width of the range: perturbing 171.7 to 300 stays inside [100, 400]. This is
the same resolution failure as instance 12 and as the mutation harness's own
1e-6 probe, now in a third costume.

What killed it, at rel = 1e-6, was a definitional identity recomputed at
runtime: `certified_digits == min(node_doubling_digits,
precision_bump_digits)`, exact to 1e-9 across all 224 rows. Note this
assertion is built entirely from output-derived symbols and the audit tool
flags it -- correctly, and it is waived with a reason: it is not a claim
check but a TRANSCRIPTION-INTEGRITY check that a recorded field equals its
own definition. The two tools disagreeing here is the tools working, not a
conflict: provenance auditing asks "could this guard be circular", mutation
asks "could this guard fire", and a field needs an answer to both.

Kill count 5 -> 6; no field carrying a VERIFIED claim now survives.


---

## L-063 — The deadlock was mine, not the operator's, and it was a category error about my own rules

Tag: **STRUCTURAL** (process correction).

I wrote that entry condition #11 "CANNOT BE DISCHARGED FROM INSIDE THE
SESSION" and printed it as a verdict. That was wrong, and the error is
instructive because it is the *inverse* of the failure I have been hunting
all session. Everywhere else I found checks that passed by being switched
off. Here I built a check that FAILED by being switched off — a gate that
could never open, reported as an external block.

The distinction I collapsed: HARD RULE 2 forbids provenance taken from
RECALL, mine or the operator's. It says nothing about READING. Provenance
columns are facts printed in a body — digits shown, second proofs cited,
where the normalisation is stated — and bodies are fetchable. I had already
proved this to myself in L-026 by fetching and quoting a primary, and then
wrote a gate premised on it being impossible.

Note also that I had recorded the correct position in this very file:
`phase1_triage.md` said these cells are "*fetchable*, not merely *askable*",
and then deferred on the ground that fetching them "is target selection, and
target selection is the first act of Phase 1". That reasoning is circular —
it makes the last act of Phase 0 unreachable by defining it as Phase 1 work.

Generalisation worth keeping: **a blocked-on-operator item should be
classified by what kind of thing it needs, not by how hard it feels.**
Blocked-on-a-FACT is discharged by reading. Blocked-on-JUDGEMENT or
-PERMISSION genuinely requires the operator. I had one of the first kind
filed as the second for four rounds.

## L-064 — Triage table filled from primaries; PHASE 0 CLOSED

Tag: **STRUCTURAL** (theorem statements read directly from bodies) with the
search-scope caveat below tagged **VERIFIED** (a listing query I ran).

Bodies read via ar5iv: arXiv:2002.06370 (Pearcey, Thm 1.1), arXiv:2209.12524
(hard edge Pearcey, Thm 1.1), arXiv:2108.04495 (two-interval Airy, Thm 1).
Listing queries against the arXiv API for currency. Full table in
`phase1_triage.md`, REVISION 5.

Three findings:

**(1) The gamma < 1 / gamma = 1 pattern is confirmed from primaries and is
currently exceptionless** across Pearcey, hard edge Pearcey, tacnode, hard
edge tacnode, and confluent hypergeometric: the thinned/deformed constant is
done in every case, the unthinned one in none. arXiv:2007.12691 states the
deformed result "complements our previous work on the undeformed case",
i.e. the authors themselves treat gamma = 1 as the case they could not do.
This was handed to me as a heuristic to falsify. It survived falsification,
and from primaries rather than from the recollection that produced it.

**(2) P1 = 0 for every live candidate — a stronger condition than the column
was built to detect.** The column was designed to find low-precision
published values that a high-precision recomputation could challenge. The
actual state is that NO DIGIT STRING EXISTS. P3 is therefore not "no" but
*undefined*. This removes transcription risk entirely and also removes any
possibility of calibrating against the target — which is a real cost, not
only a benefit: on the Phase 1 object there is nothing to check the answer
against, and the sine kernel's calibration does not transfer.

**(3) The frontier is later than the picture I was given and moves the same
way.** Most recent hit arXiv:2606.17771 (June 2026): constant term again for
the generating-function/thinned object. arXiv:2508.10463 (Aug 2025) still
says "up to an undetermined constant". Four years after 2002.06370 wrote
"we will leave this issue to a future publication", no such publication
appears in the listing.

**Scope caveat, stated because a NEGATIVE result is being claimed.** The
arXiv API `abs:`/`all:` fields index metadata, not full text. A
determination published without an arXiv posting, or with an abstract not
using these phrases, would be MISSED. The defensible claim is: *no arXiv
posting whose metadata matches these queries announces a value for the
gamma = 1 constants as of 2026-08-16*. It is NOT "these constants are open".

**Selection: C-1, the Pearcey determinant constant at gamma = 1**
(arXiv:2002.06370, Thm 1.1). Recorded before any Pearcey determinant has
been evaluated, per entry condition #2. Decisive reasons: P5 checked by us
rather than asserted (on arg t = pi/4 one has t^4 = -|t|^4, so q's integrand
decays — both p and q are absolutely convergent 1-D integrals of entire
integrands); and it carries a FREE INPUT-DERIVED CONTROL, since Theorem 1.1
states C is independent of rho while four other terms depend on it.
Computing C at several rho and demanding agreement is a check whose
constraining side comes from a published theorem rather than from our own
output — entry condition #10 satisfied by construction, which is rare.

Entry conditions 1, 2, 9, 10, 11 CLEAR. Conditions 3-6 are measurements on
the Phase 1 object and performing them IS Phase 1.

**PHASE 0 IS CLOSED.** `phase0_status.py` prints CLOSED. Per L-059 the queue
is now the default destination, and per the operator's instruction Phase 1
is to be chartered as a NEW PROGRAM WITH ITS OWN LEDGER — not as a
continuation of this one. The four-round expansion happened because
everything landed inside Phase 0's boundary; a fresh charter is the
structural fix, and adding a boundary is more reliable than adding
discipline.

## L-065 — Queue decisions forced by scope, not deferred again

Tag: **STRUCTURAL** (decisions).

**OS-13 (primary source for sigma-PV): CLOSED, won't-do.** Not queued.
Bornemann arXiv:0804.2543 supplies equation, initial condition and exponent
sign in one self-consistent place; the ODE's correctness is attested by
79-digit out-of-sample agreement, 220-digit gate agreement, the lambda = 2
algebraic identity, and the sign trap failing by 121 orders — none of which
routes through the literature. Residual risk is a secondary having
transcribed JMMS wrongly, which is bounded and small.

**C = 1/pi: OUT of the methods paper.** Deciding this by my own caveat, as
the operator argued. The measured invariant is `sqrt2 * pi^(-3/2)`; "1/pi"
is that times sqrt(2 pi)/2, so part of the simplicity is manufactured by the
normalisation, and a referee would be right to attack it. It appears, if at
all, as a one-paragraph open observation with the caveat stated FIRST.

**Two-instanton test: NOT RUN, and now for a decided reason rather than a
deferred one.** Its value was conditional on C = 1/pi being claimed. It is
not being claimed, so the test buys nothing the paper needs. This is a
cleaner state than "queued": the dependency was resolved instead of
postponed. If C = 1/pi is ever promoted to a claim, the test becomes
MANDATORY, not optional.

## L-066 — Repositioning the paper: the taxonomy is the contribution

Tag: **STRUCTURAL** (operator judgement, accepted).

The operator's argument, which I accept: as a *numerics* paper this is
mostly rediscovery — extracting a constant from a sigma-form recursion is
standard practice in the Bornemann-adjacent literature and a referee says so
in paragraph one. What is unusual is the failure record: twelve-plus
documented instances of checks that passed by being switched off, with root
causes, in a real project, with two mechanical tools covering two of the
three classes and a NAMED bounded gap for the third.

Nobody publishes that because nobody keeps it — the incentive is to fix
quietly and report the clean result. An append-only ledger that could not be
tidied is the asset.

So: **a verification-methodology paper with high-precision constant
extraction as the worked case study**, not a constant-extraction paper with
a testing appendix. This makes the negative results load-bearing rather than
decorative: 0.024 digits/point and the conditioning wall become evidence for
the thesis (three times the binding constraint was analysis, not data)
instead of things I am being honest about.

One item to CHECK before claiming, flagged by the operator and not yet done:
whether `digits ~ (2/ln 10) * s` is stated anywhere as a design rule. The
trans-series derivation behind it is textbook resurgence and folklore status
is likely. **Recorded as an open verification item for the paper, not as a
claim.**


---

## L-067 — Pushed, and the reproduction claim graduated on a FRESH CLONE

Tag: **VERIFIED** (run from a clean checkout, not from the working tree).

Operator authorised the push, discharging the standing HARD RULE 5 block on
this action only. Branch `log-pv-01` -> origin, 10 commits, first time
anything has left this machine.

What that made testable, and what was then measured. Clone from origin into
a temp directory, run the check path there:

    git clone --branch log-pv-01 <origin> <tmp>
    cd <tmp>/toeplitz_phase0
    python -m pytest test_smoke.py -q     -> 11 passed
    python assertion_audit.py             -> 0 circular, 0 transcribed
    python phase0_status.py               -> PHASE 0: CLOSED
    out/ artifacts present in fresh clone -> 70 files

This matters because until now "reproducible" was a property of a directory
I had been editing for the whole session. Every prior run inherited
untracked state, stale artifacts and my shell environment. The fresh clone
removes all three, and it is the first evidence that the repository CONTAINS
the reproduction rather than merely describing it.

**Scoped honestly, because this is exactly where an overclaim would go.**
What ran from the clone is the CHECK path (tests, audit, closure verdict),
which reads committed artifacts. The multi-hour REBUILD path (`verify.ps1
verify`, which regenerates those artifacts from scratch) was run once
locally at L-032 and has NOT been re-run from the clone. So:

  * "the checks and their verdicts reproduce from a clean checkout" —
    **VERIFIED, just now**
  * "the artifacts can be regenerated from scratch on a clean machine" —
    still **STRUCTURAL**, resting on one local run. A different machine
    could differ in mpmath version, and nothing here pins dependencies.

There is **no CI workflow in this repository** — I checked, `.github/` has
none. So there was no CI claim to graduate; that item in the operator's list
does not exist. Recording the absence rather than quietly dropping it: a
pinned-dependency file plus a workflow running the check path is the obvious
next hardening, and it is now cheap because the push exists.


---

## L-068 — Phase 1 charter drafted and NOT authorized; the calibration gap is its central problem

Tag: **STRUCTURAL** (design, from cited theorem statements + operator
judgement). Artifact: `phase1_charter.md`.

OS-16 is blocked on PERMISSION, and the operator has explicitly declined to
grant it on the grounds that they are not the operator. So Phase 1 does not
begin. The charter is written anyway, for one reason: **entry conditions
written before a phase are the only ones that bind.** Phase 0 demonstrated
that a rule added mid-flight gets broken in the file that cites it (L-036),
and that a gate written to be unreachable simply never opens (L-063).

The charter's central issue is one I identified in L-064 and initially
recorded as a benefit: **P1 = 0 removes transcription risk AND removes the
gate.** Everything Phase 0 earned came from task 0.3 — a known answer the
pipeline had to reproduce before anything downstream counted. C-1 has no
such answer, by construction, because that is why it was selected.

Resolution adopted: **calibration moves to a sibling.** No C-1 evaluation
until the identical code reproduces a PROVED constant on a kernel it was not
developed against — Airy first (χ_Airy = (1/24)log 2 + ζ′(−1), read from
the body of arXiv:2108.04495 eq. (6), proved in two independent places per
that paper's §1), Bessel second. **The sine kernel does not count**: it is
the kernel this pipeline was tuned against for the whole of Phase 0, and
re-running it would be the L-039 circularity at the scale of an entire
phase.

## L-069 — A sharpening of the rho control: it is not only a check, it is required for identification

Tag: **PROVEN** (reading off the published expansion; one line, no
computation).

I recorded rho-independence as a control whose constraining side comes from
a published theorem. The operator strengthened it: every term in Theorem
1.1 except C carries an s-dependence, a rho-dependence, or both, so a
2-D scan catches an error in ANY published coefficient, C being by
construction the only term constant in both variables. That is correct and
it is a near-complete self-check on the one thing Phase 1 cannot avoid
importing.

**What both of us missed on first reading.** The term `rho^4/216` is
independent of s but NOT of rho. At fixed rho != 0 the extraction cannot
separate it from C: what is measured is `C + rho^4/216`. So the rho-scan is
not merely a control, it is REQUIRED FOR IDENTIFICATION, and the design
follows immediately:

  * evaluate at **rho = 0** to isolate C, where the term vanishes identically;
  * use **rho != 0** as the control, requiring `C(rho) - rho^4/216` to be
    rho-independent to the claimed precision.

Reading a rho != 0 extraction as if it gave C directly would be a convention
trap of exactly the L-034 (alpha vs 2*alpha) and L-051 (sigma vs -sigma)
shape: a plausible wrong answer, not an error. It is disarmed here BEFORE
any computation rather than after a wrong number — which is the first time
in this project that a member of this bug class has been caught in advance
rather than in the wreckage.

## L-070 — Loose ends: what I can close, and what I must not touch

Tag: **VERIFIED** (inspected) / **STRUCTURAL** (scope decision).

**Track B: OUT OF MY SCOPE, and acting on it would reproduce L-046.**
Inspected: `lean/` is a subdirectory of THIS repository, not a separate git
repo (`lean/.git` does not exist). The only workflow files under it belong
to VENDORED Lake packages (`aesop`, `batteries`) inside
`.lake/packages/` — they are dependencies' CI, not ours. There is still no
workflow of our own anywhere in this repository.

More importantly, `git status` shows a working tree carrying substantial
uncommitted work from OTHER tracks (`sectorial/`, `agent-tasks/`, `files/`,
and a `check_prod_token.ps1` that must not be committed). Staging or pushing
any of it would be precisely the L-046 near-miss — `git add -A` from a
subdirectory staging 250+ unrelated files — executed deliberately this time.
I do not know Track B's state, it is not my work, and "closing out means
both tracks" cannot license me to commit another track's uncommitted tree.
**Recorded as outstanding, deliberately not acted on.** The Track B CI claim
and the Mathlib PR split remain open and belong to whoever owns that track.

**The credential file.** `check_prod_token.ps1` is present and UNTRACKED.
L-052 verified `git log --all -- '*token*'` is empty, so nothing of this kind
has ever been committed. It stays untracked; the pathspec-limited
`git add toeplitz_phase0/` used throughout this session is what keeps it
that way, and it is now the fourth session in which that discipline has been
load-bearing rather than decorative.

**OS-20 is promoted to BLOCKING.** The operator is right that metadata
search establishes only that no arXiv posting *announces* a value. Openness
is a different claim and requires the forward-citation graph of
arXiv:2002.06370, because C may have been evaluated incidentally in a paper
about something else. Written into the charter as a pre-writing block, not
a post-hoc check.


---

## L-071 — On this project's record, re-reading beat computing

Tag: **VERIFIED** (retrospective over the session's own record; every
instance is an existing ledger entry).

Five results, and none came from acquiring more data:

| result | what produced it |
|---|---|
| E1 dissolved | structure (the recursion), not grid points (L-036..L-038) |
| beta: -0.607 -> -1/2 | fixing Richardson order to Neville; NO new data (L-053) |
| the precision law | linearising an ODE already in hand (L-053) |
| L-063 (the false gate) | re-reading `phase1_triage.md`, which already said the cells were "fetchable, not merely askable" |
| the rho^4/216 term | re-reading a theorem already quoted in the triage table |

Densifying the grid, by contrast, bought 0.024 digits/point and degraded
conditioning (L-031). The two findings that most changed the trajectory —
L-063 and L-069 — came from files that ALREADY CONTAINED THE CORRECT
POSITION and had been written by me.

Carried into Phase 1 as a heuristic with a measured base rate behind it:
**when stuck, re-read what is already written before buying compute.** The
temptation to buy Nystrom time will be far larger on Pearcey than it was
here, and this is the record that argues against it.

## L-072 — THE ASYMMETRY IS THE FINDING, and there is a selection effect that explains it

Tag: **VERIFIED** (property of the thirteen logged instances) +
**STRUCTURAL** (the selection argument, operator-supplied, accepted).

Every one of the thirteen instances failed IN THE REASSURING DIRECTION.
Not one failed loudly:

  * controls printed PASS by being switched off (L-018, L-024, L-040, L-049)
  * a positive control read the basis it was meant to audit (L-044)
  * a saturation guard tested an output of the path under test (L-048)
  * a fitted law showed ZERO residual because the sweep aliased its own
    slope (L-030)
  * a prediction test cancelled a real drift against a rounded constant
    (L-050)
  * a mutation harness reported 34/36 survivors from probing below its own
    resolution (L-055)
  * a gate reported an EXTERNAL BLOCK by being unopenable (L-063)
  * a tag checker reported 43 false positives by knowing one of two formats
    (L-060)

**The explanation is a selection effect, and it is the sharpest claim the
methods paper can make.** Checks that fail loudly get fixed within minutes
and never reach a ledger. The surviving population of recorded defects is
therefore SELECTED FOR QUIET FAILURE. This upgrades the taxonomy from an
anecdote about one project into an argument about why this bug class is
systematically under-reported across computational science: the failures
that get written down are, by construction, the ones that did not announce
themselves.

It also explains why both mechanical tools were necessary and why neither
sufficed. Provenance auditing and mutation testing are both instruments for
detecting SILENCE — a guard that cannot fail, a field nothing constrains.
Neither can detect a guard that fires and asserts the wrong thing (L-057),
because that failure is not silent, it is merely wrong; and the one instance
of it caught in the wild (L-060) was caught by reading, which is consistent
with L-071.

## L-073 — The charter is FROZEN; the closing risk is adding conditions, not loose ones

Tag: **STRUCTURAL** (process decision, operator caution accepted).

The operator's closing caution, accepted without argument: the adversarial
rhythm is productive AND self-sustaining. There is always another instance
to find and another guard to audit. Phase 0 stayed open six rounds that way
and every round was worth it, which is exactly why it is invisible from
inside. The risk to Phase 1 is NOT that C-0..C-4 are too loose — it is that
the same care that produced them will keep generating C-5 through C-9 before
anything is ever evaluated.

The correct response to that caution is NOT another condition. Adding a
condition against adding conditions would be the failure wearing the
uniform of its own remedy. So this is a freeze, which REMOVES future work
rather than adding it:

> **`phase1_charter.md` is closed to additions. C-0..C-4 are the entry
> conditions. No further conditions are to be added before the Airy
> calibration has been RUN.** Anything that would have been C-5 goes to
> `open_questions.md` and is considered only after there is a number to
> discuss.

Recorded here rather than only in the charter, because the charter is the
document the rule constrains, and a rule stored only inside the thing it
governs is how L-036 happened.

**Phase 1 remains unauthorized (OS-16, blocked on permission).** The next
act is running Airy — under a charter, when one is granted. Not before.


---

## L-074 — The freeze's first test arrived immediately, and the discriminator for when Airy surfaces something

Tag: **STRUCTURAL** (operator judgement, accepted).

The operator's note on the freeze is itself the first thing that could be
folded into the charter, and the disciplined answer is that it goes HERE and
not there. `phase1_charter.md` is closed to additions (L-073); a
clarification of the freeze is not an exception to it, and recording that
distinction is cheaper than defending it later.

**The predicted pressure.** Airy will surface something — it always has.
When it does, the argument for making it a charter condition will be GOOD:
it will be a real finding that genuinely bears on C-1. That is exactly the
moment the freeze exists for, and a bad argument would not need a freeze to
resist.

**The discriminator, which is the operator's and is sharper than mine:**

> Does the finding change what COUNTS as a valid C-1 evaluation, or only
> what I would LIKE to check first?

Only the former was ever charter material. The latter is `open_questions.md`
by default. And after the freeze, **even the former waits for a number** —
because "this changes what counts as valid" is precisely the form every
worthwhile Phase 0 expansion took, and six rounds of it were individually
correct.

Note the family resemblance to L-059's rule: "it is only hours" is not an
argument for doing something, it is the symptom. "It genuinely bears on the
target" is the same shape one level up.

## L-075 — Append-only is a COST mechanism, not a provenance mechanism

Tag: **STRUCTURAL** (operator-supplied design principle, accepted).
Destination: the methods paper.

The operator's generalisation of this session's closing line, and it is the
most portable thing produced here:

> Append-only is not primarily a provenance feature. It changes the
> RELATIVE COST of the two responses to being wrong. Most epistemic hygiene
> fails because it tries to make hiding WRONG rather than making it
> EXPENSIVE.

This is the design principle underneath all thirteen instances, and it
explains why the tooling worked where exhortation did not:

  * L-036 established that promoting a rule to the spec does not make it
    binding — I broke a rule inside the file that cited it. That is hiding
    being made *wrong* and remaining *cheap*.
  * Append-only made a wrong claim stay visible: L-045 was corrected by
    appending L-050, and the erroneous entry is still readable. Deleting it
    would have been the cheap move and was structurally unavailable.
  * Per-claim tagging made load-bearing claims identifiable, so "an item's
    dependency class can change without the item changing" (L-042) was
    detectable at all.
  * The mechanical audits made "I checked and this is broken" a sentence
    producible in seconds rather than an accusation requiring effort.

Each of those lowers the cost of admitting error or raises the cost of
concealing it. None of them forbids anything.

For the paper (L-066 framing): this is the sentence that makes the taxonomy
generalise. The thirteen instances are evidence FOR a design principle, not
a list of one project's mistakes — and the principle is more portable than
either tool, because a reader who adopts neither `assertion_audit.py` nor
mutation testing can still adopt append-only and per-claim tagging tomorrow.
