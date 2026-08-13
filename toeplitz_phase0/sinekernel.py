"""Phase 0 core: sine-kernel Fredholm determinant via Nystrom / Gauss-Legendre.

Object under study
------------------
    K_s(x, y) = sin(s*(x-y)) / (pi*(x-y)),   (x, y) in [-1, 1]^2
    D(s)      = det(I - K_s)|_{L^2([-1,1])}

By the scaling u = s*x this is the sine-kernel gap probability on the interval
(-s, s) for the kernel sin(u-v)/(pi(u-v)).

Discretisation
--------------
Nystrom with n-point Gauss-Legendre nodes {x_i, w_i} on [-1,1]:

    M_ij = sqrt(w_i w_j) K_s(x_i, x_j),      D_n(s) = det(I_n - M)

Three structural facts are exploited, each verified numerically in tests:

(1) PARITY.  K_s(-x,-y) = K_s(x,y) and the GL rule is symmetric, so M commutes
    with the parity involution.  For even n, with h = n/2, jbar = n+1-j:
        B^{+-}_ij = M_ij +- M_{i,jbar}   (i,j <= h)
        det(I_n - M) = det(I_h - B^+) det(I_h - B^-)
    Exact similarity transform; 4x speedup of the O(n^3) elimination.

(2) POSITIVITY.  x -> sin(s x)/(pi x) is the Fourier transform of the
    indicator of [-s,s], hence a positive-definite function, so the sampled
    matrix [K_s(x_i,x_j)] is PSD for ANY nodes; and lambda_max(M) < 1.  So
    I - M is SPD and Cholesky needs no pivoting.  A Cholesky breakdown is
    therefore a genuine diagnostic (loss of precision), not a normal event.

(3) RANK-2 TRIG STRUCTURE.  sin(s(x_i-x_j)) = si*cj - ci*sj with
    si = sin(s x_i), ci = cos(s x_i): O(n) transcendental evaluations instead
    of O(n^2).

Everything is mpmath at configurable mp.dps.  NO numerical constant here is
recalled from literature; the only closed-form inputs are pi and the Legendre
three-term recurrence.
"""

from __future__ import annotations

import functools
from mpmath import mp
import math

try:
    import gmpy2
    from gmpy2 import mpfr as _mpfr
    _HAVE_GMPY2 = True
except ImportError:                                        # pragma: no cover
    _HAVE_GMPY2 = False

DEFAULT_BACKEND = "gmpy2" if _HAVE_GMPY2 else "mpmath"


# ----------------------------------------------------------------------------
# Gauss-Legendre nodes and weights, from scratch by Newton iteration on the
# three-term Legendre recurrence.  No table lookups.
# ----------------------------------------------------------------------------

def _legendre_pair(n: int, x):
    """(P_n(x), P_{n-1}(x)) via (k+1)P_{k+1} = (2k+1) x P_k - k P_{k-1}."""
    if n == 0:
        return mp.mpf(1), mp.mpf(0)
    if n == 1:
        return x, mp.mpf(1)
    p_prev = mp.mpf(1)
    p_curr = x
    for k in range(1, n):
        p_next = ((2 * k + 1) * x * p_curr - k * p_prev) / (k + 1)
        p_prev, p_curr = p_curr, p_next
    return p_curr, p_prev


def _legendre_deriv(n: int, x, pn, pnm1):
    """P_n'(x) = n (x P_n - P_{n-1}) / (x^2 - 1)."""
    return n * (x * pn - pnm1) / (x * x - 1)


@functools.lru_cache(maxsize=None)
def gauss_legendre(n: int, dps: int):
    """n-point Gauss-Legendre nodes/weights on [-1,1] at precision dps.

    Returns (nodes, weights), ordered so that node i and node n-1-i are exact
    negatives.  Computed with 25 guard digits, then rounded to dps.
    """
    work = dps + 25
    with mp.workdps(work):
        half = (n + 1) // 2
        xs, ws = [], []
        tol = mp.mpf(10) ** (-(work - 5))
        for i in range(half):
            x = mp.cos(mp.pi * (mp.mpf(i) + mp.mpf(3) / 4) / (mp.mpf(n) + mp.mpf(1) / 2))
            for _ in range(300):
                pn, pnm1 = _legendre_pair(n, x)
                dx = pn / _legendre_deriv(n, x, pn, pnm1)
                x = x - dx
                if abs(dx) < tol:
                    break
            else:
                raise RuntimeError(f"Legendre Newton failed, n={n}, root {i}")
            pn, pnm1 = _legendre_pair(n, x)
            dp = _legendre_deriv(n, x, pn, pnm1)
            xs.append(x)
            ws.append(2 / ((1 - x * x) * dp * dp))
    nodes, weights = [], []
    for i in range(half):
        nodes.append(+xs[i])
        weights.append(+ws[i])
    start = half - 2 if n % 2 == 1 else half - 1   # skip duplicating x = 0
    for i in range(start, -1, -1):
        nodes.append(-xs[i])
        weights.append(+ws[i])
    with mp.workdps(dps):
        nodes = [+mp.mpf(v) for v in nodes]
        weights = [+mp.mpf(v) for v in weights]
    assert len(nodes) == n
    return tuple(nodes), tuple(weights)


