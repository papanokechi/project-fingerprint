# op:xi0-d3-direct — Stage 1: β₃ scale dimension (the one untested piece)

**Scope.** This closes the *only* dimension of the d=3 Borel-radius identity that the
prior work left unexercised: the **β₃ ≠ 1 scale dependence**. It is NOT a re-run of
the already-closed op.

**Already established (not re-done here):**
- **D2-NOTE v2.1 Theorem 4.1** proves ξ₀ = d/β_d^{1/d} for *all* d ≥ 2 (Newton-polygon
  Lemma + Wasow §19 + Birkhoff–Trjitzinsky 1933). d=3 is covered uniformly.
- Prior **siarc-relay-bridge XI0-D3-DIRECT (2026-05-02)** verified d=3 for catalogue
  families 19/14/50, verdict `G2_CLOSED_AT_D3`. **But all three have β₃ = 1**, so they
  only confirm ξ₀ = 3 (the constant), never the β₃^{1/3} scaling.

**What is NEW in this run:**
1. **Fresh χ₃ derivation** — by direct symbolic operator action of
   `L = 1 − z·B(θ+1) − z²` on the WKB ansatz `f = exp(c/u)`, `z = u³`
   (independent of the prior `xi0_d3_runner.py`). Result:
   `χ₃(c) = 1 + (β₃/27)c³`, with **β₂,β₁,β₀ absent from the slope-1/3 edge** —
   so ξ₀ depends on β₃ alone. Real root `c = −3/β₃^{1/3}` ⟹ Borel radius
   `|c| = 3/β₃^{1/3}`.
   *Odd-degree note:* the operator yields the **`+`** sign; the conjecture's stated
   form `1 − (β₃/27)c³` is the opposite ansatz convention `exp(−c/u)` (c→−c) — same
   radius. This is exactly the half-integer rank `q = (d+2)/2 = 5/2` regime (Wasow §19.3).
2. **β₃ ≠ 1 scale-test objects** (constructed, clearly *not* catalogue families):
   `2n³+n²−n+1` (β₃=2) and `7n³+n` (β₃=7, parity with d=4's α₄=7 sample).
3. **Improved numeric Borel ladder** — Neville extrapolation of
   `β₃_est(n) = Qₙ/(Qₙ₋₁·n³)` in `h = 1/n` (the estimator has a clean 1/n asymptotic
   series), lifting the prior ~3.2-digit raw-ratio leg to **38–45 digits**.

## Results (dps_alg=80, dps_num=160)

| object | β₃ | ξ₀ = 3/β₃^{1/3} | algebraic | numeric raw (prior method) | numeric Neville (new) |
|---|---|---|---|---|---|
| `2n³+n²−n+1` | 2 | 2.38110157795… | 80 dig | 3.3 dig | **43 dig** |
| `7n³+n` | 7 | 1.56827387572… | 80 dig | 6.3 dig | **45 dig** |
| `n³−3n²+1` (fam 19) | 1 | 3.0 | 80 dig | 2.5 dig | **38 dig** (reproduces prior G2_CLOSED) |

ξ₀ takes three distinct non-trivial values tracking 3/β₃^{1/3} — the scaling, not just
the constant 3, is confirmed.

## Honest claim
This **closes the previously-untested β₃-scale dimension** of op:xi0-d3-direct: a fresh
symbolic χ₃ derivation plus algebraic (80-digit) and independent numeric (38–45-digit,
Neville-accelerated) confirmation that ξ₀ = 3/β₃^{1/3} at d=3 for β₃ ∈ {1,2,7}. It does
**not** newly "close the op" — Theorem 4.1 and the 2026-05-02 sweep already did that for
the leading-coeff-1 case; this run adds the missing scale dimension and a much stronger
numeric leg.

## Could-not-confirm
- General-d proof itself (that is D2-NOTE Thm 4.1, separate; not re-proven here).
- The constructed β₃≠1 cubics are synthetic scale probes, not enumerated/irreducibility-
  vetted catalogue members (by design — the catalogue is leading-coeff-1 only).

Files: `xi0_d3_scale_test.py`, `xi0_d3_scale_results.json`. Nothing committed.
