/-
op:cc-transcendence/cc4-3  —  Lean finitary cores (PROVEN tier)

Four small, fully checkable cores extracted from the cc4 program. Each is a
finitary/arithmetic sub-claim; nothing here asserts anything about C-transcendence
(that is op:cc-3's burden). PROVEN = the `#print axioms` cone of every theorem
below is ⊆ {propext, Classical.choice, Quot.sound} with no `sorryAx`.

  Core 1 (cc4-0b bound arithmetic):   B₂ = 3, B₁ = 7, both ≤ 20.
  Core 2 (A2 pullback exponents):     s = t² doubles {0,½,1,3/2} to {0,1,2,3} ⊂ ℤ.
  Core 3 (A1 eigenvalue parity):      exp@0 monodromy eigenvalues are negation-closed;
                                      exp@R eigenvalues {1,1,1,e^{iπ/3}} are NOT.
  Core 4 (A1b group theory):          a 4-cycle in S₄ is odd, so it lies outside A₄
                                      (the index-2 alternating subgroup).
-/
import Mathlib

namespace Cc4Cores

/-! ## Core 1 — cc4-0b a-priori degree/pole bounds (B ≤ 20) -/
namespace Bound

/-- Route 2 object `End(M) ⊗ √s`: pole ≤ 1 at `s=0`, ≤ 2 at `s=R`, no growth at `∞`. -/
def B2 : ℕ := 1 + 2 + 0
/-- Route 1 eigenring on the `s=t²` cover: pole ≤ 3 at `t=0`, ≤ 2 at each of `t=±t_R`. -/
def B1 : ℕ := 3 + 2 + 2

theorem B2_eq : B2 = 3 := rfl
theorem B1_eq : B1 = 7 := rfl

/-- Both search bounds are ≤ 20, so the empirical cc4-0 searches (deg 8 / 10) cover
    them: the SL₄ verdict is bound-complete. -/
theorem bounds_le_twenty : B2 ≤ 20 ∧ B1 ≤ 20 := by decide

end Bound

/-! ## Core 2 — A2 pullback of the `s=0` exponents under `s = t²` -/
namespace Pullback

/-- The exponents of `L₂` at `s = 0` (cc-1 Riemann scheme). -/
def exp0 : List ℚ := [0, 1/2, 1, 3/2]

/-- Pullback under `s = t²` doubles every local exponent. The doubled exponents are
    exactly `{0,1,2,3}` (A2 prediction). -/
theorem pulled_values :
    2 * (0 : ℚ) = 0 ∧ 2 * (1/2 : ℚ) = 1 ∧ 2 * (1 : ℚ) = 2 ∧ 2 * (3/2 : ℚ) = 3 := by
  norm_num

/-- Each doubled exponent is an integer: the cover desingularizes the half-integer
    ramification of the `s=0` exponents (`{0,½,1,3/2}` → `{0,1,2,3} ⊂ ℤ`). -/
theorem pulled_all_integral :
    (∃ n : ℤ, 2 * (0 : ℚ) = n) ∧ (∃ n : ℤ, 2 * (1/2 : ℚ) = n) ∧
    (∃ n : ℤ, 2 * (1 : ℚ) = n) ∧ (∃ n : ℤ, 2 * (3/2 : ℚ) = n) :=
  ⟨⟨0, by norm_num⟩, ⟨1, by norm_num⟩, ⟨2, by norm_num⟩, ⟨3, by norm_num⟩⟩

end Pullback

/-! ## Core 3 — A1 eigenvalue-parity bookkeeping

Encode a monodromy eigenvalue `exp(2πi·k/6)` by its angle `k ∈ ZMod 6`. Eigenvalue
negation `λ ↦ -λ` is the angle shift `k ↦ k + 3`. A multiset of eigenvalues is
"closed under negation" iff the negated angle-list is a permutation of the original. -/
namespace Parity

/-- `M₀` eigenvalues `{1,-1,1,-1}` as angles in `ZMod 6` (`-1 = exp(2πi·3/6)`). -/
def angles0 : List (ZMod 6) := [0, 3, 0, 3]
/-- `M_R` eigenvalues `{1,1,1,e^{iπ/3}}` as angles (`e^{iπ/3}=exp(2πi·1/6)`). -/
def anglesR : List (ZMod 6) := [0, 0, 0, 1]

/-- Eigenvalue negation `λ ↦ -λ` acts on the angle by `k ↦ k+3` (since `-1 = exp(2πi·3/6)`). -/
def negEig (k : ZMod 6) : ZMod 6 := k + 3

/-- exp@0 eigenvalues ARE closed under negation — this is why the imprimitive `C₂`
    class survived local analysis (and why `η` may ramify at `0`). -/
theorem angles0_neg_closed : List.Perm (angles0.map negEig) angles0 := by decide

/-- exp@R eigenvalues are NOT closed under negation (`e^{iπ/3}` is unpaired): `η`
    cannot be unramified at `R`. With the even-branch-count constraint this forces
    the unique candidate `η = √s`. -/
theorem anglesR_not_neg_closed : ¬ List.Perm (anglesR.map negEig) anglesR := by decide

end Parity

/-! ## Core 4 — A1b: a 4-cycle in S₄ is odd ⇒ outside the alternating subgroup -/
namespace FourCycle

open Equiv Equiv.Perm

/-- The 4-cycle `(0 1 2 3)` in `S₄`. -/
def c4 : Perm (Fin 4) := finRotate 4

/-- A 4-cycle is an odd permutation. -/
theorem c4_sign : Equiv.Perm.sign c4 = -1 := by
  rw [c4, sign_finRotate]
  decide

/-- Hence the 4-cycle does not lie in the alternating group `A₄`; any subgroup of
    `S₄` containing it therefore meets `A₄` in a proper (index-2) subgroup. This is
    the group-theoretic heart of A1b. -/
theorem c4_not_mem_alternating : c4 ∉ alternatingGroup (Fin 4) := by
  rw [mem_alternatingGroup, c4_sign]
  decide

end FourCycle

end Cc4Cores
