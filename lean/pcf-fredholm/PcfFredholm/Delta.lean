/-
# PcfFredholm.Delta — exact-ℚ section value + elementary tail inequality (D2)

Session B1-FDET-D2D3, Option A. Builds the finitary core of the *certified*
pcf-delta Fredholm-determinant enclosure on top of the PROVEN `T_DET`/`T_COMB`
continuant identity (see `Core.lean`).

Two deliverables, both inside current Mathlib with **no** Schatten / trace-class /
Fredholm-determinant substrate (the G3 bonus from the D1 gate):

* **D2.2 (exact-ℚ section).** With the locked pcf-delta rational weights
  `u n = 1/(((n-1)²+1)(n²+1))`, the finite section value `rsec N := cseq u 1 N`
  is an *exact rational* (no rounding) and equals both the tridiagonal determinant
  (`rsec_eq_det`, via `T_DET`) and the weighted independence polynomial
  (`rsec_eq_Rpoly`, via `T_COMB`).

* **D2.3 (elementary tail inequality).** The single elementary inequality
  `∑_{w=N+1}^{M} u w ≤ 1/(3(N-1)³)`, uniform in `M`, proved finitarily by a
  per-term comparison `u w ≤ 1/(w-1)⁴` and a telescoping `1/k⁴ ≤ 1/(3(k-1)³) − 1/(3k³)`.
  This is the explicit-constant heart of the D1 tail estimate `δ − δ_N ≤ 1/(3(N-1)³)`.
  The operator→section analytic step (limit, `log`, `R_∞/r_N` factor) stays at
  PAPER level (D5), exactly as scoped — it is *not* formalized here.
-/
import PcfFredholm.Core

namespace PcfFredholm

open Finset

/-! ## D2.2 — exact-ℚ finite section value -/

/-- Locked pcf-delta rational weights `u n = 1/(((n-1)²+1)(n²+1))` (P0 convention,
    used for `n ≥ 2`; `u 2 = 1/10`, `u 3 = 1/50`, …). Rational by construction. -/
def ud (n : ℕ) : ℚ := 1 / ((((n : ℚ) - 1) ^ 2 + 1) * ((n : ℚ) ^ 2 + 1))

/-- The exact-ℚ finite section value: the continuant at activity `lam = 1` with the
    pcf-delta rational weights. A rational number computed with no rounding. -/
def rsec (N : ℕ) : ℚ := cseq ud 1 N

/-- **Exactness as a determinant.** The section value is exactly the `N × N`
    tridiagonal determinant over `ℚ` (instantiation of the PROVEN `T_DET`). -/
theorem rsec_eq_det (N : ℕ) : rsec N = (Amat ud 1 N).det := (T_DET ud 1 N).symm

/-- **Exactness as an independence polynomial.** The section value is exactly the
    weighted sparse-subset sum over the path `{2,…,N}` (PROVEN `T_COMB`). -/
theorem rsec_eq_Rpoly (N : ℕ) : rsec N = Rpoly ud 1 N := T_COMB ud 1 N

/-- The section value obeys the exact-ℚ continuant recurrence. -/
theorem rsec_rec (n : ℕ) : rsec (n + 2) = rsec (n + 1) + ud (n + 2) * rsec n := by
  simp only [rsec, cseq_add_two, one_mul]

-- Concrete exact rationals (demonstrate "computed exactly, no rounding").
example : rsec 0 = 1 := rfl
example : rsec 1 = 1 := rfl
example : rsec 2 = 11 / 10 := by
  have h := rsec_rec 0
  rw [show (0 : ℕ) + 2 = 2 from rfl, show (0 : ℕ) + 1 = 1 from rfl] at h
  rw [h]; norm_num [rsec, ud]
example : rsec 3 = 28 / 25 := by
  have h3 := rsec_rec 1
  have h2 := rsec_rec 0
  rw [show (1 : ℕ) + 2 = 3 from rfl, show (1 : ℕ) + 1 = 2 from rfl] at h3
  rw [show (0 : ℕ) + 2 = 2 from rfl, show (0 : ℕ) + 1 = 1 from rfl] at h2
  rw [h3, h2]; norm_num [rsec, ud]

/-! ## D2.3 — elementary tail inequality (finitary, no operator substrate) -/

/-- Per-term comparison: `u w ≤ 1/(w-1)⁴` for `w ≥ 2`. Uses only the two factor
    bounds `(w-1)²+1 ≥ (w-1)²` and `w²+1 ≥ (w-1)²`. -/
