# EBR-IV adversarial referee findings (op:ebr4-3)

Reviewer stance: hostile referee under SIARC four-class discipline. Every grade
checked against its evidence type; every locator verified present (0 undefined
citations in the LaTeX log); the conditional theorem re-read line-by-line for
the circularity a hostile reader would hear; the CEILING audited in both
directions; the tau-vs-Lax line audited at every crossing; all stated dps and
hashes checked for honesty.

**Conditional-HALT status: NOT triggered.** No finding changes any claim's
*grade*. The two substantive findings (F1, F2) are completeness fixes that make
the theorem self-contained against the sharpest referee questions; both leave
the conclusion (κ ∉ ℚ̄ under H1–H4, grade **C**) and every hypothesis grade
unchanged. Per the stage rule (ebr3-d standard), drafting continues.

**Counts: fixed = 2 (both completeness) · accepted/pass = 4 · grade-affecting = 0.**

Final build: `ebr4_v0.pdf`, SHA-256
`AFA69197CE7B53003C561CA717DD6365AC021E869C9F692CE1C293E07C22382B`,
16 pages, byte-reproducible (3 in-place builds + pristine-temp-dir build all
identical), 0 undefined references, 0 overfull boxes, forbidden-string scan 0
genuine hits.

---

## Findings

### F1 — §twofacts circularity: the "H1-smuggle" reading  [FIXED · completeness]
*This is the paragraph the operator flagged for explicit stress-testing.*
The draft already separated the two facts correctly — (a) κ = A_Φ is the
identified, non-vanishing off-diagonal entry (VERIFIED, input H4); (b) its
non-algebraicity is the conclusion under H1–H4 — and the drop-one analysis
already shows H1 alone is arithmetically inert. **But** a hostile referee
reading §`sec:twofacts` *in isolation* (three subsections before the drop-one)
could still hear a subtler circularity: H1 asserts "κ **is** an exponential
period," which sounds like a strong arithmetic statement smuggling the
conclusion. The defeater — that ℚ̄ itself lies inside the ring of exponential
periods, so membership is no arithmetic constraint — was implicit in the
drop-one but not stated in §twofacts.
- Fix: added one clause to §twofacts making the membership-vs-algebraicity point
  explicit and local: *"Membership in the ring of exponential periods is, by
  itself, no arithmetic constraint — ℚ̄ lies inside that ring — so (H1) does not
  pre-judge (b); the non-algebraicity is supplied only by the dimension lower
  bound (H2) feeding the period conjecture (H3)."* The paragraph is now
  self-contained against the H1-smuggle reading.
- Grade impact: **none.** H1 stays STRUCTURAL; the (a)/(b) split is unchanged.

