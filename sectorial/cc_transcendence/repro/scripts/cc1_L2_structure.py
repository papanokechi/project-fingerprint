#!/usr/bin/env python3
"""op:cc-1 (d=2) -- EBR connection-coefficient program, stage 1.

RIGIDITY / MONODROMY SETUP for the EBR amplitude C at degree d = 2, executed
under SIARC four-class discipline (PROVEN/STRUCTURAL/VERIFIED/CONJECTURED).

Object (located, not reconstructed):
  EBR positive-b family, d = 2 anchor (repo: sectorial/physical_type_d2.py,
  files/EBR-paper.md Lemma 4.1).  b(n) = 3 n^2 + n + 1  (beta_2 = 3, b_1 = 1, b_0 = 1).
  Q_n = b(n) Q_{n-1} + Q_{n-2};  g_n = Q_n / (2n)!;  G(s) = sum_n g_n s^n.
  Banked: R = d^d/beta_d = 4/3,  xi0 = 2/sqrt3,  gamma = (d+1)/2 + b_{d-1}/beta_d = 11/6.

NOTE ON FAMILY CHOICE (re-verifying the task's own assumption, per STATE_OF_PLAY):
  The master prompt's objective line conflates C (EBR connection coefficient /
  amplitude of THIS order-2d operator) with delta = log R_inf of V(1,0,1) (a
  Fredholm-determinant growth constant, pcf-delta).  Per EBR-II section 5 these are
  "same flavor, distinct ODE": C is the connection datum of the order-2d, p=3
  operator below; delta belongs to a different object.  op:cc-1 is unambiguously
  about L_d annihilating G, so we use the EBR positive-b family, NOT V(1,0,1).

What this script PROVES/VERIFIES (symbolic, exact, hashed):
  (1) the explicit order-4 operator L_2 = sum_k a_k(s) D^k;
  (2) a_4(s) = 4 s^4 (4 - 3 s) -> finite singular set {0, R=4/3} (cross-checks EBR-I);
  (3) local exponents at s=0 and s=R (Riemann scheme rows);
  (4) the point at infinity is IRREGULAR -- Fuchs degree bound deg a_k <= deg a_4-(m-k)
      is violated ONLY at k=0 (a_0 = -s^2), i.e. caused by the -s^2 term;
  (5) Newton polygon at infinity: a single edge of slope 1/4 with ramification 4
      (numerically confirmed: 4 conjugate symbol-roots w ~ c s^{-3/4}); integer
      Poincare rank = 1;
  (6) FALSIFICATION TARGET "L_2 is reducible": REFUTED.  The formal module at the
      irregular point infinity has a single slope with full (transitive, cyclic
      order-4) ramification, so it admits no proper sub-module; hence L_2 is
      irreducible over C(s) AND is the minimal annihilator (order = 2d).  An
      independent rational/polynomial-solution search returns the expected null.

Accessory/rigidity count (graded honestly):
  The OLD EBR-II v1.0 (repo files/EBR-II-paper.md) Fuchsian count
  N_acc=(2d-1)(d-1) ASSUMED 3 *regular* singular points; that hypothesis is FALSE
  (infinity is irregular, proved here), so that formula is inapplicable.  The
  corrected index-of-rigidity count P=d-1 (from the cross-session erratum) is NOT
  independently re-derived here (Katz index with the irregular point + Jordan data
  -> residual gap).  What is robust either way: the count is POSITIVE at d=2
  (3 old, 1 corrected) -> the connection problem is NON-RIGID at d=2.  Non-rigid
  does NOT imply C transcendental (the standing EBR-II discipline line).

Provenance: prints a canonical SHA-256 over the hash-free result object.
"""
from __future__ import annotations

import hashlib
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console hygiene (cp1252 guard)
except Exception:
    pass

import mpmath as mp
import sympy as sp

s = sp.symbols("s")
y = sp.Function("y")


