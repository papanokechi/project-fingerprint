# EBR-IV — OPERATOR RUNBOOK

Every step below is **operator-executed**. The agent prepared all artifacts to a
ready state and stopped; nothing here has been run, committed, minted, moved,
deleted, or submitted. Run the steps **in order**. Do not skip the pre-flight.

Working root: `C:\LocalWork\project-fingerprint`
Artifact root: `sectorial\cc_transcendence\`

Pinned facts to confirm against:
- paper PDF SHA-256 = `afa69197ce7b53003c561ca717dd6365ac021e869c9f692ce1c293e07c22382b`
- claims-ledger snapshot (92 claims) SHA-256 = `a168f2f791883fc6aaf7144154c6436d852cbed7cad405e039930f682680297f`
- conditional-theorem result (canonical) = `1b15e7ac9a503c30e1cdae8a736677b401c2f1d8c815a2e02a2e0f18908fbfdd`
- period-matrix / kappa channel C (canonical) = `56adcb100d841756d24babb9017bbbb718887a6fc48d301ac45ba1594b3e7fb4`
- kappa-bridge (canonical) = `2cc2f6fb8f0c710496d021a321f710f8a15753f66bbeaf2e1d321beb5a73d9d3`

**EBR-IV introduces no new Lean core.** The four PROVEN Lean cores are EBR-III's;
they are verified by the EBR-III runbook (`repro/lean/cc4_cores`) and are cited
here, not rebuilt. EBR-IV's finitary identities are flagged as Lean-core
candidates for a later pass.

---

## 0. Pre-flight verification (read-only; safe)

```powershell
cd C:\LocalWork\project-fingerprint\sectorial\cc_transcendence\repro_ebr4
python verify.py                      # expect: ALL CHECKS PASS, exit 0
#   (14 results JSONs self-verify against their canonical_sha256; all file
#    hashes in HASH_MANIFEST.json match; claims_cc.jsonl present at package root)

# confirm the paper hash:
cd ..\draft
(Get-FileHash ebr4_v0.pdf -Algorithm SHA256).Hash.ToLower()
#   -> must equal afa69197ce7b53003c561ca717dd6365ac021e869c9f692ce1c293e07c22382b

# confirm the MAIN ledger snapshot hash (92 claims):
cd ..
(Get-FileHash claims_cc.jsonl -Algorithm SHA256).Hash.ToLower()
#   -> must equal a168f2f791883fc6aaf7144154c6436d852cbed7cad405e039930f682680297f
```

If any check fails, STOP and re-run the relevant reproducer; do not proceed.

**Do not touch** `sectorial\cc_transcendence\repro\` — that is the **FROZEN**
EBR-III package (45-claim ledger, snapshot `9e6f3fa5…`). It must remain
byte-identical. All EBR-IV reproduction lives in `repro_ebr4\`.

---

## 1. Git: stage and commit (you run this — the agent is barred)

Optional: keep LaTeX/Python build cruft out of the tree.

```powershell
cd C:\LocalWork\project-fingerprint
# (only if you maintain a .gitignore for this subtree)
Add-Content sectorial\cc_transcendence\.gitignore @"
draft/*.aux
draft/*.log
draft/*.out
**/__pycache__/
"@
```

Explicit add list (EBR-IV substantive artifacts — the cc-3/ebr4 reproducers and
results, the reports, the MAIN ledger, the paper, the EBR4 drafting/referee/
venue/runbook/Zenodo artifacts, and the EBR-IV repro package):

```powershell
cd C:\LocalWork\project-fingerprint
git add `
  sectorial/cc_transcendence/cc3_*.py `
  sectorial/cc_transcendence/cc3_*_results.json `
  sectorial/cc_transcendence/ebr4_*.py `
  sectorial/cc_transcendence/ebr4_*_results.json `
  sectorial/cc_transcendence/REPORT_cc3_*.md `
  sectorial/cc_transcendence/cc3_2_entry_dossier.md `
  sectorial/cc_transcendence/claims_cc.jsonl `
  sectorial/cc_transcendence/draft/ebr4_v0.tex `
  sectorial/cc_transcendence/draft/ebr4_v0.pdf `
  sectorial/cc_transcendence/draft/EBR4_outline.md `
  sectorial/cc_transcendence/draft/EBR4_claim_trace.md `
  sectorial/cc_transcendence/draft/EBR4_drafting_log.md `
  sectorial/cc_transcendence/draft/EBR4_referee_findings.md `
  sectorial/cc_transcendence/draft/EBR4_venue_memo.md `
  sectorial/cc_transcendence/draft/EBR4_zenodo_metadata.json `
  sectorial/cc_transcendence/draft/OPERATOR_RUNBOOK_ebr4.md `
  sectorial/cc_transcendence/repro_ebr4

git status                            # review what is staged
```

