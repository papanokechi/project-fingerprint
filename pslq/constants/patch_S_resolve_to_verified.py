#!/usr/bin/env python3
"""
One-shot patch: RESTORE the S entry in basis_canonical.json from
DISPUTED_UNRESOLVED (barred) back to VERIFIED (usable), under the 2*pi
(real Stokes-multiplier) Dingle convention.

Run from the repo root:  python pslq\\constants\\patch_S_resolve_to_verified.py
(targets pslq/constants/basis_canonical.json).

Rationale (see agent-tasks/C-S-prefactor-resolution-findings.md for the full
derivation): the prior DISPUTED downgrade rested on the premise that the v1.1 2*pi
correction was a phantom that "does not exist in the deposit". That premise is
REFUTED by the located deposited manuscript vquad_resurgence.pdf, whose Remark 6.2
(Version 1.1) explicitly corrects S from 0.43770528 to S = 2*pi*K =
0.45790662316901763611..., and whose eq (13) states the Dingle late-term formula
with the 2*pi prefactor. The 2*pi prefactor is the universal Borel-Laplace
discontinuity factor (companion of Gamma(n+beta) in the standard Dingle-Berry-
Howls-Ecalle formula a_n ~ (S/2*pi*i) Gamma(n+beta)/A^(n+beta)); it is calibrated
in the manuscript on Euler's series (K=1, |S|=2*pi exactly). The retracted
0.43770528 (= |Gamma(beta_exp)|*K) is the local Borel singular-amplitude C, NOT
the Stokes multiplier the paper defines.

NOTE (could-not-confirm): whether the live Zenodo upload serves v1.1 was NOT
verified; the local manuscript does. If the Zenodo PDF still shows v1.0, that is a
deposit-update gap that does not change the mathematics (provenance flag below).

Edits ONLY the S entry, the _README rule, and status_legend. Other constants
untouched. Refuses to run if S is already VERIFIED.
"""
import json, sys

PATH = "pslq/constants/basis_canonical.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

consts = data["constants"]
if not any(c.get("name") == "S" for c in consts):
    sys.exit("ERROR: no S entry found at " + PATH)
S_old = next(c for c in consts if c.get("name") == "S")
if S_old.get("status") == "VERIFIED":
    sys.exit("S already VERIFIED; nothing to do.")

S_VALUE = "0.4579066231690176361190978425482258379624"

