#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-4a  --  K-TARGETED INTEGER-RELATION RECONNAISSANCE
================================================================================
SIARC.  A structure-motivated PSLQ null battery on the connection constant K
(NOT C):  K = 1.539494848576641...  with  C_EBR = K * (4/3)*sqrt(pi)/Gamma(7/3).

Falsification target: "K is polylog-elementary / a low-height MZV-class constant,
or a genuine MIXED Gamma x polylog combination."  A documented NULL (positive
controls fired, declared heights/dps/detection-threshold/hash) is the deliverable.
A FIRE with nonzero coefficient on K HALTS the op (it would mean K is elementary
after all and reorders the conjecture landscape).

BASIS MOTIVATION (each tier traced to L's structure; cc3-1b/1c):
  * z=0 carries LOGARITHMS (cc3-1c-0: Jordan type [2,2], NOT log-free) and the
    integer-resonant exponents {0,0,1,1} motivate an MZV/polylog-flavoured
    weight-graded basis {1, log3, pi^2, zeta(3), pi^2 log3, log^3 3, Li_k(1/3)}.
  * the z=1/3 exponent -4/3 (and gamma=11/6, exp@R={0,1,2,-11/6}) motivates cubic
    /sextic arguments (Li_k(1/3)) and a Gamma(k/3) family.
  * the s^{1/4} (slope-1/4) structure motivates a weight-2 quartic constant
    (Catalan) in the polylog tier.

SKIPPED BY ARGUMENT (not re-run -- per cc3-4a spec):
  * PURE Gamma(k/3)-monomial relations on K.  Because K = C * [exact
    Gamma/algebraic factor], a pure-Gamma relation on log K is EQUIVALENT to a
    pure-Gamma relation on C, and those were already NULLED at 169 digits by
    ebr3-b (hash 9a3f942d...).  We therefore test only MIXED (Gamma x polylog)
    tiers, which ebr3-b did not cover.
  * A Bessel-moment / Broadhurst-Mellit tier is NOT added: cc3-1c-3 verdict is
    NON-RIGID (no Kloosterman/Airy rigid-catalogue match), so the Kloosterman-
    adjacency that would motivate it does not obtain.

PRECISION POLICY (matches ebr3-b):  the frozen corpus has C to 172 digits and K
to 130 digits (direct connection matching, cc3-1b).  We EXTEND K to ~169 digits
via the EXACT reduction factor K = C*Gamma(7/3)/((4/3)*sqrt(pi)) -- this does NOT
overwrite the frozen 130-digit value (cross-checked to agree to >=128 digits);
it only sharpens detection power.  dps=169, TOL=1e-150 (guard ~19 digits).
Detection threshold: with N reals known to D=169 digits, PSLQ reliably resolves
relations of height up to ~10^(D/N); every tier's declared maxcoeff sits well
inside that bound, so a NULL means "no relation of height <= maxcoeff exists."

CEILING (reproduced):  a Fuchsian relocation does not make K a classical period;
provenance, not singularity type, is what the period conjectures see.
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import mpmath as mp

RELIABLE_DIGITS = 169
mp.mp.dps = RELIABLE_DIGITS
TOL = mp.mpf(10) ** (-150)

# ---- load frozen targets (no transcription) ---------------------------------
with open("cc4_1_connection_results.json", encoding="utf-8") as f:
    conn = json.load(f)
C_EBR = mp.mpf(conn["prefactor_C_EBR"])              # frozen, 172 digits

with open("cc3_1b_K_results.json", encoding="utf-8") as f:
    kres = json.load(f)
K_direct_130 = mp.mpf(kres["K_value_130"])           # frozen, 130 digits (direct)

# EXACT reduction factor (cc3-1b CC3-1B-CRED-HARD): C = K*(4/3)*sqrt(pi)/Gamma(7/3)
gam_7_3 = mp.gamma(mp.mpf(7) / 3)
red_factor = (mp.mpf(4) / 3) * mp.sqrt(mp.pi) / gam_7_3
K = C_EBR / red_factor                               # K extended to ~169 digits

# cross-check the extension against the frozen 130-digit direct value
K_agreement = abs(K - K_direct_130)
assert K_agreement < mp.mpf(10) ** (-125), \
    f"extended K disagrees with frozen direct K_130: {K_agreement}"

# ---- constants ---------------------------------------------------------------
PI  = mp.pi
L2  = mp.log(2)
L3  = mp.log(3)
PI2 = PI ** 2
Z2  = mp.zeta(2)
Z3  = mp.zeta(3)
CAT = mp.catalan
Li2_13 = mp.polylog(2, mp.mpf(1) / 3)
Li3_13 = mp.polylog(3, mp.mpf(1) / 3)
Li2_half = mp.polylog(2, mp.mpf(1) / 2)
G13 = mp.gamma(mp.mpf(1) / 3)
G23 = mp.gamma(mp.mpf(2) / 3)
G16 = mp.gamma(mp.mpf(1) / 6)

def relation(vec, maxcoeff, maxsteps=200000):
    rel = mp.pslq(vec, tol=TOL, maxcoeff=maxcoeff, maxsteps=maxsteps)
    if rel is None:
        return None, None
    resid = abs(sum(mp.mpf(int(c)) * v for c, v in zip(rel, vec)))
    return rel, mp.nstr(resid, 8)

results = {
    "op": "cc3-4a",
    "task_id": "op:cc-transcendence/cc3-1c",
    "objective": ("structure-motivated PSLQ null battery on the connection "
                  "constant K; falsify 'K is polylog-elementary / low-height "
                  "MZV-class / a MIXED Gamma x polylog combination'."),
    "precision_policy": {
        "reliable_digits": RELIABLE_DIGITS,
        "mp_dps": mp.mp.dps,
        "tol": "1e-150",
        "guard_digits": RELIABLE_DIGITS - 150,
        "K_source": ("EXTENDED from frozen 172-digit C via exact factor "
                     "K = C*Gamma(7/3)/((4/3)*sqrt(pi)); does NOT overwrite the "
                     "frozen 130-digit direct value"),
        "K_extension_vs_frozen_direct_residual": mp.nstr(K_agreement, 6),
        "detection_threshold_note": ("with N reals known to 169 digits PSLQ "
                     "reliably resolves relations of height <= ~10^(169/N); each "
                     "tier's maxcoeff sits inside this bound, so a NULL means no "
                     "relation of height <= maxcoeff exists."),
    },
    "skipped_by_argument": {
        "pure_gamma_monomial": ("K = C*[exact Gamma/algebraic factor] => a pure "
                     "Gamma(k/3) relation on log K is equivalent to one on C, "
                     "already NULLED at 169 digits by ebr3-b (9a3f942d...). Only "
                     "MIXED tiers are new."),
        "bessel_moment_tier": ("not added: cc3-1c-3 is NON-RIGID, no Kloosterman/"
                     "Airy rigid-catalogue match, so Broadhurst-Mellit Bessel-"
                     "moment adjacency is not motivated."),
    },
    "targets": {
        "K": mp.nstr(K, 60),
        "C_EBR_frozen": mp.nstr(C_EBR, 60),
        "reduction_factor": "(4/3)*sqrt(pi)/Gamma(7/3)",
    },
    "positive_controls": {},
    "tier_polylog_weight_graded": {},
    "tier_mixed_gamma_polylog": {},
    "verdict": None,
}

fired = []

# ---- POSITIVE CONTROLS (must all detect) ------------------------------------
# (a) polylog: 12*Li2(1/2) - pi^2 + 6*log^2(2) = 0    (Li2(1/2)=pi^2/12-log^2 2/2)
rel_a, res_a = relation([Li2_half, PI2, L2 ** 2], maxcoeff=10 ** 4)
# (b) algebraic: sqrt(2) -> x^2-2=0
s2 = mp.sqrt(2)
rel_b, res_b = relation([mp.mpf(1), s2, s2 ** 2], maxcoeff=10 ** 4)
# (c) zeta(2) = pi^2/6 -> 6*zeta2 - pi^2 = 0
rel_c, res_c = relation([Z2, PI2], maxcoeff=10 ** 4)
results["positive_controls"] = {
    "polylog_Li2_half": {"relation": rel_a, "residual": res_a,
        "expected": "[12,-1,6] (12 Li2(1/2) - pi^2 + 6 log^2 2 = 0)",
        "detected": rel_a is not None},
    "algebraic_sqrt2": {"relation": rel_b, "residual": res_b,
        "expected": "[-2,0,1]", "detected": rel_b is not None},
    "zeta2_pi2": {"relation": rel_c, "residual": res_c,
        "expected": "[6,-1]", "detected": rel_c is not None},
}
controls_ok = all(r is not None for r in (rel_a, rel_b, rel_c))
results["positive_controls"]["ALL_DETECTED"] = controls_ok

# ---- TIER 1: polylog/MZV weight-graded linear (value space) -- NEW ----------
PL_LABELS = ["1", "log2", "log3", "pi^2", "zeta3", "log^2 3", "log^3 3",
             "pi^2*log3", "Li2(1/3)", "Li3(1/3)", "Catalan"]
PL_BASIS = [mp.mpf(1), L2, L3, PI2, Z3, L3 ** 2, L3 ** 3,
            PI2 * L3, Li2_13, Li3_13, CAT]
for mc in (10 ** 9, 10 ** 12):
    vec = [K] + PL_BASIS
    rel, res = relation(vec, maxcoeff=mc)
    entry = {
        "basis": ["K"] + PL_LABELS,
        "weight_grading": "<= 3 (log/polylog), cubic args 1/3, quartic Catalan",
        "height_maxcoeff": mc,
        "dps": mp.mp.dps,
        "relation": rel,
        "residual": res,
    }
    if rel is None:
        entry["verdict"] = "NULL (no relation at this height/dps)"
    elif int(rel[0]) != 0:
        entry["verdict"] = "FIRE: nonzero coeff on K"
        fired.append(("K", "tier_polylog", mc, rel))
    else:
        entry["verdict"] = "relation among polylog constants only (coeff 0 on K)"
    results["tier_polylog_weight_graded"]["maxcoeff_%d" % mc] = entry

# ---- TIER 2: MIXED Gamma(k/3) x polylog (value space) -- NEW ----------------
# adds Gamma VALUES to the polylog basis; a genuine MIXED fire has nonzero
# coeff on BOTH a Gamma value and a polylog value.
MIX_LABELS = PL_LABELS + ["Gamma(1/3)", "Gamma(2/3)", "Gamma(1/6)"]
MIX_BASIS = PL_BASIS + [G13, G23, G16]
gamma_idx = set(range(1 + len(PL_BASIS), 1 + len(MIX_BASIS)))      # +1 for K slot
polylog_idx = set(range(4, 1 + len(PL_BASIS)))   # pi^2..Catalan (genuine PL part)
for mc in (10 ** 9,):
    vec = [K] + MIX_BASIS
    rel, res = relation(vec, maxcoeff=mc)
    entry = {
        "basis": ["K"] + MIX_LABELS,
        "height_maxcoeff": mc,
        "dps": mp.mp.dps,
        "relation": rel,
        "residual": res,
    }
    if rel is None:
        entry["verdict"] = "NULL (no relation at this height/dps)"
    elif int(rel[0]) != 0:
        entry["verdict"] = "FIRE: nonzero coeff on K"
        fired.append(("K", "tier_mixed", mc, rel))
    else:
        has_gamma = any(int(rel[i]) != 0 for i in gamma_idx)
        has_pl = any(int(rel[i]) != 0 for i in polylog_idx)
        if has_gamma and has_pl:
            entry["verdict"] = ("MIXED relation among Gamma and polylog constants "
                                "(coeff 0 on K) -- inter-constant identity, not K")
        elif has_gamma and not has_pl:
            entry["verdict"] = ("pure-Gamma relation (coeff 0 on K) -- equivalent "
                                "to an already-nulled C identity")
        else:
            entry["verdict"] = "polylog-only relation (coeff 0 on K)"
    results["tier_mixed_gamma_polylog"]["maxcoeff_%d" % mc] = entry

# ---- verdict ----------------------------------------------------------------
if not controls_ok:
    results["verdict"] = "INVALID: positive controls did not all fire"
elif fired:
    results["verdict"] = {"status": "FIRE", "fired": fired,
                          "action": "HALT -- K is elementary; reorders the program"}
else:
    results["verdict"] = {
        "status": "ALL-NULL",
        "summary": ("No integer relation involving K was found in the polylog/MZV "
                    "weight-graded tier or the mixed Gamma x polylog tier at the "
                    "declared heights and dps=169; positive controls all fired. "
                    "To 169 digits K is not polylog-elementary (weight<=3, height "
                    "<=1e12) and not a low-height mixed Gamma x polylog "
                    "combination (height<=1e9). Pure-Gamma tiers were skipped by "
                    "argument (equivalent to already-nulled C tiers)."),
        "grade": "VERIFIED (high-precision null, positive-control-validated)",
    }

canon = json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
results["canonical_sha256_of_hashfree_object"] = hashlib.sha256(canon).hexdigest()
with open("cc3_4a_kpslq_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# ---- console summary --------------------------------------------------------
print("=" * 72)
print("op:cc3-4a  K-targeted PSLQ null battery  (dps=169, tol=1e-150)")
print("=" * 72)
print("K (extended from frozen C) =", mp.nstr(K, 50))
print("K-extension vs frozen direct K_130 residual:", mp.nstr(K_agreement, 4))
print()
print("POSITIVE CONTROLS (must all detect):")
print("  polylog Li2(1/2) :", rel_a, " resid", res_a)
print("  algebraic sqrt2  :", rel_b, " resid", res_b)
print("  zeta2 = pi^2/6   :", rel_c, " resid", res_c)
print("  ALL_DETECTED =", controls_ok)
print()
print("--- tier_polylog_weight_graded ---")
for k, e in results["tier_polylog_weight_graded"].items():
    print("  %-16s %s" % (k, e["verdict"]))
print("--- tier_mixed_gamma_polylog ---")
for k, e in results["tier_mixed_gamma_polylog"].items():
    print("  %-16s %s" % (k, e["verdict"]))
print()
print("VERDICT:", json.dumps(results["verdict"])
      if isinstance(results["verdict"], dict) else results["verdict"])
print("canonical_sha256:", results["canonical_sha256_of_hashfree_object"])