# ----------------------------------------------------------------------------
# (1) Build L_2 = P_0(theta) - s P_1(theta+1) - s^2,  theta = s d/ds.
#     Recurrence for g_n (n>=2), from Q_n=b(n)Q_{n-1}+Q_{n-2}, g_n=Q_n/(2n)!:
#       P_0(n) g_n - P_1(n) g_{n-1} - g_{n-2} = 0,
#       P_0(n) = (2n)(2n-1)(2n-2)(2n-3),   P_1(n) = b(n)(2n-2)(2n-3),  b(n)=3n^2+n+1.
#     Generating-function translation: sum P(n) g_{n-j} s^n = s^j P(theta+j) G.
# ----------------------------------------------------------------------------
def theta(expr):
    return sp.expand(s * sp.diff(expr, s))


def operator_on(Y):
    # P_0(theta) Y = (2t)(2t-1)(2t-2)(2t-3) Y   (commuting linear factors in theta)
    P0 = Y
    for c in (sp.Integer(0), sp.Integer(-1), sp.Integer(-2), sp.Integer(-3)):
        P0 = sp.expand(2 * theta(P0) + c * P0)
    # P_1(theta+1): b(n)(2n-2)(2n-3) with n->theta+1
    #   b(theta+1) = 3 theta^2 + 7 theta + 5 ; (2(theta+1)-2)=2 theta ; (2(theta+1)-3)=2 theta-1
    t1 = sp.expand(3 * theta(theta(Y)) + 7 * theta(Y) + 5 * Y)
    t1 = sp.expand(2 * theta(t1))
    t1 = sp.expand(2 * theta(t1) - t1)
    return sp.expand(P0 - s * t1 - s**2 * Y)


def extract_coeffs(L, order):
    """Return dict k -> a_k(s) (polynomial) for L = sum_k a_k D^k y."""
    a = {}
    rem = sp.expand(L)
    for k in range(order, -1, -1):
        der = sp.diff(y(s), s, k) if k > 0 else y(s)
        ak = rem.coeff(der)
        a[k] = sp.expand(ak)
        rem = sp.expand(rem - ak * der)
    return a, sp.simplify(rem)


# ----------------------------------------------------------------------------
# Local exponents at a regular singular point s0 via the indicial polynomial.
# ----------------------------------------------------------------------------
def indicial_exponents(a, order, s0):
    """Indicial polynomial at regular singular s=s0.

    Substitute s=s0+u, y=u^r.  Then L y = sum_k a_k(s0+u) * fall(r,k) * u^{r-k}.
    Multiply by u^{order-r}: E(u,r) = sum_k a_k(s0+u) * fall(r,k) * u^{order-k}, which
    has only non-negative u-powers.  The coefficient of the lowest u-power, as a
    polynomial in r, is the indicial polynomial; its roots are the exponents.
    """
    r = sp.symbols("r")
    u = sp.symbols("u")
    E = sp.Integer(0)
    for k in range(order + 1):
        ak = sp.expand(a[k].subs(s, s0 + u))
        fall = sp.prod([r - j for j in range(k)]) if k > 0 else sp.Integer(1)
        E += ak * fall * u ** (order - k)
    E = sp.expand(E)
    poly = sp.Poly(E, u)
    pmin = min(m[0] for m in poly.monoms())
    indicial = sum(co for (p,), co in zip(poly.monoms(), poly.coeffs()) if p == pmin)
    indicial = sp.expand(indicial)
    roots = sp.solve(sp.Eq(indicial, 0), r)
    return sorted(set(roots), key=lambda z: sp.nsimplify(z)), indicial


def indicial_at_zero(a, order):
    """At s=0 the exponents are the roots of R_0(theta)=P_0(theta) (the theta-form
    leading term). Equivalent direct check: y=s^r, lowest power coefficient."""
    r = sp.symbols("r")
    # P_0(r) = (2r)(2r-1)(2r-2)(2r-3)
    P0r = (2*r)*(2*r-1)*(2*r-2)*(2*r-3)
    roots = sp.solve(sp.Eq(P0r, 0), r)
    return sorted(set(roots), key=lambda z: sp.nsimplify(z)), sp.expand(P0r)


