#!/usr/bin/env python3
"""General-d positivity lift of the H-noclose LOCATION result (all d, location only).

Task: T1-EBR-THEOREM-52W -- general-d positivity lift.  Parent: T1-SECTORIAL-UPGRADE v5.
Discipline: falsification-first, AEAL, draft-only, no git side effects.  LOCATION ONLY --
NOT type/exponent (BRANCH-S/N), NOT the FLAG-C fluctuation bridge.  No proof step beyond
the location question.

d=2 LOCATION is UNCONDITIONAL (bridge2_othersheet_d2.py, sha 28105561).  The d=2 argument
used NOTHING about d=2 except g_n>0.  This run tests the uniform lift on the generating-
function Borel object at d in {3,4,5} (d=3,5 odd = ramified rank q=(d+2)/2 half-integer),
sidestepping the ramification that blocked the d=3 FLUCTUATION type measurement.

TWO SEPARABLE CLAIMS (not conflated):
  CLAIM A (positivity => all-directions radius).  B[y-hat_d](zeta)=G(zeta^d)=sum g_n zeta^{dn},
     g_n=Q_n/(dn)!>0.  Pringsheim: radius(G)=nearest-singularity distance in ALL s-directions,
     guaranteed singularity on +real s-axis; B is a single-valued zeta-power-series, analytic
     in |zeta|<radius^{1/d}, zeta=0 regular (g_0=1).  => "nothing strictly closer than the
     radius" is IMMEDIATE for any d once g_n>0.  [The EASY half; transfers identically.]
  CLAIM B (the radius VALUE is xi0^d).  radius(G in s)=R_d=d^d/beta_d, i.e. zeta-edge exactly
     at xi0=d/beta_d^{1/d}.  This is a SEPARATE fact, NOT inherited from Claim A.  Two legs:
     (i) ALGEBRAIC, d-FREE: R_d = lim g_{n-1}/g_n = lim (Q_{n-1}/Q_n)(Gamma(dn+1)/Gamma(dn-d+1))
         = lim (1/(beta_d n^d)) * (dn)(dn-1)...(dn-d+1) = d^d/beta_d.  Inputs: Q_n/Q_{n-1}~b(n)
         ~beta_d n^d (since Q_{n-2}/Q_{n-1}->0, super-exponential growth) and the Pochhammer
         ~ d^d n^d.  Holds for ALL d>=2, ANY positive b with leading coeff beta_d.  Ties to the
         M9 symbolic-in-d edge chi_d=1+(-1)^{d+1}(beta_d/d^d)c^d, |c|=xi0=d/beta_d^{1/d}.
     (ii) NUMERIC: Domb-Sykes on g_n at each d, recover R_d=d^d/beta_d to >=30 digits.

RAMIFICATION BYPASS (Step 3, the central claim).  The d=3 FLUCTUATION blocked on q=5/2
half-integer rank because the WKB fluctuation lives on a FRACTIONAL-POWER transseries cover
(exp(c/u + c'/u^{1/2}+...), ramified Borel plane).  The generating-function object does NOT:
B[y-hat_d]=sum g_n zeta^{dn} is an honest single-valued power series in zeta with POSITIVE
Borel coefficients g_n=Q_n/(dn)!; its radius is a plain radius of convergence -- no cover, no
ramification.  Division by the positive number (dn)! cannot introduce sign changes, so g_n>0
is robust at odd d (verified numerically, not just by the b(n)>0 induction).  Hence the odd-d
ramification obstruction is BYPASSED for the LOCATION question.

Families = the lemma31 catalogue (pslq/xi0_d3/lemma31_edge_derivation.py NUMERIC_FAMILIES),
coeffs high->low [a_d..a_0].  d3_b2 has a negative subleading coeff (positivity-risk: checked).
No git side effects.  Draft-only.
"""
from __future__ import annotations

import hashlib
import json

import mpmath as mp

