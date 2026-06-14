# REPORT — op:cc3-1c (re-planned): irregular-rigidity location of L

**Task:** op:cc-transcendence / cc3-1c · **Stage verdict:** COMPLETE, single stage-end HALT.
**Discipline:** SIARC four-class (PROVEN=Lean-only / STRUCTURAL / VERIFIED / CONJECTURED),
AEAL ledger, falsification-first, SHA-256 + dps. Nothing committed / minted; all artifacts untracked.

> **CEILING + discipline line (verbatim).** A large G_Gal does NOT imply C transcendental;
> an exponential-period classification does NOT imply C transcendental; only a named-conjecture
> conditional does. **Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.**
> *Extended (cc3-1c):* relocation to a regular-to-regular connection problem does not make K a
> classical period — provenance is exponential; rigidity, if found, sharpens the period home but
> proves no transcendence. Here rigidity is **absent**, weakening the available machinery further.

The operator (frozen, cc3-1b): `L = z⁴(1−3z) D⁴ + (4z³−25z⁴) D³ + (2z²−47z³) D² − 15 z² D − z²`,
annihilating Φ(z)=Σ Qₙ zⁿ/(n!)², Qₙ=(3n²+n+1)Qₙ₋₁+Qₙ₋₂, Q₀=1, Q₁=5 (radius 1/3).
K = 1.539494848576641… ; C_EBR = K·(4/3)√π/Γ(7/3) (171 agreeing digits, frozen).

---

## 1. M₀ verdict (op:cc3-1c-0) — z=0 CARRIES LOGARITHMS, Jordan [2,2]

The cc3-1c-0 working hypothesis (**z=0 apparent, M₀=I**) and the cc3-1b *HALT-summary /
inherited-state* paraphrase "z=0 block log-free" are **REFUTED** (erratum CC3-2-ERR-1).
*(Honesty note: cc3-1b's report body, REPORT_cc3_1bc.md §1, correctly stated "repeated roots
⇒ partner solutions carry logs; Φ is the log-free holomorphic solution"; and the claim
CC3-1B-LOGFREE scopes log-freeness to Φ@0 and the z=1/3 block — both confirmed below. The
over-generalization to "z=0 (block) log-free" lived only in the summary narration.)*
The exact θ=zD Frobenius
(L = P₀(θ) + z·P₁(θ) + z²·P₂(θ), P₀ = θ²(θ−1)²) on the {0,0,1,1} block gives a 4-dim
solution space with **max log power 1** and **exactly 2 log-free solutions** (Φ among them) ⇒ the z=0
monodromy M₀ has **Jordan type [2,2]** (two size-2 blocks, eigenvalue 1), **dim Z(M₀) = 8**.

- Exact (rational arithmetic, noise-free): `cc3_1c_frobenius_z0_v2.py` → `4482b99af1c1f673a80cdebc768f808b431f37b2958ddf8c7173f1def608b8ee`.
- Numerical corroboration (dps=80): rank(M₀−I)=2, det_rel_err 1.5e-16; SVD ladder sv((M₀−I)²) at noise floor ⇒ (M₀−I)²=0 ⇒ [2,2]. `cc3_1c_monodromy.py` → `1547689b8b7026d8b3199ce164e72e396c7d3935c93238ffcbe08562810d15f4`.
- z=1/3 integer block IS semisimple [1,1,1] + isolated e^{−2πi/3} (rank(M_{1/3}−I)=1, dim Z=10) — cc3-1b correct there.

**z=0 is NOT apparent; M₀ ≠ I.** The 𝔾ₘ-framing contemplated in 1c-0 is dropped.
*(Note: the v1 D-array Frobenius gave a spurious dim=8 by dropping negative-order
intermediate terms; the θ-form is authoritative. The cc3-1b symbolic frobenius_z0 in
`cc3_1b_riemann.py` is corrected by CC3-1C-Z0-JORDAN.)*

## 2. L ↔ L₂ verdict (op:cc3-1c-1) — NOT EQUIVALENT

L is **not** the affine pullback (s=4z) of the EBR Borel operator L₂ up to gauge.
Decisive invariant (exponents mod ℤ at corresponding points, up to one uniform gauge shift):

| | origin | dominant pt | ∞ edge |
|---|--------|-------------|--------|
| L₂ (pulled back) | {0,0,½,½} | residue ⅙ | c⁴=−1/12 → −1/3 |
| L | {0,0,0,0} | residue ⅔ | λ⁴ = −256/3 |

