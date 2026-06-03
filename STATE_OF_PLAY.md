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
partly an audit of the corpus that spawned it. CAUTION (process lesson): the S
value OSCILLATED VERIFIED -> DISPUTED -> VERIFIED across three turns. Each flip
was correct on what was known then, but the oscillation itself is the warning.
The DISPUTED downgrade rested on a phantom premise (a supposed v1.1 2pi
correction that a Zenodo-abstract check suggested did not exist). It is now
RESOLVED from-derivation: the deposited manuscript vquad_resurgence.pdf (located
in pnwork) IS v1.1 and DOES carry the correction (eq (13) + Remark 6.2), and the
2pi prefactor is forced by the standard Dingle-Berry-Howls late-term form
(companion of Gamma(n+beta) is the beta-independent 1/2pi*i) and confirmed by
applying eq (13) to the undisputed K (eq(13) -> 2*pi*K = 0.45790662...). S is
restored to VERIFIED (see OPEN ITEM 1). Lesson: a constant's status must rest on
a DERIVATION or from-definition computation, never on any document's stated
conclusion (mine, an abstract's, or even the manuscript's Remark 6.2) — those are
all just claims; what settled this was the formula structure plus the from-K
check. The re-verification discipline must apply to the TASK'S OWN ASSUMPTIONS,
not just to the data. Next substantive work: the deferred Thread B option-(b)
strengthening, the S Zenodo deposit-update push (OPEN ITEM 1), or pause.

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
  Stokes constant) prefactor dispute is RESOLVED from-derivation: correct value
  0.4579066231690176361190978425482258379624 under the 2pi real-Stokes-multiplier
  convention (S=2*pi*K), NOT the retracted Gamma-prefactor 0.43770528 (which is the
  Borel singular-amplitude C, not the Stokes multiplier). Restored to VERIFIED via
  patch_S_resolve_to_verified.py. See OPEN ITEMS for the residual deposit-update gap.
- xi0 d=3: Borel-radius identity xi0=d/beta_d^(1/d) — the beta_3 != 1 SCALE
  dimension verified at d=3 (the one piece untested; xi0 tracks 3/beta_3^(1/3)
  across beta_3 in {1,2,7}). NOTE: op:xi0-d3-direct was ALREADY closed by D2-NOTE
  v2.1 Thm 4.1 (general-d proof) and a prior 2026-05-02 sweep; this run only
  filled the untested scale dimension. Not a new op closure.

## OPEN ITEMS (carry forward — not yet resolved)

1. S value RESOLVED: 2pi correct, S=0.4579066231690176361190978425482258379624,
   restored to VERIFIED. The deposited manuscript vquad_resurgence.pdf (located in
   pnwork) IS v1.1 and carries the correction: eq (13) states the Dingle late-term
   formula with the 2pi prefactor, and Remark 6.2 explicitly retracts the v1.0
   0.43770528. The 2pi is forced by the standard Dingle-Berry-Howls-Ecalle form
   a_n ~ (S/2pi*i) Gamma(n+beta)/A^(n+beta) (companion of Gamma(n+beta) is the
   beta-independent 1/2pi*i) and confirmed by applying eq (13) to the undisputed
   K=0.0728781... (eq(13) -> 2*pi*K). The retracted 0.43770528 = |Gamma(beta_exp)|*K
   is a DIFFERENT quantity (the Borel singular-amplitude C), mislabeled as S in v1.0.
   RESIDUAL DEPOSIT-UPDATE GAP (actionable): the live Zenodo deposit (DOI
   10.5281/zenodo.20455090, latest version) was checked 2026-06-03 and showed v1.0 /
   0.43770528 with NO 2pi correction — the corrected v1.1 exists locally but appears
   NOT uploaded, so the published deposit the world sees likely still serves the
   retracted value. Fix = push the corrected manuscript to Zenodo (does NOT change
   the math). The phantom-premise warning stands as a process lesson (see One-line
   status). Full record: agent-tasks/C-S-prefactor-resolution-findings.md and
   pslq/constants/patch_S_resolve_to_verified.py.
2. Stale repo scripts (A2). pcf-research/vquad/scripts/{t2_iter20,22,23,24,
   jimbo_final} hardcode the retracted Gamma-prefactor S=0.43770528. Need the
   2pi fix or a KNOWN_ISSUE note. External to Fingerprint; operator's call.

3. M10 IndicialPoly stub -- CORPUS-INTERNAL, not a publication problem
   (CORRECTED 2026-06-03 by the M10 decision brief). Earlier framing treated this
   as a possible caveat on a DEPOSITED formalization claim. That is wrong: the
   deposited paper (vquad_resurgence_R2.tex, thm:exclusion2) claims a SYMBOLIC +
   NUMERICAL proof at dps=150 (verify_frobenius_apparent.py), which it has, and
   makes NO Lean / machine-checked / formally-verified claim. The stub
   (IndicialPoly := fun rho => rho^2, vacuous; committed proof has 2 sorrys and
   textually-but-redundantly invokes the Frobenius axiom) lives ONLY in the
   corpus-internal M10 status tracking ('Thm66 in Lean'), which is where the
   overstatement is. So: NO publication caveat needed -- this is internal-status
   cleanup, a much smaller thing than a published overstatement. Confirmed
   verbatim against the live file (branch vquad/handoff-2026-04-16, blob
   5b44e690). Full record: agent-tasks/B-M10-decision-brief.md (supersedes the
   harsher B-M10-stage0-findings.md framing).
4. M10 Lean core discoverability (unchanged). Thm66_ApparentSingularity.lean is
   on branch vquad/handoff-2026-04-16, NOT on main -- anyone cloning
   wallis-pcf-lean4 normally won't find the Lean core. Published but not
   discoverable; four neutral options (merge / pointer / leave / strengthen-first)
   in the decision brief. Operator's call.

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
