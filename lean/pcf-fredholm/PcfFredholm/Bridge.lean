/-
# PcfFredholm.Bridge — general tridiagonal determinant = three-term continuant

T1 of session A1-EXEC-v1.  Lifts the pcf-specialised `PcfFredholm.T_DET`
(`Core.lean`) to the clean, Mathlib-grade statement, with no pcf-specific
hypotheses, over an arbitrary commutative ring:

  `det (Tri d a b M) = gcont d a b M`

where `Tri d a b M` is the general `M × M` tridiagonal matrix with diagonal
`d`, super-diagonal `a`, sub-diagonal `b`, and `gcont d a b` is the three-term
continuant recurrence
  `g 0 = 1`, `g 1 = d 0`, `g (n+2) = d (n+1) * g (n+1) - a n * b n * g n`.

The pcf core `Amat`/`cseq`/`T_DET` is recovered as the instance
`d ≡ 1`, `a i = lam * w (i+2)`, `b ≡ -1` (see `T_DET_via_bridge`), demonstrating
that the bridge subsumes the existing PROVEN core.

The proof is the back-peel (last row / last column) cofactor expansion, the same
structure that proves the pcf-special `Amat_det_rec`/`T_DET`, generalised so the
diagonal `1` becomes `d`, the super-diagonal `lam·w(·+2)` becomes `a`, and the
sub-diagonal `-1` becomes `b`.
-/
import Mathlib
import PcfFredholm.Core

namespace PcfFredholm

open Matrix Finset

variable {R : Type*} [CommRing R]

/-! ## General tridiagonal matrix and its continuant -/

/-- General `M × M` tridiagonal matrix: diagonal `(i,i) ↦ d i`, super-diagonal
    `(i,i+1) ↦ a i`, sub-diagonal `(i+1,i) ↦ b i`, all other entries `0`.
    Comparisons are taken on the `ℕ`-values of the `Fin` indices, which makes the
    structure transparent to `simp`/`omega`. -/
def Tri (d a b : ℕ → R) (M : ℕ) : Matrix (Fin M) (Fin M) R :=
  fun i j =>
    if (i : ℕ) = (j : ℕ) then d (i : ℕ)
    else if (j : ℕ) = (i : ℕ) + 1 then a (i : ℕ)
    else if (i : ℕ) = (j : ℕ) + 1 then b (j : ℕ)
    else 0

/-- Three-term continuant of a general tridiagonal: `g 0 = 1`, `g 1 = d 0`,
    `g (n+2) = d (n+1) * g (n+1) - a n * b n * g n`. -/
def gcont (d a b : ℕ → R) : ℕ → R
  | 0 => 1
  | 1 => d 0
  | (n + 2) => d (n + 1) * gcont d a b (n + 1) - a n * b n * gcont d a b n

@[simp] lemma gcont_zero (d a b : ℕ → R) : gcont d a b 0 = 1 := rfl
@[simp] lemma gcont_one (d a b : ℕ → R) : gcont d a b 1 = d 0 := rfl

lemma gcont_add_two (d a b : ℕ → R) (n : ℕ) :
    gcont d a b (n + 2) = d (n + 1) * gcont d a b (n + 1) - a n * b n * gcont d a b n := rfl

/-! ## Determinant recurrence (back-peel cofactor expansion) -/

/-- Entry-evaluation helper: the value of `Tri` at indices whose `ℕ`-values are
    `p` and `q` is the `if`-cascade in `p, q`, independent of the ambient size. -/
lemma Tri_val_eq (d a b : ℕ → R) {N : ℕ} (i j : Fin N) (p q : ℕ)
    (hi : (i : ℕ) = p) (hj : (j : ℕ) = q) :
    Tri d a b N i j =
      if p = q then d p
      else if q = p + 1 then a p
      else if p = q + 1 then b q else 0 := by
  subst hi; subst hj; rfl

/-- The top-left `n × n` block of `Tri d a b (n+1)` is `Tri d a b n`. -/
lemma Tri_submatrix_castSucc (d a b : ℕ → R) (n : ℕ) :
    (Tri d a b (n + 1)).submatrix Fin.castSucc Fin.castSucc = Tri d a b n := by
  ext i j
  rfl