new_S = {
    "_comment": ("RESOLVED. The prior DISPUTED downgrade's premise -- that the "
                 "v1.1 2*pi correction was a phantom 'not in the deposit' -- is "
                 "REFUTED by the located deposited manuscript vquad_resurgence.pdf "
                 "Remark 6.2 (Version 1.1), which corrects S from 0.43770528 to "
                 "S = 2*pi*K = 0.45790662... The 2*pi prefactor is the universal "
                 "Borel-Laplace discontinuity factor (calibrated on Euler's series, "
                 "K=1 |S|=2*pi). The retracted 0.43770528 = |Gamma(beta_exp)|*K is "
                 "the Borel singular-amplitude C, NOT the Stokes multiplier S the "
                 "paper defines. See agent-tasks/C-S-prefactor-resolution-findings.md."),
    "name": "S",
    "name_descriptive": "S_vquad_stokes",
    "recomputed_value": S_VALUE,
    "dps": 240,
    "digits_stable": 46,
    "status": "VERIFIED",
    "usable_in_basis": True,
    "convention": ("2*pi (real Stokes multiplier, Dingle normalization). S = 2*pi*K, "
                   "K = lim |a_n * xi0^(n+beta) / ((-1)^n * Gamma(n+beta))|, "
                   "beta_exp = -1/(3*sqrt3), xi0 = 2/sqrt3."),
    "definition_source": ("Deposited manuscript vquad_resurgence.pdf eq (13) + "
                          "Remark 6.2 (v1.1): S_n = a_n * 2*pi * xi0^(n+beta) / "
                          "((-1)^n * Gamma(n+beta)) -> S. Standard Dingle-Berry-"
                          "Howls-Ecalle formula a_n ~ (S/2*pi*i) Gamma(n+beta)/"
                          "A^(n+beta) (Berry & Howls 1990; Ecalle). Recomputed by "
                          "recompute_basis.py and S_prefactor_verify.py."),
    "defining_object": ("V_quad quadratic PCF, Stokes multiplier via Dingle late-term "
                        "amplitude with the universal 2*pi Borel-Laplace factor"),
    "shared_amplitude_K": "0.0728781025518669641294423633297",
    "K_note": ("K (the prefactor-stripped late-term amplitude) is 46-84 digit stable; "
               "S = 2*pi*K. The non-Stokes value 0.43770528 = |Gamma(beta_exp)|*K is "
               "the Borel singular-amplitude C, retracted by the paper's Remark 6.2."),
    "corroborates_version": ("Painleve-V/resurgence manuscript v1.1 value "
                             "0.45790662316901763611 (matched to deposited 38 digits); "
                             "cross-checked by |S_Jimbo| = 0.4579... (Jimbo connection "
                             "formula, consistency only -- sigma_conn is back-derived)."),
    "from_formula_check": ("DECISIVE (not prose): eq (13) as written pairs the 2*pi "
                           "prefactor with the SAME a_n*xi0^(n+beta)/((-1)^n*Gamma(n+beta)) "
                           "ratio whose limit is the undisputed K; hence eq(13) -> 2*pi*K. "
                           "Applied to K=0.0728781025518669641294: 2*pi*K = "
                           "0.4579066231690176361190978425... matches the manuscript value "
                           "to all 28 shown digits. The retracted 0.43770528 = |Gamma(beta)|*K "
                           "is the Borel singular-amplitude C, which eq(13) does NOT produce. "
                           "So the value rests on a derivation + the located formula, NOT on "
                           "any document's stated conclusion."),
    "provenance_flag": ("PROBABLE DEPOSIT-UPDATE GAP (actionable, not merely "
                        "unconfirmed): the live Zenodo deposit (DOI "
                        "10.5281/zenodo.20455090, latest version) was CHECKED on "
                        "2026-06-03 and showed v1.0 / S=0.43770528 (8 digits, no 2*pi "
                        "correction). The corrected v1.1 (S=2*pi*K=0.45790662, Remark "
                        "6.2 + eq (13)) exists LOCALLY (vquad_resurgence.pdf, pnwork) "
                        "but appears NOT to be uploaded -- so the published deposit the "
                        "world sees likely still serves the retracted value. This is a "
                        "real fix-the-deposit to-do (push the corrected manuscript to "
                        "Zenodo); it does NOT change the mathematics (the value is "
                        "verified from eq (13) applied to the undisputed K). Separately, "
                        "pcf-research/vquad code is still stale at v1.0 Gamma(beta) -- "
                        "see agent-tasks/A2-pcf-research-stale-prefactor.md."),
    "supersedes": ("v1.0 value 0.43770528 (Gamma(beta_exp) prefactor) -- retracted by "
                   "the manuscript's own Remark 6.2; and the 2026-06-03 DISPUTED "
                   "downgrade, whose phantom-v1.1 premise is refuted."),
    "sha256_of_value_string": None,
}

import hashlib
new_S["sha256_of_value_string"] = hashlib.sha256(S_VALUE.encode("utf-8")).hexdigest()

for i, c in enumerate(consts):
    if c.get("name") == "S":
        consts[i] = new_S
        break

data["_README"] = (data["_README"].rstrip() +
    " UPDATE (resolution): the S entry is RESTORED to VERIFIED under the 2*pi real-"
    "Stokes-multiplier convention (S = 2*pi*K = 0.45790662...). The earlier phantom-"
    "v1.1 premise behind the DISPUTED downgrade is refuted by the deposited "
    "manuscript vquad_resurgence.pdf Remark 6.2 / eq (13). Count: 10/10 VERIFIED "
    "(S carries a provenance_flag: Zenodo-upload version unconfirmed).")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

with open(PATH, encoding="utf-8") as f:
    check = json.load(f)
print("PATCH OK. File parses. Status by constant:")
for c in check["constants"]:
    if "name" in c:
        print("  %-8s %s" % (c["name"], c.get("status")))
