# Phase 1 charter — DRAFT, NOT AUTHORIZED

**Status: DRAFT. Phase 1 has NOT begun and is NOT authorized.**
OS-16 is blocked on permission, which is the one kind of block that reading
cannot discharge. This document exists so that the entry conditions are
fixed *before* anyone — including me — is in a position to want them
relaxed. Writing it is not starting it.

Target: **C-1**, the constant term in the large-gap asymptotics of the
Pearcey determinant at γ = 1, arXiv:2002.06370 Theorem 1.1. Recorded in
`phase1_triage.md` REVISION 5 and L-064, before any Pearcey determinant has
been evaluated.

Phase 1 gets **its own ledger** (`ledger_phase1.md`). Phase 0's ledger is
closed at L-067+. The four-round expansion happened because every new
finding landed inside Phase 0's boundary; a fresh boundary is the structural
fix, and adding a boundary is more reliable than adding discipline.

---

## C-0. THE CALIBRATION CONDITION (the charter's central issue)

Everything Phase 0 earned came from task 0.3: a known answer the pipeline
had to reproduce before anything downstream counted. **C-1 has no such
answer by construction** — that is precisely why it was selected. P1 = 0
removes transcription risk and removes the gate with it.

So calibration moves to a sibling:

> **No C-1 evaluation until the same code has reproduced a PROVED constant
> on a kernel it was not developed against.**

* **Airy** (Tracy–Widom constant χ_Airy) is the closest structural relative
  with a proved constant. Primary already read: arXiv:2108.04495 eq. (6)
  states χ_Airy = (1/24)log 2 + ζ′(−1), conjectured by Tracy–Widom and
  proved in two independent places per that paper's §1.
* **Bessel** is the second sibling.
* **The sine kernel DOES NOT COUNT.** That is the kernel this pipeline was
  tuned against for the whole of Phase 0. Reproducing it again measures
  nothing that has not already been measured, and would be the L-039
  circularity at the scale of an entire phase.

This is an entry CONDITION, not a step. It is the only thing standing where
0.3 stood.

## C-1a. Determine the architecture in week one, before building anything

Phase 0's repeated lesson (L-058, three instances) is that the binding
constraint was analysis, not data. The analogue here:

**Question to answer first: does a tail recursion analogue exist for the
Pearcey determinant?** The literature indicates a Hamiltonian and a system
of coupled differential equations rather than a scalar σ-form. A system may
not admit the clean rational recursion that made Phase 0's extraction cost
70 seconds instead of four hours.

The answer decides which project this is:

| recursion exists | this is a ~minute-scale computation per point, precision linear in s |
| recursion absent | this is a Nyström problem at 200+ digits against a kernel defined by double contour integrals |

Determine before building. **Pre-commit (L-058): produce a written argument
for why any limit encountered is data rather than structure, BEFORE buying
compute.** On this project's record the prior is strongly against it.

What does NOT change: the constant will not come from the recursion. A
series fixes everything except its integration constant. So the shape stays
*recursion for the tail, one high-precision evaluation for the constant*.

## C-2. The (s, ρ) scan is a near-complete self-check, and it is also REQUIRED

Theorem 1.1's published expansion is:

```
F(s;ρ) = −9s^(8/3)/2^(17/3) + ρs²/4 − ρ²s^(4/3)/2^(10/3)
         − (2/9)ln s + ρ⁴/216 + C + O(s^(−2/3))
```

Every term except C carries an s-dependence, a ρ-dependence, or both. So an
error in ANY published coefficient shows up as drift in the extracted C
along one axis or the other, and C is by construction the only term constant
in both. A two-dimensional scan therefore checks the entire imported result
— which is the answer to the obvious objection that Phase 1 puts an
unverified literature result on the load-bearing path.

Its constraining side comes from the published theorem, not from our output:
**entry condition #10 satisfied by construction** (L-044's failure mode
cannot occur here).

**A sharpening that makes this more than a control.** The term ρ⁴/216 is
independent of s but not of ρ. At fixed ρ ≠ 0 the extraction cannot separate
it from C — what is measured is `C + ρ⁴/216`. Therefore:

* **evaluate at ρ = 0 to isolate C**, where that term vanishes identically;
* **use ρ ≠ 0 as the control**, requiring the recovered `C(ρ) − ρ⁴/216` to
  be ρ-independent to the claimed precision.

