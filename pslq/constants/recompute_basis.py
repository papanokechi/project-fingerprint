#!/usr/bin/env python3
"""BASIS RE-VERIFICATION — recompute every basis constant FROM ITS DEFINITION.

Never transcribes a deposited decimal as ground truth. Each value is recomputed
from first principles (standard constants) or from the defining PCF family /
formula / recurrence (project constants), then DIFFed against the deposited
value to assign a status. Emits pslq/constants/basis_canonical.json.

No network. No commit. Recompute-only.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).parent


# ──────────────────────────────────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────────────────────────────────
def stable_digits(x, y):
    """Leading decimal digits that agree between x and y."""
    with mp.workdps(max(mp.mp.dps, 60)):
        d = abs(mp.mpf(x) - mp.mpf(y))
        if d == 0:
            return float("inf")
        return float(-mp.log10(d))


def value_str(x, sig, dps):
    with mp.workdps(dps + 25):
        return mp.nstr(mp.mpf(x), sig, strip_zeros=False)


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def diff_status(recomputed, deposited_latest, tol_digits=25):
    """Compare recompute to the latest deposited value string."""
    with mp.workdps(80):
        a = mp.mpf(recomputed)
        b = mp.mpf(deposited_latest)
        agree = stable_digits(a, b)
    return agree


# ──────────────────────────────────────────────────────────────────────────
# STANDARD CONSTANTS  (mpmath first principles)
# ──────────────────────────────────────────────────────────────────────────
def recompute_standard():
    """Recompute the 7 standard constants at two precisions; report stability."""
    defs = {
        "pi": ("4*atan(1)  (mpmath mp.pi)", lambda: +mp.pi),
        "e": ("exp(1)  (mpmath mp.e)", lambda: +mp.e),
        "log2": ("natural log of 2  (mp.log(2))", lambda: mp.log(2)),
        "gamma": ("Euler-Mascheroni  (mp.euler)", lambda: +mp.euler),
        "zeta3": ("Apery zeta(3)  (mp.zeta(3))", lambda: mp.zeta(3)),
        "catalan": ("Catalan G  (mp.catalan)", lambda: +mp.catalan),
        "zeta2": ("zeta(2)=pi^2/6  (mp.zeta(2))", lambda: mp.zeta(2)),
    }
    out = {}
    REPORT_SIG = 250
    for name, (desc, fn) in defs.items():
        mp.mp.dps = 320
        v_hi = fn()
        mp.mp.dps = 270
        v_lo = fn()
        sd = stable_digits(v_hi, v_lo)
        mp.mp.dps = 320
        vs = value_str(v_hi, REPORT_SIG, 320)
        out[name] = {
            "definition": desc,
            "value": vs,
            "report_sig": REPORT_SIG,
            "dps": 320,
            "stable_digits_cross_dps": (None if sd == float("inf") else round(sd, 1)),
            "sha256": sha256_str(vs),
        }
    return out


# ──────────────────────────────────────────────────────────────────────────
# R1  — degree-(4,2) PCF family
#   a_n = n^4 - n^2 - n - 1 ,  b_n = -n^2 + n - 1
#   P_n = b_n P_{n-1} + a_n P_{n-2};  Q analogous;  R1 = lim P_n/Q_n
# ──────────────────────────────────────────────────────────────────────────
R1_A = [1, 0, -1, -1, -1]   # n^4, n^3, n^2, n^1, n^0
R1_B = [-1, 1, -1]          # n^2, n^1, n^0
R1_DEPOSITED = "-0.10123520070804963"   # April-26 abstract (latest)


def _r1_kn(N, dps):
    a4, a3, a2, a1, a0 = R1_A
    b2, b1, b0 = R1_B
    mp.mp.dps = dps
    P2 = mp.mpf(b0)
    P1 = mp.mpf(b2 + b1 + b0) * mp.mpf(b0) + mp.mpf(a4 + a3 + a2 + a1 + a0)
    Q2 = mp.mpf(1)
    Q1 = mp.mpf(b2 + b1 + b0)
    K = Kp = None
    for n in range(2, N + 1):
        an = a4 * n**4 + a3 * n**3 + a2 * n**2 + a1 * n + a0
        bn = b2 * n**2 + b1 * n + b0
        Pc = bn * P1 + an * P2
        Qc = bn * Q1 + an * Q2
        Kp, K = K, Pc / Qc
        if n % 16 == 0:
            m = max(abs(Pc), abs(Qc), mp.mpf(1))
            Pc /= m; Qc /= m; P1 /= m; Q1 /= m
        P2, P1 = P1, Pc
        Q2, Q1 = Q1, Qc
    return K, Kp


def recompute_R1():
    K1, K1m = _r1_kn(N=2000, dps=350)
    res1 = abs(K1 - K1m)
    K2, K2m = _r1_kn(N=2600, dps=420)
    cross = stable_digits(K1, K2)
    REPORT_SIG = 250
    vs = value_str(K2, REPORT_SIG, 420)
    agree = diff_status(K2, R1_DEPOSITED)
    return {
        "value": vs,
        "report_sig": REPORT_SIG,
        "dps": 420,
        "self_residual_setting1": mp.nstr(res1, 6),
        "cross_setting_digits": (None if cross == float("inf") else round(cross, 1)),
        "deposited_latest": R1_DEPOSITED,
        "agree_with_deposited_digits": round(agree, 1),
        "sha256": sha256_str(vs),
    }


# ──────────────────────────────────────────────────────────────────────────
# V_quad — quadratic PCF:  Vq = 1 + K_{n>=1} 1/(3n^2+n+1)
# ──────────────────────────────────────────────────────────────────────────
VQ_DEPOSITED = "1.19737399068835760244"   # Painleve paper eq:vquad-def (latest)


def _vquad(depth, dps):
    with mp.workdps(dps + 60):
        v = mp.mpf(0)
        for n in range(depth, 0, -1):
            v = mp.mpf(1) / (3 * n * n + n + 1 + v)
        return +(mp.mpf(1) + v)


def recompute_vquad():
    v1 = _vquad(depth=4000, dps=320)
    v2 = _vquad(depth=6000, dps=320)
    cross = stable_digits(v1, v2)
    REPORT_SIG = 250
    vs = value_str(v2, REPORT_SIG, 320)
    agree = diff_status(v2, VQ_DEPOSITED)
    return {
        "value": vs,
        "report_sig": REPORT_SIG,
        "dps": 320,
        "self_convergence_digits_depth4000_vs_6000": (
            None if cross == float("inf") else round(cross, 1)),
        "deposited_latest": VQ_DEPOSITED,
        "agree_with_deposited_digits": round(agree, 1),
        "sha256": sha256_str(vs),
    }


# ──────────────────────────────────────────────────────────────────────────
# S  — V_quad Stokes constant via Dingle late-term formula.
#   Definition-encoding (a_n) taken from pcf-research vquad/scripts
#   (wkb_riccati_coeffs / formal_series_coeffs), then Dingle late-term:
#     S_n = a_n * Gamma(beta) * xi0^{n+beta} / ((-1)^n * Gamma(n+beta)) -> S
#   beta = -1/(3 sqrt 3),  xi0 = 2/sqrt 3.
#   This recompute exists to confirm WHAT the documented Dingle definition
#   actually yields (NOT to bless any transcribed decimal).
# ──────────────────────────────────────────────────────────────────────────
# v1.0 (retracted): prefactor Gamma(beta_exp) ~ -6.00599  -> S ~ 0.43770528
# v1.1 (corrected): prefactor 2*pi          ~  6.28319  -> S ~ 0.45790662
S_V10_RETRACTED = "0.43770528073458"            # repo scripts / v1.0 deposits (Gamma prefactor)
S_V11_CORRECTED = "0.45790662316901763611"      # Painleve-V paper v1.1 (2*pi prefactor)


def _wkb_riccati_coeffs(sigma, order):
    c = [mp.mpf(0)] * (order + 1)
    c[0] = sigma
    c[1] = -1 - sigma / 6
    d = [mp.mpf(0)] * (order + 1)
    d[0] = c[0] ** 2
    d[1] = 2 * c[0] * c[1]
    for k in range(2, order + 1):
        known_s = mp.fsum(c[i] * c[k - i] for i in range(1, k))
        rest = (3 * (known_s - (k - 1) * c[k - 1])
                + d[k - 1] + d[k - 2] + 6 * c[k - 1] + c[k - 2])
        c[k] = -rest / (6 * c[0])
        d[k] = 2 * c[0] * c[k] + known_s - (k - 1) * c[k - 1]
    return c


def _formal_series_coeffs(order, dps):
    mp.mp.dps = dps
    sigma_rec = -1 / mp.sqrt(mp.mpf(3))
    rc = _wkb_riccati_coeffs(sigma_rec, order=order + 10)
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


def _neville_to_zero(xs, ys):
    """Neville polynomial extrapolation of (xs, ys) to x = 0 (h -> 0)."""
    m = len(xs)
    T = [list(ys)]
    for k in range(1, m):
        row = []
        for i in range(m - k):
            num = (0 - xs[i + k]) * T[k - 1][i] - (0 - xs[i]) * T[k - 1][i + 1]
            row.append(num / (xs[i] - xs[i + k]))
        T.append(row)
    return T[m - 1][0]


def _stokes_amplitude_K(order, dps):
    """Prefactor-STRIPPED Dingle late-term amplitude
        K = lim_n | a_n * xi0^(n+beta) / ((-1)^n * Gamma(n+beta)) |
    The full Stokes constant is S = prefactor * K. Returns (K, window_spread).
    """
    mp.mp.dps = dps
    beta = -1 / (3 * mp.sqrt(mp.mpf(3)))
    xi0 = 2 / mp.sqrt(mp.mpf(3))
    a = _formal_series_coeffs(order, dps)
    ns = list(range(order - 400, order + 1))
    Kn = [abs(a[n] * xi0 ** (n + beta) / (((-1) ** n) * mp.gamma(n + beta)))
          for n in ns]
    Kvals = []
    for w in (16, 22, 28, 34):
        idx = list(range(len(ns) - w, len(ns)))
        xs = [mp.mpf(1) / ns[i] for i in idx]
        ys = [Kn[i] for i in idx]
        Kvals.append(_neville_to_zero(xs, ys))
    K = Kvals[-1]
    spread = max(abs(v - K) for v in Kvals)
    return K, spread


def recompute_S():
    """Recompute S from the Dingle late-term DEFINITION with the prefactor made
    EXPLICIT. The repo scripts (pcf-research) use prefactor Gamma(beta_exp); the
    Painleve-V v1.1 correction replaces this by the universal 2*pi. We compute the
    prefactor-stripped amplitude K once (from definition) and report S under BOTH
    conventions so the discrepancy is mechanically attributed to the prefactor.
    """
    DPS = 240
    ORDER = 1800
    beta = -1 / (3 * mp.sqrt(mp.mpf(3)))
    # Cross-check K at two (order, dps) settings for a stable-digit estimate.
    K1, spread1 = _stokes_amplitude_K(order=1400, dps=200)
    K2, spread2 = _stokes_amplitude_K(order=ORDER, dps=DPS)
    cross = stable_digits(K1, K2)

    gamma_pref = mp.gamma(beta)          # v1.0 (retracted) prefactor
    two_pi = 2 * mp.pi                   # v1.1 (corrected) prefactor

    S_gamma = K2 * abs(gamma_pref)       # convention (a): Gamma(beta_exp)
    S_2pi = K2 * two_pi                  # convention (b): 2*pi

    agree_gamma_v10 = stable_digits(S_gamma, S_V10_RETRACTED)
    agree_2pi_v11 = stable_digits(S_2pi, S_V11_CORRECTED)

    # canonical value (convention b), reported well beyond the deposited precision
    canonical_sig = 40
    S_2pi_str = value_str(S_2pi, canonical_sig, DPS)
    digits_stable = int(min(cross, float(-mp.log10(spread2))))

    return {
        "recompute_method": (
            "prefactor-explicit Dingle late-term on Riccati a_n; "
            "S = prefactor * K, K = lim|a_n*xi0^(n+beta)/((-1)^n*Gamma(n+beta))|"),
        "dps": DPS,
        "series_order": ORDER,
        "amplitude_K": mp.nstr(K2, 30),
        "K_cross_setting_digits": (None if cross == float("inf") else round(cross, 1)),
        "K_window_spread": mp.nstr(spread2, 3),
        "beta_exp": mp.nstr(beta, 20),
        "prefactor_gamma_beta": mp.nstr(gamma_pref, 18),
        "prefactor_2pi": mp.nstr(two_pi, 18),
        "S_conv_a_gamma_prefactor": mp.nstr(S_gamma, 20),
        "S_conv_b_2pi_prefactor": S_2pi_str,
        "agree_conv_a_with_v10_retracted_digits": round(agree_gamma_v10, 1),
        "agree_conv_b_with_v11_corrected_digits": round(agree_2pi_v11, 1),
        "canonical_value_conv_b": S_2pi_str,
        "canonical_digits_stable": digits_stable,
        "v10_retracted": S_V10_RETRACTED,
        "v11_corrected": S_V11_CORRECTED,
    }


def main():
    print("=" * 74)
    print("BASIS RE-VERIFICATION — recompute-from-definition")
    print("=" * 74)

    std = recompute_standard()
    print("[std] recomputed 7 standard constants")
    r1 = recompute_R1()
    print("[R1] agree_with_deposited_digits =", r1["agree_with_deposited_digits"])
    vq = recompute_vquad()
    print("[V_quad] agree_with_deposited_digits =", vq["agree_with_deposited_digits"])
    s = recompute_S()
    print("[S] amplitude K =", s["amplitude_K"][:22], "(cross", s["K_cross_setting_digits"], "dig)")
    print("[S] (a) Gamma-prefactor ->", s["S_conv_a_gamma_prefactor"],
          "| agree v1.0-retracted:", s["agree_conv_a_with_v10_retracted_digits"])
    print("[S] (b) 2*pi-prefactor  ->", s["S_conv_b_2pi_prefactor"],
          "| agree v1.1-corrected:", s["agree_conv_b_with_v11_corrected_digits"])

    bundle = {"standard": std, "R1": r1, "V_quad": vq, "S": s,
              "generated_utc": datetime.now(timezone.utc).isoformat()}
    (HERE / "_basis_recompute_raw.json").write_text(
        json.dumps(bundle, indent=2), encoding="utf-8")
    print("\nwrote _basis_recompute_raw.json")


if __name__ == "__main__":
    main()
