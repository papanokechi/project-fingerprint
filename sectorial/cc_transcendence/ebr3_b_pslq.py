#!/usr/bin/env python3
# op:ebr3-b -- the 169-digit integer-relation NULL battery on the EBR d=2
# connection data C_EBR and amplitude A.  Falsification target:
# "C is an elementary Gamma-quotient / a low-height constant / algebraic."
# A documented NULL (with positive controls + declared height/dps/hash) is the
# deliverable.  If any tier FIRES with a nonzero coefficient on the target,
# HALT: the relation reorders the program.
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import mpmath as mp

# ---- precision policy --------------------------------------------------------
# The connection corpus (CC4-1-C-120D) is self-validated to 169 stable digits.
# We work at dps = 169 and accept an integer relation only if its residual is
# below TOL = 1e-150, leaving ~19 guard digits below the data floor.
RELIABLE_DIGITS = 169
mp.mp.dps = RELIABLE_DIGITS
TOL = mp.mpf(10) ** (-150)

# ---- load targets programmatically from the cc4-1 artifact (no transcription)
with open("cc4_1_connection_results.json", encoding="utf-8") as f:
    conn = json.load(f)
A      = mp.mpf(conn["amplitude_A"])
C_EBR  = mp.mpf(conn["prefactor_C_EBR"])
# sanity: C_EBR = A / Gamma(11/6) to the data floor
gam_11_6 = mp.gamma(mp.mpf(11) / 6)
recon_resid = abs(C_EBR - A / gam_11_6)
assert recon_resid < TOL, f"C_EBR != A/Gamma(11/6): {recon_resid}"

# ---- basis constants ---------------------------------------------------------
PI   = mp.pi
L2   = mp.log(2)
L3   = mp.log(3)
L5   = mp.log(5)
EUL  = mp.euler
CATALAN = mp.catalan
Z3   = mp.zeta(3)
Z5   = mp.zeta(5)

def gamma_at(p, q):
    return mp.gamma(mp.mpf(p) / q)

# reflection-normalized primitive 24th arguments (one rep per reflection pair):
INDEP4 = [(1, 24), (5, 24), (7, 24), (11, 24)]
# multiplication extension: reducible-denominator reps in the (1/24)Z grid,
# a < 1/2 (Gamma(1/2)=sqrt(pi) is folded into pi):
FULL11 = INDEP4 + [(1, 12), (5, 12), (1, 8), (3, 8), (1, 6), (1, 4), (1, 3)]

def relation(vec, maxcoeff, maxsteps=100000):
    """Return (rel|None, residual_str). rel is the integer null vector."""
    rel = mp.pslq(vec, tol=TOL, maxcoeff=maxcoeff, maxsteps=maxsteps)
    if rel is None:
        return None, None
    resid = abs(sum(mp.mpf(int(c)) * v for c, v in zip(rel, vec)))
    return rel, mp.nstr(resid, 8)

results = {
    "op": "ebr3-b",
    "task_id": "op:ebr3-assemble/ebr3-b",
    "objective": ("169-digit integer-relation NULL battery on the EBR d=2 "
                  "connection data; falsify 'C is an elementary "
                  "Gamma-quotient / low-height constant / algebraic'."),
    "precision_policy": {
        "reliable_digits": RELIABLE_DIGITS,
        "mp_dps": mp.mp.dps,
        "tol": "1e-150",
        "guard_digits": RELIABLE_DIGITS - 150,
        "note": ("targets known to 169 digits (CC4-1-C-120D, self-validated); "
                 "a TRUE relation has residual ~1e-168, a height-H spurious "
                 "relation among k terms has residual ~H^-k; for every tier "
                 "k*log10(maxcoeff) << 169 so no false positive is detectable."),
    },
    "targets": {
        "C_EBR": mp.nstr(C_EBR, 60),
        "A": mp.nstr(A, 60),
        "C_EBR_eq_A_over_Gamma_11_6_residual": mp.nstr(recon_resid, 6),
    },
    "positive_controls": {},
    "tier_i_gamma_monomial": {},
    "tier_ii_constants": {},
    "tier_iii_algebraicity": {},
    "verdict": None,
}

