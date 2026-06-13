import Cc4Cores

/-! Axiom-cone audit for the cc4-3 Lean cores. PROVEN requires every cone to be
    ⊆ {propext, Classical.choice, Quot.sound} with no `sorryAx`. -/

-- Core 1 (cc4-0b bounds)
#print axioms Cc4Cores.Bound.B2_eq
#print axioms Cc4Cores.Bound.B1_eq
#print axioms Cc4Cores.Bound.bounds_le_twenty

-- Core 2 (A2 pullback exponents)
#print axioms Cc4Cores.Pullback.pulled_values
#print axioms Cc4Cores.Pullback.pulled_all_integral

-- Core 3 (A1 eigenvalue parity)
#print axioms Cc4Cores.Parity.angles0_neg_closed
#print axioms Cc4Cores.Parity.anglesR_not_neg_closed

-- Core 4 (A1b 4-cycle is odd ⇒ outside A₄)
#print axioms Cc4Cores.FourCycle.c4_sign
#print axioms Cc4Cores.FourCycle.c4_not_mem_alternating
