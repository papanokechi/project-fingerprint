# EBR-IV — section skeleton (op:ebr4-2)

**Working title.** *The Edge–Borel growth constant is a non-classical
exponential period: an SL₂ monodromy on the Painlevé III(D₈) surface and a
conditional transcendence theorem.*

**Grade architecture (stated up front, not as an apology).** EBR-IV's headline
is a **CONDITIONAL** theorem (κ ∉ ℚ̄ under a four-hypothesis conjunction); it is
the program's **ceiling** and says so. The supporting results are **STRUCTURAL**
(the reduction chain; G_Gal(H₂)=SL₂ and non-Liouvillianity; non-rigidity rig=0;
the S6 exponential-period closure via the κ-bridge) and **VERIFIED** (the
Painlevé III(D₈)=D₈⁽¹⁾ identification under RULE S; the monodromy point
(tr M₀, κ); the three independent κ channels to 129 digits; the two extended
nulls; the off-locus exclusion; the de Rham dimension counts). **PROVEN** items:
**none new** — the only machine-checked substrate in the program is the inherited
EBR-III Lean cores (cited as such, §9); EBR-IV's own finitary identities are
**flagged as Lean-core candidates** (future work, §11). Unconditional
transcendence of C/κ remains **CONJECTURED** (§1, §9, §11).

**CEILING line, final form, cutting BOTH ways (introduction + §9 box).** *The
transcendence of the EBR connection coefficient C — equivalently of the Stokes
constant κ = Γ(4/3)·C/√π — remains CONJECTURED UNCONDITIONALLY; it is NOT
established at any grade here. The conditional theorem is the ceiling. Exhibiting
κ as a constructive exponential period, the off-locus verdict, the NOT-COVERED
coverage result, and the two PSLQ nulls prove NOTHING about transcendence; a
closed form (had one fired) would have argued the OPPOSITE —
elementarity-in-extended-class. The period conjectures see exponential
provenance, not singularity type.*

**Verbatim non-implication line (introduction + §4 + §9 — the discipline line).**
*Non-rigidity (rig = 0, moduli dim 2) does NOT imply κ transcendental; a large
differential Galois group (SL₂) does NOT imply κ transcendental. The differential
side targets the GROUP only. The transcendence conclusion is licensed solely by
the conjunction of the four named hypotheses, of which two are external,
well-defined conjectures.*

---

## §1 Introduction
- EBR-I/II/III recap (roles only, cite DOIs; EBR-I 10.5281/zenodo.20564079,
  EBR-II 10.5281/zenodo.20566465, EBR-III concept DOI [operator fills at mint]).
- The object: κ (= the Stokes/connection constant of the rank-2 core), its
  identity κ = Γ(4/3)·A₀ = Γ(4/3)·C_EBR/√π; the κ/K disambiguation note (one
  sentence: the symbol κ throughout; collision with V_quad's Stokes K is
  cosmetic, the two are different constants on different Sakai surfaces).
- The question; the four-class architecture; forward-ref to §10 table.
- State the CEILING line and the non-implication line here.
- *Forbidden-string audit:* no "we prove transcendence" / "κ is transcendental"
  / "κ is a period" (unconditional) anywhere; the unconditional result is
  NON-membership-pending-conjecture.

## §2 The reduction to a rank-2 core and the Borel-2 operator
- 2.1 From the PCF Qₙ=(3n²+n+1)Qₙ₋₁+Qₙ₋₂ to the OGF y(t)=ΣQₙtⁿ and its
  inhomogeneous ODE 3t³y″+10t²y′+(t²+5t−1)y=−1; the rank-2 core
  **H₂ = 3t³D²+10t²D+(t²+5t−1)**. [CC3-2-CORE-CHAIN]
