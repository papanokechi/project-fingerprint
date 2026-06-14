# REPORT — op:cc-3 (period rebuild), stage cc3-1b (reduction hardening + GATE 0)

**Task:** `op:cc-transcendence/cc-3`  ·  **Stage:** cc3-1b (Riemann scheme,
GATE 0 at ∞, K to ≥120 digits, Route B).  ·  **Status:** **HALT for review
before cc3-1c — GATE 0 triggered (∞ IRREGULAR).** Nothing committed/minted.

**Discipline + CEILING (verbatim, standing rule for this op):**
> A large G_Gal does NOT imply C transcendental; an exponential-period
> classification does NOT imply C transcendental; only a named-conjecture
> conditional (or out-of-scope genuinely new technology) does. **Unconditional
> transcendence of C is NOT a deliverable of op:cc-3 and may not appear as a
> claim at any grade.** Admissible outcomes: (a) hierarchy location, (b)
> integral/period representation, (c) exponential-period classification, (d)
> CONDITIONAL transcendence under a NAMED conjecture (conditionality in the
> claim text), (e) documented technology-gap / obstruction reports.
>
> **Extended for cc3-1b:** a Fuchsian *relocation* does **not** imply K is a
> classical period — provenance, not singularity type, is what the period
> conjectures see; and the operator carrying K is **not** Fuchsian, it is
> irregular at ∞ (slope 1/4).

---

## 0. Position

cc3-1a (Route A, `7762ace0…`) reduced the EBR connection constant
`C = C_EBR = A = 3.0557068…` (corpus anchor `f3400831…`, 169 digits) to a
single connection coefficient **K** of the Borel-2 companion operator

> **L = z⁴(1−3z) D⁴ + (4z³−25z⁴) D³ + (2z²−47z³) D² − 15 z² D − z²**,
> annihilating `Φ(z) = Σ Qₙ zⁿ/(n!)²` (radius 1/3),

via `C_EBR = K·(4/3)√π/Γ(7/3)`, where `K` is the amplitude of Φ's
`(1−3z)^{−4/3}` local solution at `z=1/3`. cc3-1a graded the reduction
STRUCTURAL+VERIFIED but its numeric link was weak (`K` only to relative
`6.4e-4` by Richardson — the WEAKEST LINK). cc3-1b is **gate 0**: complete the
Riemann scheme, decide whether `L` is regular-singular at ∞, and harden the
reduction to ≥120 digits with an independent second route.

**Headline.** Two things landed, one of them a gate trigger:

1. **GATE 0 FAILS — `L` is IRREGULAR at `z=∞` (slope 1/4)**, by two independent
   rigorous routes. The cc3-1a phrase *"Fuchsian operator `L`"* is therefore an
   **overclaim and is superseded** (rescope in §3). The connection problem
   `0 → 1/3` remains regular-to-regular, so `K` is well-defined; but the global
   operator is **non-Fuchsian**, and `K`'s natural period home is **exponential**,
   not classical Kontsevich–Zagier.
