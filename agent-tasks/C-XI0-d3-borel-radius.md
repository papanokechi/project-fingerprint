# TASK C-XI0: Close op:xi0-d3-direct — the Borel-radius identity at degree 3

> Filled-in instance of `agent-tasks/TEMPLATE.md`. New research space: the
> Borel-singularity-radius universality conjecture xi0(b) = d / beta_d^(1/d) for
> degree-d polynomial continued fractions. Corpus status: PROVEN at d=2, VERIFIED
> at d=4 (dps=80, 8 quartic representatives); d=3 is the open item op:xi0-d3-direct
> (a bounded Newton-polygon computation per Channel Theory v1.3 / D2-NOTE v2.1).
>
> This is a SYMBOLIC + NUMERIC computation (sympy Newton polygon + mpmath
> verification), NOT a PSLQ run. Different toolchain; both CPU-local. All standard
> rules bind: locate-don't-reconstruct, no commit/push, "could not confirm"
> required, an honest negative is a complete result.

---

## CRITICAL — this is a proof/computation task, so a wrong SETUP yields a
## confidently-wrong "result," which is worse than a null. The defining objects
## MUST be located from the deposits, never reconstructed from memory or from the
## formula being tested.

## STAGE 0 — locate the construction AND determine the task's true character
## (do this FIRST, then STOP for operator confirmation before any computation)

1. Find, in the deposits / repos (Channel Theory concept DOI 10.5281/zenodo.19941678;
   D2-NOTE; siarc-relay-bridge sessions referencing CC-PIPELINE / xi0 / Newton
   polygon), the ACTUAL definitions — do not reconstruct:
   - The order-d ODE governing the PCF denominator generating function
     f(z) = sum Q_n z^n at z=0 (the object whose Newton polygon is taken).
   - The Newton-polygon construction used at d=2 and d=4: how the slope-1/d edge
     and its characteristic polynomial chi are extracted.
   - The EXACT d=2 result (chi = 1 - (beta_2/4)c^2, xi0 = 2/sqrt(beta_2)) and the
     d=4 result (chi = 1 - (beta_4/4^4)c^4, xi0 = 4/beta_4^(1/4)) as the corpus
     states them — to confirm you've reproduced the same construction.
   - One concrete CUBIC (degree-3) PCF representative to test, with its exact
     a_n / b_n (beta_3, beta_2, beta_1, beta_0). Report which family and source.
   - The dps the d=4 verification used (for parity), and any documented handling
     of half-integer rank / ramification (Wasow §19.3 is cited for the q=(d+2)/2
     fractional-rank case — d=3 gives q=5/2, a half-integer, which is exactly
     where the odd-degree case may differ).

2. **Determine the task's character** by reading the D2-NOTE v2.1 status:
   - D2-NOTE v2.1 Theorem 4.1 claims a GENERAL-d proof (xi0 = d/beta_d^(1/d) at
     all d>=2) composing a Newton-polygon lemma + Wasow §19. Read whether that
     general proof is stated to ALREADY COVER d=3, or whether d=3 is excluded /
     deferred / flagged.
   - If the general proof covers d=3: this task is a CONFIRMATION computation
     (verify the explicit cubic matches xi0 = 3/beta_3^(1/3); expected to match).
   - If d=3 is genuinely deferred/open (e.g. the half-integer rank q=5/2 is not
     covered by the general argument): this is a GENUINE-OPEN computation where a
     mismatch would be a real finding, not an error.
   - Report which of the two it is, with the supporting quote/location. Do NOT
     proceed to Stage 1 until the operator confirms the character.

3. If you cannot locate the ODE construction or a concrete cubic family, STOP and
   say so — do NOT reconstruct the ODE from the formula being tested (that would
   make the computation circular: deriving the answer from the thing you're
   checking).

STOP here. Report Stage 0 and await operator confirmation before computing.

## STAGE 1 — the Newton-polygon computation (only after Stage 0 confirmed)

