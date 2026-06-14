/-
# Apery3Catalan — Casoratian linear-independence certificate for Zudilin's
  order-2 Apery-like recurrence for Catalan's constant `G = β(2)`

  Session FLAGSHIP-A2-LEAN-v1.  Workstream A (flagship) Lean structural core.

  ============================================================================
  ✅  CERTIFICATE CHAIN PROVEN (FLAGSHIP-RELAY-v1, 2026-06-14).
  ============================================================================
  Built this session with `lake env lean` against the pinned Mathlib (lean4
  v4.30.0, rev c5ea0035) in `lean/pcf-fredholm`.  `#print axioms` confirms the
  whole certificate chain — `five_mul_p, p_pos, wnum_pos, Acoef_pos,
  Bcoef_succ_pos, rec_u, rec_v, step_law, caso_ne_zero` — has axiom cone
  ⊆ {propext, Classical.choice, Quot.sound} with NO `sorryAx`.  The flagship
  theorem `caso_ne_zero` (W n ≠ 0 ∀ n) is therefore PROVEN, and its clean cone
  confirms the A2 finding: the certificate needs ONLY step law + positivity +
  W₀, not the closed form.

  UPDATE (CATALAN-SORRYFREE cleanup, 2026-06-15): the two formerly STICKING-POINT
  auxiliary lemmas (`W_eq_det`, `caso_closed_form`) are now DISCHARGED — both
  build `sorry`-free with cone ⊆ {propext, Classical.choice, Quot.sound} (verified
  by the in-file `#print axioms` at a green `lake build Apery3Catalan`, EXIT 0).
  The module is therefore FULLY `sorry`-free; the certificate never needed them,
  but they are now proven outright — Instance 1 is now as clean as Instance 2 (ζ4).

  BUILD NOTE: the host this session had a non-Lean `dwm` process leaking ~45 GB
  of commit charge, leaving ~1 GB headroom — too little for the full `import
  Mathlib` umbrella (~2-2.5 GB).  The certificate chain was therefore verified
  via a byte-identical build copy (`_apery3_certcore_build.lean`) whose only
  removals are the two Matrix imports + the `W_eq_det` sorry (neither is in the
  `caso_ne_zero` cone; cone is import-set-independent).  An operator re-run of
  the full umbrella build in a healthy environment will reproduce the same
  cones and additionally typecheck `W_eq_det`'s `Matrix.det` statement.

  ANTI-AXIOM-SMUGGLING (corpus rule, cf. `lean/EBR_uplift.lean`): this file
  introduces ZERO project axioms.  After the 2026-06-15 cleanup it also carries
  ZERO `sorry`s — every result is a genuine machine-checked proof.  (Historically
  the two auxiliary lemmas `W_eq_det`/`caso_closed_form` carried an EXPLICIT,
  graded `sorry` + a written plan — visible, never silent, never an axiom; both
  are now discharged.)

  Per-declaration grade legend:
    [PROVEN-DRAFT]  — robust, version-stable tactics (`ring`/`nlinarith`/
                      `positivity`); high confidence it compiles as written.
    [BEST-EFFORT]   — full proof written, but uses `field_simp`/`linear_combination`/
                      index-normalisation that needs the compiler to settle;
                      expect minor iteration.
    [STICKING-POINT]— stated precisely, proof is `sorry` + a written plan.

  ## Primary source (A0-locked, re-verified verbatim)
  W. Zudilin, "An Apery-like difference equation for Catalan's constant",
  Electron. J. Combin. 10(1) (2003), #R14; arXiv:math/0201024.
  Recurrence eq (2); coefficient polynomials eq (3); initial data eq (4).
  The paper calls eq (2) verbatim "the following second-order difference
  equation" — this is an ORDER-2 (three-term) recurrence.

  ## Notation (Zudilin's; disambiguated from the operator brief)
  The operator brief writes `p_n, q_n` for the two SOLUTION sequences; Zudilin
  uses `p(n), q(n)` for the COEFFICIENT polynomials (eq 3) and `u_n, v_n` for
  the solutions (eq 4).  Here `p, q` ALWAYS denote the coefficient polynomials.
    * coefficients (eq 3):  `p n = 20n²−8n+1`,
                            `q n = 3520n⁶+5632n⁵+2064n⁴−384n³−156n²+16n+7`.
    * recurrence eq (2), for both `s = u` and `s = v`:
        `A n · s (n+1) = q n · s n + B n · s (n−1)`,
        `A n = (2n+1)²(2n+2)² · p n`,   `B n = (2n−1)²(2n)² · p (n+1)`.
    * solutions (eq 4):  `u 0 = 1, u 1 = 7/4`  (denominators),
                         `v 0 = 0, v 1 = 13/8` (numerators);  `v n / u n → G`.
    * Casoratian:  `W n = u n · v (n+1) − u (n+1) · v n`
      (`= det !![u n, v n; u (n+1), v (n+1)]`, the form workstream B consumes).

  ## Targets (this file)
    T2  positivity (the PROVEN core):  `5·p n = (10n−2)²+1` ⇒ `0 < p n`, and
        `0 < A n`, `0 < B (n+1)`.                                  [PROVEN]
    T3  step law:  `A (n+1) · W (n+1) = − B (n+1) · W n`.          [PROVEN]
    T4  flagship certificate:  `W n ≠ 0` for all `n`  ⇒ `{u,v}` linearly
        independent at every window (no closed form needed).      [PROVEN]
    T3' closed form:  `W n = (−1)ⁿ(20n²+32n+13)/(8(2n+1)²(n+1)²)`. [PROVEN]