fired = []  # any FIRE (nonzero coeff on a genuine target) -> HALT

# ---- POSITIVE CONTROLS (prove the battery detects real relations) ------------
# (a) Gamma reflection/multiplication: Gamma(1/3)Gamma(2/3) = 2pi/sqrt(3)
ctrl_a_vec = [mp.log(gamma_at(1, 3)), mp.log(gamma_at(2, 3)), mp.log(PI), L2, L3]
rel_a, res_a = relation(ctrl_a_vec, maxcoeff=10**6)
# (b) algebraic: sqrt(2) satisfies x^2-2=0
s2 = mp.sqrt(2)
rel_b, res_b = relation([mp.mpf(1), s2, s2**2], maxcoeff=10**4)
# (c) linear const: kappa = 2*pi + 3*log2
kc = 2 * PI + 3 * L2
rel_c, res_c = relation([kc, mp.mpf(1), PI, L2, L3, EUL], maxcoeff=10**4)
results["positive_controls"] = {
    "gamma_reflection_1_3": {"relation": rel_a, "residual": res_a,
        "expected": "[2,2,-2,-2,1] (2logG(1/3)+2logG(2/3)-2logpi-2log2+log3=0)",
        "detected": rel_a is not None},
    "algebraic_sqrt2": {"relation": rel_b, "residual": res_b,
        "expected": "[-2,0,1] (x^2-2=0)", "detected": rel_b is not None},
    "linear_2pi_plus_3log2": {"relation": rel_c, "residual": res_c,
        "expected": "[-1,0,2,3,0,0]", "detected": rel_c is not None},
}
controls_ok = (rel_a is not None and rel_b is not None and rel_c is not None)
results["positive_controls"]["ALL_DETECTED"] = controls_ok

# ---- the battery, run for both targets --------------------------------------
TARGETS = [("C_EBR", C_EBR), ("A", A)]

# Tier i: Gamma-monomial / quotient test in log space
MAXCOEFF_I = 10**9
for name, kappa in TARGETS:
    for bname, args in [("indep4", INDEP4), ("full11", FULL11)]:
        logG = [mp.log(gamma_at(p, q)) for (p, q) in args]
        vec = [mp.log(kappa)] + logG + [mp.log(PI), L2, L3]
        rel, res = relation(vec, maxcoeff=MAXCOEFF_I)
        labels = (["log(%s)" % name]
                  + ["logG(%d/%d)" % (p, q) for (p, q) in args]
                  + ["log(pi)", "log2", "log3"])
        entry = {
            "basis": labels,
            "args_grid": "(1/24)Z, reflection-normalized" if bname == "indep4"
                         else "(1/24)Z + multiplication extension",
            "height_maxcoeff": MAXCOEFF_I,
            "dps": mp.mp.dps,
            "relation": rel,
            "residual": res,
        }
        if rel is None:
            entry["verdict"] = "NULL (no relation at this height/dps)"
        else:
            kc0 = int(rel[0])
            if kc0 != 0:
                entry["verdict"] = "FIRE: nonzero coeff on target"
                fired.append((name, "tier_i", bname, rel))
            else:
                entry["verdict"] = ("inter-Gamma identity (coeff 0 on target) "
                                    "-- does NOT involve the target")
        results["tier_i_gamma_monomial"]["%s_%s" % (name, bname)] = entry

# Tier ii: linear relation among standard constants
MAXCOEFF_II = 10**12
const_basis = [("1", mp.mpf(1)), ("pi", PI), ("log2", L2), ("log3", L3),
               ("gamma_E", EUL), ("Catalan", CATALAN), ("zeta3", Z3),
               ("zeta5", Z5)]
