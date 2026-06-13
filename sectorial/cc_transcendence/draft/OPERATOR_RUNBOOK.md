# EBR-III — OPERATOR RUNBOOK

Every step below is **operator-executed**. The agent prepared all artifacts to a
ready state and stopped; nothing here has been run, committed, minted, or
submitted. Run the steps **in order**. Do not skip the pre-flight.

Working root: `C:\LocalWork\project-fingerprint`
Artifact root: `sectorial\cc_transcendence\`

Pinned facts to confirm against:
- paper PDF SHA-256 = `32e6f216da6c18daeb6eb7159ec68bc046c366defe33b89a8ab1fb6af8e445f1`
- claims-ledger snapshot SHA-256 = `9e6f3fa5a2986cce8edddaad5945e9da4008ea637c1b5c6d5b1fa9691362f6bb`
- integer-relation null SHA-256 = `9a3f942def64737dd0bfc00495077f99ea7fe1ae5110982e343d8e12d5f7bcaf`

---

## 0. Pre-flight verification (read-only; safe)

```powershell
cd C:\LocalWork\project-fingerprint\sectorial\cc_transcendence\repro
python verify.py                      # expect: ALL CHECKS PASS, exit 0
cd lean\cc4_cores
lake build                            # expect: clean build
Get-Content AXIOM_AUDIT.txt           # expect: cones in {propext,Classical.choice,Quot.sound}; no sorryAx
# confirm the paper hash:
cd ..\..\paper
(Get-FileHash ebr3_v1.pdf -Algorithm SHA256).Hash.ToLower()
#   -> must equal 32e6f216da6c18daeb6eb7159ec68bc046c366defe33b89a8ab1fb6af8e445f1
```

If any check fails, STOP and re-run the relevant reproducer; do not proceed.

---

## 1. Git: stage and commit (you run this — the agent is barred)

Optional but recommended: keep LaTeX/Python build cruft out of the tree.

```powershell
cd C:\LocalWork\project-fingerprint
# (only if you maintain a .gitignore for this subtree)
Add-Content sectorial\cc_transcendence\.gitignore @"
draft/*.aux
draft/*.log
draft/*.out
draft/*.txt
**/__pycache__/
repro/lean/cc4_cores/.lake/
lean/cc4_cores/.lake/
"@
```

Explicit add list (the substantive artifacts — sources, PDF, repro package,
reports, ledger, drafting/referee/venue/runbook artifacts, Zenodo metadata):

```powershell
cd C:\LocalWork\project-fingerprint
git add `
  sectorial/cc_transcendence/*.py `
  sectorial/cc_transcendence/*.json `
  sectorial/cc_transcendence/*.jsonl `
  sectorial/cc_transcendence/REPORT_*.md `
  sectorial/cc_transcendence/ERRATUM_cc4_narration.md `
  sectorial/cc_transcendence/OP_CC2_PROMPT.txt `
  sectorial/cc_transcendence/draft/ebr3_v1.tex `
  sectorial/cc_transcendence/draft/ebr3_v1.pdf `
  sectorial/cc_transcendence/draft/EBR3_*.md `
  sectorial/cc_transcendence/draft/EBR3_zenodo_metadata.json `
  sectorial/cc_transcendence/draft/OPERATOR_RUNBOOK.md `
  sectorial/cc_transcendence/lean/cc4_cores/Audit.lean `
  sectorial/cc_transcendence/lean/cc4_cores/Cc4Cores.lean `
  sectorial/cc_transcendence/lean/cc4_cores/AXIOM_AUDIT.txt `
  sectorial/cc_transcendence/lean/cc4_cores/lakefile.toml `
  sectorial/cc_transcendence/lean/cc4_cores/lean-toolchain `
  sectorial/cc_transcendence/lean/cc4_cores/lake-manifest.json `
  sectorial/cc_transcendence/repro

git status                            # review what is staged
```

Do **not** stage: `draft/*.aux`, `draft/*.log`, `draft/*.out`, `draft/*.txt`,
any `__pycache__/`, or `.lake/` oleans.

Commit (message draft — edit freely):

```
EBR-III: d=2 EBR operator is not a G-operator; differential Galois group SL(4)

Self-contained paper + reproducibility package for op:ebr3-assemble.
- Not-a-G-function (normalization-scoped): denominator growth, p-curvature,
  Katz/irregular-infinity trichotomy.
- L_2 irreducible and minimal (two routes); M_R semisimple pseudo-reflection
  {1,1,1,e^{i pi/3}} (supersedes the retired "resonance log" reading).
- Main theorem (STRUCTURAL, bound-complete): G_Gal(L_2)^0 = SL(4) via 8/8
  Aschbacher maximal-subgroup elimination; corollary: no Liouvillian solutions.
- Connection coefficient to 169 digits (third channel); integer-relation
  battery ALL-NULL at 169 digits with fired positive controls.
- Four Lean 4 / Mathlib cores, axiom cones audited (the only PROVEN items).
- Transcendence of the connection coefficient remains CONJECTURED; sole route
  is op:cc-3 (period analysis, post-Andre).

Paper PDF sha256 32e6f216da6c18daeb6eb7159ec68bc046c366defe33b89a8ab1fb6af8e445f1
Ledger snapshot sha256 9e6f3fa5a2986cce8edddaad5945e9da4008ea637c1b5c6d5b1fa9691362f6bb

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

```powershell
git commit -F <your-message-file>
# git push origin <branch>        # only if/when you choose to push
```

---

## 2. Zenodo deposit (IRREVERSIBLE on publish — operator only)

Metadata is prepared at
`sectorial\cc_transcendence\draft\EBR3_zenodo_metadata.json`
(legacy deposition-API shape: `{ "metadata": { ... } }`, v1.0, creator
Papanokechi / ORCID 0009-0000-6192-8273, license cc-by-4.0, EBR-I/II concept
DOIs linked as `isContinuationOf` + `cites`).

**Files to upload to the record:**
- `draft/ebr3_v1.pdf` (the paper)
- a zipped copy of `repro/` (the reproducibility package)

### Option A — web UI (recommended for the first mint)
1. Log in to Zenodo as Papanokechi.
2. New upload → upload `ebr3_v1.pdf` and `repro.zip`.
3. Fill the form from `EBR3_zenodo_metadata.json` (title, authors+ORCID,
   description HTML, keywords, license CC-BY-4.0, version v1.0).
4. Related/alternate identifiers: add
   `10.5281/zenodo.20564079` (EBR-I) and `10.5281/zenodo.20566465` (EBR-II),
   relation **is continuation of** (and **cites**).
5. Save as **draft**; review the rendered preview. Publishing mints a DOI and is
   **irreversible** — publish only when you are certain.

### Option B — API (only if you prefer scripted minting)
```powershell
# requires a personal access token with deposit:write
$tok = "<ZENODO_TOKEN>"
$body = Get-Content sectorial\cc_transcendence\draft\EBR3_zenodo_metadata.json -Raw
# 1) create deposition, 2) PUT metadata from $body, 3) upload files to the
#    bucket, 4) POST .../actions/publish  <-- IRREVERSIBLE; do last, deliberately.
```
Capture the minted concept DOI and version DOI; record both in the submission
ledger (`OneDrive\...\siarc\submitted\submission_log.txt`, §B Zenodo) and
regenerate `submission_log.html` via `_build_submission_html.py`.

---

## 3. Journal submission (operator only)

**Primary: Journal of Symbolic Computation (JSC), Elsevier.**
Fallback: AAECC (Springer). See `EBR3_venue_memo.md` for the full ranked
shortlist, the JDE concurrent-submission caveat, and the SIGMA direct-PDF flag.

1. Confirm no live submission conflict for JSC (it is currently FREE per the
   venue memo; Ramanujan J / Acta Arithmetica / JDE are occupied — do not
   submit there).
2. Editorial Manager (JSC) → new submission; upload `ebr3_v1.pdf` (or the .tex +
   figures if source is requested).
3. Cover letter: state it is a preprint deposited at Zenodo (cite the minted
   DOI from step 2), that PROVEN is reserved for the Lean cores, and that
   transcendence of the connection coefficient is explicitly left open.
4. **GenAI disclosure:** include Elsevier's required statement that an AI
   assistant was used for drafting/derivation assistance under author
   supervision, and that all mathematical content was verified.
5. Record the submission in the ledger (§A journal) and rebuild the HTML.

---

## 4. What the agent did NOT do (your responsibility)
- No `git add` / `commit` / `push` / `tag`.
- No file moves or deletions outside `sectorial\cc_transcendence\` scratch.
- No Zenodo create/upload/publish.
- No journal submission.

Standing reminder: transcendence of the connection coefficient C remains
**CONJECTURED**. Its sole remaining route is **op:cc-3** (period analysis,
post-André). EBR-III makes no transcendence claim.