lemma ud_le (w : ℕ) (hw : 2 ≤ w) : ud w ≤ 1 / ((w : ℚ) - 1) ^ 4 := by
  have hx : (2 : ℚ) ≤ (w : ℚ) := by exact_mod_cast hw
  have hx1 : (0 : ℚ) < (w : ℚ) - 1 := by linarith
  have hden : ((w : ℚ) - 1) ^ 4 ≤ (((w : ℚ) - 1) ^ 2 + 1) * ((w : ℚ) ^ 2 + 1) := by
    nlinarith [mul_nonneg (sq_nonneg ((w : ℚ) - 1)) (show (0 : ℚ) ≤ 2 * (w : ℚ) - 1 by linarith),
      sq_nonneg ((w : ℚ) - 1), sq_nonneg (w : ℚ)]
  have hpos : (0 : ℚ) < ((w : ℚ) - 1) ^ 4 := by positivity
  calc ud w = 1 / ((((w : ℚ) - 1) ^ 2 + 1) * ((w : ℚ) ^ 2 + 1)) := rfl
    _ ≤ 1 / ((w : ℚ) - 1) ^ 4 := one_div_le_one_div_of_le hpos hden

/-- Telescoping comparison: `1/x⁴ ≤ 1/(3(x-1)³) − 1/(3x³)` for `x ≥ 2`.
    Certificate: cross-multiplied difference `= 3x³(6x²-8x+3) = ½x³(6x-4)² + x³ ≥ 0`. -/
lemma tele (x : ℚ) (hx : 2 ≤ x) :
    1 / x ^ 4 ≤ 1 / (3 * (x - 1) ^ 3) - 1 / (3 * x ^ 3) := by
  have hx0 : (0 : ℚ) < x := by linarith
  have hx1 : (0 : ℚ) < x - 1 := by linarith
  rw [div_sub_div _ _ (by positivity : (3 : ℚ) * (x - 1) ^ 3 ≠ 0)
        (by positivity : (3 : ℚ) * x ^ 3 ≠ 0),
      div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith [mul_nonneg (le_of_lt (pow_pos hx0 3)) (sq_nonneg (6 * x - 4)),
    pow_pos hx0 3, pow_pos hx1 3, hx0, hx1]

/-- Strengthened telescoped bound (the induction carrier). -/
lemma tail_bound_strong (N : ℕ) (hN : 2 ≤ N) :
    ∀ M, N ≤ M →
      (∑ w ∈ Finset.Ioc N M, ud w)
        ≤ 1 / (3 * ((N : ℚ) - 1) ^ 3) - 1 / (3 * ((M : ℚ) - 1) ^ 3) := by
  intro M hM
  induction M, hM using Nat.le_induction with
  | base => simp only [Ioc_self, sum_empty, sub_self, le_refl]
  | succ M hM ih =>
      rw [Finset.sum_Ioc_succ_top hM]
      have hM2 : (2 : ℚ) ≤ (M : ℚ) := by exact_mod_cast (le_trans hN hM)
      have hcast : (((M + 1 : ℕ) : ℚ) - 1) = (M : ℚ) := by push_cast; ring
      have h1 : ud (M + 1) ≤ 1 / (((M + 1 : ℕ) : ℚ) - 1) ^ 4 := ud_le (M + 1) (by omega)
      rw [hcast] at h1
      have h2 : 1 / (M : ℚ) ^ 4 ≤ 1 / (3 * ((M : ℚ) - 1) ^ 3) - 1 / (3 * (M : ℚ) ^ 3) :=
        tele (M : ℚ) hM2
      rw [hcast]
      linarith [ih, le_trans h1 h2]

/-- **D2.3 tail inequality.** For `N ≥ 2` and any cutoff `M`, the truncated weight
    tail is bounded by the explicit rational constant `1/(3(N-1)³)`. Finitary and
    elementary; no operator-level / trace-class content. -/
theorem tail_bound (N M : ℕ) (hN : 2 ≤ N) :
    (∑ w ∈ Finset.Ioc N M, ud w) ≤ 1 / (3 * ((N : ℚ) - 1) ^ 3) := by
  have hN1 : (0 : ℚ) < (N : ℚ) - 1 := by
    have : (2 : ℚ) ≤ (N : ℚ) := by exact_mod_cast hN
    linarith
  by_cases h : N ≤ M
  · have hs := tail_bound_strong N hN M h
    have hMpos : (0 : ℚ) ≤ 1 / (3 * ((M : ℚ) - 1) ^ 3) := by
      have hM2 : (2 : ℚ) ≤ (M : ℚ) := by exact_mod_cast (le_trans hN h)
      have : (0 : ℚ) < (M : ℚ) - 1 := by linarith
      positivity
    linarith
  · rw [Finset.Ioc_eq_empty (by omega : ¬ N < M), Finset.sum_empty]
    positivity

end PcfFredholm

/-! ## Phase V — axiom-cone audit (must be ⊆ {propext, Classical.choice, Quot.sound}) -/

#print axioms PcfFredholm.rsec_eq_det
#print axioms PcfFredholm.rsec_eq_Rpoly
#print axioms PcfFredholm.rsec_rec
#print axioms PcfFredholm.ud_le
#print axioms PcfFredholm.tail_bound
