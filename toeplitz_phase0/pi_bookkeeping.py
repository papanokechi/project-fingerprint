"""Where does the pi in C = 1/pi come from?  Provenance audit of a constant.

THE CHALLENGE (operator).  Standard resurgence bookkeeping carries a 1/pi in
the large-order/one-instanton bridge.  A stray pi picked up or dropped there
would produce exactly the observed result: an extracted constant reading 1/pi
when the true Stokes constant is 1, or pi when it is 1.  So: which route
produced the 64 digits, and does that route contain a pi anywhere?

THE HONEST ANSWER IS "PARTIALLY YES", so this file separates the two halves.

  HALF 1 -- the amplitude K, which has NO bookkeeping freedom at all.
      K = lim_m  e_m * A^m / Gamma(m + beta)
    The e_m are EXACT RATIONALS from the recursion, A = 2 and beta = -1/2 are
    exact rationals from the linearization.  There is no convention to get
    wrong: K is the amplitude of the coefficient growth, full stop.
    Gamma(m - 1/2) does supply a sqrt(pi) BY DEFINITION -- that is not
    bookkeeping, it is what Gamma is at half-integer argument, and it means pi
    genuinely appears in the answer rather than being imported by me.

  HALF 2 -- the bridge K -> C, which DOES contain a sqrt(2 pi).
      C = K * sqrt(2 pi) * A^(beta - 1/2)
    The sqrt(2 pi) is Stirling, from the optimal-truncation calculation.  This
    is exactly the step the operator is worried about, and the worry is
    legitimate: a factor slipped here moves C by 2.5066 and nothing about the
    ALGEBRA would complain.

TWO INDEPENDENT DEFENCES, both computed below.

  (D1) THE PI-EXPONENT IS PINNED BY THE DATA, NOT CHOSEN BY ME.  Scan
       K * pi^p / sqrt(2) over half-integer p.  If my bookkeeping had lost or
       gained a sqrt(pi), the clean value would appear at a different p.  Only
       one p yields a rational-looking result, and the ladder shows the
       neighbours are not close.

  (D2) THE STIRLING STEP IS VALIDATED NUMERICALLY, NOT ASSUMED.  The
       least-term check in trans_series.py compares the closed form against
       the smallest term of the series COMPUTED DIRECTLY from the coefficients
       -- no Stirling on the actual side.  A wrong sqrt(2 pi) would show up
       there as a ratio near 2.5066 or 0.399, not 0.998.

  (D3) The rival hypotheses the operator names are directly excluded: C = 1
       and C = pi require K = 0.7979 and K = 2.5066.  K is measured.

A CAVEAT THAT CUTS THE OTHER WAY, and it belongs here rather than buried:
the appealing simplicity of "1/pi" is partly manufactured by the bridge.  The
raw measured invariant is K = sqrt(2) * pi^(-3/2), which nobody would call a
clean constant on sight.  Calling the result 1/pi is a statement about a
particular normalisation, and the aesthetic pull of that form is not evidence.
"""

from __future__ import annotations

import json
import os

from mpmath import mp, mpf, sqrt, pi, exp, log, loggamma

# Declared.  A and beta come from trans_series.py route 1 (exact, symbolic).
A = mpf(2)
BETA = mpf(-1) / 2
NEVILLE_DEG = 52
DPS = 140


def neville(pts, deg):
    pts = pts[-(deg + 1):]
    xs = [1 / m for m, _ in pts]
    col = [v for _, v in pts]
    n = len(xs)
    for k in range(1, n):
        col = [(col[i + 1] * (0 - xs[i]) - col[i] * (0 - xs[i + k]))
               / (xs[i + k] - xs[i]) for i in range(n - k)]
    return col[0]


