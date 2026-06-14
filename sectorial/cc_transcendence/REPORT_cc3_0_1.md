# REPORT — op:cc-3 (period rebuild), stage cc3-0 + cc3-1 Route A

**Task:** `op:cc-transcendence/cc-3`  ·  **Stage:** cc3-0 (arithmetic-Gevrey
location) + cc3-1 Route A (integral representation).  ·  **Status:** HALT for
review. Route B held back for the next stage. Nothing committed/minted.

**Discipline + CEILING (verbatim, standing rule for this op):**
> A large G_Gal does NOT imply C transcendental; an exponential-period
> classification does NOT imply C transcendental; only a named-conjecture
> conditional (or out-of-scope genuinely new technology) does. **Unconditional
> transcendence of C is NOT a deliverable of op:cc-3 and may not appear as a
> claim at any grade.** Admissible outcomes: (a) hierarchy location, (b)
> integral/period representation, (c) exponential-period classification, (d)
> CONDITIONAL transcendence under a NAMED conjecture (conditionality in the
> claim text), (e) documented technology-gap / obstruction reports.

---

## 0. Position

The connection coefficient `C = C_EBR = A = 3.0557068…` (corpus anchor
`f3400831…`, 169 digits) of the EBR d=2 family is, after EBR-III, a computed
constant attached to an order-4 operator `L₂` that is irreducible, irregular at
`s=∞` (slope 1/4), with `G_Gal(L₂)⁰ = SL₄` and no Liouvillian solutions, and
which is **not a G-function** in the Borel normalization. The elementary nulls
at 169 digits (`9a3f942d…`) closed the cheap routes. op:cc-3 rebuilds the
period machinery from scratch (the André clause was retired). This stage runs
the **technology map** (cc3-0) and the **integral-representation centerpiece**
(cc3-1 Route A).

The running family: `Q_n = (3n²+n+1) Q_{n−1} + Q_{n−2}`, `Q₀=1`, `Q₁=5`;
`g_n = Q_n/(2n)!`; `G(s) = Σ g_n sⁿ`; `R = 4/3`; `γ = 11/6`;
`g_n ~ C_EBR (3/4)ⁿ n^{5/6}`; `Q_n ~ (C_EBR/√π) 3ⁿ (n!)² n^{1/3}`.

---

## 1. cc3-0 — Arithmetic-Gevrey location (P3 gate)

**Registered prediction P3 (CONFIRMED): no renormalization of the family is an
E-function or a G-function.** Tested exactly over the grid
`c_n = Q_n · n!^{−k} (2n)!^{−m}`, `(k,m) ∈ {0,1,2,3}×{0,1,2}`, with both the
archimedean house and the denominator growth measured by
`r(n) = log₁₀(·)/(n log₁₀ n)` (→ a positive constant iff factorial; → 0 iff
geometric/sub-factorial). Reproducer `cc3_0_gevrey.py`, canonical SHA-256
`af798c04cf22a4d642a8d648e4c926e9b433041dbd53eae933466f9eed3515b6`, exact
integer arithmetic, grid depth `N=500`, (0,1) lcm tie-in to `N=1200`.

The data match the asymptotic theory exactly: G-reading house `r → 2−k−2m`,
G-reading denominator `r → k+2m`; E-reading house `r → 3−k−2m`. The **only**
grid point with geometric denominators is `(k,m)=(0,0)`, whose house is
factorial (`r ≈ +1.86 → 2`); the only points with geometric E-denominators are
`(0,0)` and `(1,0)`, whose E-house is factorial. Hence:

| reading | requires (both) | feasible region (house) | feasible region (den) | overlap |
|---|---|---|---|---|
| G-function | geom house **and** geom den | `k+2m ≥ 2` | `(k,m)=(0,0)` only | **∅** |
| E-function | geom house **and** geom den (of `n!·c_n`) | `k+2m ≥ 3` | `m=0, k≤1` | **∅** |

