# The Detectability Spectrum of Imaginary-Quadratic Invariants in Isomonodromy Data

**Tier-2 research scoping memo. No minting. HALT before any deposit/Zenodo/external submission.**
Companion artifacts: `claims_detectability.jsonl` (22 entries, 7-field schema),
`detect_spectrum_verify.py` (reproduce, sha256 `4db46c46…5469f`).

---

## 0. Problem and the established anchor

For the QL15 family — PCF `a_n = n`, `b_n = 3n² − 2n + 2`, with `Δ = −20`,
`K = Q(√−5)`, `h = 2`, `ξ₀ = 2/√3` — the corpus has a **no-channel theorem**:
on the self-adjoint *V_quad* locus

> `(a y')' − x² y = 0`,  `a = β₂x² + β₁x + β₀`,  `b = a'`,  `c = −x²`,  `Δ = β₁² − 4β₂β₀`,

the Sakai **surface type is constant** (`≡ D₅⁽¹⁾`, symmetry `W(A₃⁽¹⁾)`, `δ = −1/2`) and
**does not factor through the class number** `h(Δ)`. This memo generalizes the question:
*which arithmetic invariants of `K` leave a trace in Painlevé/isomonodromy data, and in which channel?*

**Channels (distinct granularities — this distinction does the work):**
- `surface_type` — the discrete Sakai label of the isomonodromy system.
- `monodromy` — the full Riemann–Hilbert datum: linear monodromy representation **plus**
  connection matrices **plus** the positions of the singular points.
- `stokes` — Stokes multipliers/constants at the rank-1 irregular point at `∞`.

---

## 1. The no-channel mechanism, re-derived this session

Both halves are now self-contained (not merely cited); see `detect_spectrum_verify.py` §7 and §5.

**Surface-type half (symbolic, β₀-free selectors).** Because `b = a'`, the indicial
polynomial at each finite root of `a` collapses to `r² = 0` (residue `p₀ = 1`, sub-leading
`q`-term `0`) → exponents `{0,0}`; at `∞`, `c/a → −1/β₂` gives an irregular point of
**Poincaré rank 1** with formal rate `λ = ±1/√β₂`; `x = 0` is ordinary iff `β₀ ≠ 0`. Every
selector is independent of `β₀`. *(Verified symbolically: `indicial = r²`, `λ = ±1/√β₂`.)*

**Arithmetic half (numeric, `h` varies).** `Δ(β₀) = β₁² − 4β₂β₀` sweeps a one-parameter
family of fields, and `h(Δ(β₀))` is wildly non-constant. On the **QL15 locus** `β₂ = 3`
(so `ξ₀ = 2/√3`), `a = 3x² − 2x + β₀` gives `Δ = 4 − 12β₀`:

| β₀ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|----|---|---|---|---|---|---|---|---|---|
| Δ  | −8 | **−20** | −32 | −44 | −56 | −68 | −80 | −92 | −104 |
| h  | 1 | **2** | 2 | 3 | 4 | 4 | 4 | 3 | 6 |

`β₀ = 2` reproduces QL15 (`Δ = −20`, `K = Q(√−5)`, `h = 2`). **Explicit no-channel witness:**
`β₀ = 1` (`K = Q(√−2)`, `h = 1`) and `β₀ = 2` (`K = Q(√−5)`, `h = 2`) sit on the **same**
surface `D₅⁽¹⁾` with `Δ ≠ 0`, yet have different `h`. Hence `h` does not factor through the
surface-type map.

**Crucially, the same argument is `Δ`-blind, not just `h`-blind:** the constant surface type
cannot see the *value* of `Δ` at all (only the non-arithmetic confluence dichotomy `Δ = 0/≠0`).
Everything downstream of `Δ` is therefore invisible to surface type *for free*.

---

## 2. The spectrum (invariant × channel)

| Invariant of `K` | vs `surface_type` | vs `monodromy` | vs `stokes` |
|---|---|---|---|
| Discriminant `Δ` | **PROVEN-invisible** (β₀-free selectors) | **STRUCTURAL** (singularity positions `= roots of a ⇒ √Δ ⇒ K`) | STRUCTURAL (moduli-dependent connection const.) |
| Ramified primes `{p∣Δ}` | **PROVEN-invisible** | STRUCTURAL (factor recovered `Δ`) | UNKNOWN |
| Splitting type `(Δ/p)` | **PROVEN-invisible** | STRUCTURAL (function of `Δ`; all-primes `≡ χ_Δ ≡ K`) | UNKNOWN |
| Unit order `w` (`μ_w`) | **PROVEN-invisible** | STRUCTURAL (`w>2 ⇔ Δ∈{−3,−4}`, CM extra symmetry) | UNKNOWN |
| **Class number `h`** | **PROVEN-invisible** (no-channel thm) | **CONJECTURED** (recoverable via `K`; no intrinsic trace) | UNKNOWN |
| **Class group `Cl(K)`** | **PROVEN-invisible** (*a fortiori* from `h`) | UNKNOWN (needs group structure, not order) | UNKNOWN |
| Regulator `R_K` | **PROVEN-invisible (VACUOUS)** | VACUOUS | VACUOUS |

**Two notions of "detectable" — the central subtlety.** *(R)* recoverable-in-principle: once a
channel determines `K`, every invariant that is a function of `K` (i.e. **all** of them) can be
computed externally. *(C)* intrinsic channel trace: the invariant leaves a structural imprint on
the datum, read off rather than computed. The detectability **spectrum** is sharp only under *(C)*;
under *(R)* the connection channel trivially "detects everything" the moment it recovers `K`.
Per the task constraint we never upgrade *(C)* to PROVEN without an explicit argument.

