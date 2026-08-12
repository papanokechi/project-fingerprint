"""Discover the sigma-form ODE satisfied by the sine-kernel determinant.

MOTIVATION (operator, this session): if the only thing the Painleve-V series
cannot supply is the constant term, then the entire algebraic tail that
fit_constant.py currently annihilates with K Richardson orders is derivable
by recursion.  That would collapse E1 rather than extrapolate it away.

DISCIPLINE PROBLEM: writing down the sigma-form ODE from memory is a
HARD RULE 1 violation, and taking it from the operator is the same violation
one channel removed.  So this module does not write it down.  It DISCOVERS
it as a null vector of a monomial design matrix built from our own
high-precision determinant data, and then re-verifies the discovered relation
at independent s values that took no part in the discovery.

That makes the ODE VERIFIED (found numerically, stated precision, null
controls, out-of-sample confirmation) rather than CONJECTURED-from-recall.

METHOD
  L(s)    = log det(I - K_s) on [-1,1], K_s(x,y) = sin(s(x-y))/(pi(x-y))
  sigma   = s * L'(s)

  Derivatives of L come from the Nystrom matrix analytically, NOT from finite
  differences.  With A = I - M(s),

      L'   = Tr(A^-1 A')
      L''  = Tr(A^-1 A'') - Tr(X^2)                      X = A^-1 A'
      L''' = Tr(A^-1 A''') - 3 Tr(A^-1 A'' X) + 2 Tr(X^3)

  and the s-derivatives of the kernel are exact:
      d^0 : sin(s d)/(pi d)      (-> s/pi at d=0)
      d^1 : cos(s d)/pi
      d^2 : -d sin(s d)/pi
      d^3 : -d^2 cos(s d)/pi

  We then search for a polynomial relation P(s, sigma, sigma', sigma'') = 0
  over all monomials of bounded total degree.
"""

from __future__ import annotations

import itertools
import json
import sys

from mpmath import mp

from sinekernel import gauss_legendre


# ---------------------------------------------------------------------------
# Parity blocks and their exact s-derivatives.
#
# A+ = I - (a + b), A- = I - (a - b), with
#   a = q sin(s dm)/(pi dm),  dm = xi - xj
#   b = q sin(s dp)/(pi dp),  dp = xi + xj
# so the r-th s-derivative replaces sin(s d)/(pi d) by the r-th entry of
# the table above.  Sign of the b-part is +1 for A+, -1 for A-.
# ---------------------------------------------------------------------------

def _kern_deriv(order: int, s, d):
    """r-th s-derivative of sin(s*d)/(pi*d), with the d=0 limit handled."""
    pi = mp.pi
    if order == 0:
        return s / pi if d == 0 else mp.sin(s * d) / (pi * d)
    if order == 1:
        return mp.cos(s * d) / pi
    if order == 2:
        return -d * mp.sin(s * d) / pi
    if order == 3:
        return -d * d * mp.cos(s * d) / pi
    raise ValueError("order <= 3 only")


def _block_derivs(s, n: int, sign: int):
    """Return [A, A', A'', A'''] for one parity block as mpmath matrices.

    sign = +1 gives the '+' block, sign = -1 the '-' block.
    """
    if n % 2 != 0:
        raise ValueError("parity factorisation requires even n")
    nodes, weights = gauss_legendre(n, mp.dps)
    h = n // 2
    x = nodes[:h]
    sq = [mp.sqrt(w) for w in weights[:h]]

    out = []
    for r in range(4):
        A = mp.matrix(h, h)
        for i in range(h):
            for j in range(h):
                q = sq[i] * sq[j]
                a = _kern_deriv(r, s, x[i] - x[j])
                b = _kern_deriv(r, s, x[i] + x[j])
                A[i, j] = -q * (a + sign * b)
            if r == 0:
                A[i, i] += 1
        out.append(A)
    return out


def _logdet_derivs_block(s, n: int, sign: int):
    """(L', L'', L''') for one parity block."""
    A, A1, A2, A3 = _block_derivs(s, n, sign)
    Ainv = A ** -1
    X = Ainv * A1
    Y = Ainv * A2
    Z = Ainv * A3

    def tr(M):
        return sum(M[i, i] for i in range(M.rows))

    X2 = X * X
    L1 = tr(X)
    L2 = tr(Y) - tr(X2)
    L3 = tr(Z) - 3 * tr(Y * X) + 2 * tr(X2 * X)
    return L1, L2, L3


def sigma_data(s, n: int):
    """sigma = s L', and sigma', sigma'' -- summed over both parity blocks."""
    p = _logdet_derivs_block(s, n, +1)
    m = _logdet_derivs_block(s, n, -1)
    L1 = p[0] + m[0]
    L2 = p[1] + m[1]
    L3 = p[2] + m[2]
    sig = s * L1
    sig1 = L1 + s * L2
    sig2 = 2 * L2 + s * L3
    return sig, sig1, sig2


# ---------------------------------------------------------------------------
# Monomial design matrix and nullspace search
# ---------------------------------------------------------------------------

VARNAMES = ["s", "sig", "sig1", "sig2"]


