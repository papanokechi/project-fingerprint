# Thread C — S (V_quad Stokes constant) prefactor dispute: RESOLUTION findings

> Audit-trail record of the Stage-0 locate + Stage-1 derive/decide investigation
> that resolves the `DISPUTED_UNRESOLVED` status of the `S` entry in
> `pslq/constants/basis_canonical.json`. No constant was committed. A ready (un-run)
> patch is prepared for the operator (see "Ready-but-not-done").

**Decision (one line):** The **2π prefactor is correct → S = 2πK =
0.45790662316901763611…** The deposited *manuscript* (v1.1) is already correct;
the session's `DISPUTED` downgrade rested on a premise ("the v1.1 2π correction is
a phantom / does not exist in the deposit") that is **refuted** by the located
manuscript. The earlier `0.43770528` (Γ(β) prefactor) is a different, non-Stokes
normalization (a Borel singular-amplitude), explicitly retracted by the paper.

---

## The dispute (recap)

`K = 0.0728781025518669641294…` (late-term Borel amplitude) is NOT disputed.
Only the prefactor relating K to S was:

| convention | prefactor | S |
|---|---|---|
| A — Γ(β) | `|Γ(β_exp)| = 6.00599…` | `0.437705286193537221230…` |
| B — 2π | `2π = 6.28319…` | `0.457906623169017636119…` |

`β_exp = -1/(3√3) = -0.19245…`, `ξ₀ = 2/√3`. Ratio `2π/|Γ(β_exp)| = 1.04615…`
(~4.4%). Confirmed by recompute (`S_prefactor_verify_results.json`, this repo).

---

## STAGE 0 — located derivations (verbatim, not reconstructed)

### Source 1 — the deposited manuscript `vquad_resurgence.pdf` (located at
`C:\LocalWork\pnwork\vquad_resurgence.pdf`, 12 pp, the Painlevé-V / resurgence paper)

**This manuscript IS v1.1 and DOES carry the 2π correction.** Two verbatim items:

- **Definitional convention (§6):** *"Throughout, S denotes the **real Stokes
  multiplier** of the Dingle normalization — the real coefficient of the
  discontinuity"* `y(Stokes+)_rec − y(Stokes−)_rec = S · y_dom`.

- **Eq (13), the Dingle late-term formula as the paper states it:**
  > `S_n = a_n · 2π · ξ₀^(n+β_exp) / ((−1)^n · Γ(n+β_exp)) ──→ S as n→∞.   (13)`
  > "The prefactor 2π is the universal Borel–Laplace discontinuity factor; it was
  > calibrated by running the identical extraction on Euler's series, for which
  > K=1 and |S|=2π exactly. (Version 1.0 used Γ(β_exp) = −6.00599… in place of
  > 2π = 6.28319… here; the two agree to 4.4%, which camouflaged a systematic
  > factor in the reported S.)"

- **Remark 6.2 (Version 1.1 — Stokes-constant numeric correction):**
  > "The Stokes constant is corrected from the version 1.0 value S≈0.43770528 to
  > S = 2πK = 0.45790662316901763611… (certified to 38 digits). The v1.0 value was
  > produced by an incorrect normalization prefactor in the Dingle late-term
  > extraction (13): the late-term amplitude was multiplied by Γ(β_exp) =
  > −6.00599… instead of the universal resurgence factor 2π = 6.28319…; because
  > the two agree to 4.4% the slip survived the internal multi-method consensus.
  > The underlying amplitude K = 0.07287810255… is unchanged and triple-confirmed
  > (Neville–Richardson, Berry–Howls, Domb–Sykes)."

- **Independent cross-check (Conjecture 7.1):** the Jimbo (1982) connection formula
  `S_Jimbo = 2i·sin(πσ_conn)·Γ(1−σ_conn)²/Γ(1+σ_conn)²` gives `|S_Jimbo| = 0.4579…`
  — i.e. the RH-monodromy route lands on **2πK**, not Γ(β)K. (Caveat: σ_conn is
  back-derived from S, so this is a consistency check, not independent.)

