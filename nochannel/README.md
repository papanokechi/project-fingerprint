# `nochannel/` — Surface-type no-channel lemma (committed anchor)

**Foundational, committed-ready anchor** for two downstream papers (the PCF-1
strengthening and the *Detectability Spectrum* paper). It replaces a prior-session
artifact so that downstream work cites a committed, self-contained derivation
rather than ephemeral session state.

- `surface_type_nochannel_verify.py` — self-contained symbolic reproduce (sympy only).
- `surface_type_nochannel_results.json` — machine output (generated).
- `surface_type_nochannel_raw_output.txt` — captured stdout (generated, UTF-8).
- `claims_nochannel.jsonl` — claims `NC-1 … NC-7` (provenance + VERIFIED steps).

```
python surface_type_nochannel_verify.py     # exits 0 iff the theorem verifies
```
CAS: sympy (exact symbolic for the ODE algebra; exact integer form-counts for class
numbers). Verify-script sha256 `47726c1fee747edc55f0b8b74430e2dbc41f4271ca9d679f1d1c8dedc9a2b341`.

---

## Provenance (why this module exists)

The **weaker** committed statement (PCF-1, `p12_pcf1_main.tex`) is empirical: across
the six degree-2 `Δ<0` PCF families the Stokes predicate `S<1` and PSLQ-non-detection
are controlled by *the sign of `Δ` / the CM field, **not** the class number* — evidenced
by the pair `QL06`/`QL26` in the **same** field `Q(√−7)` at `h=1` vs `h=2` (lines
751–757, 971–980). That is a **Stokes/PSLQ-channel** observation, not a surface-type proof.

The **stronger SYMBOLIC surface-type** version (`T` is selected by `β₀`-free local data,
hence cannot factor through `h`) was a **prior-session artifact only** —
`surface_type_no_classnumber_paper.md` (sha256 `9098ee95…`) — and was **never committed**;
its reproduce imported a non-committed `selector_harness`. This module **re-derives the
chain cleanly from scratch**, self-contained, and records it at status **VERIFIED**.

---

## The ODE

Self-adjoint, exact Wallis structure (V_quad anchor, deposited `10.5281/zenodo.20455090`):

> `(a(x) y')' − x² y = 0`,  `a(x) = β₂x² + β₁x + β₀`,  `b := a'`,  `c := −x²`,
> `Δ = disc(a) = β₁² − 4β₂β₀`.

Singular set `{x₋, x₊, ∞}` with `x± = (−β₁ ± √Δ)/(2β₂)`.

## The derivation (each step machine-verified)

1. **Structure.** `b = a' = β₁ + 2β₂x` (β₀-free) and `c = −x²` are polynomial identities,
   valid for all coefficients. `Δ` enters **only** through the positions `x±`.
2. **Finite roots — indices `{0,0}`, β₀-free.** Writing `P = a'/a`, `Q = c/a`: since
   `b = a'`, `P = d/dx log a` has residue `p₀ = 1` at every root; `Q` has only a simple
   pole, so `q₀ = lim (x−x₀)² Q = 0`. The indicial equation `r(r−1) + p₀r + q₀ = r²`
   gives the **repeated exponent `{0,0}`** identically. The resonance is resolved to an
   **apparent** (no-log) singularity by `b = a'` for *all* coefficients — **not** an
   "exponent-difference ∈ ℤ" branch tied to `Δ`.
3. **Infinity — irregular rank 1, `λ = ±1/√β₂`, β₀-free.** `x·(a'/a) → 2` (so
   `a'/a ~ 2/x`, no exponential contribution) and `c/a → −1/β₂` (nonzero constant) ⇒
   irregular singular point of **Poincaré rank 1** with leading exponential rate
   `λ² = 1/β₂`, i.e. `λ = ±1/√β₂` (= `±θ_∞`, `θ_∞ = 2/√β₂`). Depends on `β₂` only.
4. **Origin.** `a(0) = β₀`, so `x = 0` is ordinary iff `β₀ ≠ 0` (algebraic non-degeneracy).
5. **Constancy.** Every surface-type selector is `β₀`-free ⇒
   `T(β₂,β₁,β₀,aₙ) = T(β₂,β₁,aₙ)` is **constant** on `L = {β₂,β₁,aₙ fixed; β₀ free; Δ≠0}`.
6. **Arithmetic variation.** `H(Δ(β₀))` (form class number of the order `O_Δ`; `= h_K`
   when `Δ` fundamental) is **non-constant** on `L`:
   - **QL15 locus** `β₂=3, β₁=−2` (`Δ = 4 − 12β₀`): `β₀=2 ⇒ Δ=−20 = disc Q(√−5)` — the
     QL15 field, `h=2`. Distinct `h ∈ {1,2,3,4,6}` over `β₀=1..12`.
   - **Prior-paper locus** `β₂=3, β₁=1` (`Δ = 1 − 12β₀`, all fundamental):
     `h(β₀=1..10) = 1,3,2,5,3,7,3,8,3,10` — reproduces
     `surface_type_no_classnumber_paper.md §4` exactly.
7. **No-channel theorem.** If `H = f∘T` then `H` is constant on `L` (since `T` is),
   contradicting step 6. So **`T` does not factor through `H`**, and the same argument
   gives `A ≠ g∘T` for **any** non-constant arithmetic invariant `A(Δ)`. ∎

## Epistemic partition (honest)

| Object | Status | Note |
|---|---|---|
| Steps 1–4 (β₀-free local jet) | **VERIFIED** | exact symbolic (sympy) |
| Step 6 (`H` non-constant; tables) | **VERIFIED** | exact form-count, 12 anchors cross-checked |
| No-channel theorem (T ∤ H) | **PROVEN** *given premise* | premise = Sakai/Okamoto: `T` is a function of the local jet |
| Surface **value** `T₀ = D₅⁽¹⁾` | **VERIFIED**, off critical path | deposited `20455090` MEDIUM band; proof uses only *constancy*, never the label |
| General `aₙ` / higher degree | **STRUCTURAL** | not proved here |

The premise (Step "T determined by the local jet") is the standard isomonodromy
framework: Sakai's classification of spaces of initial conditions and Okamoto's theory
assign the surface from pole orders, local/formal exponents, and apparent-singularity
(no-log) conditions — precisely the data shown `β₀`-free above.

## References

- K. Sakai, *Rational surfaces associated with affine root systems and geometry of the
  Painlevé equations*, Comm. Math. Phys. 220 (2001) 165–229 (surface classification;
  PV = `D₅⁽¹⁾`, symmetry `A₃⁽¹⁾`).
- K. Takeuchi, *Arithmetic triangle groups*, J. Math. Soc. Japan 29 (1977) 91–106
  (arithmetic/CM background, as used in PCF-1).
- V_quad anchor, Zenodo `10.5281/zenodo.20455090` (PV / `D₅⁽¹⁾` determination, verdict VQ-N1).

*No deposit, no commit, git untouched — staged to ready-state for the operator.*