No uniform shift matches the origin; dominant residues differ; ∞-edges differ by 4⁴=256.
L and L₂ are **Hadamard-quotient partners by binom(2n,n)** (gₙ=Qₙ/(2n)! for L₂ vs
φₙ=Qₙ/(n!)² for L). **Consequence:** cc4's SL₄/irreducibility does **not** transfer.
L's irreducibility is argued directly: a single slope-¼ ramification-4 transitive ℤ/4
Galois orbit at ∞ admits no proper stable subset ⇒ irreducible.
Artifact: `cc3_1c_L_vs_L2.py` → `90cdaed3d2055c49ede15c7e6eba84ed3bba9fc7818703883dcdf9c881c88a3d`.

## 3. Rigidity index (op:cc3-1c-2) — **rig(L) = 0, NON-RIGID (moduli dim 2, P = 1)**

Irregular Euler-characteristic formula (Bloch–Esnault / Arinkin / Jakob–Yun),
convention rig = 2 − dim H¹(ℙ¹, j_{!∗}End E), rigid ⟺ rig=2, irreducible ⟹ rig ≤ 2:

```
rig = (2 − #S)·n² + Σ_x dim Z(formal)_x − Σ_x irr_x(End E)
    = (2 − 3)·4²  +  (8 + 10 + 1)        − 3
    = −16         +  19                  − 3   =  0.
```

| point | dim Z(formal) | source |
|-------|---------------|--------|
| z=0 | 8 ([2,2]) | exact Frobenius `4482b99a…` |
| z=1/3 | 10 ([1,1,1]+ω) | monodromy `1547689b…` |
| z=∞ | 1 (irreducible formal type) | cc3-1b Newton polygon `2d98e76…` |
| irr_∞(End) | 3 = (12 nonzero pairwise diffs)·¼ | slope-¼ split |

**Controls (must give rig=2): Airy → 2, ₂F₁ → 2, Bessel → 2 — ALL PASS.** Internal:
L₂ also rig=0. **Derivation artifact (its own deliverable per prompt):**
`cc3_1c_rigidity.py` → **`845ee916336d834a5ee0d7c6cd86eb7c48914e03d8e27733a09affca36ea9d22`**.
**rig(L)=0 < 2 ⇒ L is NON-RIGID.** Headline of the stage.

**Accessory-parameter convention (CC3-2-CONV-1).** The local moduli space of connections with
these fixed formal types has dimension **2P = 2 − rig = 2**, where **P** is the number of
*accessory parameters*. Hence **P = 1**. This reconciles with EBR-II's count for L₂: there
P = d − 1 = 1 at d = 2, and L₂ internally also has rig = 0 ⟹ 2P = 2 ⟹ P = 1 — the **same**
accessory parameter count. Earlier cc3-1c phrasing "accessory count 2" denoted the *moduli
dimension* 2P, not the accessory-parameter number P; both numbers are now stated explicitly to
avoid the off-by-factor-2 ambiguity.

**Corroboration (op:cc3-1c-4):** p-curvature of L is NON-nilpotent at every prime
p∈{5,7,11,13,17,19,23,29} ⇒ not globally nilpotent ⇒ (Chudnovsky–André/Katz) consistent
with irregular ∞. No contradiction. `cc3_1c_pcurvature.py` → `0a3ff3f45fd528b597fbcee19c1658ed05886fbbe44ad03a74e274a2b30663d5`.

## 4. Branch dossier (op:cc3-1c-3) — NON-RIGID ⇒ generic exponential-motives track

Because L is non-rigid, **no identification-based theorem route exists**: the Katz
middle-convolution / hypergeometric-Kloosterman-Airy catalogue (Ann. Math. Stud. 139,
1996; 124, 1990), the Jakob–Yun rigid-irregular classification, and Fresán–Sabbah–Yu
Bessel-moment period theory (Alg. & Number Theory **17**, 2023) all require **rigidity**
(and L is also NOT equivalent to a Kloosterman/L₂ pullback, §2). cc3-2 therefore proceeds
on the **generic exponential-motives track** (Fresán–Jossen, *Exponential Motives*):

- *THEOREM (literature, VERIFIED-by-citation):* exponential motives form a Tannakian
  category with a period pairing; connection coefficients of algebraic-de-Rham / rapid-decay
  pairings are exponential periods.
- *ASSERTED-HERE (CONJECTURED-with-architecture):* that **K** is realized as such a pairing
  for **L** requires constructing the rapid-decay cycle + algebraic de Rham class explicitly
  — the cc3-2 work item; until built + numerically confirmed, membership stays CONJECTURED.
- The moduli dimension **2P = 2** (accessory-parameter count **P = 1**, CC3-2-CONV-1) is the
  precise measure of L's distance from the theorem-rich
  rigid locus. Full dossier: **`cc3_2_entry_dossier.md`**.

## 5. cc3-4a — K-targeted PSLQ reconnaissance: **ALL-NULL**

K extended to 169 digits from frozen 172-digit C via the exact factor (4/3)√π/Γ(7/3)
(cross-checked vs frozen 130-digit direct K to 130 digits, residual 1.05e-130); dps=169,
tol=1e-150; positive controls Li₂(½), √2, ζ(2) all fired.

