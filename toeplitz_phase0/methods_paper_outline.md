# Methods paper — outline (DRAFT, operator-gated, no submission)

Status: **outline only.** HARD RULE 5 forbids external submission; nothing
here is to leave the repository without operator instruction.

## The argument for writing it now

The operator's case: the methods content is self-contained and does not
depend on Phase 1 finding anything. Writing it also *derisks* the track — if
the triage table comes back showing every candidate constant is
well-established and adequately proved, we still have a result rather than a
very well-audited null.

That argument is sound and I want to record why I did not previously see it.
I had been treating the tooling as overhead on the way to a constant, so
each hardening round felt like a detour from the deliverable. The tooling is
the deliverable that actually exists; the constant is the one that does not
yet. That inversion is worth its own note (L-058's pattern, one level up:
not "reaching for data when the limit is analysis", but *mistaking which
output is the product*).

## Claim of the paper

A protocol for extracting subleading constants from Fredholm determinant
asymptotics at several hundred digits, in which the reported precision is an
**audited** quantity rather than the working precision — together with the
verification machinery that makes that auditing mechanical rather than a
matter of the author's alertness.

The second half is the unusual part. Numerical-analysis papers report what
their method achieved. This one also reports the instrumentation that
established the number was not an artifact, and the twelve documented
occasions on which that instrumentation caught the author.

## Sections

**1. The object and the calibration target.**
Sine kernel on [-1,1]; `log det(I-K_s) = a s^2 + b log s + c + O(1/s)`.
`c` known in closed form with several independent proofs, hence a
calibration target and explicitly not a result. Normalisation stated in the
body, with the alpha-vs-2alpha convention trap and how the numerics resolve
it without reference to any source (L-026, L-051).

**2. Nyström evaluation and its conditioning wall.**
Gauss–Legendre Nyström, parity reduction, node-doubling and precision-bump
certification. The measured digit-loss law. **The negative result belongs
here**: densifying the grid bought 0.024 digits/point and hit a conditioning
wall (L-031) — one of three occasions where the binding constraint was
analysis, not data (L-058).

**3. The sigma-form recursion, and constant extraction with no fit.**
The sigma-PV form recovered from the data by numerical nullspace, then
matched to Jimbo–Miwa–Okamoto in `x = 2s` via the purely algebraic
`4 lambda^2` coefficient identity (lambda = 2, needing no literature
convention at all). Constant extracted from the recursion rather than by
Richardson fitting: 132 digits, no fit residual, hence no fit uncertainty.
This is the methodological core — *replacing extrapolation with a recursion
removes the dominant error term rather than estimating it*.

**4. The precision law and its derivation.**
`digits ~ 2s/ln 10 ~ 0.869 s`, measured first and then **derived**:
linearisation of the sigma equation gives a WKB one-instanton term with
`A = 2` and `theta = 1/2` as exact rationals, and an independent
large-order/resurgence route on 300 exact rational coefficients confirms
`A = 2` to 8e-33 and `beta = -1/2` to 1e-31. Two routes, disjoint
machinery.
Include the three-exponent reconciliation as a cautionary subsection: the
trans-series exponent in `log det`, in `sigma`, and in the least term differ
by Stirling and by a derivative, so a naive comparison of "the" exponent
against measurement fails by 1/2 for reasons unrelated to either being
wrong.
Include the Neville-vs-Richardson trap (L-053): repeatedly applying a single
1/m eliminator removes a term already gone; fixing it moved `beta` from
-0.607 to -0.5 with no new data.

**5. Verification instrumentation.** *(the part that is not standard)*
- **Provenance auditing of assertions.** A guard is suspect if every
  comparison in it has a common computed ancestor on both sides. Finds
  checks that exist but cannot fail. Validated against a broken/fixed
  fixture; two earlier criteria were discarded after being *measured*
  useless. Found instance 12 where predicted.
- **Mutation testing of artifacts.** Finds checks that were never written.
  A field surviving mutation is unguarded. Requires an escalating
  perturbation ladder: at a fixed small probe, "survived" conflates *no
  check* with *check coarser than the probe*, and fails in the reassuring
  direction.
- **Null + positive controls in pairs.** A basis that cannot recover a
  relation it contains is switched off. The positive control must be built
  from something the suspect path cannot influence — the first
  implementation read the passed-in basis and inherited the circularity it
  existed to detect.
- **The honest-digit discipline.** Fit residual vs working precision are
  different numbers; every reported figure states which.
- **The bounded gap, stated as such**: checks that exist, fire, and assert
  the wrong thing are caught by neither tool (a mutation kill proves
  sensitivity, not correctness). One instance caught in the wild, by
  reading (L-060).

**6. Failure taxonomy.**
Twelve-plus instances, all sharing one signature: **a plausible wrong answer
rather than an error**. The mechanical criterion that unified them —
classify each symbol in an assertion as input/specification-derived or
output-derived; any assertion with an output-derived symbol on the
constraining side is suspect. Two of the instances were guards written
specifically to prevent the failure they missed, which is the argument that
an audit must not depend on the auditor's alertness.

**7. Reproduction.** `verify.ps1` re-derives every VERIFIED claim from
scratch; `phase0_status.py` prints the closure verdict.

## Honest positioning

- The constant is a calibration target, not a discovery. Say so in the
  abstract, not only in the body.
- The sigma-PV form was *rediscovered*, not derived from the literature.
  That is a validation of the discovery procedure and must not be dressed as
  a new equation. OS-13 (primary source) is open and disclosed.
- `C = 1/pi` is CONJECTURED, post-hoc recognised, and its route contains a
  sqrt(2 pi) from Stirling (L-056). Either exclude it or include it with the
  caveat that cuts against it — the measured invariant is
  `sqrt2 * pi^(-3/2)`, and part of "1/pi"'s simplicity is manufactured by
  normalisation.

## Venue shape

Numerical-analysis / reliable-computing, journal-first (fits the standing
arXiv constraint). **Operator decision, not mine.**

## What is NOT in this paper

Anything from Phase 1. The paper is deliberately complete without it.