4. For the chosen cubic representative, construct the order-3 ODE per the located
   d=2/d=4 method, take its Newton polygon at z=0 (sympy), and extract the
   slope-1/3 edge and its characteristic polynomial chi_3(c). Report chi_3
   symbolically.
5. The conjecture predicts chi_3(c) = 1 - (beta_3 / 3^3) c^3 and hence
   xi0 = 3 / beta_3^(1/3). Check whether the constructed chi_3 MATCHES this form.
   - MATCH -> the identity holds for this cubic (confirmation, or open->closed).
   - MISMATCH -> report the actual chi_3 and the actual xi0; this is a real
     finding (the universality fails or needs modification at d=3), NOT an error
     to debug away. Re-derive carefully and, if the mismatch persists, report it
     plainly.
6. NUMERIC confirmation: compute xi0 independently from the PCF data (the way d=4
   was verified at dps=80) — e.g. via the Borel-singularity radius from the
   large-order behavior of Q_n, or the documented numerical method — and confirm
   it equals 3/beta_3^(1/3) to the dps the corpus used. Report dps and agreement
   digits.
7. If possible, test a SECOND cubic representative (different beta coefficients)
   to confirm the result isn't an artifact of one family — the d=4 case used 8.

## OUT OF SCOPE — do NOT

- Do NOT reconstruct the ODE or the cubic family from memory or from the target
  formula. Located-from-deposit only; STOP if not found.
- Do NOT debug a genuine MISMATCH into a match — if chi_3 doesn't fit
  1-(beta_3/27)c^3 after careful re-derivation, that is the finding.
- Do NOT claim this PROVES the general conjecture — a per-representative
  computation VERIFIES the identity for those cubics; the general proof is
  D2-NOTE's Theorem 4.1, separate. State precisely what was verified.
- No PSLQ here (wrong tool). No commit/push/tag/move/delete.

## A clean result either way is success
- Identity holds for the cubic(s) -> op:xi0-d3-direct is CLOSED (the wanted
  outcome; lifts the conjecture to proven-d2 / verified-d3-d4).
- Identity does NOT hold -> a genuine, reportable finding about odd-degree /
  half-integer-rank behavior. Either is a complete, honest answer.

---

## REQUIRED FINAL REPORT (fill every field)

**Stage 0 — located construction:**
- ODE construction source + form: <...>
- d=2 / d=4 results reproduced from corpus: <chi forms + xi0>
- cubic representative(s) used + source: <family, beta coeffs>
- d=4 verification dps (for parity): <...>
- half-integer-rank (q=5/2) handling, if documented: <...>

**Task character (REQUIRED):** CONFIRMATION or GENUINE-OPEN, with the D2-NOTE
v2.1 quote/location that determines it.

**Stage 1 — computation:**
- constructed chi_3(c) symbolically: <...>
- matches 1 - (beta_3/27)c^3 ? <yes/no; if no, the actual chi_3 and xi0>
- numeric xi0 vs 3/beta_3^(1/3): <value, dps, agreement digits>
- second cubic (if run): <result>

**Honest claim (one sentence):**
<e.g. "op:xi0-d3-direct CLOSED: for cubic representative <fam>, the slope-1/3
Newton-polygon edge gives chi_3 = 1-(beta_3/27)c^3, hence xi0 = 3/beta_3^(1/3),
confirmed numerically to <N> digits — verifying the universality identity at
d=3 (proof of the general case remains D2-NOTE Thm 4.1)." OR a mismatch finding.>

**What I could NOT confirm (REQUIRED — never empty):**
<whether the result generalizes beyond the tested cubic(s); whether the
half-integer rank is fully handled; whether the located ODE construction is the
canonical one; any source not found.>

**Ready-but-not-done (awaiting operator):**
<git add/commit for the computation script + results; save agent-tasks/C-XI0-...md
to disk. Selective staging (pslq/constants/ has multi-thread files). By hand.>
