"""Smoke tests: GL quadrature correctness, parity factorisation identity, timing."""
import time
from mpmath import mp
import sinekernel as sk


def test_gl_rule():
    """GL rule must integrate polynomials up to degree 2n-1 exactly."""
    mp.dps = 40
    n = 12
    x, w = sk.gauss_legendre(n, 40)
    worst = mp.mpf(0)
    for k in range(0, 2 * n):
        approx = sum(wi * xi ** k for xi, wi in zip(x, w))
        exact = mp.mpf(0) if k % 2 else mp.mpf(2) / (k + 1)
        worst = max(worst, abs(approx - exact))
    print(f"  GL n={n}: max |quad - exact| over deg<{2*n} = {mp.nstr(worst, 5)}")
    assert worst < mp.mpf(10) ** -35, "GL rule failed exactness test"
    # symmetry
    assert all(abs(x[i] + x[n - 1 - i]) == 0 for i in range(n)), "nodes not symmetric"
    print("  GL nodes exactly symmetric: OK")


def test_parity_identity():
    """Factored and unfactored log-determinants must agree.

    The unfactored path is implemented only in the mpmath backend (it exists
    purely as an independent check on the parity block-diagonalisation), so
    the comparison is made explicitly across backends:

        factored/gmpy2  vs  unfactored/mpmath

    That is the stronger test of the two available: it exercises the parity
    argument AND the two independent arithmetic implementations at once, so a
    coincidental agreement would require both to be wrong in the same way.
    """
    mp.dps = 50
    for s in (mp.mpf(1), mp.mpf(5)):
        n = 40
        a_mp = sk.log_det(s, n, 50, factored=True, backend="mpmath")
        b_mp = sk.log_det(s, n, 50, factored=False, backend="mpmath")
        rel = abs(a_mp - b_mp) / abs(b_mp)
        print(f"  s={s}: factored vs full (mpmath),        rel diff = {mp.nstr(rel, 5)}")
        assert rel < mp.mpf(10) ** -42, "parity factorisation mismatch"

        a_g = sk.log_det(s, n, 50, factored=True, backend="gmpy2")
        rel2 = abs(a_g - b_mp) / abs(b_mp)
        print(f"  s={s}: factored/gmpy2 vs full/mpmath,    rel diff = {mp.nstr(rel2, 5)}")
        assert rel2 < mp.mpf(10) ** -42, "backend/parity cross-check mismatch"


def test_spd_diagnostic():
    """An under-resolved grid must RAISE, not return a plausible number.

    I - K_s is SPD, so a non-positive Cholesky pivot is impossible in exact
    arithmetic on a resolved grid.  Below the resolution threshold the code is
    required to detect its own breakdown.  A silent wrong answer here is the
    failure mode this whole pipeline is built to exclude, so it is tested
    rather than assumed.
    """
    try:
        sk.log_det(mp.mpf(30), 40, 160)
    except ArithmeticError as exc:
        print(f"  under-resolved (s=30, n=40) correctly raised: "
              f"{str(exc).split(':')[0]}")
        return
    raise AssertionError("under-resolved grid did not trigger the SPD diagnostic")


def test_grid_spec_matches_data():
    """`build_grid.BLOCKS` must generate EXACTLY the grid in certified_data.json.

    This test exists because of L-025.  The rebuild target declared a grid that
    was not the grid the published claims were computed on -- a CORRECT claim
    with a WRONG reproduction path.  That defect is invisible to every check
    except actually running the hours-long rebuild and comparing, which is
    precisely why it survived to be found by inspection.

    The underlying fragility is that BLOCKS is a SECOND source of truth for the
    grid, alongside the data file that extend_adaptive.py actually wrote.  Two
    sources of truth silently diverge whenever the grid is extended.  This test
    does not remove the duplication, it makes the divergence loud and immediate.

    Skips (rather than fails) when the data file is absent, because `verify`
    runs the smoke tests BEFORE building the grid from nothing.
    """
    import json
    import os

    import build_grid

    if not os.path.exists("out/certified_data.json"):
        print("  no certified_data.json yet -- skipped (from-scratch run)")
        return

    mp.dps = 30
    want = set()
    for a, b, st in build_grid.BLOCKS:
        a, b, st = mp.mpf(a), mp.mpf(b), mp.mpf(st)
        s = a
        while s <= b + st / 10:
            want.add(mp.nstr(+s, 20))
            s += st
    have = {r["s"] for r in json.load(open("out/certified_data.json"))["rows"]}

    missing, extra = sorted(want - have), sorted(have - want)
    print(f"  BLOCKS generates {len(want)} points; data file holds {len(have)}")
    assert not missing, f"BLOCKS declares {len(missing)} points absent from data: {missing[:5]}"
    assert not extra, f"data holds {len(extra)} points BLOCKS would never build: {extra[:5]}"
    print("  rebuild spec and data agree exactly (set equality, both directions)")


