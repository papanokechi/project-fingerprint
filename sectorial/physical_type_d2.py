#!/usr/bin/env python3
"""d=2 PHYSICAL singularity TYPE at xi0 (BRANCH-S/N fork) on G(zeta^2).

Task: T1-EBR-THEOREM-52W v2 -- Q1' W5-9.  Parent T1-SECTORIAL-UPGRADE v5.
Discipline: falsification-first, AEAL, draft-only, no git side effects.  TYPE at d=2 ONLY,
on the PHYSICAL object G(zeta^2); NOT d>=3, NOT the FLAG-C fluctuation bridge, NOT location.
No proof step.  HALT-PHYS-TYPE > read a number off non-converged estimators.

Physical object (banked): B[y-hat_2](zeta)=G(zeta^2)=sum g_n zeta^{2n}, g_n=Q_n/(2n)!>0,
Q_n=b(n)Q_{n-1}+Q_{n-2}, b(n)=3n^2+n+1, beta_2=3.  Radius xi0=2/sqrt3, R=xi0^2=4/3.  The two
real saddles +-xi0 both map to s=zeta^2=+R; read the exponent of G(s) at s=R (cleaner than the
zeta-plane where the two saddles coincide).

KEY HAZARD (expected): g_n>0 monotone makes Pringsheim/location trivial but makes Darboux
exponent extraction ILL-CONDITIONED (no sign structure).  Use methods robust to it; if the
exponent will not stabilize -> HALT-PHYS-TYPE (a real outcome, not a reason to loosen tols).

Darboux model at an algebraic singularity (s-R)^{alpha_s}, equivalently G ~ (1-s/R)^{-gamma}
with gamma = -alpha_s:  g_n ~ C * n^{gamma-1} * R^{-n} * (1+o(1)).  Ratio:
  r_n = g_n/g_{n-1} = (1/R)*(1 + (gamma-1)/n + a/n^2 + ...).
Exponent estimators:
  (a) Domb-Sykes: r_n vs 1/n, intercept 1/R, slope/intercept -> gamma-1.  [R NOT assumed]
  (b) R-anchored: e_n = n*(R*r_n - 1) -> gamma-1, Neville/Richardson accelerated.  [R=4/3 banked]
  (c) log-detection: fit log(g_n R^n) vs (log n, log log n) -> detect a log factor (logarithmic
      singularity) and a drifting pseudo-exponent (the d=3 fluctuation pathology).

s=zeta^2 map: near +xi0, (s-R)=(zeta-xi0)(zeta+xi0) ~ 2*xi0*(zeta-xi0) (regular factor) =>
alpha_zeta = alpha_s at each physical edge zeta=+-xi0.

GATE: methods (a),(b) must agree AND be stable across >=2 truncation orders to >=10 digits
before recording alpha_s; else HALT-PHYS-TYPE.
"""
from __future__ import annotations

import hashlib
import json

import mpmath as mp


def b_eval(n):
    return mp.mpf(3) * n * n + mp.mpf(n) + 1


def compute_g(N, dps):
    with mp.workdps(dps):
        Q = [mp.mpf(1), b_eval(1)]
        for n in range(2, N + 1):
            Q.append(b_eval(n) * Q[-1] + Q[-2])
        return [Q[n] / mp.factorial(2 * n) for n in range(N + 1)]


def neville_limit(xs, ys):
    """Polynomial extrapolation to x=0 (Richardson/Neville in the node abscissae xs)."""
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
    return float(-mp.log10(dd / max(abs(x), mp.mpf(1))))