# (label, d, coeffs high->low [a_d..a_0], beta_d)   -- lemma31 catalogue
FAMILIES = [
    ("d3_b2", 3, [2, 1, -1, 1],       2),
    ("d3_b1", 3, [1, 0, 0, 1],        1),
    ("d4_b1", 4, [1, 0, 0, 0, 1],     1),
    ("d4_b7", 4, [7, 0, 0, 1, 0],     7),
    ("d5_b1", 5, [1, 0, 0, 0, 0, 1],  1),
    ("d5_b2", 5, [2, 0, 0, 1, 0, 1],  2),
]


def b_eval(coeffs, n):
    nn = mp.mpf(n)
    acc = mp.mpf(0)
    for a in coeffs:
        acc = acc * nn + mp.mpf(a)
    return acc


def compute_Q(coeffs, N, dps):
    with mp.workdps(dps):
        Q = [mp.mpf(1), b_eval(coeffs, 1)]
        for n in range(2, N + 1):
            Q.append(b_eval(coeffs, n) * Q[-1] + Q[-2])
        return Q


def neville_zero(xs, ys):
    n = len(xs)
    P = list(ys)
    for k in range(1, n):
        for i in range(n - k):
            P[i] = (P[i] * (0 - xs[i + k]) - P[i + 1] * (0 - xs[i])) / (xs[i] - xs[i + k])
    return P[0]


def stable_digits(x, y):
    x = mp.mpf(x); y = mp.mpf(y)
    dd = abs(x - y)
    if dd == 0:
        return float("inf")
    return float(-mp.log10(dd))


def pade_interior(g, R, M, dps):
    """Pade[M/M] of sum (g_n R^n) s'^n; return genuine interior poles (|s'|<0.99, not Froissart)."""
    with mp.workdps(dps):
        c = [g[n] * R ** n for n in range(2 * M + 1)]
        p, q = mp.pade(c, M, M)
        poles = mp.polyroots(q[::-1], maxsteps=300, extraprec=300)
        zeros = mp.polyroots(p[::-1], maxsteps=300, extraprec=300) if len(p) > 1 else []
        gi = []
        for r in poles:
            if abs(r) < mp.mpf("0.99"):
                dz = min((abs(r - z) for z in zeros), default=mp.inf)
                if dz > mp.mpf("1e-6"):
                    gi.append(mp.nstr(abs(r), 8))
        return gi


_RUN_SENSITIVE = {"HERE", "abspath", "absolute_path", "timestamp", "cwd", "_path"}


def canonical_bytes(obj):
    filtered = {k: v for k, v in obj.items() if k not in _RUN_SENSITIVE}
    s = json.dumps(filtered, sort_keys=True, ensure_ascii=False,
                   separators=(",", ":"), default=str)
    return (s + "\n").encode("utf-8")


