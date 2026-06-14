/-
# CasoratianFramework — a general order-2 Casoratian linear-independence
  certificate over an arbitrary field.

  Session ZETA4-FRAMEWORK-v1.  This module is the shared abstraction whose
  two instances are `Apery3Catalan` (Catalan's constant `G`, open/conjectured
  target, SOS positivity) and `Zeta4Caso` (`ζ(4)=π⁴/90`, known target, factored
  positivity, degree-13 coefficients).  Both instance certificates factor
  through the single theorem `CasoratianFramework.caso_ne_zero` proved here
  (see `FrameworkInstances`).

  ## The abstraction
  Fix a field `K` and a homogeneous three-term (order-2) linear recurrence in
  canonical form
        `lead n · s (n+2) + mid n · s (n+1) + trail n · s n = 0`        (R)
  with two solution sequences `u, v : ℕ → K`.  The Casoratian (discrete
  Wronskian) is `W n = u n · v (n+1) − u (n+1) · v n`.

  Two facts, both elementary and field-general:
    * `step_law`     `lead n · W (n+1) = trail n · W n`.  The middle
                     coefficient `mid` cancels identically (a `linear_combination`
                     of the two recurrences); it never enters the certificate.
    * `caso_ne_zero` if `trail n ≠ 0` for all `n` and `W 0 ≠ 0`, then `W n ≠ 0`
                     for all `n` — i.e. `(u, v)` is a fundamental system of (R)
                     at every window.  (The non-vanishing of `lead`, which makes
                     `u, v` well-defined as a forward recurrence, is supplied by
                     the instance but is NOT needed for this proof.)

  No closed form, no determinant reformulation, and no positivity machinery is
  needed for the certificate: positivity enters each instance only to discharge
  the `trail n ≠ 0` hypothesis, and is therefore an instance-level input, not a
  part of the abstraction.

  ## Substrate
  Everything is `ring` + `mul_eq_zero` over a `Field`; the only structure used is
  `CommRing` (for `linear_combination`) and `NoZeroDivisors` (for `mul_eq_zero`),
  both implied by `Field`.  The result generalizes verbatim to any integral
  domain; `Field` is chosen because the instances live over `ℚ`.

  ANTI-AXIOM-SMUGGLING: this module introduces ZERO project axioms and ZERO
  `sorry`.  `#print axioms` at the foot confirms the clean cone.
-/
import Mathlib

namespace CasoratianFramework

variable {K : Type*} [Field K]

/-- The Casoratian (discrete Wronskian) of two `K`-valued sequences `u, v`. -/
def W (u v : ℕ → K) (n : ℕ) : K := u n * v (n + 1) - u (n + 1) * v n

/-- **General step law.** For two solutions `u, v` of the homogeneous three-term
recurrence `lead n · s (n+2) + mid n · s (n+1) + trail n · s n = 0`, the
Casoratian satisfies `lead n · W (n+1) = trail n · W n`.  The middle coefficient
`mid` cancels identically. [PROVEN] -/
theorem step_law {lead mid trail u v : ℕ → K}
    (hu : ∀ n, lead n * u (n + 2) + mid n * u (n + 1) + trail n * u n = 0)
    (hv : ∀ n, lead n * v (n + 2) + mid n * v (n + 1) + trail n * v n = 0)
    (n : ℕ) :
    lead n * W u v (n + 1) = trail n * W u v n := by
  have hun := hu n
  have hvn := hv n
  simp only [W]
  linear_combination u (n + 1) * hvn - v (n + 1) * hun

/-- **General linear-independence certificate.** If the trailing coefficient
never vanishes (`trail n ≠ 0`) and the initial Casoratian is nonzero (`W 0 ≠ 0`),
then the Casoratian never vanishes: `(u, v)` is a fundamental system of the
recurrence at every window.  Proof: induction on `n`, base `W 0 ≠ 0`, step from
`step_law` (`lead n · W (n+1) = trail n · W n`) — if `W (n+1) = 0` then
`trail n · W n = 0`, and `mul_eq_zero` forces `trail n = 0` (excluded) or
`W n = 0` (excluded by the induction hypothesis). [PROVEN] -/
theorem caso_ne_zero {lead mid trail u v : ℕ → K}
    (hu : ∀ n, lead n * u (n + 2) + mid n * u (n + 1) + trail n * u n = 0)
    (hv : ∀ n, lead n * v (n + 2) + mid n * v (n + 1) + trail n * v n = 0)
    (htrail : ∀ n, trail n ≠ 0) (hW0 : W u v 0 ≠ 0) :
    ∀ n, W u v n ≠ 0
  | 0 => hW0
  | (n + 1) => by
      intro hW1
      have hstep : lead n * W u v (n + 1) = trail n * W u v n := step_law hu hv n
      rw [hW1, mul_zero] at hstep
      rcases mul_eq_zero.mp hstep.symm with h | h
      · exact htrail n h
      · exact caso_ne_zero hu hv htrail hW0 n h

end CasoratianFramework

/-! ## Phase V — axiom-cone audit -/
#print axioms CasoratianFramework.step_law
#print axioms CasoratianFramework.caso_ne_zero
