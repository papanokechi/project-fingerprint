# Thread B (M10) — DECISION BRIEF for the operator

> Purpose: gather the confirmed facts the operator needs to make TWO decisions.
> This task took NO actions — no commits, no edits to `wallis-pcf-lean4`, no Lean
> authoring. Both decisions below are explicitly the operator's, laid out neutrally.
>
> Evidence base (live remote, read at investigation time):
> - `papanokechi/wallis-pcf-lean4` main `3af07fc`, branch `vquad/handoff-2026-04-16` `83f3ade`
>   (Lean file blob `5b44e690`).
> - `papanokechi/siarc-relay-bridge` main (deposited math paper + corpus audit).

---

## DECISION 1 — Should the "Thm 6.6 formalized in Lean" claim be caveated?

### 1a. The Lean stub — CONFIRMED verbatim against the real file

File: `lean/Thm66_ApparentSingularity.lean` on `vquad/handoff-2026-04-16` (155 lines,
blob `5b44e690`). Confirmed against the actual remote file, not the bridge notes.

**The `IndicialPoly` definition (line 86) ignores both arguments:**
```lean
def IndicialPoly (a : ℂ → ℂ) (s : ℂ) : ℂ → ℂ := fun ρ => ρ ^ 2
```
It returns `fun ρ => ρ^2` unconditionally — neither `a` (the ODE coefficient) nor
`s` (the singular point) is used. So `IndicialPoly` carries none of the ODE's
mathematical content.

**The central theorem (lines 112–120):**
```lean
theorem apparent_singularity_thm_i :
    (IndicialPoly a_coeff_c s₁ = fun ρ => ρ ^ 2) ∧
    (IndicialPoly a_coeff_c s₂ = fun ρ => ρ ^ 2) := by
  constructor
  · exact frobenius_double_root_at_apparent_singularity
      a_coeff_c c_coeff_c s₁ root_s1 a_deriv_s1_ne_zero (by sorry)
  · exact frobenius_double_root_at_apparent_singularity
      a_coeff_c c_coeff_c s₂ root_s2 a_deriv_s2_ne_zero (by sorry)
```
Because `IndicialPoly a_coeff_c s₁` reduces definitionally to `fun ρ => ρ^2`, each
conjunct's goal is literally `(fun ρ => ρ^2) = (fun ρ => ρ^2)`. The statement is a
**tautology**: it could be closed by `⟨rfl, rfl⟩`. This is the substance gap — the
theorem does NOT encode the real claim (that THIS ODE's indicial polynomial is `ρ²`);
it asserts that a constant function equals itself.

**Two precise corrections to the Stage-0 write-up** (both matter for the decision):
1. Stage-0 said the Frobenius axiom is "unused / the theorem does not consume it."
   Imprecise. The proof term **does** textually invoke
   `frobenius_double_root_at_apparent_singularity` (lines 117–120). The axiom is
   **logically redundant** (the goal is true by `rfl`, so the axiom is not needed),
   but it is not textually absent.
2. Stage-0 said a clean cone here "would be PROVEN-but-VACUOUS." As **committed**,
   the proof is NOT clean: it contains **two `sorry`s** (the `h_exact` argument at
   lines 118 and 120). So `#print axioms apparent_singularity_thm_i` would report
   `sorryAx` (plus the Frobenius axiom and `root_s1/s2`, `a_deriv_s1/s2_ne_zero`).
   The theorem is therefore **vacuous AND sorry-blocked** — not a clean-cone PROVEN.
   (Vacuity is real: it is `rfl`-provable. The point is the committed text is not
   even a closed proof.)

Net: the **substance gap is confirmed and is in fact slightly worse** than Stage-0
stated — the as-written formalization is both vacuous (stub statement) and not
closed (2 sorries).

The file also carries two genuine analytic-gap axioms
(`frobenius_double_root_at_apparent_singularity`,
`monodromy_unipotent_from_double_root`) plus four routine axioms
(`root_s1/s2`, `a_deriv_s1/s2_ne_zero`) — consistent with the Stage-0 Finding 3.

### 1b. What the DEPOSITED PAPER actually claims — and where

The deposited mathematical source for this result is
`sessions/2026-04-25/P08-CAS-HEUNC/vquad_resurgence_R2.tex` in
`papanokechi/siarc-relay-bridge` (companion `…/P08-SICF-REVISION/vquad_resurgence_R1.tex`).

- The result is stated as a numbered analytic theorem:
  `\begin{theorem}[Apparent singularity exclusion for V_quad] \label{thm:exclusion2}`
  in `\section{Apparent singularity exclusion}` (`\label{sec:frobenius}`), with a
  full four-step analytic proof (indicial exponents → analytic first solution →
  exact-ODE/Wronskian → trivial monodromy on `M_11`).
- **Its verification claim is SYMBOLIC + NUMERICAL — not Lean.** Verbatim
  ("Numerical certificate", lines 564–580):
  > "The identity `b(x) ≡ a'(x)` was verified symbolically. The resulting values
  > `p_0 = 1` and `q_0 = 0` at both `s_{1,2}` were confirmed numerically at
  > `dps=150` … Verification script: `verify_frobenius_apparent.py`; results in
  > `frobenius_apparent_verification.json`."
- The paper contains **no occurrence of "Lean", "machine-checked", or "formally
  verified"** in connection with this theorem (grep confirms zero such hits).
- The corpus's own master audit agrees. In
  `…/AUDIT-MASTER-THEOREM-INVENTORY/master_theorem_audit.md`, row `Vq-T-AppSing`
  records: *"Apparent singularity exclusion | **symbolic** | PROVED |
  vquad_resurgence_R[12] | LOW"* — and it lists Lean-verified items separately
  (the JAR manuscripts), so "symbolic" here is a deliberate, contrasting label.

### 1c. The gap, stated plainly

- **As an analytic result, the paper's claim is substantive and not vacuous.** Its
  proof genuinely derives `p_0=1, q_0=0 ⇒ I(ρ)=ρ²` and is backed by a real Python
  check. The vacuity problem is confined to the **Lean artifact**, which is a
  separate, exploratory SIARC relay deliverable (`Task ID: LEAN4-THM66`, header of
  the `.lean` file), not something the deposited paper relies on or cites.
- **The deposited paper does not claim a Lean formalization of this theorem.** So a
  caveat attached *to the paper* would have nothing to correct — the paper's stated
  method (symbolic + dps=150 numerics) matches what was actually done.
- **Where the overstatement risk lives is the corpus-internal "M10 / Theorem 6.6
  formalized in Lean" framing** (control-center status, e.g. the M1–M12 closure
  outlooks and the `LEAN4-THM66` task). That framing, read naturally, suggests the
  apparent-singularity content was machine-checked. It was not: the Lean file is a
  vacuous stub with 2 sorries. Notably, the corpus's OWN side already records this
  — the slot-140 outlook logs `Thm66_ApparentSingularity.lean = 2 sorries` and
  treats M10 as OPEN/deferred (not closed).

