"""PSLQ basis constants, every one COMPUTED in-session by mpmath.

No value in this file is transcribed from memory or from a reference table.
Each entry is a callable of the working precision, so `check_constants` can
recompute at dps and dps+30 and confirm agreement -- the convergence evidence
required to tag a value VERIFIED rather than CONJECTURED.

The one thing that is NOT established here is the *interpretation*: that these
particular constants are the right basis for c is a modelling choice, and any
relation found among them is CONJECTURED until proved.
"""

from __future__ import annotations

from mpmath import mp


def _one(_):
    return mp.mpf(1)


def _log2(_):
    return mp.log(2)


def _logpi(_):
    return mp.log(mp.pi)


def _gamma(_):
    return +mp.euler


def _zeta_prime_m1(_):
    """zeta'(-1), by mpmath's derivative-of-zeta routine."""
    return mp.zeta(-1, 1, 1)


def _zeta3_over_pi2(_):
    return mp.zeta(3) / mp.pi ** 2


def _catalan(_):
    return +mp.catalan


def _log1psqrt2(_):
    return mp.log(1 + mp.sqrt(2))


#: Ordered PSLQ basis as specified for Phase 0.4.
BASIS = [
    ("1", _one),
    ("log2", _log2),
    ("logpi", _logpi),
    ("gamma", _gamma),
    ("zeta'(-1)", _zeta_prime_m1),
    ("zeta(3)/pi^2", _zeta3_over_pi2),
    ("Catalan", _catalan),
    ("log(1+sqrt2)", _log1psqrt2),
]


def basis_values(dps: int, names=None):
    """Evaluate the basis at precision dps.  Returns (names, values)."""
    items = BASIS if names is None else [b for b in BASIS if b[0] in names]
    with mp.workdps(dps + 10):
        vals = [f(dps) for _, f in items]
    with mp.workdps(dps):
        vals = [+v for v in vals]
    return [n for n, _ in items], vals


def check_constants(dps: int, bump: int = 30):
    """Recompute every basis constant at dps and dps+bump; report agreement.

    Returns a list of (name, agreed_digits) where agreed_digits is
    -log10|v_hi - v_lo| / |v_hi| (capped at dps).
    """
    names, lo = basis_values(dps)
    _, hi = basis_values(dps + bump)
    out = []
    with mp.workdps(dps + bump + 10):
        for nm, a, b in zip(names, lo, hi):
            if b == 0:
                d = mp.inf
            else:
                rel = abs(mp.mpf(a) - mp.mpf(b)) / abs(b)
                d = mp.inf if rel == 0 else -mp.log10(rel)
            out.append((nm, min(mp.mpf(dps), d)))
    return out


def glaisher_cross_check(dps: int):
    """Independent-route check: zeta'(-1) = 1/12 - log A (Glaisher-Kinkelin).

    mpmath computes glaisher and zeta' by different code paths, so agreement
    is evidence against a transcription or API-misuse error on our side.  It
    is NOT an independent mathematical derivation.
    """
    with mp.workdps(dps + 10):
        via_zeta = mp.zeta(-1, 1, 1)
        via_glaisher = mp.mpf(1) / 12 - mp.log(mp.glaisher)
        rel = abs(via_zeta - via_glaisher) / abs(via_zeta)
        digits = mp.inf if rel == 0 else -mp.log10(rel)
    return via_zeta, via_glaisher, digits