Reading ρ ≠ 0 as if it gave C directly would be a convention trap of exactly
the L-034 / L-051 shape, and it is disarmed here in advance rather than
after a wrong number.

## C-3. Basis design comes from the thinned case, not a generic menu

Tag: **CONJECTURED** (search heuristic, operator-suggested, not evidence).

The γ < 1 constant is known in Barnes G (arXiv:2007.12691), and the γ → 1⁻
transition connects the two, so the γ = 1 constant plausibly lives in the
same field. Build the basis from what appears in the DEFORMED result rather
than from the standard sine/Airy menu — which requires reading
2007.12691's body first, and that reading is Phase 1 work.

**Specific addition a generic list would miss: `log 3`.** Pearcey carries
cube-root structure throughout — a 3×3 RH problem, exponents in thirds, a
t⁴ scaling with 8/3 and 4/3 powers — whereas sine/Airy/Bessel constants are
rational combinations of log 2 and ζ′(−1) tracking their own 2-fold
structure. If a third-order analogue exists, log 3 is where it shows.

Binding constraints carried forward from Phase 0:
* T(b) **re-measured** at the actual basis size and maxcoeff (entry
  condition #3). The b > 8 extrapolations are CONJECTURED and a T-law was
  fabricated once already (L-030).
* Null controls **shown sensitive at the precision used** (#5, L-018).
* Positive control built from something **the suspect path cannot
  influence** (#10, L-044).
* A hit in a basis built from the thinned constant is
  **harness-confirmation, not independent evidence** (#6, L-027, L-039).

## C-4. PRE-REGISTERED SUCCESS CRITERIA

Declared now, before any computation, because declaring them afterwards is
worthless:

> **A high-precision value for C that PSLQ cannot identify COUNTS AS
> SUCCESS AND AS THE DELIVERABLE.**

The authors of arXiv:2002.06370 wrote that evaluating C "is a challenging
problem" and that they "leave this issue to a future publication." A
high-precision determination is a contribution independent of any closed
form.

This pre-commitment exists to defuse a specific, predictable failure: an
unidentified constant creates pressure to grow the basis until something
fits, and Phase 0's own null-control history (L-019, L-034, L-039) shows
what that produces. **The basis is declared before the search and is not
enlarged in response to a null result.** Enlarging it is permitted only as
a separately logged, separately controlled experiment with T re-measured at
the new size.

## C-5. Honest-digit budget with no external check

On the sine kernel the honest digit count could be cross-checked against a
closed form. Here it cannot. The budget must therefore be entirely
self-certifying:

* node doubling **and** a ≥ 20-digit precision bump (task 0.1 protocol);
* cross-s agreement between independent evaluations;
* cross-ρ agreement per C-2;
* and the reported figure is the FIT/EXTRACTION uncertainty, never `mp.dps`.
  Conflating those two was named a session failure in the Phase 0 brief and
  the rule survives unchanged.

## C-6. Blocking items

* **OS-20 BLOCKS any novelty claim.** Metadata search establishes that no
  arXiv posting *announces* a value; it does not establish that the
  constant is open. The check is the forward-citation graph of
  arXiv:2002.06370 — someone may have evaluated C incidentally in a paper
  about something else. Do this BEFORE writing, not after.
* **OS-19**: read the body of arXiv:2508.10463 if C-1's evaluation proves
  harder than C-2's architecture study predicts.
* Contacting the authors (OS-22) is an **operator decision** and is not
  taken unilaterally. HARD RULE 5 forbids external submission; a value in
  hand does not change that.

## What Phase 1 does NOT inherit

Phase 0's certified data, digit-loss law, and `m* ≈ 2s` truncation optimum
are properties of the **sine kernel**. A different kernel has different
conditioning and a different digit-loss law (entry condition #4). Nothing in
`out/certified_data.json` is evidence about Pearcey.


---

## FREEZE (L-073)

**This charter is CLOSED TO ADDITIONS.** C-0 through C-4 are the entry
conditions for Phase 1. No further condition may be added before the Airy
calibration of C-0 has actually been RUN.

Rationale, which is the opposite of the usual one: the demonstrated risk to
this project is not loose conditions but an indefinitely deferred start.
Phase 0 stayed open for six rounds of individually worthwhile hardening.
Anything that would have become C-5 goes to `open_questions.md` and is
considered only once there is a number to discuss.

Note that this freeze is a REMOVAL of future work, not another condition. A
condition forbidding conditions would be the failure mode wearing the
uniform of its own remedy.
