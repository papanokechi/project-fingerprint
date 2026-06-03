#!/usr/bin/env python3
"""S re-verification — prefactor-explicit, independent from-definition recompute.

Constant S is the V_quad / Painleve Stokes constant extracted from the Dingle
late-term behaviour of the WKB/Riccati formal series a_n:

    K  = lim_n | a_n * xi0^(n+beta) / ((-1)^n * Gamma(n+beta)) |   (prefactor-stripped)
    S  = prefactor * K
    beta = -1/(3 sqrt 3),  xi0 = 2/sqrt 3.

Two prefactor conventions are in circulation:
  (a) Gamma(beta_exp) ~ -6.00599   -- the v1.0 (RETRACTED) Dingle prefactor; this
      is what the pcf-research repo scripts carry (S_best = 0.43770528073458051568).
  (b) 2*pi             ~  6.28319   -- the universal large-order/resurgence
      prefactor asserted by the Painleve-V v1.1 correction (S ~ 0.45790662).

This script computes K ONCE from the documented definition (independent inline
reimplementation of the Riccati recursion) and reports S under BOTH prefactors,
so the ~4.5% discrepancy is mechanically attributed to the prefactor choice.
It writes NO canonical value -- it reports and stops.
"""
from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).parent

# External anchors (NOT transcribed as canonical; used only to attribute the
# discrepancy to a convention).
S_V10_REPO_GAMMA = "0.43770528073458051568"   # pcf-research vquad t2_iter22_s_precision.json (Gamma prefactor)
S_V11_PAPER_2PI_8DIG = "0.45790662"           # Painleve-V v1.1 paper (8 digits, operator-supplied)


def stable_digits(x, y):
    x = mp.mpf(x); y = mp.mpf(y)
    d = abs(x - y)
    if d == 0:
        return float("inf")
    return float(-mp.log10(d))


def riccati_coeffs(sigma, order):
    """WKB/Riccati recursion for the V_quad problem (documented definition)."""
    c = [mp.mpf(0)] * (order + 1)
    c[0] = sigma
    c[1] = -1 - sigma / 6
    d = [mp.mpf(0)] * (order + 1)
    d[0] = c[0] ** 2
    d[1] = 2 * c[0] * c[1]
    for k in range(2, order + 1):
        known = mp.fsum(c[i] * c[k - i] for i in range(1, k))
        rest = (3 * (known - (k - 1) * c[k - 1])
                + d[k - 1] + d[k - 2] + 6 * c[k - 1] + c[k - 2])
        c[k] = -rest / (6 * c[0])
        d[k] = 2 * c[0] * c[k] + known - (k - 1) * c[k - 1]
    return c


def formal_series_coeffs(order, dps):
    mp.mp.dps = dps
    sigma_rec = -1 / mp.sqrt(mp.mpf(3))
    rc = riccati_coeffs(sigma_rec, order=order + 10)
    f = [mp.mpf(0)] * (order + 1)
    for k in range(1, order + 1):
        if k + 1 < len(rc):
            f[k] = -rc[k + 1] / k
    a = [mp.mpf(0)] * (order + 1)
    a[0] = mp.mpf(1)
    for n in range(1, order + 1):
        s = mp.fsum(k * f[k] * a[n - k] for k in range(1, n + 1))
        a[n] = s / n
    return a


def neville_to_zero(xs, ys):
    m = len(xs)
    T = [list(ys)]
    for k in range(1, m):
        row = []
        for i in range(m - k):
            num = (0 - xs[i + k]) * T[k - 1][i] - (0 - xs[i]) * T[k - 1][i + 1]
            row.append(num / (xs[i] - xs[i + k]))
        T.append(row)
    return T[m - 1][0]


def amplitude_K(order, dps):
    """Prefactor-stripped Dingle late-term amplitude K, extrapolated n->inf."""
    mp.mp.dps = dps
    beta = -1 / (3 * mp.sqrt(mp.mpf(3)))
    xi0 = 2 / mp.sqrt(mp.mpf(3))
    a = formal_series_coeffs(order, dps)
    ns = list(range(order - 400, order + 1))
    Kn = [abs(a[n] * xi0 ** (n + beta) / (((-1) ** n) * mp.gamma(n + beta))) for n in ns]
    Kvals = []
    for w in (16, 22, 28, 34):
        idx = list(range(len(ns) - w, len(ns)))
        xs = [mp.mpf(1) / ns[i] for i in idx]
        ys = [Kn[i] for i in idx]
        Kvals.append(neville_to_zero(xs, ys))
    K = Kvals[-1]
    spread = max(abs(v - K) for v in Kvals)
    return K, spread