**Regulator is a category note, not a result.** For every imaginary quadratic `K` the unit group
has rank 0, so `R_K ≡ 1`. Its "invisibility" is vacuous — there is nothing to detect. Content
appears only in the **real-quadratic** generalization (`R_K = log ε₀`); QL15's `K = Q(√−5)` is
imaginary, so this axis is dormant in the present corpus and is the natural next domain.

---

## 3. The functor and its kernel

**Discrete channel — strongest PROVEN statement.** Let
`F_T : {self-adjoint PCF ODEs on the locus, Δ ≠ 0}/isomonodromy → {Sakai surface types}`.
Then `F_T ≡ D₅⁽¹⁾` is **constant**. Consequently the composite to any arithmetic invariant is
constant and the indistinguishability kernel `ker F_T` contains the **entire** arithmetic spectrum
`{Δ, h, Cl, w, ramified primes, splitting}`:

> **The discrete isomonodromy invariant is arithmetically blind** — it detects no invariant of
> `K` beyond the non-arithmetic confluence dichotomy `Δ = 0/≠0`.

**Connection channel — structural statement.** Let `F_M : {ODEs on locus} → {arithmetic of K}`.
`F_M` factors through `K` (singularity positions recover `√Δ`). The *provable* kernel
`ker F_M = ∅` (every invariant is a function of `K`), but the *effective / known-channel* kernel —
invariants with no reading map beyond "recover `K`, then compute" — still contains the **L-value
stratum `{h, Cl}`**. So:

> `ker F_M` is **trivial** in sense *(R)* and **non-trivial, `= {h, Cl}`**, in sense *(C)*.

**One-axis picture.** Geometric stratum (`Δ` and its elementary functions: ramified primes,
splitting, `w`) — invisible to surface type, faithful to `K` in connection moduli. L-value stratum
(`h`, `Cl`, tied to `L(1, χ_Δ)` via `h = (w√|Δ|/2π)·L(1, χ_Δ)`) — invisible to surface type, no
intrinsic channel known anywhere. Regulator — vacuous for imaginary quadratic.

---

## 4. Triage: quick PROVEN vs needs new machinery

**Quick PROVEN (existing machinery):**
1. **Regulator invisibility** — one line (`R_K ≡ 1`); trivially settled.
2. **Whole-`Δ`-tower invisibility to surface type** — the β₀-free-selector argument generalizes
   *verbatim* from `h` to `{Δ, ramified primes, splitting, w, Cl}`. This upgrades the headline from
   "`h` is invisible" to "**all arithmetic of `K` is invisible to surface type**" — the strongest
   immediate paper result, essentially free.
3. **Unit-group reachability** — finite symbolic check whether a locus meets `Δ ∈ {−3,−4}`. Clean
   witnesses both ways: `a = x² + β₀` hits `Δ = −4` at `β₀ = 1`; the QL15 locus
   `a = 3x² − 2x + β₀` hits *neither* for integer `β₀` (since `3β₀ − 1` is never a perfect square).

**Needs new machinery:**
- **A. Intrinsic `h`-trace in monodromy/Stokes** — requires linking monodromy-group arithmetic or
  Stokes constants to `L(1, χ_Δ)`. Deep and open; default **CONJECTURED-invisible**. A targeted
  first probe: sweep the V_quad Stokes constant `S = 2πK` across the β₀-family and test for any
  `h`-correlation (currently a single data point).
- **B. Class-group structure `Cl(K)`** — strictly harder than A (group structure, not just order).

---

## 5. Assumptions surfaced

- **A0 (locus scope).** All `PROVEN-invisible(surface_type)` verdicts are scoped to the self-adjoint
  V_quad/QL15 locus; they do **not** transfer to other strata (e.g. Class B degree-(2,1)), where the
  V_quad calibration is inapplicable.
- **A1 (discriminant normalization).** `Δ` means the field discriminant of `K = Q(√Δ)`; the
  fundamental discriminant is its squarefree-core normalization (QL15's `−20` is already fundamental).
  Connection data recovers the *square-class* of `Δ` (the field), not `disc(a)` literally.
- **A2 (proof split).** Surface-type half re-derived symbolically here; the corpus deposit
  (zenodo 20455090, `surface_type_no_classnumber_paper.md`) carries the original GATE-A/B proof.
- **A3 (channel granularity).** Verdicts are channel-specific; `monodromy` is the full RH datum
  (incl. singularity positions), strictly richer than `surface_type`.
- **A4 (imaginary-only).** The whole analysis is for imaginary quadratic `K`; the regulator/units
  axis acquires content only over real quadratic fields.
- **A5 ((R) vs (C)).** "Detectable" is disambiguated into recoverable-in-principle vs intrinsic
  channel trace; the spectrum is sharp only under (C).

---

## 6. Reproduce

```
python files/detectability/detect_spectrum_verify.py
```
Verified this session: 12/12 `(h, w)` anchors incl. `h(−20)=2`, `w(−3)=6`, `w(−4)=4`; `−20`
fundamental ⇒ `K = Q(√−5)`; splitting of `p ≤ 29` for `Δ = −20`; `h` non-constant on the
`Δ(β₀)` loci (QL15 locus realizes `h ∈ {1,2,3,4,6}`, `β₀=2 ⇒ Δ=−20`); symbolic `indicial = r²`
and `λ = ±1/√β₂`, both `β₀`-free.

*No deposit, Zenodo action, or external submission performed. Git untouched — staged to ready-state
for the operator per the standing commit policy.*
