/-
# PcfFredholm.Core — finitary core of the pcf-delta Fredholm determinant identity

Machine-checked core of the finite determinant identity underlying the Fredholm
representation of the pcf-delta growth constant (session DELTA-FREDHOLM-P0,
numerically VERIFIED to 65 digits by two independent channels).

## Locked G0 convention (see SCOPE.md)

* `cseq w lam : ℕ → R` is the load-bearing recurrence
  `c 0 = 1`, `c 1 = 1`, `c (n+2) = c (n+1) + lam * w (n+2) * c n`.
* `Amat w lam M : Matrix (Fin M) (Fin M) R` is the verbatim tridiagonal matrix:
  diagonal `1`, super-diagonal `(i,i+1) ↦ lam * w (i+2)`, sub-diagonal `(i+1,i) ↦ -1`.

G0 FALSIFICATION FINDING: the brief's G0 text stated `c 1 = 1 + lam * w 1`, but the
*verbatim* matrix gives `det (Amat 1) = 1` (a `1×1` matrix `[1]`).  Hence the
load-bearing base case is `c 1 = 1`, and `cseq w lam M` is the weighted
independence polynomial of the path on the index set `{2,…,M}` (vertex `i` carries
weight `w i`) — exactly the P0 object "path on indices {2..N}".  This file proves
the corrected, self-consistent identity `det (Amat w lam M) = cseq w lam M`.

Everything is stated over a general `CommRing R`.
-/
import Mathlib

namespace PcfFredholm

open Matrix Finset

variable {R : Type*} [CommRing R]

/-! ## Definitions -/

/-- The load-bearing scaled sequence ("continuant"), defined by the recurrence
    `c 0 = 1`, `c 1 = 1`, `c (n+2) = c (n+1) + lam * w (n+2) * c n`. -/
def cseq (w : ℕ → R) (lam : R) : ℕ → R
  | 0 => 1
  | 1 => 1
  | (n + 2) => cseq w lam (n + 1) + lam * w (n + 2) * cseq w lam n

@[simp] lemma cseq_zero (w : ℕ → R) (lam : R) : cseq w lam 0 = 1 := rfl
@[simp] lemma cseq_one (w : ℕ → R) (lam : R) : cseq w lam 1 = 1 := rfl

lemma cseq_add_two (w : ℕ → R) (lam : R) (n : ℕ) :
    cseq w lam (n + 2) = cseq w lam (n + 1) + lam * w (n + 2) * cseq w lam n := rfl

/-- The verbatim tridiagonal matrix `A_M` of the brief: size `M × M`, diagonal `1`,
    super-diagonal `(i, i+1) ↦ lam * w (i+2)`, sub-diagonal `(i+1, i) ↦ -1`,
    all other entries `0`.  Comparisons are taken on the `ℕ`-values of the `Fin`
    indices, which makes the structure transparent to `simp`/`omega`. -/
def Amat (w : ℕ → R) (lam : R) (M : ℕ) : Matrix (Fin M) (Fin M) R :=
  fun i j =>
    if (i : ℕ) = (j : ℕ) then 1
    else if (j : ℕ) = (i : ℕ) + 1 then lam * w ((i : ℕ) + 2)
    else if (i : ℕ) = (j : ℕ) + 1 then -1
    else 0

/-! ## Phase G0 — convention gate (small `M`, symbolic `w`, `lam`)

These lock the convention by computing `det (Amat w lam M)` for `M = 1, 2, 3`
directly from `Matrix.det_fin_one/two/three`.  They show the determinants are
`1`, `1 + lam·w 2`, `1 + lam·w 2 + lam·w 3` — i.e. `cseq w lam M` with `c 1 = 1`,
**not** the brief's `1 + lam·w 1`. -/

section G0
variable (w : ℕ → R) (lam : R)

theorem g0_det_one : (Amat w lam 1).det = 1 := by
  simp [Amat]

