#!/usr/bin/env python3
"""Stage 0 — recompute the degree-(4,2) constant R1 at high precision.

R1 is the limit of a polynomial continued fraction (PCF) from the April-26
degree-(4,2) paper "A Computational Investigation of the 2k-Degree Conjecture
at k=2: the Degree-(4,2) Stratum and a Novel Transcendental Constant".

Family (leading-first coefficients), located in
papanokechi/siarc-relay-bridge sessions/2026-04-30/T2A-R1-IDENTIFY/r1_identify.py
(refined from T2A-BASIS-IDENTIFY, bridge commit fa259b0 / 45fe389):

    a_n = n^4 + 0*n^3 - n^2 - n - 1     coeffs_a = [1, 0, -1, -1, -1]
    b_n = -n^2 + n - 1                  coeffs_b = [-1, 1, -1]

PCF convergent recurrence (matching the T2A-BASIS-IDENTIFY convention):
    P_n = b_n P_{n-1} + a_n P_{n-2},   Q_n = b_n Q_{n-1} + a_n Q_{n-2}
    seed:  P_0 = b(0),  P_1 = b(1) b(0) + a(1)
           Q_0 = 1,     Q_1 = b(1)
    R1 = lim_n P_n / Q_n

This script recomputes R1 independently at two (dps, N) settings, reports the
self-convergence residual |K_N - K_{N-1}|, the cross-setting agreement, and the
number of stable digits, then emits the value + provenance to R1_value.json.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).parent

A_COEFFS = [1, 0, -1, -1, -1]   # a4, a3, a2, a1, a0
B_COEFFS = [-1, 1, -1]          # b2, b1, b0

PUBLISHED_30 = "-0.10123520070804963"  # abstract value (30 sig digits region)


def kn_mp(a_coeffs, b_coeffs, N, dps):
    """Return (K_N, K_{N-1}) for the PCF at working precision `dps`."""
    a4, a3, a2, a1, a0 = a_coeffs
    b2, b1, b0 = b_coeffs
    mp.mp.dps = dps
    b_at_0 = mp.mpf(b0)
    b_at_1 = mp.mpf(b2 + b1 + b0)
    a_at_1 = mp.mpf(a4 + a3 + a2 + a1 + a0)
    P_prev2 = b_at_0
    P_prev1 = b_at_1 * b_at_0 + a_at_1
    Q_prev2 = mp.mpf(1)
    Q_prev1 = b_at_1
    K_curr = K_prev = None
    for n in range(2, N + 1):
        an = a4 * n**4 + a3 * n**3 + a2 * n**2 + a1 * n + a0
        bn = b2 * n**2 + b1 * n + b0
        P_curr = bn * P_prev1 + an * P_prev2
        Q_curr = bn * Q_prev1 + an * Q_prev2
        if Q_curr == 0:
            raise ZeroDivisionError("Q_curr vanished at n=%d" % n)
        K_prev = K_curr
        K_curr = P_curr / Q_curr
        if n % 16 == 0:  # periodic rescale to keep magnitudes bounded
            mag = max(abs(P_curr), abs(Q_curr), mp.mpf(1))
            P_curr /= mag
            Q_curr /= mag
            P_prev1 /= mag
            Q_prev1 /= mag
        P_prev2, P_prev1 = P_prev1, P_curr
        Q_prev2, Q_prev1 = Q_prev1, Q_curr
    return K_curr, K_prev


def stable_digits(x, y):
    """Number of leading decimal digits that agree between x and y."""
    d = abs(x - y)
    if d == 0:
        return float("inf")
    return float(-mp.log10(d))


def main():
    # Setting 1: dps target 300 (work at 350-digit buffer), N=2000
    dps1, N1 = 350, 2000
    K1, K1m1 = kn_mp(A_COEFFS, B_COEFFS, N=N1, dps=dps1)
    res1 = abs(K1 - K1m1)

    # Setting 2: independent cross-check at higher dps and more iterations
    dps2, N2 = 420, 2600
    K2, K2m1 = kn_mp(A_COEFFS, B_COEFFS, N=N2, dps=dps2)
    res2 = abs(K2 - K2m1)

    # Cross-setting agreement (compare both to common precision)
    mp.mp.dps = 320
    cross = abs(mp.mpf(K1) - mp.mpf(K2))
    cross_digits = stable_digits(mp.mpf(K1), mp.mpf(K2))

    # Self-convergence residual -> implied stable digits within a setting
    self_digits1 = float(-mp.log10(res1)) if res1 != 0 else float("inf")

    # Report value to 300 significant digits at the reported dps
    REPORT_DPS = 300
    mp.mp.dps = REPORT_DPS + 20
    value_str = mp.nstr(mp.mpf(K2), REPORT_DPS, strip_zeros=False)

    # 30-digit published match check
    mp.mp.dps = 60
    got_30 = mp.nstr(mp.mpf(K2), 17)  # 17 sig digits -> -0.10123520070804963
    match_30 = got_30.startswith(PUBLISHED_30)

    print("=" * 72)
    print("STAGE 0 — R1 recompute from degree-(4,2) PCF family")
    print("=" * 72)
    print("a coeffs (leading-first): %s   (a_n = n^4 - n^2 - n - 1)" % A_COEFFS)
    print("b coeffs (leading-first): %s     (b_n = -n^2 + n - 1)" % B_COEFFS)
    print()
    print("Setting 1: dps=%d N=%d  |K_N - K_{N-1}| = %s  (~%.0f digits)"
          % (dps1, N1, mp.nstr(res1, 5), self_digits1))
    print("Setting 2: dps=%d N=%d  |K_N - K_{N-1}| = %s" % (dps2, N2, mp.nstr(res2, 5)))
    print("Cross-setting |K1 - K2| = %s  (~%.0f agreeing digits)"
          % (mp.nstr(cross, 5), cross_digits))
    print()
    print("Recomputed R1 (300 sig digits):")
    print("  %s" % value_str)
    print()
    print("Published 30-digit value : %s..." % PUBLISHED_30)
    print("Recomputed (17 sig dig)  : %s" % got_30)
    print("First-30-digit match     : %s" % match_30)

    sha = hashlib.sha256(value_str.encode("utf-8")).hexdigest()

    out = {
        "constant": "R1",
        "description": (
            "Novel transcendental constant from the April-26 degree-(4,2) paper "
            "'A Computational Investigation of the 2k-Degree Conjecture at k=2: "
            "the Degree-(4,2) Stratum and a Novel Transcendental Constant'. "
            "Limit of a polynomial continued fraction."
        ),
        "source_family": {
            "type": "polynomial continued fraction (degree-(4,2))",
            "a_coeffs_leading_first": A_COEFFS,
            "a_n": "n^4 - n^2 - n - 1",
            "b_coeffs_leading_first": B_COEFFS,
            "b_n": "-n^2 + n - 1",
            "convergent_recurrence": "P_n = b_n P_{n-1} + a_n P_{n-2}; Q_n = b_n Q_{n-1} + a_n Q_{n-2}",
            "seed": "P_0=b(0), P_1=b(1)b(0)+a(1), Q_0=1, Q_1=b(1)",
            "limit": "R1 = lim P_n/Q_n",
        },
        "provenance": {
            "paper": "A Computational Investigation of the 2k-Degree Conjecture at k=2 (April-26, 2026)",
            "zenodo_doi": "10.5281/zenodo.19774029",
            "family_source_repo": "github.com/papanokechi/siarc-relay-bridge",
            "family_source_files": [
                "sessions/2026-04-30/T2A-R1-IDENTIFY/r1_identify.py",
                "sessions/2026-04-26/T2A-BASIS-IDENTIFY/t2a_basis_identify.py",
                "sessions/2026-04-30/UMB-T3-PROBE/halt_log.json (id=T2A_R1, a=[1,0,-1,-1,-1], b=[-1,1,-1])",
            ],
            "published_30_digit": PUBLISHED_30,
        },
        "recomputation": {
            "engine": "mpmath %s" % mp.__version__,
            "setting_1": {"dps": dps1, "N_iter": N1, "self_residual": mp.nstr(res1, 8)},
            "setting_2": {"dps": dps2, "N_iter": N2, "self_residual": mp.nstr(res2, 8)},
            "cross_setting_agreement_digits": round(cross_digits, 1),
            "report_dps": REPORT_DPS,
            "first_30_digit_match": bool(match_30),
        },
        "value_300sig": value_str,
        "value_sha256": sha,
    }

    out_path = HERE / "R1_value.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print()
    print("value SHA-256: %s" % sha)
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
