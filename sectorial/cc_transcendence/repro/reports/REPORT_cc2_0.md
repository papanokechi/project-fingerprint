# op:cc-2 — Differential Galois Group of L₂ — Gate Report **cc2-0** (ARITHMETIC CONSISTENCY)

**Program:** `op:cc-transcendence` · **Stage:** `op:cc2-0` (audits `op:cc-1`) · **Degree:** d = 2
**Reproducer:** `sectorial/cc_transcendence/cc2_0_arithmetic_gate.py`
**Canonical SHA-256 (hash-free results object):** `dc54bbedd961649e3807406f4a0882022c8856d07460820cb2581a4282e3b5eb`
**Inherits:** `op:cc-1` sha `bfb91bdeef251be00b770f486ec53d2304f4c1064f85d907a82951a49f5f227e`
**Status:** ✅ outcome **(a)** — HALT condition (b) did **not** fire. **HALTED before `cc2-1`** per START directive.

---

## Position

`op:cc2-0` is the falsification gate that *audits* `op:cc-1` before any group machinery
runs. It tests the standing assumption (carried implicitly by the master prompt's
`op:cc-3` "André G-function" clause) that the physical Borel object
`G(s) = Σ Qₙ sⁿ/(2n)!` is a **G-function**. The arithmetic trichotomy is:

> Chudnovsky–André: the minimal operator of a G-function is **globally nilpotent**.
> Katz: globally nilpotent ⇒ **regular singular** (Fuchsian) with rational exponents.
> `op:cc-1`: L₂ is **minimal** (irreducible) and ∞ is **irregular**.
> ⇒ at most **two** of { G-function, irreducible, irregular-∞ } can hold.

Since `op:cc-1` independently established *irreducible* and *irregular-∞*, the third —
"G is a G-function" — must be **false**. Two independent numerical channels confirm it.

---

## Per-leg findings

### LEG A — G-function falsification (VERIFIED)
Exact integer arithmetic, `qₙ = lcm_{n≤N} denom(Qₙ/(2n)!)`, N up to 2000.

| N | log₁₀ qₙ | log₁₀ qₙ / N | log₁₀ qₙ / (N·log₁₀N) | qₙ vs (2N)! (log ratio) |
|---:|---:|---:|---:|---:|
| 250 | 1 134.28 | 4.537 | 1.8921 | 1.0002 |
| 500 | 2 566.88 | 5.134 | 1.9021 | 0.9997 |
| 1000 | 5 735.53 | 5.736 | 1.9118 | 1.0000 |
| 1500 | 9 130.84 | 6.087 | 1.9166 | 1.0000 |
| 2000 | 12 672.46 | 6.336 | 1.9195 | 0.9999 |

* `N log N` model fit **R² = 0.9999983** vs linear `a·N+c` model **R² = 0.998858**.
* The per-coefficient slope `log qₙ/N` **rises monotonically** (4.54 → 6.34) while
  `log qₙ/(N log N)` is **flat** (~1.92): the signature of **superlinear ~N log N** growth.
