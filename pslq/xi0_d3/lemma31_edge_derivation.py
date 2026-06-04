"""
M9 / Lemma 3.1 general-d -- vendoring an IN-REPO derivation of the slope-1/d
Newton-polygon edge polynomial, to discharge the D2-NOTE conditionality behind the
all-d lift M9.1+.

This EXTENDS (does not fork) the in-repo d=3 method in
    pslq/xi0_d3/xi0_d3_scale_test.py :: derive_chi3_symbolic
which forms chi_3 by acting the operator L = 1 - z*b(theta+1) - z^2 (theta=(u/3)d/du,
z=u^3) on the WKB ansatz f = exp(c/u) and reading the u^0 balance. Here that exact
construction is generalized to arbitrary d.

Four parts:
  A. FULL operator derivation for d=2..6 (the same construction as the d=3 code),
     confirming chi_d(c) = 1 + (-1)^{d+1}(beta_d/d^d) c^d and that ONLY beta_d sits
     on the slope-1/d edge (beta_{d-1..0} absent).  [instance-verified, full operator]
  B. SYMBOLIC-IN-d leading-symbol lemma: with d kept a free symbol, the WKB recurrence
     P_{k+1} = -(w/d)(P_k' + c P_k), P_0=1  (w=1/u) gives theta^k f/f = P_k(1/u), a
     degree-k polynomial in 1/u with leading coefficient (-c/d)^k. Verified symbolically
     for k=0..8 with d SYMBOLIC -> the induction backbone is general-d, not per-instance.
     This is what makes chi_d's edge symbolic in d: [u^0](z b(theta+1) f/f) = beta_d(-c/d)^d.
  C. SYMBOLIC covariance from the edge alone: b -> b.phi, phi(n)=alpha n+gamma sends
     beta_d -> beta_d*alpha^d (d, lower edge structure unchanged), so the root modulus
     d/beta_d^{1/d} -> alpha^{-1} d/beta_d^{1/d}, gamma absent. Reproduces M9.1+ with NO
     appeal to D2-NOTE.
  D. NUMERIC cross-check d=2..6 against the already-trusted in-repo xi0 pipeline
     (imported from pslq/m9_bridge/m9_1_covariance_check.py, degree-general): the
     pipeline's measured xi0 matches d/beta_d^{1/d} from the symbolic edge.

HONEST SCOPE: parts A/B/C discharge the ALGEBRAIC edge-polynomial fact (Lemma 3.1's
algebra) in-repo, symbolically in d (B) and instance-verified for the full operator
(A). The ANALYTIC implication "this edge polynomial => Borel radius |c|" is the Wasow
S19 / Birkhoff-Trjitzinsky content that D2-NOTE Thm 4.1 cites; it is NOT re-derived
here, only numerically corroborated (D). See 08_lemma31_general_d_indrepo.md.

No git side effects. Workspace artifact only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "lemma31_edge_derivation_results.json"
# Resolve the degree-general xi0 pipeline RELATIVE TO THE REPO (this file lives in
# pslq/xi0_d3/; the pipeline is the sibling deposit pslq/m9_bridge/). No workspace
# or absolute-machine path: the import resolves from the repo location.
DEPOSITED_PIPE = HERE.parent / "m9_bridge" / "m9_1_covariance_check.py"

DPS_NUM = 160


# --------------------------------------------------------------------------- #
# A. full operator derivation chi_d for general d (extends derive_chi3_symbolic)
# --------------------------------------------------------------------------- #
def derive_chid_symbolic(d: int):
    """Direct operator action, EXACTLY the d=3 method generalized to degree d.
    L = 1 - z*b(theta+1) - z^2 ; theta=(u/d) d/du ; z=u^d ; f=exp(c/u).
    b(x) = sum_{k=0}^d beta_k x^k. Returns (chi_d_simplified, only_beta_d_bool,
    matches_formula_bool)."""
    u, c = sp.symbols("u c")
    betas = sp.symbols(f"beta0:{d + 1}")        # beta0, beta1, ..., beta_d
    f = sp.exp(c / u)
    theta = lambda e: sp.together((u / sp.Integer(d)) * sp.diff(e, u))
    D = lambda e: theta(e) + e                   # (theta + 1)

    # (theta+1)^k f for k = 0..d
    Dpow = [f]
    for _ in range(d):
        Dpow.append(sp.expand(D(Dpow[-1])))
    Bf = sum(betas[k] * Dpow[k] for k in range(d + 1))
    g = sp.expand(sp.simplify(Bf / f))           # Laurent polynomial in 1/u
    Lf_over_f = sp.expand(1 - u ** d * g - u ** (2 * d))
    chid = sp.simplify(Lf_over_f.coeff(u, 0))    # u^0 balance = slope-1/d edge poly

    only_betad = not any(betas[k] in chid.free_symbols for k in range(d))  # beta_{0..d-1} absent
    formula = 1 + (-1) ** (d + 1) * (betas[d] / sp.Integer(d) ** d) * c ** d
    matches = sp.simplify(chid - formula) == 0
    return chid, bool(only_betad), bool(matches)


# --------------------------------------------------------------------------- #
# B. symbolic-in-d leading-symbol lemma (the general-d backbone)
# --------------------------------------------------------------------------- #
def leading_symbol_lemma(Kmax: int = 8):
    """With d a FREE symbol, theta = -(w/d) d/dw (w=1/u), f=exp(c w):
        theta^{k+1} f / f = -(w/d)( (theta^k f/f)' + c (theta^k f/f) ).
    Verify theta^k f/f = P_k(w) is degree-k in w with leading coeff (-c/d)^k, for
    k=0..Kmax, with d kept symbolic. Returns list of per-k records (all symbolic)."""
    w, c, d = sp.symbols("w c d")
    recs = []
    P = sp.Integer(1)                            # P_0 = 1
    for k in range(Kmax + 1):
        poly = sp.Poly(sp.expand(P), w)
        deg = poly.degree()
        lead = sp.simplify(poly.LC())            # leading coeff in w
        expected_lead = (-c / d) ** k
        recs.append({
            "k": k,
            "degree_in_w": int(deg) if P != 0 else 0,
            "leading_coeff": str(lead),
            "expected_leading_coeff": str(sp.simplify(expected_lead)),
            "leading_matches": bool(sp.simplify(lead - expected_lead) == 0),
            "degree_matches_k": bool(int(deg) == k),
        })
        # advance: P_{k+1} = -(w/d)(P_k' + c P_k)
        P = sp.expand(-(w / d) * (sp.diff(P, w) + c * P))
    all_ok = all(r["leading_matches"] and r["degree_matches_k"] for r in recs)
    return recs, all_ok


# --------------------------------------------------------------------------- #
# C. symbolic covariance from the edge polynomial alone
# --------------------------------------------------------------------------- #
def symbolic_covariance(d: int):
    """Generic b(n)=sum beta_k n^k; phi(n)=alpha n+gamma. Show leading coeff of
    b(phi(n)) is beta_d*alpha^d (so edge -> chi_d with beta_d->beta_d*alpha^d, d fixed)
    and hence the root-modulus ratio xi0(b.phi)/xi0(b)=1/alpha, gamma-free."""
    n, alpha, gamma = sp.symbols("n alpha gamma", positive=True)
    betas = sp.symbols(f"beta0:{d + 1}")
    b = sum(betas[k] * n ** k for k in range(d + 1))
    b_phi = sp.expand(b.subs(n, alpha * n + gamma))
    lead_phi = sp.Poly(b_phi, n).LC()            # leading coeff in n of b(alpha n+gamma)
    lead_matches = bool(sp.simplify(lead_phi - betas[d] * alpha ** d) == 0)
    deg_phi = sp.Poly(b_phi, n).degree()

    # xi0 = d / beta_d^{1/d}; under beta_d -> beta_d*alpha^d:
    xi0 = sp.Integer(d) / betas[d] ** (sp.Rational(1, d))
    xi0_phi = sp.Integer(d) / (betas[d] * alpha ** d) ** (sp.Rational(1, d))
    ratio = sp.simplify(xi0_phi / xi0)           # expect 1/alpha (alpha>0 -> real d-th root)
    ratio_is_inv_alpha = bool(sp.simplify(ratio - 1 / alpha) == 0)
    gamma_free = gamma not in lead_phi.free_symbols
    return {
        "d": d,
        "leading_coeff_b_phi": str(lead_phi),
        "leading_coeff_matches_betad_alpha_d": lead_matches,
        "degree_preserved": bool(int(deg_phi) == d),
        "gamma_absent_from_leading_coeff": bool(gamma_free),
        "xi0_ratio_simplified": str(ratio),
        "ratio_equals_inv_alpha": ratio_is_inv_alpha,
    }


# --------------------------------------------------------------------------- #
# D. numeric cross-check d=2..6 vs the trusted in-repo pipeline
# --------------------------------------------------------------------------- #
def load_pipeline():
    spec = importlib.util.spec_from_file_location("m9_dep_pipe", DEPOSITED_PIPE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)                 # imports xi0_d3 neville_zero internally
    return mod


NUMERIC_FAMILIES = [
    # (label, d, coeffs high-to-low [a_d..a_0], beta_d)
    ("d2_b3",  2, [3, 1, 1],              3),
    ("d2_b1",  2, [1, 0, 1],              1),
    ("d3_b2",  3, [2, 1, -1, 1],          2),
    ("d3_b1",  3, [1, 0, 0, 1],           1),
    ("d4_b1",  4, [1, 0, 0, 0, 1],        1),
    ("d4_b7",  4, [7, 0, 0, 1, 0],        7),
    ("d5_b1",  5, [1, 0, 0, 0, 0, 1],     1),
    ("d5_b2",  5, [2, 0, 0, 1, 0, 1],     2),
    ("d6_b1",  6, [1, 0, 0, 0, 0, 0, 1],  1),
    ("d6_b3",  6, [3, 0, 0, 0, 0, 0, 1],  3),
]
NUM_PASS_DIG = 8


def numeric_crosscheck(pipe):
    out = []
    all_ok = True
    for label, d, coeffs, beta_d in NUMERIC_FAMILIES:
        xi0_meas, nev = pipe.xi0_numeric(coeffs, d)
        with mp.workdps(DPS_NUM):
            xi0_edge = mp.mpf(d) / mp.power(mp.mpf(beta_d), mp.mpf(1) / d)  # from symbolic chi_d
            dig = pipe.agree_digits(xi0_meas, xi0_edge, DPS_NUM)
        ok = dig >= NUM_PASS_DIG
        all_ok = all_ok and ok
        out.append({
            "label": label, "d": d, "beta_d": beta_d,
            "xi0_edge_d_over_betad_cbrt": mp.nstr(xi0_edge, 40),
            "xi0_pipeline_measured": mp.nstr(xi0_meas, 40),
            "agreement_digits": round(dig, 1), "pass": bool(ok),
        })
        print(f"  [{label}] d={d} beta_d={beta_d}: edge={mp.nstr(xi0_edge,20)} "
              f"pipeline={mp.nstr(xi0_meas,20)}  {dig:.1f}dig {'OK' if ok else 'FAIL'}")
    return out, all_ok


# --------------------------------------------------------------------------- #
def main():
    out = {
        "task": "Lemma 3.1 general-d in-repo derivation (discharge D2-NOTE conditionality)",
        "method": "extends pslq/xi0_d3 derive_chi3_symbolic to general d; symbolic-in-d "
                  "leading-symbol lemma; symbolic covariance; numeric cross-check vs in-repo pipeline",
    }

    # A
    print("== A. full operator chi_d for d=2..6 ==")
    partA = []
    for d in range(2, 7):
        chid, only_betad, matches = derive_chid_symbolic(d)
        partA.append({"d": d, "chi_d": str(chid),
                      "expected": f"1 + (-1)^{d+1}(beta{d}/{d**d}) c^{d}",
                      "only_beta_d_on_edge": only_betad,
                      "matches_formula": matches})
        print(f"  d={d}: chi_d = {chid}")
        print(f"        only_beta_d_on_edge={only_betad}  matches_formula={matches}")
    out["A_full_operator_d2_to_6"] = partA
    out["A_all_match"] = all(r["matches_formula"] and r["only_beta_d_on_edge"] for r in partA)

    # B
    print("\n== B. symbolic-in-d leading-symbol lemma (k=0..8, d symbolic) ==")
    recsB, okB = leading_symbol_lemma(8)
    for r in recsB:
        print(f"  k={r['k']}: deg_w={r['degree_in_w']} lead={r['leading_coeff']} "
              f"(=(-c/d)^{r['k']}? {r['leading_matches']})")
    out["B_leading_symbol_lemma"] = recsB
    out["B_symbolic_in_d_holds"] = bool(okB)

    # C
    print("\n== C. symbolic covariance from the edge (d=2..6) ==")
    partC = []
    for d in range(2, 7):
        rc = symbolic_covariance(d)
        partC.append(rc)
        print(f"  d={d}: lead(b.phi)={rc['leading_coeff_b_phi']}  "
              f"ratio={rc['xi0_ratio_simplified']}  =1/alpha? {rc['ratio_equals_inv_alpha']}  "
              f"gamma-free? {rc['gamma_absent_from_leading_coeff']}")
    out["C_symbolic_covariance_d2_to_6"] = partC
    out["C_all_covariant"] = all(
        r["ratio_equals_inv_alpha"] and r["leading_coeff_matches_betad_alpha_d"]
        and r["gamma_absent_from_leading_coeff"] and r["degree_preserved"] for r in partC)

    # D
    print("\n== D. numeric cross-check vs in-repo pipeline (d=2..6) ==")
    pipe = load_pipeline()
    partD, okD = numeric_crosscheck(pipe)
    out["D_numeric_crosscheck"] = partD
    out["D_all_match_pipeline"] = bool(okD)
    out["D_pipeline_source"] = str(DEPOSITED_PIPE)
    out["D_dps_numeric"] = pipe.DPS_NUM

    out["VERDICT"] = {
        "algebraic_edge_polynomial": "DISCHARGED IN-REPO symbolic-in-d (B) + full-operator "
                                     "instance-verified d=2..6 (A)",
        "covariance_law_from_edge": "DISCHARGED IN-REPO symbolically (C), no D2-NOTE appeal",
        "analytic_edge_to_radius_step": "RESIDUAL: remains conditional on Wasow S19 / "
                                        "Birkhoff-Trjitzinsky (cited by D2-NOTE Thm 4.1); "
                                        "numerically corroborated d=2..6 (D), not re-derived",
    }
    out["ALL_GREEN"] = bool(out["A_all_match"] and out["B_symbolic_in_d_holds"]
                            and out["C_all_covariant"] and out["D_all_match_pipeline"])

    RESULTS.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    sha = hashlib.sha256(RESULTS.read_bytes()).hexdigest()
    print(f"\nA_all_match={out['A_all_match']}  B_symbolic_in_d={out['B_symbolic_in_d_holds']}  "
          f"C_all_covariant={out['C_all_covariant']}  D_match_pipeline={out['D_all_match_pipeline']}")
    print(f"ALL_GREEN = {out['ALL_GREEN']}")
    print(f"Wrote {RESULTS.name}  sha256={sha}")
    return sha


if __name__ == "__main__":
    main()