theorem g0_det_two : (Amat w lam 2).det = 1 + lam * w 2 := by
  simp [Amat, Matrix.det_fin_two]

theorem g0_det_three : (Amat w lam 3).det = 1 + lam * w 2 + lam * w 3 := by
  simp [Amat, Matrix.det_fin_three]; ring

theorem g0_matches_cseq_one : (Amat w lam 1).det = cseq w lam 1 := by
  rw [g0_det_one, cseq_one]

theorem g0_matches_cseq_two : (Amat w lam 2).det = cseq w lam 2 := by
  rw [g0_det_two, cseq_add_two, cseq_one, cseq_zero]; ring

theorem g0_matches_cseq_three : (Amat w lam 3).det = cseq w lam 3 := by
  rw [g0_det_three, cseq_add_two, cseq_add_two, cseq_one, cseq_zero]; ring

end G0

/-- G0 small-`M` counterexample to the brief's stated base value: with `w ≡ 1`,
    `lam = 1` over `ℤ`, `det (Amat 1) = 1` while `1 + lam · w 1 = 2`. -/
theorem g0_brief_base_is_wrong :
    ∃ (w : ℕ → ℤ) (lam : ℤ), (Amat w lam 1).det ≠ 1 + lam * w 1 := by
  refine ⟨fun _ => 1, 1, ?_⟩
  norm_num [Amat, Matrix.det_fin_one]

/-! ## Phase P1 — `T_DET : det (Amat w lam M) = cseq w lam M` -/

/-- Entry-evaluation helper: the value of `Amat` at indices whose `ℕ`-values are
    `p` and `q` is the `if`-cascade in `p, q`.  Lets every concrete entry be settled
    by `if_pos`/`if_neg` + `omega`, independent of the ambient matrix size. -/
lemma Amat_val_eq (w : ℕ → R) (lam : R) {N : ℕ} (i j : Fin N) (p q : ℕ)
    (hi : (i : ℕ) = p) (hj : (j : ℕ) = q) :
    Amat w lam N i j =
      if p = q then 1
      else if q = p + 1 then lam * w (p + 2)
      else if p = q + 1 then -1 else 0 := by
  subst hi; subst hj; rfl

/-- The top-left `n × n` block of `Amat w lam (n+1)` is `Amat w lam n`. -/
lemma Amat_submatrix_castSucc (w : ℕ → R) (lam : R) (n : ℕ) :
    (Amat w lam (n + 1)).submatrix Fin.castSucc Fin.castSucc = Amat w lam n := by
  ext i j
  rfl

/-- The doubly-inner block: deleting the last row and last column of the inner
    cofactor matrix returns `Amat w lam M`. -/
lemma Amat_inner_submatrix (w : ℕ → R) (lam : R) (M : ℕ) :
    (((Amat w lam (M + 2)).submatrix Fin.castSucc
        (Fin.succAbove (Fin.castSucc (Fin.last M)))).submatrix Fin.castSucc Fin.castSucc)
      = Amat w lam M := by
  ext i j
  simp only [Matrix.submatrix_apply]
  rw [Fin.succAbove_of_castSucc_lt _ _ (by
        rw [Fin.lt_def]; simp only [Fin.val_castSucc, Fin.val_last]; exact j.isLt)]
  rfl

/-- Determinant of the sub-diagonal cofactor block: removing the last row and the
    second-to-last column of `Amat w lam (M+2)` yields a matrix whose determinant
    is `lam * w (M+2) * det (Amat w lam M)`. -/
