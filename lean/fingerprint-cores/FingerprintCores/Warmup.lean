/-
Warm-up theorems (cone-workflow validation, Pillar C shakedown).

Two genuinely-proven declarations (0 sorry), chosen to exercise both ends of the
axiom-cone spectrum:

  * `taut`         — pure-logic tautology; expected MINIMAL cone (no axioms).
  * `real_le_refl` — `le_refl` on ℝ (a quotient/classical construction); expected
                     FULL cone {propext, Classical.choice, Quot.sound}. Still PROVEN.

Every Mathlib lemma used here was confirmed with `#check` before use
(`Nat.le_succ`, `le_refl`); none came from memory.
-/
import Mathlib

namespace FingerprintCores.Warmup

/-- Warm-up #1: pure-logic tautology `p → p`. Expected minimal axiom cone. -/
theorem taut (p : Prop) : p → p := fun h => h

#print axioms taut

/-- Warm-up #2: reflexivity of `≤` on ℝ, via the `#check`ed Mathlib `le_refl`.
    ℝ is built from quotients with classical order, so the cone is expected to be
    the full `{propext, Classical.choice, Quot.sound}` — still PROVEN. -/
theorem real_le_refl (x : ℝ) : x ≤ x := le_refl x

#print axioms real_le_refl

end FingerprintCores.Warmup
