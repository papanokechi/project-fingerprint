/-
# PcfFredholm.Symmetric — Prop 3 symmetric-form uplift  det(I + T_N²) = r_N²

T2 of session A1-EXEC-v1, built on the general tridiagonal bridge `det_Tri`
(`Bridge.lean`).  The headline is the "section identity" of the B1/v1.1 companion
(`eq:section-identity`):

  det (I + T_N²) = r_N²

where `T_N` is the real symmetric **zero-diagonal** tridiagonal finite section with
off-diagonal entries `√(u_{j+1})` (in `Fin N` coordinates, the `(i,i+1)` entry is
`√(u_{i+2})`), and `r_N = rsec N` is the pcf continuant (`Delta.lean`).

## Proof strategy (complex factorisation)

Over `ℂ`, `I + T² = (I + iT)(I − iT)` (scalars commute), so by `Matrix.det_mul`
`det(I + T²) = det(I + iT)·det(I − iT)`.  Both `I ± iT` are diagonal-`1`
tridiagonals whose off-diagonal **products** equal `(±i·s)² = −s²`; hence by the
bridge `det_Tri` both determinants equal the same continuant `G_N` of the `+s²`
recurrence (`gcont` depends on the off-diagonals only through their product —
`gcont_eq_of_prod`).  Thus `det(I + T²) = G_N²`, and with `s_k² = u_{k+2}` the
continuant `G_N` is exactly the pcf continuant `r_N` (cast to `ℂ`).  The real
statement `T_SYM` is recovered by ring-hom descent `ℝ → ℂ` (`RingHom.map_det`).
-/
import Mathlib
import PcfFredholm.Bridge
import PcfFredholm.Delta

namespace PcfFredholm

open Matrix Finset

/-! ## General `gcont` / tridiagonal facts (any commutative ring) -/

variable {R : Type*} [CommRing R]

/-- `gcont` depends on the off-diagonals only through the products `a n * b n`. -/
theorem gcont_eq_of_prod (d a b a' b' : ℕ → R)
    (h : ∀ n, a n * b n = a' n * b' n) :
    ∀ M, gcont d a b M = gcont d a' b' M
  | 0 => rfl
  | 1 => rfl
  | (M + 2) => by
      rw [gcont_add_two, gcont_add_two, gcont_eq_of_prod d a b a' b' h (M + 1),
          gcont_eq_of_prod d a b a' b' h M, h M]

/-- `1 + c • (symmetric zero-diagonal tridiagonal of off-diagonal `s`)` is the
    diagonal-`1` tridiagonal with off-diagonals `c * s`. -/
lemma one_add_smul_Tsym (c : R) (s : ℕ → R) (N : ℕ) :
    (1 : Matrix (Fin N) (Fin N) R) + c • (Tri (fun _ => 0) s s N)
      = Tri (fun _ => 1) (fun k => c * s k) (fun k => c * s k) N := by
  ext i j
  rw [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul, Matrix.one_apply]
  simp only [Tri]
  by_cases h1 : (i : ℕ) = (j : ℕ)
  · have hfin : i = j := Fin.val_injective h1
    rw [if_pos hfin, if_pos h1, if_pos h1]; ring
  · have hfin : i ≠ j := fun h => h1 (by rw [h])
    rw [if_neg hfin, if_neg h1, if_neg h1]
    by_cases h2 : (j : ℕ) = (i : ℕ) + 1
    · rw [if_pos h2, if_pos h2]; ring
    · rw [if_neg h2, if_neg h2]
      by_cases h3 : (i : ℕ) = (j : ℕ) + 1
      · rw [if_pos h3, if_pos h3]; ring
      · rw [if_neg h3, if_neg h3]; ring