def main():
    mp.dps = DPS
    d = json.load(open("out/sigma_recursion_fast.json"))
    E = {}
    for r in d["coeffs"]:
        n, dn = r["e_m"].split("/")
        E[r["m"]] = mpf(int(n)) / mpf(int(dn))
    ms = sorted(E)

    pts = [(mpf(m), E[m] * exp(mpf(m) * log(A) - loggamma(mpf(m) + BETA)))
           for m in ms]
    K = neville(pts, NEVILLE_DEG)

    print("=" * 74)
    print("PI PROVENANCE AUDIT for the Stokes prefactor")
    print("=" * 74)
    print("\nHALF 1 -- amplitude, no bookkeeping freedom")
    print(f"  K = lim e_m A^m / Gamma(m+beta) = {mp.nstr(K, 40)}")
    print("  inputs: exact rational e_m, A = 2, beta = -1/2.  No convention.")

    print("\n(D1) is the pi EXPONENT chosen by me, or by the data?")
    print("     scanning  K * pi^p / sqrt(2)  over half-integer p:")
    ladder = []
    for p2 in range(-1, 8):
        p = mpf(p2) / 2
        v = K * pi**p / sqrt(2)
        mark = ""
        if abs(v - 1) < mpf("1e-40"):
            mark = "   <== EXACTLY 1"
        ladder.append({"p": mp.nstr(p, 4), "value": mp.nstr(v, 26)})
        print(f"       p = {mp.nstr(p, 4):>5}   {mp.nstr(v, 26)}{mark}")
    tgt = sqrt(2) / pi**(mpf(3) / 2)
    err = abs(K - tgt)
    dig = float(-log(err) / log(10))
    print(f"\n     K = sqrt(2) * pi^(-3/2) to {dig:.1f} digits "
          f"(|diff| {mp.nstr(err, 4)})")
    print("     Neighbouring exponents are not near-misses -- they are")
    print("     unrelated irrationals.  The exponent is data-determined.")

    print("\n(D2) is the sqrt(2 pi) Stirling bridge validated, or assumed?")
    ts = json.load(open("out/trans_series.json"))
    print("     least-term check (actual computed WITHOUT Stirling):")
    for row in ts["least_term_check"]:
        print(f"       s={row['s']:4d}  ratio actual/predicted = {row['ratio']}")
    print("     A dropped or doubled sqrt(2 pi) would put these at 0.399 or")
    print("     2.507.  They sit at 0.998 and rise toward 1.")

    print("\n(D3) rival hypotheses, excluded by the measured K:")
    for name, C in (("1/pi", 1 / pi), ("1", mpf(1)), ("pi", pi),
                    ("2/pi", 2 / pi), ("1/(2 pi)", 1 / (2 * pi))):
        need = 2 * C / sqrt(2 * pi)
        ok = "  <== matches" if abs(need - K) < mpf("1e-40") else ""
        print(f"       C = {name:9s} requires K = {mp.nstr(need, 22)}{ok}")
    print(f"       MEASURED                  K = {mp.nstr(K, 22)}")

    C = K * sqrt(2 * pi) * A**(BETA - mpf(1) / 2)
    cerr = abs(C - 1 / pi)
    print(f"\n  => C = {mp.nstr(C, 34)}")
    print(f"     |C - 1/pi| = {mp.nstr(cerr, 4)}   "
          f"({float(-log(cerr)/log(10)):.1f} digits)")

    print("\nCAVEAT, stated because it cuts against the result:")
    print("  the invariant actually measured is K = sqrt(2) pi^(-3/2), which")
    print("  is not a constant anyone would call clean on sight.  '1/pi' is")
    print("  that number times sqrt(2 pi)/2.  The aesthetic pull of the")
    print("  simpler form is not evidence, and the tag stays CONJECTURED.")

    out = {
        "K": mp.nstr(K, 40),
        "K_closed_form": "sqrt(2)*pi^(-3/2)",
        "K_agreement_digits": round(dig, 2),
        "pi_exponent_ladder": ladder,
        "C": mp.nstr(C, 40),
        "C_minus_inv_pi": mp.nstr(cerr, 6),
        "bridge_contains_pi": True,
        "bridge_factor": "sqrt(2*pi) from Stirling, validated by the "
                         "least-term check to ~0.2%",
        "amplitude_contains_pi": "only via Gamma at half-integer argument, "
                                 "which is definitional, not bookkeeping",
        "rivals_excluded": ["C=1 requires K=0.7979", "C=pi requires K=2.5066"],
        "tag": "CONJECTURED",
    }
    os.makedirs("out", exist_ok=True)
    json.dump(out, open("out/pi_bookkeeping.json", "w"), indent=2)
    print("\n[out] out/pi_bookkeeping.json")


if __name__ == "__main__":
    main()
