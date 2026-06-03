# Project Fingerprint — State of Play

*Durable snapshot of what exists, what's validated, and what comes next.*
*A fresh session starts from this map, not from git archaeology or chat history.*
*Update this file at the end of each working session.*

Last updated: after the xi0 d=3 beta-scale commit (HEAD 5f97ac4).

---

## One-line status

The three-pillar discovery factory is built, validated, and has now been run on
several real targets. All runs so far are in the verify/confirm/null register —
no novel finding yet. The highest-leverage unrun thread is **Thread B (Lean
conditional-core / M10)**, the only one that produces PROVEN.

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

## The next move

Thread B — Lean conditional-core / M10 (the PROVEN-producing thread).
Highest-leverage unrun work, deliberately NOT picked several times because it is
harder to start than a PSLQ run. It produces PROVEN (not verify/confirm/null),
directly strengthens already-deposited papers, and uses the most
thoroughly-validated capability (D1/C1 cone gate).

Concretely: take ONE specific conditional hypothesis from a deposited Lean core —
the even-quadratic paper's analytic hypothesis (convergence/exact-error input
"not available in current Mathlib"), or an M10 sorry from the wallis-pcf-lean4
repo — and either DISCHARGE it (if Mathlib has since gained the needed lemma) or
TIGHTEN it (reduce precisely what it assumes, document what remains conditional).
Cone-gated either way: "discharged, now unconditional, cone clean" or "still
conditional on H, but H now narrower/precisely stated."

First step: locate the specific sorry / hypothesis in a deposited repo, confirm
the pinned Lean+Mathlib version, scope the single hypothesis to attack.

Lower-priority alternatives: R-constants Trans-stratum sweep (more PSLQ nulls,
low leverage); hosted-model decision to unlock OpenEvolve discovery (spend call).

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
