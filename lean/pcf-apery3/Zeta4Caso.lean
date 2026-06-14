/-
# Zeta4Caso — Casoratian linear-independence certificate for the
  Schneider–Zudilin order-2 Apéry-like recurrence for `ζ(4) = π⁴/90`

  Session ZETA4-CASO2-LEAN-v1.  Second order-2 instance of the shared
  Casoratian framework whose first instance is `Apery3Catalan` (Catalan's
  constant).  This module mirrors that file's PROVEN structure exactly;
  the only mathematical differences are the (degree-13) coefficient
  polynomials and the initial data.

  ## Primary source (A0-locked, gate-cross-checked)
  C. Schneider, W. Zudilin, "A case study for ζ(4)", in: Transcendence in
  Algebra, Combinatorics, Geometry and Number Theory, Springer PROMS 373
  (2021) 421–435; arXiv:2004.08158.  DOI 10.1007/978-3-030-84304-5_17.
  The ζ(4) linear forms `L_n = q_n·ζ(4) − p_n` satisfy the ORDER-2
  (three-term) recurrence eq (23):
        C0(n)·Z(n) + C1(n)·Z(n+1) + C2(n)·Z(n+2) = 0,
  with C0, C2 given FACTORED (eq 23) and the middle coefficient C1 of
  degree 13.  Exact-ℚ cross-checked (n ≤ 50) in session
  ZETA4-CASO2-LEAN-GATE-v1 (gate.py sha256 2f9afa59…3fd825): the recurrence
  holds for both solution sequences, `q_n = (−1)ⁿ C(2n,n)⁴`, the 2×2
  Casoratian `W_n ≠ 0` (W₀ = −277/16), and the step law
  `C2(n)·W(n+1) = C0(n)·W(n)`.

  ## Notation (disambiguated, as in Apery3Catalan)
  `C0, C1, C2` are the COEFFICIENT polynomials of eq (23) (here `C0` is the
  trailing / lowest-index coefficient, `C2` the leading); `u, v` are the
  two SOLUTION sequences (`u` = denominators `q_n`, `v` = numerators `p_n`).

  ## Targets (this file) — all PROVEN, NO sorry
    positivity:  `0 < C2 n`, `0 < C0 n`  (factored ⇒ `positivity`; no SOS —
        the residual quartics have all-positive coefficients).        [PROVEN]
    step law:    `C2 n · W (n+1) = C0 n · W n`   (the degree-13 `C1`
        cancels; it stays an atom, so `ring` is light).                [PROVEN]
    certificate: `W n ≠ 0` for all `n`  ⇒ `{u, v}` linearly independent
        at every window (no closed form needed).                       [PROVEN]

  Unlike `Apery3Catalan` (which ships two STICKING-POINT sorries for the
  Casoratian closed form and the `Matrix.det` reformulation, both OUTSIDE
  the certificate cone) this module is fully sorry-FREE: the closed form
  `q_n = (−1)ⁿ C(2n,n)⁴` and the det form are not needed for the
  certificate and are documented in prose only.
-/
import Mathlib

namespace Zeta4Caso

/-! ## Coefficient polynomials of Schneider–Zudilin eq (23)

`C0` (trailing) and `C2` (leading) are written in the source's FACTORED
form — a product of a positive numeral, powers of `a·n+b` with `a,b>0`, and
a single quartic whose coefficients are all positive.  `C1` (middle,
degree 13) is written expanded; it is used only as an opaque atom in the
proofs (it cancels in the step law), so its degree never enters `ring`. -/

/-- eq (23) trailing coefficient `C0 n` (factored; manifestly positive). -/
def C0 (n : ℕ) : ℚ :=
  16 * (2 * (n : ℚ) + 1) ^ 4 * ((n : ℚ) + 1) ^ 3 * (4 * (n : ℚ) + 3) * (4 * (n : ℚ) + 5)
    * (5460 * (n : ℚ) ^ 4 + 35339 * (n : ℚ) ^ 3 + 85858 * (n : ℚ) ^ 2
        + 92804 * (n : ℚ) + 37656)

/-- eq (23) middle coefficient `C1 n` (degree 13; opaque atom in all proofs). -/
def C1 (n : ℕ) : ℚ :=
  357913920 * (n : ℚ) ^ 13 + 5716680688 * (n : ℚ) ^ 12 + 41762423804 * (n : ℚ) ^ 11
    + 184637211081 * (n : ℚ) ^ 10 + 550778114541 * (n : ℚ) ^ 9
    + 1169740743051 * (n : ℚ) ^ 8 + 1818232366245 * (n : ℚ) ^ 7
    + 2092705983417 * (n : ℚ) ^ 6 + 1782121652067 * (n : ℚ) ^ 5
    + 1108272850929 * (n : ℚ) ^ 4 + 488951050619 * (n : ℚ) ^ 3
    + 144869028586 * (n : ℚ) ^ 2 + 25833166356 * (n : ℚ) + 2094206184

/-- eq (23) leading coefficient `C2 n` (factored; manifestly positive). -/
def C2 (n : ℕ) : ℚ :=
  8 * (2 * (n : ℚ) + 3) ^ 5 * ((n : ℚ) + 2) ^ 4
    * (5460 * (n : ℚ) ^ 4 + 13499 * (n : ℚ) ^ 3 + 12601 * (n : ℚ) ^ 2
        + 5265 * (n : ℚ) + 831)