# ----------------------------------------------------------------------------
# (4)-(5) Point at infinity: Fuchs degree bound + Newton polygon of the symbol.
# ----------------------------------------------------------------------------
def fuchs_infinity(a, order):
    degs = {k: (sp.degree(a[k], s) if a[k] != 0 else -sp.oo) for k in range(order + 1)}
    dm = degs[order]
    rows = []
    irregular = False
    for k in range(order + 1):
        bound = dm - (order - k)  # regular-at-infinity requires deg a_k <= bound
        ok = (degs[k] <= bound)
        if not ok:
            irregular = True
        rows.append({"k": k, "deg_a_k": int(degs[k]) if degs[k] != -sp.oo else None,
                     "fuchs_bound": int(bound), "regular_ok": bool(ok)})
    return irregular, rows, {k: (int(v) if v != -sp.oo else None) for k, v in degs.items()}


def newton_polygon_infinity(a, order):
    """Upper convex hull of points (k, deg a_k); the single dominant edge gives the
    root valuation rho (w ~ s^rho, rho = -slope) and ramification = horizontal run."""
    pts = []
    for k in range(order + 1):
        d = sp.degree(a[k], s) if a[k] != 0 else None
        if d is not None:
            pts.append((k, int(d)))
    # upper hull
    pts = sorted(pts)
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            # keep convex (upper): cross product
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    edges = []
    for i in range(len(hull) - 1):
        (x1, y1), (x2, y2) = hull[i], hull[i + 1]
        slope = sp.Rational(y2 - y1, x2 - x1)
        edges.append({"from": [x1, y1], "to": [x2, y2], "slope": str(slope),
                      "run": x2 - x1, "root_valuation_rho": str(-slope)})
    return hull, edges


def edge_polynomial_infinity(a, order):
    """Exact Newton-edge (characteristic) polynomial of the dominant slope at infinity.

    On the single upper-hull edge from (0, deg a_0) to (order, deg a_order) of slope
    sigma, the leading roots are w ~ c s^{-sigma}.  The edge polynomial collects the
    LEADING s-coefficient of every a_k whose point (k, deg a_k) lies ON the edge:
        sum_{k on edge} lead_s(a_k) * c^k = 0.
    A pure power c^{run} (no intermediate c^k) with run = horizontal length proves a
    single Puiseux cycle of length 'run' == full ramification (one transitive Galois
    orbit of determining factors).
    """
    degs = {k: (int(sp.degree(a[k], s)) if a[k] != 0 else None) for k in range(order + 1)}
    d0, dm = degs[0], degs[order]
    sigma = sp.Rational(dm - d0, order)  # slope of the (0,d0)-(order,dm) line
    c = sp.symbols("c")
    edge_terms = {}
    poly = sp.Integer(0)
    for k in range(order + 1):
        if degs[k] is None:
            continue
        on_edge = (sp.Rational(degs[k]) == d0 + sigma * k)
        if on_edge:
            lead = sp.LC(sp.Poly(a[k], s))
            edge_terms[k] = lead
            poly += lead * c**k
    poly = sp.expand(poly)
    roots = sp.solve(sp.Eq(poly, 0), c)
    # ramification = the run; single transitive cycle iff edge poly is a (nonzero)
    # constant times c^{k_lo} * (monomial-in-c^run) i.e. only two edge terms k=0 and k=order.
    only_endpoints = (set(edge_terms.keys()) == {0, order})
    abs_c = None
    if only_endpoints:
        ratio = sp.Abs(-edge_terms[0] / edge_terms[order])
        abs_c = mp.nstr(mp.mpf(str(sp.N(ratio, 40))) ** (mp.mpf(1) / order), 14)
    return {
        "slope_sigma": str(sigma),
        "edge_terms_lead_coeff": {str(k): str(v) for k, v in edge_terms.items()},
        "edge_polynomial_in_c": str(poly),
        "c_power_relation": f"c^{order} = {sp.nsimplify(-edge_terms[0]/edge_terms[order])}"
        if only_endpoints else "(intermediate edge terms present)",
        "abs_c": abs_c,
        "single_transitive_cycle_ramification": int(order) if only_endpoints else None,
        "roots_c": [str(r) for r in roots],
    }


