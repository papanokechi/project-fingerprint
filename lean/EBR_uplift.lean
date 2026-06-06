/-
  EBR (positive-b) — M10 Lean uplift: fixed-d algebraic core (clean axiom cone)
  ============================================================================
  Task T1-EBR-THEOREM-52W (v4) M10 Lean uplift. Governs: the ANTI-AXIOM-SMUGGLING
  rule — a `sorry`-free file that encodes a load-bearing general-d claim as an
  `axiom` is WORSE than the honest "symbolic+verified-to-d6" grade. So this file
  introduces **ZERO project axioms**: every theorem below is genuinely proven and
  its `#print axioms` cone is {propext, Classical.choice, Quot.sound} (the Mathlib
  baseline), zero sorry.

  WHAT IS MACHINE-CHECKED HERE (clean cone, fixed d):
    (A) Positivity — GENERAL (any b with b n>0, all n, ANY degree, d-independent):
        the Wallis denominators Q_n>0. This is the (H-pos) ⇒ Q_n>0 step, fully
        general, not fixed-d.
    (B) The claimed leading-coefficient polynomial a_{2d}(s)=d^d s^{2d}(d^d−β s)
        — its ALGEBRA at fixed d=2,3,4,5: factorisation, the root set {0,R}, and
        the parity fact that NO negative real is a root (the Cor-2.2 content that
        retires the odd-d edge-image worry), for both an even (d=2) and an odd
        (d=3) degree.
    (C) The exponent γ=(d+1)/2+b_{d−1}/β_d — its ARITHMETIC at fixed instances
        (d=2 → 11/6 branch; d=3,5 → 2,3 pole) and the branch/pole (∈ℤ) split.
    (D) One CONDITIONAL assembled fixed-d=2 statement whose two classical inputs
        (Pringsheim; D-finite singularity-localisation — both ABSENT from Mathlib,
        Step-0 audit) are EXPLICIT HYPOTHESES in the statement, NOT axioms. Its
        `#print axioms` stays clean; the hypotheses are visible to the reader.

  WHAT IS **NOT** DONE (honestly characterised, NOT axiomatised):
    - That a_{2d} IS the holonomic ODE's leading coefficient (the Weyl-algebra
      derivation of transfer_hypothesis.py) — not formalised; referenced as
      verified outside Lean. NOT introduced as an axiom.
    - The general-d (∀ d) quantified statements: a_{2d}=d^d s^{2d}(d^d−β s) and the
      γ-law. INFEASIBLE with current tactics — the term d^d s^{2d} has a VARIABLE
      exponent, so it is not a Lean polynomial and `ring`/`decide` do not apply.
      Left as a characterised gap, NOT an axiom.
    - The analytic bridges (Pringsheim, localisation, Δ-domain transfer): absent
      from Mathlib; supplied as explicit hypotheses in (D), not as axioms.
-/
import Mathlib

namespace EBRUplift

noncomputable section

/-! ## (A) Positivity — general (any positive b, any degree).  (H-pos) ⇒ Q_n>0. -/

/-- State pair `QPair b n = (Q_n, Q_{n+1})` for the Wallis recurrence
    `Q_0=1, Q_1=b 1, Q_{n+2}=b(n+2)·Q_{n+1}+Q_n`.  Structural recursion on `n`. -/
def QPair (b : ℕ → ℝ) : ℕ → ℝ × ℝ
  | 0 => (1, b 1)
  | (n + 1) => ((QPair b n).2, b (n + 2) * (QPair b n).2 + (QPair b n).1)

/-- `Q_n` = first component. -/
def Qval (b : ℕ → ℝ) (n : ℕ) : ℝ := (QPair b n).1

theorem Qval_zero (b : ℕ → ℝ) : Qval b 0 = 1 := by simp only [Qval, QPair]

theorem Qval_one (b : ℕ → ℝ) : Qval b 1 = b 1 := by simp only [Qval, QPair]

/-- The Wallis recurrence holds for `Qval` (so `Qval b n` really is `Q_n`). -/
theorem Qval_rec (b : ℕ → ℝ) (n : ℕ) :
    Qval b (n + 2) = b (n + 2) * Qval b (n + 1) + Qval b n := by
  simp only [Qval, QPair]

/-- **(A) Positivity, general.**  If `b n > 0` for every `n ≥ 1`, then `Q_n > 0`
    for all `n`.  Two-term induction via the state pair.  This is degree-INDEPENDENT
    (positivity needs no `d`), so it covers (H-pos) for every degree at once. -/
