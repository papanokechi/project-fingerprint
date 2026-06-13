# EBR-III — venue memo (op:ebr3-f)

**Paper.** *The EBR operator at d=2 is not a G-operator and its differential
Galois group is SL(4): arithmetic, irreducibility, and the non-Liouvillian
corollary.* PDF SHA-256 `92696419103760e4b9cf0ec6b81cf586f7268466b98fe794d7561d263c781a6f`.

**Nature of the work (for scope-matching).** Algorithmic / computational
differential Galois theory: explicit order-4 operator; Aschbacher
maximal-subgroup elimination executed via rational-solution searches with *a
priori* degree bounds; p-curvature certification; a 169-digit PSLQ null battery;
**four Lean 4 / Mathlib cores with audited axiom cones**; structural payoff is
the identity-component identification `G_Gal(L_2)° = SL(4)` and the
non-Liouvillian corollary. Subject classes 34M35, 12H05, 34M03, 33C20, **68V20**
(formalized mathematics), 11J81. The centre of mass is **algorithmic
differential Galois + formalization**, with a structural theorem on top.

**Standing constraints applied** (from house memory):
- Experimental Mathematics — **BLACKLISTED**, excluded.
- NNTDM — **blocked**, excluded.
- Ramanujan J, Acta Arithmetica — **OCCUPIED** (one-submission-per-venue rule);
  excluded while a submission is live there.
- J. Differential Equations — **OCCUPIED**; listed only *conditionally*, with
  the concurrent-submission policy question flagged (see note).
- SIGMA — listed **with the direct-PDF/submission-route question flagged**.
- arXiv — endorsement barrier assumed unresolved ⇒ **Zenodo-first** (deposit
  mints the citable DOI; journal submission references it).

---

## Ranked shortlist

| # | Venue | Scope fit | Preprint policy | LLM-policy risk | Turnaround | Status |
|---|-------|-----------|-----------------|-----------------|-----------|--------|
| 1 | **Journal of Symbolic Computation (JSC)** | **Best.** Computer algebra, algorithmic differential Galois, *and* formalized mathematics — covers both the algorithmic core and the Lean cores | Elsevier: preprint posting permitted (Zenodo/arXiv) | Disclose genAI assistance in a statement; allowed with disclosure — **manageable** | 6–12 mo | **FREE** |
| 2 | **AAECC (Applicable Algebra in Eng., Comm. & Computing)** | **Strong.** Applicable/computer algebra incl. differential-equation algorithms and symbolic methods | Springer: preprint permitted | Springer genAI disclosure required — manageable | 4–9 mo | **FREE** |
| 3 | **SIGMA** | Good. Special functions / integrable systems / differential Galois; diamond OA, fast | arXiv/Zenodo-friendly (OA) | Lenient | 3–6 mo (fast) | **FREE — flag** direct-PDF/submission route works with a Zenodo-first DOI |
| 4 | **Journal of Algebra** | Moderate. The `SL_4` identification and algebraic-group elimination are in scope, but the paper is more algorithmic than pure algebra | Elsevier: preprint permitted | Disclosure — manageable | 8–14 mo | **FREE** |
| 5 | **Annales de l'Institut Fourier** | Moderate/structural, high tier. Differential Galois + arithmetic of ODEs fits, but a generalist top-tier venue may resist a *d=2-only*, STRUCTURAL (non-Lean) main theorem | Preprint permitted (OA) | Lenient | 9–18 mo, selective | **FREE** |
| 6 | **J. Differential Equations** *(conditional)* | Good on the irregular-singularity / ODE side | Elsevier: preprint permitted | Disclosure | 6–12 mo | **OCCUPIED — verify policy first** |

### Note on JDE (constraint resolution)
The one-submission rule that blocks Ramanujan J / Acta Arithmetica is the
*same-manuscript-to-multiple-venues* prohibition. Elsevier's policy bars
submitting **the same** manuscript elsewhere while under review; it does **not**
generally bar submitting a **different** manuscript to a journal that already has
an unrelated submission from the same author. EBR-III is a distinct manuscript
from whatever currently occupies JDE, so a second *distinct* JDE submission is
*probably* permissible — **but the operator must confirm** (a) the occupying
submission's status and (b) that no editor-level "one active submission per
author" norm applies, **before** listing JDE live. Until confirmed, treat JDE as
unavailable.

### Note on SIGMA
SIGMA's submission route is a direct upload to their editorial system (not a
journal-managed arXiv overlay). The Zenodo-first workflow is compatible — deposit
mints the DOI, then upload the same PDF to SIGMA — but **confirm the direct-PDF
upload path** and that prior Zenodo posting does not conflict with their
originality policy (it does not, for preprints, but flag it).

---

## Recommendation

- **Primary: Journal of Symbolic Computation (JSC).**
  One-line rationale: it is the only venue whose scope simultaneously covers the
  paper's algorithmic differential-Galois core *and* its Lean/Mathlib
  formalization (subject class 68V20), so nothing in the contribution reads as
  out-of-scope.

- **Fallback: AAECC.**
  One-line rationale: same algorithmic-algebra centre of mass with a faster,
  less selective process, and no occupancy or policy flag against it.

SIGMA is the best *fast/open-access* option if turnaround dominates, contingent
on clearing the direct-PDF-route flag. J. Algebra and Annales Fourier are
viable if the structural `SL_4` theorem is judged the lead contribution rather
than the algorithmics.
