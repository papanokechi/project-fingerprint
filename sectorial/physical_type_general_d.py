#!/usr/bin/env python3
"""Q2': general-d PHYSICAL branch-exponent law -- is the TYPE axis d-free?

Task: T1-EBR-THEOREM-52W v2, Q2'.  Parent T1-SECTORIAL-UPGRADE v5.
Discipline: falsification-first, AEAL, draft-only, no git side effects.  HALT > assume.
SCOPE: physical-object branch EXPONENT, general d, positive-b families.  NOT the fluctuation
(HALTs at d=3, irrelevant), NOT amplitudes/Stokes, NOT location (banked).  Stop at the
exponent-law verdict; NO proof of the full localization theorem (that is Q4' assembly).

OBJECT: G(zeta^d)=sum g_n zeta^{dn}, g_n=Q_n/(dn)!, Q_n=b(n)Q_{n-1}+Q_{n-2}, b(n)=beta_d n^d
+ b_{d-1} n^{d-1}+...  Read the branch exponent at s=R=xi0^d=d^d/beta_d in the s=zeta^d plane.
Use r_n=g_n/g_{n-1}=(Q_n/Q_{n-1})/prod_{j=0}^{d-1}(dn-j) -- NO factorials needed (positivity
g_n>0 <=> Q_n>0).  Darboux model r_n=(1/R)(1+(gamma-1)/n+...), G~(1-s/R)^{-gamma}, alpha_s=-gamma.
s=zeta^d map near zeta=xi0: s-R=zeta^d-xi0^d ~ d xi0^{d-1}(zeta-xi0) (REGULAR linear, nonzero since
xi0!=0) => alpha_zeta=alpha_s at EACH of the d preimages zeta=xi0*exp(2pi i k/d) (verified the
conversion holds for d>2 multi-preimage clusters, not just d=2).

CONJECTURE TO FALSIFY (a 2-point fit from d=2 gamma=3/2+b1/beta2, d=3 gamma=2+b2/beta3):
    gamma_conj(d) = (d+1)/2 + b_{d-1}/beta_d.
The constant (d+1)/2 is a GUESS fixed by only d in {2,3}; d>=4 is the test.  Also unknown:
whether sub-subleading b_{d-2} enters at d>=4 (the prod_{j}(dn-j) has more terms at higher d).
The conjecture MUST be allowed to fail.

VERDICT: TYPE-LAW-SYMBOLIC (d-free closed form, derived not just fit, surviving b_{d-1} AND
b_{d-2} sweeps) / TYPE-LAW-PER-D / CONJECTURE-FALSE / HALT-DARBOUX-DEGRADE.
No git side effects.  Draft-only.
"""
from __future__ import annotations

import hashlib
import json

import mpmath as mp


def b_eval(coeffs, n):
    nn = mp.mpf(n); acc = mp.mpf(0)
    for a in coeffs:
        acc = acc * nn + mp.mpf(a)
    return acc


def neville_zero(xs, ys):
    n = len(xs); P = list(ys)
    for k in range(1, n):
        for i in range(n - k):
            P[i] = (P[i] * (0 - xs[i + k]) - P[i + 1] * (0 - xs[i])) / (xs[i] - xs[i + k])
    return P[0]


def stable_digits(x, y):
    dd = abs(mp.mpf(x) - mp.mpf(y))
    if dd == 0:
        return float("inf")
    return float(-mp.log10(dd / max(abs(mp.mpf(x)), mp.mpf(1))))


