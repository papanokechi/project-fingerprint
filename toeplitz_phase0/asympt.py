"""Asymptotic extraction for log det(I - K_s).

Model
-----
    log det(I - K_s) = a s^2 + b log s + c + sum_{k=1..K} d_k s^{-k} + R_K(s)

The three leading exponents are treated as unknowns to be *measured*, not
imposed, so that agreement with a = -1/2 and b = -1/4 is evidence about the
pipeline rather than an assumption baked into it.

Given m = K + 3 sample points the system is square and solved exactly in
mpmath.  Sweeping K is a Richardson-type sequence acceleration: each increment
of K removes one more power of 1/s from the residual, and the successive
differences |c(K) - c(K-1)| form the honest convergence diagnostic.

There are two entirely different error scales in this module and they must
never be conflated:

  * mp.dps            -- arithmetic working precision.  Says nothing about
                         how well c is determined.
  * fit uncertainty   -- how well c is pinned down by the data, estimated from
                         (i) successive-order differences and (ii) held-out
                         prediction residuals.  This is the reportable number.
"""

from __future__ import annotations

from mpmath import mp


def design_row(s, K: int, step: int = 1):
    """[s^2, log s, 1, s^-step, s^-2*step, ..., s^-K*step]."""
    row = [s * s, mp.log(s), mp.mpf(1)]
    inv = mp.mpf(1) / s ** step
    p = mp.mpf(1)
    for _ in range(K):
        p *= inv
        row.append(p)
    return row


def fit(svals, yvals, K: int, step: int = 1):
    """Exact square solve on m = K+3 points.  Returns (a, b, c, [d_1..d_K])."""
    m = K + 3
    if len(svals) != m:
        raise ValueError(f"need exactly {m} points for K={K}, got {len(svals)}")
    A = mp.matrix([design_row(mp.mpf(s), K, step) for s in svals])
    y = mp.matrix([mp.mpf(v) for v in yvals])
    sol = mp.lu_solve(A, y)
    return sol[0], sol[1], sol[2], [sol[3 + i] for i in range(K)]


def fit_lstsq(svals, yvals, K: int, step: int = 1):
    """Overdetermined fit via normal equations (used for held-out checks)."""
    rows = [design_row(mp.mpf(s), K, step) for s in svals]
    A = mp.matrix(rows)
    y = mp.matrix([mp.mpf(v) for v in yvals])
    At = A.T
    sol = mp.lu_solve(At * A, At * y)
    return sol[0], sol[1], sol[2], [sol[3 + i] for i in range(K)]


def predict(a, b, c, ds, s, step: int = 1):
    s = mp.mpf(s)
    v = a * s * s + b * mp.log(s) + c
    inv = mp.mpf(1) / s ** step
    p = mp.mpf(1)
    for dk in ds:
        p *= inv
        v += dk * p
    return v


def order_sweep(pts, Kmax: int, step: int = 1):
    """Sweep K using the K+3 largest available s.  Returns list of records."""
    svals = sorted(pts)
    out = []
    for K in range(0, Kmax + 1):
        m = K + 3
        if m > len(svals):
            break
        use = svals[-m:]
        a, b, c, ds = fit(use, [pts[s] for s in use], K, step)
        out.append({"K": K, "a": a, "b": b, "c": c, "d": ds, "s": use})
    return out


def holdout_residual(pts, K: int, held, step: int = 1):
    """Fit on all points except `held`, then report |prediction - truth|.

    This is a genuine falsification test of the model class: the held-out
    point plays no role in determining the coefficients.
    """
    svals = [s for s in sorted(pts) if s != held]
    use = svals[-(K + 3):]
    a, b, c, ds = fit(use, [pts[s] for s in use], K, step)
    return abs(predict(a, b, c, ds, held, step) - pts[held]), c
