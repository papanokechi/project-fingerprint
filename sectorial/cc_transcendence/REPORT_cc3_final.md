# REPORT — op:cc3-S6 + op:cc3-3: the program summit (period closure + conditional theorem)

**Task:** op:cc-transcendence / cc3-S6 (S6-1, S6-2) + cc3-3 (3-1, 3-2, 3-3) ·
**Stage verdict:** COMPLETE through S6-1 → S6-2 → 3-1 → 3-2 → 3-3, **single stage-end HALT**.
No mid-stage HALT fired: S6-2 produced **no unexplained-factor mismatch** (every bridge factor is
the identity or exactly Γ(4/3), confirmed ≥129 d), and cc3-3-1 returned **OFF the classical locus**
(no locus HIT).
**Discipline:** SIARC four-class (PROVEN=Lean-only / STRUCTURAL / VERIFIED / CONJECTURED), AEAL
ledger, falsification-first, SHA-256 + dps. Nothing committed / minted; all artifacts untracked.

> **CEILING (FINAL FORM, cutting BOTH ways).** The transcendence of the EBR connection coefficient
> C — equivalently of the Stokes constant **κ = Γ(4/3)·C/√π** — remains **CONJECTURED
> UNCONDITIONALLY**; it is **NOT** established at any grade by this program. The cc3-3-2 conditional
> theorem (κ ∉ ℚ̄ under the Fresán–Jossen exponential period conjecture + the SL₂ motivic-Galois
> identification + non-degeneracy) **IS the program's ceiling and says so**. Exhibiting κ as a
> constructive exponential period, an off-locus verdict, or a PSLQ null prove **NOTHING** about
> transcendence; a closed form (had one fired) would have argued the **OPPOSITE** —
> elementarity-in-extended-class. Provenance is exponential (Borel-2 / instanton); the period
> conjectures see provenance, not singularity type.

---

## 1. op:cc3-S6-1 — Rapid-decay period matrix / connection coefficient

**Object.** The rank-2 H₂ solution y(t) is **divergent** (t=0 irregular, slope ½), so the
rapid-decay pairing is realised on the **convergent Borel-2 transform** Φ(z)=Σ Qₙ zⁿ/(n!)² (radius
1/3), which satisfies the **order-4 operator L**:

> p₄Φ⁗ + p₃Φ‴ + p₂Φ″ + p₁Φ′ + p₀Φ = 0,  p₀=−z², p₁=−15z², p₂=−z²(47z−2), p₃=−z³(25z−4), p₄=−z⁴(3z−1).

θ-form θ²(θ−1)² − z(3θ²+7θ+5)θ² − z². Singular set **{0, 1/3}**, **z=∞ irregular slope 1/4**
⟹ L globally irregular ⟹ its connection coefficients are **exponential** (rapid-decay) periods,
not classical Kontsevich–Zagier periods. Indicial roots z=0 → {0,0,1,1}, z=1/3 → {−4/3,0,1,2}
(both match cc3-1b). L annihilates the Φ series to order 14 (residual 0).

**The period = the connection coefficient A_Φ.** A_Φ := the coefficient of the leading-coeff-1
exponent-(−4/3) Frobenius solution Sₐ at z=1/3 in the z=0-analytic solution Φ. Extracted by the
**monodromy spectral projector** P_μ = (M−I)³/(μ−1)³, μ = e^{−2πi/3} (the −4/3 eigenvalue; the
three integer exponents {0,1,2} form a unipotent block killed by (M−I)³):

> A_Φ·s⃗ = (M−I)³ φ⃗ / (μ−1)³,  (M−I)³φ⃗ = φ⃗₃ − 3φ⃗₂ + 3φ⃗₁ − φ⃗₀,

so **only Φ is continued** (3 loops around z=1/3), not a full basis. Result:

> **A_Φ = 1.53949484857664103484378190338406903821939089055314873092629… = κ**