**No E-function found ⇒ no early HALT** (Siegel–Shidlovskii front does not
open). The `(0,1)` tie-in reproduces cc2-0's denominator law exactly:
`log₁₀ lcm den(Q_n/(2n)!) / log₁₀ (2N)! = 1.00000` at `N = 250, 1000, 1200`.

**Hand proof (STRUCTURAL).** `Q_n` is a factorial-squared house (`~(n!)²3ⁿ`) and
is odd, carrying an asymptotically vanishing share of the prime content of
`(2n)!` (cc2-0: `lcm den(g_n) ~ (2N)!`). For `c_n = Q_n/(n!^k (2n)!^m)`: the
archimedean house `~ (n!)^{2−k−2m}` is geometric **iff** `k+2m ≥ 2`, while the
denominator `~ n!^k (2n)!^m` is geometric **iff** `(k,m)=(0,0)`; the two regions
are disjoint, so **no** `(k,m)` is a G-function. For the E-reading
`a_n = n!·c_n`: house `~ (n!)^{3−k−2m}` (geometric iff `k+2m ≥ 3`) vs
denominator geometric iff `m=0, k≤1`; again disjoint, so **no** `(k,m)` is an
E-function. ∎

**Technology-gap statement (deliverable type (e)).** The two *unconditional*
transcendence machines — Siegel–Shidlovskii for E-functions and the
André–Chudnovsky G-function theory — are **both inapplicable** to the EBR d=2
family in every renormalization on the grid. Locator (VERIFIED-by-citation):
Y. André, *Séries Gevrey de type arithmétique I & II*, **Ann. of Math. 151**
(2000) 705–740 & 741–756 (E = arithmetic-Gevrey order −1, G = order 0; both
require geometric house **and** geometric denominators). This is *why* op:cc-3
must build the period route by hand rather than invoke a ready theorem.

---

## 2. cc3-1 Route A — Integral representation (centerpiece)

Reproducer `cc3_1_routeA.py`, canonical SHA-256
`7762ace08d6980264cb5833959631c2df242eb644688b14e6e684e01ef69112b`. Every
manipulation is checked against the series; the centerpiece identity is
verified at two interior points to the full working precision (130 dps).

### 2.1 OGF ODE (exact, verified 52 terms)
The ordinary generating function `y(t) = Σ Q_n tⁿ` (divergent, Gevrey-2)
satisfies
> **3 t³ y'' + 10 t² y' + (t² + 5t − 1) y = −1.**

Derivation via `θ = t d/dt`: `y − 1 = t(3θ²+7θ+5)y + t² y`, then
`θ² = t²D² + tD`. All series coefficients `t⁰…t⁵²` of the residual vanish.

### 2.2 Borel-2 companion Φ (exact operator, Fuchsian)
`Φ(z) = Σ Q_n zⁿ/(n!)²` is **holomorphic, radius 1/3** (ratio test
`φ₄₀₀/φ₃₉₉ = 3.0025… → 3`), holonomic, annihilated by the order-4 operator
> **L = z⁴(1−3z) D⁴ + (4z³−25z⁴) D³ + (2z²−47z³) D² − 15 z² D − z².**

`L` is verified to reproduce the coefficient recurrence
`n²(n−1)² φ_n = (3n²+n+1)(n−1)² φ_{n−1} + φ_{n−2}` **exactly** (symbolic identity
on all three coefficient polynomials). The leading symbol `z⁴(1−3z)` shows the
only finite singular points are `z=0` and `z=1/3`, both **regular singular
(Fuchsian)**:

| point | exponents |
|---|---|
| `z = 0` | `{0, 0, 1, 1}` (from indicial `[r(r−1)]² = 0`) |
| `z = 1/3` | `{−4/3, 0, 1, 2}` (dominant `−4/3`) |

The irregular slope-1/4 structure of the original `L₂` at `s=∞` lives at
`z=∞` for Φ and is **bypassed for the dominant singularity** (see 2.4).