### Source 2 — the deposited *code* `pcf-research/vquad/scripts/` (located at
`C:\LocalWork\_refs\pcf-research\vquad\`)

The code is **STALE at v1.0**: `t2_iter21_hyperasymptotic.py` and
`t2_iter22_s_precision.py` both extract S with
`S_n = a_n · Γ(β) · ξ₀^(n+β) / ((−1)^n · Γ(n+β))` (Γ(β) prefactor → 0.43770528).
This is the already-logged provenance defect in `agent-tasks/A2-pcf-research-stale-prefactor.md`.
Notably the v1.0 authors *were aware* of the 2πi normalization question —
`iter21` lines 453–458 explicitly PSLQ-test `gamma_beta`, `1/gamma_beta`, and a
`stokes_norm` = `S·sin(πβ)/π` — but shipped the Γ(β) value. The manuscript's
Remark 6.2 is the correction of exactly this code.

### Standard formula (independent of the deposit; web-corroborated)

Dingle–Berry–Howls–Écalle universal late-term / large-order formula:
> `a_n ~ (S / 2πi) · Γ(n+β) / A^(n+β) · [1 + O(1/n)]`

Refs: Dingle (1973); **Berry & Howls, "Hyperasymptotics," Proc. R. Soc. Lond. A
430 (1990)**; Howls, Proc. R. Soc. A 439 (1992); Écalle, *Les Fonctions
Résurgentes*. The companion of `Γ(n+β)` is the **β-independent** factor `1/2πi`
(the Borel–Laplace discontinuity / Cauchy-jump normalization). β and A enter only
`Γ(n+β)` and `A^(n+β)`.

**Do the sources agree?** Yes. The standard formula and the deposited manuscript
v1.1 both pair `Γ(n+β)` with the universal `1/2πi` (magnitude 2π). The deposited
*code* (v1.0) and the abstract the session's Zenodo lookup read are the stale Γ(β)
variant.

---

## STAGE 1 — derivation and decision

### What the Γ(β) value actually is (the rubber-duck nuance)

Γ(β)·K is **not nonsense** — it is a *different, legitimate quantity*: the local
**Borel singular-amplitude** C. If the Borel transform near its singularity is
`f̂(ξ) ~ C·(1 − ξ/A)^(−β)`, then `a_n ~ (C/Γ(β))·Γ(n+β)/A^n`, so the extracted
amplitude is `K = C/Γ(β)` and `C = Γ(β)·K = 0.43770528`. So `0.43770528` is the
Borel branch coefficient C, **not** the Stokes multiplier. The v1.0 error was
computing C and *labelling it the Stokes constant S*.

### Which one is "the Stokes constant S"?

The paper **defines** S as the **Stokes multiplier** — the coefficient of the
discontinuity `y(Stokes+) − y(Stokes−) = S·y_dom`, with the adjacent (dominant)
sector normalized to leading 1. For that object the universal companion of
`Γ(n+β)` is `1/2πi`, so:

> **|S| = 2π · K = 0.457906623169017636119…**

This is fixed by the *definition* of the Stokes multiplier, not by a "2π is
universal" hand-wave, and it is pinned three ways:
1. the standard resurgence formula (companion of Γ(n+β) is 1/2πi);
2. the manuscript's **Euler-series calibration** — running the *identical*
   extraction on a known case (Euler: K=1, |S|=2π exactly) reproduces |S|=2π only
   with the 2π prefactor (a derivation-by-known-answer, the test the task asked
   for); and
3. the Jimbo connection-formula route, `|S_Jimbo| = 0.4579…` (consistency only).

### Decision

Outcome **(a) with a correction to its framing:** **2π is correct → S =
0.45790662…** *But* the deposited **manuscript is already right** (it carries
exactly this in eq (13) + Remark 6.2). The thing in error is **not** the
manuscript — it is:
- the v1.0 value `0.43770528` (a mislabeled Borel amplitude C; retracted by the
  paper's own Remark 6.2);
- the stale **pcf-research code** (A2, still Γ(β)); and
- **this session's `DISPUTED` downgrade**, whose premise "no 2π correction exists
  in the deposit / the v1.1 correction is a phantom" is **refuted** by the located
  manuscript Remark 6.2.

So: **the canonical file needs correcting** (restore `S` to VERIFIED, 2π
convention); the paper does not.

---

## What I could NOT confirm (required)

- **Whether the live Zenodo upload (DOI 10.5281/zenodo.20455090, "latest version")
  actually serves v1.1.** The *local* manuscript `vquad_resurgence.pdf` contains
  Remark 6.2 + eq (13) with 2π. I could not verify the Zenodo-hosted PDF/abstract
  from here. If the Zenodo deposit still serves the v1.0 abstract (0.43770528),
  that is a **deposit-update gap** (manuscript corrected, upload stale) — a
  provenance/hygiene to-do that does **not** change the mathematics. This is
  exactly the discrepancy that misled the session's Zenodo-only check.
- **K was not re-derived here** (already 46–84 digit stable, not disputed).
- The **Jimbo cross-check is not independent** (σ_conn is back-derived from S), so
  it corroborates but does not independently prove 2π.
- I did not inspect every vquad iteration script; the prefactor finding rests on
  iter21/iter22 (the S-extraction iterations) + the manuscript.

---

## Ready-but-not-done (awaiting operator; nothing committed)

- A ready, un-run patch `pslq/constants/patch_S_resolve_to_verified.py` is prepared
  (mirrors the existing `patch_S_to_disputed.py`). It restores the `S` entry to
  `VERIFIED` at `0.4579066231690176361190978425482258379624` (2π convention) with
  full provenance to `vquad_resurgence.pdf` Remark 6.2 / eq (13), records the
  Γ(β)=Borel-amplitude clarification, and carries the unconfirmed-Zenodo caveat.
  **Per the standing meta-rule, I did NOT run it** — operator reviews this findings
  file, then runs `python pslq\constants\patch_S_resolve_to_verified.py` by hand.
- Follow-on (separate, already logged): fix the stale `pcf-research` code
  (`agent-tasks/A2-pcf-research-stale-prefactor.md`); and a deposit-hygiene check
  that the Zenodo upload reflects v1.1.