- 2.2 The Borel-2 transform Φ(z)=ΣQₙzⁿ/(n!)² (radius 1/3) and the **order-4
  operator L**: p₀=−z², p₁=−15z², p₂=−z²(47z−2), p₃=−z³(25z−4), p₄=−z⁴(3z−1);
  θ-form θ²(θ−1)²−z(3θ²+7θ+5)θ²−z²; sing {0,1/3}, **z=∞ irregular slope 1/4**
  ⟹ exponential (rapid-decay) periods, NOT classical Kontsevich–Zagier.
  [CC3-S6-PMAT]
- 2.3 *Mandatory scope statement:* z=1/3 is a Borel-plane (instanton-action)
  singularity of the Gevrey-2 series y; κ is a Stokes-type constant, not a
  two-regular-point connection coefficient (the EBR-II reading, refined). The
  relation κ = Γ(4/3)·A₀ via Flajolet–Sedgewick transfer. [CC3-2S2-KAPPA-RES]

## §3 Local structure and the Painlevé III(D₈) identification
- 3.1 H₂ formal data: singular set {0,∞}, BOTH irregular **slope ½ ramif 2**;
  trace-free form Y″=rY, r=1/(3t³)−5/(9t²)−1/(3t). [CC3-2-CORE-LOCAL]
- 3.2 Non-rigidity: **rig(H₂) = (2−2)·4 + (1+1) − (1+1) = 0** ⟹ NON-RIGID,
  moduli dim 2 (a Painlevé phase space), accessory P=1; controls Airy/₂F₁/Bessel
  = 2 (rigid). [CC3-2S2-RIG]
- 3.3 **RULE S and the D₈⁽¹⁾ label (VERIFIED).** Local type (ram2,ram2) selects
  **PIII(D₈)=Sakai surface D₈⁽¹⁾** uniquely among the leg-2 dictionary
  (D₆⁽¹⁾=(1,1), D₇⁽¹⁾=(2,1), D₈⁽¹⁾=(2,2)); the leg-2 Padé screen reproduces
  z=1/3 to ~34 digits with a converging pole table. **RULE S text reproduced
  here at first use of the D₈ label** (the governance point: surface labels are
  assigned by *selectors*, not pattern-matching). [CC3-2S2-RULES]

## §4 The differential Galois group G_Gal(H₂) = SL₂
- 4.1 Kovacic over the three cases: Case 1 (indicial pole 3/2 half-integer,
  empty Riccati over ℂ(t)); Case 3 (irregular slope ½); Case 2 (imprimitive)
  via reducibility over the unique quadratic cover √t — pullback
  R(x)=4/(3x⁴)−53/(36x²)−4/3, Riccati forced to a/x²+b/x+c (a²=4/3), exhaustive
  search over ℚ(√3) EMPTY. ⟹ **G_Gal(H₂)=SL₂, NON-LIOUVILLIAN.** [CC3-2-KOV]
- 4.2 Corollary: no Liouvillian solutions (van der Put–Singer).
- 4.3 **The discipline line, first statement:** SL₂ is the GROUP; it does not by
  itself bound the transcendence of any connection entry. Forward-ref to §9-H2.

## §5 κ as a constructive exponential period
- 5.1 The rapid-decay pairing on Φ; the **monodromy spectral projector**
  P_μ=(M−I)³/(μ−1)³, μ=e^{−2πi/3} (only Φ continued, 3 loops); the connection
  coefficient **A_Φ = κ to 129 digits**; witnesses (consistency 208, invariance
  204), A_Φ real to ~209. [CC3-S6-PMAT]
- 5.2 The **κ-bridge (S6 closure → STRUCTURAL).** The scalar gauge
  y=x^{−17/6}w leaves Stokes matrices invariant ⟹ s\*(B;x=0)=s\*(H₂;t=0)=A_Φ;
  **κ = Γ(4/3)A₀ = A_Φ = s\***; factor between s\* and κ = identity, between A_Φ
  and A₀ = exactly Γ(4/3); identities 130/200/130 d. *κ lies in the ring of
  exponential periods of the H₂/L connection, constructively.* Full
  exponential-MOTIVE membership stays CONJECTURED (G4). [CC3-S6-CLOSE]