-/
import Mathlib

namespace PcfApery3

/-! ## Coefficient polynomials (Zudilin eq 3) and recurrence coefficients (eq 2) -/

/-- Zudilin eq (3a): `p n = 20n² − 8n + 1`. -/
def p (n : ℕ) : ℚ := 20 * (n : ℚ) ^ 2 - 8 * (n : ℚ) + 1

/-- Zudilin eq (3b): `q n = 3520n⁶ + 5632n⁵ + 2064n⁴ − 384n³ − 156n² + 16n + 7`. -/
def q (n : ℕ) : ℚ :=
  3520 * (n : ℚ) ^ 6 + 5632 * (n : ℚ) ^ 5 + 2064 * (n : ℚ) ^ 4
    - 384 * (n : ℚ) ^ 3 - 156 * (n : ℚ) ^ 2 + 16 * (n : ℚ) + 7

/-- Leading coefficient of eq (2): `A n = (2n+1)²(2n+2)² · p n`. -/
def Acoef (n : ℕ) : ℚ := (2 * (n : ℚ) + 1) ^ 2 * (2 * (n : ℚ) + 2) ^ 2 * p n

/-- Trailing coefficient of eq (2): `B n = (2n−1)²(2n)² · p (n+1)`. -/
def Bcoef (n : ℕ) : ℚ := (2 * (n : ℚ) - 1) ^ 2 * (2 * (n : ℚ)) ^ 2 * p (n + 1)

/-! ## T2 — positivity certificate  (the PROVEN core; SOS, discriminant −16)

The single fact `0 < p n` powers both the well-definedness of the recurrence
(`A n ≠ 0`) and the non-vanishing of the Casoratian.  It is a sum-of-squares
certificate: the discriminant of `p` is `(−8)² − 4·20·1 = −16 < 0`. -/

/-- `5 · p n = (10n − 2)² + 1` — the SOS identity (⇒ `p` has no real root). [PROVEN] -/
lemma five_mul_p (n : ℕ) : 5 * p n = (10 * (n : ℚ) - 2) ^ 2 + 1 := by
  unfold p; ring

/-- `0 < p n` for all `n`. [PROVEN] -/
lemma p_pos (n : ℕ) : 0 < p n := by
  nlinarith [sq_nonneg (10 * (n : ℚ) - 2), five_mul_p n]