theorem Qval_pos (b : ℕ → ℝ) (hb : ∀ n, 1 ≤ n → 0 < b n) : ∀ n, 0 < Qval b n := by
  have key : ∀ n, 0 < (QPair b n).1 ∧ 0 < (QPair b n).2 := by
    intro n
    induction n with
    | zero =>
      refine ⟨?_, ?_⟩
      · simp only [QPair]; norm_num
      · simp only [QPair]; exact hb 1 (by norm_num)
    | succ k ih =>
      obtain ⟨h0, h1⟩ := ih
      simp only [QPair]
      refine ⟨h1, ?_⟩
      have hb2 : 0 < b (k + 2) := hb (k + 2) (by omega)
      have hp := mul_pos hb2 h1
      linarith
  exact fun n => (key n).1

/-! ## (B) Leading-coefficient polynomial algebra, fixed d (the a_{2d} content).

    `Ld β s` is the CLAIMED order-2d ODE leading coefficient
    `a_{2d}(s) = d^d s^{2d}(d^d − β s)` (form from transfer_hypothesis.py, verified
    there exact d=2..6).  Here we machine-check its ALGEBRA: factorisation, roots
    {0, R}, and that no negative real is a root.  We do NOT assert here that `Ld`
    is the ODE leading coefficient (that derivation is referenced, not formalised). -/

def L2 (β s : ℝ) : ℝ := 16 * s ^ 4 - 4 * β * s ^ 5          -- d=2: 2^2 s^4(2^2−βs)
def L3 (β s : ℝ) : ℝ := 729 * s ^ 6 - 27 * β * s ^ 7        -- d=3: 3^3 s^6(3^3−βs)
def L4 (β s : ℝ) : ℝ := 65536 * s ^ 8 - 256 * β * s ^ 9     -- d=4: 4^4 s^8(4^4−βs)
def L5 (β s : ℝ) : ℝ := 9765625 * s ^ 10 - 3125 * β * s ^ 11 -- d=5: 5^5 s^10(5^5−βs)

theorem L2_factor (β s : ℝ) : L2 β s = 4 * s ^ 4 * (4 - β * s) := by unfold L2; ring
theorem L3_factor (β s : ℝ) : L3 β s = 27 * s ^ 6 * (27 - β * s) := by unfold L3; ring
theorem L4_factor (β s : ℝ) : L4 β s = 256 * s ^ 8 * (256 - β * s) := by unfold L4; ring
theorem L5_factor (β s : ℝ) : L5 β s = 3125 * s ^ 10 * (3125 - β * s) := by unfold L5; ring

/-- **(B) Root classification, d=2.**  For `β>0`, `a_4(s)=0 ↔ s=0 ∨ s=R` with
    `R=4/β=ξ₀²`.  (⇒ direction; the only one the assembly uses.) -/
theorem L2_root_imp (β s : ℝ) (hβ : 0 < β) (h : L2 β s = 0) : s = 0 ∨ s = 4 / β := by
  rw [L2_factor] at h
  have hb : β ≠ 0 := ne_of_gt hβ
  rcases mul_eq_zero.mp h with h1 | h2
  · left
    rcases mul_eq_zero.mp h1 with h4 | hs4
    · norm_num at h4
    · exact (pow_eq_zero_iff (by norm_num)).mp hs4
  · right
    rw [eq_div_iff hb, mul_comm]
    linarith

/-- s=0 and s=R are indeed roots (d=2). -/
theorem L2_zero_root (β : ℝ) : L2 β 0 = 0 := by unfold L2; ring
theorem L2_R_root (β : ℝ) (hβ : 0 < β) : L2 β (4 / β) = 0 := by
  have hb : β ≠ 0 := ne_of_gt hβ
  rw [L2_factor]
  have h4 : β * (4 / β) = 4 := by field_simp
  rw [h4]; ring

/-- **(B) Parity / Cor-2.2 content, EVEN d=2.**  NO negative real is a root: for
    `s<0`, `a_4(s)>0`.  In particular `s=−R` (the formal edge image) is not a
    singularity — the odd/even worry resolved on the algebra, even degree. -/
