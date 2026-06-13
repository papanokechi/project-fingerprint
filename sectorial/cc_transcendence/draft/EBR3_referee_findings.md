# EBR-III adversarial referee findings (op:ebr3-d)

Reviewer stance: hostile referee under SIARC four-class discipline. Each grade
checked against its evidence type; every citation locator verified present; the
Aschbacher table audited for silent gaps; the degree-bound derivation re-read
for the apparent-singularity caveat; all stated dps checked for honesty.

**Conditional-HALT status: NOT triggered.** No finding changes any claim's
*grade*; all findings are wording or completeness. Per the stage rule, drafting
continues.

**Counts: fixed = 4 · accepted = 1 · grade-affecting = 0.**

---

## Findings

### F1 — Aschbacher class labels mis-numbered  [FIXED · wording]
The draft labelled $\SO_4,\Sp_4$ as classes $C_5,C_6$. In the standard
Kleidman--Liebeck / Aschbacher *geometric* numbering the classical-form
subgroups are class **$C_8$**, while $C_5$ = subfield, $C_6$ = extraspecial
normalizer, $C_7$ = tensor-induced (verified against the Kleidman--Liebeck
scheme). A referee answering Q2 would catch this immediately. The inherited
ledger never assigned $C_5/C_6$ to the forms (claims call them "SO4"/"Sp4";
only $C_2$ = monomial and $S$ = $\Sym^3$ are class-numbered there), so the
mis-numbering was introduced in drafting, not inherited.
- Fix: relabelled $\SO_4,\Sp_4\to C_8$ in the table and the §6.2 heading; added
  an explicit numbering sentence to the §6 intro ($C_8$ forms, $C_5$ subfield,
  $C_6$ extraspecial, $C_7$ tensor-induced); added a $C_5$ row (vacuous over
  $\overline{\C}$, char $0$) and merged $C_7$ with $C_4$ (shared identity
  component $\SL_2\otimes\SL_2$); retitled §6.3 to "$C_4$, $C_7$, $S$"; the
  "finite" row is now "$C_6$/fin." (extraspecial-type / finite, killed by the
  torus). All of $C_1$–$C_8$, $S$ now appear explicitly with no silent gap.
- Grade impact: **none.** The exclusions and their V/S grades are unchanged;
  only the organizing labels were corrected.

### F2 — Colloquial "prove" / "period" phrasing  [FIXED · wording]
"We prove four things" (none of the four headline results is Lean-PROVEN) and
"the sole route is a period interpretation" (could read as asserting $C$ is a
period). Fixed to "We **establish** four things" and "via a **period-theoretic
analysis**". (Also logged in the ebr3-c drafting log; the mechanical PDF
text-layer scan is now 0 hits.)
- Grade impact: **none.**

