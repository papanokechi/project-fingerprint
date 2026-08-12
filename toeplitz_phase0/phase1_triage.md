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

**Measured T, at `maxcoeff = 1e4`, 3 random targets per precision:**

| basis size b | 3 | 4 | 6 | 8 |
|---|---|---|---|---|
| measured T | 25 | 30 | 40 | 50 |

These four points are **exactly linear**:

```
T(b) = 5b + 10          (VERIFIED at b = 3, 4, 6, 8; residual zero)
```

Consequences, and this is the Phase 1 entry condition:

| basis size b | T(b) | required honest digits D |
|---|---|---|
| 4  | 30 | 64 |
| 6  | 40 | 73 |
| 8  | 50 | **83** |
| 10 | 60 | **93**  (T extrapolated) |
| 12 | 70 | **103** (T extrapolated) |

Current capability: **D = 71** (142-point grid). This clears b = 6 and fails
b = 8. Phase 1 bases will realistically be 8-12 entries, so Phase 1 needs
**D ~ 83-103**.

CAVEATS, stated because the table above is the thing most likely to be misused:
* `T(b) = 5b + 10` is fitted to four points over a narrow range and is
  **CONJECTURED** outside `b in [3,8]`. The b = 10 and b = 12 rows are
  extrapolations and MUST be re-measured before being relied on.
* `T` is measured only at `maxcoeff = 1e4`. Dependence on the coefficient
  bound is unmeasured. A Phase 1 target needing larger coefficients raises `T`
  by an unknown amount.
* The heuristic `T ~ b*log10(maxcoeff)` under-predicts the measured values by
  ~40-100% and should not be used.

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