/-- The doubly-inner block: deleting the last row and last column of the inner
    cofactor matrix returns `Tri d a b M`. -/
lemma Tri_inner_submatrix (d a b : ℕ → R) (M : ℕ) :
    (((Tri d a b (M + 2)).submatrix Fin.castSucc
        (Fin.succAbove (Fin.castSucc (Fin.last M)))).submatrix Fin.castSucc Fin.castSucc)
      = Tri d a b M := by
  ext i j
  simp only [Matrix.submatrix_apply]
  rw [Fin.succAbove_of_castSucc_lt _ _ (by
        rw [Fin.lt_def]; simp only [Fin.val_castSucc, Fin.val_last]; exact j.isLt)]
  rfl

/-- Determinant of the sub-diagonal cofactor block: removing the last row and the
    second-to-last column of `Tri d a b (M+2)` yields a matrix whose determinant
    is `a M * det (Tri d a b M)` (the surviving entry is the super-diagonal `a M`). -/
lemma Tri_inner_det (d a b : ℕ → R) (M : ℕ) :
    ((Tri d a b (M + 2)).submatrix Fin.castSucc
        (Fin.succAbove (Fin.castSucc (Fin.last M)))).det
      = a M * (Tri d a b M).det := by
  rw [Matrix.det_succ_column _ (Fin.last M), Finset.sum_eq_single (Fin.last M)]
  · -- main term: row index `i = last M`
    have hcol : (Fin.castSucc (Fin.last M)).succAbove (Fin.last M) = Fin.last (M + 1) := by
      rw [Fin.succAbove_of_le_castSucc _ _ (le_refl _), Fin.succ_last]
    have hsign : (-1 : R) ^ ((Fin.last M : ℕ) + (Fin.last M : ℕ)) = 1 := by
      simp only [Fin.val_last]; rw [show M + M = 2 * M by ring, pow_mul]; simp
    rw [Matrix.submatrix_apply, hcol,
        Tri_val_eq d a b _ _ M (M + 1)
          (by rw [Fin.val_castSucc, Fin.val_last]) (Fin.val_last _),
        if_neg (by omega), if_pos (by omega)]
    simp only [Fin.succAbove_last]
    rw [Tri_inner_submatrix, hsign]; ring
  · -- vanishing for `i ≠ last M`
    intro i _ hi
    have hcol : (Fin.castSucc (Fin.last M)).succAbove (Fin.last M) = Fin.last (M + 1) := by
      rw [Fin.succAbove_of_le_castSucc _ _ (le_refl _), Fin.succ_last]
    have hiM : (i : ℕ) < M := by
      have h1 := i.isLt
      have h2 : (i : ℕ) ≠ M := fun h =>
        hi (Fin.val_injective (by rw [Fin.val_last]; exact h))
      omega
    rw [Matrix.submatrix_apply, hcol,
        Tri_val_eq d a b _ _ (i : ℕ) (M + 1) (Fin.val_castSucc _) (Fin.val_last _),
        if_neg (by omega), if_neg (by omega), if_neg (by omega)]
    ring
  · intro h; exact absurd (Finset.mem_univ _) h

/-- The load-bearing determinant recurrence (back-peel cofactor expansion along the
    last row): `det A_{M+2} = d_{M+1}·det A_{M+1} − a_M·b_M·det A_M`. -/
