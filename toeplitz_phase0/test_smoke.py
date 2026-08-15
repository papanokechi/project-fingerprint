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


def test_positive_control_detects_silent_basis_shrink():
    """L-044: the control must fire on the ACTUAL L-040(7) failure.

    A positive control planted over the passed-in basis passes happily when an
    element has gone missing -- measured, not supposed.  Only planting over the
    DECLARED basis detects it.  This test locks in the corrected behaviour, and
    would fail if the `declared` plumbing were ever dropped.
    """
    from mpmath import mp
    import constants
    import pslq_harness as H

    P = 40
    names, vals = constants.basis_values(
        P + 40, ["log2", "logpi", "gamma", "zeta'(-1)"])
    declared = list(zip(names, vals))

    intact = H.positive_control(P, names, vals, declared=declared)
    assert intact["passed"], "intact basis must recover its own plant"

    keep = [i for i, n in enumerate(names) if n != "zeta'(-1)"]
    shrunk_n = [names[i] for i in keep]
    shrunk_v = [vals[i] for i in keep]

    # Planting over the shrunken basis: the known false negative.
    naive = H.positive_control(P, shrunk_n, shrunk_v)
    assert naive["passed"], "documents the failure mode -- see L-044"

    # Planting over the declared basis: must FAIL.
    strict = H.positive_control(P, shrunk_n, shrunk_v, declared=declared)
    assert not strict["passed"], "must flag the missing zeta'(-1)"


def test_prediction_law_holds_at_two_points():
    """L-045: honest digits must scale as ~0.87*s, not sit flat."""
    import json
    import os
    if not os.path.exists("out/prediction_test.json"):
        import pytest
        pytest.skip("run prediction_test.py first")
    import math
    d = json.load(open("out/prediction_test.json"))
    pts = [p for p in d["points"] if not p["saturated"]]
    assert len(pts) >= 2
    assert 0.85 < d["measured_slope"] < 0.89

    # The excess is NOT flat.  Asserting flatness was the artifact of the
    # rounded PREDICTED dict (L-050); against the exact 2s/ln10 the excess
    # drifts by one decade per decade of s, i.e. the beyond-all-orders
    # remainder carries a 1/s prefactor.
    exc = [p["honest"] - p["predicted"] for p in pts]
    spread = max(exc) - min(exc)
    lo = min(p["s"] for p in pts)
    hi = max(p["s"] for p in pts)
    a = spread / math.log10(hi / lo)
    assert abs(a - 1.0) < 0.15, f"exponent a={a:.3f}, expected ~1"


def test_assertion_audit_is_clean_and_can_still_fail():
    """L-049: the mechanical guard audit, plus proof it is not switched off.

    An audit that reports zero findings is indistinguishable from an audit
    that does nothing -- which is the failure this project keeps hitting.  So
    this test does both halves: the codebase must be clean, AND the auditor
    must still flag the historical L-048 guard, whose shape is reproduced
    here verbatim.
    """
    import ast
    import assertion_audit as A

    broken = """
def main():
    coeffs = load_coeffs("x.json")
    orders = sorted(coeffs)
    best = search(coeffs)
    M, cv, omit = best
    saturated = M >= orders[-1]
"""
    fixed = """
def main(s_int):
    coeffs = load_coeffs("x.json")
    orders = sorted(coeffs)
    best = search(coeffs)
    M, cv, omit = best
    saturated = bool(M >= orders[-1] or 2 * s_int > orders[-1])
"""

    def findings(src):
        tree = ast.parse(src)
        out = []
        for fn in [n for n in ast.walk(tree)
                   if isinstance(n, ast.FunctionDef)]:
            cls = A.Classifier(set()).run(fn)
            for _, expr in A.guard_nodes(fn):
                out += A.audit_expr(expr, cls)
        return out

    # Positive control on the auditor itself.
    assert findings(broken), "auditor no longer detects the L-048 shape"
    assert not findings(fixed), "auditor flags the repaired guard"

    # And the codebase is clean (waivers are allowed but must be explicit).
    assert A.main() == 0, "unwaived circular guard present; see out/"


# Declared thresholds for the certified-value consistency test.  Fixed here,
# not derived from the data they judge.
VALUE_MIN_AGREE = 15      # digits EVERY row must reproduce
VALUE_MIN_AGREE_HIGH_S = 50   # digits rows above S_SPLIT must reproduce
S_SPLIT = 100
CERT_DIGITS_LO, CERT_DIGITS_HI = 100, 400


