#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-0  --  ARITHMETIC-GEVREY LOCATION (the technology map)
================================================================================
SIARC. Tests REGISTERED PREDICTION P3: no renormalization
    f_{k,m}(x) = sum_n Q_n * n!^{-k} * (2n)!^{-m} * x^n
is an E-function or a G-function (Andre's arithmetic-Gevrey orders -1 and 0).

Method (EXACT integer/rational arithmetic):
  Q_n = (3n^2+n+1) Q_{n-1} + Q_{n-2},  Q_0=1, Q_1=5.
  For each (k,m) on a declared grid:
    * G-reading coefficients  c_n = Q_n / (n!^k (2n)!^m)
    * E-reading coefficients  a_n = n! * c_n   (E-function f = sum a_n x^n/n!)
  A power series sum b_n x^n is a G-function only if BOTH
    (i)  archimedean house |b_n| <= C^n  (geometric), and
    (ii) den(b_0..b_n) <= C^n            (geometric denominators).
  E-function: same two conditions on a_n.
  Factorial growth is detected by  r(n) = log10(.) / (n*log10 n) -> positive
  constant (since log n! ~ n log n); geometric/sub-factorial => r(n) -> 0.

Early-HALT gate: if ANY (k,m) reads as an E-function, Siegel-Shidlovskii opens
an unconditional front -> the op redesigns. Expected: P3 holds (no E, no G).

Locator (VERIFIED-by-citation): Y. Andre, "Series Gevrey de type arithmetique
I/II", Annals of Mathematics 151 (2000) 705-740 / 741-756: E-functions =
arithmetic-Gevrey order -1, G-functions = order 0; both require geometric house
AND geometric denominators of the coefficient sequence.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import hashlib
from fractions import Fraction
from math import log10, lgamma, log
import mpmath as mp

mp.mp.dps = 40

N_GRID = 500          # grid depth (signature unambiguous well before this)
N_BIG = 1200          # depth for the (k,m)=(0,1) tie-in to cc2-0's (2N)! result
K_VALS = [0, 1, 2, 3]
M_VALS = [0, 1, 2]
FACT_THRESHOLD = 0.10   # r(N) above this => factorial; below => geometric/sub


def log10_big(x):
    """log10 of a positive Python int or Fraction, via mpmath (exact-ish)."""
    if isinstance(x, Fraction):
        return float(mp.log10(mp.mpf(x.numerator)) - mp.log10(mp.mpf(x.denominator)))
    return float(mp.log10(mp.mpf(x)))


def build_Q(N):
    Q = [1, 5]
    while len(Q) <= N:
        n = len(Q)
        Q.append((3 * n * n + n + 1) * Q[n - 1] + Q[n - 2])
    return Q


def classify(rN):
    return "factorial" if rN > FACT_THRESHOLD else "geometric/sub"


def main():
    print("== op:cc3-0  arithmetic-Gevrey location (P3 gate) ==")
    Q = build_Q(N_GRID)

    # precompute factorials as ints
    fact = [1] * (2 * N_GRID + 1)
    for i in range(1, 2 * N_GRID + 1):
        fact[i] = fact[i - 1] * i

    grid = {}
    any_E = False
    any_G = False
    for k in K_VALS:
        for m in M_VALS:
            # measure r(n) = log10|.|/(n log10 n) at a few large n for both readings
            ns = [N_GRID // 2, (3 * N_GRID) // 4, N_GRID]
            # archimedean + denominator growth, per reading, at n=N_GRID
            n = N_GRID
            den_nk = fact[n] ** k
            den_2nm = fact[2 * n] ** m
            c_n = Fraction(Q[n], den_nk * den_2nm)
            a_n = c_n * fact[n]            # E-reading coefficient
            denom_c = c_n.denominator
            denom_a = a_n.denominator
            absc = abs(c_n)
            absa = abs(a_n)
            nl = n * log10(n)
            # guard zero
            r_house_G = log10_big(absc) / nl if absc != 0 else -9.99
            r_den_G = (log10_big(denom_c) / nl) if denom_c > 1 else 0.0
            r_house_E = log10_big(absa) / nl if absa != 0 else -9.99
            r_den_E = (log10_big(denom_a) / nl) if denom_a > 1 else 0.0

            house_G = classify(r_house_G)
            den_G = classify(r_den_G)
            house_E = classify(r_house_E)
            den_E = classify(r_den_E)

            is_G = (house_G == "geometric/sub" and den_G == "geometric/sub")
            is_E = (house_E == "geometric/sub" and den_E == "geometric/sub")
            any_E = any_E or is_E
            any_G = any_G or is_G

            grid[f"k{k}_m{m}"] = {
                "k": k, "m": m,
                "G_reading": {
                    "r_house": round(r_house_G, 4), "house": house_G,
                    "r_den": round(r_den_G, 4), "den": den_G,
                    "is_G_function": is_G,
                },
                "E_reading": {
                    "r_house": round(r_house_E, 4), "house": house_E,
                    "r_den": round(r_den_E, 4), "den": den_E,
                    "is_E_function": is_E,
                },
                "predicted_r_house_G": 2 - k - 2 * m,   # asymptotic theory
                "predicted_r_den_G": k + 2 * m,
            }
            print(f"  (k={k},m={m})  G:[house {r_house_G:+.3f}->{house_G}, den {r_den_G:+.3f}->{den_G}] "
                  f"E:[house {r_house_E:+.3f}->{house_E}, den {r_den_E:+.3f}->{den_E}]  "
                  f"isG={is_G} isE={is_E}")

    # --- (0,1) tie-in to cc2-0: lcm den(Q_n/(2n)!) ~ (2N)! ? ---
    print("\n  [(0,1) tie-in] running lcm den(Q_n/(2n)!) vs (2N)! ...")
    Qb = build_Q(N_BIG)
    import math
    lcm = 1
    factb = [1] * (2 * N_BIG + 1)
    for i in range(1, 2 * N_BIG + 1):
        factb[i] = factb[i - 1] * i
    tie = {}
    checkpoints = {250, 500, 1000, N_BIG}
    for n in range(N_BIG + 1):
        d = Fraction(Qb[n], factb[2 * n]).denominator
        lcm = lcm // math.gcd(lcm, d) * d
        if n in checkpoints:
            ratio = log10_big(lcm) / log10_big(factb[2 * n])
            tie[str(n)] = {"log10_lcm": round(log10_big(lcm), 2),
                           "log10_(2N)!": round(log10_big(factb[2 * n]), 2),
                           "ratio": round(ratio, 5)}
            print(f"    N={n}: log10 lcm={log10_big(lcm):.2f}, "
                  f"log10 (2N)!={log10_big(factb[2*n]):.2f}, ratio={ratio:.5f}")

    p3_holds = (not any_E) and (not any_G)
    verdict = "P3_HOLDS_no_E_no_G" if p3_holds else (
        "E_FUNCTION_FOUND_HALT" if any_E else "G_FUNCTION_FOUND")

    print(f"\n  any E-function on grid: {any_E}")
    print(f"  any G-function on grid: {any_G}")
    print(f"  VERDICT: {verdict}")

    obj = {
        "op": "cc3-0",
        "task_id": "op:cc-transcendence/cc3-0",
        "title": "Arithmetic-Gevrey location of the EBR d=2 family (P3 gate)",
        "family": "Q_n=(3n^2+n+1)Q_{n-1}+Q_{n-2}, Q_0=1, Q_1=5; renorm grid c_n=Q_n n!^{-k}(2n)!^{-m}",
        "grid_k": K_VALS, "grid_m": M_VALS, "N_grid": N_GRID,
        "fact_threshold": FACT_THRESHOLD,
        "grid": grid,
        "tie_in_0_1_lcm_vs_2Nfact": tie,
        "any_E_function": bool(any_E),
        "any_G_function": bool(any_G),
        "P3_verdict": verdict,
        "P3_holds": bool(p3_holds),
        "early_halt_triggered": bool(any_E),
        "hand_proof_sketch": (
            "Q_n ~ (C_EBR/sqrt(pi)) 3^n (n!)^2 n^{1/3} (factorial-squared house) and Q_n is "
            "ODD with asymptotically vanishing share of the prime content of (2n)! (cc2-0: "
            "lcm den(Q_n/(2n)!) ~ (2N)!, log-ratio ~1.0000). G-reading c_n=Q_n/(n!^k(2n)!^m): "
            "archimedean house ~ (n!)^{2-k-2m} (geometric iff k+2m>=2) while denominators ~ "
            "n!^k(2n)!^m are geometric iff (k,m)=(0,0); the two regions are disjoint, so NO (k,m) "
            "is a G-function. E-reading a_n=n! c_n: house ~ (n!)^{3-k-2m} (geometric iff k+2m>=3) "
            "while denominators are geometric iff m=0 and k<=1; disjoint, so NO (k,m) is an "
            "E-function. Hence the two unconditional transcendence machines (Siegel-Shidlovskii "
            "for E; Andre-Chudnovsky for G) are inapplicable at every grid point."),
        "locator": ("Y. Andre, Series Gevrey de type arithmetique I & II, Ann. of Math. 151 "
                    "(2000), 705-740 & 741-756 (E=order -1, G=order 0; geometric house+denominator)."),
        "grade": ("STRUCTURAL (hand proof: house/denominator tension) + VERIFIED (exact grid "
                  "data, N<=%d; (0,1) lcm tie-in to N=%d)." % (N_GRID, N_BIG)),
        "discipline_line": (
            "A large G_Gal does NOT imply C transcendental; an exponential-period classification "
            "does NOT imply C transcendental; only a named-conjecture conditional (or out-of-scope "
            "new technology) does. Unconditional transcendence of C is not a deliverable of op:cc-3."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_0_gevrey_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_0_gevrey_results.json")


if __name__ == "__main__":
    main()