agreeing with frozen κ₁₃₀ to **129 digits**. (The transfer theorem Flajolet–Sedgewick VI.1 gives
A_Φ = Γ(4/3)·A₀ with A₀ = lim Qₙ/((n!)²3ⁿn^{1/3}) = C_EBR/√π = 1.7239979513877744…; the cc3-2s2-1
bridge κ = Γ(4/3)A₀ makes **A_Φ = κ directly**.)

**Witnesses** (deformation invariance + 4-component consistency — NOT any structural/det quantity;
`mp.dps=210` set **before** any module-level mpf, per the 2a dps-ordering control):

| witness | digits |
|---|---|
| marcher vs direct series (zb+0.01) | 181 |
| 4-component consistency of A_Φ | **208** |
| base/radius/step invariance (config2: zb=1/3−1/10, ρ=1/10, 48 steps) | **204** |
| agreement vs frozen κ₁₃₀ (frozen-limited) | 129 |
| A_Φ imag/real (real period) | ~2e-209 |

This is a **third, fully independent channel** for κ (Channel A: Qₙ asymptotics, 60 d; Channel B:
frozen composition; **Channel C: this monodromy projector, 129 d**). The dim-2 D₈ period point
(tr M₀, κ) is now **fully computed**. Artifact `cc3_s6_1_period_matrix.py` → **56adcb10…**.

## 2. op:cc3-S6-2 — The κ-bridge (Stokes-from-periods) — **S6 CLOSED to STRUCTURAL**

Explicit bridge, every factor stated: (B0) the 2b gauge chain H₂ → u″=ru → (t=x²) w″=Rw → companion
**B=[[0,1],[R,0]]** with composite **scalar** gauge y=x^{−17/6}w; (B1) a scalar gauge leaves the
Stokes **matrices** invariant ⟹ s\*(B;x=0)=s\*(H₂;t=0), the single off-diagonal multiplier of the
slope-½ point; (B2) for slope-½ the multiplier is the Borel-plane connection coefficient s\*=A_Φ;
(B3) A_Φ=Γ(4/3)A₀ (transfer); (B4) κ:=Γ(4/3)A₀ ⟹ **κ = Γ(4/3)A₀ = A_Φ = s\*(B;x=0)**. The factor
between s\* and κ is the **identity**; between A_Φ and the large-order amplitude A₀ is exactly
**Γ(4/3)**. Numerically: κ=Γ(4/3)(C_EBR/√π) **130 d**, A_Φ=κ **200 d**, A_Φ/Γ(4/3)=C_EBR/√π **130 d**.

**Verdict.** S6 upgrades **CONJECTURED-with-architecture → STRUCTURAL**: *κ lies in the ring of
exponential periods of the H₂/L connection, constructively (Borel-side connection-coefficient
realisation)*, certified by the explicit integrand chain S1–S5 plus the S6-1 numeric coefficient.
The full exponential-**MOTIVE** membership (abstract Hien rapid-decay de Rham pairing as an object
of the motivic category) remains **CONJECTURED-with-architecture**. **Supersedes CC3-2S2-EXPPER**
(non-destructive). Artifact `cc3_s6_2_bridge.py` → **2cc2f6fb…**.

## 3. op:cc3-3-1 — Classical-locus exclusion — **OFF the locus**

Two strata of the classical/algebraic PIII(D₈) locus: **(R)** reducible monodromy ⟺ Riccati /
special-function solutions; **(A)** algebraic solutions ⟺ finite braid orbit (algebraic trace
coordinates), with the finite-linear-group subcase forcing |tr|≤2. For PIII(D₈) the **only**
algebraic solutions are q=c√t, c⁴=1 (OKSO 2006) — a finite set.

- **(R) EXCLUDED** (STRUCTURAL): G_Gal(H₂)=SL₂ (cc3-2a Kovacic) is Zariski-dense ⟹ irreducible;
  |tr M₀|≫2 hyperbolic.