/-! ## Positivity certificate  (the gate's "easy part", confirmed)

No sum-of-squares is needed: both coefficients are products of positive
numerals, powers of `a·n+b` (`a,b>0`), and an all-positive-coefficient
quartic.  `positivity` discharges each directly (using `0 ≤ (n:ℚ)` from
`Nat.cast_nonneg`), mirroring `Apery3Catalan.Acoef_pos`. -/

/-- `0 < C2 n` for all `n`. [PROVEN] -/
lemma C2_pos (n : ℕ) : 0 < C2 n := by unfold C2; positivity

/-- `0 < C0 n` for all `n`. [PROVEN] -/
lemma C0_pos (n : ℕ) : 0 < C0 n := by unfold C0; positivity

/-! ## The two solution sequences (eq 23 recurrence + ζ(4) initial data)

`u` = ζ(4)-coefficients / denominators (`q_n`); `v` = rational numerators
(`p_n`).  Initial data from the gate: `u₀=1, u₁=−16, v₀=0, v₁=−277/16`.
The forward recurrence solves eq (23) for the top index:
`Z(n+2) = −(C0 n · Z n + C1 n · Z(n+1)) / C2 n`. -/

/-- Denominator sequence `u` (`q_n`). -/
def u : ℕ → ℚ
  | 0 => 1
  | 1 => -16
  | (n + 2) => -(C0 n * u n + C1 n * u (n + 1)) / C2 n

/-- Numerator sequence `v` (`p_n`). -/
def v : ℕ → ℚ
  | 0 => 0
  | 1 => -277 / 16
  | (n + 2) => -(C0 n * v n + C1 n * v (n + 1)) / C2 n

@[simp] lemma u_zero : u 0 = 1 := rfl
@[simp] lemma u_one : u 1 = -16 := rfl
@[simp] lemma v_zero : v 0 = 0 := rfl
@[simp] lemma v_one : v 1 = -277 / 16 := rfl

lemma u_add_two (n : ℕ) :
    u (n + 2) = -(C0 n * u n + C1 n * u (n + 1)) / C2 n := rfl
lemma v_add_two (n : ℕ) :
    v (n + 2) = -(C0 n * v n + C1 n * v (n + 1)) / C2 n := rfl

/-- The Casoratian (discrete Wronskian) of the pair `(u, v)`. -/
def W (n : ℕ) : ℚ := u n * v (n + 1) - u (n + 1) * v n

@[simp] lemma W_zero : W 0 = -277 / 16 := by norm_num [W]

/-! ## Recurrence-clearing lemmas and the Casoratian step law -/

/-- eq (23) for `u`, denominator cleared (`C2 n ≠ 0`). [PROVEN] -/
lemma rec_u (n : ℕ) :
    C2 n * u (n + 2) = -(C0 n * u n + C1 n * u (n + 1)) := by
  rw [u_add_two]
  field_simp [(C2_pos n).ne']

/-- eq (23) for `v`, denominator cleared. [PROVEN] -/
lemma rec_v (n : ℕ) :
    C2 n * v (n + 2) = -(C0 n * v n + C1 n * v (n + 1)) := by
  rw [v_add_two]
  field_simp [(C2_pos n).ne']

/-- **Step law** `C2 n · W (n+1) = C0 n · W n`. [PROVEN]
    Substituting `rec_u`, `rec_v` into `C2·(u·v' − u'·v)`, the `C1`-terms
    cancel, leaving `C0·(u n·v(n+1) − u(n+1)·v n) = C0·W n`.  `C1` stays an
    opaque atom, so `ring` does not see its degree 13. -/
lemma step_law (n : ℕ) :
    C2 n * W (n + 1) = C0 n * W n := by
  have hu := rec_u n
  have hv := rec_v n
  simp only [W]
  linear_combination u (n + 1) * hv - v (n + 1) * hu

/-! ## Flagship certificate: the Casoratian never vanishes -/

/-- **Linear-independence certificate.** `W n ≠ 0` for every `n`: the pair
    `(u, v)` is a fundamental system of the order-2 recurrence eq (23) at
    every window.  Induction with base `W 0 = −277/16 ≠ 0` and the step law
    `C2·W(n+1) = C0·W n` with `C0 (n) ≠ 0`.  Independent of any closed
    form. [PROVEN] -/
theorem caso_ne_zero : ∀ n, W n ≠ 0
  | 0 => by simp only [W_zero]; norm_num
  | (n + 1) => by
      intro hW1
      have hstep : C2 n * W (n + 1) = C0 n * W n := step_law n
      rw [hW1, mul_zero] at hstep
      have hCW : C0 n * W n = 0 := hstep.symm
      rcases mul_eq_zero.mp hCW with h | h
      · exact (C0_pos n).ne' h
      · exact (caso_ne_zero n) h

end Zeta4Caso

/-! ## Phase V — axiom-cone audit -/
#print axioms Zeta4Caso.C2_pos
#print axioms Zeta4Caso.C0_pos
#print axioms Zeta4Caso.rec_u
#print axioms Zeta4Caso.rec_v
#print axioms Zeta4Caso.step_law
#print axioms Zeta4Caso.caso_ne_zero