for name, kappa in TARGETS:
    vec = [kappa] + [v for _, v in const_basis]
    rel, res = relation(vec, maxcoeff=MAXCOEFF_II)
    entry = {
        "basis": [name] + [n for n, _ in const_basis],
        "degree": 1,
        "height_maxcoeff": MAXCOEFF_II,
        "dps": mp.mp.dps,
        "relation": rel,
        "residual": res,
    }
    if rel is None:
        entry["verdict"] = "NULL"
    elif int(rel[0]) != 0:
        entry["verdict"] = "FIRE: nonzero coeff on target"
        fired.append((name, "tier_ii", "linear", rel))
    else:
        entry["verdict"] = "relation among constants only (coeff 0 on target)"
    results["tier_ii_constants"][name] = entry

# Tier iii: algebraicity (integer min-poly search)
MAXCOEFF_III = 10**6
MAXDEG = 8
for name, kappa in TARGETS:
    hit = None
    for d in range(1, MAXDEG + 1):
        powers = [kappa**k for k in range(d + 1)]
        rel, res = relation(powers, maxcoeff=MAXCOEFF_III)
        if rel is not None:
            hit = {"degree": d, "relation": rel, "residual": res}
            break
    entry = {
        "search": "min-poly sum_k c_k kappa^k = 0",
        "max_degree": MAXDEG,
        "height_maxcoeff": MAXCOEFF_III,
        "dps": mp.mp.dps,
    }
    if hit is None:
        entry["verdict"] = ("NULL: not algebraic of degree <= %d, height <= %d"
                            % (MAXDEG, MAXCOEFF_III))
        entry["relation"] = None
    else:
        entry["verdict"] = "FIRE: algebraic"
        entry.update(hit)
        fired.append((name, "tier_iii", "algebraic", hit["relation"]))
    results["tier_iii_algebraicity"][name] = entry

# ---- verdict -----------------------------------------------------------------
if not controls_ok:
    results["verdict"] = ("INVALID: positive controls did not all fire; "
                          "battery not trustworthy")
elif fired:
    results["verdict"] = {"status": "FIRE", "fired": fired,
                          "action": "HALT -- relation reorders the program"}
else:
    results["verdict"] = {
        "status": "ALL-NULL",
        "summary": ("No integer relation involving C_EBR or A was found in any "
                    "tier at the declared heights and dps=169; positive "
                    "controls all fired. C_EBR and A are, to 169 digits, not "
                    "elementary Gamma-quotients, not low-height combinations of "
                    "{1,pi,log2,log3,gamma_E,Catalan,zeta3,zeta5}, and not "
                    "algebraic of degree<=8/height<=1e6."),
        "grade": "VERIFIED (high-precision null, positive-control-validated)",
    }

# (no timestamp in the hashed object: the canonical hash must be reproducible)

# ---- canonical hash of the hash-free object ----------------------------------
canon = json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
results["canonical_sha256_of_hashfree_object"] = hashlib.sha256(canon).hexdigest()

with open("ebr3_b_pslq_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# ---- console summary ---------------------------------------------------------
print("=" * 72)
print("op:ebr3-b  169-digit integer-relation NULL battery")
print("=" * 72)
print("dps = %d, tol = 1e-150, guard ~ %d digits"
      % (mp.mp.dps, RELIABLE_DIGITS - 150))
print("C_EBR = A/Gamma(11/6) check residual:", mp.nstr(recon_resid, 4))
print()
print("POSITIVE CONTROLS (must all detect):")
print("  gamma reflection 1/3 :", rel_a, "  resid", res_a)
print("  algebraic sqrt2      :", rel_b, "  resid", res_b)
print("  linear 2pi+3log2     :", rel_c, "  resid", res_c)
print("  ALL_DETECTED =", controls_ok)
print()
for tier in ("tier_i_gamma_monomial", "tier_ii_constants",
             "tier_iii_algebraicity"):
    print("---", tier, "---")
    for k, e in results[tier].items():
        print("  %-16s %s" % (k, e["verdict"]))
print()
print("VERDICT:", json.dumps(results["verdict"])
      if isinstance(results["verdict"], dict) else results["verdict"])
print("canonical_sha256:", results["canonical_sha256_of_hashfree_object"])