- **(A) EXCLUDED** (VERIFIED): |tr M₀|−2 = **49.0655** (eigenvalue λ=−0.01959, |λ|≠1 ⟹ M₀ infinite
  order ⟹ monodromy group infinite); and tr M₀ is **not algebraic of degree ≤8** within height 10⁷
  (PSLQ **NULL**; deg≤4 at H≤10⁹ also null). Detector controls fired: √2 → 2x²−x⁴=0,
  2cos(2π/7) → x³+x²−2x−1=0. Finite-braid-orbit points have algebraic coordinates ⟹ (tr M₀,κ) is
  not one.

**Caveat (honest).** The exact monodromy data of the q=c√t solutions was not computed for a direct
point comparison; the exclusion rests on the structural characterisations + irreducibility +
non-low-degree-algebraicity. **No locus HIT ⟹ no HALT.** Artifact `cc3_3_1_locus.py` → **a6b8d588…**.
Locators: FIKN (AMS Math. Surveys Monogr. **128**, 2006); OKSO (J. Math. Sci. Univ. Tokyo **13**
(2006) 145–204); Umemura–Watanabe (Nagoya Math. J. **151** (1998) 1–24); Lisovyy–Tykhyy (J. Geom.
Phys. **85** (2014) 124–163).

## 4. op:cc3-3-2 — The conditional theorem + GAP LIST

**Named conjecture (verbatim form).** *Period conjecture for exponential motives* (Fresán–Jossen;
exponential analogue of Grothendieck's): for an exponential motive M, **trdeg_ℚ⟨periods(M)⟩ =
dim G_mot(M)**; every polynomial relation among the exponential periods is of motivic origin.
*(Locator: Fresán–Jossen, "Exponential Motives", book in preparation; Kontsevich–Zagier "Periods",
2001; André, SMF Panoramas 17, 2004. NOTE: an AI-returned arXiv id **1705.07173 was VERIFIED FALSE**
— it is an unrelated physics paper — so no arXiv number is cited.)*

> **THEOREM (CONDITIONAL).** Assume **(H1, STRUCTURAL)** κ is an exponential period of M [CC3-S6-CLOSE];
> **(H2, CONJECTURED H-aux; differential side VERIFIED)** dim G_mot(M) ≥ 3 via G_Gal(H₂)=SL₂;
> **(H3, CONJECTURED external)** the Fresán–Jossen period conjecture; **(H4, VERIFIED)** the
> period-count / non-degeneracy inputs (dim H¹_dR(H₂)=2, irreducible, off-locus, κ the non-trivial
> off-diagonal entry). **Then** the period algebra of M has transcendence degree dim G_mot(M) ≥ 3,
> and **κ ∉ ℚ̄** (transcendental); hence **C = κ√π/Γ(4/3) is transcendental** too.

**Strongest licensed form (NOT rounded up).** κ ∉ ℚ̄ holds **only** under the full conjunction
H1∧H2∧H3∧H4. The **unconditional residue** is merely: *κ is a non-classical exponential period off
the algebraic PIII(D₈) locus* (STRUCTURAL+VERIFIED) — which says **nothing** about ℚ̄-membership.

**GAP LIST (first-class — the open-problems section of EBR-IV).**

| # | gap | grade | what would close it |
|---|---|---|---|
| G1 | H3 period conjecture is open | CONJECTURED (external) | a proof (or the single instance for M) |
| G2 | H2 G_mot=SL₂ motivic identification conjectural (only differential SL₂ computed) | CONJECTURED (H-aux); anchor VERIFIED | André/Nori realisation comparison for M, or direct G_mot(M) |
| G3 | "κ **specifically** transcendental" uses genericity, not entry-wise non-degeneracy proof | STRUCTURAL (argued) | period-matrix non-vanishing argument for M |
| G4 | M not yet built as a Fresán–Jossen-category object with realisation comparison | STRUCTURAL (constructive shadow) | construct M=(X,f), verify comparison; seed = I₀(2√z) kernel |
| G5 | OKSO / finite-orbit principle used without direct q=c√t monodromy comparison | VERIFIED + caveat | compute c√t monodromy, or cite explicit PIII(D₈) algebraic-locus character variety |

Artifact `cc3_3_2_conditional_theorem.py` → **1b15e7ac…**.

## 5. op:cc3-3-3 — Epistemic close-out

**Program four-class table (cc-1 → cc3-3, 89 claims):**

| class | count | notes |
|---|---|---|
| **PROVEN** (Lean v4.30.0 + Mathlib) | **4** | CC4-LEAN-BOUNDS / PULLBACK / PARITY / A1B |
| **STRUCTURAL** | 34 | incl. CC3-S6-CLOSE, CC3-2-KOV (SL₂), CC3-2S2-RIG (rig 0) |
| **VERIFIED** | 48 | incl. CC3-S6-PMAT, CC3-3-LOCUS, CC3-2S2-RULES (D₈⁽¹⁾) |
| **CONJECTURED** | 3 | CC1-DISCIPLINE; CC3-2S2-EXPPER (**superseded → STRUCTURAL**); CC3-3-CONDITIONAL |

**Discipline line (final form).** Transcendence of C/κ remains **CONJECTURED unconditionally**. The
cc3-3-2 conditional theorem is the program's ceiling and says so; the ceiling cuts both ways (the
NOT-COVERED verdict and the two extended nulls prove nothing; a closed form would have argued
elementarity).

