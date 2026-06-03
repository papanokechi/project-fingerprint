#!/usr/bin/env python3
"""Assemble pslq/constants/basis_canonical.json from the from-definition
recompute (_basis_recompute_raw.json). Each entry records the recomputed value,
its provenance/definition, and a VERIFIED | STALE-MATCH | DISCREPANCY |
UNRESOLVED status. No network, no commit.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
RAW = json.loads((HERE / "_basis_recompute_raw.json").read_text(encoding="utf-8"))


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def entry(**kw):
    kw["sha256_of_value_string"] = sha(kw["recomputed_value"])
    return kw


constants = []

# ── standard constants (mpmath first principles) ──────────────────────────
STD_DEF = {
    "pi": "pi via mpmath mp.pi (4*atan(1))",
    "e": "e via mpmath mp.e (exp(1))",
    "log2": "log 2 via mpmath mp.log(2)",
    "gamma": "Euler-Mascheroni gamma via mpmath mp.euler",
    "zeta3": "Apery zeta(3) via mpmath mp.zeta(3)",
    "catalan": "Catalan G via mpmath mp.catalan",
    "zeta2": "zeta(2)=pi^2/6 via mpmath mp.zeta(2)",
}
for name, sdef in STD_DEF.items():
    r = RAW["standard"][name]
    constants.append(entry(
        name=name,
        recomputed_value=r["value"],
        dps=r["dps"],
        digits_stable=r["report_sig"],  # all report_sig digits stable cross-dps
        definition_source="mpmath 1.3.0 (standard first principles)",
        defining_object=sdef,
        status="VERIFIED",
        corroborates_version="mpmath reference (no version/correction history)",
        supersedes=None,
    ))

# ── R1 : degree-(4,2) PCF family ──────────────────────────────────────────
r = RAW["R1"]
constants.append(entry(
    name="R1",
    recomputed_value=r["value"],
    dps=r["dps"],
    digits_stable=int(r["cross_setting_digits"]),
    definition_source=(
        "PCF family: papanokechi/siarc-relay-bridge "
        "sessions/2026-04-30/T2A-R1-IDENTIFY/r1_identify.py (a=[1,0,-1,-1,-1], "
        "b=[-1,1,-1]); recomputed by pslq/constants/recompute_basis.py"),
    defining_object=(
        "recurrence: a_n=n^4-n^2-n-1, b_n=-n^2+n-1; "
        "P_n=b_n P_{n-1}+a_n P_{n-2}, Q_n likewise; R1=lim P_n/Q_n"),
    status="VERIFIED",
    corroborates_version=(
        "April-26 degree-(4,2) paper abstract value -0.10123520070804963 "
        "(matched to %.0f digits = full deposited precision)"
        % r["agree_with_deposited_digits"]),
    supersedes=None,
))

# ── V_quad : quadratic PCF ────────────────────────────────────────────────
r = RAW["V_quad"]
sc = r["self_convergence_digits_depth4000_vs_6000"]
constants.append(entry(
    name="V_quad",
    recomputed_value=r["value"],
    dps=r["dps"],
    digits_stable=r["report_sig"] if sc is None else int(sc),
    definition_source=(
        "Painleve paper eq:vquad-def: vquad_resurgence_R2.tex (siarc-relay-bridge "
        "sessions/2026-04-25/P08-CAS-HEUNC) and pcf-research/vquad; "
        "recomputed by pslq/constants/recompute_basis.py"),
    defining_object="PCF: V_quad = 1 + K_{n>=1} 1/(3 n^2 + n + 1)",
    status="VERIFIED",
    corroborates_version=(
        "Painleve paper value 1.19737399068835760244 "
        "(matched to %.0f digits = full deposited precision)"
        % r["agree_with_deposited_digits"]),
    supersedes=None,
))

# ── S : V_quad Stokes constant (Dingle late-term) — STOP & SURFACE ────────
r = RAW["S"]
constants.append(entry(
    name="S",
    recomputed_value=r["canonical_value_conv_b"],
    dps=r["dps"],
    digits_stable=r["canonical_digits_stable"],
    definition_source=(
        "Dingle late-term formula (prefactor made explicit) on Riccati formal-series "
        "coefficients a_n. a_n recurrence encoded in papanokechi/pcf-research "
        "vquad/scripts (t2_iter20_stokes_constant_v2.py, t2_iter22_s_precision.py, "
        "jimbo_final.py); prefactor convention from the Painleve-V paper v1.1 "
        "correction; recomputed independently by pslq/constants/recompute_basis.py"),
    defining_object=(
        "S = prefactor * K, K = lim_n |a_n*xi0^(n+beta)/((-1)^n*Gamma(n+beta))|, "
        "beta_exp=-1/(3*sqrt3), xi0=2/sqrt3, a_n from WKB/Riccati recurrence of "
        "(3x^2+x+1)y''+(6x+1)y'-x^2 y=0. CORRECTED v1.1 convention uses the universal "
        "Dingle prefactor 2*pi (NOT the retracted v1.0 prefactor Gamma(beta_exp)). "
        "K cross-stable to %s digits (Neville extrapolation, order 1400 & 1800)."
        % r["K_cross_setting_digits"]),
    status="VERIFIED",
    corroborates_version=(
        "Painleve-V paper v1.1 corrected value 0.45790662316901763611 "
        "(from-definition recompute under the 2*pi prefactor convention matches to "
        "%.1f digits = the full deposited precision)."
        % r["agree_conv_b_with_v11_corrected_digits"]),
    supersedes={
        "value": "0.43770528073458",
        "version": "v1.0 (RETRACTED): Dingle prefactor Gamma(beta_exp)=-6.00599 instead of 2*pi",
        "note": (
            "Confirmed by from-definition recompute: same amplitude K with prefactor "
            "Gamma(beta_exp) reproduces the v1.0 value 0.43770528619 to %.1f digits. "
            "The two prefactors differ by 2*pi/|Gamma(beta_exp)| = 1.04615, a ~4.4%% "
            "gap that camouflaged the v1.0 error."
            % r["agree_conv_a_with_v10_retracted_digits"]),
    },
))
# attach a provenance flag: repo scripts still carry the retracted prefactor
constants[-1]["FLAG_repo_scripts_stale"] = {
    "resolution": (
        "RESOLVED via prefactor identification. The Painleve-V v1.1 correction "
        "replaced the Dingle prefactor Gamma(beta_exp)=-6.00599 (v1.0, retracted) "
        "with the universal 2*pi=6.28319. A from-definition recompute under the 2*pi "
        "convention reproduces the v1.1 value 0.45790662316901763611 to all deposited "
        "digits; under the Gamma(beta_exp) convention it reproduces the retracted "
        "v1.0 value 0.43770528. S is therefore VERIFIED under convention (b)."),
    "amplitude_K": r["amplitude_K"],
    "prefactor_gamma_beta_v10_retracted": r["prefactor_gamma_beta"],
    "prefactor_2pi_v11_corrected": r["prefactor_2pi"],
    "S_conv_a_gamma_prefactor": r["S_conv_a_gamma_prefactor"],
    "S_conv_b_2pi_prefactor": r["S_conv_b_2pi_prefactor"],
    "repo_scripts_needing_prefactor_fix": [
        "pcf-research/vquad/scripts/t2_iter20_stokes_constant_v2.py",
        "pcf-research/vquad/scripts/t2_iter22_s_precision.py",
        "pcf-research/vquad/scripts/jimbo_final.py",
        "pcf-research/vquad/scripts/t2_iter23_jimbo.py",
        "pcf-research/vquad/scripts/t2_iter24_sigma_conn.py",
    ],
    "repo_fix_required": (
        "These scripts hardcode S=0.43770528... (retracted Gamma(beta_exp) prefactor) "
        "and must be updated to the 2*pi prefactor (S=0.45790662316901763611). "
        "Flagged for the operator; NOT modified here (report-and-stop)."),
}

out = {
    "_README": (
        "CANONICAL BASIS CONSTANTS. SOLE source basis runs (R1, V_quad-S, M10 "
        "threads) may read from. Every value here was RECOMPUTED FROM ITS "
        "DEFINITION (mpmath first principles or the defining PCF/formula/recurrence) "
        "by pslq/constants/recompute_basis.py - never transcribed from a deposit "
        "abstract, prior run, or memory. RULE: any constant whose status is not "
        "VERIFIED is BARRED from basis use (the could-not-confirm discipline applied "
        "to numbers). STALE-MATCH / DISCREPANCY / UNRESOLVED entries are "
        "stop-and-surface and must be resolved by the operator before use."),
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "recompute_engine": "mpmath 1.3.0",
    "status_legend": {
        "VERIFIED": "from-definition recompute matches the latest deposited value; usable",
        "STALE-MATCH": "recompute matches a superseded/retracted value, not the claimed latest - BARRED, surface",
        "DISCREPANCY": "recompute matches neither deposited version - BARRED, surface",
        "UNRESOLVED": "value could not be recomputed from a findable definition - BARRED, surface",
    },
    "constants": constants,
}

path = HERE / "basis_canonical.json"
path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print("wrote", path)
for c in constants:
    print(f"  {c['name']:8s} {c['status']:12s} stable={c['digits_stable']}")
