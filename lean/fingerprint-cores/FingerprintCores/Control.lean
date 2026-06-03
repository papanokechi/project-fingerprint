/-
ADVERSARIAL NEGATIVE CONTROL (gate self-test).

`control_sorry` states a TRUE proposition (2 + 2 = 4) but discharges it with
`sorry`. Its only purpose is to confirm that the axiom-cone gate catches an
incomplete proof: `#print axioms control_sorry` MUST report `sorryAx`.

This declaration is the DELIBERATE negative control. It is NOT proven and must
never be labelled PROVEN — a `sorryAx` in the cone is the gate working.
-/

namespace FingerprintCores.Control

theorem control_sorry : 2 + 2 = 4 := by
  sorry

#print axioms control_sorry

end FingerprintCores.Control