/-- `Matrix.map` of a symmetric zero-diagonal tridiagonal through a ring hom. -/
lemma Tsym_map {S : Type*} [CommRing S] (f : R →+* S) (s : ℕ → R) (N : ℕ) :
    (Tri (fun _ => 0) s s N).map f
      = Tri (fun _ => 0) (fun k => f (s k)) (fun k => f (s k)) N := by
  ext i j
  simp only [Matrix.map_apply, Tri]
  by_cases h1 : (i : ℕ) = (j : ℕ)
  · rw [if_pos h1, if_pos h1, map_zero]
  · rw [if_neg h1, if_neg h1]
    by_cases h2 : (j : ℕ) = (i : ℕ) + 1
    · rw [if_pos h2, if_pos h2]
    · rw [if_neg h2, if_neg h2]
      by_cases h3 : (i : ℕ) = (j : ℕ) + 1
      · rw [if_pos h3, if_pos h3]
      · rw [if_neg h3, if_neg h3, map_zero]

/-! ## ℂ workhorse: factorisation `I + T² = (I + iT)(I − iT)` -/

/-- For any complex off-diagonal sequence `s`, the symmetric zero-diagonal
    tridiagonal `T = Tri 0 s s` satisfies `det(I + T²) = G_N²`, where `G_N` is the
    continuant of the `+s²` recurrence `g(n+2) = g(n+1) + s_n² g(n)`. -/
theorem det_one_add_Tsym_sq (s : ℕ → ℂ) (N : ℕ) :
    (1 + (Tri (fun _ => 0) s s N) ^ 2).det
      = (gcont (fun _ => 1) (fun k => Complex.I * s k) (fun k => Complex.I * s k) N) ^ 2 := by
  set T := Tri (fun _ => (0 : ℂ)) s s N with hT
  have hII : (Complex.I • T) * (Complex.I • T) = -(T ^ 2) := by
    rw [Matrix.smul_mul, Matrix.mul_smul, smul_smul, Complex.I_mul_I, neg_one_smul, ← pow_two]
  have hfac : (1 + Complex.I • T) * (1 - Complex.I • T) = 1 + T ^ 2 := by
    have key : (1 + Complex.I • T) * (1 - Complex.I • T)
        = 1 - (Complex.I • T) * (Complex.I • T) := by generalize Complex.I • T = x; noncomm_ring
    rw [key, hII, sub_neg_eq_add]
  have hplus : (1 : Matrix (Fin N) (Fin N) ℂ) + Complex.I • T
      = Tri (fun _ => 1) (fun k => Complex.I * s k) (fun k => Complex.I * s k) N := by
    rw [hT]; exact one_add_smul_Tsym Complex.I s N
  have hminus : (1 : Matrix (Fin N) (Fin N) ℂ) - Complex.I • T
      = Tri (fun _ => 1) (fun k => -Complex.I * s k) (fun k => -Complex.I * s k) N := by
    rw [hT, sub_eq_add_neg, ← neg_smul]; exact one_add_smul_Tsym (-Complex.I) s N
  rw [← hfac, Matrix.det_mul, hplus, hminus, det_Tri, det_Tri,
      gcont_eq_of_prod (fun _ => 1) (fun k => -Complex.I * s k) (fun k => -Complex.I * s k)
        (fun k => Complex.I * s k) (fun k => Complex.I * s k)
        (fun n => by
          show (-Complex.I * s n) * (-Complex.I * s n) = (Complex.I * s n) * (Complex.I * s n)
          ring) N,
      ← pow_two]

/-! ## pcf instance: `s k = √(u_{k+2})`, `det(I + T_N²) = r_N²` -/

/-- Off-diagonal weight of the Prop-3 operator: `s k = √(u_{k+2})` (real). -/
noncomputable def sval (k : ℕ) : ℝ := Real.sqrt ((ud (k + 2) : ℚ) : ℝ)

/-- The same weight viewed in `ℂ`. -/
noncomputable def svalC (k : ℕ) : ℂ := ((sval k : ℝ) : ℂ)

lemma ud_nonneg (n : ℕ) : (0 : ℚ) ≤ ud n := by
  unfold ud; positivity

lemma sval_mul_self (k : ℕ) : sval k * sval k = ((ud (k + 2) : ℚ) : ℝ) := by
  unfold sval
  exact Real.mul_self_sqrt (by exact_mod_cast ud_nonneg (k + 2))

