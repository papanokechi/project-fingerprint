# Project Fingerprint — State of Play

*Durable snapshot of what exists, what's validated, and what comes next.*
*A fresh session starts from this map, not from git archaeology or chat history.*
*Update this file at the end of each working session.*

Last updated: after Thread B (M10) Stage 0 investigation (HEAD e5b1025 + this commit).

---

## One-line status

The three-pillar discovery factory is built, validated, and has now been run on
several real targets. All runs so far are in the verify/confirm/null register —
no novel finding yet. NOTABLE PATTERN: the re-verification discipline keeps
surfacing provenance/substance gaps in the SURROUNDING deposited corpus (the S
correction, the M10 Lean core, the IndicialPoly stub) — Fingerprint has become
partly an audit of the corpus that spawned it. Next substantive work: the
deferred Thread B option-(b) strengthening (make M10's IndicialPoly load-bearing),
or pause.

---

## The three pillars (each gated by a machine the model can't bluff past)

| Pillar | Tool | Output class | Gate |
|--------|------|-------------|------|
| Search (evolutionary) | OpenEvolve + local 7B | VERIFIED witness | independent evaluator confirms a valid configuration |
| Integer relations | PSLQ (mpmath) | CONJECTURED relation | survives high-precision re-test above the Bailey floor |
| Formal proof | Lean 4 + Mathlib | PROVEN theorem | #print axioms subset {propext, Classical.choice, Quot.sound}, no sorryAx |

Pillars chain: PSLQ CONJECTURED -> Lean PROVEN, validated end-to-end on Basel
zeta(2)=pi^2/6 (Task D1).

## Host constraints (shape every decision)

CPU-only, 16 GB, no usable GPU. Local model capped at ~7B (qwen2.5-coder:7b via
Ollama). Consequence: OpenEvolve search pillar is shakedown-only locally (7B too
weak to mutate code for discovery; real search-pillar discovery needs a hosted
model — a spend+principle decision not yet made). PSLQ and Lean pillars run at
full strength locally (deterministic engines; the model only proposes/assists).

---

## What is built and validated (committed + pushed; HEAD 5f97ac4)

Repo: github.com/papanokechi/project-fingerprint (private). Working tree
C:\LocalWork\project-fingerprint (local, non-OneDrive). Commit arc:
day-one infra -> circle-packing (01-03) -> cap-sets (04) -> PSLQ/B1 -> Lean/C1 ->
D1 pillar-chain -> STATE_OF_PLAY -> basis re-verification -> R1 null -> task
specs (A1/A2) -> xi0 d=3 beta-scale.

Pillars: OpenEvolve validated across two shakedown domains (circle-packing n=26,
cap-sets AG(n,3) with adversarial-tested evaluator). PSLQ harness B1 validated on
all four outcome types (true relation accepted, phantom rejected, Machin
rediscovered, Catalan null) + an L-coefficient phantom filter (validated against
the zeta(2)=pi^2/6 phantom). Lean C1 validated with the sorryAx control gate
firing. D1 chain (PSLQ->Lean) validated on Basel.

Research runs completed (all verify/confirm/null register):
- R1 (degree-(4,2) Trans-stratum constant, -0.10123520...): recomputed from its
  defining PCF family (a_n=n^4-n^2-n-1, b_n=-n^2+n-1) to 300+ digits; 6-basis
  PSLQ null to 165 effective digits, L-filter active. R1 remains unidentified
  against {pi,zeta3,Catalan,log2,gamma} + low-order products.
- Basis re-verification: 10/10 constants VERIFIED from definition. The S (V_quad
  Stokes constant) prefactor discrepancy resolved: correct value
  0.45790662316901763611... under the 2pi resurgence convention (NOT the
  retracted Gamma-prefactor 0.43770528). See OPEN ITEMS.
- xi0 d=3: Borel-radius identity xi0=d/beta_d^(1/d) — the beta_3 != 1 SCALE
  dimension verified at d=3 (the one piece untested; xi0 tracks 3/beta_3^(1/3)
  across beta_3 in {1,2,7}). NOTE: op:xi0-d3-direct was ALREADY closed by D2-NOTE
  v2.1 Thm 4.1 (general-d proof) and a prior 2026-05-02 sweep; this run only
  filled the untested scale dimension. Not a new op closure.

## OPEN ITEMS (carry forward — not yet resolved)

1. S published-provenance (UNRESOLVED — operator action). The canonical S VALUE
   is computationally verified (two independent recomputes, 46 digits). But the
   v1.1 correction (2pi prefactor, 0.45790662...) was NOT located in deposit
   artifacts — the deposited manuscript PDF found is the v1.0/Gamma version (8
   digits, "unidentified"). ACTION: check the LIVE Zenodo record (DOI
   10.5281/zenodo.20455090) — does the latest version carry 0.45790662
   (corrected, benign access gap) or still 0.43770528 (a real publication
   correction to push)? Until resolved, S is usable computationally but NOT
   citation-ready.
2. Stale repo scripts (A2). pcf-research/vquad/scripts/{t2_iter20,22,23,24,
   jimbo_final} hardcode the retracted Gamma-prefactor S=0.43770528. Need the
   2pi fix or a KNOWN_ISSUE note. External to Fingerprint; operator's call.

3. M10 Lean core — IndicialPoly is a STUB (substance gap). In
   wallis-pcf-lean4 (branch vquad/handoff-2026-04-16), Thm66_ApparentSingularity
   .lean defines IndicialPoly := fun rho => rho^2 ignoring its arguments, so the
   central theorem is definitionally true (a tautology) and the Frobenius axiom is
   UNUSED. The deposited "Thm 6.6 formalized in Lean" claim does NOT yet encode
   its mathematical content. A clean cone here would be PROVEN-but-VACUOUS. May
   warrant a caveat on the deposited formalization claim (operator/governance
   call). Full investigation: agent-tasks/B-M10-stage0-findings.md.
4. M10 Lean core discoverability. The file is on branch vquad/handoff-2026-04-16,
   NOT on main — anyone cloning wallis-pcf-lean4 normally won't find the Lean core
   backing the deposited Thm 6.6. Published but not discoverable. Operator's call.

## The next move

Thread B investigated (Stage 0 done): M10 located, retrievable, but the central
formalization is a STUB (see OPEN ITEM 3). The valuable next step is the
DEFERRED option-(b) strengthening: port Thm66 into FingerprintCores AND rewrite
IndicialPoly to actually COMPUTE the indicial polynomial from the ODE
coefficients, so the Frobenius axiom becomes load-bearing and the theorem encodes
real content -> a GENUINE PROVEN-conditional-on-H result. This needs the ODE's
actual indicial-polynomial definition located from the paper (NOT reconstructed),
and is substantive Lean work best done fresh, not at the tail of a long session.

Alternatives: resolve the OPEN ITEMS (S Zenodo check, the two M10 corpus gaps) as
a corpus-governance pass; R-constants Trans-stratum sweep (low leverage); the
hosted-model decision to unlock OpenEvolve discovery (spend call).

HONEST NOTE: three threads of verify/confirm/null plus a Thread-B investigation
that found a stub means the session's net NEW mathematics is ~0 — but its net
findings about the corpus (one stale published value, one mis-branched core, one
vacuous formalization) are real and arguably more valuable than another clean
cone. Worth weighing whether the next session is more discovery or more
corpus-governance/cleanup.

## Operating reminders

- Label set by machine gate, never confidence. PROVEN = clean cone, not green
  build.
- No Mathlib lemma names / constant values / citations from memory — recompute or
  #check in-project. (Basis re-verification caught a stale published value this
  way.)
- Locate, don't reconstruct — especially for proof/computation tasks where a
  reconstructed setup makes the result circular.
- Null / confirmation / "could not confirm" are complete successful answers.
- Commit + push same session; remote is the durable state. Update THIS file at
  session end so state never lives only in chat.
- Beware the easy-to-start thread crowding out the higher-leverage hard one (the
  verify/confirm/null runs have outnumbered the find/prove ones; Thread B
  interrupts that).
