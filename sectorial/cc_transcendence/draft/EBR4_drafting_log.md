# EBR-IV drafting log (op:ebr4-3)

Source: `draft/ebr4_v0.tex`. Compiled with MiKTeX pdflatex, two passes,
`-interaction=nonstopmode -halt-on-error`, `SOURCE_DATE_EPOCH=1718150400`.
Build status: **exit 0, 16 pages, 0 undefined references, 0 overfull boxes.**
PDF SHA-256
`AFA69197CE7B53003C561CA717DD6365AC021E869C9F692CE1C293E07C22382B`,
byte-reproducible across three in-place builds and one pristine-temp-dir build.
PDF text-layer forbidden-string scan: **0 genuine hits** (see guard below).

Document class: **`amsart`** (portable). Rationale identical to EBR-III: the
venue is undecided until the op:ebr4-4 memo; a class swap is a one-line change
recorded in the operator runbook. (Skeleton deviation #1.)

Claim coverage: **24 distinct claim_ids cited** (49 `\claim` occurrences); **0
dangling citations** (every `\claim{...}` resolves to a `claims_cc.jsonl`
entry, verified mechanically). Uncited CC3-*/EBR4-* claims are intentional
(see "Intentionally uncited claims").

The re-graded **four-hypothesis** theorem (per ebr4-0, verdict (iii), no
collapse) is transcribed verbatim as Theorem~\ref{thm:main}; the gap list is in
its hardened **G1 + G2/G4 + G5** form (per ebr4-1).

---

## Section-by-section map (`\section`/`\subsection` → skeleton → claim_ids)

### §1 Introduction (`sec:intro`) ← skeleton §1
- 1.1 The program and the object — the object κ, the EBR-I/II/III lineage;
  `eq:kappa`, `eq:kappaC`; Notation remark (`rem:kappa-name`) carries the
  **κ/K rename** and the one-time note of the V_quad-K collision (`CC3-2S2-REN`,
  realized as annotation not citation).
- 1.2 Results and their evidential status (`sec:grades`) — the four-class
  architecture up front; PROVEN defined Lean-only; results R1–R9 listed.
- 1.3 What we do not claim, and the ceiling (`sec:nonclaim`) — the **verbatim
  discipline / non-implication line** and the **CEILING (both directions)**;
  `CC1-DISCIPLINE`.
- *Forbidden-string audit:* abstract + intro make no transcendence claim of any
  kind and no unqualified "is a period" statement.

### §2 Reduction to a rank-2 core and the Borel-2 operator (`sec:reduction`) ← skeleton §2
- 2.1 From the continued fraction to the core H₂ — `eq:ogf`, `eq:H2`;
  `CC3-2-CORE-CHAIN`, `CC3-2-CORE-LOCAL`.
- 2.2 The Borel-2 operator and the home of κ (`sec:borel`) — the order-4 `eq:L`,
  singular {0,1/3}, z=∞ irregular slope ¼ (⇒ exponential periods);
  `CC3-S6-PMAT`.

### §3 Local structure and the Painlevé III(D₈) surface (`sec:surface`) ← skeleton §3
- 3.1 Formal data and non-rigidity — `eq:r`, `eq:rig` (rig = 0); `CC3-2-CORE-LOCAL`,
  `CC3-2S2-RIG`.
- 3.2 The surface-type selector and the D₈⁽¹⁾ label (`sec:rules`) — **RULE S
  selector box reproduced where the D₈ label is first used** (the
  selectors-not-pattern-matching governance point); `CC3-2S2-RULES`.

### §4 The differential Galois group (`sec:galois`) ← skeleton §4
- 4.1 G_Gal(H₂) = SL₂ (`eq:SL2`) — exact Kovacic, ℚ(√3)-emptiness; `CC3-2-KOV`,
  `CC3-2-NF`.
- 4.2 The discipline line, first statement (`sec:discipline1`) — SL₂ bounds the
  group, not the transcendence degree (referee Q5); `CC1-DISCIPLINE`.

### §5 κ as a constructive exponential period (`sec:period`) ← skeleton §5
- 5.1 The connection coefficient A_Φ (`sec:Aphi`) — monodromy spectral projector
  `eq:proj`, `eq:AphiVal`, 129 digits; `CC3-S6-PMAT`.
- 5.2 The κ-bridge (`sec:bridge`) — `eq:kbridge`; Proposition `prop:expperiod`
  (STRUCTURAL) "κ is a constructive exponential period"; `CC3-S6-CLOSE`,
  `CC3-2S2-KAPPA-RES`.
- 5.3 Three independent channels (`sec:channels`) — A/B/C disjoint inputs
  (referee Q4); `CC3-2S2-KAPPA-NUM`.

### §6 The monodromy point and the coverage verdict (`sec:point`) ← skeleton §6
- 6.1 The point (tr M₀, κ) (`sec:pointval`) — `eq:trM0`, hyperbolic ⇒ irreducible;
  `CC3-2S2-2A-COORDS`.
- 6.2 A methodology note (`sec:pointmeth`) — the two integrator-bug catches and
  the 15-dps module-level-mpf hazard; `CC3-2S2-2A-METH`.
- 6.3 The gauge dictionary and the coverage verdict (`sec:coverage`) — the
  **tau-side/Lax-side box** + per-citation ILP/GL statement; **(iii) NOT
  COVERED** (referee Q6); `CC3-2S2-2B-DICT`, `CC3-2S2-2C-VERDICT`.

### §7 Two integer-relation nulls (`sec:nulls`) ← skeleton §7
- 7.1 The elementary null (`sec:nullelem`) — EBR-III frozen battery, cited not
  recomputed; `EBR3-B-GAMMA`, `EBR3-B-CONST`, `EBR3-B-ALG`.
- 7.2 The Barnes–Glaisher log-space null (`sec:nullbarnes`) — positive control
  G(1/2) fires; `CC3-2S2-3-BARNES`.
- 7.3 The null-discipline rule (`sec:nulldisc`) — the rule + the **live false
  positive** it caught in the locus computation; `EBR4-METH-NULLDISC`.

### §8 Off the classical locus (`sec:locus`) ← skeleton §8
- Stratum (R) **unconditional** (SL₂ irreducible), stratum (A) well-resourced
  PSLQ null + infinite order; Remark `rem:G5` states the residual **honestly
  (hardened, not closed)** — referee Q3; `EBR4-1-LOCUS-DIRECT`.

### §9 The conditional theorem (`sec:theorem`) ← skeleton §9 (CENTERPIECE)
- 9.1 The named conjecture (`sec:namedconj`) — Fresán–Jossen `eq:FJ`, cited as a
  **book-in-preparation without an arXiv number** (the verified-false id
  1705.07173 is *not* used).
- 9.2 The differential-to-motivic comparison (`sec:comparison`) — `eq:comp`,
  theorem-grade classically [André], here contingent; **H2 ⊥ H3 made explicit**
  (referee Q1, Q2); `EBR4-0-HYP`.
- 9.3 The theorem (`sec:thmstatement`) — **Theorem~\ref{thm:main} verbatim,
  four hypotheses H1–H4**; drop-one necessity proof discussion;
  `CC3-3-CONDITIONAL`, `EBR4-0-HYP`.
- 9.4 Two facts about κ, never elided (`sec:twofacts`) — the (a) identified /
  nonzero VERIFIED input vs (b) non-algebraicity CONCLUSION split (referee
  stress-test target); `EBR4-1-LOCUS-DIRECT`.
- 9.5 The ceiling, boxed (`sec:ceilingbox`) — **CEILING final form, both
  directions, verbatim**.
- 9.6 The gap list (`sec:gaps`) — **G1 + G2/G4 + G5**, first-class artifact.

### §10 Four-class grade table (`sec:gradetable`) ← skeleton §10
- Per-result rows; **no PROVEN row** (explicit sentence: the machine-checked
  cores are EBR-III's).

### §11 On the Lean substrate (`sec:lean`) ← skeleton §11
- EBR-IV adds no machine-checked core; the four EBR-III cores are the only
  PROVEN items; EBR-IV finitary identities flagged as Lean-core candidates.

### §12 Open problems (`sec:open`) ← skeleton §12
- (1) unconditional transcendence (the ceiling); (2) the motivic realisation
  G2/G4; (3) the full off-locus close G5; (4) Lean-core candidates; (5) the
  **surface-type synthesis pointer** (V on D₅⁽¹⁾ / κ on D₈⁽¹⁾), recorded as a
  pointer not a result.

### Reproducibility (`\section*`) ← skeleton Appendix
- **Deviation #2:** realized as an unnumbered `\section*{Reproducibility}`
  pointing to the op:ebr4-4 `repro_ebr4/` package. Substance unchanged.

### Bibliography
- 21-entry inline `thebibliography` (no `.bib`/bibtex): EBR-I/II/III DOIs, André
  (×3 locators), van der Put–Singer, Kovacic, Sakai, OKSO, Umemura–Watanabe,
  ILP, GL, FIKN, Katz, Fresán–Jossen (book, no number), PSLQ, Mathlib, DLMF.

---

## Two completeness edits during the referee pass (both NON-grade-changing)

Per the ebr3-d rule, a grade-changing finding would HALT before patching; neither
of these is grade-changing, so both were applied inline (the EBR-III F2/F4/F5
precedent). Full detail in `EBR4_referee_findings.md`.

- **F1 (§twofacts H1-smuggle):** added the clause that ℚ̄ ⊆ exponential periods,
  so (H1) membership is no arithmetic constraint and does not pre-judge the
  conclusion. Makes the operator-flagged paragraph self-contained.
- **F2 (localization mechanism):** added the positive mechanism by which (H4) +
  the dimension bound descend to the *single* entry κ (period-torsor: a
  dense-image SL₂ fixes no non-constant off-diagonal coordinate). Closes the
  "trdeg ≥ 3 does not pin *this* κ" gap a referee would raise.

Each edit was followed by a full recompile + byte-reproducibility re-check + the
forbidden-string scan; the final hash above is post-edit.

---

## Forbidden-string guard (mechanical, over the PDF text layer)

Extraction: `pdftotext ebr4_v0.pdf` (MiKTeX), then regex scan (case-insensitive).
Patterns checked: `we prove transcendence`, `proof of transcendence`,
`prove[s]? the transcendence`, `establishes transcendence`,
`is unconditionally transcendental`, `we show … transcendental`, and a
qualifier-stripped `is a period`.

Result: **0 genuine hits.**
- Every "is transcendental" occurrence is inside a conditional "under H1–H4 /
  Assuming … then" clause (abstract and Theorem~4 conclusion), each immediately
  followed by the both-ways conditionality disclaimer.
- The only `is a period` string is inside the guard's own denial sentence
  (§`sec:nonclaim`: "no unqualified statement that κ or C 'is a period'").
- `proves transcendence` appears only negated ("no null proves transcendence";
  "prove nothing about transcendence"); the open-problems list names
  "Unconditional transcendence of C/κ" as item (1), i.e. as **open**.

---

## Intentionally uncited claims (CC3-*/EBR4-*)

The cc-3 program reached the rank-2 core through a longer development than the
final paper retraces; the body cites the **consolidated destination** claims and
omits the route-finding precursors. Four groups:

1. **Development / route-finding (subsumed).** `CC3-0-*` (arithmetic-Gevrey
   location), `CC3-1-*` (Route-A OGF/Borel-2 derivation and the integral-rep
   credibility/obstruction), `CC3-1B-*` (the reduction-hardening Riemann/K/RouteB
   pass), `CC3-1C-*` (the **order-4** irregular-rigidity, z=0 Jordan, L-vs-L₂,
   p-curvature). The paper presents the destination — the H₂ core, the order-4 L
   with slope-¼ ∞, non-rigidity — and cites `CC3-2-CORE-CHAIN`, `CC3-S6-PMAT`,
   `CC3-2S2-RIG`. Citing the precursors would relitigate superseded framings
   (notably the cc3-1b "log-free" reading that cc3-1c corrected).
2. **Superseded.** `CC3-2S2-EXPPER` (κ-as-exp-period, **CONJECTURED-with-
   architecture**) is replaced by `CC3-S6-CLOSE` (**STRUCTURAL**, cited). Citing
   the precursor would understate the result. `CC3-4A-KPSLQ` (the order-4-L
   K-PSLQ null) is subsumed by the cited elementary (`EBR3-B-*`) and Barnes
   (`CC3-2S2-3-BARNES`) nulls.
3. **Rename annotation.** `CC3-2S2-REN` (K→κ) is realized as the Notation remark
   `rem:kappa-name`, not as a cited result.
4. **Process / hygiene.** `CC3-2-ERR-1` (log-free-supersession disposition),
   `CC3-2-CONV-1` (accessory-count convention), `CC3-3-LOCUS` / `CC3-3-CLOSEOUT`
   (the summit-report locus pass and four-class close-out, superseded by the
   **hardened** `EBR4-1-LOCUS-DIRECT` and this paper's own grade table),
   `CC3-2-DIM` (dim H¹_dR feeds H4, stated in the theorem not separately cited).

No dangling `\claim` exists (24/24 cited ids resolve in `claims_cc.jsonl`).

---

## Skeleton-deviation summary
1. `amsart` not a venue class — venue undecided; swap deferred to the ebr4-4
   runbook.
2. Reproducibility realized as `\section*`, not a numbered appendix — substance
   unchanged.
3. Two referee-pass completeness edits (F1, F2 above) — discipline / rigor
   compliance, non-grade-changing.
