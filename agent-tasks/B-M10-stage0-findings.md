# Thread B (M10) — Stage 0 + retrieval investigation: FINDINGS

> Audit-trail record of the M10 locate/retrieve investigation. No Lean was
> authored; no port was performed. The deliverable of this thread (so far) is the
> investigation itself and the three provenance/substance findings below. The
> Stage-1 port is deliberately DEFERRED as separate, fresh-start work (see
> "Decision deferred").

Status: investigation complete, port NOT done (by operator decision).
Branch/commit context: Fingerprint HEAD e5b1025 at time of investigation.

---

## What M10 is

A Lean-4 formalization/sorry-discharge axis (NOT new mathematics). The math is
closed under other axes; "M10" = the tooling-state claim "Lean build green,
sorries discharged." Target: Theorem 6.6 (apparent singularity) for the Wallis
family. Lives in `papanokechi/wallis-pcf-lean4`,
`lean/Thm66_ApparentSingularity.lean`.

## Retrieval status (RESOLVED — case 1, file is on the remote)

- The file IS on the remote, on branch **`vquad/handoff-2026-04-16`** (155 lines),
  NOT on `main` (main's `lean/` has only WallisFamily.lean, lakefile.lean,
  lean-toolchain).
- Self-contained: imports are Mathlib-only; `IndicialPoly` and all
  coefficients/roots are defined in-file. Needs none of the named siblings
  (WallisFamily, ShiftConsistency, CasoratianPi4, proof_targets, LemmaK,
  CardEvenOfInvolution) — confirmed a dependency-graph leaf. Retrieval scope =
  this single file.
- Version: the committed branch pins `leanprover/lean4:stable` + UNPINNED mathlib
  HEAD. Fingerprint pins v4.29.0 + mathlib 8a178386. A port would re-pin backward
  to v4.29.0 and fix API drift.

## THE THREE FINDINGS (the real deliverable)

### Finding 1 — IndicialPoly is a STUB; the central theorem is vacuous
`IndicialPoly (a : C->C) (s : C) := fun rho => rho^2` (line 86) **ignores both
arguments** — it returns rho^2 unconditionally. Therefore
`apparent_singularity_thm_i` is definitionally `<rfl, rfl>`, and the Frobenius
axiom is **decorative at the use site**: the theorem does not consume it. The
formalization does NOT yet encode the mathematical content (that THIS ODE's
indicial polynomial genuinely is rho^2). A clean axiom cone on this file would be
PROVEN-but-VACUOUS — the cone certifies "no gaps in the proof," NOT "the
statement is non-trivial." This is an edge case of the PROVEN=clean-cone
convention: a stub can have a perfectly clean cone.

Implication for the deposited paper: the published "Thm 6.6 formalized in Lean"
claim, read naturally, suggests the content was machine-verified. As written, it
is not — it is a tautology with an unused axiom. This may warrant a caveat on the
deposited formalization claim (a corpus-governance call for the operator).

### Finding 2 — the Lean core lives only on a handoff branch, not main
`Thm66_ApparentSingularity.lean` is on `vquad/handoff-2026-04-16`, not on `main`.
It is published (not lost — no durability emergency), but it is not on the default
branch, so anyone cloning `wallis-pcf-lean4` normally would not find the Lean core
backing the deposited Thm 6.6. A discoverability/provenance gap on a deposited
artifact.

### Finding 3 — the file carries TWO genuine analytic-gap axioms, not one
Beyond `frobenius_double_root_at_apparent_singularity` (Frobenius ODE theory),
the file also has `monodromy_unipotent_from_double_root` (monodromy of linear
ODE) — both genuine mathlib_gaps. Plus four "routine" axioms
(root_s1/s2, a_deriv_s1/s2_ne_zero) that are computation-dischargeable. The
earlier characterization as "one conditional hypothesis H" was incomplete.

## Decision deferred (operator)

The Stage-1 port is NOT a faithful as-is copy (which would carry the vacuous stub
into Fingerprint, well-labelled but low-value). The valuable response is to make
`IndicialPoly` actually COMPUTE the indicial polynomial from the ODE coefficients,
so the Frobenius axiom becomes load-bearing and the theorem encodes real content
(option b — a genuine conditional-core strengthening). That is substantive Lean
formalization work requiring the ODE's actual indicial-polynomial definition
located from the paper (NOT reconstructed), and is deferred to a fresh session as
its own scoped task. Logged, not abandoned.

## Could-not-confirm
- The exact mathematical indicial-polynomial definition for the Wallis ODE (would
  be needed for option b; not yet located from the paper).
- Whether the four "routine" axioms are as trivially dischargeable as the corpus
  claims (not attempted).