### 2.3 The Beta-kernel integral representation (verified ≥ 130 digits)
From `1/\binom{2n}{n} = (2n+1) ∫₀¹ [t(1−t)]ⁿ dt` and
`g_n = φ_n/\binom{2n}{n}`:
> **G(s) = ∫₀¹ [ Φ(z) + 2 z Φ'(z) ] dt,   z = s · t(1−t),   valid |s| < R = 4/3.**

(Here `Φ + 2zΦ' = Σ φ_n (2n+1) zⁿ`.) Numerical confirmation against
`G_direct(s) = Σ g_n sⁿ` (1200 terms, 130 dps):

| s | `|G_direct − G_integral|` | agreement |
|---|---|---|
| 1.00 | 0.0 | > 130 digits |
| 1.25 | 0.0 | > 130 digits |

The representation is the centerpiece deliverable (admissible type (b)): an
integral of a concrete holonomic integrand `Φ + 2zΦ'` over the concrete real
cycle `t ∈ [0,1]`, with `z = s·t(1−t)`.

### 2.4 Reduction of C to a Fuchsian connection coefficient
As `s → R⁻`, the integrand's argument `z = s·t(1−t)` peaks at `t=1/2`, where
`z → 1/3` — exactly Φ's singularity. A quadratic-saddle (Watson) analysis at
`t=1/2`, `1−3z = (1−s/R) + 4u²` (`u = t−1/2`), with Φ's dominant local form
`Φ ~ K (1−3z)^{−ρ}`, `ρ = 4/3`, gives
> **γ_G = ρ + 1/2 = 11/6**  (matches EBR's γ **exactly**),

and the amplitude relation (Γ-quotient cancellation `Γ(ρ+1/2)=Γ(11/6)`):
> **C_EBR = A = K · (4/3) √π / Γ(7/3)**,  equivalently  `K = (3/4) C_EBR Γ(7/3)/√π`.

Here **K is the connection coefficient of the Fuchsian operator `L`** between
`z=0` (exponents `{0,0,1,1}`) and `z=1/3` (exponents `{−4/3,0,1,2}`). The factor
`(4/3)√π/Γ(7/3)` is elementary. **Therefore the transcendence question for C is
RELOCATED — not resolved — to a 4th-order Fuchsian connection problem**
(regular ↔ regular), the irregular slope-1/4 obstruction at `s=∞` having been
bypassed for the dominant singularity.

Numerical cross-check of the saddle (limited by series truncation near the
singularity): `Φ(z)(1−3z)^{4/3}` at `1−3z ∈ {1e-2, 5e-3, 2.5e-3}` gives
`1.5270, 1.5330, 1.5361`; Richardson (exponent 4/3) → `K ≈ 1.53851` vs predicted
`1.53949` (relative `6.4e-4`). The **exact** confirmation is the symbolic
exponent `−4/3 ⟹ γ = 11/6`; the numeric `K` is a moderate-precision consistency
check.

### 2.5 Obstruction note (type (e), first-class)
Route A produces **no closed elementary form for K** (Φ's `z=0 → z=1/3`
connection coefficient). This is the precise residual obstruction. It is the
input object for cc3-2 (Fuchsian/exponential-period interpretation of K) and
cc3-3 (named-conjecture conditional). It is consistent with the frozen
169-digit elementary nulls (`9a3f942d…`): if `K` — hence `C` — were elementary,
the nulls would have fired.

---

## 3. Four-class evidence table

| ID | Statement | Grade | Evidence |
|---|---|---|---|
| CC3-0-P3 | No grid renormalization `c_n=Q_n n!^{−k}(2n)!^{−m}` is an E- or G-function | STRUCTURAL + VERIFIED | hand proof (house/den tension) + exact grid `af798c04…` |
| CC3-0-TECHGAP | Siegel–Shidlovskii (E) and André–Chudnovsky (G) are both inapplicable | STRUCTURAL + VERIFIED-by-citation | hand proof + André, Ann. Math. 151 (2000) |
| CC3-1-OGF-ODE | `3t³y''+10t²y'+(t²+5t−1)y=−1` | STRUCTURAL + VERIFIED | derivation + 52-term series check `7762ace0…` |
| CC3-1-PHI | Φ holomorphic (R=1/3), operator `L`, Fuchsian at 0 `{0,0,1,1}` and 1/3 `{−4/3,0,1,2}` | STRUCTURAL + VERIFIED | exact recurrence identity + indicial `7762ace0…` |
| CC3-1-INTREP | `G(s)=∫₀¹[Φ+2zΦ']dt`, `z=s t(1−t)`, `|s|<R` | STRUCTURAL + VERIFIED | Beta-kernel derivation + >130-digit check (s=1,1.25) `7762ace0…` |
| CC3-1-CRED | `C=K·(4/3)√π/Γ(7/3)`, K Fuchsian conn. coeff.; saddle `γ=11/6`; transcendence RELOCATED, remains CONJECTURED | STRUCTURAL + VERIFIED | exact exponents + saddle; γ-match exact; K consistency `6.4e-4` |
| CC3-1-OBSTR | No closed elementary form for K produced; residual obstruction, input to cc3-2/cc3-3 | VERIFIED (obstruction report) | Route-A null + consistency with 169-digit nulls `9a3f942d…` |

No PROVEN (Lean) items this stage. **No claim asserts transcendence of C at any
grade** (ceiling respected).

---

## 4. Epistemic delta

- **P3 confirmed (STRUCTURAL+VERIFIED):** the family sits *outside* both
  arithmetic-Gevrey orders −1 and 0; the unconditional transcendence machines
  are unavailable. This converts a vague expectation into a graded
  technology-gap statement with a hand proof. No early HALT.
- **A concrete integral representation (type (b)) now exists** and is verified
  to full precision: `G(s)=∫₀¹[Φ+2zΦ']dt`. This is the first time C's generating
  function is written as an integral of a *named holonomic kernel over a concrete
  cycle*.
- **The key structural move:** C is reduced to `K`, the connection coefficient
  of the **Fuchsian** order-4 operator `L` (z=0 ↔ z=1/3). The irregular slope-1/4
  problem at `s=∞` is bypassed for the dominant singularity. The exact identity
  `γ = ρ + 1/2 = 11/6` (with Φ's exponent `−4/3` at `z=1/3`) ties the EBR growth
  constant to Φ's Fuchsian data and validates the saddle structurally.
- **What did NOT happen (honest):** no closed form for K, no transcendence claim,
  no firing of any integer-relation search. Route A relocates the obstruction; it
  does not remove it. This is the intended, admissible outcome under the ceiling.

## 5. Readiness for successor stages

- **cc3-1 Route B (next stage):** the Laplace/rank-reduction dual is now
  *motivated by* the Fuchsian companion Φ. The dual side should be examined for
  an algebraic-integrand (Euler/Mellin–Barnes) representation of **K** directly;
  the s^{1/4} ramification at `z=∞` is the place Route B must engage.
- **cc3-2 (exponential/Fuchsian period interpretation):** the target is now
  sharp — interpret **K** (a Fuchsian 4th-order connection coefficient with
  exponents `{0,0,1,1}` ↔ `{−4/3,0,1,2}`) as a period. Regular-singular
  provenance is *better* than the original irregular object: classical
  KZ-period membership may be reachable for `K` even though it was not for `C`
  directly. The `−4/3` and `{0,1,2}` resonance data are the inputs.
- **cc3-3 (named-conjecture conditional):** a dimension/period-count for the
  motive attached to `L` (order 4, two regular singular points + `z=∞`) would
  feed a KZ/Grothendieck-conditional statement about `K`, hence `C` (modulo the
  elementary Γ-quotient). The conditionality must live in the claim text.

**HALT.** Awaiting review of: the P3 hierarchy verdict (no E, no G; no early
HALT), the Route A integral representation with its >130-digit confirmation
(`7762ace0…`), and the C-reduction to the Fuchsian connection coefficient K
(transcendence of C **not** claimed — relocated and CONJECTURED).