lemma Amat_inner_det (w : ℕ → R) (lam : R) (M : ℕ) :
    ((Amat w lam (M + 2)).submatrix Fin.castSucc
        (Fin.succAbove (Fin.castSucc (Fin.last M)))).det
      = lam * w (M + 2) * (Amat w lam M).det := by
  rw [Matrix.det_succ_column _ (Fin.last M), Finset.sum_eq_single (Fin.last M)]
  · -- main term: row index `i = last M`
    have hcol : (Fin.castSucc (Fin.last M)).succAbove (Fin.last M) = Fin.last (M + 1) := by
      rw [Fin.succAbove_of_le_castSucc _ _ (le_refl _), Fin.succ_last]
    have hsign : (-1 : R) ^ ((Fin.last M : ℕ) + (Fin.last M : ℕ)) = 1 := by
      simp only [Fin.val_last]; rw [show M + M = 2 * M by ring, pow_mul]; simp
    rw [Matrix.submatrix_apply, hcol,
        Amat_val_eq w lam _ _ M (M + 1)
          (by rw [Fin.val_castSucc, Fin.val_last]) (Fin.val_last _),
        if_neg (by omega), if_pos (by omega)]
    simp only [Fin.succAbove_last]
    rw [Amat_inner_submatrix, hsign]; ring
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
        Amat_val_eq w lam _ _ (i : ℕ) (M + 1) (Fin.val_castSucc _) (Fin.val_last _),
        if_neg (by omega), if_neg (by omega), if_neg (by omega)]
    ring
  · intro h; exact absurd (Finset.mem_univ _) h

/-- The load-bearing determinant recurrence (back-peel cofactor expansion along the
    last row). -/
theorem Amat_det_rec (w : ℕ → R) (lam : R) (M : ℕ) :
    (Amat w lam (M + 2)).det
      = (Amat w lam (M + 1)).det + lam * w (M + 2) * (Amat w lam M).det := by
  rw [Matrix.det_succ_row (Amat w lam (M + 2)) (Fin.last (M + 1)), Fin.sum_univ_castSucc]
  rw [Finset.sum_eq_single (Fin.last M)
        (fun j _ hj => by
          have hjM : (j : ℕ) < M := by
            have h1 := j.isLt
            have h2 : (j : ℕ) ≠ M := fun h =>
              hj (Fin.val_injective (by rw [Fin.val_last]; exact h))
            omega
          have he : Amat w lam (M + 2) (Fin.last (M + 1)) (Fin.castSucc j) = 0 := by
            rw [Amat_val_eq w lam _ _ (M + 1) (j : ℕ) (Fin.val_last _) (Fin.val_castSucc _),
                if_neg (by omega), if_neg (by omega), if_neg (by omega)]
          rw [he]; ring)
        (fun h => absurd (Finset.mem_univ _) h)]
  have hsL : (-1 : R) ^ ((Fin.last (M + 1) : ℕ) + (Fin.last (M + 1) : ℕ)) = 1 := by
    simp only [Fin.val_last]; rw [show (M + 1) + (M + 1) = 2 * (M + 1) by ring, pow_mul]; simp
  have hsS : (-1 : R) ^ ((Fin.last (M + 1) : ℕ) + (Fin.castSucc (Fin.last M) : ℕ)) = -1 := by
    simp only [Fin.val_last, Fin.val_castSucc]
    rw [show (M + 1) + M = 2 * M + 1 by ring, pow_succ, pow_mul]; simp
  simp only [Fin.succAbove_last]
  rw [Amat_submatrix_castSucc, Amat_inner_det,
      Amat_val_eq w lam _ _ (M + 1) (M + 1) (Fin.val_last _) (Fin.val_last _), if_pos (by omega),
      Amat_val_eq w lam _ _ (M + 1) M (Fin.val_last _)
        (by rw [Fin.val_castSucc, Fin.val_last]),
      if_neg (by omega), if_neg (by omega), if_pos (by omega),
      hsL, hsS]
  ring

/-- **T_DET** : the verbatim tridiagonal determinant equals the load-bearing
    continuant sequence, for every `M`. -/
theorem T_DET (w : ℕ → R) (lam : R) : ∀ M, (Amat w lam M).det = cseq w lam M
  | 0 => by simp [Matrix.det_fin_zero]
  | 1 => g0_matches_cseq_one w lam
  | (M + 2) => by
      rw [Amat_det_rec, cseq_add_two, T_DET w lam (M + 1), T_DET w lam M]

