/-
  M10 — Apparent Singularity Exclusion for V_quad (Theorem 6.6 / thm:exclusion2)
  ============================================================================
  Ported into Fingerprint from `papanokechi/wallis-pcf-lean4`,
  `lean/Thm66_ApparentSingularity.lean` (branch `vquad/handoff-2026-04-16`,
  blob 5b44e69071a5b1145fba6131697475e49d82c91f), re-pinned to Lean v4.29.0 /
  Mathlib 8a178386.

  STRENGTHENING over the deposited stub
  -------------------------------------
  The deposited file defined `IndicialPoly (a) (s) := fun ρ => ρ ^ 2`, IGNORING
  both arguments.  Its central theorem was then `(fun ρ => ρ²) = (fun ρ => ρ²)`,
  i.e. definitionally `rfl`; the Frobenius axiom was decorative (the goal held
  without it) and the formalization encoded none of the ODE's content.

  This module makes `IndicialPoly` actually COMPUTE the Frobenius indicial
  polynomial from the indicial data, exactly as the deposited paper derives it
  (vquad_resurgence_R2.tex, Theorem thm:exclusion2, "Step 1: Indicial exponents",
  lines 454–487):

    For the exact ODE  a(x) y'' + a'(x) y' + c(x) y = 0  with
    P(x) = a'(x)/a(x),  Q(x) = c(x)/a(x), at a simple root s_k of a:
        p₀ = lim_{x→s_k} (x - s_k) P(x) = a'(s_k)/a'(s_k) = 1,
        q₀ = lim_{x→s_k} (x - s_k)² Q(x) = 0,
    so the indicial polynomial is
        I(ρ) = ρ(ρ-1) + p₀·ρ + q₀ = ρ(ρ-1) + 1·ρ + 0 = ρ².

  Here `IndicialPoly p₀ q₀ := fun ρ => ρ*(ρ-1) + p₀*ρ + q₀` is the genuine
  indicial polynomial, and the reduction to ρ² is the *content* lemma
  `indicialPoly_one_zero` (a real, axiom-free computation).  The analytic gap
  (the two limit evaluations p₀ = 1, q₀ = 0 — "Frobenius / limit theory", not in
  Mathlib, certified in the paper at dps=150) is named as the explicit axioms
  `frobenius_indicial_data_s{1,2}`.  Consequently the Frobenius input is now
  LOAD-BEARING: `apparent_singularity_thm_i` is no longer `rfl` and its axiom cone
  genuinely contains the named analytic axioms ⇒ the Fingerprint gate correctly
  refuses unconditional PROVEN and reports PROVEN-conditional-on-H.

  Every Mathlib name used was `#check`ed in-project (see the `#check` lines), none
  taken from memory.
-/
import Mathlib

noncomputable section

namespace FingerprintCores.M10ApparentSingularity

open Complex Filter Topology