theorem Tri_det_rec (d a b : ℕ → R) (M : ℕ) :
    (Tri d a b (M + 2)).det
      = d (M + 1) * (Tri d a b (M + 1)).det - a M * b M * (Tri d a b M).det := by
  rw [Matrix.det_succ_row (Tri d a b (M + 2)) (Fin.last (M + 1)), Fin.sum_univ_castSucc]
  rw [Finset.sum_eq_single (Fin.last M)
        (fun j _ hj => by
          have hjM : (j : ℕ) < M := by
            have h1 := j.isLt
            have h2 : (j : ℕ) ≠ M := fun h =>
              hj (Fin.val_injective (by rw [Fin.val_last]; exact h))
            omega
          have he : Tri d a b (M + 2) (Fin.last (M + 1)) (Fin.castSucc j) = 0 := by
            rw [Tri_val_eq d a b _ _ (M + 1) (j : ℕ) (Fin.val_last _) (Fin.val_castSucc _),
                if_neg (by omega), if_neg (by omega), if_neg (by omega)]
          rw [he]; ring)
        (fun h => absurd (Finset.mem_univ _) h)]
  have hsL : (-1 : R) ^ ((Fin.last (M + 1) : ℕ) + (Fin.last (M + 1) : ℕ)) = 1 := by
    simp only [Fin.val_last]; rw [show (M + 1) + (M + 1) = 2 * (M + 1) by ring, pow_mul]; simp
  have hsS : (-1 : R) ^ ((Fin.last (M + 1) : ℕ) + (Fin.castSucc (Fin.last M) : ℕ)) = -1 := by
    simp only [Fin.val_last, Fin.val_castSucc]
    rw [show (M + 1) + M = 2 * M + 1 by ring, pow_succ, pow_mul]; simp
  simp only [Fin.succAbove_last]
  rw [Tri_submatrix_castSucc, Tri_inner_det,
      Tri_val_eq d a b _ _ (M + 1) (M + 1) (Fin.val_last _) (Fin.val_last _), if_pos (by omega),
      Tri_val_eq d a b _ _ (M + 1) M (Fin.val_last _)
        (by rw [Fin.val_castSucc, Fin.val_last]),
      if_neg (by omega), if_neg (by omega), if_pos (by omega),
      hsL, hsS]
  ring

/-- **Bridge (general `T_DET`)**: the determinant of any tridiagonal matrix over a
    commutative ring equals its three-term continuant, for every size `M`. -/
theorem det_Tri (d a b : ℕ → R) : ∀ M, (Tri d a b M).det = gcont d a b M
  | 0 => by simp [Matrix.det_fin_zero]
  | 1 => by simp [Tri]
  | (M + 2) => by
      rw [Tri_det_rec, gcont_add_two, det_Tri d a b (M + 1), det_Tri d a b M]

/-! ## Recovery of the pcf core as the instance `d ≡ 1`, `a i = lam·w(i+2)`, `b ≡ -1`.

These corollaries show the general bridge subsumes the existing PROVEN core
(`Amat`/`cseq`/`T_DET` from `Core.lean`). -/

/-- The pcf matrix `Amat w lam` is the `d ≡ 1, a i = lam·w(i+2), b ≡ -1` tridiagonal. -/
lemma Amat_eq_Tri (w : ℕ → R) (lam : R) (M : ℕ) :
    Amat w lam M = Tri (fun _ => 1) (fun i => lam * w (i + 2)) (fun _ => -1) M := by
  ext i j
  rfl

/-- The pcf continuant `cseq w lam` is the `d ≡ 1, a i = lam·w(i+2), b ≡ -1` continuant. -/
lemma cseq_eq_gcont (w : ℕ → R) (lam : R) :
    ∀ M, cseq w lam M = gcont (fun _ => 1) (fun i => lam * w (i + 2)) (fun _ => -1) M
  | 0 => rfl
  | 1 => rfl
  | (M + 2) => by
      rw [cseq_add_two, gcont_add_two, cseq_eq_gcont w lam (M + 1), cseq_eq_gcont w lam M]
      ring

/-- `T_DET` recovered from the general bridge: the pcf determinant identity is the
    `d ≡ 1, a = lam·w(·+2), b ≡ -1` instance of `det_Tri`. -/
theorem T_DET_via_bridge (w : ℕ → R) (lam : R) (M : ℕ) :
    (Amat w lam M).det = cseq w lam M := by
  rw [Amat_eq_Tri, det_Tri, cseq_eq_gcont]

end PcfFredholm

/-! ## Phase V — axiom-cone audit

Each target declaration must rest only on `{propext, Classical.choice, Quot.sound}`
with **no** `sorryAx`. -/

#print axioms PcfFredholm.det_Tri
#print axioms PcfFredholm.Tri_det_rec
#print axioms PcfFredholm.Tri_inner_det
#print axioms PcfFredholm.T_DET_via_bridge
