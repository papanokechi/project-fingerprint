# Phase 1 triage — gating table and entry conditions

**Status: PREPARATORY. No Phase 1 computation has been performed.**
This document exists to satisfy the rule that target selection happens BEFORE
computation, so that a target cannot be chosen after seeing which one the
pipeline happens to resolve.

---

## 1. How many honest digits a target needs (VERIFIED, and it is predictive)

The reportability rule proven by arithmetic on the protocol (L-014, L-018) is

```
D  >=  max( T(basis),  PERTURB_DIGIT + GUARD + log10|target| )  +  RECONFIRM_BUMP + MARGIN
```

with the harness constants `PERTURB_DIGIT = 20`, `GUARD = 8`,
`RECONFIRM_BUMP = 30`, `MARGIN = 3`. For a target of order unity the control
floor is 31, so `D >= max(T, 31) + 33`.

`T(basis)` is the measured spurious-relation threshold: the lowest precision
above which the harness returns NOTHING on random targets, read from ABOVE
(L-019 — reading it from below returns the precision at which PSLQ merely
fails to converge, which is bug class 3).

**Measured T, at `maxcoeff = 1e4`, 3 random targets per precision, on a
STEP-1 sweep over dps 24..52 (see L-030 — an earlier step-5 sweep produced a
spuriously "exact" linear law and is superseded):**

| basis size b | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| measured T | 24 | 27 | 30 | 35 | 39 | 44 |

A second, independent run of the same measurement inside `run_pslq.py`
(different sweep list, hence a different random-target sequence) returned
T = 35 at b = 6 and **45** at b = 8. T is a small-sample estimate of the edge
of a stochastic phenomenon, reproducible to about +/-1, not a constant.

Increments are 3, 3, 5, 4, 5 — **concave, not linear**. The earlier claim
`T(b) = 5b + 10` is FALSIFIED (it predicts 45 at b = 7; the measurement is 39)
and its apparent zero residual was an artefact of a sweep spaced by 5, equal
to the fitted slope. No functional form is asserted here to replace it: six
points over b in [3,8] do not determine one, and the honest statement is the
table.

Consequences, and this is the Phase 1 entry condition:

| basis size b | T(b) | required honest digits D | status at D = 73 |
|---|---|---|---|
| 4  | 27 | 64 | reportable |
| 6  | 35 | 68 | **REPORTABLE (achieved, L-034)** |
| 7  | 39 | 72 | reachable |
| 8  | 44-45 | **77-78** | 5 short |
| 10 | **UNMEASURABLE** | unknown | — |
| 12 | **UNMEASURABLE** | unknown | — |

Current capability: **D = 73** (224-point grid, L-033). That clears b = 6 —
achieved and reported — and falls about 5 digits short of the full 8-element
basis.

CAVEATS, stated because the table above is the thing most likely to be misused:
* **T cannot be measured at b > 8 at all with the present basis, which has
  only 8 entries.** The b = 10 and b = 12 rows are not "extrapolated", they
  are undefined: a Phase 1 basis that size requires new constants to be
  declared FIRST, after which T must be re-measured. Any digit requirement
  quoted for b > 8 today is fabricated.
* `T` is measured only at `maxcoeff = 1e4`. Dependence on the coefficient
  bound is unmeasured. A Phase 1 target needing larger coefficients raises `T`
  by an unknown amount.
* The heuristic `T ~ b*log10(maxcoeff)` under-predicts the measured values by
  ~40-100% and should not be used.
* T is resolved to +/-1 dps by the step-1 sweep, and rests on only 3 random
  targets per precision. It is a small-sample estimate of the edge of a
  stochastic phenomenon, not a constant of nature.

---

## 2. Triage table (TO BE FILLED BEFORE TARGET SELECTION)

The research value of a target is a function of how weak the existing value
is. A target with 30+ published digits and two independent derivations is
calibration, not research. The columns are therefore chosen so that the
decision is made from the table rather than after a week of Nystrom runs.

Legend for provenance: `PROVED` (rigorous derivation exists) / `DERIVED`
(non-rigorous but constructive) / `CONJECTURED` (pattern or heuristic) /
`UNKNOWN`.