Do **not** stage: `draft/ebr4_v0.aux`, `draft/ebr4_v0.log`,
`draft/ebr4_v0.out`, any `__pycache__/`. Do **not** stage or modify anything
under `sectorial/cc_transcendence/repro/` (FROZEN EBR-III).

Commit (message draft — edit freely):

```
EBR-IV: the EBR growth constant on Painleve III(D8); SL(2) monodromy and a
conditional transcendence theorem

Self-contained paper + reproducibility package for op:ebr4-assemble.
- H_2 (Borel-2 reduction of the OGF) has singular set {0, infinity}, both
  irregular slope 1/2; index of rigidity 0 (non-rigid, moduli dim 2); local
  type (2,2) selects the Sakai surface D_8^(1) = PIII(D_8) under RULE S.
- Differential Galois group G_Gal(H_2) = SL(2) (exact Kovacic); irreducible,
  no Liouvillian solutions.
- kappa realised constructively as the connection coefficient A_Phi of an
  order-4 operator (slope-1/4 irregular point), to 129 digits, three
  independent channels; kappa = Gamma(4/3)*A_0, an exponential period.
- Monodromy point (tr M_0, kappa), tr M_0 = -51.0655631399546...; survey of the
  solved D_8 connection problems returns NOT COVERED (tau-side vs Lax-side);
  two positive-control-validated integer-relation nulls; off the algebraic
  PIII(D_8) locus.
- Conditional theorem: under the Fresan-Jossen period conjecture, a
  differential-to-motivic comparison, and a verified non-degeneracy datum,
  kappa not in Q-bar, hence C transcendental. Four graded hypotheses, gap list.
- No new Lean core (the four PROVEN cores are EBR-III's, cited).
- Unconditional transcendence of C/kappa remains CONJECTURED; the conditional
  theorem is the program ceiling and the ceiling cuts both ways.

Paper PDF sha256 afa69197ce7b53003c561ca717dd6365ac021e869c9f692ce1c293e07c22382b
Ledger snapshot sha256 a168f2f791883fc6aaf7144154c6436d852cbed7cad405e039930f682680297f

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

```powershell
git commit -F <your-message-file>
# git push origin <branch>        # only if/when you choose to push
```

---

## 2. Zenodo deposit (IRREVERSIBLE on publish — operator only)

Metadata is prepared at
`sectorial\cc_transcendence\draft\EBR4_zenodo_metadata.json`
(legacy deposition-API shape: `{ "metadata": { ... } }`, v1.0, creator
Papanokechi / ORCID 0009-0000-6192-8273, license cc-by-4.0).

> **Underscore keys are operator-only.** `_operator_todo` and `_provenance` are
> annotations; the siarc `_zenodo_uploader.py` `clean_meta` step strips all
> `_`-prefixed keys before the API call. If you mint via the web UI, simply
> ignore them (but **read `_operator_todo` first** — it carries the EBR-III-DOI
> insertion step).

> **AT MINT — EBR-III concept DOI.** EBR-III's concept DOI was **not yet minted**
> at packaging time (`EBR4_outline.md:41` "[operator fills at mint]"). When you
> mint, add it to `related_identifiers` as **two** entries — relation
> **is continuation of** and relation **cites** — and add it to the `notes`
> lineage line. The validated array currently links only EBR-I
> (`10.5281/zenodo.20564079`), EBR-II (`10.5281/zenodo.20566465`), and the
> V_quad/D5 companion (`10.5281/zenodo.20455089`, relation **references**).

**Files to upload to the record:**
- `draft/ebr4_v0.pdf` (the paper)
- a zipped copy of `repro_ebr4/` (the reproducibility package)

### Option A — web UI (recommended)
1. Log in to Zenodo as Papanokechi.
2. New upload → upload `ebr4_v0.pdf` and `repro_ebr4.zip`.
3. Fill the form from `EBR4_zenodo_metadata.json` (title, author+ORCID,
   description HTML, keywords, license CC-BY-4.0, version v1.0).
4. Related identifiers: EBR-I + EBR-II + **EBR-III (fill the minted concept
   DOI)** as **is continuation of** and **cites**; V_quad `10.5281/zenodo.20455089`
   as **references**.
5. Save as **draft**; review the rendered preview. Publishing mints a DOI and is
   **irreversible** — publish only when you are certain.

### Option B — API (scripted)
```powershell
# requires a personal access token with deposit:write
$tok = "<ZENODO_TOKEN>"
$body = Get-Content sectorial\cc_transcendence\draft\EBR4_zenodo_metadata.json -Raw
# strip the _-prefixed keys first (or use _zenodo_uploader.py prepare/execute,
# which does this for you). Then: 1) create deposition, 2) PUT metadata,
# 3) upload files to the bucket, 4) POST .../actions/publish  <-- IRREVERSIBLE.
```

> **STANDING RULE — §B-entry-in-the-same-session-as-the-mint.** The moment you
> publish, capture the minted **concept DOI** and **version (record) DOI** and
> write the Zenodo `§B` entry in
> `OneDrive\…\siarc\submitted\submission_log.txt` **in the same working
> session**, then regenerate `submission_log.html` via
> `_build_submission_html.py`. Do not defer it — an un-logged mint is how a DOI
> goes stale in the ledger.

---

## 3. Journal submission (operator only)

See `EBR4_venue_memo.md` for the full ranked shortlist and the per-venue
reasoning. Headlines:

- **Primary: Constructive Approximation** (Springer). Highest-fit FREE venue
  with **no all-math-flagship comparative-priority gate and no program
  adjacency**. Lead the cover letter with the isomonodromy/period **structure**
  (the D8 identification under RULE S, the kappa-bridge, the three channels),
  **not** the transcendence headline — the result is conditional and the paper
  says so.
- **High-tier alternative: CMP**, only after an **R3 pre-fire realistic-ceiling
  check** (Q-216-2). CMP is the operator's own post-Nonlinearity cascade target
  for this program and the home of the ILP/GL isomonodromy literature; it is
  clear of the sibling (V_quad is at SIGMA, not CMP).
- **Fallbacks:** IMRN (flagship, R3 check) → Letters in Math. Phys. → J. Phys. A.

**Do NOT submit to:**
- **Nonlinearity** — it **desk-rejected the directly-adjacent V_quad/doubly-degenerate PV, Sakai D5^(1), W(A3^(1)) [superseded PIII(D6); corrected LOG-PV-01, 2026-08-03]
  sibling** (ms NON-110708, 28 Apr 2026, content-mute). Same program, same
  desk-screen risk.
- **Experimental Mathematics** (BLACKLISTED), **NNTDM** (blocked).
- **Acta Arithmetica** (Item 17 rejected, cooldown ≥2027-02), **Ramanujan
  Journal** (Item 32 rejected, theorem-deficit).

**Occupied (do not stack a second concurrent submission):**
- **SIGMA** — the V_quad/doubly-degenerate PV, Sakai D5^(1), W(A3^(1)) [superseded PIII(D6); corrected LOG-PV-01, 2026-08-03] **sibling** is live there (Item 35, since
  1 Jun 2026). SIGMA becomes a strong option **once V_quad resolves**, not before.
- **JMP** (WKB-Newton-polygons paper, pending) and **JDE** (active review).

Submission mechanics:
1. Confirm the chosen venue is still FREE and no concurrent-submission conflict
   exists (R7 dup-audit).
2. Portal → new submission; upload `ebr4_v0.pdf` (or .tex if source requested).
3. Cover letter: state it is a preprint deposited at Zenodo (cite the DOI minted
   in §2); foreground the external isomonodromy/period anchors (André, Sakai,
   ILP, GL, Fresán–Jossen) to pre-empt the self-citation (`external_validation_
   deficit`) read; state that PROVEN is reserved for the (EBR-III) Lean cores
   and that transcendence is explicitly **conditional**.
4. **GenAI disclosure:** include the publisher's required statement that an AI
   assistant was used for drafting/derivation under author supervision and that
   all mathematical content was verified. (An explicit "Use of AI tools"
   paragraph is in the paper's Acknowledgements.)
5. Record the submission in the ledger (`§A` journal) with a **decision horizon**
   (≈3 wk no-ack → courtesy query; ≈6 mo no movement → withdraw and re-route),
   then rebuild the HTML.

---

## 4. What the agent did NOT do (your responsibility)
- No `git add` / `commit` / `push` / `tag`.
- No file moves or deletions.
- No Zenodo create / upload / publish.
- No journal submission.
- Did not touch the FROZEN `repro/` (EBR-III) package.

---

## 5. Standing reminders
- **Transcendence of the EBR connection coefficient C / the growth constant κ
  remains CONJECTURED unconditionally.** The conditional theorem (κ ∉ ℚ̄ under
  H1–H4) is the program's ceiling, and **the ceiling cuts both ways**: a closed
  form would have argued elementarity-in-an-extended-class, and a null proves
  neither direction.
- **Synthesis-thread flag (for your judgment, not an action item).** Both program
  constants — V_quad's Stokes constant on `D_5^(1)` and the present κ on
  `D_8^(1)` — are Stokes data of rank-2 Painlevé Lax operators on different
  Sakai surfaces. Whether the surface type a PCF's growth constant lands on
  predicts the arithmetic of that constant is recorded as the open-problem
  pointer in the paper and in `cc3_2_entry_dossier.md`; it is the candidate
  spine of a post-EBR-IV synthesis paper, not EBR-IV's burden.
