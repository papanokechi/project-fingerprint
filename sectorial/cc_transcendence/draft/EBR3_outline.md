# EBR-III — section skeleton (op:ebr3-a)

**Working title.** *The EBR operator at d = 2 is not a G-operator and its
differential Galois group is SL(4): arithmetic, irreducibility, and the
non-Liouvillian corollary.*

**Grade architecture (stated up front, not as an apology).** The SL₄ theorem is
**STRUCTURAL** with enumerated, individually graded inputs. The only **PROVEN**
items are the four Lean cores (§9). The integer-relation result (§8.3) and the
connection corpus (§8.1) are **VERIFIED** (high-precision numeric). Transcendence
of the connection coefficient *C* remains **CONJECTURED** (§1, §7, §11).

**Verbatim non-implication line (introduction + §7).** *Non-rigidity (P = d−1 > 0)
does NOT imply C transcendental; a large G_Gal does NOT imply C transcendental.
op:cc-2/4 targets the GROUP only; C's transcendence is op:cc-3's burden via
periods. Connection coefficients are not differential-Galois invariants.*

---

## §1 Introduction
- EBR-I/II recap (roles only, cite DOIs; concept 10.5281/zenodo.20566465 v1.2).
- The question; what is proven / structural / verified / conjectured.
- Forward-reference to the four-class table (§10); state the non-implication line.
- *Forbidden strings audit:* no "we prove transcendence" or cousins anywhere.

## §2 The operator L₂ and its singular structure
- 2.1 The positive-b family d = 2 (b(n)=3n²+n+1, β₂=3, gₙ=Qₙ/(2n)!); L₂ explicit
  (order 4, a₄ = 4s⁴(4−3s)); Riemann scheme; exp@0 = {0,½,1,3/2}, exp@R = {0,1,2,−11/6}.
- 2.2 The point at ∞ is irregular (Poincaré rank 1; Fuchs bound violated).
- 2.3 Accessory-parameter count / index of rigidity (P = d−1; EBR-II erratum-aware).

## §3 Arithmetic nature: L₂ is not a G-operator (NORMALIZATION-SCOPED)
- *Mandatory scope statement:* the result is for the Borel normalization
  gₙ = Qₙ/(2n)!; it does not extend to arbitrary rescalings.
- 3.1 Integrality: Qₙ ∈ ℤ (integer recurrence), so "no geometric denominator
  collapse" is the precise content.
- 3.2 Not-a-G-function via denominator growth.
- 3.3 p-curvature ψ_p non-nilpotent (consistency channel, 8 primes).
- 3.4 Katz / irregular-∞ trichotomy (André–Chudnovsky: minimal op of a G-function
  is globally nilpotent; Katz: globally nilpotent ⇒ regular singular; ∞ irregular).
- 3.5 Consequence: the "André G-function" clause for the period route op:cc-3 is
  retired (the period rebuild must be period-first, not G-function-first).

## §4 Irreducibility and minimality (two independent routes)
- 4.1 Route A — formal-module / Newton-polygon route at ∞ refutes reducibility.
- 4.2 Route B — exhaustive order-1,2,3 right-factor exclusion over ℂ(s).

## §5 Local monodromy and the semisimple correction
- 5.1 M_R is semisimple (audit/correction): pseudo-reflection {1,1,1,e^{iπ/3}},
  rank(M_R−I)=1; M₀ = diag(1,−1,1,−1).
- 5.2 Exact-arithmetic no-log confirmation: integer-exponent resonances
  {0→1,0→2,1→2} carry no logarithm to 169 digits (γ = 11/6 ∉ ℤ).
- 5.3 Erratum: "unipotent / resonance log at R" → semisimple pseudo-reflection;
  scope-patch audit of the G-function normalization caveat.

## §6 The differential Galois group: G_Gal(L₂)⁰ = SL₄ (MAIN THEOREM)
- 6.1 Determinant / twist (w'/w = −a₃/a₄; χ = det^{1/4} algebraic); exponential
  torus at ∞ (units c·{1,i,−1,−i}).
- 6.2 Adjoint test: not self-dual up to twist (R-eigenvalue obstruction).
- 6.3 Exterior square: Λ²L₂ has order 6, no rational solution ⇒ G ⊄ Sp₄.
- 6.4 Symmetric square: no rational symmetric invariant ⇒ G ⊄ SO₄.
- 6.5 Tensor / induced exclusions: Sym³SL₂ and SL₂×SL₂ excluded; imprimitivity
  not decidable from local data alone (deferred — resolved in §6.7).
- 6.6 Aschbacher 8-class elimination table (conditional verdict at this stage).
- 6.7 Primitivity: η = √s is the unique candidate quadratic character (parity);
  the ∞ formal monodromy is the 4-cycle ⇒ index-2 closure; two independent
  searches (pullback s=t², direct η-twist gauge) both NULL ⇒ primitive.
- 6.8 A priori degree bounds B₂ = 3, B₁ = 7 (both ≤ 20) close the search gap.
- 6.9 **Theorem.** G_Gal(L₂)⁰ = SL₄, unconditional and bound-complete
  (STRUCTURAL; every input graded in §10).

## §7 Corollary: no Liouvillian solutions; the non-implication for C
- SL₄ non-solvable ⇒ L₂ has no Liouvillian solutions (VERIFIED-by-citation,
  van der Put–Singer). Then the verbatim non-implication line for C.

## §8 Numerical corpus and the 169-digit null
- 8.1 The connection coefficient via three independent channels (EBR-I prefactor,
  EBR-II continuation, full 4×4 connection matrix), to 169 stable digits;
  amplitude A and prefactor C_EBR = A/Γ(11/6). *Honest interval note:* mpmath
  mpf, not formal Arb intervals — VERIFIED, not PROVEN.
- 8.2 Stokes structure at ∞: determining factors, singular directions, formal
  monodromy 4-cycle, det-consistency Σμₖ ≡ 1/3 (mod 1). *Mandatory scope
  statement:* numerical Stokes multipliers are OUT OF SCOPE (ramified slope ¼,
  infeasible on host) — flagged, not proxied.
- 8.3 The 169-digit integer-relation NULL: C_EBR and A are not elementary
  Γ-quotients (reflection-normalized (1/24)ℤ grid), not low-height combinations
  of {1,π,log2,log3,γ_E,Catalan,ζ3,ζ5}, not algebraic of degree ≤ 8/height ≤ 10⁶;
  positive-control-validated. (Falsification target retired with a documented null.)

## §9 Lean cores and axiom audit
- Four PROVEN cores (lean4 v4.30.0 + Mathlib v4.30.0 rev c5ea0035): degree bound
  arithmetic; pullback exponent integrality; eigenvalue-parity bookkeeping;
  4-cycle-is-odd (index-2 heart). #print axioms: cones ⊆ {propext,
  Classical.choice, Quot.sound}, no sorryAx.

## §10 Four-class grade table
- Per-result rows with grade + evidence type + claim_id (mirrors §5 of REPORT_cc4_close).

## §11 Open problems (with op-codes)
- Transcendence of C → op:cc-3 (periods, post-André); the period interpretation.
- Numerical Stokes multipliers at ramified slope ¼.
- General d (only d = 2 is settled here).
- The rigidity dividing-line conjecture, restated precisely.

## Appendix A — Erratum (formally superseding EBR-I/II narration)
- DOI-cited (concept 10.5281/zenodo.20566465, latest v1.2); the two corrected
  narration lines and why the load-bearing claims are unaffected.

## Appendix B — Reproducibility (pointer to /repro; built in op:ebr3-e)