### F2 — Localization of the dimension bound to the single entry κ  [FIXED · completeness]
The substantive hostile-referee finding. Theorem~\ref{thm:main} concludes
"trdeg_ℚ⟨periods(M)⟩ = dim G_mot(M) ≥ 3 **and** the off-diagonal entry κ is not
algebraic." The first conjunct is an **algebra-level** bound; the second is a
statement about **one specific entry**. A referee will object that trdeg ≥ 3 of
the whole period algebra does not, on its face, force *this* κ to be
transcendental — the transcendence could a priori live in other entries. The
draft named H4 as the bridge ("κ is the non-vanishing off-diagonal entry, not a
diagonal normalisation") and the drop-H4 line gave the contrapositive, but the
**positive mechanism** by which H4 + the dimension bound descend to κ was not
stated.
- Fix: added the explicit localization mechanism to the drop-one proof
  discussion: in the period-torsor formalism the motivic group acts on the de
  Rham / rapid-decay comparison; an SL₂ of dense image fixes no non-constant
  off-diagonal coordinate of the 2-dimensional realisation; (H4) certifies κ to
  be such an entry, so κ is not in the fixed field ℚ̄ — and *without that
  certificate the dimension bound would not descend to the single entry.*
- Grade impact: **none.** This explicates the role of an existing hypothesis
  (H4, VERIFIED) and the conditional conclusion; it asserts the mechanism within
  the period-conjecture framework (it is part of what H1–H4 deliver), not as a
  new unconditional theorem. The theorem grade stays **C**.

### F3 — Q2 contingency ("why SL₂ licenses a motivic lower bound") never dropped  [PASS]
The comparison dim G_mot ≥ dim G_Gal = 3 \eqref{eq:comp} is theorem-grade in the
classical pure/regular-singular setting [André] but is applied to an
**exponential** motive with an **irregular** connection. Audit: the contingency
("here contingent on the (G4) realisation and the irregular/exponential form of
the comparison") is stated in **all three** places it must be — §`sec:comparison`,
the H2 line of the theorem, and the gap list G2/G4 — and the logical
independence of \eqref{eq:comp} from \eqref{eq:FJ} is spelled out. No overstated
"André gives it directly" reading survives. No edit.

### F4 — H1 vs the "no unqualified 'is a period'" guard  [ACCEPTED · clarified by F1]
The abstract says "this places κ in the ring of exponential (rapid-decay)
periods of the connection," and §`sec:nonclaim` pledges "no unqualified
statement that κ or C 'is a period'." A referee could allege tension. Accepted as
consistent: H1's membership is **graded** (STRUCTURAL), **constructive** (the
rapid-decay pairing / spectral projector), and **scoped** ("of the connection")
— it is exactly *not* the unconditional Kontsevich–Zagier "κ is a period" claim
the guard bans, and after F1 the text states outright that this membership
carries no non-algebraicity content. The mechanical scan confirms the only bare
"is a period" string in the document is inside the guard's own denial sentence.
No edit beyond F1.

### F5 — The surface-type synthesis as a paper open-problem (item 5)  [ACCEPTED]
Open-problem item 5 records the V-family-on-D₅⁽¹⁾ / κ-on-D₈⁽¹⁾ Sakai-surface
synthesis thread. A referee might call it out of scope. Accepted as intentionally
in-scope: it is stated "as a pointer, not a result," does not feed any graded
claim, and honestly signposts a question larger than the paper. (The operator
also receives this as a dossier placeholder at the final halt.)

---

## Anticipated referee questions — where answered IN THE PAPER

1. **H2 ⊥ H3 independence (audit).** §`sec:comparison` (the comparison is a
   *separate* statement from FJ; logically independent; dropping either breaks
   the chain) + the drop-one discussion; `EBR4-0-HYP`.
2. **Why does the differential SL₂ license a *motivic* lower bound at all?**
   §`sec:comparison`: the comparison dim G_mot ≥ dim G_Gal \eqref{eq:comp},
   theorem-grade classically [André], applied within the Fresán–Jossen framework
   and explicitly contingent on the (G4) realisation — H2 carries both grades
   (CONJECTURED motivic / VERIFIED differential).
3. **Is the locus exclusion now direct?** §`sec:locus`: stratum (R) excluded
   **unconditionally** by SL₂ irreducibility (no margin), stratum (A) by the
   direct q=c√t orbit-degree bound + the well-resourced PSLQ null + M₀ infinite
   order; the residual height-≤10¹⁰ caveat is stated honestly (Remark
   `rem:G5`); `EBR4-1-LOCUS-DIRECT`.
4. **Are the three κ channels mutually independent?** §`sec:channels`: channel A
   (Qₙ large-order asymptotics, 60 d), channel B (frozen composition via the
   169-d C_EBR), channel C (monodromy spectral projector, 129 d) take disjoint
   inputs; their agreement is the cross-check.
5. **Why does NON-rigidity not by itself yield the period conclusion?** The
   discipline line, stated twice (§`sec:discipline1` and §`sec:nonclaim`): a
   Zariski-dense SL₂ bounds the *group*, not the transcendence degree of a single
   entry; non-rigidity is a moduli statement, not an arithmetic one; `CC1-DISCIPLINE`.
6. **The tau-side / Lax-side distinction in the NOT-COVERED verdict.**
   §`sec:coverage`: the boxed tau/Lax line + the per-citation statement that ILP
   and GL compute tau-side objects taking monodromy (the analogue of κ) as
   **input**, never as output; `CC3-2S2-2C-VERDICT`.

## Standing audits (all pass)

- **Grades vs evidence.** No row is PROVEN (the only machine-checked cores are
  EBR-III's four, cited §`sec:lean`); the conditional theorem is **C**; H1 S,
  H2 C-motivic/V-differential, H3 C-external, H4 V; the two nulls and the
  monodromy point V; κ = Γ(4/3)A₀ and the κ-bridge S. Consistent with the
  ledger grades.
- **Locators.** 0 undefined `\ref`/`\eqref`/`\cite` (LaTeX log clean). The
  Fresán–Jossen conjecture is cited as a book-in-preparation **without an arXiv
  number** (the AI-returned id 1705.07173 was verified to be an unrelated physics
  paper and is *not* used). ILP/GL/FIKN/Katz/OKSO/André locators transcribed from
  the located sources.
- **CEILING, both directions.** The boxed ceiling (§`sec:ceilingbox`) states
  transcendence remains conjectural unconditionally; every null/verdict "proves
  nothing about transcendence; a closed form, had one fired, would have argued
  the opposite — elementarity in an extended class."
- **Null-discipline.** §`sec:nulldisc` states the rule (τ ≫ n·log₁₀H and d > τ;
  coefficients ~10^{τ/n} = artifact) and documents the live false positive it
  caught in the locus computation; `EBR4-METH-NULLDISC`.
- **G5 honesty.** Remark `rem:G5` and open-problem item 3 state stratum (A) as
  *hardened, not closed* — the height-≤10¹⁰ assumption is named, the full close
  (explicit q=c√t Stokes trace) is named as a finite elementary computation.
- **Stated-dps honesty.** κ to 129 d (spectral projector), tr M₀ to ~86 d, C_EBR
  to 169 d (frozen, cited not recomputed); the three κ channels' precisions are
  stated individually. mpmath `mpf`, VERIFIED not PROVEN.

## Build state after fixes
`pdflatex` (MiKTeX) two passes: exit 0, 16 pages, 0 undefined references, 0
overfull boxes; PDF text-layer forbidden-string scan 0 genuine hits (the sole
"is a period" is the guard's denial); byte-reproducible SHA-256
`AFA69197CE7B53003C561CA717DD6365AC021E869C9F692CE1C293E07C22382B` across three
in-place builds and one pristine-temp-dir build.