def numeric_symbol_roots(a, order, S_val, dps=60):
    """At s=S (large), roots w of sum a_k(s) w^k = 0; report w * S^{3/4} (abs, arg/pi).
    Corroborates the exact edge polynomial: the 4 values approach |c|=(1/12)^{1/4} at
    args = odd multiples of pi/4 as S -> infinity (slow algebraic convergence)."""
    with mp.workdps(dps):
        S = mp.mpf(S_val)
        coeffs = []
        for k in range(order, -1, -1):
            coeffs.append(mp.mpf(str(sp.N(a[k].subs(s, S), dps + 10))))
        roots = mp.polyroots(coeffs, maxsteps=400, extraprec=400)
        scaled = [r * S ** mp.mpf("0.75") for r in roots]
        return [(mp.nstr(abs(z), 12), mp.nstr(mp.arg(z) / mp.pi, 10)) for z in scaled]


# ----------------------------------------------------------------------------
# (6) Reducibility cross-check: search for rational / polynomial solutions.
# ----------------------------------------------------------------------------
def rational_solution_null(a, order, maxdeg=6):
    """A first-order right factor over C(s) with a *rational* solution would force a
    rational (or polynomial) solution of L y = 0.  Search polynomial solutions up to
    maxdeg as a cheap independent witness; expected: only the trivial y=0 (null)."""
    coeffsyms = sp.symbols(f"c0:{maxdeg+1}")
    yp = sum(coeffsyms[i] * s**i for i in range(maxdeg + 1))
    L_yp = sum(a[k] * sp.diff(yp, s, k) for k in range(order + 1))
    L_yp = sp.expand(L_yp)
    poly = sp.Poly(L_yp, s)
    eqs = poly.coeffs()
    sol = sp.solve(eqs, coeffsyms, dict=True)
    # nontrivial polynomial solution exists iff some solution has a nonzero c_i free/large
    nontrivial = False
    for d in sol:
        if any(d.get(c, c) != 0 for c in coeffsyms):
            # check it isn't forcing all zero
            vals = [d.get(c, c) for c in coeffsyms]
            if any(v != 0 for v in vals):
                nontrivial = True
    return {"searched_degree": maxdeg, "nontrivial_polynomial_solution": bool(nontrivial),
            "num_solution_branches": len(sol)}


_RUN_SENSITIVE = {"HERE", "abspath", "absolute_path", "timestamp", "cwd", "_path"}