| # | candidate constant | digits in literature | provenance | independent 2nd derivation? | expected basis size b | required D | pipeline reach today | verdict |
|---|---|---|---|---|---|---|---|---|
| T-1 | Fisher-Hartwig prefactor (pure FH symbol, single jump) | OPERATOR-SUPPLY | OPERATOR-SUPPLY | OPERATOR-SUPPLY | ? | ? | ? | pending |
| T-2 | Jin-Korepin XX-chain entanglement additive constant | OPERATOR-SUPPLY | OPERATOR-SUPPLY | OPERATOR-SUPPLY | ? | ? | ? | pending |
| T-3 | Emptiness formation probability (XX / free fermion) constant | OPERATOR-SUPPLY | OPERATOR-SUPPLY | OPERATOR-SUPPLY | ? | ? | ? | pending |
| T-4 | Widom-Dyson constant (this session's target) | >= 72 (this session) | PROVED (L-026) | YES (Krasovsky; Ehrhardt) | 4 | 64 | 71 | **CALIBRATION ONLY — not a Phase 1 target** |
T-4 is entered deliberately, as the worked example of a row that the table
should REJECT: the value is proved, independently twice, and now reproduced to
72 digits. There is no research value left in it. Any Phase 1 candidate whose
row looks like T-4's is calibration.

**The table cannot be completed in-session.** Every literature column is an
OPERATOR-SUPPLY item (see `open_questions.md`, OS-2..OS-4, OS-10) because
Rule 1 forbids citing published values from memory. Note that this session
demonstrated that primary text CAN be fetched and quoted verbatim (L-026), so
these cells are *fetchable*, not merely *askable* — but fetching them is
target selection, and target selection is the first act of Phase 1, not the
last act of Phase 0.

---

## 3. Entry conditions for Phase 1 (pre-committed)

Phase 1 may begin only when ALL of the following hold. They are written down
now so that they cannot be relaxed later in the light of results.

1. The triage table above is filled for every candidate, with provenance.
2. A target is selected whose literature value is low-precision,
   single-sourced, or conjectural — and the selection is recorded BEFORE any
   determinant for that target is computed.
3. `T(b)` is re-measured at the actual basis size and `maxcoeff` to be used,
   rather than extrapolated from the table in section 1.
4. The pipeline demonstrably reaches the required `D` for that basis, measured
   by the E1/E2/E3 budget on the Phase 1 object itself — NOT inherited from
   the sine-kernel result. A different kernel has a different conditioning and
   a different digit-loss law.
5. The null controls are shown to be SENSITIVE at the precision used
   (L-018): a control that cannot resolve its own perturbation is switched
   off, not passed.
6. It is stated in advance which basis the target is expected to decompose in,
   and it is acknowledged in writing that a hit in that basis is
   harness-confirmation, not independent evidence (L-027).
7. Grid points are bought at the largest `s` the certification budget allows,
   not at the cheapest `s` (L-033). Densifying an already-sampled region
   returned 0.024 digits/point against 0.448 digits/point for extending to
   high `s` — a factor of 19 — while actively degrading conditioning. Cost per
   point is the wrong figure of merit; digits per point is the right one.

---

# REVISION: digit budget after the fit-free extraction (L-036..L-039)

Everything below supersedes the "required D" analysis above, which assumed
digits had to be bought with grid points.

## What changed

`c` is no longer obtained by fitting. It is read off as the integration
constant of a VERIFIED ODE after exact subtraction of a DERIVED tail, from a
single data point. The budget that used to bind (E1, order truncation) no
longer exists.

    quantity            before          after
    honest digits       73              132
    cost                224 pts, ~4 h   1 pt, ~70 s
    binding budget      E1 (truncation) truncation of the ASYMPTOTIC series
    error bar           sigma_c, scale  calibrated: 3 cross-s checks land at
                        unknown to 2x   ~80% of the predicted bar

## Basis reachability, revised

Required precision `D >= max(T, 31) + 33`, with T measured (L-030):

    b       3    4    5    6    7    8
    T      24   27   30   35   39   44
    D      57   60   63   68   72   77

At 132 honest digits, **every basis size up to b=8 is now reachable with
>= 54 digits of margin**, and b=8 is confirmed REPORTABLE with all five
decoy constants at coefficient zero (L-039).

Extrapolating the measured T (concave, roughly +4 to +5 per element at
b=7..8), 132 digits should support roughly b=14-16 before the spurious
threshold binds. That is a large enough basis for a genuine Phase 1 search,
and it is the first time in this project that basis size has not been the
limiting factor.

**This must be re-measured, not assumed.** T was fabricated once already by
reading a law off too coarse a grid (L-030). The b>8 thresholds above are
CONJECTURED extrapolation; measure them against random controls before
relying on any of them.

## How to buy more digits now, in cost order

The old rule ("buy points at the largest s") is superseded for `c`-type
extractions. The new ordering:

  1. **More recursion orders** -- free until the asymptotic optimum `m* ~ 2s`
     is reached. At s=149 that is m=298 and we are already there.
  2. **Larger s** -- now the ONLY lever that raises the optimum, since
     `m* ~ 2s` and the floor falls steeply with it. Going from s=149 to
     s=300 should roughly double the achievable digits again. This requires
     Nystrom at large s, which is the expensive direction, but ONE point
     suffices -- not a grid.
  3. **Higher certified precision per point** -- currently slack by ~57
     digits (E_data 1e-190 vs truncation 1e-133), so worth nothing today.

Note the inversion: entry condition #7 ("buy points at the largest s the
budget allows") survives, but "points" is now singular. There is no grid.

## Entry conditions: status

Conditions 1-6 unchanged. Condition 7 amended as above. One condition is
ADDED, arising from L-040:

  **8. Every control must compute its own resolution at runtime and assert
     that it exceeds the floor it is testing.** A hand-chosen perturbation
     constant will eventually sit below resolution and the control will pass
     by being switched off. This has now happened twice (L-024, L-040(6)),
     the second time in a file whose docstring cited the first.