def analyse(label, d, coeffs, beta_d, N, dps):
    mp.mp.dps = dps
    xi0 = mp.mpf(d) / mp.power(mp.mpf(beta_d), mp.mpf(1) / d)
    R_exact = mp.mpf(d) ** d / mp.mpf(beta_d)              # = xi0^d

    Q = compute_Q(coeffs, N, dps)
    # STEP 0 positivity: b(n)>0 for all n in [1,N], Q_n>0, g_n>0
    b_min = min(b_eval(coeffs, n) for n in range(1, N + 1))
    b_positive = b_min > 0
    Q_positive = all(q > 0 for q in Q)
    g = [Q[n] / mp.factorial(d * n) for n in range(N + 1)]
    g_min = min(g)
    g_positive = g_min > 0
    g0_regular = (g[0] == 1)

    # STEP 2 numeric leg: Domb-Sykes on g_n -> R_d
    nodes = list(range(N - 20 * 12, N + 1, 12))           # 660..900, 21 nodes
    with mp.workdps(dps):
        hs = [mp.mpf(1) / n for n in nodes]
        rg = [g[n] / g[n - 1] for n in nodes]
        inv_R = neville_zero(hs[-21:], rg[-21:])
        R_meas = 1 / inv_R
        zeta_radius = mp.power(R_meas, mp.mpf(1) / d)
        # cross-check via beta extraction
        rb = [Q[n] / (Q[n - 1] * mp.mpf(n) ** d) for n in nodes]
        beta_meas = neville_zero(hs[-21:], rb[-21:])
        xi0_from_beta = mp.mpf(d) / mp.power(beta_meas, mp.mpf(1) / d)

    R_digits = stable_digits(R_meas, R_exact)
    xi0_digits = stable_digits(zeta_radius, xi0)
    beta_digits = stable_digits(beta_meas, beta_d)
    gate_b = (R_digits >= 30.0) and (xi0_digits >= 30.0)
    # confirm NOT a fluctuation scale: zeta-radius is xi0, distinctly NOT 2*xi0
    not_2xi0 = stable_digits(zeta_radius, 2 * xi0) < 1.0

    # Step 1/3 defense-in-depth: no genuine interior Pade pole
    gi = pade_interior(g, R_exact, M=60, dps=110)
    no_interior = (len(gi) == 0)

    location_ok = (b_positive and Q_positive and g_positive and g0_regular
                   and gate_b and not_2xi0 and no_interior)

    return {
        "label": label, "d": d, "beta_d": beta_d, "coeffs_hi_to_lo": coeffs,
        "xi0_exact": mp.nstr(xi0, 30), "R_exact_xi0_pow_d": mp.nstr(R_exact, 30),
        "STEP0_positivity": {
            "b_min_over_n_1_to_N": mp.nstr(b_min, 12), "b_positive": bool(b_positive),
            "Q_all_positive": bool(Q_positive), "g_min": mp.nstr(g_min, 8),
            "g_all_positive": bool(g_positive), "g0_regular_equals_1": bool(g0_regular),
        },
        "STEP2_radius_value": {
            "R_measured": mp.nstr(R_meas, 30), "R_agree_vs_xi0pow_d_digits": round(R_digits, 1),
            "zeta_radius_R_pow_1_over_d": mp.nstr(zeta_radius, 30),
            "zeta_radius_agree_vs_xi0_digits": round(xi0_digits, 1),
            "beta_measured": mp.nstr(beta_meas, 24), "beta_agree_digits": round(beta_digits, 1),
            "xi0_from_beta": mp.nstr(xi0_from_beta, 24),
            "GATE_B_pass": bool(gate_b), "zeta_radius_is_xi0_not_2xi0": bool(not_2xi0),
        },
        "STEP1_3_no_closer": {
            "pade_genuine_interior_poles": gi, "no_interior_singularity": bool(no_interior),
        },
        "location_ok": bool(location_ok),
    }