theorem L2_no_neg_root (β : ℝ) (hβ : 0 < β) : ∀ s : ℝ, s < 0 → 0 < L2 β s := by
  intro s hs
  rw [L2_factor]
  have hsne : s ≠ 0 := ne_of_lt hs
  have h1 : 0 < s ^ 4 := by positivity
  have h2 : 0 < 4 - β * s := by nlinarith [mul_pos hβ (neg_pos.mpr hs)]
  nlinarith [mul_pos h1 h2]

/-- **(B) Parity / Cor-2.2 content, ODD d=3.**  Same conclusion at an odd degree
    (where the deposits' odd-d ramification worry lives): for `s<0`, `a_6(s)>0`. -/
theorem L3_no_neg_root (β : ℝ) (hβ : 0 < β) : ∀ s : ℝ, s < 0 → 0 < L3 β s := by
  intro s hs
  rw [L3_factor]
  have hsne : s ≠ 0 := ne_of_lt hs
  have h1 : 0 < s ^ 6 := by positivity
  have h2 : 0 < 27 - β * s := by nlinarith [mul_pos hβ (neg_pos.mpr hs)]
  nlinarith [mul_pos h1 h2]

/-! ## (C) Exponent γ=(d+1)/2+b_{d−1}/β_d — arithmetic + branch/pole split (over ℚ). -/

def gammaFormula (d bsub βd : ℚ) : ℚ := (d + 1) / 2 + bsub / βd

theorem gamma_d2_vquad : gammaFormula 2 1 3 = 11 / 6 := by norm_num [gammaFormula]
theorem gamma_d3_pole  : gammaFormula 3 0 1 = 2 := by norm_num [gammaFormula]
theorem gamma_d5_pole  : gammaFormula 5 0 1 = 3 := by norm_num [gammaFormula]

/-- **(C) Character split.**  d=2 (b=3n²+n+1): γ=11/6 ∉ ℤ ⇒ BRANCH point. -/
theorem gamma_d2_branch : ¬ ∃ k : ℤ, gammaFormula 2 1 3 = (k : ℚ) := by
  rintro ⟨k, hk⟩
  rw [gamma_d2_vquad] at hk
  have h2 : (11 : ℚ) = 6 * (k : ℚ) := by linarith
  have h3 : (11 : ℤ) = 6 * k := by exact_mod_cast h2
  omega

/-- **(C) Character split.**  d=3 (b=n³+1): γ=2 ∈ ℤ ⇒ POLE. -/
theorem gamma_d3_pole_int : ∃ k : ℤ, gammaFormula 3 0 1 = (k : ℚ) :=
  ⟨2, by rw [gamma_d3_pole]; norm_num⟩

/-! ## (D) Conditional assembled fixed-d=2 statement.

    The two classical inputs absent from Mathlib (Step-0 audit) are EXPLICIT
    HYPOTHESES — `pringsheim` (the positive-coefficient dominant singularity sits
    at the radius R) and `localization` (every singularity is a root of the
    leading coefficient).  They are visible in the statement; NO axiom is used, so
    `#print axioms` stays clean.  Conclusion: the dominant singularity is unique on
    the radius circle (only candidates are 0 and R; no negative point), i.e. the
    transfer/uniqueness content at d=2 — CONDITIONAL on the named classical inputs. -/
theorem ebr_d2_dominant_unique
    (β : ℝ) (hβ : 0 < β)
    (Sing : ℝ → Prop)
    (pringsheim : Sing (4 / β))
    (localization : ∀ s, Sing s → L2 β s = 0) :
    Sing (4 / β) ∧ (∀ s, Sing s → s = 0 ∨ s = 4 / β) ∧ (∀ s, s < 0 → ¬ Sing s) := by
  refine ⟨pringsheim, ?_, ?_⟩
  · intro s hs
    exact L2_root_imp β s hβ (localization s hs)
  · intro s hs hSing
    have hpos := L2_no_neg_root β hβ s hs
    have hzero := localization s hSing
    linarith

/-! ## Axiom cones — recorded verbatim in the report (every one must be the clean
       baseline {propext, Classical.choice, Quot.sound}, zero project axioms). -/

#print axioms Qval_pos
#print axioms Qval_rec
#print axioms L2_factor
#print axioms L3_factor
#print axioms L4_factor
#print axioms L5_factor
#print axioms L2_root_imp
#print axioms L2_R_root
#print axioms L2_no_neg_root
#print axioms L3_no_neg_root
#print axioms gamma_d2_vquad
#print axioms gamma_d2_branch
#print axioms gamma_d3_pole_int
#print axioms ebr_d2_dominant_unique

end

end EBRUplift