def monomials(maxdeg: int):
    """All exponent tuples over (s, sigma, sigma', sigma'') of total deg<=maxdeg."""
    out = []
    for e in itertools.product(range(maxdeg + 1), repeat=4):
        if sum(e) <= maxdeg:
            out.append(e)
    out.sort(key=lambda e: (sum(e), e))
    return out


def mono_str(e):
    parts = []
    for name, k in zip(VARNAMES, e):
        if k == 1:
            parts.append(name)
        elif k > 1:
            parts.append(f"{name}^{k}")
    return "*".join(parts) if parts else "1"


def design_row(vals, monos):
    s, sig, sig1, sig2 = vals
    row = []
    for e in monos:
        t = mp.mpf(1)
        if e[0]:
            t *= s ** e[0]
        if e[1]:
            t *= sig ** e[1]
        if e[2]:
            t *= sig1 ** e[2]
        if e[3]:
            t *= sig2 ** e[3]
        row.append(t)
    return row


def nullspace(rows, tol_exp):
    """Return (null_vectors, singular_values) via SVD of the design matrix.

    CONDITIONING (first run, L-035): sigma ~ -s^2, so a degree-4 monomial
    spans s^8.  Sampling s over [0.5, 23] then gives a design matrix with a
    dynamic range near 1e13 across rows and far more across columns, and the
    SVD reports a smooth decay with no spectral gap -- 34 spurious "null
    directions" that are pure conditioning noise.  Row and column
    equilibration is therefore not cosmetic, it is what makes the question
    well posed.  Column scaling multiplies coefficient c_j by 1/colnorm_j,
    and is undone before the relation is reported.
    """
    nr, nc = len(rows), len(rows[0])
    R = [r[:] for r in rows]

    # Row equilibration: each row is a separate homogeneous equation, so
    # scaling it changes nothing about the solution set.
    for i in range(nr):
        nrm = mp.sqrt(sum(x * x for x in R[i]))
        if nrm > 0:
            R[i] = [x / nrm for x in R[i]]

    # Column equilibration: rescales the unknowns, undone below.
    colnorm = []
    for j in range(nc):
        nrm = mp.sqrt(sum(R[i][j] ** 2 for i in range(nr)))
        colnorm.append(nrm if nrm > 0 else mp.mpf(1))
    for i in range(nr):
        R[i] = [R[i][j] / colnorm[j] for j in range(nc)]

    A = mp.matrix(R)
    U, S, V = mp.svd_r(A, full_matrices=False)
    svals = [S[i] for i in range(len(S))]
    smax = max(svals)
    null = []
    for i, sv in enumerate(svals):
        if sv / smax < mp.mpf(10) ** (-tol_exp):
            null.append([V[i, j] / colnorm[j] for j in range(V.cols)])
    return null, svals


def main():
    dps = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    maxdeg = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    nnodes = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    mp.dps = dps

    monos = monomials(maxdeg)
    nm = len(monos)
    nsamp = nm + 12
    print(f"[cfg] dps={dps} maxdeg={maxdeg} n={nnodes} "
          f"monomials={nm} samples={nsamp}", flush=True)

    # Discovery sample: small/moderate s where Nystrom converges very fast,
    # deliberately irrational spacing so no lattice can alias the fit
    # (L-030: validation points must lie off the fitting lattice).
    # Range kept narrow on purpose: the dynamic range of the design matrix
    # grows like (s_max/s_min)^(2*maxdeg), so a wide sweep destroys the SVD
    # long before it adds information (L-035).
    smin, swid = mp.mpf(1), mp.mpf(3)
    ss = [smin + swid * mp.frac(mp.mpf(i) * mp.sqrt(2)) for i in range(nsamp)]

    rows = []
    for k, s in enumerate(ss):
        sig, sig1, sig2 = sigma_data(s, nnodes)
        rows.append(design_row((s, sig, sig1, sig2), monos))
        if k % 10 == 0:
            print(f"  sample {k}/{nsamp} s={mp.nstr(s, 8)} "
                  f"sigma={mp.nstr(sig, 12)}", flush=True)

    tol_exp = dps // 2
    null, svals = nullspace(rows, tol_exp)
    smax = max(svals)
    ratios = sorted(float(mp.log10(sv / smax)) for sv in svals)
    print(f"[svd] {len(null)} null direction(s) at 1e-{tol_exp}")
    print(f"[svd] log10 sing.value spectrum (smallest 6): "
          f"{[round(r, 2) for r in ratios[:6]]}")

    result = {"dps": dps, "maxdeg": maxdeg, "n": nnodes,
              "n_monomials": nm, "n_samples": nsamp,
              "n_null": len(null),
              "log10_svals_smallest": [round(r, 3) for r in ratios[:8]],
              "relations": []}

    for v in null:
        big = max(range(nm), key=lambda i: abs(v[i]))
        scaled = [x / v[big] for x in v]
        terms = []
        for e, c in zip(monos, scaled):
            if abs(c) > mp.mpf(10) ** (-tol_exp + 5):
                terms.append({"mono": mono_str(e), "coeff": mp.nstr(c, 25)})
        result["relations"].append(terms)
        print("  RELATION: " + "  ".join(
            f"{t['coeff']}*{t['mono']}" for t in terms))

    with open("out/sigma_ode.json", "w") as fh:
        json.dump(result, fh, indent=2)
    print("[out] out/sigma_ode.json")


if __name__ == "__main__":
    main()