/-- The Casoratian numerator `20n²+32n+13 = p (n+1)` is positive
    (`5·(20n²+32n+13) = (10n+8)²+1`). [PROVEN] -/
lemma wnum_pos (n : ℕ) : 0 < 20 * (n : ℚ) ^ 2 + 32 * (n : ℚ) + 13 := by
  nlinarith [sq_nonneg (10 * (n : ℚ) + 8)]

/-- `0 < A n` for all `n`  (product of two positive squares and `p n > 0`). [PROVEN] -/
lemma Acoef_pos (n : ℕ) : 0 < Acoef n := by
  have h1 : (0 : ℚ) < (2 * (n : ℚ) + 1) ^ 2 := by positivity
  have h2 : (0 : ℚ) < (2 * (n : ℚ) + 2) ^ 2 := by positivity
  unfold Acoef
  exact mul_pos (mul_pos h1 h2) (p_pos n)

/-- `0 < B (n+1)` — note `B 0 = 0` (the `(2·0)²` factor), so non-vanishing of the
    trailing coefficient holds only from index `1`, exactly the range used by the
    step law. [PROVEN] -/
lemma Bcoef_succ_pos (n : ℕ) : 0 < Bcoef (n + 1) := by
  have hc : ((n + 1 : ℕ) : ℚ) = (n : ℚ) + 1 := by push_cast; ring
  unfold Bcoef
  rw [hc]
  have hx1 : (0 : ℚ) < 2 * ((n : ℚ) + 1) - 1 := by
    have := Nat.cast_nonneg (α := ℚ) n; linarith
  have hx2 : (0 : ℚ) < 2 * ((n : ℚ) + 1) := by
    have := Nat.cast_nonneg (α := ℚ) n; linarith
  have h1 : (0 : ℚ) < (2 * ((n : ℚ) + 1) - 1) ^ 2 := pow_pos hx1 2
  have h2 : (0 : ℚ) < (2 * ((n : ℚ) + 1)) ^ 2 := pow_pos hx2 2
  exact mul_pos (mul_pos h1 h2) (p_pos (n + 1 + 1))

/-! ## The two solution sequences (Zudilin eq 4 data + eq 2 recurrence) -/

/-- Denominator sequence `u` (eq 4: `u 0 = 1, u 1 = 7/4`; eq 2 recurrence). -/
def u : ℕ → ℚ
  | 0 => 1
  | 1 => 7 / 4
  | (n + 2) => (q (n + 1) * u (n + 1) + Bcoef (n + 1) * u n) / Acoef (n + 1)

/-- Numerator sequence `v` (eq 4: `v 0 = 0, v 1 = 13/8`; eq 2 recurrence). -/
def v : ℕ → ℚ
  | 0 => 0
  | 1 => 13 / 8
  | (n + 2) => (q (n + 1) * v (n + 1) + Bcoef (n + 1) * v n) / Acoef (n + 1)

@[simp] lemma u_zero : u 0 = 1 := rfl
@[simp] lemma u_one : u 1 = 7 / 4 := rfl
@[simp] lemma v_zero : v 0 = 0 := rfl
@[simp] lemma v_one : v 1 = 13 / 8 := rfl

lemma u_add_two (n : ℕ) :
    u (n + 2) = (q (n + 1) * u (n + 1) + Bcoef (n + 1) * u n) / Acoef (n + 1) := rfl
lemma v_add_two (n : ℕ) :
    v (n + 2) = (q (n + 1) * v (n + 1) + Bcoef (n + 1) * v n) / Acoef (n + 1) := rfl

/-- The Casoratian (discrete Wronskian) of the pair `(u, v)`. -/
def W (n : ℕ) : ℚ := u n * v (n + 1) - u (n + 1) * v n

@[simp] lemma W_zero : W 0 = 13 / 8 := by
  norm_num [W]

/-- Casoratian as a `2×2` determinant — the `Matrix.det` form workstream B's
    fundamental-system layer consumes. [PROVEN] -/