2. **The reduction is HARDENED to 171 digits.** `K` computed directly as a
   connection coefficient (local-basis matching) `= 1.539494848576641034843781903…`;
   `K·(4/3)√π/Γ(7/3)` reproduces frozen `C_EBR` to **171 digits** (limited only
   by the frozen value's precision). Route B (Hadamard quotient) gives the same
   `K` and an algebraically identical factor. CC3-1-CRED's `6.4e-4` is replaced.

The running family: `Qₙ = (3n²+n+1) Qₙ₋₁ + Qₙ₋₂`, `Q₀=1`, `Q₁=5`;
`gₙ = Qₙ/(2n)!`; `R = 4/3`; `γ = 11/6`.

---

## 1. Complete Riemann scheme of `L`  (`cc3_1b_riemann.py`, `2d98e76…`)

Indicial polynomials (exact, from `L[(x−x₀)ʳ]` lowest-order coefficient):

| point | indicial | exponents | logs? |
|---|---|---|---|
| `z = 0`   | `r²(r−1)²` | `{0, 0, 1, 1}` | repeated roots ⇒ partner solutions carry logs; **Φ (exp 0) is the log-free holomorphic solution** `1+5z+…` |
| `z = 1/3` | `−r(r−2)(r−1)(3r+4)/81` | `{−4/3, 0, 1, 2}` | **integer block `{0,1,2}` is LOG-FREE** (all resonance obstructions vanish); `−4/3` isolated ⇒ log-free |
| `z = ∞`   | — (irregular) | ramified, slope 1/4 | exp(λ z^{1/4}), `λ⁴ = −256/3`, four conjugates |

**Why this matters for `K`.** Φ is the unique (up to scale) holomorphic
solution at `z=0`; we continue *it*. At `z=1/3` the `−4/3` exponent is isolated
(non-integer gap to `{0,1,2}`), so its `(1−3z)^{−4/3}` solution is log-free and
**`K`, its amplitude in the continuation of Φ, is cleanly defined**. The
integer block `{0,1,2}` is also log-free (resonance obstructions `0,0,0`
verified symbolically and again numerically in §4), so all four local
solutions at `z=1/3` are pure Frobenius series — the connection matrix is
clean.

### 1.1 GATE 0 — `z=∞` is IRREGULAR (slope 1/4), two routes

**Route (1) — z-chart Fuchsian test.** `L` is regular-singular at ∞ iff
`deg pⱼ − j ≤ deg p₄ − 4 = 1` for all `j`. Degrees `deg pⱼ = (2,2,3,4,5)` give
`deg pⱼ − j = (2,1,1,1,1)`: **violated at `j=0`** (`2 > 1`). The culprit is
`p₀ = −z²` — exactly the `φₙ₋₂` term of the three-term recurrence, the precise
analogue of the `−s²` term that makes EBR's `L₂` irregular at `s=∞`.

**Route (2) — Newton polygon at `w=0` (`z=1/w`, `D_z=−w²D_w`).** In `D_w`-form
`L = Σ bⱼ(w) D_wʲ`,

| j | `bⱼ(w)` | `val_{w=0}` | reg. needs `≥ val₄−(4−j)` |
|---|---|---|---|
| 0 | `−1/w²` | **−2** | −1 → **VIOLATED** |
| 1 | `4w−1` | 0 | 0 ✓ |
| 2 | `w(14w−5)` | 1 | 1 ✓ |
| 3 | `w²(8w−11)` | 2 | 2 ✓ |
| 4 | `w³(w−3)` | 3 | 3 ✓ |

`val(b₀) = −2 < −1` ⇒ **irregular**. The single ramified slope `k` comes from
the dominant balance `min_j (valⱼ − j(k+1))` attained twice: it is attained at
`j=0` (`−2`) and `j=4` (`−2`), giving `−2 = 3 − 4(k+1) ⇒ k = 1/4`. Leading-
coefficient match `b₄(λ(−k))⁴ + b₀ = 0` (`b₄ ~ −3w³`, `b₀ = −1/w²`) gives
**`λ⁴ = −256/3`**. Both routes agree: **`z=∞` irregular, slope 1/4** — the same
slope as the inherited `L₂` at `s=∞`. The irregularity was **relocated** by the
Borel-2 transform from `s=∞` to `z=∞`, **not removed**.

### 1.2 Fuchs-relation audit (consistency, not a constraint here)

Finite exponent sums: `Σ@0 = 2`, `Σ@(1/3) = 5/3`, total `11/3`. A *Fuchsian*
order-4 operator with 3 singular points would need total `(3−2)·4·3/2 = 6`. The
deficit `6 − 11/3 = 7/3` is **not** a missing finite exponent at ∞: the Fuchs
relation does not apply to a non-Fuchsian operator. The "budget" is carried by
the irregularity (slope 1/4). This supersedes the prompt's tentative
"∞ forced to 4/3".

---

## 2. Hardened reduction — `K` to ≥120 digits  (`cc3_1b_K.py`, `2ff9da3…`)

**Method (regular-to-regular connection matching).** Both `z=0` and `z=1/3`
are regular-singular, so `K` is a genuine Frobenius connection coefficient.
At an interior matching point `z_m = 1/6` (`v_m = 1−3z_m = 1/2`):

- Φ (holomorphic exp-0 solution, log-free) and its first three derivatives are
  summed from the `z=0` power series (`aₙ = Qₙ/(n!)²`, radius 1/3, rate
  `3z_m = 1/2`; 1100 terms, tail `~10^{−330}` at dps 220).
- The four local Frobenius solutions at `z=1/3` are built in `v=1−3z` (radius 1,
  rate `1−3z_m = 1/2`; 900 terms, tails `~10^{−274}`): the singular
  `S_sing = v^{−4/3}(1+…)` and the three **log-free** holomorphic `H_a,H_b,H_c`
  (exponents 0,1,2). All resonance obstructions are `0.0` to ≥180 digits — an
  independent numerical confirmation of the §1 symbolic log-free finding.
- Solving the 4×4 connection system gives `K` = coefficient of `S_sing`:

> **K = 1.5394948485766410348437819033840690382193908905531487309262945606…**
> (130 digits in `cc3_1b_K_results.json`).

**Identity check vs frozen `C_EBR` (`f3400831…`):**

| quantity | value (head) |
|---|---|
| `K·(4/3)√π/Γ(7/3)` | `3.05570680789048136570191220172768136887554277497383057467638…` |
| `C_EBR` (frozen, 169 d) | `3.05570680789048136570191220172768136887554277497383057467638…` |
| relative error | `1.07e-172` ⇒ **171 agreeing digits** |

This **hardens CC3-1-CRED** from relative `6.4e-4` to ≥171 digits and confirms
the cc3-1a predicted `K = 1.53949…` (the cc3-1a Richardson `1.53851` was the
moderate-precision artifact, now superseded). Admissible deliverable type (b).

---

## 3. RESCOPE — superseding the cc3-1a "Fuchsian" framing

cc3-1a (REPORT_cc3_0_1.md §2.2 / §2.4; claims CC3-1-PHI, CC3-1-CRED) called `L`
"Fuchsian" and described a "4th-order **Fuchsian** connection problem". GATE 0
shows this is imprecise. The corrected, load-bearing statement:

> **`L` is regular-singular at `z=0` and `z=1/3` but IRREGULAR at `z=∞`
> (slope 1/4, `λ⁴=−256/3`). `K` is the connection coefficient between the two
> regular-singular points `0` and `1/3` — a regular-to-regular problem on a
> globally NON-Fuchsian operator.** The dominant-singularity reduction
> `C_EBR = K·(4/3)√π/Γ(7/3)` is unaffected (it is derived from the integral
> representation + Watson saddle, which never touch `z=∞`) and is now hardened
> to 171 digits.

Note cc3-1a §2.2 (line 115) **already** recorded that "the irregular slope-1/4
structure … lives at `z=∞` for Φ"; the rescope simply removes the contradictory
"Fuchsian operator" label and states the global type explicitly. **Consequence
for provenance:** because the operator carrying `K` is irregular (Stokes-
carrying) at ∞, `K`'s natural arithmetic home is **exponential periods**
(Fresán–Jossen), *not* classical Kontsevich–Zagier periods. A Fuchsian
relocation would have suggested a classical period; the correct non-Fuchsian
picture does not. This is consistent with cc3-0 (Φ is **not** a G-function).

---

## 4. Route B — independent derivation (`cc3_1b_routeB.py`, `78fceee…`)

The cc4-0 two-route discipline: a second, independent derivation of the same
reduction.

- **Route A** (integral rep + Watson saddle): `C_EBR = K·(4/3)√π/Γ(7/3)`.
- **Route B** (Hadamard quotient `gₙ = φₙ/binom(2n,n)`, coefficient
  asymptotics): `φₙ ~ (K/Γ(4/3)) 3ⁿ n^{1/3}`, `binom(2n,n) ~ 4ⁿ/√(πn)` ⇒
  `gₙ ~ (K√π/Γ(4/3)) (3/4)ⁿ n^{5/6}` ⇒ `C_EBR = K√π/Γ(4/3)`.

**Agreement (the gate).** The two factors are **algebraically identical** via
the Γ-recurrence `Γ(7/3) = (4/3)Γ(4/3)` ⇒ `(4/3)/Γ(7/3) = 1/Γ(4/3)` (verified
symbolically, `diff = 0`), and both define the **same `K`** (the `(1−3z)^{−4/3}`
amplitude of Φ). Both factors times the directly-computed `K` reproduce frozen
`C_EBR` to >50 digits; an independent Richardson fit of the raw sequence
`gₙ = Qₙ/(2n)!` (Route B's asymptotic input) confirms the `(3/4)ⁿ n^{5/6}` law
and the `C_EBR` value to **44 digits**. **Routes agree — no disagreement HALT.**

---

## 5. Updated obstruction inventory (first-class artifact, type (e))

| # | item | status after cc3-1b |
|---|---|---|
| O1 | numeric link `C ↔ K` | **CLOSED** — 171 digits (was `6.4e-4`) |
| O2 | global singularity type of `L` | **CLOSED** — reg-sing at `0,1/3`; **irregular slope 1/4 at ∞** (two routes); supersedes "Fuchsian" |
| O3 | log structure at `1/3` | **CLOSED** — integer block log-free, `−4/3` isolated ⇒ `K` well-defined |
| O4 | second independent derivation | **CLOSED** — Route B agrees (same `K`, identical factor) |
| O5 | rigidity / arithmetic of `L` (P4/P4a) | **RE-PLANNED** — the Fuchsian index of rigidity and the "rigid ⇒ motivic ⇒ G-function" logic (P4 premise) are **inapplicable**; `L` is non-Fuchsian. cc3-1c must use the **irregular** index of rigidity (Bloch–Esnault, Arinkin, Jakob–Yun) — this is the gate-triggered re-plan |
| O6 | period nature of `K` | **OPEN** — candidate: exponential period (Fresán–Jossen); cc3-2 target |

---

## 6. Four-class ledger for this stage

| claim | grade | evidence |
|---|---|---|
| CC3-1B-RIEMANN — complete Riemann scheme; `z=∞` irregular slope 1/4 (two routes) | **VERIFIED** | exact symbolic indicials + Newton polygon, `2d98e76…` |
| CC3-1B-INFTY-IRREG — `L` irregular at ∞ (slope 1/4, `λ⁴=−256/3`); supersedes "Fuchsian `L`" | **STRUCTURAL+VERIFIED** | Fuchsian test + Newton-polygon dominant balance, `2d98e76…` |
| CC3-1B-LOGFREE — `z=1/3` integer block `{0,1,2}` log-free; `−4/3` isolated; Φ@0 holomorphic log-free | **VERIFIED** | symbolic resonance obstructions `0,0,0` + numeric `≥180 d`, `2d98e76…` / `2ff9da3…` |
| CC3-1B-K-120D — `K = 1.5394948485766…` to ≥120 digits (connection matching) | **VERIFIED** | local-basis matching, interval/dps-stated, `2ff9da3…` |
| CC3-1B-CRED-HARD — `C_EBR = K·(4/3)√π/Γ(7/3)` to **171 digits** (upgrades CC3-1-CRED) | **STRUCTURAL+VERIFIED** | direct `K` × elementary factor vs frozen `C_EBR`, `2ff9da3…` |
| CC3-1B-ROUTEB — Route B (Hadamard) gives same `K` + identical factor (`Γ(7/3)=(4/3)Γ(4/3)`); routes agree | **STRUCTURAL+VERIFIED** | symbolic factor identity + 44-digit `gₙ` Richardson, `78fceee…` |
| CC3-1B-RESCOPE — `0→1/3` is regular-to-regular on a NON-Fuchsian operator; `K`'s home is exponential, not classical KZ; cc3-1c needs irregular rigidity | **VERIFIED (type (e))** | §1.1 + §3 + O5; literature locators in §7 |

**No transcendence claim appears at any grade (ceiling honored).**

---

## 7. GATE verdict & why HALT before cc3-1c

**GATE 0 result: FAIL — `z=∞` is irregular (slope 1/4).** Per the stage START
rule ("HALT for review before cc3-1c ONLY IF a gate fails (∞ irregular, …)"),
this triggers the halt. The reduction-identity gate PASSED (171 digits) and the
routes AGREE — neither of those is a failure; the sole trigger is `∞ irregular`.

**Why the halt is substantive, not bookkeeping.** cc3-1c's registered
prediction **P4** ("`L` not rigid, forced by *rigid irreducible Fuchsian ⇒
motivic (Katz) ⇒ G-function*, contradicting cc3-0") rests on the **Fuchsian**
index of rigidity `χ = (2−#sing)n² + Σ dim Z(M_p)` (Katz, *Rigid Local
Systems*, 1996). That formula and the "rigid ⇒ motivic" implication are
**defined for Fuchsian (regular-singular) systems**. `L` is **not** Fuchsian.
The correct tool is the **irregular index of rigidity** (Bloch–Esnault,
*Local Fourier transforms and rigidity for D-modules*, Asian J. Math. 8 (2004);
Arinkin, *Rigid irregular connections on P¹*, Compositio 146 (2010);
Jakob–Yun, recent work on irregular rigidity), which adds irregularity/Swan-
conductor terms at `∞`. cc3-1c must be re-planned around this before any
rigidity verdict or p-curvature interpretation is issued. **P4a** (p-curvature
non-nilpotent) survives as stated (it is a mod-p test independent of the
Fuchsian/irregular distinction) and can proceed once cc3-1c is re-scoped.

**Literature locators (VERIFIED-by-citation, not silently load-bearing):**
André, *Séries Gevrey de type arithmétique I/II*, Ann. of Math. 151 (2000)
705–740 / 741–756 (G-/E-function dichotomy, cc3-0); Katz, *Rigid Local Systems*,
Ann. Math. Studies 139 (1996) (Fuchsian rigidity — the tool that does **not**
apply); Bloch–Esnault (2004), Arinkin (2010), Jakob–Yun (irregular rigidity —
the tools cc3-1c needs); Fresán–Jossen, *Exponential Motives* (in prep.;
exponential periods — the candidate home for `K`, cc3-2).

---

## 8. Artifacts (untracked, uncommitted, unminted)

| file | role | canonical hash |
|---|---|---|
| `cc3_1b_riemann.py` + `_results.json` | Riemann scheme, GATE 0 (two routes), log structure | `2d98e7623dc7dea6f149303fa708270c3ccc48ae3215e573d2dbd4b7eae9ba81` |
| `cc3_1b_K.py` + `_results.json` | `K` ≥120 d, reduction identity 171 d | `2ff9da32fc16213fe8373ad112e16748576975c6111d86301f72fda90b629d96` |
| `cc3_1b_routeB.py` + `_results.json` | independent Route B, routes-agree gate | `78fceeea4d200a3ba8fe54d87dd103ed0e330abd758aa4d70b0da223f52fe3bf` |
| `REPORT_cc3_1bc.md` | this report | — |
| `claims_cc.jsonl` (MAIN) | +7 CC3-1B-* (52 → 59) | — |

**`repro/` (frozen EBR-III deposit, 45 claims / `9e6f3fa5…`) NOT touched.**

**HALT.** Awaiting review of: the hardened reduction (`2ff9da3…`, 171 digits),
the `∞`-irregular GATE-0 verdict + the "Fuchsian" rescope, the Route A/B
agreement, and the cc3-1c re-plan (irregular index of rigidity). Do **not**
proceed to cc3-1c or cc3-4a until the re-plan is approved.
