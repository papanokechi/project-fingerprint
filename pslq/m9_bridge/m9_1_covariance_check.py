"""
M9.1 covariance check  --  numerical corroboration of Proposition M9.1:
    for deg b = d, phi(n) = alpha*n + gamma (alpha in Z>0, gamma in Z),
        xi0(b . phi) = alpha^-1 * xi0(b)           (dilation-covariant)
    and gamma has NO effect                        (shift-invariant).

METHOD PROVENANCE (faithful REUSE of the in-repo xi0 pipeline, NOT a rival
re-implementation):
This script reuses pslq/xi0_d3/xi0_d3_scale_test.py:
    * neville_zero  : IMPORTED directly from that module (the degree-agnostic
                      O(1/n)-tail extrapolator -- the load-bearing accelerator).
                      No copy is kept here.
    * compute_Q     : the SAME PCF-denominator recurrence
                      Q_0=1, Q_1=b(1), Q_n = b(n) Q_{n-1} + Q_{n-2}.
    * beta_d est.   : the SAME estimator beta_d_est(n) = Q_n / (Q_{n-1} * n^d),
                      Neville-accelerated in h=1/n.
    * xi0 = d / beta_d^(1/d)                        (the in-repo Borel-radius map)
    * node set 60..300 step 12, DPS_NUM=160, DPS_ALG=80  (in-repo constants)
The recurrence/estimator are kept LOCAL because the in-repo copies are hardcoded
to d=3 (4-tuple coeffs, n**3); here they are generalized to arbitrary degree d
via a high-to-low coeff list. This is the ONLY generalization vs the d=3 code;
the extrapolation primitive is the original in-repo function, imported.
The reindexed family b.phi is obtained by evaluating the SAME b at alpha*n+gamma
(an affine reindex preserves degree d), which is exactly the object M9.1 concerns.

No git side effects. Writes results JSON next to this file.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "m9_1_covariance_results.json"

# Reuse the in-repo extrapolator without duplicating it: load the sibling
# pipeline module by path and import its neville_zero verbatim.
_XI0_D3 = HERE.parent / "xi0_d3" / "xi0_d3_scale_test.py"
_spec = importlib.util.spec_from_file_location("xi0_d3_scale_test", _XI0_D3)
_xi0_d3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_xi0_d3)
neville_zero = _xi0_d3.neville_zero   # the in-repo function, reused

DPS_ALG = 80       # in-repo parity
DPS_NUM = 160      # in-repo parity
NODES = list(range(60, 301, 12))   # in-repo node set: 60,72,...,300 (21 nodes)

# Pass criteria (stated up front):
#   NUMERIC leg : |xi0(b.phi)/xi0(b) - 1/alpha| < 10^-NUM_PASS_DIG (Neville, measured from Q_n)
#   ALGEBRAIC leg: same ratio from known leading coeffs, agree to >= ALG_PASS_DIG digits
#   SHIFT       : |xi0(b.phi_{a,0}) - xi0(b.phi_{a,1})|/xi0 < 10^-NUM_PASS_DIG
NUM_PASS_DIG = 8
ALG_PASS_DIG = 70


# --------------------------------------------------------------------------- #
# pipeline (SAME recurrence/estimator as pslq/xi0_d3, generalized to degree d) #
# --------------------------------------------------------------------------- #
def b_eval(coeffs, n):
    """Evaluate b(n) for high-to-low coeffs [a_d,...,a_0] (Horner)."""
    nn = mp.mpf(n)
    acc = mp.mpf(0)
    for a in coeffs:
        acc = acc * nn + mp.mpf(a)
    return acc


def b_eval_phi(coeffs, n, alpha, gamma):
    """Evaluate (b . phi)(n) = b(alpha*n + gamma) -- the reindexed family."""
    return b_eval(coeffs, alpha * n + gamma)


def compute_Q(coeffs, N, alpha=1, gamma=0, dps=DPS_NUM):
    """Q_0=1, Q_1=b(phi(1)), Q_n = b(phi(n)) Q_{n-1} + Q_{n-2}.  [in-repo recurrence]"""
    with mp.workdps(dps):
        Q = [mp.mpf(1), b_eval_phi(coeffs, 1, alpha, gamma)]
        for n in range(2, N + 1):
            Q.append(b_eval_phi(coeffs, n, alpha, gamma) * Q[-1] + Q[-2])
        return Q


def measure_betad(coeffs, d, alpha=1, gamma=0, dps=DPS_NUM):
    """beta_d_est(n) = Q_n / (Q_{n-1} * n^d) -> beta_d, Neville-accelerated in h=1/n.
    Generalizes the in-repo n^3 estimator to n^d. Returns (raw_at_Nmax, neville)."""
    Nmax = NODES[-1]
    Q = compute_Q(coeffs, Nmax, alpha=alpha, gamma=gamma, dps=dps)
    with mp.workdps(dps):
        hs, est = [], []
        for n in NODES:
            e = Q[n] / (Q[n - 1] * mp.mpf(n) ** d)
            hs.append(mp.mpf(1) / n)
            est.append(e)
        return +est[-1], +neville_zero(hs, est)


def xi0_numeric(coeffs, d, alpha=1, gamma=0, dps=DPS_NUM):
    """In-repo map: xi0 = d / beta_d^(1/d), beta_d measured from Q_n (Neville leg)."""
    _, nev = measure_betad(coeffs, d, alpha=alpha, gamma=gamma, dps=dps)
    with mp.workdps(dps):
        return mp.mpf(d) / mp.power(nev, mp.mpf(1) / d), +nev


def xi0_algebraic(beta_d, d, dps=DPS_ALG):
    """xi0 = d / beta_d^(1/d) from the KNOWN leading coeff (formula leg, exact)."""
    with mp.workdps(dps + 20):
        return mp.mpf(d) / mp.power(mp.mpf(beta_d), mp.mpf(1) / d)


def agree_digits(measured, exact, dps):
    with mp.workdps(dps):
        if exact == 0:
            return 0.0
        rel = abs(measured - exact) / abs(exact)
        return float(dps) if rel == 0 else float(-mp.log10(rel))


# --------------------------------------------------------------------------- #
# families (one d=2, two d=3, two d=4) and the phi-set                         #
# --------------------------------------------------------------------------- #
# coeffs high-to-low [a_d,...,a_0]; beta_d = a_d.
FAMILIES = [
    # d=2: the in-repo V_quad denominator b(n)=3n^2+n+1 (basis_canonical V_quad).
    ("vquad_d2",      2, [3, 1, 1],        "in-repo V_quad PCF denominator b=3n^2+n+1, beta_2=3"),
    # d=3: in-repo catalogue + synthetic scale objects (xi0_d3_scale_test TEST_OBJECTS).
    ("fam19_d3",      3, [1, -3, 0, 1],    "in-repo catalogue family 19 b=n^3-3n^2+1, beta_3=1"),
    ("synth_b3_2_d3", 3, [2, 1, -1, 1],    "in-repo synth b=2n^3+n^2-n+1, beta_3=2"),
    # d=4: constructed scale probes (clearly NOT catalogue; parity w/ d=4 alpha_4=7 note).
    ("synth_b4_1_d4", 4, [1, 0, 0, 0, 1],  "constructed quartic b=n^4+1, beta_4=1"),
    ("synth_b4_7_d4", 4, [7, 0, 0, 1, 0],  "constructed quartic b=7n^4+n, beta_4=7"),
]
PHIS = [(2, 0), (2, 1), (3, 0), (3, 1)]   # alpha in {2,3}, gamma in {0,1}


def main():
    out = {
        "proposition": "M9.1: xi0(b.phi)=alpha^-1 xi0(b); phi(n)=alpha n+gamma",
        "method_provenance": "reuses pslq/xi0_d3/xi0_d3_scale_test.py "
                             "(neville_zero IMPORTED; same compute_Q recurrence + "
                             "Q_n/(Q_{n-1} n^d) estimator), generalized from hardcoded "
                             "d=3 to degree d",
        "dps_numeric": DPS_NUM, "dps_algebraic": DPS_ALG,
        "nodes": [NODES[0], NODES[-1], len(NODES)],
        "pass_criteria": {"numeric_ratio_digits_min": NUM_PASS_DIG,
                          "algebraic_ratio_digits_min": ALG_PASS_DIG,
                          "shift_invariance_digits_min": NUM_PASS_DIG},
        "families": [],
    }

    all_pass = True
    for label, d, coeffs, desc in FAMILIES:
        beta_d = coeffs[0]
        xi0_b_num, nev_b = xi0_numeric(coeffs, d)               # baseline (phi=id)
        xi0_b_alg = xi0_algebraic(beta_d, d)
        fam = {"label": label, "d": d, "beta_d": beta_d, "description": desc,
               "xi0_b_numeric": mp.nstr(xi0_b_num, 45),
               "xi0_b_algebraic": mp.nstr(xi0_b_alg, 45),
               "phis": []}
        print(f"\n=== {label} (d={d}, beta_d={beta_d}) {desc}")
        print(f"  xi0(b) numeric  = {mp.nstr(xi0_b_num, 36)}")
        print(f"  xi0(b) algebraic= {mp.nstr(xi0_b_alg, 36)}")

        shift_pairs = {}   # alpha -> {gamma: xi0}
        for (alpha, gamma) in PHIS:
            xi0_phi_num, nev_phi = xi0_numeric(coeffs, d, alpha=alpha, gamma=gamma)
            beta_phi = beta_d * alpha ** d                       # known leading coeff of b.phi
            xi0_phi_alg = xi0_algebraic(beta_phi, d)
            with mp.workdps(DPS_NUM):
                inv_alpha = mp.mpf(1) / alpha
                ratio_num = xi0_phi_num / xi0_b_num
                ratio_alg = xi0_phi_alg / xi0_b_alg
            num_dig = agree_digits(ratio_num, inv_alpha, DPS_NUM)
            alg_dig = agree_digits(ratio_alg, inv_alpha, DPS_ALG)
            num_ok = num_dig >= NUM_PASS_DIG
            alg_ok = alg_dig >= ALG_PASS_DIG
            shift_pairs.setdefault(alpha, {})[gamma] = xi0_phi_num
            rec = {"phi_alpha": alpha, "phi_gamma": gamma,
                   "beta_d_of_b_phi": beta_phi,
                   "xi0_b_phi_numeric": mp.nstr(xi0_phi_num, 45),
                   "xi0_b_phi_algebraic": mp.nstr(xi0_phi_alg, 45),
                   "ratio_numeric": mp.nstr(ratio_num, 45),
                   "ratio_target_1_over_alpha": mp.nstr(inv_alpha, 20),
                   "ratio_numeric_agreement_digits": round(num_dig, 1),
                   "ratio_algebraic_agreement_digits": round(alg_dig, 1),
                   "numeric_pass": bool(num_ok), "algebraic_pass": bool(alg_ok)}
            fam["phis"].append(rec)
            all_pass = all_pass and num_ok and alg_ok
            print(f"  phi=({alpha},{gamma}): ratio={mp.nstr(ratio_num,18)} "
                  f"target=1/{alpha}  num={num_dig:.1f}dig {'OK' if num_ok else 'FAIL'} "
                  f"| alg={alg_dig:.0f}dig {'OK' if alg_ok else 'FAIL'}")

        # shift invariance: gamma=0 vs gamma=1 at fixed alpha
        shift_checks = []
        for alpha, gm in shift_pairs.items():
            if 0 in gm and 1 in gm:
                sdig = agree_digits(gm[1], gm[0], DPS_NUM)
                ok = sdig >= NUM_PASS_DIG
                shift_checks.append({"alpha": alpha, "agreement_digits": round(sdig, 1),
                                     "pass": bool(ok)})
                all_pass = all_pass and ok
                print(f"  shift-inv alpha={alpha}: xi0(gamma=0) vs xi0(gamma=1) "
                      f"agree {sdig:.1f} dig {'OK' if ok else 'FAIL'}")
        fam["shift_invariance"] = shift_checks
        out["families"].append(fam)

    out["all_pass"] = bool(all_pass)
    RESULTS.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    sha = hashlib.sha256(RESULTS.read_bytes()).hexdigest()
    print(f"\nALL_PASS = {all_pass}")
    print(f"Wrote {RESULTS.name}  sha256={sha}")
    return sha


if __name__ == "__main__":
    main()