- 5.3 *Integrand chain S1–S6* one-paragraph summary (Gevrey-2 → I₀(2√z) kernel
  = exp period [DLMF 10.9.19] → Hadamard pairing → Borel-2 summability → κ Stokes
  datum → exp-period/Stokes constant). [CC3-2S2-KAPPA-RES]

## §6 The monodromy point and the coverage verdict
- 6.1 **tr(M₀) = −51.0655631399546622698…** (hyperbolic SL₂, |tr|≫2 ⟹
  IRREDUCIBLE, off reducibility locus); the dim-2 D₈ character-variety point
  (tr M₀, κ); accuracy witness = path/radius/node invariance (NOT det=1).
  *Methodology note (two integrator bugs caught):* the 15-dps module-level-mpf
  hazard and the asymmetric-range bug — cited as a named hazard. [CC3-2S2-2A-COORDS,
  CC3-2S2-2A-METH]
- 6.2 The **gauge dictionary** H₂ → companion B=[[0,1],[R,0]] (two rank-1
  irregular points = D₈ shape = symmetric DCHE), composite scalar gauge
  y=x^{−17/6}w. [CC3-2S2-2B-DICT]
- 6.3 **COVERAGE VERDICT (iii) NOT COVERED.** ILT (CMP 363, 2018) computes the
  tau connection-constant = Barnes-G(monodromy); Gavrylenko–Lisovyy (CMP 2018)
  computes τ = Fredholm-det(monodromy); both **tau-side**, κ is a **Lax-side**
  input never output. **NAMED HAZARD (tau-vs-Lax line) stated in every crossing
  paragraph.** H₂ non-rigid ⟹ outside the rigid (hypergeometric/Bessel/Airy)
  catalogue. [CC3-2S2-2C-VERDICT]

## §7 Two extended nulls and the null-discipline rule
- 7.1 The **169-digit elementary null:** C_EBR/A_Φ not an elementary Γ-quotient,
  not a low-height combination of {1,π,log2,log3,γ,Catalan,ζ3,ζ5}, not algebraic
  deg≤8 — positive-control-validated (the EBR-III frozen battery, cited not
  recomputed). [EBR3-B-GAMMA/-CONST/-ALG via the frozen 9a3f942d]
- 7.2 The **Barnes-G/Glaisher log-space null:** log κ, log A₀ not ℤ-linear in
  the Barnes-G/Glaisher-extended basis (m∈{2,3,4,6,12}, H≤10¹², 150 d); positive
  control G(1/2)=2^{1/24}π^{−1/4}e^{1/8}A^{−3/2} fires [24,−1,6,36,−3].
  [CC3-2S2-3-BARNES]
- 7.3 **The null-discipline rule (METH, twice load-bearing).** A PSLQ relation is
  a precision artifact unless tol_dps ≫ (deg+1)·log₁₀H and dps > tol_dps;
  signature is coeffs ~10^(tol_dps/n). Stated as the standing detection-threshold
  rule of the program (ebr3-b + the ebr4-1 spurious-relation catch).
  [EBR4-METH-NULLDISC]
- *Both nulls carry the CEILING annotation: a null proves non-elementarity-up-to-
  precision, never transcendence; a fire would have argued elementarity.*

## §8 Off the classical/algebraic locus (hardened)
- 8.1 **Stratum (R) reducible/Riccati: EXCLUDED UNCONDITIONALLY** — SL₂
  Zariski-dense ⟹ irreducible ⟹ not in any Borel (no margin). [EBR4-1-LOCUS-DIRECT]
