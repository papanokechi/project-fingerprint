# Erratum patch — op:cc-transcendence/cc4-2

Two errata are executed and recorded here as a standalone artifact, as directed
by the `op:cc4-CLOSE` prompt. Both are **narration / scope** corrections; no
load-bearing computational claim of any prior stage changes.

---

## CC4-ERR-1 — "unipotent / resonance log at R" → "semisimple pseudo-reflection"

**What was wrong.** Early narration (cc-1 report, and propagated into the
`op:cc-2` prompt block) described the local monodromy `M_R` at `s = R` as
*unipotent-times-eigenvalue*, i.e. carrying a **Jordan block / "resonance log"**
arising from the `−γ` vs `{0,1,2}` exponent resonance.

**The correction.** `M_R` is **SEMISIMPLE**. It is a complex **pseudo-reflection**
of order 6 with eigenvalues `{1, 1, 1, e^{iπ/3}}`, `rank(M_R − I) = 1`. There is
**NO logarithm at R**.

**Why.** A `−γ` resonance produces a logarithm **only if `γ ∈ ℤ`**. Here
`γ = 11/6 ∉ ℤ`, so the integer-exponent resonances `{0→1, 0→2, 1→2}` on the
eigenvalue-1 tower carry no log and `M_R` stays diagonalizable. This is
**consistent with EBR-II's own criterion** and is established by three
independent routes:

1. **Exact symbolic Frobenius at R** (cc2-2d / `cc2_1_2.py`): every resonance
   obstruction `P̃₁(0) = P̃₁(1) = P̃₂(0) = 0` vanishes ⇒ 3 independent log-free
   solutions ⇒ geometric mult = algebraic mult = 3.
2. **Numerical monodromy** at dps 40 (`cc2_2d_numerical_monodromy.py`,
   sha `03e42926…`): `rank(M_R − I) = 1` (one singular value `2.159`, the rest
   `≤ 1e-30`).
3. **No-log resonance residuals to 169 digits** (cc4-1 `cc4_1_connection.py`,
   sha `f3400831…`): the free coefficients at the integer-exponent resonances
   are forced with residual `≈ 0` to 169 digits — an exact-arithmetic
   confirmation deeper than the dps-40 numerical channel.

**Scope of the fix.** Only the *adjective* on `M_R` changes. The R-eigenvalues
`{1,1,1,e^{iπ/3}}`, the exponents `{−11/6, 0, 1, 2}`, irreducibility of `L₂`,
the irregular-∞ structure, and **`G_Gal(L₂)⁰ = SL₄`** are all **UNAFFECTED**.

**Files patched (inline `[ERRATUM CC4-ERR-1: …]` markers, archive preserved):**

| File | Location | Before | After |
|---|---|---|---|
| `OP_CC2_PROMPT.txt` | local-monodromy classes block (≈ ln 49–51) | "s=R unipotent-times-eigenvalue (a Jordan block from the −γ vs {0,1,2} resonance)" | "s=R SEMISIMPLE pseudo-reflection {1,1,1,exp(πi/3)}; NO log; γ=11/6∉ℤ" |
| `REPORT_cc1_d2.md` | open-problems item 2 (≈ ln 91–93) | "the `s=R` resonance log" | "the `s=R` semisimple pseudo-reflection `{1,1,1,e^{iπ/3}}` (no log; γ=11/6∉ℤ)" |

(The cc-2 report `REPORT_cc2_12.md` already states the correction and recommends
this erratum; it needs no patch. `REPORT_cc1_d2.md` line ≈99 "resonance condition
`γ ∈ ℤ`" is **correct as stated** — it is precisely the criterion that yields
*no* log here — and is left unchanged.)

---

## CC4-ERR-2 — CC2-0-GFUNC normalization-scope audit

**Requirement.** Confirm that the "G is not a G-function" finding (CC2-0-GFUNC)
carries its normalization caveat in **both** the claims ledger **and** the shared
memory entry; fix the memory entry if it predates the patch.

**Ledger — CONFIRMED CORRECT (no change needed).** `claims_cc.jsonl` CC2-0-GFUNC
is explicitly **`NORMALIZATION-SCOPED`** for `g_n = Q_n/(2n)!` and carries the
verbatim caveat: *"this finding is about the Q_n/(2n)! normalization and does NOT
extend to arbitrary rescalings of the coefficient sequence … The op:cc-3
consequence is only that THIS G cannot be used as a G-function."* The companion
**CC2-0-QINT** (`Q_n ∈ ℤ` for `n ≤ 2000` ⇒ `q_N | (2N)!`) is present and makes the
"no collapse" statement precise (`log10 q_N / log10((2N)!) ~ 1.0000`).

**Shared memory — NO CONFLICTING ENTRY FOUND.** No surfaced memory entry asserts
an unscoped "G is not a G-function" / "Q_n/(2n)! no-collapse" claim. There is
therefore nothing to downvote or rewrite; the ledger remains the authoritative,
correctly-scoped record. (If an unsurfaced memory later appears without the
normalization scope, downvote it and store the scoped version: *"CC2-0-GFUNC is
normalization-scoped to g_n=Q_n/(2n)!; it does not extend to rescalings."*)

**Disposition:** CC4-ERR-2 = **CONFIRMED** (ledger already correct; no memory
patch required).
