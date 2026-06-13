# EBR-III drafting log (op:ebr3-c)

Source: `draft/ebr3_v1.tex`. Compiled with MiKTeX pdflatex (MiKTeX-pdfTeX 4.23
/ MiKTeX 25.12), two passes, `-interaction=nonstopmode -halt-on-error`.
Build status: **exit 0, 13 pages, 0 undefined references, 1 residual overfull
hbox of 2.49 pt (sub-millimetre, invisible).** PDF text-layer forbidden-string
scan: **0 hits** (see §"Forbidden-string guard" below).

Document class: **`amsart`** (portable), *not* `etna.cls`. Rationale: venue is
undecided until op:ebr3-f; a class swap is a one-line change recorded in the
operator runbook. (Skeleton deviation #1.)

Claim coverage: **39 of 41** ledger claims are cited in the body; **0** dangling
citations (every `\claim{...}` resolves to a ledger entry). The two uncited
claims are intentional (see "Intentionally uncited claims").

---

## Section-by-section map (actual `\section`/`\subsection` → skeleton → claim_ids)

### §1 Introduction (`sec:intro`) ← skeleton §1
- 1.1 Background and object of study — `CC1-OP-L2`, `CC1-INF-IRREGULAR`.
- 1.2 Results and their evidential status (`sec:grades`) — the four-class
  grade architecture stated up front (not as apology); `proven` defined as
  Lean-only. Lists R1–R6.
- 1.3 What we do not claim (`sec:nonclaim`) — the **verbatim non-implication
  line**; `CC1-DISCIPLINE`, `CC2-0-CC3-AMEND`.
- *Forbidden-string audit:* abstract + intro carry the normalization scope on
  the not-a-G-function result and make no transcendence claim of any kind.

### §2 The operator and its singular structure (`sec:operator`) ← skeleton §2
- 2.1 Riemann data at the regular points — `CC1-OP-L2`, `CC1-RIEMANN`
  (eq. `eq:operator`, `eq:riemann`).
- 2.2 The irregular point at infinity (`sec:inf`) — `CC1-INF-IRREGULAR`.
- 2.3 Accessory count and non-rigidity — `CC1-ACCESSORY`.

### §3 Arithmetic nature: not a $G$-operator (`sec:gfun`) ← skeleton §3
- *Mandatory scope statement present:* result is for the Borel normalization
  $g_n=Q_n/(2n)!$, does not extend to arbitrary rescalings.
- 3.1 Integrality and denominator growth — `CC2-0-QINT`, `CC2-0-GFUNC`.
- 3.2 Two confirming channels — `CC2-0-PCURV` ($p$-curvature), trichotomy lead-in.
- 3.3 Consequence for the period route — `CC2-0-TRICHOTOMY`, `CC2-0-CC3-AMEND`.
- **Deviation #2:** skeleton planned five subsections (3.1–3.5); consolidated to
  three. No content or claim dropped — $p$-curvature and the
  André–Chudnovsky–Katz trichotomy are folded into 3.2/3.3.

### §4 Irreducibility and minimality (`sec:irred`) ← skeleton §4
- 4.1 Formal module at infinity — `CC1-IRREDUCIBLE`.
- 4.2 Exhaustive low-order factor exclusion — `CC2-0-FACTOR`.

### §5 Local monodromy and the semisimple correction (`sec:local`) ← skeleton §5
- 5.1 Monodromy at $R$ is a semisimple pseudo-reflection — `CC2-2D-JORDAN`,
  `CC4-1-NOLOG` (no-log confirmation folded in here).
- 5.2 Erratum (`sec:erratum`) — `CC4-ERR-1`; DOI-pinned supersession of the
  EBR-II "resonance logarithm" narration ($\gamma=11/6\notin\Z$).
- **Deviation #3:** skeleton placed the Erratum as Appendix A; realized instead
  as §5.2, adjacent to the correction it documents. Content unchanged, DOI-cited.

### §6 The differential Galois group (`sec:main`) ← skeleton §6 (MAIN THEOREM)
- 6.1 Determinant and the $\SL_4$ normalization — `CC2-1-EXPTORUS`, `CC2-1-TWIST`.
- 6.2 No invariant form $C_5,C_6$ ($\SO_4$, $\Sp_4$) (`sec:selfdual`) —
  `CC2-2A-SELFDUAL`, `CC2-2B-SP4`, `CC2-2C-SO4`.
- 6.3 Tensor-induced classes $C_4$, $S$ — `CC2-2D-TENSOR`.
- 6.4 The imprimitive classes $C_2,C_3$ and primitivity — `CC2-2D-IMPRIM`,
  `CC4-A1-ETA-UNIQUE`, `CC4-A1B-MONOMIAL-CLOSURE`, `CC4-0-ROUTE1-PRIMITIVE`,
  `CC4-0-ROUTE2-PRIMITIVE`.
- 6.5 Completeness of the searches (`sec:bounds`) — `CC4-0B-BOUNDS`.
- 6.6 The classification and the main theorem — Aschbacher 8/8 table;
  `CC4-0-SL4-VERDICT`. Theorem `thm:main`.
- **NEW (per ebr3-c prompt) — taxonomy framing:** the 8/8 elimination is
  presented as the **maximal-subgroup classification of the algebraic subgroups
  of $\SL_4$** in the differential-Galois (van der Put–Singer) setting, with the
  Aschbacher class labels $C_1$–$C_8$, $S$ used as organizing vocabulary and
  cited as such — explicitly **not** as an application of the finite-group
  Aschbacher theorem.

### §7 The non-Liouvillian corollary and the bridge (`sec:bridge`) ← skeleton §7
- Corollary `liouville` (no Liouvillian solutions) — `CC4-2-BRIDGE`; then the
  bridge with the verbatim non-implication line repeated; `CC1-DISCIPLINE`.

### §8 Connection data and the integer-relation null (`sec:numerics`) ← skeleton §8
- 8.1 The connection coefficient to 169 digits — `CC4-1-C-120D`, `CC4-1-MONODROMY`;
  honest interval note (mpmath `mpf`, not formal Arb intervals → VERIFIED).
- 8.2 Stokes structure, and what is out of scope (`sec:stokes`) — `CC4-1-STOKES`;
  *mandatory scope statement:* numerical Stokes multipliers are OUT OF SCOPE
  (ramified slope 1/4), flagged not proxied.
- 8.3 The integer-relation null as exclusion bounds (`sec:null`) — `EBR3-B-GAMMA`,
  `EBR3-B-CONST`, `EBR3-B-ALG`.
- **NEW (per ebr3-c prompt) — null-as-exclusion-bounds:** per tier we derive the
  precision-detection ceiling $H_{\max}\approx10^{150/(n-1)}$ (a spurious
  height-$H$ relation among $n$ terms has residual $\sim H^{-(n-1)}$; the search
  is precision-limited only if $H^{-(n-1)}$ falls below tolerance), tabulate
  searched height vs ceiling, and conclude "any relation has height exceeding
  the searched $H$." The derivation is in prose; **no recomputation** of the
  frozen ebr3-b artifact. Positive-control fires reported as battery validation.

### §9 Lean cores and the axiom audit (`sec:lean`) ← skeleton §9
- Four PROVEN cores — `CC4-LEAN-BOUNDS`, `CC4-LEAN-PULLBACK`, `CC4-LEAN-PARITY`,
  `CC4-LEAN-A1B`. lean4 v4.30.0 + Mathlib rev c5ea0035; axiom cones audited.

### §10 Four-class grade table (`sec:gradetable`) ← skeleton §10
- Per-result rows (grade + evidence claim_ids); the only PROVEN rows are the
  four Lean cores; transcendence of $C$ row carries grade C, `CC1-DISCIPLINE`.

### §11 Open problems (`sec:open`) ← skeleton §11
- Five items with op-codes: transcendence of $C$ (op:cc-3, period route);
  numerical Stokes multipliers; general $d$; the rigidity index; the rigidity
  dividing-line conjecture restated precisely.

### Reproducibility (`\section*`) ← skeleton Appendix B
- **Deviation #4:** skeleton placed reproducibility as Appendix B; realized as an
  unnumbered `\section*{Reproducibility}` pointing to the op:ebr3-e `/repro`
  package. Substance unchanged.

### Bibliography
- 8 references: EBR-I (concept `10.5281/zenodo.20564079`, v1.0 `20564080`),
  EBR-II (concept `10.5281/zenodo.20566465`, v1.2 `20571232`), van der Put–Singer,
  André, Katz, Kovacic, PSLQ (Ferguson–Bailey–Arno), Mathlib. Inline
  `thebibliography` (no `.bib`/bibtex needed).

---

## Forbidden-string guard (mechanical, over the PDF text layer)

Extraction: `pdftotext ebr3_v1.pdf ebr3_v1.txt` (MiKTeX), then regex scan.
Patterns checked (case-insensitive): `we prove transcendence`,
`prove[ds]? the transcendence`, `proof of transcendence`, `C is transcendental`,
`transcendence of C is (proven|established|proved)`, `is a period`,
`is a transcendental period`, `we prove four`.

Result: **0 genuine hits.** Two pre-edit flags, both resolved:
- `\textbf{Deviation #5}` — colloquial "We prove four things" (none of the four
  headline results are Lean-PROVEN) → reworded to "We **establish** four things".
- "The sole route is a period interpretation" (could read as asserting $C$ is a
  period) → reworded to "via a **period-theoretic analysis**".
- The remaining match `proof of transcendence` is inside the explicit disclaimer
  "it is **not** a proof of transcendence, and we do not present it as one" —
  retained intentionally (it is the discipline statement).

## Intentionally uncited claims (2 of 41)

- `CC2-2E-VERDICT` (STRUCTURAL-conditional) — the **superseded** intermediate
  verdict ("SL4 conditional on the cc2-4 primitivity check"). Replaced in the
  paper by the final unconditional, bound-complete `CC4-0-SL4-VERDICT` (§6.6).
  Citing the conditional precursor would misrepresent the result's status.
- `CC4-ERR-2` (VERIFIED) — a process/ledger-hygiene **disposition** ("scope-patch
  audit CONFIRMED; no patch required"), not a mathematical result. Its substance
  (the not-a-G-function finding is normalization-scoped) is reflected wherever
  that result appears (abstract, §1, §3, §10).

## Skeleton-deviation summary (each with one-line justification)
1. `amsart` not `etna.cls` — venue undecided; swap deferred to ebr3-f runbook.
2. §3 five planned subsections → three — consolidation only; no claim dropped.
3. Erratum realized as §5.2, not Appendix A — placed adjacent to the correction.
4. Reproducibility realized as `\section*`, not Appendix B — substance unchanged.
5. Two forbidden-string-guard rewrites (above) — discipline compliance.