def bench():
    for (n, dps) in ((60, 60), (120, 120), (200, 160)):
        t = time.time()
        v = sk.log_det(mp.mpf(10), n, dps)
        print(f"  n={n:4d} dps={dps:4d}: {time.time()-t:7.2f}s  logdet(10)={mp.nstr(v, 12)}")


if __name__ == "__main__":
    print("[gl rule]");         test_gl_rule()
    print("[parity identity]"); test_parity_identity()
    print("[spd diagnostic]");  test_spd_diagnostic()
    print("[grid spec]");       test_grid_spec_matches_data()
    print("[timing]");          bench()
    print("ALL SMOKE TESTS PASSED")


def test_sigma_ode_holds_out_of_sample():
    """L-036: the discovered ODE must hold far outside its discovery window.

    Cheap version of sigma_ode_verify.py: one point at s=6, which took no
    part in the nullspace search (window was s in [1,4]).
    """
    from mpmath import mp
    import sigma_ode
    old = mp.dps
    try:
        mp.dps = 50
        s = mp.mpf(6)
        sig, sig1, sig2 = sigma_ode.sigma_data(s, 50)
        u = s * sig1 - sig
        t1 = s ** 2 * sig2 ** 2
        t2 = 16 * u ** 2
        t3 = 4 * u * sig1 ** 2
        rel = abs(t1 + t2 + t3) / max(abs(t1), abs(t2), abs(t3))
        assert rel < mp.mpf(10) ** -40, f"sigma ODE residual {mp.nstr(rel,5)}"
    finally:
        mp.dps = old


def test_recursion_parity_and_first_coefficient():
    """L-037: odd orders vanish and e_2 = 1/32 exactly, by derivation."""
    from fractions import Fraction as F
    import sigma_recursion_fast as SRF
    res = SRF.solve(12, verbose=False)
    got = dict(res)
    assert all(m % 2 == 0 for m in got), "odd order appeared in even-only solve"
    assert got[2] == F(-1, 16), f"a_2 = {got[2]}, expected -1/16"
    e2 = -got[2] / 2
    assert e2 == F(1, 32), f"e_2 = {e2}, expected 1/32 (settles IQ-2)"


def test_recursion_matches_certified_data():
    """L-038: derived coefficients must predict independent determinant data.

    Nothing in the recursion was fitted to certified_data.json, so this is a
    genuine out-of-sample prediction rather than a consistency check.
    """
    import json
    import os
    from fractions import Fraction as F
    from mpmath import mp
    if not os.path.exists("out/certified_data.json"):
        return  # verify builds this later; do not fail a from-nothing run
    import sigma_recursion_fast as SRF
    old = mp.dps
    try:
        mp.dps = 120
        coeffs = {m: v for m, v in SRF.solve(20, verbose=False)}
        rows = json.load(open("out/certified_data.json"))["rows"]
        r = max(rows, key=lambda q: mp.mpf(q["s"]))
        s = mp.mpf(r["s"])
        L = mp.mpf(r["value"])
        c = mp.log(2) / 12 + 3 * mp.zeta(-1, derivative=1)
        resid = L - (-s ** 2 / 2 - mp.log(s) / 4 + c)
        pred = mp.mpf(0)
        for m, a in coeffs.items():
            e = -a / m
            pred += (mp.mpf(e.numerator) / mp.mpf(e.denominator)) * s ** (-m)
        # 20 orders at s>=149 must explain the residual to well beyond 1e-30
        assert abs(resid - pred) < mp.mpf(10) ** -30, \
            f"tail prediction off by {mp.nstr(abs(resid - pred), 5)}"
    finally:
        mp.dps = old