**Operator's decision (1):** whether to add a caveat. Two coherent readings:
- *If "the deposited claim" = the published paper:* no caveat needed — the paper
  claims symbolic/numerical verification, which is accurate. (Optional: nothing.)
- *If "the deposited claim" = any corpus artifact that asserts/implies "Thm 6.6
  formalized in Lean":* a caveat IS warranted on those status artifacts, because the
  Lean formalization is a vacuous, sorry-blocked stub that encodes no ODE content.

This is a corpus-governance call. Both the facts and the two readings are above; the
choice is the operator's.

---

## DECISION 2 — What to do about the mis-branched Lean core

### Confirmed against the live remote
- `wallis-pcf-lean4` has exactly **two branches**: `main` (`3af07fc`) and
  `vquad/handoff-2026-04-16` (`83f3ade`).
- **`main`'s `lean/`** = `WallisFamily.lean`, `lakefile.lean`, `lean-toolchain`.
  `Thm66_ApparentSingularity.lean` is **absent** on main (direct fetch → HTTP 404).
- **`vquad/handoff-2026-04-16`'s `lean/`** = the same three files **plus**
  `Thm66_ApparentSingularity.lean`.
- Consequence: a normal `git clone` of `wallis-pcf-lean4` (default branch `main`)
  does **not** surface the Lean core associated with the apparent-singularity /
  "Theorem 6.6" work. It is published (not lost) but not discoverable on the default
  branch. (Discoverability is moot if Decision 1 concludes the stub is not worth
  surfacing as-is.)

### Options for the operator (neutral; the decision is yours)
1. **Merge / cherry-pick `Thm66_ApparentSingularity.lean` to `main`.** Maximizes
   discoverability. Downside: it would place the vacuous, sorry-blocked stub on the
   default branch — arguably worse than hiding it unless Decision 1 is resolved
   first (e.g., strengthen `IndicialPoly`, or land it clearly labelled WIP).
2. **Leave it on the handoff branch and add a pointer.** E.g., a note in `main`'s
   README or `lean/` that the Thm 6.6 exploration lives on
   `vquad/handoff-2026-04-16`, with its current stub/sorry status disclosed. Fixes
   discoverability without promoting unfinished content to `main`.
3. **Leave as-is.** Lowest effort. Acceptable if Decision 1 concludes the Lean
   artifact is exploratory and the deposited paper (which does not depend on it)
   stands on its own symbolic/numerical proof.
4. **Strengthen first, then merge** (the deferred "option (b)"). Rewrite
   `IndicialPoly` to actually compute the indicial polynomial from the ODE
   coefficients so the Frobenius axiom becomes load-bearing, discharge the 2 sorries,
   then merge to `main`. Highest value, but substantive Lean work — out of scope here.

These interact: Decision 1's outcome (is the stub worth surfacing as-is?) naturally
informs the choice between options 1–4.

---

## What I could NOT confirm
- **No deposited manuscript literally numbering this result "Theorem 6.6" was
  located.** "Theorem 6.6" is the corpus-internal / control-center M10 label (e.g.
  the `LEAN4-THM66` task and the M1–M12 closure outlooks, which call it the "M10
  closure target Theorem 6.6"). In the deposited math source
  (`vquad_resurgence_R2.tex`) the result is `\label{thm:exclusion2}`, numbered by
  section (Section 3, `sec:frobenius`), NOT "6.6". The "6.6" therefore comes from
  an umbrella/aggregate numbering I did not find as a single deposited PDF/tex.
- **I did not build the Lean file**, so the axiom-cone / sorry analysis is by source
  inspection, not a live `#print axioms` run. (The two `sorry` tokens and the
  arg-ignoring `IndicialPoly` are literal in the committed source, so the conclusion
  is robust; but the exact printed cone was not executed. A port would be needed:
  the branch pins `leanprover/lean4:stable` + unpinned Mathlib HEAD, vs Fingerprint's
  v4.29.0 / Mathlib `8a178386`.)
- **Whether the Python certificate is itself sound** (`verify_frobenius_apparent.py`
  / `frobenius_apparent_verification.json`) was not independently re-run — only that
  the paper cites it and the master audit labels the theorem "symbolic, PROVED".
- **Whether the four "routine" Lean axioms** (`root_s1/s2`, `a_deriv_s1/s2_ne_zero`)
  are as trivially dischargeable as claimed was not attempted.

---

## Standing rule
Per the project meta-rule, no commit/push/tag/move/delete was performed and none is
proposed here. This brief is the deliverable; the two decisions are the operator's.