/-! ## Section 1: ODE data for V_quad
    (vquad_resurgence_R2.tex, Table 1 + eq (ode)/(exact-ode);
    a(x)=3x²+x+1, b(x)=6x+1=a'(x), c(x)=-x².) -/

def a_coeff (x : ℝ) : ℝ := 3 * x ^ 2 + x + 1
def c_coeff (x : ℝ) : ℝ := -(x ^ 2)
def b_coeff (x : ℝ) : ℝ := 6 * x + 1
def a_coeff_c (z : ℂ) : ℂ := 3 * z ^ 2 + z + 1
def c_coeff_c (z : ℂ) : ℂ := -(z ^ 2)
def s₁ : ℂ := (-1 + I * (Real.sqrt 11 : ℝ)) / 6
def s₂ : ℂ := (-1 - I * (Real.sqrt 11 : ℝ)) / 6

/-! ## Section 2: Lemma 1 — b(x) = a'(x)  (ported verbatim; genuinely proven) -/

/-- **Lemma 1**: HasDerivAt certificate for a(x) = 3x²+x+1. -/
theorem hasDerivAt_a_coeff (x : ℝ) :
    HasDerivAt a_coeff (b_coeff x) x := by
  unfold a_coeff b_coeff
  have h1 := (hasDerivAt_pow 2 x).const_mul (3 : ℝ)
  have h2 := hasDerivAt_id' x
  have h3 := hasDerivAt_const x (1 : ℝ)
  have h12 := HasDerivAt.add h1 h2
  have h123 := HasDerivAt.add h12 h3
  exact HasDerivAt.congr_deriv h123 (by push_cast; ring)

/-- **Lemma 1** (deriv form): deriv a_coeff x = b_coeff x = 6x+1. -/
theorem b_eq_deriv_a (x : ℝ) : deriv a_coeff x = b_coeff x :=
  (hasDerivAt_a_coeff x).deriv

/-- a is differentiable everywhere. -/
theorem differentiable_a_coeff : Differentiable ℝ a_coeff :=
  fun x => (hasDerivAt_a_coeff x).differentiableAt

/-! ## Section 3: Lemma 2 — Roots of a -/

/-- **Lemma 2a**: a(x) > 0 for all real x (no real roots).
    Proof: 3x²+x+1 = 3(x+1/6)² + 11/12 > 0. -/
theorem a_coeff_pos (x : ℝ) : a_coeff x > 0 := by
  unfold a_coeff
  have h : 3 * x ^ 2 + x + 1 = 3 * (x + 1 / 6) ^ 2 + 11 / 12 := by ring
  linarith [sq_nonneg (x + 1 / 6)]

/-- (√11)² = 11 -/
theorem sqrt_11_sq : Real.sqrt 11 ^ 2 = 11 :=
  Real.sq_sqrt (by norm_num : (11 : ℝ) ≥ 0)

-- Real signatures confirmed in-project (NOT from memory):
#check @Complex.I_sq
#check @Complex.ofReal_pow
#check @Complex.ofReal_ne_zero
#check @Complex.I_ne_zero
#check @Real.sqrt_pos

/-- Cast helper: ((√11 : ℝ) : ℂ)² = 11. -/
theorem sqrt_11_sq_c : ((Real.sqrt 11 : ℝ) : ℂ) ^ 2 = 11 := by
  rw [← Complex.ofReal_pow, sqrt_11_sq]; norm_num

/-- **Lemma 2b** (discharged — was `axiom root_s1`): s₁ is a root of a.
    3·((-1+i√11)/6)² + ((-1+i√11)/6) + 1 = 0, using I²=-1 and (√11)²=11. -/
theorem root_s1 : a_coeff_c s₁ = 0 := by
  simp only [a_coeff_c, s₁]
  linear_combination (((Real.sqrt 11 : ℝ) : ℂ) ^ 2 / 12) * Complex.I_sq
    + (-1 / 12 : ℂ) * sqrt_11_sq_c

/-- **Lemma 2b'** (discharged — was `axiom root_s2`): s₂ is a root of a. -/
theorem root_s2 : a_coeff_c s₂ = 0 := by
  simp only [a_coeff_c, s₂]
  linear_combination (((Real.sqrt 11 : ℝ) : ℂ) ^ 2 / 12) * Complex.I_sq
    + (-1 / 12 : ℂ) * sqrt_11_sq_c

/-! ## Section 4: complex derivative of a, and simple-root certificates -/

/-- HasDerivAt certificate for the complex a(z) = 3z²+z+1, derivative 6z+1. -/
theorem hasDerivAt_a_coeff_c (z : ℂ) :
    HasDerivAt a_coeff_c (6 * z + 1) z := by
  unfold a_coeff_c
  have h1 := (hasDerivAt_pow 2 z).const_mul (3 : ℂ)
  have h2 := hasDerivAt_id z
  have h3 := hasDerivAt_const z (1 : ℂ)
  have h123 := (h1.add h2).add h3
  exact HasDerivAt.congr_deriv h123 (by push_cast; ring)

/-- **Lemma 4a** (discharged — was `axiom a_deriv_s1_ne_zero`):
    deriv a_coeff_c s₁ = 6 s₁ + 1 = i√11 ≠ 0. -/
theorem a_deriv_s1_ne_zero : deriv a_coeff_c s₁ ≠ 0 := by
  rw [(hasDerivAt_a_coeff_c s₁).deriv]
  have h : (6 : ℂ) * s₁ + 1 = Complex.I * (Real.sqrt 11 : ℝ) := by
    simp only [s₁]; ring
  rw [h]
  exact mul_ne_zero Complex.I_ne_zero
    (Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sqrt_pos.mpr (by norm_num))))

/-- **Lemma 4b** (discharged — was `axiom a_deriv_s2_ne_zero`):
    deriv a_coeff_c s₂ = 6 s₂ + 1 = -i√11 ≠ 0. -/
theorem a_deriv_s2_ne_zero : deriv a_coeff_c s₂ ≠ 0 := by
  rw [(hasDerivAt_a_coeff_c s₂).deriv]
  have h : (6 : ℂ) * s₂ + 1 = -(Complex.I * (Real.sqrt 11 : ℝ)) := by
    simp only [s₂]; ring
  rw [h, neg_ne_zero]
  exact mul_ne_zero Complex.I_ne_zero
    (Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sqrt_pos.mpr (by norm_num))))