/-! ## Phase P2 — `T_COMB : cseq w lam M = Rpoly w lam M`

`cseq` equals the weighted independence (sparse-subset) polynomial of the path on
the vertex set `{2,…,M}`.  This is the full general-`M` identity, proved by showing
`Rpoly` satisfies the same order-two recurrence as `cseq` via deletion–contraction
on the top vertex `M`. -/

/-- Sparse (independent) subsets of the path on vertex set `{2,…,M}`: subsets `S`
    of `Icc 2 M` containing no two consecutive integers. -/
def Sp (M : ℕ) : Finset (Finset ℕ) :=
  (Finset.Icc 2 M).powerset.filter (fun S => ∀ i ∈ S, i + 1 ∉ S)

lemma mem_Sp {M : ℕ} {S : Finset ℕ} :
    S ∈ Sp M ↔ S ⊆ Finset.Icc 2 M ∧ ∀ i ∈ S, i + 1 ∉ S := by
  simp only [Sp, Finset.mem_filter, Finset.mem_powerset]

/-- Weighted independence (sparse-subset) polynomial: `R_M = ∑_{S sparse} ∏_{i∈S} lam·w i`. -/
def Rpoly (w : ℕ → R) (lam : R) (M : ℕ) : R :=
  ∑ S ∈ Sp M, ∏ i ∈ S, lam * w i

lemma Sp_zero : Sp 0 = {∅} := by decide
lemma Sp_one : Sp 1 = {∅} := by decide

lemma Rpoly_zero (w : ℕ → R) (lam : R) : Rpoly w lam 0 = 1 := by
  simp [Rpoly, Sp_zero]

lemma Rpoly_one (w : ℕ → R) (lam : R) : Rpoly w lam 1 = 1 := by
  simp [Rpoly, Sp_one]

/-- Sparse subsets of `{2,…,n+2}` avoiding the top vertex `n+2` are exactly the
    sparse subsets of `{2,…,n+1}`. -/
lemma Sp_succ_not (n : ℕ) :
    (Sp (n + 2)).filter (fun S => n + 2 ∉ S) = Sp (n + 1) := by
  ext S
  simp only [Finset.mem_filter, mem_Sp]
  constructor
  · rintro ⟨⟨hsub, hsp⟩, hnot⟩
    refine ⟨fun x hx => ?_, hsp⟩
    have hx2 := hsub hx
    rw [Finset.mem_Icc] at hx2 ⊢
    have hne : x ≠ n + 2 := fun h => hnot (h ▸ hx)
    omega
  · rintro ⟨hsub, hsp⟩
    refine ⟨⟨fun x hx => ?_, hsp⟩, fun h => ?_⟩
    · have hx2 := hsub hx
      rw [Finset.mem_Icc] at hx2 ⊢
      omega
    · have := hsub h
      rw [Finset.mem_Icc] at this
      omega

/-- Sparse subsets of `{2,…,n+2}` containing the top vertex `n+2` are exactly the
    images under `insert (n+2)` of the sparse subsets of `{2,…,n}`. -/