| tier | basis (motivation) | height | verdict |
|------|--------------------|--------|---------|
| polylog/MZV weight-graded | {1,log2,log3,π²,ζ3,log²3,log³3,π²log3,Li₂(⅓),Li₃(⅓),Catalan} — z=0 logs + cubic args ⅓ + quartic | ≤10⁹, ≤10¹² | **NULL** |
| MIXED Γ(k/3)×polylog | above ∪ {Γ(⅓),Γ(⅔),Γ(⅙)} (values) | ≤10⁹ | **NULL** |
| pure Γ(k/3)-monomial | — | — | **SKIPPED by argument** (≡ C, nulled `9a3f942d…`) |
| Bessel-moment (Broadhurst–Mellit) | — | — | **NOT ADDED** (NON-RIGID, no Kloosterman match) |

**To 169 digits K is not polylog-elementary (weight ≤3, height ≤10¹²) nor a low-height
mixed Γ×polylog combination (height ≤10⁹).** No fire ⇒ no HALT. Consistent with the
non-rigid / exponential-provenance picture. Artifact: `cc3_1c_kpslq.py` →
**`94c3eb916392a87e983bcb9ad82683b1ea05772c904543f5720a13e84558deb2`**.

---

## Four-class evidence table

| claim_id | grade | one-line |
|----------|-------|----------|
| CC3-1C-Z0-JORDAN | VERIFIED (exact) | z=0 log-carrying, Jordan [2,2], dim Z=8 (corrects cc3-1b) |
| CC3-1C-MONODROMY | VERIFIED (numeric) | rank(M₀−I)=2, rank(M_{1/3}−I)=1 corroboration |
| CC3-1C-LvsL2 | STRUCTURAL+VERIFIED | L ≠ pullback of L₂; Hadamard partners; SL₄ no-transfer |
| CC3-1C-RIGIDITY | STRUCTURAL+VERIFIED | rig(L)=0 NON-RIGID, moduli dim 2 / P=1 (controls pass) |
| CC3-1C-PCURV | VERIFIED (arith.) | p-curvature non-nilpotent ⇒ consistent w/ irregular ∞ |
| CC3-1C-BRANCH | VERIFIED (obstruction, type (e)) | no rigid-catalogue route; cc3-2 → exp-motives; K-as-exp-period CONJECTURED-w-arch |
| CC3-4A-KPSLQ | VERIFIED (null) | K not polylog-elementary / mixed-Γ×polylog to 169 d |

**No PROVEN claims this stage** (no Lean). No CONJECTURED claim is asserted beyond the
explicitly-labelled "K-as-exponential-period (CONJECTURED-with-architecture)."

## Artifacts (untracked, uncommitted)
| file | sha256 |
|------|--------|
| cc3_1c_frobenius_z0_v2.py | 4482b99af1c1f673a80cdebc768f808b431f37b2958ddf8c7173f1def608b8ee |
| cc3_1c_monodromy.py | 1547689b8b7026d8b3199ce164e72e396c7d3935c93238ffcbe08562810d15f4 |
| cc3_1c_L_vs_L2.py | 90cdaed3d2055c49ede15c7e6eba84ed3bba9fc7818703883dcdf9c881c88a3d |
| cc3_1c_rigidity.py | 845ee916336d834a5ee0d7c6cd86eb7c48914e03d8e27733a09affca36ea9d22 |
| cc3_1c_pcurvature.py | 0a3ff3f45fd528b597fbcee19c1658ed05886fbbe44ad03a74e274a2b30663d5 |
| cc3_1c_kpslq.py | 94c3eb916392a87e983bcb9ad82683b1ea05772c904543f5720a13e84558deb2 |
| cc3_2_entry_dossier.md | (prose dossier; hashes referenced inline) |

Ledger: MAIN `claims_cc.jsonl` 59 → 66 (7 appended). `repro/` FROZEN (45) untouched.

## Epistemic delta (this stage)
- z=0 reclassified: apparent/log-free (1c-0 hypothesis + summary narration) → **log-carrying [2,2]** (CC3-2-ERR-1).
- L placed in the **non-rigid irregular** landscape: rig=0, moduli dim 2 (P=1), irreducible,
  NOT equivalent to L₂ (so cc4's SL₄ does not transfer; L stands on its own).
- The theorem-rich rigid-catalogue route is **closed**; cc3-2 is routed to the generic
  exponential-motives track with an explicit obstruction inventory and the honest note
  that K-as-exponential-period is CONJECTURED-with-architecture until the pairing is built.
- K shown **not polylog-elementary** to 169 digits (new tiers beyond the C battery).
- CEILING intact: no transcendence claim at any grade.