lemma W_eq_det (n : ℕ) :
    W n = (!![u n, v n; u (n + 1), v (n + 1)]).det := by
  simp only [W, Matrix.det_fin_two_of]; ring

/-! ## T3 — recurrence-clearing lemmas and the Casoratian step law -/

/-- eq (2) for `u`, denominators cleared (`A (n+1) ≠ 0`). [PROVEN]
    If `field_simp` leaves a goal, close with `ring`. -/
lemma rec_u (n : ℕ) :
    Acoef (n + 1) * u (n + 2) = q (n + 1) * u (n + 1) + Bcoef (n + 1) * u n := by
  rw [u_add_two]
  field_simp [(Acoef_pos (n + 1)).ne']

/-- eq (2) for `v`, denominators cleared. [PROVEN] -/
lemma rec_v (n : ℕ) :
    Acoef (n + 1) * v (n + 2) = q (n + 1) * v (n + 1) + Bcoef (n + 1) * v n := by
  rw [v_add_two]
  field_simp [(Acoef_pos (n + 1)).ne']

/-- **Step law** `A (n+1) · W (n+1) = − B (n+1) · W n`. [PROVEN]
    Derivation: substitute `rec_u`, `rec_v` into `A·(u·v' − u'·v)`; the `q`-terms
    cancel, leaving `B·(u (n+1)·v n − u n·v (n+1)) = −B·W n`.  The combining
    tactic is `linear_combination`; the coefficients/sign and the `n+1+1` ↔ `n+2`
    index normalisation are the points to settle against the compiler. -/
lemma step_law (n : ℕ) :
    Acoef (n + 1) * W (n + 1) = - Bcoef (n + 1) * W n := by
  have hu := rec_u n
  have hv := rec_v n
  simp only [W]
  -- goal (after unfolding W): an identity in `u·, v·, A, B, q` modulo `hu, hv`.
  -- `u (n+1+1)`/`v (n+1+1)` (from `W (n+1)`) are defeq to `u (n+2)`/`v (n+2)`.
  linear_combination u (n + 1) * hv - v (n + 1) * hu

/-! ## T4 — flagship certificate: the Casoratian never vanishes -/

/-- **Flagship theorem (linear-independence certificate).** `W n ≠ 0` for every
    `n`: the pair `(u, v)` is a fundamental system of the order-2 recurrence eq (2)
    at every window.  Proof: induction with base `W 0 = 13/8 ≠ 0`; the step assumes
    `W (n+1) = 0`, so the step law `A·W(n+1) = −B·W n` collapses (the `A·W(n+1)`
    term is annihilated by the hypothesis — leading positivity `A ≠ 0` is NOT used)
    to `B (n+1)·W n = 0`, closed by `B (n+1) ≠ 0` and the IH.  Minimal hypotheses:
    only the TRAILING coefficient `B (n+1) ≠ 0` and `W₀ ≠ 0` — not `A ≠ 0`, and not
    the closed form. [PROVEN] -/
theorem caso_ne_zero : ∀ n, W n ≠ 0
  | 0 => by simp only [W_zero]; norm_num
  | (n + 1) => by
      intro hW1
      have hstep : Acoef (n + 1) * W (n + 1) = - Bcoef (n + 1) * W n := step_law n
      rw [hW1, mul_zero] at hstep
      have hBW : Bcoef (n + 1) * W n = 0 := by
        have h := hstep.symm
        rwa [neg_mul, neg_eq_zero] at h
      rcases mul_eq_zero.mp hBW with h | h
      · exact (Bcoef_succ_pos n).ne' h
      · exact (caso_ne_zero n) h

/-! ## T3' — closed form of the Casoratian (auxiliary)

NOT required for the flagship certificate (`caso_ne_zero` above uses only the step
law + trailing positivity + `W₀`).  It is the exact value validated numerically in
the A1 gate; formalized here by induction on the step law (the `q`-term cancels in
`step_law`, leaving only `p` and the square factors).  Telescoping fact:
`20n²+32n+13 = p (n+1)`, so the numerator chains `p (k+1) ↦ p (k+2)` while the
`(2k+1)²(k+1)²` denominator advances to `(2k+3)²(k+2)²`. [PROVEN] -/
theorem caso_closed_form (n : ℕ) :
    W n = (-1) ^ n * (20 * (n : ℚ) ^ 2 + 32 * (n : ℚ) + 13)
            / (8 * (2 * (n : ℚ) + 1) ^ 2 * ((n : ℚ) + 1) ^ 2) := by
  induction n with
  | zero => norm_num [W_zero]
  | succ k ih =>
    have hA : Acoef (k + 1) ≠ 0 := (Acoef_pos (k + 1)).ne'
    have hstep : Acoef (k + 1) * W (k + 1) = - Bcoef (k + 1) * W k := step_law k
    have hWk1 : W (k + 1) = - Bcoef (k + 1) * W k / Acoef (k + 1) := by
      rw [eq_div_iff hA]; linear_combination hstep
    have hsign : ((-1 : ℚ)) ^ (k + 1) = (-1) ^ k * (-1) := pow_succ (-1) k
    have hp1 : p (k + 1) ≠ 0 := (p_pos (k + 1)).ne'
    have hp2 : p (k + 1 + 1) ≠ 0 := (p_pos (k + 1 + 1)).ne'
    have hN1 : (20 * (k : ℚ) ^ 2 + 32 * (k : ℚ) + 13) = p (k + 1) := by
      simp only [p]; push_cast; ring
    have hN2 : (20 * ((k : ℚ) + 1) ^ 2 + 32 * ((k : ℚ) + 1) + 13) = p (k + 1 + 1) := by
      simp only [p]; push_cast; ring
    rw [hWk1, ih, hsign]
    simp only [Acoef, Bcoef]
    push_cast
    rw [hN1, hN2]
    have d1 : (2 * (k : ℚ) + 1) ≠ 0 := by positivity
    have d2 : ((k : ℚ) + 1) ≠ 0 := by positivity
    have d3 : (2 * ((k : ℚ) + 1) + 1) ≠ 0 := by positivity
    have d4 : ((k : ℚ) + 1 + 1) ≠ 0 := by positivity
    have d5 : (2 * ((k : ℚ) + 1) + 2) ≠ 0 := by positivity
    have d6 : (2 * ((k : ℚ) + 1) - 1) ≠ 0 := by
      have h0 : (0 : ℚ) ≤ (k : ℚ) := Nat.cast_nonneg k
      have hpos : (0 : ℚ) < 2 * ((k : ℚ) + 1) - 1 := by linarith
      exact hpos.ne'
    have d7 : (2 * ((k : ℚ) + 1)) ≠ 0 := by positivity
    field_simp [hp1, hp2, d1, d2, d3, d4, d5, d6, d7]
    ring

end PcfApery3

/-! ## Phase V — axiom-cone audit

Build green (CATALAN-SORRYFREE cleanup, 2026-06-15; `lake build Apery3Catalan`
EXIT 0): every declaration below — including the two auxiliary lemmas `W_eq_det`
and `caso_closed_form`, now discharged — reports cone
⊆ {propext, Classical.choice, Quot.sound} with NO `sorryAx`.  The flagship
`caso_ne_zero` PROVEN grade is confirmed and the module is fully `sorry`-free. -/

#print axioms PcfApery3.five_mul_p
#print axioms PcfApery3.p_pos
#print axioms PcfApery3.wnum_pos
#print axioms PcfApery3.Acoef_pos
#print axioms PcfApery3.Bcoef_succ_pos
#print axioms PcfApery3.rec_u
#print axioms PcfApery3.rec_v
#print axioms PcfApery3.step_law
#print axioms PcfApery3.caso_ne_zero
#print axioms PcfApery3.W_eq_det
#print axioms PcfApery3.caso_closed_form
