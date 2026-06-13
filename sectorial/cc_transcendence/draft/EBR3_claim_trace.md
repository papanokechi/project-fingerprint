# EBR-III — claim-trace table (op:ebr3-a)

Every load-bearing statement in the planned paper maps to exactly one `claim_id`
in `claims_cc.jsonl`. **Rule:** any statement with no `claim_id` either earns a
new claim (with evidence) or is cut. This table is the audit instrument for the
ebr3-d referee pass; it is complete over the 38 inherited claims + 3 new
`EBR3-B-*` (41 total). Grades: P=PROVEN, S=STRUCTURAL, V=VERIFIED, C=CONJECTURED.

| § | Load-bearing statement | claim_id | grade |
|---|---|---|---|
| 1 | Transcendence of C is the open problem framing the paper | CC1-DISCIPLINE | C |
| 1, 7 | Bridge: SL₄ + non-Liouvillian + the non-implication for C | CC4-2-BRIDGE | S |
| 2.1 | L₂ is the explicit order-4 operator of the d=2 family (a₄=4s⁴(4−3s)) | CC1-OP-L2 | V |
| 2.1 | Riemann scheme: exp@0={0,½,1,3/2}, exp@R={0,1,2,−11/6}, R=4/3 | CC1-RIEMANN | V |
| 2.2 | ∞ is irregular (Poincaré rank 1; Fuchs bound violated) | CC1-INF-IRREGULAR | V |
| 2.3 | Accessory / index-of-rigidity count P=d−1 (EBR-II erratum-aware) | CC1-ACCESSORY | V |
| 3.1 | Qₙ ∈ ℤ (integer recurrence) ⇒ the result is "no collapse" | CC2-0-QINT | V |
| 3.2 | L₂ is not a G-operator for gₙ=Qₙ/(2n)! (NORMALIZATION-SCOPED) | CC2-0-GFUNC | V |
| 3.3 | p-curvature ψ_p non-nilpotent (8 primes; consistency channel) | CC2-0-PCURV | V |
| 3.4 | Katz/irregular-∞ trichotomy ⇒ not the minimal op of a G-function | CC2-0-TRICHOTOMY | S |
| 3.5 | André G-function clause retired for op:cc-3 (period-first rebuild) | CC2-0-CC3-AMEND | S |
| 4.1 | Irreducibility via the formal module at ∞ (route A) | CC1-IRREDUCIBLE | S |
| 4.2 | Irreducibility via exhaustive order-1,2,3 right-factor exclusion (route B) | CC2-0-FACTOR | S |
| 5.1 | M_R semisimple: pseudo-reflection {1,1,1,e^{iπ/3}}, rank(M_R−I)=1 | CC2-2D-JORDAN | V |
| 5.1 | M₀=diag(1,−1,1,−1), M_R explicit in semisimple Frobenius bases | CC4-1-MONODROMY | V |
| 5.2 | No log at the integer-exponent resonances to 169 digits (γ=11/6∉ℤ) | CC4-1-NOLOG | V |
| 5.3, A | Erratum: "unipotent/resonance log at R" → semisimple pseudo-reflection | CC4-ERR-1 | V |
| 5.3 | Scope-patch audit: CC2-0-GFUNC carries the normalization caveat | CC4-ERR-2 | V |
| 6.1 | Determinant/twist: w'/w=−a₃/a₄, χ=det^{1/4} algebraic | CC2-1-TWIST | V |
| 6.1 | Exponential torus at ∞: units c·{1,i,−1,−i} | CC2-1-EXPTORUS | S |
| 6.2 | Not self-dual up to twist (adjoint; R-eigenvalue obstruction) | CC2-2A-SELFDUAL | S |
| 6.3 | Λ²L₂ order 6, no rational solution ⇒ G ⊄ Sp₄ | CC2-2B-SP4 | V |
| 6.4 | Sym²L₂ no rational symmetric invariant ⇒ G ⊄ SO₄ | CC2-2C-SO4 | V |
| 6.5 | Sym³SL₂ and SL₂×SL₂ excluded (tensor/slope arguments) | CC2-2D-TENSOR | S |
| 6.5 | Imprimitivity not decidable from local data alone (deferred → 6.7) | CC2-2D-IMPRIM | S |
| 6.6 | Aschbacher 8-class elimination (conditional verdict at this stage) | CC2-2E-VERDICT | S |
| 6.7 | η=√s is the unique candidate quadratic character (parity) | CC4-A1-ETA-UNIQUE | S |
| 6.7 | ∞ formal monodromy is the 4-cycle ⇒ index-2 closure | CC4-A1B-MONOMIAL-CLOSURE | S |
| 6.7 | Route 1 (pullback s=t²) primitivity search NULL | CC4-0-ROUTE1-PRIMITIVE | S |
| 6.7 | Route 2 (direct η-twist gauge) primitivity search NULL | CC4-0-ROUTE2-PRIMITIVE | S |
| 6.8 | A priori degree bounds B₂=3, B₁=7 (both ≤ 20) close the search gap | CC4-0B-BOUNDS | S |
| 6.9 | **MAIN THEOREM:** G_Gal(L₂)⁰=SL₄, unconditional, bound-complete | CC4-0-SL4-VERDICT | S |
| 8.1 | C to 169 digits via 3 channels; A, C_EBR=A/Γ(11/6) | CC4-1-C-120D | V |
| 8.2 | Stokes layout at ∞ (multipliers OUT OF SCOPE, flagged) | CC4-1-STOKES | V |
| 8.3 | C_EBR, A not elementary Γ-quotients to 169 digits | EBR3-B-GAMMA | V |
| 8.3 | C_EBR, A not low-height combos of {1,π,log2,log3,γ_E,Catalan,ζ3,ζ5} | EBR3-B-CONST | V |
| 8.3 | C_EBR, A not algebraic (degree ≤ 8, height ≤ 10⁶) | EBR3-B-ALG | V |
| 9 | Lean: degree-bound arithmetic (B₂,B₁,≤20) | CC4-LEAN-BOUNDS | P |
| 9 | Lean: pullback exponent integrality {0,1,2,3} | CC4-LEAN-PULLBACK | P |
| 9 | Lean: eigenvalue-parity bookkeeping (negation-closure) | CC4-LEAN-PARITY | P |
| 9 | Lean: 4-cycle is odd ⇒ index-2 heart | CC4-LEAN-A1B | P |
| 11 | Transcendence of C → op:cc-3 (periods, post-André) | CC1-DISCIPLINE, CC2-0-CC3-AMEND | C, S |
| 11 | Numerical Stokes multipliers at slope ¼ remain open | CC4-1-STOKES | V |

**Coverage check.** 38 inherited claims: all placed. 3 new claims
(EBR3-B-GAMMA / -CONST / -ALG): defined in `ebr3_b_pslq_results.json`
(hash `9a3f942d…`), appended to the ledger. No planned load-bearing statement
lacks a `claim_id`.

**Statements deliberately NOT made (forbidden-string guard).** "C is
transcendental"; "we prove transcendence"; "C is a period" (period
interpretation is op:cc-3, not claimed here); any unqualified G-function claim
(always normalization-scoped); any general-d claim (only d=2 settled).