def main():
    DPS = 200
    N = 900
    results = [analyse(*fam, N=N, dps=DPS) for fam in FAMILIES]

    all_ok = all(r["location_ok"] for r in results)
    odd_ok = all(r["location_ok"] for r in results if r["d"] % 2 == 1)
    gate_b_all = all(r["STEP2_radius_value"]["GATE_B_pass"] for r in results)
    pos_all = all(r["STEP0_positivity"]["g_all_positive"] for r in results)

    if all_ok:
        verdict = ("H-noclose LOCATION LIFTS to all tested degrees d in {3,4,5} on the generating-function "
                   "object, UNIFORMLY, ramification SIDESTEPPED. Claim A (positivity=>all-directions radius) "
                   "transfers identically (g_n>0 confirmed incl. odd d=3,5); Claim B (radius=d^d/beta_d=xi0^d) "
                   "holds per-tested-d numerically to >=30 dig AND via the d-FREE algebraic limit "
                   "R_d=lim g_{n-1}/g_n=d^d/beta_d, tied to the M9 symbolic-in-d edge chi_d (|c|=xi0). The "
                   "odd-d rank-(d+2)/2 ramification that blocked the FLUCTUATION type measurement does NOT "
                   "afflict this single-valued positive-coefficient zeta-power-series. LOCATION HALF of EBR "
                   "universality at the tested degrees + symbolic-in-d Claim-B link. TYPE axis untouched "
                   "(BRANCH-S/N out of reach of positivity); L_loc stays ARGUED-CONDITIONAL; FLAG-C bridge "
                   "open; no propagation.")
    else:
        verdict = "HALT -- a claim/degree failed location; see per-family location_ok. Location stays d=2-only."

    out = {
        "task": "T1-EBR-THEOREM-52W general-d positivity lift (H-noclose LOCATION, all d)",
        "object": "B[y-hat_d](zeta)=G(zeta^d)=sum g_n zeta^{dn}, g_n=Q_n/(dn)!, Q_n=b(n)Q_{n-1}+Q_{n-2}",
        "scope": "LOCATION only (nearest-singularity radius + nothing-closer); NOT type/exponent; NOT FLAG-C",
        "order_N": N, "dps": DPS,
        "claim_A_positivity_all_directions": bool(pos_all),
        "claim_B_radius_value_xi0pow_d_GATE_B": bool(gate_b_all),
        "claim_B_algebraic_leg_d_free": ("R_d = lim g_{n-1}/g_n = lim (Q_{n-1}/Q_n)*Poch(dn-d+1,d) "
                                         "= (1/(beta_d n^d))*(d^d n^d) = d^d/beta_d, for ALL d>=2, any positive b; "
                                         "matches M9 symbolic edge chi_d root |c|=xi0=d/beta_d^(1/d). Genuinely d-free."),
        "ramification_bypass": ("odd-d rank (d+2)/2 half-integer ramification afflicts the WKB FLUCTUATION "
                                "(fractional-power transseries cover), NOT the generating-function germ: "
                                "B[y-hat_d]=sum g_n zeta^{dn} is single-valued in zeta with positive g_n; "
                                "(dn)!-division preserves sign; g_n>0 verified numerically at odd d=3,5."),
        "families": results,
        "all_tested_d_location_ok": bool(all_ok),
        "odd_d_location_ok": bool(odd_ok),
        "VERDICT": verdict,
        "scope_caveats": [
            "LOCATION only: firms WHERE the nearest Borel singularity is (|zeta|=xi0, none closer) on the",
            "generating-function object; does NOT touch the singularity TYPE/exponent (BRANCH-S/N) -- positivity",
            "cannot reach type; L_loc stays ARGUED-CONDITIONAL.",
            "Does NOT close the FLAG-C object-bridge to the WKB fluctuation/transseries object (radius 2xi0).",
            "Positivity scope: covers families with b(n)>0 for all n>=1 (verified for the 6 catalogue families,",
            "incl. d3_b2 which has a negative subleading coeff but stays positive). A family with b(n)<=0 at some",
            "n would be out of this argument's scope (HALT-POSITIVITY-SCOPE) -- none here.",
            "Tested representatives d in {3,4,5} (plus d=2 prior). Claim-B numeric is per-tested-d; the algebraic",
            "leg is d-free, so all-d location rests on that d-free limit + per-d positivity, not on d<=5 numerics.",
            "Says nothing about continuation past |zeta|=xi0 (genuine other sheets).",
            "No grade change / no propagation this run.",
        ],
    }

    sha = hashlib.sha256(canonical_bytes(out)).hexdigest()
    final = dict(out)
    final["canonical_sha256_of_hashfree_object"] = sha
    with open("positivity_lift_general_d_results.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(final, indent=2, ensure_ascii=False, default=str))
        fh.write("\n")

    print("=" * 80)
    print("General-d positivity lift -- H-noclose LOCATION (location only)")
    print("=" * 80)
    print("%-7s %-3s %-5s %-14s %-10s %-10s %-9s %-7s" %
          ("fam", "d", "beta", "xi0", "R=xi0^d", "Rdig", "xi0dig", "loc_ok"))
    for r in results:
        s2 = r["STEP2_radius_value"]
        print("%-7s %-3d %-5d %-14s %-10s %-10s %-9s %-7s" %
              (r["label"], r["d"], r["beta_d"], r["xi0_exact"][:12], r["R_exact_xi0_pow_d"][:9],
               s2["R_agree_vs_xi0pow_d_digits"], s2["zeta_radius_agree_vs_xi0_digits"], r["location_ok"]))
    print("-" * 80)
    print("positivity g_n>0 all families (incl odd d): %s" % pos_all)
    print("GATE B (radius=d^d/beta) all families      : %s" % gate_b_all)
    print("odd-d location ok (ramification bypassed)  : %s" % odd_ok)
    print("ALL tested d location ok                   : %s" % all_ok)
    print("VERDICT: %s" % verdict)
    print("canonical sha256: %s" % sha)


if __name__ == "__main__":
    main()