lemma svalC_mul_self (k : ℕ) : svalC k * svalC k = (((ud (k + 2) : ℚ) : ℝ) : ℂ) := by
  unfold svalC
  rw [← Complex.ofReal_mul, sval_mul_self]

/-- The `+s²` continuant with `s_k = √(u_{k+2})` equals the pcf continuant `r_N`
    (cast `ℚ → ℝ → ℂ`). -/
lemma gcont_svalC_eq_rsec :
    ∀ N, gcont (fun _ => (1 : ℂ)) (fun k => Complex.I * svalC k) (fun k => Complex.I * svalC k) N
        = (((rsec N : ℚ) : ℝ) : ℂ)
  | 0 => by rw [gcont_zero, show rsec 0 = 1 from rfl]; norm_num
  | 1 => by rw [gcont_one, show rsec 1 = 1 from rfl]; norm_num
  | (M + 2) => by
      have hs : (Complex.I * svalC M) * (Complex.I * svalC M)
          = -(((ud (M + 2) : ℚ) : ℝ) : ℂ) := by
        calc (Complex.I * svalC M) * (Complex.I * svalC M)
            = (Complex.I * Complex.I) * (svalC M * svalC M) := by ring
          _ = (-1) * (((ud (M + 2) : ℚ) : ℝ) : ℂ) := by rw [Complex.I_mul_I, svalC_mul_self]
          _ = -(((ud (M + 2) : ℚ) : ℝ) : ℂ) := by ring
      simp only [gcont_add_two]
      rw [gcont_svalC_eq_rsec (M + 1), gcont_svalC_eq_rsec M, hs, rsec_rec]
      push_cast
      ring

/-- The real symmetric zero-diagonal √u-weighted tridiagonal finite section `T_N`. -/
noncomputable def TsymR (N : ℕ) : Matrix (Fin N) (Fin N) ℝ := Tri (fun _ => 0) sval sval N

lemma ofRealHom_sval (k : ℕ) : Complex.ofRealHom (sval k) = svalC k := by
  rw [Complex.ofRealHom_eq_coe]; rfl

lemma TsymR_map (N : ℕ) :
    (TsymR N).map Complex.ofRealHom = Tri (fun _ => (0 : ℂ)) svalC svalC N := by
  unfold TsymR
  rw [Tsym_map]
  simp only [ofRealHom_sval]

/-- **Prop 3 (ℂ form).** `det(I + T_N²) = r_N²` for the complexified √u-weighted
    symmetric zero-diagonal section. -/
theorem T_SYM_complex (N : ℕ) :
    (1 + (Tri (fun _ => (0 : ℂ)) svalC svalC N) ^ 2).det = (((rsec N : ℚ) : ℝ) : ℂ) ^ 2 := by
  rw [det_one_add_Tsym_sq, gcont_svalC_eq_rsec]

/-- **T_SYM (Prop 3, real form).** For the real symmetric √u-weighted zero-diagonal
    finite section `T_N`, `det(I + T_N²) = r_N²`. -/
theorem T_SYM (N : ℕ) : (1 + (TsymR N) ^ 2).det = ((rsec N : ℚ) : ℝ) ^ 2 := by
  have h := T_SYM_complex N
  rw [← TsymR_map] at h
  have hcomm : (1 + (TsymR N) ^ 2).map Complex.ofRealHom
      = 1 + ((TsymR N).map Complex.ofRealHom) ^ 2 := by
    rw [← RingHom.mapMatrix_apply, map_add, map_one, map_pow, RingHom.mapMatrix_apply]
  rw [← hcomm, ← RingHom.mapMatrix_apply, ← RingHom.map_det, Complex.ofRealHom_eq_coe] at h
  exact_mod_cast h

end PcfFredholm

/-! ## Phase V — axiom-cone audit -/

#print axioms PcfFredholm.det_one_add_Tsym_sq
#print axioms PcfFredholm.T_SYM_complex
#print axioms PcfFredholm.T_SYM