def main():
    DPS = 240
    # K at two independent (order, dps) settings -> cross-setting stability.
    K1, sp1 = amplitude_K(order=1400, dps=200)
    K2, sp2 = amplitude_K(order=1800, dps=DPS)
    cross = stable_digits(K1, K2)

    mp.mp.dps = DPS
    beta = -1 / (3 * mp.sqrt(mp.mpf(3)))
    gamma_pref = mp.gamma(beta)        # (a) retracted prefactor
    two_pi = 2 * mp.pi                 # (b) corrected prefactor

    S_a = K2 * abs(gamma_pref)         # convention (a): |Gamma(beta_exp)|
    S_b = K2 * two_pi                  # convention (b): 2*pi

    agree_a = stable_digits(S_a, S_V10_REPO_GAMMA)
    agree_b8 = stable_digits(S_b, S_V11_PAPER_2PI_8DIG)
    ratio = two_pi / abs(gamma_pref)

    out = {
        "method": "independent from-definition Dingle late-term; S = prefactor * K",
        "definition": "K = lim_n |a_n * xi0^(n+beta) / ((-1)^n Gamma(n+beta))|, beta=-1/(3 sqrt3), xi0=2/sqrt3",
        "dps": DPS,
        "K_setting1": "order=1400 dps=200",
        "K_setting2": "order=1800 dps=240",
        "amplitude_K": mp.nstr(K2, 30),
        "K_cross_setting_stable_digits": (None if cross == float("inf") else round(cross, 1)),
        "K_window_spread": mp.nstr(sp2, 3),
        "beta_exp": mp.nstr(beta, 20),
        "prefactor_a_gamma_beta": mp.nstr(gamma_pref, 18),
        "prefactor_b_2pi": mp.nstr(two_pi, 18),
        "prefactor_ratio_2pi_over_gamma": mp.nstr(ratio, 12),
        "S_conv_a_gamma_prefactor": mp.nstr(S_a, 22),
        "S_conv_b_2pi_prefactor": mp.nstr(S_b, 22),
        "anchor_repo_v10_gamma": S_V10_REPO_GAMMA,
        "anchor_paper_v11_2pi_8dig": S_V11_PAPER_2PI_8DIG,
        "agree_conv_a_with_repo_v10_digits": round(agree_a, 1),
        "agree_conv_b_with_paper_v11_digits": round(agree_b8, 1),
    }

    print("=" * 72)
    print("S RE-VERIFICATION — prefactor explicit (report & STOP; no canonical)")
    print("=" * 72)
    print("amplitude K           = %s" % out["amplitude_K"])
    print("  K cross-setting     = %s stable digits  (spread %s)"
          % (out["K_cross_setting_stable_digits"], out["K_window_spread"]))
    print("beta_exp              = %s" % out["beta_exp"])
    print("prefactor (a) Gamma   = %s   |Gamma| used" % out["prefactor_a_gamma_beta"])
    print("prefactor (b) 2*pi    = %s" % out["prefactor_b_2pi"])
    print("ratio 2pi/|Gamma|     = %s   (vs S ratio 0.457906/0.437705 = 1.046153)"
          % out["prefactor_ratio_2pi_over_gamma"])
    print()
    print("S (a) Gamma-prefactor = %s" % out["S_conv_a_gamma_prefactor"])
    print("    vs repo v1.0      = %s   -> agree %s digits"
          % (S_V10_REPO_GAMMA, out["agree_conv_a_with_repo_v10_digits"]))
    print("S (b) 2*pi-prefactor  = %s" % out["S_conv_b_2pi_prefactor"])
    print("    vs paper v1.1 (8) = %s   -> agree %s digits"
          % (S_V11_PAPER_2PI_8DIG, out["agree_conv_b_with_paper_v11_digits"]))

    (HERE / "S_prefactor_verify_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print()
    print("wrote %s" % (HERE / "S_prefactor_verify_results.json"))


if __name__ == "__main__":
    main()
