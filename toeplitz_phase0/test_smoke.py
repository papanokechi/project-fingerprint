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
