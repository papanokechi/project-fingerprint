/-
# FrameworkInstances — the two proven certificates as corollaries of the
  general `CasoratianFramework.caso_ne_zero`.

  Session ZETA4-FRAMEWORK-v1.  This module imports the general abstraction and
  both instance modules and re-derives each instance's flagship certificate
  (`W n ≠ 0 ∀ n`) by a SINGLE application of `CasoratianFramework.caso_ne_zero`.
  It demonstrates that the abstraction genuinely covers both arithmetically
  distinct instances — Catalan (open target, SOS positivity, `lead = Acoef(·+1)`,
  `trail = −Bcoef(·+1)`) and `ζ(4)` (known target, factored positivity,
  `lead = C2`, `trail = C0`) — with no leak or forcing.

  Each derivation supplies exactly the three instance-level inputs the
  abstraction asks for:
    1. the homogeneous form of the recurrence for both solution sequences
       (`hu, hv`, a one-line `linear_combination` of the instance's proven
       `rec_u, rec_v`);
    2. non-vanishing of the trailing coefficient (`htrail`, from the instance's
       positivity lemma — `Bcoef_succ_pos` for Catalan, `C0_pos` for `ζ(4)`);
    3. `W 0 ≠ 0` (`hW0`, from the instance's `W_zero`).
  The middle coefficient (`q` for Catalan, the degree-13 `C1` for `ζ(4)`) is
  passed only inside `hu, hv` and cancels in the framework's `step_law`.

  The instance `W`s are DEFINITIONALLY the framework `W` (same formula); the
  `*_W_eq` lemmas (`rfl`) record this so the corollary statements are about the
  very same Casoratian the instances define.

  ANTI-AXIOM-SMUGGLING: ZERO axioms, ZERO `sorry`.  `#print axioms` at the foot
  confirms both corollaries inherit the clean cone of the abstraction.
-/
import CasoratianFramework
import Apery3Catalan
import Zeta4Caso

namespace FrameworkInstances

/-! ## Instance 1 — Catalan's constant (`Apery3Catalan`) -/

/-- The Catalan instance's Casoratian is the framework Casoratian (`rfl`). -/
lemma catalan_W_eq (n : ℕ) :
    PcfApery3.W n = CasoratianFramework.W PcfApery3.u PcfApery3.v n := rfl

/-- **Catalan certificate as a corollary of the general theorem.**
    `lead = Acoef(·+1)`, `mid = −q(·+1)`, `trail = −Bcoef(·+1)`. [PROVEN] -/
theorem catalan_caso_ne_zero : ∀ n, PcfApery3.W n ≠ 0 := by
  have hu : ∀ n, PcfApery3.Acoef (n + 1) * PcfApery3.u (n + 2)
      + (- PcfApery3.q (n + 1)) * PcfApery3.u (n + 1)
      + (- PcfApery3.Bcoef (n + 1)) * PcfApery3.u n = 0 := by
    intro n; linear_combination PcfApery3.rec_u n
  have hv : ∀ n, PcfApery3.Acoef (n + 1) * PcfApery3.v (n + 2)
      + (- PcfApery3.q (n + 1)) * PcfApery3.v (n + 1)
      + (- PcfApery3.Bcoef (n + 1)) * PcfApery3.v n = 0 := by
    intro n; linear_combination PcfApery3.rec_v n
  have htrail : ∀ n, (- PcfApery3.Bcoef (n + 1)) ≠ 0 := by
    intro n; exact neg_ne_zero.mpr (PcfApery3.Bcoef_succ_pos n).ne'
  have hW0 : CasoratianFramework.W PcfApery3.u PcfApery3.v 0 ≠ 0 := by
    show PcfApery3.W 0 ≠ 0
    rw [PcfApery3.W_zero]; norm_num
  exact CasoratianFramework.caso_ne_zero hu hv htrail hW0

/-! ## Instance 2 — `ζ(4) = π⁴/90` (`Zeta4Caso`) -/

/-- The `ζ(4)` instance's Casoratian is the framework Casoratian (`rfl`). -/
lemma zeta4_W_eq (n : ℕ) :
    Zeta4Caso.W n = CasoratianFramework.W Zeta4Caso.u Zeta4Caso.v n := rfl

/-- **`ζ(4)` certificate as a corollary of the general theorem.**
    `lead = C2`, `mid = C1` (degree 13), `trail = C0`. [PROVEN] -/
theorem zeta4_caso_ne_zero : ∀ n, Zeta4Caso.W n ≠ 0 := by
  have hu : ∀ n, Zeta4Caso.C2 n * Zeta4Caso.u (n + 2)
      + Zeta4Caso.C1 n * Zeta4Caso.u (n + 1)
      + Zeta4Caso.C0 n * Zeta4Caso.u n = 0 := by
    intro n; linear_combination Zeta4Caso.rec_u n
  have hv : ∀ n, Zeta4Caso.C2 n * Zeta4Caso.v (n + 2)
      + Zeta4Caso.C1 n * Zeta4Caso.v (n + 1)
      + Zeta4Caso.C0 n * Zeta4Caso.v n = 0 := by
    intro n; linear_combination Zeta4Caso.rec_v n
  have htrail : ∀ n, Zeta4Caso.C0 n ≠ 0 := by
    intro n; exact (Zeta4Caso.C0_pos n).ne'
  have hW0 : CasoratianFramework.W Zeta4Caso.u Zeta4Caso.v 0 ≠ 0 := by
    show Zeta4Caso.W 0 ≠ 0
    rw [Zeta4Caso.W_zero]; norm_num
  exact CasoratianFramework.caso_ne_zero hu hv htrail hW0

end FrameworkInstances

/-! ## Phase V — axiom-cone audit (both corollaries inherit the clean cone) -/
#print axioms FrameworkInstances.catalan_caso_ne_zero
#print axioms FrameworkInstances.zeta4_caso_ne_zero