# ----------------------------------------------------------------------------
# Kernel
# ----------------------------------------------------------------------------

def sine_kernel(s, x, y):
    """K_s(x,y) = sin(s(x-y))/(pi(x-y)) with the removable singularity."""
    d = x - y
    if d == 0:
        return s / mp.pi
    return mp.sin(s * d) / (mp.pi * d)


# ----------------------------------------------------------------------------
# Dense Cholesky on list-of-lists (mpmath's matrix class costs ~5x more)
# ----------------------------------------------------------------------------

def _chol_logdet(A):
    """log det of an SPD matrix given as a list of lists (lower part used).

    Returns 2*sum_i log L_ii.  A non-positive pivot signals catastrophic
    precision loss (see structural fact (2)), and is raised, not absorbed.
    """
    n = len(A)
    L = [[mp.mpf(0)] * (i + 1) for i in range(n)]
    acc = mp.mpf(0)
    for i in range(n):
        Ai = A[i]
        Li = L[i]
        for j in range(i):
            Lj = L[j]
            t = Ai[j]
            for k in range(j):
                t -= Li[k] * Lj[k]
            Li[j] = t / Lj[j]
        t = Ai[i]
        for k in range(i):
            t -= Li[k] * Li[k]
        if t <= 0:
            raise ArithmeticError(
                f"Cholesky pivot {i} non-positive ({mp.nstr(t, 5)}): precision loss")
        d = mp.sqrt(t)
        Li[i] = d
        acc += mp.log(d)
    return 2 * acc


# ----------------------------------------------------------------------------
# Nystrom assembly
# ----------------------------------------------------------------------------

def _blocks(s, n: int):
    """Parity blocks I_h - B^+ and I_h - B^- as lists of lists (even n)."""
    if n % 2 != 0:
        raise ValueError("parity factorisation requires even n")
    nodes, weights = gauss_legendre(n, mp.dps)
    h = n // 2
    x = nodes[:h]
    sq = [mp.sqrt(w) for w in weights[:h]]
    sn = [mp.sin(s * xi) for xi in x]
    cs = [mp.cos(s * xi) for xi in x]
    pi = mp.pi
    spi = s / pi
    Ap = [[mp.mpf(0)] * h for _ in range(h)]
    Am = [[mp.mpf(0)] * h for _ in range(h)]
    for i in range(h):
        xi, si, ci, qi = x[i], sn[i], cs[i], sq[i]
        Api, Ami = Ap[i], Am[i]
        for j in range(h):
            xj, sj, cj, qj = x[j], sn[j], cs[j], sq[j]
            q = qi * qj
            dm = xi - xj
            a = spi * q if dm == 0 else q * (si * cj - ci * sj) / (pi * dm)
            dp = xi + xj
            b = spi * q if dp == 0 else q * (si * cj + ci * sj) / (pi * dp)
            Api[j] = -(a + b)
            Ami[j] = -(a - b)
        Api[i] += 1
        Ami[i] += 1
    return Ap, Am


