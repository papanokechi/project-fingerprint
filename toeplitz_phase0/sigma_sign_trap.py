"""Which sigma-form rendering does OUR DATA select?

Two published renderings of the same equation differ by sigma -> -sigma, and
therefore by the sign of the cross term.  Written in x with u = x*sig' - sig:

    (P)  x^2 sig''^2 + 4 u^2 + 4 u sig'^2 = 0     [Bornemann arXiv:0804.2543]
    (M)  x^2 sig''^2 + 4 u^2 - 4 u sig'^2 = 0     [Bornemann arXiv:0904.1581]

They are not in conflict: (M) is the image of (P) under sig -> -sig, and the
exponent sign in the determinant formula and the small-x initial condition
flip along with it.  Both are internally consistent.  The hazard is taking
the equation from one paper and the initial condition from the other, which
is silent -- the algebra stays consistent and the answer is wrong.

This is the SECOND convention trap in this project, after alpha-vs-2alpha,
and it has the same resolution: the numerics adjudicate.  We do not need to
decide which paper's convention is "right"; we measure which one our own
sigma satisfies, and we measure the discriminant the operator identified --
the sign of sigma near 0 -- so the pairing of equation with initial condition
is fixed by data rather than by a citation.

Run: python sigma_sign_trap.py
"""
import json

from mpmath import mp

from sigma_ode import sigma_data

LAMBDA = 2  # our s relates to the published x by x = 2 s  (L-042)


def residuals(s, n):
    """(P, M) residuals in the PUBLISHED variable x = 2s, plus sigma itself."""
    sig, sig1, sig2 = sigma_data(s, n)
    # tau(x) = sigma(x/2):  tau' = sigma'/2, tau'' = sigma''/4, x = 2s.
    x = LAMBDA * s
    t1 = sig1 / LAMBDA
    t2 = sig2 / LAMBDA ** 2
    u = x * t1 - sig
    cross = 4 * u * t1 ** 2
    base = x ** 2 * t2 ** 2 + 4 * u ** 2
    return sig, base + cross, base - cross


def main():
    mp.dps = 120
    print("[cfg] dps=120, x = 2s, tau(x) = sigma(x/2)\n")
    print(f"{'s':>6} {'sigma':>16} {'resid (P), +cross':>22} "
          f"{'resid (M), -cross':>22}")

    rows = []
    for s in (mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf(1), mp.mpf(2),
              mp.mpf(4), mp.mpf(8)):
        n = max(60, (int(6 * s) + 60) // 2 * 2)
        sig, rp, rm = residuals(s, n)
        rows.append((s, sig, rp, rm))
        print(f"{mp.nstr(s,4):>6} {mp.nstr(sig,10):>16} "
              f"{mp.nstr(rp,6):>22} {mp.nstr(rm,6):>22}")

    print("\n[discriminant] sign of sigma near 0 (this is what pairs the")
    print("               equation with its initial condition):")
    small = rows[0]
    print(f"  sigma({mp.nstr(small[0],4)}) = {mp.nstr(small[1],12)}  -> "
          f"{'NEGATIVE' if small[1] < 0 else 'POSITIVE'}")
    print("  log det(I-K_s) is decreasing in s, so sigma = s*(log det)' < 0.")
    print("  Our convention therefore matches the rendering whose small-x")
    print("  behaviour is sigma < 0, i.e. arXiv:0804.2543, and the +cross")
    print("  form -- which is exactly what the residual column shows.")

    okP = all(abs(r[2]) < mp.mpf(10) ** -60 for r in rows)
    okM = all(abs(r[3]) < mp.mpf(10) ** -60 for r in rows)
    print(f"\n[verdict] (P) +cross holds on our data: {okP}")
    print(f"[verdict] (M) -cross holds on our data: {okM}")
    if okP and not okM:
        print("  Selected: (P). The alternative is not a variant we may")
        print("  adopt -- on OUR sigma it is false by many orders, so the")
        print("  pairing is fixed by measurement, not by choosing a source.")
    elif okP and okM:
        raise SystemExit("BOTH hold -- the test cannot discriminate; the "
                         "residual scale is wrong, not the mathematics.")
    else:
        raise SystemExit("Neither rendering holds; normalisation is wrong.")

    json.dump({"lambda": LAMBDA,
               "sigma_small_s_sign": "negative" if rows[0][1] < 0 else "positive",
               "plus_cross_holds": bool(okP),
               "minus_cross_holds": bool(okM),
               "rows": [{"s": mp.nstr(r[0], 6), "sigma": mp.nstr(r[1], 20),
                         "resid_plus": mp.nstr(r[2], 6),
                         "resid_minus": mp.nstr(r[3], 6)} for r in rows]},
              open("out/sigma_sign_trap.json", "w"), indent=2)
    print("\n[out] out/sigma_sign_trap.json")


if __name__ == "__main__":
    main()
