"""Phase 0.1: convergence tables in BOTH node count and working precision.

Two independent knobs are swept, because they control two different errors:

  * NODE COUNT n  -> quadrature (discretisation) error.  Super-exponential in
    n once n exceeds roughly the bandwidth of the kernel.
  * mp.dps        -> arithmetic error.  Amplified by the condition number of
    I - K_s, which grows like exp(2s); the tables measure this amplification
    rather than assuming it.

The dps sweep is what exposes the digit LOSS: the plateau of the node sweep
sits at 10^-(dps - loss), and (dps - agreement) is a direct measurement of the
loss.  This is reported so that downstream precision choices are calibrated,
not guessed.
"""

from __future__ import annotations

import json
import time
from mpmath import mp

import sinekernel as sk

S_LIST = [10, 20, 30, 40]
#: node counts are taken RELATIVE to s: the kernel has bandwidth ~2s/pi, so
#: the resolution threshold moves with s and a fixed absolute list would mix
#: "under-resolved" and "converged" regimes across rows.
N_FACTORS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
N_REF_FACTOR = 6.0
DPS_FIXED = 200
DPS_LIST = [60, 80, 100, 120, 140]
DPS_REF = 180
OUTPUT = "out/convergence.json"


def _even(x):
    return 2 * int(round(x / 2))


def _d(x):
    return "exact" if x == 0 else mp.nstr(-mp.log10(abs(x)), 6)


def _safe(s, n, dps, **kw):
    """log_det, but an SPD failure is DATA, not a crash.

    I - K_s is symmetric positive definite for the true operator, and the
    Nystrom matrix inherits positive semidefiniteness of K for ANY nodes
    (sin(s*x)/(pi*x) is the Fourier transform of an indicator, hence a
    positive-definite function).  So a non-positive Cholesky pivot cannot
    happen in exact arithmetic on a resolved grid.  When it does happen it
    means one of two things, both of which we want in the table rather than
    hidden behind a try/except that returns a number anyway:

      * n is below the resolution threshold for this s (the quadrature has not
        yet captured the kernel bandwidth ~2s/pi, and the discrete spectrum
        has not settled below 1);
      * dps is below the arithmetic requirement (digit loss ~0.866*s).

    Recording the failure is the point: it demonstrates the implementation
    detects its own breakdown instead of returning a plausible wrong value.
    """
    try:
        return sk.log_det(s, n, dps, **kw), None
    except ArithmeticError as exc:
        msg = str(exc).split(":")[0]
        return None, msg


def node_table():
    print("=" * 78)
    print(f"NODE-COUNT CONVERGENCE  (mp.dps fixed at {DPS_FIXED}; "
          f"error vs n = {N_REF_FACTOR:g}*s)")
    print("   node counts are relative to s because the kernel bandwidth is ~2s/pi")
    print("=" * 78)
    out = {}
    for s in S_LIST:
        n_ref = _even(N_REF_FACTOR * s)
        ref, err = _safe(s, n_ref, DPS_FIXED)
        rows = []
        print(f"\n  s = {s}   reference n = {n_ref}   logdet = {mp.nstr(ref, 25)}")
        print(f"  {'n':>6}  {'n/s':>5}  {'|logdet(n) - logdet(nref)|':>28}  "
              f"{'agreeing digits':>16}")
        for f in N_FACTORS:
            n = _even(f * s)
            v, err = _safe(s, n, DPS_FIXED)
            if v is None:
                rows.append({"n": n, "n_over_s": f, "abs_err": None,
                             "digits": None, "diagnostic": err})
                print(f"  {n:>6}  {f:>5.1f}  {err:>28}  {'-':>16}")
                continue
            e = abs(v - ref)
            rows.append({"n": n, "n_over_s": f, "abs_err": mp.nstr(e, 6),
                         "digits": _d(e), "diagnostic": None})
            print(f"  {n:>6}  {f:>5.1f}  {mp.nstr(e, 6):>28}  {_d(e):>16}")
        out[str(s)] = rows
    return out


def dps_table():
    print("\n" + "=" * 78)
    print(f"PRECISION CONVERGENCE  (n = {N_REF_FACTOR:g}*s; error vs dps={DPS_REF})")
    print("   'digit loss' = dps - agreeing digits = conditioning cost of I-K_s")
    print("=" * 78)
    out = {}
    for s in S_LIST:
        n_ref = _even(N_REF_FACTOR * s)
        ref, _ = _safe(s, n_ref, DPS_REF)
        rows = []
        print(f"\n  s = {s}   (n = {n_ref})")
        print(f"  {'dps':>6}  {'|logdet(dps) - logdet(ref)|':>28}  "
              f"{'agreeing digits':>16}  {'digit loss':>11}")
        for dps in DPS_LIST:
            v, err = _safe(s, n_ref, dps)
            if v is None:
                rows.append({"dps": dps, "abs_err": None, "digits": None,
                             "digit_loss": None, "diagnostic": err})
                print(f"  {dps:>6}  {err:>28}  {'-':>16}  {'-':>11}")
                continue
            e = abs(v - ref)
            dg = mp.inf if e == 0 else -mp.log10(e)
            loss = mp.nstr(dps - dg, 5) if e != 0 else "-"
            rows.append({"dps": dps, "abs_err": mp.nstr(e, 6),
                         "digits": _d(e), "digit_loss": loss,
                         "diagnostic": None})
            print(f"  {dps:>6}  {mp.nstr(e, 6):>28}  {_d(e):>16}  {loss:>11}")
        out[str(s)] = rows
    return out


def cross_checks():
    """Structural identities the implementation must satisfy exactly."""
    print("\n" + "=" * 78)
    print("STRUCTURAL CROSS-CHECKS")
    print("=" * 78)
    res = {}

    n, dps = 12, 40
    x, w = sk.gauss_legendre(n, dps)
    with mp.workdps(dps):
        worst = max(abs(sum(wi * xi ** k for xi, wi in zip(x, w))
                        - (mp.mpf(0) if k % 2 else mp.mpf(2) / (k + 1)))
                    for k in range(2 * n))
    res["gl_exactness"] = mp.nstr(worst, 6)
    print(f"  GL exactness on polynomials of degree < {2*n}: max err {mp.nstr(worst,6)}")

    a = sk.log_det(5, 40, 50, factored=True, backend="mpmath")
    b = sk.log_det(5, 40, 50, factored=False, backend="mpmath")
    res["parity_factorisation"] = mp.nstr(abs(a - b), 6)
    print(f"  parity factorisation vs unfactored determinant: {mp.nstr(abs(a-b),6)}")

    a = sk.log_det(20, 80, 120, backend="mpmath")
    b = sk.log_det(20, 80, 120, backend="gmpy2")
    res["backend_agreement"] = mp.nstr(abs(a - b), 6)
    print(f"  mpmath backend vs gmpy2/MPFR backend:           {mp.nstr(abs(a-b),6)}")
    return res


def main():
    t0 = time.time()
    mp.dps = DPS_REF + 20
    out = {"node": node_table(), "dps": dps_table(), "cross": cross_checks()}
    out["wall_seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(OUTPUT, "w"), indent=1)
    print(f"\nwrote {OUTPUT}  ({out['wall_seconds']}s)")


if __name__ == "__main__":
    main()