def method_a_dombsykes(g, nodes, dps):
    """No R assumed: fit r_n = A + B*(1/n) over the node window; A=1/R, gamma-1 = B/A * (-1)?
    Standard Domb-Sykes uses r_n = (1/R)(1+(gamma-1)/n) => A=1/R, slope = A*(gamma-1).
    We extrapolate r_n -> 1/R (Neville) and the estimator n*(r_n/A_lim - 1) -> gamma-1."""
    with mp.workdps(dps):
        hs = [mp.mpf(1) / n for n in nodes]
        r = [g[n] / g[n - 1] for n in nodes]
        invR = neville_limit(hs, r)          # -> 1/R
        R = 1 / invR
        e = [nodes[i] * (r[i] / invR - 1) for i in range(len(nodes))]
        gamma_m1 = neville_limit(hs, e)      # -> gamma-1
        return R, gamma_m1 + 1


def method_b_anchored(g, nodes, R, dps):
    """R=4/3 banked: e_n = n*(R r_n - 1) -> gamma-1, Neville accelerated."""
    with mp.workdps(dps):
        hs = [mp.mpf(1) / n for n in nodes]
        e = [nodes[i] * (R * (g[nodes[i]] / g[nodes[i] - 1]) - 1) for i in range(len(nodes))]
        gamma_m1 = neville_limit(hs, e)
        return gamma_m1 + 1


def method_c_logdetect(g, nodes, R, dps):
    """Fit log(g_n R^n) ~ const + (gamma-1) log n + delta * log log n.
    delta ~ 0 => pure power (no log factor); |delta| away from 0 => logarithmic component."""
    with mp.workdps(dps):
        rows, rhs = [], []
        for n in nodes:
            ln = mp.log(mp.mpf(n))
            rows.append([mp.mpf(1), ln, mp.log(ln)])
            rhs.append(mp.log(g[n]) + n * mp.log(R))
        A = mp.matrix(rows); y = mp.matrix(rhs)
        # least squares via normal equations
        AtA = A.T * A
        Aty = A.T * y
        coef = mp.lu_solve(AtA, Aty)
        return coef[1] + 1, coef[2]  # gamma (=slope+1), delta (loglog coeff)


def pade_branch(g, R, M, dps):
    """Pade[M/M] of G(s): pole at R (simple) vs accumulation of poles -> branch.
    Return real poles in [R*0.8, R*4], count of poles clustering beyond R."""
    with mp.workdps(dps):
        c = [g[n] for n in range(2 * M + 1)]
        p, q = mp.pade(c, M, M)
        roots = mp.polyroots(q[::-1], maxsteps=400, extraprec=400)
        zeros = mp.polyroots(p[::-1], maxsteps=400, extraprec=400) if len(p) > 1 else []
        near = []
        for r in roots:
            if abs(mp.im(r)) < mp.mpf("1e-6") and mp.re(r) > R * mp.mpf("0.8"):
                dz = min((abs(r - z) for z in zeros), default=mp.inf)
                if dz > mp.mpf("1e-6"):          # not a Froissart doublet
                    near.append(mp.re(r))
        near = sorted(near)
        beyond = [mp.nstr(x, 10) for x in near if x > R * mp.mpf("1.001")]
        nearest = mp.nstr(min((x for x in near), key=lambda t: abs(t - R)), 14) if near else None
        return nearest, beyond


_RUN_SENSITIVE = {"HERE", "abspath", "absolute_path", "timestamp", "cwd", "_path"}


