/-
Trivial, Mathlib-free module. Builds instantly and independently of Mathlib so we
can confirm the project skeleton compiles before the (slow) first Mathlib build.
-/

namespace FingerprintCores

/-- A trivial definition so the module has non-empty content. -/
def hello : String := "fingerprint-cores skeleton OK"

end FingerprintCores