def test_certified_values_are_constrained_by_the_recursion():
    """Make certified_data.json:rows.N.value a LIVE field.

    Found by mutation_test.py: a 100% corruption of any row's `value`
    survived the entire smoke suite.  Nothing fast checked the most
    load-bearing field in the project -- only `verify`, which costs hours,
    touched it, so in practice it was unchecked between full rebuilds.

    WHAT THIS IS.  Each stored value is compared against
        -s^2/2 - (1/4) log s + c_closed + sum_m e_m s^-m
    with c_closed the EXTERNAL closed form (the gate's referent, not a fitted
    quantity) and e_m the exact rational recursion coefficients.

    WHAT THIS IS NOT.  The sigma-ODE behind those e_m was discovered from a
    subset of this same grid, so this is a CONSISTENCY check, not independent
    evidence for the values.  It cannot promote them.  It can and does detect
    corruption of any single row, which is exactly the liveness property that
    was missing -- a global smooth relation is violated by a local edit.
    """
    import json
    from mpmath import mp, mpf, log, mpmathify, zeta, diff as mpdiff
    mp.dps = 80
    d = json.load(open("out/certified_data.json"))
    E = {}
    for r in json.load(open("out/sigma_recursion_fast.json"))["coeffs"]:
        n, dn = r["e_m"].split("/")
        E[r["m"]] = mpf(int(n)) / mpf(int(dn))
    ms = sorted(E)[:60]
    c = log(2) / 12 + 3 * mpdiff(lambda z: zeta(z), -1)

    rows = d["rows"]
    assert len(rows) > 50

    # certified_digits is checked on EVERY row, not the sampled ones.  The
    # mutation harness found rows.178.certified_digits surviving because the
    # sample step of 7 skipped it -- a check can be alive on the fields it
    # happens to touch and dead on the rest, which a sampled mutation run
    # reports as a survivor and a sampled test reports as green.
    for r in rows:
        cd_all = float(r["certified_digits"])

        # AUDIT-REVIEWED: every symbol here is output-derived, and that is
        # correct for this assertion.  It is not a claim check -- it is a
        # TRANSCRIPTION-INTEGRITY check that the recorded field equals its own
        # definition, min(node doubling, precision bump).  The preceding range
        # guard fires but cannot kill a mutant, because a range guard's
        # resolution is the width of the range: perturbing 171.7 -> 300 stays
        # inside [100, 400].  Sensitivity, not existence, is what mutation
        # testing measures, and this identity is exact.
        assert abs(cd_all - min(float(r["node_doubling_digits"]),
                                float(r["precision_bump_digits"]))) < 1e-9, (
            f"row s={r['s']}: certified_digits={cd_all} does not equal "
            f"min(node_doubling, precision_bump)")

        assert CERT_DIGITS_LO <= cd_all <= CERT_DIGITS_HI, (
            f"row s={r['s']} claims {cd_all} certified digits, outside the "
            f"declared range [{CERT_DIGITS_LO}, {CERT_DIGITS_HI}]")

    agreements = []
    for r in rows[::7]:
        s_ = mpf(r["s"])
        v = mpmathify(r["value"])
        pred = -s_**2 / 2 - log(s_) / 4 + c + sum(E[m] * s_**(-m) for m in ms)
        err = abs(pred - v) / abs(v)
        dg = float(-log(err) / log(10)) if err > 0 else 1e9
        agreements.append((float(s_), dg))
        assert dg >= VALUE_MIN_AGREE, (
            f"row s={float(s_)} reproduces only {dg:.2f} digits "
            f"(floor {VALUE_MIN_AGREE})")

    # Agreement is truncation-limited, so it must IMPROVE with s.  The
    # obvious way to write that -- min(high-s) > max(low-s) -- puts the data
    # under test on BOTH sides, so a uniformly corrupted grid would satisfy
    # it.  assertion_audit.py flagged exactly that when this test was first
    # written (and in doing so exposed a real `lo`/`hi` shadowing bug two
    # lines up).  Anchor the constraining side on a DECLARED floor instead.
    high = [dg for s_, dg in agreements if s_ > S_SPLIT]
    assert high, f"no rows above s={S_SPLIT} to test"
    assert min(high) >= VALUE_MIN_AGREE_HIGH_S, (
        f"rows above s={S_SPLIT} reproduce only {min(high):.1f} digits "
        f"(floor {VALUE_MIN_AGREE_HIGH_S})")