def analyse(d, coeffs, N, dps):
    """coeffs high->low [a_d..a_0].  Returns dict; gates location then reads exponent."""
    with mp.workdps(dps):
        beta_d = coeffs[0]
        b_dm1 = coeffs[1]            # subleading coeff
        b_dm2 = coeffs[2] if len(coeffs) >= 3 else 0   # sub-subleading
        R = mp.mpf(d) ** d / mp.mpf(beta_d)
        xi0 = mp.mpf(d) / mp.power(mp.mpf(beta_d), mp.mpf(1) / d)

        # positivity precondition
        b_min = min(b_eval(coeffs, n) for n in range(1, N + 1))
        Q = [mp.mpf(1), b_eval(coeffs, 1)]
        for n in range(2, N + 1):
            Q.append(b_eval(coeffs, n) * Q[-1] + Q[-2])
        Q_pos = all(q > 0 for q in Q)
        positivity = (b_min > 0) and Q_pos

        # r_n = g_n/g_{n-1} = (Q_n/Q_{n-1}) / prod_{j=0}^{d-1}(dn-j)
        def poch(n):
            p = mp.mpf(1)
            for j in range(d):
                p *= (d * n - j)
            return p
        r = {n: (Q[n] / Q[n - 1]) / poch(n) for n in range(1, N + 1)}

        # single-dominant check: r_n monotone (no oscillation) over the tail
        tail = [r[n] for n in range(N - 200, N + 1)]
        diffs = [tail[i + 1] - tail[i] for i in range(len(tail) - 1)]
        sign_changes = sum(1 for i in range(len(diffs) - 1) if diffs[i] * diffs[i + 1] < 0)
        single_dominant = sign_changes <= 1   # smooth/monotone => one dominant real singularity

        def gamma_on(nodes, anchored):
            hs = [mp.mpf(1) / n for n in nodes]
            if anchored:
                e = [n * (R * r[n] - 1) for n in nodes]
                return neville_zero(hs, e) + 1
            # R-free: extrapolate r_n -> 1/R, then e_n with measured invR
            invR = neville_zero(hs, [r[n] for n in nodes])
            e = [n * (r[n] / invR - 1) for n in nodes]
            return neville_zero(hs, e) + 1, 1 / invR

        win_hi = list(range(N - 20 * 16, N + 1, 16))
        win_lo = list(range(N - 640 - 20 * 16, N - 640 + 1, 16))
        gA_hi, R_meas = gamma_on(win_hi, anchored=False)
        gA_lo, _ = gamma_on(win_lo, anchored=False)
        gB_hi = gamma_on(win_hi, anchored=True)
        gB_lo = gamma_on(win_lo, anchored=True)

        # LOCATION GATE: R_meas must equal R=xi0^d (NOT 2xi0 etc) to >=30 dig
        gate_digits = stable_digits(R_meas, R)
        gate_pass = gate_digits >= 30.0
        not_2xi0 = stable_digits(R_meas, (2 ** d) * R) < 1.0  # R != (2xi0)^d=2^d R

        gamma_conj = mp.mpf(d + 1) / 2 + mp.mpf(b_dm1) / beta_d
        ab_agree = stable_digits(gA_hi, gB_hi)
        order_stable = min(stable_digits(gA_hi, gA_lo), stable_digits(gB_hi, gB_lo))
        vs_conj = stable_digits(gB_hi, gamma_conj)
        method_gate = (ab_agree >= 10 and order_stable >= 10)

        alpha_s = -gB_hi
        nearest_int = mp.nint(alpha_s)
        is_branch = stable_digits(alpha_s, nearest_int) < 10   # non-integer => branch

        return {
            "degree": d, "coeffs_hi_to_lo": coeffs, "beta_d": beta_d,
            "b_dminus1": b_dm1, "b_dminus2": b_dm2,
            "xi0": mp.nstr(xi0, 24), "R_exact_xi0_pow_d": mp.nstr(R, 24),
            "positivity_ok": bool(positivity), "single_dominant": bool(single_dominant),
            "sign_changes_tail": sign_changes,
            "GATE_location": {
                "R_measured": mp.nstr(R_meas, 30), "gate_digits": round(gate_digits, 1),
                "gate_pass": bool(gate_pass), "R_is_xi0pow_d_not_2pow_d": bool(not_2xi0),
            },
            "gamma_measured_A_Rfree": mp.nstr(gA_hi, 22),
            "gamma_measured_B_anchored": mp.nstr(gB_hi, 22),
            "gamma_conjecture_(d+1)/2+b_dm1/beta": mp.nstr(gamma_conj, 22),
            "method_AB_agree_digits": round(ab_agree, 1),
            "order_stable_digits": round(order_stable, 1),
            "measured_vs_conjecture_digits": round(vs_conj, 1),
            "method_gate_pass": bool(method_gate),
            "alpha_s": mp.nstr(alpha_s, 22), "is_branch_point": bool(is_branch),
            "exponent_recorded": bool(gate_pass and method_gate),
        }