- 8.2 **Stratum (A) algebraic q=c√t** (c⁴=1, the ONLY algebraic PIII(D₈)
  solutions, OKSO 2006): the ≤4 solutions over ℚ(i) form a Galois-stable orbit
  ⟹ trace coordinate algebraic deg≤4; tr M₀ is **PSLQ-NULL deg≤4 at H≤10¹⁰**
  (well-resourced tol 1e-72; reinforced deg≤6@1e8, deg≤8@1e6; controls
  √2/2cos2π7/2cos2π5 fire); and M₀ has infinite order (|λ|=0.0196≠1). **G5
  HARDENED but NOT fully closed:** the residual is a *height ≤10¹⁰* bound on a
  bounded-modulus deg≤4 algebraic integer (overwhelmingly safe, not proven); the
  **full close is the explicit q=c√t Stokes/monodromy trace — a named finite
  elementary computation.** State this as an open sub-problem, not as closed.
  [EBR4-1-LOCUS-DIRECT]

## §9 The conditional theorem and the gap list
- 9.1 **Named conjecture (verbatim, located).** Fresán–Jossen period conjecture
  for exponential motives: trdeg_ℚ⟨periods(M)⟩ = dim G_mot(M). (Locator:
  Fresán–Jossen, *Exponential Motives*, book in preparation; Kontsevich–Zagier,
  *Periods*, 2001; André, SMF Panoramas 17, 2004. **The false AI-returned arXiv
  id 1705.07173 is NOT cited** — it is an unrelated physics paper; cited as book,
  no number.)
- 9.2 **The differential→motivic comparison clause (ebr4-0, made explicit).**
  dim G_mot(M) ≥ dim G_Gal = 3 — theorem-grade classically [André IHÉS 83 (1996);
  SMF Panoramas 17 (2004); Ann. Sci. ÉNS 34 (2001)], **here contingent on the G4
  realisation and the irregular/exponential form of the comparison.** This is a
  DIFFERENT statement from the period conjecture (H3); H2 and H3 are logically
  independent (the ebr4-0 verdict (iii)). [EBR4-0-HYP]
- 9.3 **THEOREM (CONDITIONAL) — verbatim re-graded ebr4-0 form (②).** Reproduce
  `theorem_restated_verbatim` from ebr4_0_hypothesis_audit_results.json EXACTLY:
  H1 (STRUCTURAL: κ exp-period = A_Φ, S6 closure) ∧ H2 (CONJECTURED motivic /
  VERIFIED differential: dim G_mot≥3 via SL₂ + comparison) ∧ H3 (CONJECTURED
  external: FJ period conjecture) ∧ H4 (VERIFIED: dim H¹_dR=2, irreducible,
  off-locus, κ the non-vanishing off-diagonal entry) ⟹ **κ ∉ ℚ̄**, hence
  **C = κ√π/Γ(4/3) transcendental.** Drop-one: each hypothesis necessary.
  Dropping H3 leaves only "κ a non-classical exponential period off the algebraic
  locus" — nothing about ℚ̄. [CC3-3-CONDITIONAL, re-graded by EBR4-0-HYP]
- 9.4 **The G3 two-distinct-facts framing (referee-stress-tested).** State as TWO
  facts, never elided: (a) κ = A_Φ is the *identified, non-vanishing* off-diagonal
  connection entry (≠0 to 129 d) — **VERIFIED**; (b) its *non-algebraicity* is
  what the conjectural chain H1–H4 *delivers* — the theorem's **conclusion**, not
  a standalone gap. (a) is not (b); the entry's existence-and-nonvanishing is
  independent of the transcendence question. [EBR4-1-LOCUS-DIRECT (G3 tightened)]
- 9.5 **GAP LIST (first-class, hardened form).** G1 (FJ period conjecture,
  external) · **G2/G4 merged** ("the real conjectural core": realise M as a
  Fresán–Jossen-category exponential motive with the expected Galois group —
  this is where the conjectural mass concentrates after ebr4-0) · G5 (the height
  residual: a verified deg≤4 exclusion up to H≤10¹⁰, full close = the explicit
  c√t Stokes trace). Each row: grade + what would close it.
- 9.6 **CEILING box, final form** (verbatim, cutting both ways).

