# M9 — The SIARC Bridge: invariant-triple stratification map Φ

*Program statement (deposit). Forbidden-verb hygiene applied: nothing empirical is
written as "proved/established." Status labels are set by the strongest evidence
confirmable from a repo artifact or a cited deposit; items with no repo artifact are
marked deposit-only / unverified.*

> **TITLE NOTE (morphism decision).** "Functor" is **not** in the headline: on the
> full triple, Φ is an **invariant-triple / stratification map**, not a demonstrated
> functor (decision **B**). The word "functor" survives in exactly one place —
> **Proposition M9.1** — where a morphism class (affine reindexing) and a grounded
> covariance law are exhibited.

**In-repo artifacts of this deposit (this directory `pslq/m9_bridge/`):**
- `m9_1_covariance_check.py` — the M9.1 numeric verification; reuses the in-repo ξ₀
  pipeline `pslq/xi0_d3/xi0_d3_scale_test.py` (imports its `neville_zero`; same
  Q-recurrence + β_d estimator, generalized to degree d).
- `m9_1_covariance_results.json` — machine record
  (sha256 `aa31c7a358079e4e8f16ac137efdfbe7737ac64b54260b03a7d758da79b9bbdd`).
- `m9_1_covariance_raw_output.txt` — raw stdout of the run.
- `claims.jsonl` — AEAL provenance ledger (47 entries) for every load-bearing
  assertion; entries citing `files/M9/…` point to the session-workspace analysis
  chain (01–06) that produced this statement, retained as provenance pointers.

---

## Abstract

The SIARC umbrella posits a cross-degree **bridge** assignment

    Φ : PCF(1, b) ⟼ ( Δ_d(b), ‖Δ‖_Pet(τ_b), ξ₀(b) ),

attaching to a polynomial continued fraction the **invariant triple** of (i) a
modular discriminant Δ_d(b), (ii) its Petersson norm, and (iii) the Borel-singularity
radius ξ₀(b) = d/β_d^{1/d}. M9 asks whether this assignment **organizes** the
cross-degree "bridge" between PCF families and Painlevé labels. The morphism question
is posed and resolved honestly:
- On the **full triple**, the most natural continued-fraction morphisms (limit-fixing
  equivalence transforms) do **not** preserve Φ, and two coordinates (Δ_d, disc) have
  deposit-only transformation behaviour — so Φ is recorded as a **stratification map,
  not a functor** (decision B). The cross-degree arrows are **unposed**, not just
  unproved.
- On the **ξ₀ coordinate alone**, restricted to the **affine-reindexing monoid**
  `n ↦ αn+γ`, Φ_ξ₀ **is** a covariant functor with the grounded law `ξ₀ ↦ α^{-1}ξ₀`
  (**Proposition M9.1**), numerically VERIFIED here for d∈{2,3,4}.
Coordinate (iii) is the most advanced axis (PROVEN at d=2, VERIFIED at d=3 and d=4;
`op:xi0-d3-direct` is **CLOSED**, not open). Coordinates (i)–(ii) are EMPIRICAL (a
single deposited rank correlation). M9 is **partial**, not closed.

## Epistemic partition (the four-way SIARC discipline, per coordinate)

| Object | PROVEN | VERIFIED | EMPIRICAL | CONJECTURED |
|---|---|---|---|---|
| ξ₀ = d/β_d^{1/d} | d=2 (Newton-polygon + Wasow §19) | d=3, d=4 (algebraic dps=80 + numeric) | — | general-d (D2-NOTE Thm 4.1 *claims* a proof; audit pending) |
| Δ_d(b) modular discriminant | — | — | rank-correlated with PCF data (ρ=+0.638, p_Bonf=8.6e−6, 50 cubics) | that Δ_d is the "right" first coordinate |
| ‖Δ‖_Pet(τ_b) | — | — | co-deposited with Δ_d | its role in the stratification |
| disc(b) (Wallis-ODE) | — | — | — | the discriminant-invariant identification |
| **Φ on the full triple** | — | — | — | **stratification map, NOT a functor (decision B); cross-degree morphisms unposed** |
| **Φ_ξ₀ under affine reindexing** | covariance law (β_d-only slope-1/d edge) | **numerically VERIFIED** d∈{2,3,4}, φ∈{(2,0),(2,1),(3,0),(3,1)} | — | general d≥5 (pending D2-NOTE Thm 4.1) |

*(Forbidden-verb note: the Δ_d row is "rank-correlated / detected," never "shown" or
"proved." A p-value is detection, not proof.)*

## Conjecture (stated as a conjecture, not a theorem)

> **Conjecture M9 (Bridge stratification).** The invariant triple
> ( Δ_d, ‖Δ‖_Pet, ξ₀ ) **stratifies** the PCF→Painlevé-label bridge into tiers
> B1 ⊃ B2 ⊃ B3, with ξ₀ the degree-rigid coordinate (PROVEN/VERIFIED), Δ_d the
> modular coordinate (currently EMPIRICAL), and ‖Δ‖_Pet the metric refinement. *No
> functoriality on the full triple is asserted* (decision B): a cross-degree morphism
> class with a grounded coordinate law would first have to be defined.

*(Tiers B1/B2/B3 are named per the umbrella brief; their exact definitions are
deposit-only and unverified here — placeholder pending umbrella §4.4.)*

## The grounded positive results (this deposit)

> **Proposition M9.0 (object-level invariant triple — defensible).** On the deposited
> family sets, every b admits all three coordinates, and the third satisfies
> ξ₀(b) = d/β_d^{1/d}: PROVEN at d=2, VERIFIED at d=3 (this repo, β₃∈{1,2,7}) and d=4.
> This is a **map of objects**; it asserts no morphism action and no functoriality.