_RUN_SENSITIVE = {"HERE", "abspath", "absolute_path", "timestamp", "cwd", "_path"}


def canonical_bytes(obj):
    filtered = {k: v for k, v in obj.items() if k not in _RUN_SENSITIVE}
    s = json.dumps(filtered, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return (s + "\n").encode("utf-8")


def main():
    DPS = 240
    N = 1100

    # Representatives.  coeffs high->low [a_d..a_0].  Positive-b families.
    # group label encodes the sweep: 'reconfirm', 'b_dm1_sweep' (subleading), 'b_dm2_sweep' (sub-sub).
    families = [
        # reconfirm d=2,3
        ("d2_recon", 2, [3, 1, 1], "reconfirm"),
        ("d3_recon", 3, [2, 1, -1, 1], "reconfirm"),
        # d=4 : beta=1, base b3=0
        ("d4_b3_0", 4, [1, 0, 0, 0, 1], "b_dm1_sweep"),
        ("d4_b3_1", 4, [1, 1, 0, 0, 1], "b_dm1_sweep"),
        ("d4_b3_3", 4, [1, 3, 0, 0, 1], "b_dm1_sweep"),
        # d=4 : sub-subleading b2 sweep at fixed b3=1 (gamma must stay 7/2 if conjecture holds)
        ("d4_b2_5",  4, [1, 1, 5, 0, 1], "b_dm2_sweep"),
        ("d4_b2_20", 4, [1, 1, 20, 0, 1], "b_dm2_sweep"),
        # d=5 : beta=1, base b4=0
        ("d5_b4_0", 5, [1, 0, 0, 0, 0, 1], "b_dm1_sweep"),
        ("d5_b4_1", 5, [1, 1, 0, 0, 0, 1], "b_dm1_sweep"),
        ("d5_b4_2", 5, [1, 2, 0, 0, 0, 1], "b_dm1_sweep"),
        # d=5 : sub-subleading b3 sweep at fixed b4=1 (gamma must stay 4)
        ("d5_b3_5", 5, [1, 1, 5, 0, 0, 1], "b_dm2_sweep"),
        # d=6 : beta=1, base b5=0
        ("d6_b5_0", 6, [1, 0, 0, 0, 0, 0, 1], "b_dm1_sweep"),
        ("d6_b5_1", 6, [1, 1, 0, 0, 0, 0, 1], "b_dm1_sweep"),
        # d=6 : sub-subleading b4 sweep at fixed b5=1 (gamma must stay 9/2)
        ("d6_b4_7", 6, [1, 1, 7, 0, 0, 0, 1], "b_dm2_sweep"),
    ]

    results = []
    for label, d, coeffs, group in families:
        r = analyse(d, coeffs, N, DPS)
        r["label"] = label; r["group"] = group
        results.append(r)

    # ---- confront conjecture ----
    recorded = [r for r in results if r["exponent_recorded"]]
    conj_ok = all(r["measured_vs_conjecture_digits"] >= 10 for r in recorded)
    all_branch_or_pole_clean = all(r["GATE_location"]["gate_pass"] for r in recorded)
    # b_dm2 invariance: within each (d, b_dm1) fixed group, gamma must be independent of b_dm2.
    # compare each b_dm2_sweep family to its base b_dm1 family (same d, same b_dm1).
    with mp.workdps(DPS):
        b_dm2_invariant = True
        for r in results:
            if r["group"] == "b_dm2_sweep" and r["exponent_recorded"]:
                base = next((x for x in results if x["degree"] == r["degree"]
                             and x["b_dminus1"] == r["b_dminus1"]
                             and x["group"] == "b_dm1_sweep" and x["exponent_recorded"]), None)
                if base is None:
                    b_dm2_invariant = False
                else:
                    d_ = stable_digits(mp.mpf(r["gamma_measured_B_anchored"]),
                                       mp.mpf(base["gamma_measured_B_anchored"]))
                    r["gamma_vs_same_b_dm1_base_digits"] = round(d_, 1)
                    if d_ < 10:
                        b_dm2_invariant = False
        # constant sequence (d+1)/2 confirmed at each measured d?
        constants = {}
        for r in recorded:
            d = r["degree"]
            constants[d] = mp.nstr(mp.mpf(r["gamma_measured_B_anchored"])
                                   - mp.mpf(r["b_dminus1"]) / r["beta_d"], 16)

    all_gates = all(r["exponent_recorded"] for r in results)
    if all_gates and conj_ok and b_dm2_invariant:
        verdict = "TYPE-LAW-SYMBOLIC"
        vtext = ("The physical branch exponent obeys the d-FREE closed form gamma=(d+1)/2+b_{d-1}/beta_d at "
                 "ALL measured d in {2,3,4,5,6}: location gate (R=xi0^d) >=30 dig, methods agree >=10 dig, "
                 "measured=conjecture >=10 dig, b_{d-1} sweeps track, and b_{d-2} sweeps leave gamma INVARIANT "
                 "(sub-subleading does NOT enter). Confirmed by the symbolic O(1/n) derivation: "
                 "r_n=g_n/g_{n-1}=(Q_n/Q_{n-1})/prod_{j=0}^{d-1}(dn-j); Q_n/Q_{n-1}=b(n)+O(n^-d); "
                 "b(n)/(beta_d n^d)=1+(b_{d-1}/beta_d)/n+(b_{d-2}/beta_d)/n^2+...; "
                 "prod=d^d n^d(1-(d-1)/(2n)+...); so the O(1/n) coeff (=gamma-1) is b_{d-1}/beta_d+(d-1)/2, "
                 "d-free, and b_{d-2} enters only at O(1/n^2) (NOT the exponent). TYPE axis is symbolic-in-d on "
                 "the physical object, like location. L_loc TYPE component lifts to all positive-b d.")
    elif all_gates and conj_ok and not b_dm2_invariant:
        verdict = "TYPE-LAW-PER-D (b_dm2 enters)"
        vtext = "Exponents read clean and match (d+1)/2+b_{d-1}/beta_d at base families, BUT b_{d-2} sweep moves gamma => the 2-coeff law is INCOMPLETE; record corrected form."
    elif all_gates and not conj_ok:
        verdict = "CONJECTURE-FALSE"
        vtext = "Exponents read clean but the (d+1)/2 constant fit BREAKS at some d>=4; see constants sequence; re-fit honestly."
    else:
        verdict = "HALT-DARBOUX-DEGRADE"
        vtext = "Some d>=4 family failed the location/method gate (multi-dominant or ill-conditioned); exponent not recorded there. TYPE stays d=2,3(+passing d)-only."

    out = {
        "task": "T1-EBR-THEOREM-52W v2 Q2': general-d PHYSICAL branch-exponent law (is it d-free?)",
        "object": "G(zeta^d)=sum g_n zeta^{dn}, g_n=Q_n/(dn)!; exponent at s=R=xi0^d via r_n=(Q_n/Q_{n-1})/prod_{j<d}(dn-j)",
        "scope": "physical branch exponent, general d, positive-b; NOT fluctuation, NOT amplitudes, NOT location",
        "conjecture": "gamma=(d+1)/2 + b_{d-1}/beta_d  (2-point fit d in {2,3}; d>=4 is the falsification test)",
        "s_to_zeta_map": "s-R=zeta^d-xi0^d ~ d xi0^{d-1}(zeta-xi0): regular linear at each of d preimages => alpha_zeta=alpha_s (verified d>2 cluster)",
        "dps": DPS, "order_N": N,
        "families": results,
        "all_location+method_gates_pass": bool(all_gates),
        "conjecture_holds_all_recorded": bool(conj_ok),
        "b_dminus2_invariance_(sub-subleading_drops_out)": bool(b_dm2_invariant),
        "constant_sequence_gamma_minus_b_dm1_over_beta_by_degree": constants,
        "symbolic_O(1/n)_derivation": ("gamma-1 = O(1/n) coeff of (Q_n/Q_{n-1})/prod_{j=0}^{d-1}(dn-j) "
                                       "= b_{d-1}/beta_d + (d-1)/2; b_{d-2} only at O(1/n^2); d-free. "
                                       "(d+1)/2 = 1+(d-1)/2.)"),
        "VERDICT": verdict, "VERDICT_text": vtext,
        "scope_caveats": [
            "TYPE EXPONENT only -- a COMPLETE localization argument (Q4') may also need the amplitude/",
            "connection datum; this run does NOT certify that. L_loc TYPE lifts on TYPE-LAW-SYMBOLIC, but",
            "L_loc as a whole stays ARGUED-CONDITIONAL pending Q4' assembly.",
            "Positive-b families only (b(n)>0 all n>=1); non-positive-b out of scope (named residual).",
            "Physical TYPE is degree/family dependent in CHARACTER: integer gamma => pole (e.g. d3 b=n^3+1 -> 2,",
            "d5 b=n^5+1 -> 3), non-integer => branch -- the LAW is uniform but the pole/branch character varies.",
            "Tested representatives d in {2,3,4,5,6}; all-d rests on the symbolic d-free derivation + per-d positivity.",
            "No grade change, no propagation, git untouched.",
        ],
    }

    sha = hashlib.sha256(canonical_bytes(out)).hexdigest()
    final = dict(out); final["canonical_sha256_of_hashfree_object"] = sha
    with open("physical_type_general_d_results.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(final, indent=2, ensure_ascii=False, default=str)); fh.write("\n")

    print("=" * 92)
    print("Q2' general-d PHYSICAL branch-exponent law -- is gamma=(d+1)/2+b_{d-1}/beta_d d-free?")
    print("=" * 92)
    print("%-10s %-7s %-9s %-14s %-14s %-7s %-7s %-7s %-6s" %
          ("family", "group", "b=[..]", "gamma_meas", "gamma_conj", "vsConj", "gate", "Rgate", "rec"))
    for r in results:
        print("%-10s %-7s %-9s %-14s %-14s %-7s %-7s %-7s %-6s" % (
            r["label"], r["group"][:7], str(r["coeffs_hi_to_lo"])[:9],
            r["gamma_measured_B_anchored"][:13], r["gamma_conjecture_(d+1)/2+b_dm1/beta"][:13],
            r["measured_vs_conjecture_digits"], r["order_stable_digits"],
            r["GATE_location"]["gate_digits"], r["exponent_recorded"]))
    print("-" * 92)
    print("constants gamma-b_dm1/beta by degree: %s" % constants)
    print("all gates pass            : %s" % all_gates)
    print("conjecture holds          : %s" % conj_ok)
    print("b_{d-2} invariance        : %s" % b_dm2_invariant)
    print("VERDICT: %s" % verdict)
    print(vtext)
    print("canonical sha256: %s" % sha)


if __name__ == "__main__":
    main()
