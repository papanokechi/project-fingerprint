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


---

# Revision 3 (appended; nothing above removed)

## Precision has stopped being a constraint, and that changes the ranking rule

Measured law, pre-registered and confirmed at three points (L-045):

    honest digits = 0.871 * s + 2.7      (spread 0.05 over s in [149, 250])

Achieved: **220.04 honest digits** at s = 250, agreeing with the closed form
to 219.765. Cost ~7 min per certified point plus a one-off recursion.

| basis size b | measured T | required D = max(T,31)+33 | headroom at 220 |
|---|---|---|---|
| 4  | 27 | 64 | 156 |
| 6  | 35 | 68 | 152 |
| 8  | 44 | 77-78 | **142** |
| 12 | ~55 (CONJECTURED, MUST RE-MEASURE) | ~88 | ~132 |
| 16 | ~65 (CONJECTURED, MUST RE-MEASURE) | ~98 | ~122 |

The extrapolated T values stay CONJECTURED. A T-law was fabricated once in
this session and falsified (L-030); the concave fit is not to be trusted off
the measured range, and re-measurement is cheap relative to a wrong claim.

To buy 100 more digits: +115 units of s, ~7 min/point. Precision is now the
cheapest input to the whole enterprise.

**Therefore the ranking rule changes.** The "required basis size" and
"pipeline reach" columns were the discriminating columns in revisions 1-2.
They no longer discriminate: every plausible Phase 1 target clears the bar.
Target selection must now be driven almost entirely by LITERATURE PROVENANCE
QUALITY. Concretely, rank candidates by:

  1. **Published precision.** A constant published to 30+ digits is a
     calibration opportunity, not a research target. Research value is
     highest where the published value is low-precision (say < 15 digits).
  2. **Sourcing multiplicity.** Single-sourced values carry unchecked
     transcription risk. Two independent derivations => calibration.
  3. **Derivation status.** Conjectured or numerically-inferred constants are
     worth more than proved ones, because a high-precision numerical value
     can materially change their status. A proved constant cannot be improved
     by more digits.
  4. **Whether an exact form is claimed at all.** A constant with no proposed
     closed form is the highest-value case: the PSLQ harness can propose one,
     and there is now basis headroom to do it honestly.

Scoring: research value is HIGH when (1) is low, (2) is single, (3) is
conjectural. It is NIL when (1) is high and (2) is multiple -- that is T-4,
this session's calibration target, by construction.

The point of stating this now: the ranking can be computed FROM the table,
before any Nystrom time is spent. Discovering after a week of computation
that the target was already known to 40 digits is the expensive mistake, and
it is entirely avoidable at the cost of filling in three columns.

## Entry condition #9 (new)

Phase 1 may not begin until the triage table's provenance columns are filled
from PRIMARY sources for at least the selected target. Operator-supplied
values enter as CONJECTURED (HARD RULE 2) and cannot by themselves justify
target selection -- selecting a target BECAUSE the literature value is
low-precision requires knowing the literature value's precision, which is
itself a literature claim.

Corollary, and it is not a technicality: if the provenance of a candidate
cannot be established, that candidate is not disqualified -- it is
*promoted*, since unclear provenance is exactly the condition Phase 1 exists
to address. But the unclear provenance must be RECORDED as the finding, not
resolved by assumption.

## Entry condition #10 (new)

Every control in the harness must be constructed from something the suspect
path cannot influence. Verified failure of this for positive controls built
over the passed-in basis (L-044). Applies to any new check added in Phase 1.

---

## 4. The six provenance columns (operator-supplied schema, revision 4)

The prose ranking in section 3 is replaced by a scored table. Six columns;
audit value is high when the LEFT columns are weak and the RIGHT are strong.

| # | Column | What is recorded | Levels |
|---|---|---|---|
| P1 | Published precision | digits ACTUALLY PRINTED in the source, not the precision claimed | 0 / 1-5 / 6-15 / 16+ |
| P2 | Proof status | conjectured only / proved once / proved independently >= 2 | C / P1 / P2+ |
| P3 | Numerical independence | was the printed digit string produced by a method OTHER than the derivation it appears in? | yes / no / unknown |
| P4 | Convention risk | is the normalisation stated in the BODY, or only in the abstract? | body / abstract-only |
| P5 | Recomputability | does a Fredholm/Toeplitz form exist that our Nystrom path can evaluate? | yes / no |
| P6 | Downstream reuse | is the constant cited and reused, so an error propagates? | high / low |

Scoring rule: research value HIGH when P1 low, P2 = C or P1, P3 = no/unknown,
and P5 = yes. Value NIL when P1 = 16+ and P2 = P2+ -- that is calibration.

