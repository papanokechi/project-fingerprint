"""Is the 2.7-digit excess constant, or is there an algebraic prefactor?

The operator read the excess (2.69, 2.72, 2.74 at s = 149, 200, 250) as
drift-free, concluding the beyond-all-orders remainder is C*exp(-2s) with no
algebraic correction, and bounding any power s^-a by |a| <= 0.22.

Recomputing the same three numbers gives a DIFFERENT reading.  The drift is
not zero: the two intervals independently imply a = 0.235 and a = 0.206.
Those agree with each other and sit AT the operator's bound rather than below
it, which is what one would see if a were genuinely nonzero and near 1/4.

Two decimal places is not enough to tell "at the bound" from "below it", so
this script does the measurement properly: honest digits to many decimals
over a wide range of s, then a three-parameter fit

    digits(s) = A*s + a*log10(s) + B

with A compared against 2/ln(10), and a against 0 and 1/4.

The confound to respect: optimal truncation picks an INTEGER M, so E_trunc
jitters as the minimum hops between neighbouring terms.  That jitter is
common-mode in a 3-point read and can easily manufacture a drift of a few
hundredths.  Using many s values averages it down and, more importantly,
makes it visible.
"""
import json

from mpmath import mp

from direct_c import load_coeffs, c_estimate


def rows():
    out = {}
    for path in ("out/certified_data.json", "out/highs_points.json"):
        try:
            d = json.load(open(path))
        except FileNotFoundError:
            continue
        for r in d["rows"]:
            s = mp.mpf(r["s"])
            cert = mp.mpf(r["certified_digits"])
            k = int(s)
            if k not in out or cert > out[k][1]:
                out[k] = (r, cert)
    return out


def main():
    coeffs = load_coeffs("out/sigma_recursion_fast.json")
    orders = sorted(coeffs)
    mp.dps = 700

    pts = []
    for s_int, (r, cert) in sorted(rows().items()):
        if 2 * s_int > orders[-1]:
            continue                      # truncation minimum unreachable
        if s_int < 60:
            continue                      # asymptotic regime only
        s = mp.mpf(r["s"])
        L = mp.mpf(r["value"])
        best = None
        for M in orders:
            cv, omit = c_estimate(s, L, coeffs, M)
            if omit == 0:
                continue
            if best is None or omit < best[2]:
                best = (M, cv, omit)
        M, cv, omit = best
        if omit <= mp.mpf(10) ** (-cert):
            continue                      # data-limited, not truncation
        digits = -mp.log10(omit / abs(cv))
        pts.append((s, digits, M))

    print(f"[cfg] {len(pts)} usable points, s in "
          f"[{mp.nstr(pts[0][0],4)}, {mp.nstr(pts[-1][0],4)}]; "
          f"coefficients to m={orders[-1]}")

    # Least squares for digits = A*s + a*log10(s) + B, in mpmath.
    n = len(pts)
    basis = [[p[0], mp.log10(p[0]), mp.mpf(1)] for p in pts]
    y = [p[1] for p in pts]
    ata = [[sum(basis[k][i] * basis[k][j] for k in range(n))
            for j in range(3)] for i in range(3)]
    aty = [sum(basis[k][i] * y[k] for k in range(n)) for i in range(3)]
    sol = mp.lu_solve(mp.matrix(ata), mp.matrix(aty))
    A, a, B = sol[0], sol[1], sol[2]

    resid = [y[k] - (A * basis[k][0] + a * basis[k][1] + B) for k in range(n)]
    rms = mp.sqrt(sum(r ** 2 for r in resid) / n)

    print(f"\n  A (slope)      = {mp.nstr(A, 8)}   vs 2/ln10 = "
          f"{mp.nstr(2 / mp.log(10), 8)}")
    print(f"  a (log coeff)  = {mp.nstr(a, 6)}")
    print(f"  B (constant)   = {mp.nstr(B, 6)}")
    print(f"  rms residual   = {mp.nstr(rms, 4)} digits over {n} points")

    print("\n[jitter check] integer-M truncation makes E_trunc hop; the")
    print("  residual scatter bounds how much of any drift is real.")
    print(f"  max |residual| = {mp.nstr(max(abs(r) for r in resid), 4)}")

    # Compare the two hypotheses on equal footing.
    for label, afix in (("a = 0    (pure C*exp(-2s))", mp.mpf(0)),
                        ("a = 1/4", mp.mpf(1) / 4),
                        ("a = free", None)):
        if afix is None:
            r2 = rms
        else:
            b2 = [[p[0], mp.mpf(1)] for p in pts]
            y2 = [y[k] - afix * mp.log10(pts[k][0]) for k in range(n)]
            m2 = [[sum(b2[k][i] * b2[k][j] for k in range(n))
                   for j in range(2)] for i in range(2)]
            v2 = [sum(b2[k][i] * y2[k] for k in range(n)) for i in range(2)]
            s2 = mp.lu_solve(mp.matrix(m2), mp.matrix(v2))
            rr = [y2[k] - (s2[0] * b2[k][0] + s2[1]) for k in range(n)]
            r2 = mp.sqrt(sum(t ** 2 for t in rr) / n)
        print(f"  {label:<26} rms = {mp.nstr(r2, 4)}")

    json.dump({"n": n, "A": mp.nstr(A, 10), "a": mp.nstr(a, 8),
               "B": mp.nstr(B, 8), "rms": mp.nstr(rms, 6),
               "two_over_ln10": mp.nstr(2 / mp.log(10), 10)},
              open("out/excess_structure.json", "w"), indent=2)
    print("\n[out] out/excess_structure.json")


if __name__ == "__main__":
    main()