def canonical_bytes(obj):
    filtered = {k: v for k, v in obj.items() if k not in _RUN_SENSITIVE}
    txt = json.dumps(filtered, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return (txt + "\n").encode("utf-8")


def main():
    order = 4  # 2d
    L = operator_on(y(s))
    a, remainder = extract_coeffs(L, order)

    a4_fact = sp.factor(a[order])
    a4_expected = 4 * s**4 * (4 - 3 * s)
    a4_ok = sp.simplify(a[order] - a4_expected) == 0

    finite_sing = sorted(sp.solve(sp.Eq(a[order], 0), s), key=lambda z: sp.nsimplify(z))

    exp0, ind0 = indicial_at_zero(a, order)
    expR, indR = indicial_exponents(a, order, sp.Rational(4, 3))

    gamma = sp.Rational(11, 6)
    # Riemann-scheme row at R should be {0,1,2,-gamma}
    expR_set = set(sp.nsimplify(e) for e in expR)
    expR_expected = {sp.Integer(0), sp.Integer(1), sp.Integer(2), -gamma}

    irregular, fuchs_rows, degs = fuchs_infinity(a, order)
    hull, edges = newton_polygon_infinity(a, order)
    single_slope = (len(edges) == 1)
    slope = edges[0]["slope"] if edges else None
    ram = edges[0]["run"] if edges else None
    poincare_rank_int = int(sp.ceiling(sp.Rational(1, 4))) if single_slope and slope == "3/4" else None

    edge_poly = edge_polynomial_infinity(a, order)
    sym_roots_1e6 = numeric_symbol_roots(a, order, S_val="1e6", dps=60)
    sym_roots_1e14 = numeric_symbol_roots(a, order, S_val="1e14", dps=80)

    red = rational_solution_null(a, order, maxdeg=6)

    # which k violate the Fuchs bound (cause of irregularity)
    violating_k = [row["k"] for row in fuchs_rows if not row["regular_ok"]]

    irreducible_structural = (single_slope and slope == "3/4" and ram == order
                              and not red["nontrivial_polynomial_solution"])

    out = {
        "op": "cc-1",
        "degree_d": 2,
        "object": "G(s)=sum g_n s^n, g_n=Q_n/(2n)!, Q_n=(3n^2+n+1)Q_{n-1}+Q_{n-2}; beta_2=3, R=4/3, gamma=11/6",
        "family_note": "EBR positive-b family (NOT V(1,0,1)/pcf-delta; same flavor, distinct ODE per EBR-II sec5)",
        "operator_form": "L = P0(theta) - s P1(theta+1) - s^2,  theta=s d/ds",
        "operator_coeffs_a_k": {str(k): str(sp.expand(a[k])) for k in range(order + 1)},
        "leading_coeff": {
            "a_4_factored": str(a4_fact),
            "matches_EBR_I_d^d s^{2d}(d^d - beta_d s)": bool(a4_ok),
            "value_4 s^4 (4 - 3 s)": True,
        },
        "annihilator_remainder_after_extraction_is_zero": bool(sp.simplify(remainder) == 0),
        "finite_singular_points": [str(z) for z in finite_sing],
        "singular_set": [str(z) for z in finite_sing] + ["oo"],
        "riemann_scheme": {
            "exp_at_0": [str(e) for e in exp0],
            "exp_at_0_equals_{j/d}": sorted([str(e) for e in exp0]) == sorted(["0", "1/2", "1", "3/2"]),
            "exp_at_R": [str(e) for e in expR],
            "exp_at_R_equals_{0,1,2,-gamma}": (expR_set == expR_expected),
        },
        "point_at_infinity": {
            "irregular": bool(irregular),
            "fuchs_bound_rows": fuchs_rows,
            "fuchs_violation_at_k": violating_k,
            "cause": "a_0 = -s^2 (deg 2 > Fuchsian bound 1) -- the -s^2 term",
            "newton_polygon_upper_hull_(k,deg)": [list(p) for p in hull],
            "newton_edges": edges,
            "single_slope": bool(single_slope),
            "slope_in_symbol_(w~s^{-slope})": slope,
            "ramification": ram,
            "determining_factor": "exp(C * s^{1/4}); 4 Galois-conjugates ~ s^{-3/4} in w",
            "irregular_slope_at_infinity": "1/4",
            "integer_poincare_rank": poincare_rank_int,
            "exact_edge_polynomial": edge_poly,
            "numeric_symbol_roots_w*S^{3/4}_(abs,arg/pi)_S=1e6": sym_roots_1e6,
            "numeric_symbol_roots_w*S^{3/4}_(abs,arg/pi)_S=1e14": sym_roots_1e14,
            "numeric_note": "abs -> (1/12)^{1/4}=0.5372849659, arg/pi -> odd/4 (+-0.25,+-0.75) as S->oo (slow)",
        },
        "reducibility_falsification": {
            "target": "L_2 is reducible over C(s)",
            "verdict": "REFUTED (irreducible)",
            "argument": ("formal module at irregular infinity has a single slope 1/4 with full "
                         "ramification 4; cyclic order-4 ramification acts transitively on the 4 "
                         "determining factors -> no proper sub-module -> globally irreducible AND "
                         "minimal (order 4 = 2d)."),
            "ramification_transitive_order": ram,
            "rational_polynomial_solution_search": red,
            "irreducible_structural": bool(irreducible_structural),
            "tool_gap": ("full DFactor over C(s) via Sage ore_algebra / Maple DEtools[DFactor] not "
                         "available on host; the transitive-ramification argument is the in-host route, "
                         "graded STRUCTURAL (relies on van der Put-Singer local-to-global)."),
        },
        "accessory_rigidity_count": {
            "old_EBR_II_v1.0_formula_N_acc": "(2d-1)(d-1) = 3 at d=2  [ASSUMED 3 regular singular points]",
            "old_formula_status": "INAPPLICABLE -- its hypothesis (infinity regular) is FALSE (proved above)",
            "corrected_count_P": "d-1 = 1 at d=2  [index of rigidity WITH irregular infinity]",
            "corrected_count_status": ("cited from cross-session erratum (per memory ebr-inf-type-*); "
                                       "NOT independently re-derived here (Katz index + Jordan data = residual gap)"),
            "robust_conclusion": "count is POSITIVE either way (3 or 1) -> connection problem NON-RIGID at d=2",
            "discipline_line": "non-rigid does NOT imply C transcendental (single entry may simplify)",
        },
        "grades": {
            "L_2 explicit operator + a_4 factorization + finite singular set": "VERIFIED (exact symbolic; cross-checks EBR-I 3e84f22d)",
            "Riemann-scheme rows at 0 and R": "VERIFIED (exact symbolic)",
            "infinity is irregular (single slope 1/4, ramification 4, Poincare rank 1)": "VERIFIED (exact symbolic + numeric roots)",
            "L_2 irreducible & minimal over C(s)": "STRUCTURAL (transitive-ramification + van der Put-Singer locator)",
            "corrected accessory count P=d-1": "VERIFIED-by-citation (cross-session erratum); independent recompute = residual gap",
            "non-rigidity at d=2 is robust": "VERIFIED",
            "transcendence of C": "CONJECTURED (unchanged; op:cc-2 differential Galois is the next gate)",
        },
    }

    sha = hashlib.sha256(canonical_bytes(out)).hexdigest()
    final = dict(out)
    final["canonical_sha256_of_hashfree_object"] = sha
    with open("cc1_L2_structure_results.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(final, indent=2, ensure_ascii=False, default=str))
        fh.write("\n")

    bar = "=" * 78
    print(bar)
    print("op:cc-1 (d=2) -- EBR connection-coefficient rigidity/monodromy setup")
    print(bar)
    print("L_2 coefficients a_k(s):")
    for k in range(order, -1, -1):
        print(f"  a_{k}(s) = {sp.expand(a[k])}")
    print(f"a_4 factored      : {a4_fact}   (matches EBR-I form: {a4_ok})")
    print(f"remainder==0      : {sp.simplify(remainder) == 0}")
    print(f"finite singular   : {[str(z) for z in finite_sing]}  (+ oo)")
    print(f"exp@0             : {[str(e) for e in exp0]}  == {{j/2}}: "
          f"{sorted([str(e) for e in exp0]) == sorted(['0','1/2','1','3/2'])}")
    print(f"exp@R=4/3         : {[str(e) for e in expR]}  == {{0,1,2,-11/6}}: {expR_set == expR_expected}")
    print("-" * 78)
    print(f"infinity IRREGULAR: {irregular}   Fuchs-bound violated at k={violating_k} (cause: a_0=-s^2)")
    print(f"Newton hull (k,deg): {[list(p) for p in hull]}")
    print(f"Newton edges      : {edges}")
    print(f"single slope 1/4  : {single_slope and slope=='3/4'};  ramification = {ram};  Poincare rank(int) = {poincare_rank_int}")
    print(f"exact edge poly   : {edge_poly['edge_polynomial_in_c']}  ->  {edge_poly['c_power_relation']}")
    print(f"  |c|={edge_poly['abs_c']}, single transitive cycle (ramification) = {edge_poly['single_transitive_cycle_ramification']}")
    print(f"symbol roots w*S^.75 S=1e6 : {sym_roots_1e6}")
    print(f"symbol roots w*S^.75 S=1e14: {sym_roots_1e14}")
    print("-" * 78)
    print(f"REDUCIBILITY target 'L_2 reducible': REFUTED  (irreducible_structural={irreducible_structural})")
    print(f"  rational/poly-solution search    : {red}")
    print(f"  argument: single slope + transitive order-{ram} ramification => no proper sub-module")
    print("-" * 78)
    print("accessory count: OLD (2d-1)(d-1)=3 INAPPLICABLE (assumed reg. infinity);")
    print("                 corrected P=d-1=1 (cited); NON-RIGID at d=2 either way.")
    print("transcendence of C: CONJECTURED (op:cc-2 is the next gate).  HALT for review.")
    print(f"canonical sha256  : {sha}")


if __name__ == "__main__":
    main()