lemma Sp_succ_mem (n : ℕ) :
    (Sp (n + 2)).filter (fun S => n + 2 ∈ S) = (Sp n).image (insert (n + 2)) := by
  ext S
  simp only [Finset.mem_filter, mem_Sp, Finset.mem_image]
  constructor
  · rintro ⟨⟨hsub, hsp⟩, hmem⟩
    refine ⟨S.erase (n + 2), ⟨fun x hx => ?_, fun i hi => ?_⟩, Finset.insert_erase hmem⟩
    · have hxS := Finset.mem_of_mem_erase hx
      have hxne : x ≠ n + 2 := Finset.ne_of_mem_erase hx
      have hx2 := hsub hxS
      rw [Finset.mem_Icc] at hx2 ⊢
      have hxne1 : x ≠ n + 1 := by
        intro h
        exact (hsp (n + 1) (h ▸ hxS)) hmem
      omega
    · have hiS := Finset.mem_of_mem_erase hi
      exact fun hcon => hsp i hiS (Finset.mem_of_mem_erase hcon)
  · rintro ⟨S', ⟨hsub', hsp'⟩, rfl⟩
    have hns : n + 2 ∉ S' := fun h => by
      have := hsub' h; rw [Finset.mem_Icc] at this; omega
    refine ⟨⟨fun x hx => ?_, fun i hi => ?_⟩, Finset.mem_insert_self _ _⟩
    · rw [Finset.mem_insert] at hx
      rcases hx with h | h
      · subst h; rw [Finset.mem_Icc]; omega
      · have := hsub' h; rw [Finset.mem_Icc] at this ⊢; omega
    · rw [Finset.mem_insert] at hi
      rw [Finset.mem_insert, not_or]
      rcases hi with h | h
      · subst h
        refine ⟨by omega, fun hc => ?_⟩
        have := hsub' hc; rw [Finset.mem_Icc] at this; omega
      · have hile := hsub' h; rw [Finset.mem_Icc] at hile
        refine ⟨by omega, hsp' i h⟩

/-- `insert (n+2)` is injective on the sparse subsets of `{2,…,n}` (none of which
    contains `n+2`). -/
lemma insert_injOn_Sp (n : ℕ) :
    Set.InjOn (insert (n + 2)) (Sp n : Set (Finset ℕ)) := by
  intro A hA B hB hAB
  have hnA : n + 2 ∉ A := fun h => by
    have := (mem_Sp.mp hA).1 h; rw [Finset.mem_Icc] at this; omega
  have hnB : n + 2 ∉ B := fun h => by
    have := (mem_Sp.mp hB).1 h; rw [Finset.mem_Icc] at this; omega
  have := congrArg (fun T => T.erase (n + 2)) hAB
  simpa [Finset.erase_insert hnA, Finset.erase_insert hnB] using this

/-- `R_M` satisfies the same order-two recurrence as the continuant `c_M`. -/
lemma Rpoly_rec (w : ℕ → R) (lam : R) (n : ℕ) :
    Rpoly w lam (n + 2) = Rpoly w lam (n + 1) + lam * w (n + 2) * Rpoly w lam n := by
  unfold Rpoly
  rw [← Finset.sum_filter_add_sum_filter_not (Sp (n + 2)) (fun S => n + 2 ∈ S)]
  rw [add_comm]
  congr 1
  · rw [Sp_succ_not]
  · rw [Sp_succ_mem, Finset.sum_image (insert_injOn_Sp n), Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro S' hS'
    have hns : n + 2 ∉ S' := fun h => by
      have := (mem_Sp.mp hS').1 h; rw [Finset.mem_Icc] at this; omega
    rw [Finset.prod_insert hns]

/-- **T_COMB** : the continuant equals the weighted independence polynomial of the
    path on `{2,…,M}`, for every `M`. -/
theorem T_COMB (w : ℕ → R) (lam : R) : ∀ M, cseq w lam M = Rpoly w lam M
  | 0 => by rw [cseq_zero, Rpoly_zero]
  | 1 => by rw [cseq_one, Rpoly_one]
  | (M + 2) => by
      rw [cseq_add_two, Rpoly_rec, T_COMB w lam (M + 1), T_COMB w lam M]

end PcfFredholm

/-! ## Phase V — axiom-cone audit

Each target declaration must rest only on `{propext, Classical.choice, Quot.sound}`
with **no** `sorryAx`.  The `#print axioms` output is captured verbatim in SCOPE.md. -/

#print axioms PcfFredholm.T_DET
#print axioms PcfFredholm.T_COMB
#print axioms PcfFredholm.Amat_det_rec
#print axioms PcfFredholm.Amat_inner_det
#print axioms PcfFredholm.Rpoly_rec