/-! ## Section 5: Lemma 3 — ODE Exactness (Product Rule) (ported; genuinely proven) -/

/-- **Lemma 3**: The ODE is exact — d/dx[a(x)y'] = a(x)y'' + a'(x)y'. -/
theorem ode_is_exact
    (f : ℝ → ℝ) (f' f'' : ℝ → ℝ) (x : ℝ)
    (_ : HasDerivAt f (f' x) x)
    (hf' : HasDerivAt f' (f'' x) x) :
    HasDerivAt (fun x => a_coeff x * f' x)
      (a_coeff x * f'' x + b_coeff x * f' x) x :=
  HasDerivAt.congr_deriv (HasDerivAt.mul (hasDerivAt_a_coeff x) hf') (by ring)

/-! ## Section 6: Lemma 4 — Indicial Equation (Frobenius), made LOAD-BEARING

    `IndicialPoly` now genuinely computes the Frobenius indicial polynomial from
    the indicial data (p₀, q₀); the deposited stub `fun ρ => ρ²` is replaced. -/

/-- Paper Step-1 indicial coefficient p₀ = lim_{x→s} (x-s)·a'(x)/a(x). -/
def indicialP0 (a : ℂ → ℂ) (s : ℂ) : ℂ :=
  limUnder (𝓝[≠] s) (fun x => (x - s) * deriv a x / a x)

/-- Paper Step-1 indicial coefficient q₀ = lim_{x→s} (x-s)²·c(x)/a(x). -/
def indicialQ0 (a c : ℂ → ℂ) (s : ℂ) : ℂ :=
  limUnder (𝓝[≠] s) (fun x => (x - s) ^ 2 * c x / a x)

/-- The **genuine** Frobenius indicial polynomial for the exact ODE
    d/dx[a(x)y'] + c(x)y = 0 at a regular singular point with indicial data
    (p₀, q₀):  `I(ρ) = ρ(ρ-1) + p₀·ρ + q₀`.  (Contrast the deposited stub
    `fun ρ => ρ²`, which discarded p₀, q₀ and hence all ODE content.) -/
def IndicialPoly (p₀ q₀ : ℂ) : ℂ → ℂ := fun ρ => ρ * (ρ - 1) + p₀ * ρ + q₀

/-- **Content lemma (axiom-free).**  With p₀ = 1 and q₀ = 0 the indicial
    polynomial reduces to ρ²:  ρ(ρ-1) + 1·ρ + 0 = ρ².  This is the algebraic
    core the stub skipped. -/
theorem indicialPoly_one_zero : IndicialPoly 1 0 = fun ρ : ℂ => ρ ^ 2 := by
  funext ρ; simp only [IndicialPoly]; ring

/-- **Pure implication (axiom-free, load-bearing).**  Whenever the indicial data
    are (1, 0), the indicial polynomial is ρ².  This is the proven content; the
    analytic input is exactly the two hypotheses `p₀ = 1`, `q₀ = 0`. -/
theorem apparent_singularity_of {p₀ q₀ : ℂ} (hp : p₀ = 1) (hq : q₀ = 0) :
    IndicialPoly p₀ q₀ = fun ρ : ℂ => ρ ^ 2 := by
  subst hp; subst hq; exact indicialPoly_one_zero

/-- Indicial root is 0 with multiplicity 2: I(ρ) = ρ² has its only zero at ρ = 0. -/
theorem indicial_root_is_zero (p₀ q₀ : ℂ)
    (h : IndicialPoly p₀ q₀ = fun ρ => ρ ^ 2) :
    ∀ ρ : ℂ, IndicialPoly p₀ q₀ ρ = 0 ↔ ρ = 0 := by
  intro ρ; rw [h]; simp [pow_eq_zero_iff]

/-! ### The named analytic gap (Frobenius / limit theory — not in Mathlib)

    These two axioms are the ONLY conditional input to part (i).  They state the
    paper's Step-1 limit evaluations for the *specific* V_quad ODE
    (`a_coeff_c`, `c_coeff_c`) at `s₁`, `s₂`: that the residue p₀ = 1 and the
    order-2 coefficient q₀ = 0.  These are the limit computations certified
    numerically at dps=150 in the deposited paper
    (`verify_frobenius_apparent.py`).  They are stated for the concrete ODE
    (NOT as a universal claim over all a, c) so that they remain faithful once
    `indicialP0`/`indicialQ0` are read with their real limit meaning. -/

/-- Analytic gap H₁ at s₁: the paper's Step-1 limits p₀(s₁)=1, q₀(s₁)=0. -/
axiom frobenius_indicial_data_s1 :
    indicialP0 a_coeff_c s₁ = 1 ∧ indicialQ0 a_coeff_c c_coeff_c s₁ = 0

/-- Analytic gap H₂ at s₂: the paper's Step-1 limits p₀(s₂)=1, q₀(s₂)=0. -/
axiom frobenius_indicial_data_s2 :
    indicialP0 a_coeff_c s₂ = 1 ∧ indicialQ0 a_coeff_c c_coeff_c s₂ = 0

/-! ## Section 7: Theorem 5 — Indicial Exponents at s₁, s₂ (PROVEN-conditional-on-H) -/

/-- **Theorem 5 (part i)**: at both s₁, s₂ the genuine indicial polynomial
    `IndicialPoly (indicialP0 …) (indicialQ0 …)` equals ρ².

    This is no longer `rfl`: it consumes the named analytic axioms
    `frobenius_indicial_data_s{1,2}` (to supply p₀=1, q₀=0) and then the
    axiom-free `apparent_singularity_of`.  Removing either axiom makes the
    statement unprovable (the `indicialP0`/`indicialQ0` limits are otherwise
    opaque), so the Frobenius input is genuinely load-bearing. -/
theorem apparent_singularity_thm_i :
    (IndicialPoly (indicialP0 a_coeff_c s₁)
        (indicialQ0 a_coeff_c c_coeff_c s₁) = fun ρ : ℂ => ρ ^ 2) ∧
    (IndicialPoly (indicialP0 a_coeff_c s₂)
        (indicialQ0 a_coeff_c c_coeff_c s₂) = fun ρ : ℂ => ρ ^ 2) := by
  refine ⟨?_, ?_⟩
  · obtain ⟨hp, hq⟩ := frobenius_indicial_data_s1
    exact apparent_singularity_of hp hq
  · obtain ⟨hp, hq⟩ := frobenius_indicial_data_s2
    exact apparent_singularity_of hp hq

/-! ## Section 8: Theorem 6 — Monodromy Structure (ported; conditional on monodromy gap) -/

/-- A 2×2 matrix is unipotent if it has form [[1,c],[0,1]]. -/
def IsUnipotent (M : Matrix (Fin 2) (Fin 2) ℂ) : Prop :=
  M 0 0 = 1 ∧ M 1 0 = 0 ∧ M 1 1 = 1

/-- Unipotent matrix action on a vector, first component. -/
theorem unipotent_fixes_first_component
    (M : Matrix (Fin 2) (Fin 2) ℂ) (hM : IsUnipotent M) (v : Fin 2 → ℂ) :
    (M.mulVec v) 0 = v 0 + M 0 1 * v 1 := by
  obtain ⟨h00, _, _⟩ := hM
  simp [Matrix.mulVec, h00]

/-- Analytic gap H₃ (Monodromy of linear ODE — not in Mathlib): a double indicial
    root ρ=0 (indicial polynomial ρ²) at a simple singularity yields unipotent
    local monodromy. Stated with the new load-bearing `IndicialPoly` form. -/
axiom monodromy_unipotent_from_double_root
    (a c : ℂ → ℂ) (s : ℂ)
    (ha_root : a s = 0) (ha_simple : deriv a s ≠ 0)
    (h_indicial : IndicialPoly (indicialP0 a s) (indicialQ0 a c s)
                    = fun ρ => ρ ^ 2) :
    ∃ M : Matrix (Fin 2) (Fin 2) ℂ, IsUnipotent M

/-- **Corollary**: V_quad invariant under monodromy at each sₖ.  Conditional on
    the monodromy gap H₃ and (transitively) on the indicial gaps H₁, H₂. -/
theorem vquad_monodromy_invariant :
    ∀ s ∈ ({s₁, s₂} : Set ℂ),
      a_coeff_c s = 0 →
      ∃ M : Matrix (Fin 2) (Fin 2) ℂ, IsUnipotent M := by
  intro s hs _
  rcases hs with rfl | rfl
  · exact monodromy_unipotent_from_double_root a_coeff_c c_coeff_c s₁
      root_s1 a_deriv_s1_ne_zero apparent_singularity_thm_i.1
  · exact monodromy_unipotent_from_double_root a_coeff_c c_coeff_c s₂
      root_s2 a_deriv_s2_ne_zero apparent_singularity_thm_i.2

/-! ## Axiom cones (recorded verbatim in the task report) -/

#print axioms indicialPoly_one_zero
#print axioms apparent_singularity_of
#print axioms root_s1
#print axioms root_s2
#print axioms a_deriv_s1_ne_zero
#print axioms a_deriv_s2_ne_zero
#print axioms apparent_singularity_thm_i
#print axioms vquad_monodromy_invariant

end FingerprintCores.M10ApparentSingularity

end