## §10 Four-class grade table
- Per-result rows (grade + evidence claim_id), mirroring REPORT_cc3_final §5.
  The headline conditional theorem row is C; SL₂/rig-0/S6-closure rows S;
  D₈/monodromy/three-channel/nulls/locus/dim rows V; **no PROVEN row** (note:
  PROVEN substrate = inherited EBR-III cores, cited; EBR-IV Lean cores are §11
  candidates).

## §11 Open problems (with op-codes)
1. *Unconditional transcendence of C/κ* (op:cc-transcendence) — the ceiling; the
   conditional theorem stands on G1 + G2/G4 (two named external conjectures).
2. *The G2/G4 motivic realisation* — construct M=(X,f) as a Fresán–Jossen object
   and verify the irregular realisation comparison; seed = the I₀(2√z) kernel.
3. *The full G5 close* — the explicit q=c√t Stokes/monodromy trace (a finite
   elementary computation removing the height≤10¹⁰ residual).
4. *Lean-core candidates for EBR-IV* (op:cc3-5) — the L-operator/indicial data;
   the H₂→B gauge-chain residual-0 identity; the Kovacic ℚ(√3)-emptiness
   certificate; the dim H¹_dR counts. Template = the four EBR-III cc4 cores.
5. *The cc-5 / Sakai-surface synthesis* (placeholder, flagged for a later paper):
   both program constants — V_quad's Stokes S on D₅⁽¹⁾ and EBR's κ on D₈⁽¹⁾ — are
   Stokes data of rank-2 Painlevé Lax operators; the sharpened question is whether
   the Sakai surface type a PCF's growth constant lands on predicts the arithmetic
   of that constant. **Not EBR-IV's burden — a one-paragraph forward pointer only.**

## Appendix A — Relationship to EBR-II (the home of κ)
- The EBR-II "two-regular-point connection coefficient" reading refined: with the
  {0,∞}-only irregular structure of H₂, z=1/3 is a Borel-plane singularity and κ
  is a Stokes constant whose home is exponential periods (Fresán–Jossen), not
  classical KZ periods. DOI-pinned; load-bearing claims unaffected.

## Appendix B — Reproducibility (pointer to /repro_ebr4; built in op:ebr4-4)
- One-command verifier; the three κ channels independently reproducible; PDF
  byte-reproducible + hashed. The FROZEN EBR-III /repro is untouched; EBR-IV has
  its own package.

---

### Anticipated-referee questions — where each is answered IN THE PAPER
1. **H2⊥H3 independence?** §9.2 (the comparison clause, ebr4-0 verdict (iii);
   drop-one backbone).
2. **Why does differential SL₂ license a motivic lower bound at all?** §9.2 (the
   André normal-subgroup comparison dim G_mot≥dim G_Gal; classical theorem,
   contingent application stated).
3. **Locus exclusion — direct?** §8 (R unconditional; A well-resourced PSLQ +
   infinite order; G5 residual stated honestly, not as closed).
4. **The three κ channels' mutual independence?** §5.1 + a dedicated remark:
   Channel A (Qₙ large-order asymptotics, 60 d), Channel B (frozen composition
   via 169-d C_EBR), Channel C (monodromy spectral projector, 129 d) use disjoint
   inputs and methods.
5. **Why does NON-rigidity not by itself yield the period conclusion?** §4.3 + §9
   (the discipline line: rig=0 and SL₂ are GROUP facts; transcendence needs the
   four hypotheses).
6. **The tau-vs-Lax distinction in NOT-COVERED?** §6.3 (every crossing paragraph
   names the line; κ is Lax-side, the solved formulas are tau-side).

### Deliberately NOT made (forbidden-string guard)
"κ is transcendental"; "we prove transcendence"; "κ is a period" / "C is a
period" (unconditional — exp-period membership is STRUCTURAL-constructive, full
motivic membership CONJECTURED); any claim that SL₂ or non-rigidity *implies*
transcendence; any unconditional ℚ̄ statement. The unconditional result is
NON-membership-pending-conjecture.