* `log qₙ / log((2N)!) ≈ 1.0000` throughout ⇒ denominators retain **essentially the full
  factorial (2N)!** (negligible cancellation with the integers Qₙ — consistent with
  `b(k)=3k²+k+1` being always odd, so Qₙ carries almost none of (2n)!'s prime content).

**Verdict:** denominators are **not** geometrically bounded ⇒ **G is NOT a G-function**
(Gevrey/Borel object, `1/(2n)!` factorial denominators). **Outcome (a).**

### LEG B — order-<4 right-factor exclusion (STRUCTURAL)
Independent re-confirmation of `op:cc-1` irreducibility via **slope additivity at ∞**
(Newton polygon of a product = concatenation of the factors' polygons).

* The four determining factors `E_k = exp(4c·ζ₄ᵏ·s^{1/4})` (c⁴ = −1/12) form **one
  transitive orbit** under the full ramification group **ℤ/4** (generator = 4-cycle
  σ = (0 1 2 3)).
* A right factor in C(s)[∂] of order m has a C(s)-rational, hence **σ-stable**, set of m
  determining factors. **Finite enumeration:** the only σ-stable subsets have sizes **{0, 4}**.

| factor order | needs | exists | why |
|:--:|:--|:--:|:--|
| 1 | σ-stable singleton | ✗ | transitive orbit has no fixed point; every Eₖ ramified (s^{1/4}) ⇒ no rational `r` for ∂−r (cc-1 null search) |
| 2 | σ-stable 2-subset | ✗ | ⟨σ⟩ has a single size-4 orbit; no size-2 stable subset |
| 3 | σ-stable 3-subset | ✗ | complement would be a stable singleton (see order 1) |

**Verdict:** no order-1/2/3 right factor ⇒ **L₂ irreducible & minimal** (order 4 = 2d).
Re-derives cc-1's `CC1-IRREDUCIBLE` by the explicit exhaustive route the gate demands.

### LEG C — p-curvature consistency channel (VERIFIED)
ψ_p = ∂ᵖ on the rank-4 module M = 𝔽_p(s)[∂]/(L) (a4-power representation), specialized at
3 generic points per prime.

| p | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| ψ_p nilpotent? | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Non-nilpotent for all 8 primes** ⇒ L₂ is **not globally nilpotent** ⇒ (Chudnovsky–André)
G is **not a G-function**, matching the irregular-∞ prediction (Katz). p = 2, 3 excluded
as degenerate (a₄ = 16s⁴ − 12s⁵ reduces badly mod 2, 3).

---

## Four-class grade table

| Claim | Grade |
|:--|:--|
| `G is NOT a G-function` (superlinear lcm-denominator growth, R²=0.99999983 N logN) | **VERIFIED** |
| `order-1,2,3 right factors excluded` (irreducibility re-confirmed) | **STRUCTURAL** |
| `p-curvature non-nilpotent` for 8 primes ⇒ not globally nilpotent | **VERIFIED** |
| trichotomy resolution ⇒ not-a-G-function (cites Chudnovsky–André, Katz) | **STRUCTURAL** |
| `op:cc-3` André clause amended (G-function route does not apply to G itself) | **STRUCTURAL** |
| transcendence of C | **CONJECTURED** (unchanged) |

Citations are **VERIFIED-by-citation**: Chudnovsky–André (G-functions ⇒ global
nilpotence), Katz (global nilpotence ⇒ Fuchsian/rational exponents), van der Put–Singer
ch. 3 (formal classification / slope additivity at irregular points).

---

## Open problems (with op-codes)

1. **`op:cc-3` (re-stated):** is C nonetheless a **period** (Kontsevich–Zagier) of the
   order-4 operator — a connection/Stokes quantity — even though G is not a G-function?
   The André G-function transcendence route is **no longer available for G itself**;
   any period argument must be built afresh.
2. **`op:cc2-1…cc2-5`:** identify G_Gal(L₂) (the now-cleared next gate).
3. **(residual, from cc-1):** independent recomputation of the Katz rigidity index with
   the irregular point — candidate for the Lean finitary core `op:cc2-6`.

---

## Discipline line (verbatim, in force)

> **Non-rigidity (P = d−1 > 0) does NOT imply C transcendental; a large G_Gal does NOT
> imply C transcendental. `op:cc-2` targets the GROUP only; C's transcendence is
> `op:cc-3`'s burden via periods.**

---

## Epistemic-status delta

`op:cc2-0` moved **one** claim to **VERIFIED** that was previously an unexamined
assumption: *G is **not** a G-function* (superlinear ~N log N denominator growth, R² =
0.9999983; corroborated by non-nilpotent p-curvature at 8 primes). The arithmetic
trichotomy resolves **consistently with `op:cc-1`** — irreducibility and irregular-∞ both
hold, so the not-a-G-function conclusion **audits and corroborates** cc-1 rather than
contradicting it; **HALT outcome (b) did not fire**. The single downstream consequence is
that `op:cc-3`'s "André G-function" clause is **amended/retired for G itself**. Nothing
moved toward transcendence of C; it remains **CONJECTURED**. **Halted before `cc2-1`**
for review per the START directive.