### F3 — Two ledger claims uncited in the body  [ACCEPTED · with reason]
`CC2-2E-VERDICT` and `CC4-ERR-2` are in the 41-claim ledger but not cited.
Accepted as intentional:
- `CC2-2E-VERDICT` is the *superseded* STRUCTURAL-conditional verdict ("SL4
  conditional on the cc2-4 primitivity check"); the paper cites its
  unconditional replacement `CC4-0-SL4-VERDICT`. Citing the precursor would
  misstate the result's status.
- `CC4-ERR-2` is a process/ledger-hygiene disposition ("scope-patch audit
  CONFIRMED; no patch required"), not a mathematical result; its substance (the
  not-a-$G$-function finding is normalization-scoped) is present wherever that
  result appears.
- No dangling citations exist (39/41 cited, 0 `\claim` ids absent from ledger).

### F4 — Q4 ("why $d=2$ only / what breaks") answered too thinly  [FIXED · completeness]
Strengthened §11 item 3 with the three $d$-specific ingredients that do not
transfer: the determining-factor orbit is a single $4$-cycle at $d=2$ (a
transitive $\Z/2d$-orbit at general $d$, enlarging the slope-additivity
enumeration); the target group becomes $\SL_{2d}$ with a larger maximal-subgroup
list; and the a priori degree bounds must be recomputed from order-$2d$ exponent
data. Arithmetic conclusions "expected to persist but not established here".
- Grade impact: **none** (scope/wording only).

### F5 — Q1 ("trust irreducibility absent full DFactor") not stated as such  [FIXED · completeness]
The two routes were present (§4.1 formal module, §4.2 factor enumeration) and
§4.1 already noted "an independent `DFactor`-style confirmation was unavailable
on the host", but the *trust basis* was not stated. Added a closing sentence to
§4: the two routes are logically independent (one local-analytic, one a finite
combinatorial enumeration), neither relies on a decision procedure, and
irreducibility is graded STRUCTURAL on the strength of their agreement — and it
is this irreducibility the §6.5 bound completeness later makes load-bearing.
- Grade impact: **none.**

---

## Anticipated referee questions — where answered IN THE PAPER

1. **Why trust STRUCTURAL irreducibility without a full `DFactor`?** §4
   (two independent routes; explicit DFactor-unavailable note; new trust-basis
   sentence) + the §6.5 bound-completeness that makes it load-bearing.
2. **Is the maximal-subgroup taxonomy correctly sourced for algebraic groups?**
   §6 intro: the strategy is the maximal-subgroup classification of *algebraic*
   subgroups of $\SL_4$ following van der Put--Singer Ch.4; Aschbacher labels are
   organizing vocabulary, explicitly *not* the finite-group Aschbacher theorem;
   correct $C_8/C_5/C_6/C_7$ numbering now stated.
3. **Is the semisimple erratum unambiguous and DOI-pinned?** §5.2: names EBR-II,
   the superseded "unipotent / resonance logarithm" reading, the criterion
   $\gamma\in\Z$ vs $\gamma=11/6$, the concept DOI `10.5281/zenodo.20566465` and
   current version `10.5281/zenodo.20571232` (v1.2), and that the load-bearing
   claims (exponents, irreducibility, irregular-$\infty$) are unaffected.
4. **Why $d=2$ only and what breaks at general $d$?** §11 item 3 (now specific).
5. **Is "not a $G$-function" normalization-scoped everywhere?** Abstract ("in the
   Borel normalization $g_n=Q_n/(2n)!$"), §1.2 R1 ("In the normalization (1)"),
   §3 (mandatory scope statement), §10 grade-table row ("normalization-scoped").

## Standing audits (all pass)

- **Grades vs evidence.** PROVEN reserved for the four Lean cores (§9, audited
  cones); SL$_4$ theorem STRUCTURAL with enumerated inputs; the 169-digit $C$ and
  the PSLQ null VERIFIED (with the honest "mpmath `mpf`, not formal Arb
  intervals" note); no-Liouvillian V/S (verified-by-citation + structural
  application); transcendence of $C$ CONJECTURED. Consistent throughout.
- **Locators.** 0 dangling `\claim` citations; 0 undefined `\ref`/`\eqref`
  (LaTeX log clean); EBR-I/II DOIs correct.
- **Aschbacher table.** After F1, all of $C_1$–$C_8$, $S$ present and correctly
  labelled; no silent gap.
- **Bound derivation (apparent-singularity caveat).** §6.5 derives $B_2=3$,
  $B_1=7$ from integer $\End$-exponents and explicitly invokes the semisimplicity
  of $M_0,M_R$ (no logarithm $\Rightarrow$ single-valued horizontal section, no
  apparent-singularity pole inflation), so the bound is honest.
- **Stated-dps honesty.** 169 digits throughout (mpmath `mpf`, VERIFIED not
  PROVEN); null battery at working precision $\le169$; matches the frozen ebr3-b
  artifact (`9a3f942d…`).

## Build state after fixes
`pdflatex` (MiKTeX) two passes: exit 0, 14 pages, 0 undefined references,
forbidden-string scan over the PDF text layer = 0 hits, residual overfull boxes
$\le2.49$ pt (sub-millimetre).