P3 deserves emphasis because it is the column most often silently absent. A
digit string generated by evaluating the very closed form under test is not
evidence for that closed form; it is a restatement of it. This is L-039
(the PSLQ hit that could only have found the relation placed in its basis)
in literature form, and it is why P3 is separated from P1.

P4 is this session's own bug promoted to a column: see L-034 (the alpha
vs 2*alpha abstract/body trap) and L-051 (the sigma -> -sigma sign trap).
Note the mitigation now available -- for any target with a KNOWN log
coefficient or known sign structure, the numerics adjudicate the convention
(L-051), so P4 = abstract-only is a hazard we can DISARM rather than a
disqualifier. Record it anyway: the disarming has to be performed.

### The calibration end of the table (established this session)

| target | P1 | P2 | P3 | P4 | P5 | P6 | value |
|---|---|---|---|---|---|---|---|
| sine-kernel gap constant (T-4) | 16+ | P2+ (Krasovsky 2004; Ehrhardt 2006; DIKZ 2007) | yes | body (OS-1 discharged) | yes | high | **NIL -- calibration** |

By construction. Reproducing it is what earned the right to make Phase 1
claims; it cannot itself be a Phase 1 claim.

### 5. Candidate list -- CONJECTURED, and every row is a HYPOTHESIS TO CHECK

**Tag: CONJECTURED. Provenance: operator, second-hand, explicitly caveated
by the operator as "my picture of what's currently open stops in May, and
this subfield publishes fast."**