**Readiness for op:ebr4-assemble (result inventory).** (1) Reduction G/C → Borel-2 Φ → rank-2 core
H₂; (2) **D₈⁽¹⁾** under RULE S (6c8dd5ee); (3) **SL₂ / rig-0** (Kovacic + irregular rigidity); (4)
resurgence bridge κ=Γ(4/3)A₀ (8f52843c); (5) **monodromy point (tr M₀, κ) fully computed**
(b1fea3ed + 56adcb10); (6) **NOT-COVERED** coverage verdict (c72bec88); (7) two extended nulls
(169-d C-null 9a3f942d, Barnes null 1887c410); (8) **S6 closure** (56adcb10 / 2cc2f6fb); (9)
**conditional theorem + gap list** (1b15e7ac) + off-locus (a6b8d588). **Lean-core candidates
flagged:** the L-operator / indicial data; the H₂→B gauge-chain residual-0 identity (87be6028); the
Kovacic ℚ(√3) emptiness certificate; the dim H¹_dR counts — template = the four cc4 cores.

Artifact `cc3_3_3_closeout.py` → **7c5d38e9…**.

---

## Claims appended to MAIN ledger (84 → 89)

| claim_id | grade | hash |
|---|---|---|
| CC3-S6-PMAT | STRUCTURAL+VERIFIED | 56adcb10… |
| CC3-S6-CLOSE | STRUCTURAL (supersedes CC3-2S2-EXPPER) | 2cc2f6fb… |
| CC3-3-LOCUS | STRUCTURAL+VERIFIED | a6b8d588… |
| CC3-3-CONDITIONAL | CONJECTURED (conditional theorem) | 1b15e7ac… |
| CC3-3-CLOSEOUT | VERIFIED | 7c5d38e9… |

`repro/` FROZEN (45 EBR-III claims) untouched.

## Epistemic delta

S6 moved **CONJECTURED-with-architecture → STRUCTURAL** (constructive exponential-period realisation
of κ as the order-4 Borel connection coefficient, 129 d, 208/204 witnesses — a third independent
channel). The program acquired its **ceiling artifact** (the conditional theorem) and its **off-locus
exclusion**. **No grade was upgraded to PROVEN** (PROVEN remains the four cc4 Lean cores only).
**Unconditional transcendence of C/κ: unchanged — OPEN.**

## HALT

Stage-end HALT. Delivered: the period-matrix/connection-coefficient hash (**56adcb10…**, κ to 129 d);
the κ-bridge verdict (**S6 → STRUCTURAL**, identities 130/200/130 d); the locus-exclusion margin
(**|tr M₀|−2 = 49.07**, PSLQ deg≤8 null); the conditional theorem statement verbatim (§4); the GAP
LIST (G1–G5). The EBR-IV arc is complete through the conditional ceiling; op:ebr4-assemble is the
next stage. Nothing committed / minted.
