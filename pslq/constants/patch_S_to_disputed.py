#!/usr/bin/env python3
"""
One-shot patch: change the S entry in basis_canonical.json from
VERIFIED_VALUE_PROVENANCE_FLAGGED (usable) to DISPUTED_UNRESOLVED (barred).

Run from the repo root:  python pslq\constants\patch_S_to_disputed.py
(or wherever you place it; it targets pslq/constants/basis_canonical.json).

Rationale: the live Zenodo check (DOI 10.5281/zenodo.20455090, latest version)
shows the deposited paper carries S = 0.43770528 (8 digits, Dingle formula) with
NO 2*pi-prefactor correction. The 'v1.1 correction to 0.45790662' that the prior
entry treated as superseding DOES NOT EXIST in the deposit -- a phantom premise.
So S is DISPUTED (which Dingle prefactor is correct is unresolved), not VERIFIED.
Edits ONLY the S entry, the _README rule, and status_legend. Other constants
untouched. Refuses to run if S is already DISPUTED.
"""
import json, sys

PATH = "pslq/constants/basis_canonical.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

consts = data["constants"]
if not any(c.get("name") == "S" for c in consts):
    sys.exit("ERROR: no S entry found at " + PATH)
S_old = next(c for c in consts if c.get("name") == "S")
if S_old.get("status") == "DISPUTED_UNRESOLVED":
    sys.exit("S already DISPUTED_UNRESOLVED; nothing to do.")

new_S = {
    "_comment": ("CORRECTED. Prior framing (0.45790662 / 2*pi correct, 0.43770528 "
                 "retracted) rested on a PHANTOM premise: a supposed v1.1 "
                 "correction to 2*pi. The live Zenodo check (DOI "
                 "10.5281/zenodo.20455090, latest version) shows the deposited "
                 "paper carries 0.43770528 (8 digits, Dingle formula) with NO "
                 "2*pi correction. That correction does not exist in the deposit. "
                 "S is therefore DISPUTED, not resolved."),
    "name": "S",
    "name_descriptive": "S_vquad_stokes",
    "status": "DISPUTED_UNRESOLVED",
    "usable_in_basis": False,
    "_usable_rationale": ("BARRED until the correct Dingle prefactor is established "
                          "from the derivation. A value disputed by ~4.4% cannot "
                          "be a trustworthy PSLQ basis member."),
    "dispute": {
        "deposited_value": "0.43770528",
        "deposited_convention": ("Dingle late-term formula as PUBLISHED; consistent "
                                 "with Gamma(beta_exp) = -6.00599"),
        "deposited_source": ("Zenodo DOI 10.5281/zenodo.20455090, latest version "
                             "abstract: 'The Stokes constant S = 0.43770528... is "
                             "computed to eight digits by the Dingle late-term "
                             "formula.' No 2*pi-prefactor correction in the deposit."),
        "recompute_value": "0.4579066231690176361190978425482258379624",
        "recompute_convention": "2*pi = 6.28319 prefactor",
        "recompute_stability": "46 digits; two independent reimplementations agree to 20",
        "prefactor_ratio": ("2*pi / |Gamma(beta_exp)| = 1.04615 (~4.4%) = exactly "
                            "0.457906/0.437705; the two differ ONLY by the prefactor"),
        "what_is_known": ("Both values are correctly computed from their respective "
                          "conventions. What is NOT established is which prefactor is "
                          "the correct Dingle normalization for THIS ODE."),
        "why_unresolved": ("Needs the actual Dingle late-term derivation for this ODE "
                           "(beta_exp=-1/(3*sqrt3), xi0=2/sqrt3), NOT a general '2*pi "
                           "is usually universal' heuristic. The earlier 2*pi "
                           "preference was reinforced by the now-disproven phantom "
                           "v1.1 premise."),
        "two_outcomes": [
            "If 2*pi correct: the DEPOSITED PAPER has an error (0.43770528 should be "
            "0.45790662) and needs a correction.",
            "If Gamma(beta_exp) correct: the deposited paper is fine and the session's "
            "earlier 'retracted v1.0' framing was itself the error."
        ],
        "resolution_path": ("Establish the correct Dingle prefactor from the "
                            "derivation (fresh-session math task). NOT resolvable by "
                            "Zenodo lookup (done) or by heuristic.")
    },
    "shared_amplitude_K": "0.0728781025518669641294423633297",
    "K_note": "K itself is NOT disputed (46 digits stable); only the prefactor is.",
    "definition_source": ("Dingle late-term formula S = prefactor * K, K = lim "
                          "|a_n * xi0^(n+beta) / ((-1)^n * Gamma(n+beta))|, "
                          "beta=-1/(3*sqrt3), xi0=2/sqrt3; recomputed by "
                          "recompute_basis.py and S_prefactor_verify.py"),
    "defining_object": "V_quad quadratic PCF, Stokes constant via Dingle late-term amplitude",
    "thread_a_caveat": ("The earlier thread-A confirmation run used 0.45790662; any "
                        "such result must be re-examined once the dispute is resolved. "
                        "A Gamma/period-basis NULL is likely prefactor-robust, but do "
                        "not assume."),
    "sha256_of_value_string": "DISPUTED - no single canonical value string"
}

for i, c in enumerate(consts):
    if c.get("name") == "S":
        consts[i] = new_S
        break

data["_README"] = (data["_README"].rstrip() +
    " UPDATE 2026-06-03: the S entry is now DISPUTED_UNRESOLVED and BARRED (the "
    "prior 'usable' framing rested on a phantom v1.1-correction premise disproven "
    "by the live Zenodo check). Count: 9/10 VERIFIED, 1 DISPUTED (S).")

data["status_legend"]["DISPUTED_UNRESOLVED"] = (
    "recompute and deposited value disagree by a prefactor/convention choice not "
    "settled - BARRED, needs resolution from the derivation")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

with open(PATH, encoding="utf-8") as f:
    check = json.load(f)
print("PATCH OK. File parses. Status by constant:")
for c in check["constants"]:
    if "name" in c:
        print("  %-8s %s" % (c["name"], c.get("status")))