def canonical_bytes(obj):
    filtered = {k: v for k, v in obj.items() if k not in _RUN_SENSITIVE}
    s = json.dumps(filtered, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return (s + "\n").encode("utf-8")


def main():
    DPS = 260
    N = 1300
    mp.mp.dps = DPS
    R = mp.mpf(4) / 3
    xi0 = 2 / mp.sqrt(3)
    g = compute_g(N, DPS)

    # node windows at two truncation orders for stability gate
    win_hi = list(range(N - 20 * 14, N + 1, 14))      # ~1020..1300, 21 nodes
    win_lo = list(range(N - 600 - 20 * 14, N - 600 + 1, 14))  # ~420..700, 21 nodes

    Ra, gamma_a_hi = method_a_dombsykes(g, win_hi, DPS)
    _, gamma_a_lo = method_a_dombsykes(g, win_lo, DPS)
    gamma_b_hi = method_b_anchored(g, win_hi, R, DPS)
    gamma_b_lo = method_b_anchored(g, win_lo, R, DPS)
    gamma_c, delta_log = method_c_logdetect(g, win_hi, R, DPS)

    gamma_exact = mp.mpf(11) / 6           # the pre-analysis candidate (NOT assumed; tested)
    alpha_s = -gamma_b_hi                  # alpha_s = -gamma

    # agreement gates
    ab_agree = stable_digits(gamma_a_hi, gamma_b_hi)
    a_order_stable = stable_digits(gamma_a_hi, gamma_a_lo)
    b_order_stable = stable_digits(gamma_b_hi, gamma_b_lo)
    matches_11_6 = stable_digits(gamma_b_hi, gamma_exact)
    log_present = abs(delta_log) > mp.mpf("1e-3")

    # R recovered NOT 2xi0 scale: R must be 4/3 not (2xi0)^2=16/3
    R_ok = stable_digits(Ra, R) >= 10

    pade_nearest, pade_beyond = pade_branch(g, R, M=70, dps=140)
    branch_accumulation = len(pade_beyond) >= 2     # poles beyond R cluster => branch cut

    gate_pass = (ab_agree >= 10 and a_order_stable >= 10 and b_order_stable >= 10 and R_ok)

    if not gate_pass:
        verdict = "HALT-PHYS-TYPE"
        verdict_text = ("Exponent did not stabilize to >=10 digits across methods/orders "
                        "(positivity ill-conditioning realized). d=2 physical type stays OPEN.")
    else:
        gamma_is_integer = stable_digits(gamma_b_hi, mp.nint(gamma_b_hi)) >= 10
        # alpha_s = -gamma; pole <=> alpha_s non-negative integer <=> gamma a non-positive integer
        alpha_is_nonneg_int = (stable_digits(alpha_s, mp.nint(alpha_s)) >= 10) and (mp.nint(alpha_s) >= 0)
        if log_present:
            verdict = "BRANCH-N"
            verdict_text = ("Logarithmic factor detected (loglog coeff delta=%s != 0): physical d=2 "
                            "singularity is logarithmic/branch." % mp.nstr(delta_log, 6))
        elif alpha_is_nonneg_int:
            verdict = "BRANCH-S"
            verdict_text = ("alpha_s a non-negative integer with pole structure: physical d=2 "
                            "singularity is a POLE. Localization classical.")
        else:
            verdict = "BRANCH-N"
            verdict_text = ("alpha_s NON-integer = %s (gamma=%s): physical d=2 singularity is a "
                            "BRANCH POINT of exponent alpha_s. Recorded to converged precision. "
                            "Pade corroboration: poles beyond R = %s (branch-cut accumulation=%s)."
                            % (mp.nstr(alpha_s, 16), mp.nstr(gamma_b_hi, 16),
                               pade_beyond[:6], branch_accumulation))

    out = {
        "task": "T1-EBR-THEOREM-52W v2 Q1' W5-9: d=2 PHYSICAL type at xi0 (BRANCH-S/N fork)",
        "object": "G(s)=sum g_n s^n, g_n=Q_n/(2n)!, Q_n=(3n^2+n+1)Q_{n-1}+Q_{n-2}; s=zeta^2; R=4/3=xi0^2",
        "scope": "d=2 type ONLY on physical object; NOT d>=3, NOT FLAG-C, NOT location",
        "dps": DPS, "order_N": N,
        "model": "g_n ~ C n^{gamma-1} R^{-n}, G~(1-s/R)^{-gamma}, alpha_s=-gamma; (s-R)^{alpha_s}",
        "R_exact": mp.nstr(R, 30), "xi0_exact": mp.nstr(xi0, 30),
        "method_a_dombsykes_noR": {
            "R_recovered": mp.nstr(Ra, 24), "R_recovered_ok_eq_4_3": bool(R_ok),
            "gamma_hi_window": mp.nstr(gamma_a_hi, 20), "gamma_lo_window": mp.nstr(gamma_a_lo, 20),
            "order_stable_digits": round(a_order_stable, 1),
        },
        "method_b_anchored_R": {
            "gamma_hi_window": mp.nstr(gamma_b_hi, 20), "gamma_lo_window": mp.nstr(gamma_b_lo, 20),
            "order_stable_digits": round(b_order_stable, 1),
        },
        "method_c_logdetect": {
            "gamma": mp.nstr(gamma_c, 16), "loglog_coeff_delta": mp.nstr(delta_log, 8),
            "log_factor_present": bool(log_present),
        },
        "agreement": {
            "a_vs_b_digits": round(ab_agree, 1),
            "matches_11_over_6_digits": round(matches_11_6, 1),
            "gate_pass": bool(gate_pass),
        },
        "pade_branch_test": {
            "M": 70, "nearest_real_pole_to_R": pade_nearest,
            "real_poles_beyond_R": pade_beyond[:8], "branch_cut_accumulation": bool(branch_accumulation),
        },
        "measured": {
            "gamma": mp.nstr(gamma_b_hi, 20), "alpha_s_eq_minus_gamma": mp.nstr(alpha_s, 20),
            "alpha_zeta_eq_alpha_s": mp.nstr(alpha_s, 20),
            "s_to_zeta_map": "(s-R)=(zeta-xi0)(zeta+xi0)~2 xi0 (zeta-xi0): regular factor, alpha_zeta=alpha_s",
        },
        "VERDICT": verdict,
        "VERDICT_text": verdict_text,
        "scope_caveats": [
            "TYPE at d=2 alone does NOT close L_loc -- stays ARGUED-CONDITIONAL.",
            "Measured alpha_s is the PHYSICAL generating-function exponent; the fluctuation type at 2*xi0",
            "is a DIFFERENT object (FLAG-C) -- a numeric coincidence with 11/6 is NOT a claimed identity here.",
            "Location banked (xi0), unchanged. d>=3 type = Q2', not this run.",
            "No grade change, no propagation, git untouched.",
        ],
    }

    sha = hashlib.sha256(canonical_bytes(out)).hexdigest()
    final = dict(out); final["canonical_sha256_of_hashfree_object"] = sha
    with open("physical_type_d2_results.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(final, indent=2, ensure_ascii=False, default=str)); fh.write("\n")

    print("=" * 78)
    print("d=2 PHYSICAL type at xi0 -- BRANCH-S/N fork (type only)")
    print("=" * 78)
    print("R recovered (no-R Domb-Sykes): %s  (exact 4/3, ok=%s)" % (mp.nstr(Ra, 18), R_ok))
    print("gamma  method a (hi/lo)       : %s / %s" % (mp.nstr(gamma_a_hi, 16), mp.nstr(gamma_a_lo, 16)))
    print("gamma  method b (hi/lo)       : %s / %s" % (mp.nstr(gamma_b_hi, 16), mp.nstr(gamma_b_lo, 16)))
    print("gamma  method c (logfit)      : %s   delta_loglog=%s" % (mp.nstr(gamma_c, 16), mp.nstr(delta_log, 6)))
    print("a-vs-b agree digits           : %.1f" % ab_agree)
    print("order-stable digits (a/b)     : %.1f / %.1f" % (a_order_stable, b_order_stable))
    print("matches 11/6 to digits        : %.1f" % matches_11_6)
    print("alpha_s = -gamma              : %s" % mp.nstr(alpha_s, 18))
    print("Pade nearest pole / beyond-R  : %s / %s" % (pade_nearest, pade_beyond[:5]))
    print("-" * 78)
    print("VERDICT: %s -- %s" % (verdict, verdict_text))
    print("canonical sha256: %s" % sha)


if __name__ == "__main__":
    main()