HARD RULE 2 applies without exception: these are not findings. NO CELL BELOW
IS FILLED, because filling it from an abstract, or from recollection, would
be the next instance in the bug taxonomy -- the operator named this outcome
in advance ("a triage table built from abstracts would be the twelfth
instance"), and instance 12 was found in code the same day (L-049).

Structural pattern offered with the list, ALSO CONJECTURED and ALSO to be
checked: in the large-gap literature the CONSTANT TERM is consistently the
last thing proved -- thirty years for the sine kernel. And for the
thinned/deformed case (gamma < 1) the constant reportedly comes out
explicitly in Barnes G, whereas the unthinned gamma = 1 case has a
super-exponential leading term and a harder constant. If that pattern holds,
the gamma = 1 constants for newer kernels are the slot where "conjectured,
low precision, single source" is most likely to be true. THIS IS A SEARCH
HEURISTIC, NOT EVIDENCE, and it must not be allowed to pre-select the answer.

| candidate | pointer as given (UNVERIFIED) | P1 | P2 | P3 | P4 | P5 | P6 |
|---|---|---|---|---|---|---|---|
| Pearcey determinant on L^2(-s,s) | arXiv:2002.06370, CMP 2021 | ? | ? | ? | ? | likely yes | ? |
| hard-edge Pearcey determinant | arXiv:2209.12524 | ? | ? | ? | ? | likely yes | ? |
| confluent hypergeometric kernel | (no pointer given) | ? | ? | ? | ? | likely yes | ? |
| two-interval Airy / two-interval sine | Krasovsky-Maroudas, arXiv:2108.04495 | ? | ? | ? | ? | likely yes | ? |
| Fisher-Hartwig prefactors | Deift-Its-Krasovsky 2008 | ? | P2+ (claimed) | ? | ? | yes | high |
| Airy-kernel (Tracy-Widom) constant | Deift-Its-Krasovsky 2008 | ? | P2+ (claimed) | ? | ? | yes | high |
| Jin-Korepin XX-chain additive constant | OS-4, open | ? | ? | ? | ? | ? | ? |
| emptiness formation probability | OS-5, open | ? | ? | ? | ? | ? | ? |

P5 is marked "likely yes" only where the operator states the kernel is
Nystrom-evaluable on an interval; that claim is cheap for us to CHECK
directly and expensive to assume, so it is checkable-by-us rather than
literature-dependent -- the one column we can fill without a primary source.

### 6. Entry condition #11 (new)

A candidate may not be selected on the basis of an UNFILLED provenance row.
Since P1-P4 all require primary sources, and HARD RULE 2 makes every
operator- or memory-supplied value CONJECTURED, Phase 1 target selection is
BLOCKED pending operator-confirmed primary provenance for at least the
selected candidate. This is the intended state, not a failure: the entry
condition exists precisely so that the block is visible.

Note the asymmetry that makes this affordable: the block is on SELECTION, not
on capability. The pipeline reach question is settled (section 3), so nothing
is idle-waiting on computation.

### 7. What is NOT a Phase 1 target, though it is tempting

The beyond-all-orders constant C in E_trunc ~ C*exp(-2s)/s, now measured to
have a 1/s prefactor (L-050) and C ~ 10^-2.7 relative. This is a genuine
mini-target and it is OURS -- but identifying C needs the residual measured
DIRECTLY to many digits, not inferred from an honest-digit count, which is a
different instrument from the one we have. Logged as adjacent; explicitly not
chased. The operator's framing is right: this is the kind of adjacent shiny
thing that eats a Phase 1.


---

# REVISION 5 — THE TABLE, FILLED FROM PRIMARIES

<!-- ACTIVE-TRIAGE -->

**Every cell below was read from the BODY of the cited paper** (ar5iv full
text, Section 1 / Theorem 1.1 in each case), not from an abstract and not
from recall. Where a cell is filled from an abstract it is marked `[abs]`
and treated as weaker evidence. Tag: **STRUCTURAL** (cited theorem
statements, read directly) except where marked.

## Method, and its stated limits

Sources: arXiv full text via ar5iv, plus the arXiv API listing service for
currency checks. Queries run 2026-08-15/16:

  * `all:"Pearcey determinant" OR all:"Pearcey process"` -> 28 results
  * `abs:"large gap asymptotics"` -> 21 results
  * `abs:"confluent hypergeometric kernel"` -> 7 results

**Limits of this search, stated because a negative result is being claimed.**
The arXiv API `abs:`/`all:` fields index METADATA (title, abstract, authors,
comments), NOT full text. A determination of one of these constants that is
(a) published in a journal without an arXiv posting, (b) posted with an
abstract not using these phrases, or (c) buried in a paper about something
else, would be MISSED. The claim below is therefore precisely: *no arXiv
posting whose metadata matches these queries announces a value for the
gamma = 1 constants, as of 2026-08-16.* It is not "these constants are
open". That distinction is the whole point of the P1 column.

## The live table

| # | candidate | primary read | P1 published precision | P2 proof status | P3 numerical independence | P4 convention risk | P5 recomputable | P6 downstream reuse | verdict |
|---|---|---|---|---|---|---|---|---|---|
| C-1 | **Pearcey determinant, gamma = 1** | arXiv:2002.06370 Thm 1.1 (body) | **0 digits** — no numerical value printed anywhere | expansion PROVED (RH steepest descent); constant NOT DERIVED, no closed form even conjectured | n/a — no digit string exists | **body** (kernel (1.2)-(1.3), operator on L^2(-s,s), F in (1.6)) | **yes** — p, q are 1-D integrals; on arg t = pi/4, t^4 = -|t|^4 so q's integrand DECAYS | moderate-high (cited by counting-function/CLT work) | **PRIMARY PHASE 1 TARGET** |
| C-2 | hard edge Pearcey, gamma = 1 | arXiv:2209.12524 Thm 1.1 (body) | **0 digits** | expansion PROVED; "we cannot evaluate explicitly the constant C" | n/a | **body** (kernel (1.1)-(1.2), operator on L^2(0,s)) | yes, harder — contours encircle an essential singularity e^{1/(2t^2)} at 0 | moderate | **ALTERNATE** |
| C-3 | confluent hypergeometric, n=1 multi-interval | arXiv:2508.10463 [abs] | **0 digits** | "a precise large gap asymptotics **up to an undetermined constant**" | n/a | not yet read (body not fetched) | yes — mpmath has `hyp1f1` | moderate | **ALTERNATE, body unread** |
| C-4 | tacnode, unthinned | arXiv:2307.05622 [abs] | **0 digits** | constant term obtained "in the thinned case" only | n/a | not read | plausible, kernel more involved | moderate | alternate |
| C-5 | hard edge tacnode, unthinned | arXiv:2412.12920 [abs] | **0 digits** | constant term "in the thinned case" only | n/a | not read | plausible | low-moderate | alternate |
| C-6 | two-interval Airy | arXiv:2108.04495 Thm 1 (body) | closed form GIVEN: chi = (1/4)log(a-c) - (1/8)log|2q(a)q(b)q(c)| + c_sine + chi_Airy | PROVED; independent simultaneous analysis by Blackstone-Charlier-Lenells left chi' UNDETERMINED | n/a | body | yes | high | **SOLVED — calibration, not a target** |
| C-7 | higher-order Tracy-Widom multiplicative constant | arXiv:2501.12679 [abs] | closed form given (integral of a P_I hierarchy Hamiltonian) | PROVED (2025), explicitly "resolving an open problem in the work of Claeys, Its and Krasovsky" | n/a | not read | Painleve-I-hierarchy kernels, hard | moderate | **RECENTLY CLOSED — not a target** |
| T-4 | sine-kernel (this session) | arXiv:2108.04495 body, eqs (7)-(8) | 16+ (closed form) | **P2+**: "justified in 3 different ways" | yes | body | yes | high | **NIL — calibration** |

## Three findings, none of which I expected to be able to state

**F1. The operator's gamma < 1 / gamma = 1 heuristic is CONFIRMED from
primaries, across six kernel families, and it is stronger than stated.** It
is not a tendency; in this literature it is currently exceptionless:

| kernel | thinned / deformed (gamma < 1) | unthinned (gamma = 1) |
|---|---|---|
| Pearcey | constant DONE (2007.12691) | **undetermined** (2002.06370) |
| hard edge Pearcey | constant DONE (2204.04625) | **undetermined** (2209.12524) |
| tacnode | constant DONE (2307.05622) | not done |
| hard edge tacnode | constant DONE (2412.12920) | not done |
| confluent hypergeometric | constant DONE (2205.03897) | **undetermined** (2508.10463) |

2007.12691's own abstract states the deformed calculation "complements our
previous work on the undeformed case", i.e. the authors treat gamma = 1 as
the case they could not do. This was offered to me as a search heuristic to
falsify; it survived, and it survived from primaries rather than from the
recollection that generated it.

**F2. The relevant frontier is later than the operator's May-era picture,
and moves the same way.** The most recent hit is arXiv:2606.17771 (June
2026, tacnode generating function) — again constant term for the
generating-function/thinned object. The August 2025 confluent
hypergeometric paper still says "up to an undetermined constant". Four
years after 2002.06370 said "we will leave this issue to a future
publication", no such publication appears in this listing.

**F3. P1 = 0 for every live candidate, which is a STRONGER condition than
the column was designed to detect.** The column anticipated low-precision
published values that a high-precision recomputation could challenge. The
actual situation is that **no digit string exists at all**. There is
nothing to disagree with, which removes the entire class of
transcription-risk failure — and also removes any possibility of
calibrating against the target. P3 (numerical independence) is not "no", it
is *undefined*: there is no published number whose provenance could be
independent.

## Why C-1 is the selection

1. P1 = 0, P2 = not derived, P3 undefined — the maximum of the research-value
   scoring rule in section 4.
2. P5 checked BY US, not asserted: the only awkward object is q(y) on the
   four rays arg t = pi/4, 3pi/4, 5pi/4, 7pi/4, and on those rays
   t^4 = -|t|^4, so `exp(t^4/4)` decays. Both p and q are absolutely
   convergent 1-D integrals of entire integrands — exactly the regime
   mpmath's `quad` handles at high precision.
3. **It carries a free, input-derived internal control.** Theorem 1.1 states
   C is *independent of rho*, while the rest of the expansion depends on rho
   through four terms. Computing C at several rho and requiring agreement is
   a check whose constraining side comes from the PUBLISHED THEOREM, not
   from our own output — it satisfies entry condition #10 by construction,
   which is rare and worth spending.
4. The 8/3 power and the -2/9 log coefficient are both published and both
   independently measurable by our pipeline. A wrong normalisation shows up
   in the exponent before it reaches the constant (the L-051 mechanism).

**Selection is RECORDED, not acted on.** Entry condition #2 requires the
target be named before any determinant for it is computed; that is now
satisfied for C-1. No Pearcey determinant has been evaluated.

## Entry conditions: final status

| # | condition | status |
|---|---|---|
| 1 | table filled with provenance | **CLEARED** (this revision) |
| 2 | target selected and recorded before computation | **CLEARED** (C-1, above) |
| 3 | T(b) re-measured at the Phase 1 basis | **PHASE 1 WORK** |
| 4 | pipeline reach demonstrated on the Phase 1 object itself | **PHASE 1 WORK** |
| 5 | null controls shown SENSITIVE at the precision used | **PHASE 1 WORK** |
| 6 | expected basis stated in advance, hit acknowledged as harness-confirmation | **PHASE 1 WORK** |
| 7 | points bought at largest s | superseded (no grid) |
| 8 | every control computes its own resolution at runtime | tooling in place |
| 9 | provenance from PRIMARY sources for the selected target | **CLEARED** — body of 2002.06370 read directly |
| 10 | controls built from what the suspect path cannot influence | tooling in place; C-1's rho-independence check satisfies it |
| 11 | no selection on an unfilled provenance row | **CLEARED** — C-1's row has no unfilled cell |

Conditions 3-6 are deliberately NOT cleared: they are measurements on the
Phase 1 object, and performing them IS Phase 1. Phase 0's gate was 1, 2, 9,
10, 11, and those are now clear.