def nystrom_matrix_full(s, n: int):
    """Full unfactored I_n - M as a list of lists.  Cross-check use only."""
    nodes, weights = gauss_legendre(n, mp.dps)
    sq = [mp.sqrt(w) for w in weights]
    A = [[mp.mpf(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = -sq[i] * sq[j] * sine_kernel(s, nodes[i], nodes[j])
        A[i][i] += 1
    return A


# ----------------------------------------------------------------------------
# gmpy2 / MPFR fast path.  Identical algorithm, C-speed inner loops.
# Conversions are bit-exact (mantissa/exponent), never via decimal strings.
# ----------------------------------------------------------------------------

def _to_mpfr(v):
    """mpmath mpf -> gmpy2 mpfr, exactly (context precision must suffice)."""
    sign, man, exp, bc = v._mpf_
    if man == 0:
        if bc == 0:
            return _mpfr(0)
        raise ValueError("non-finite mpf")
    r = _mpfr(man)
    r = gmpy2.mul_2exp(r, exp) if exp >= 0 else gmpy2.div_2exp(r, -exp)
    return -r if sign else r


def _from_mpfr(r):
    """gmpy2 mpfr -> mpmath mpf, exactly (mp precision must suffice)."""
    m, e = r.as_mantissa_exp()
    return mp.mpf(int(m)) * mp.mpf(2) ** int(e)


def _chol_logdet_mpfr(A):
    """log det of an SPD list-of-lists of mpfr, via fused multiply-add."""
    n = len(A)
    fma = gmpy2.fma
    L = [[_mpfr(0)] * (i + 1) for i in range(n)]
    acc = _mpfr(0)
    for i in range(n):
        Ai, Li = A[i], L[i]
        for j in range(i):
            Lj = L[j]
            t = Ai[j]
            for k in range(j):
                t = fma(-Li[k], Lj[k], t)
            Li[j] = t / Lj[j]
        t = Ai[i]
        for k in range(i):
            t = fma(-Li[k], Li[k], t)
        if t <= 0:
            raise ArithmeticError(
                f"Cholesky pivot {i} non-positive ({t}): precision loss")
        d = gmpy2.sqrt(t)
        Li[i] = d
        acc += gmpy2.log(d)
    return 2 * acc


def _blocks_mpfr(s, n: int):
    """Parity blocks as lists of lists of mpfr.  Nodes still from mpmath."""
    if n % 2 != 0:
        raise ValueError("parity factorisation requires even n")
    nodes, weights = gauss_legendre(n, mp.dps)
    h = n // 2
    x = [_to_mpfr(v) for v in nodes[:h]]
    sq = [gmpy2.sqrt(_to_mpfr(w)) for w in weights[:h]]
    sm = _to_mpfr(mp.mpf(s))
    sn = [gmpy2.sin(sm * xi) for xi in x]
    cs = [gmpy2.cos(sm * xi) for xi in x]
    pi = gmpy2.const_pi()
    spi = sm / pi
    zero = _mpfr(0)
    Ap = [[zero] * h for _ in range(h)]
    Am = [[zero] * h for _ in range(h)]
    for i in range(h):
        xi, si, ci, qi = x[i], sn[i], cs[i], sq[i]
        Api, Ami = Ap[i], Am[i]
        for j in range(h):
            xj, sj, cj, qj = x[j], sn[j], cs[j], sq[j]
            q = qi * qj
            dm = xi - xj
            a = spi * q if dm == 0 else q * (si * cj - ci * sj) / (pi * dm)
            dp = xi + xj
            b = spi * q if dp == 0 else q * (si * cj + ci * sj) / (pi * dp)
            Api[j] = -(a + b)
            Ami[j] = -(a - b)
        Api[i] += 1
        Ami[i] += 1
    return Ap, Am


def log_det(s, n: int, dps: int, factored: bool = True, backend: str = None):
    """log det(I - K_s) via n-point Nystrom at working precision dps.

    The determinant is exponentially small, so the logarithm is accumulated
    from the Cholesky pivots rather than from a product that would be lost to
    the exponent range of intermediates.

    backend='gmpy2' (default when available) and backend='mpmath' run the same
    algorithm; test_smoke.py asserts they agree.
    """
    if backend is None:
        backend = DEFAULT_BACKEND
    with mp.workdps(dps):
        s = mp.mpf(s)
        if backend == "gmpy2":
            if not factored:
                raise NotImplementedError("gmpy2 path is parity-factored only")
            old = gmpy2.get_context().precision
            gmpy2.get_context().precision = int(dps * math.log2(10)) + 20
            try:
                Ap, Am = _blocks_mpfr(s, n)
                tot = _chol_logdet_mpfr(Ap) + _chol_logdet_mpfr(Am)
                return +_from_mpfr(tot)
            finally:
                gmpy2.get_context().precision = old
        if factored:
            Ap, Am = _blocks(s, n)
            return +(_chol_logdet(Ap) + _chol_logdet(Am))
        return +_chol_logdet(nystrom_matrix_full(s, n))