> **Proposition M9.1 (ξ₀ affine-reindexing covariance — GROUNDED; numerically
> VERIFIED @ d∈{2,3,4}).** For `b ∈ ℤ[n]`, `deg b = d ∈ {2,3,4}`, leading coeff
> `β_d > 0`, and `φ_{α,γ}(n)=αn+γ` with `α ∈ ℤ_{>0}, γ ∈ ℤ`:
> ```
>     ξ₀(b∘φ_{α,γ}) = d/(β_d α^d)^{1/d} = α^{-1}·ξ₀(b).
> ```
> ξ₀ is shift-invariant (γ free) and dilation-covariant; as a map of action
> categories over the monoid `𝒜=(ℤ_{>0}×ℤ,∘)` (acting on ℝ_{>0} by `α·r=r/α`) it is a
> covariant functor.
>
> **Grounding (exact).** ξ₀ = d/β_d^{1/d} depends on (d, β_d) **only** — the
> slope-1/d Newton-polygon edge involves only the leading coefficient. This is proven
> at d=2 (Newton-polygon + Wasow §19) and grounded in-repo at d=3 by the fresh χ₃
> derivation `pslq/xi0_d3/` (`chi3_only_beta3_on_edge = true`,
> `χ₃ = 1 + (β₃/27)c³`). An affine reindex sends b(n) → b(αn+γ), whose leading
> coefficient is β_d·α^d while γ touches only lower-order terms; hence
> ξ₀ → d/(β_d α^d)^{1/d} = α^{-1}ξ₀, independent of γ. General d≥5 is conjectural
> pending an audit of D2-NOTE Thm 4.1.
>
> **VERIFIED.** The covariance law and γ-invariance were numerically confirmed for the
> exact pairs **d∈{2,3,4}, φ∈{(2,0),(2,1),(3,0),(3,1)}** by reusing the in-repo ξ₀
> pipeline (`m9_1_covariance_check.py`; Q-recurrence + β_d estimator + imported
> `neville_zero`; dps=160 numeric / dps=80 algebraic). Five families — `vquad_d2`
> (b=3n²+n+1, the in-repo V_quad denominator), `fam19_d3` (n³−3n²+1), `synth_b3_2_d3`
> (2n³+n²−n+1), `synth_b4_1_d4` (n⁴+1, constructed), `synth_b4_7_d4` (7n⁴+n,
> constructed). All 20 numeric ratios match 1/α to **37.6–45.7 digits**, algebraic to
> **80–102 digits**, shift-invariance to **42.4–49.8 digits**; `ALL_PASS=True`
> (`m9_1_covariance_results.json`). **NOT** extended to d≥5; the d=4 families are
> constructed scale probes, not catalogue members.

## Open problems

1. **Morphism question — resolved to decision B.** The natural CF morphisms
   (limit-fixing) do not preserve Φ; affine reindexing preserves only ξ₀ and only
   intra-degree (M9.1). A *cross-degree* morphism with a grounded coordinate law
   remains **undefined** → the full-triple functor is unposed.
2. **Extend M9.1 to the full triple** — needs grounded transformation laws for Δ_d
   and disc(b) under reindexing (deposit definitions required; currently unverified).
3. **Audit D2-NOTE Thm 4.1** for the odd-degree half-integer rank q=(d+2)/2 (d=3 ⇒
   q=5/2, Wasow §19.3) to lift ξ₀ (and M9.1) to all d. *(Cheap reading.)*
4. **Lift coordinates 1–2 from EMPIRICAL to derived** — a mechanism behind the
   ρ=+0.638 Δ_d correlation; relate ‖Δ‖_Pet and disc(b) structurally.
5. **`op:xi0-d3-direct` is CLOSED** (D2-NOTE Thm 4.1 + 2026-05-02 sweep + in-repo
   β₃∈{1,2,7} scale test) — not an open item. The M9.1 covariance has now also been
   numerically VERIFIED across d∈{2,3,4} for φ∈{(2,0),(2,1),(3,0),(3,1)}.

## Related-identifier citation graph (concept-DOIs)

```
SIARC umbrella  10.5281/zenodo.19885549  (v2.2 = 20114861)   [Φ def §4.4, M9 row]
  ├─ ξ₀ axis
  │    ├─ Channel Theory   10.5281/zenodo.19941678  (v1.3)    [ξ₀ d=2 proof, d=4 verify]
  │    └─ D2-NOTE          10.5281/zenodo.19996689  (v2.1)    [Thm 4.1 general-d]
  ├─ Δ_d / Petersson axis
  │    └─ PCF-2            10.5281/zenodo.19936297  (v1.4)    [ρ=+0.638 empirical]
  └─ disc(b) axis
       └─ Wallis-ODE       10.5281/zenodo.20173746            [self-adjoint disc invariant]

Related V_quad anchor (this repo): vquad_resurgence (S = 2πK), V_quad PCF basis entry.
```

## Status line
**M9 = PARTIAL.** Morphism question **posed and resolved to decision B**: the
full-triple Φ is an **invariant-triple / stratification map**, not a functor. One
genuine functor survives — **Proposition M9.1** (ξ₀ affine-reindexing covariance,
grounded for d∈{2,3,4}, numerically VERIFIED at φ∈{(2,0),(2,1),(3,0),(3,1)}).
Coordinates Δ_d, ‖Δ‖_Pet remain EMPIRICAL/deposit-only; disc(b)/Δ_d transformation
laws under reindexing remain open/unverified; `op:xi0-d3-direct` is CLOSED.
Deposit scope: Proposition M9.0 (object bundling) + Proposition M9.1 + this honest
partition — **not** any "bridge functor" claim, and **no** d≥5 generalization.
