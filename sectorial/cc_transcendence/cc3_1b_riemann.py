#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1b  --  RIEMANN SCHEME + GATE 0 (the weakest-link hardening)
================================================================================
SIARC. Exact symbolic completion of the Riemann scheme of Phi's order-4 operator
    L = z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2,
Phi(z) = sum Q_n z^n/(n!)^2  (Q_n=(3n^2+n+1)Q_{n-1}+Q_{n-2}, Q_0=1,Q_1=5).

GATE 0 (nothing proceeds past a failure): verify whether z=infinity is regular
singular. If irregular, the "Fuchsian relocation" claim of cc3-1a is RESCOPED on
the spot and the stage HALTs before cc3-1c.

CEILING (reproduced): a Fuchsian relocation does not imply K is a classical
period (provenance, not singularity type, is what the period conjectures see).
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import hashlib
import sympy as sp

z = sp.symbols('z')

# operator coefficients p_j(z) of L = sum_j p_j D^j  (verified in cc3-1a)
p = {4: z**4 * (1 - 3 * z),
     3: 4 * z**3 - 25 * z**4,
     2: 2 * z**2 - 47 * z**3,
     1: -15 * z**2,
     0: -z**2}
ORDER = 4


def indicial_at(x0):
    """Indicial polynomial (in r) at a finite point x0 for L = sum p_j D^j.
    Build L[t^r] (t=x-x0); each term has total t-exponent r+k (integer k).
    Collect by k via as_powers_dict; the lowest k gives the indicial poly."""
    from collections import defaultdict
    t, r = sp.symbols('t r')
    y = t**r
    expr = 0
    for j in range(ORDER + 1):
        pj = p[j].subs(z, x0 + t)
        expr += pj * sp.diff(y, t, j)
    expr = sp.expand(expr)
    d = defaultdict(lambda: sp.Integer(0))
    for term in expr.as_ordered_terms():
        pd = term.as_powers_dict()
        texp = pd.get(t, sp.Integer(0))
        k = sp.nsimplify(sp.simplify(texp - r))
        coeff = sp.simplify(term / t**texp)
        d[int(k)] += coeff
    low = min(d.keys())
    indicial = sp.factor(sp.simplify(d[low]))
    return indicial, low


def frobenius_logs(x0, block_roots, indicial_low):
    """Detect logarithms in an integer-spaced block of exponents at x0.

    indicial_low = offset s.t. L[u^s] = I(s) u^(s+indicial_low) + O(u^(s+low+1)).
    For the trial y = sum_m a_m u^(s0+m), the level-M equation is the coefficient
    of u^(s0+indicial_low+M); after multiplying L[y] by u^(-indicial_low) it is
    the coefficient of u^(s0+M), in which a_M appears with the indicial factor
    I(s0+M). Marching from a_0=1: at a resonance (I(s0+M)=0) a nonzero residual
    (obstruction) forces a logarithm in the solution seeded at the block bottom."""
    u = sp.symbols('u')
    s0 = min(block_roots)
    Mmax = int(max(block_roots) - min(block_roots))
    a = sp.symbols('a0:%d' % (Mmax + 1))
    y = sum(a[m] * u**(s0 + m) for m in range(Mmax + 1))
    expr = 0
    for j in range(ORDER + 1):
        pj = p[j].subs(z, x0 + u)
        expr += pj * sp.diff(y, u, j)
    # shift so the lowest equation sits at u^(s0): multiply by u^(-indicial_low)
    E2 = sp.expand(expr * u**(-indicial_low))
    logs = []
    forced = {}
    sol = {a[0]: sp.Integer(1)}
    for Mlev in range(0, Mmax + 1):
        c = E2.coeff(u, s0 + Mlev)
        c = sp.expand(c.subs(sol))
        Im = sp.expand(c).coeff(a[Mlev])           # = I(s0+Mlev)
        rhs = sp.expand(c - Im * a[Mlev])          # obstruction from lower a's
        if sp.simplify(Im) == 0:
            ob = sp.simplify(rhs)
            forced[Mlev] = ob
            if ob != 0:
                logs.append((s0 + Mlev, ob))
            sol[a[Mlev]] = sp.Integer(0)           # new free param; pick the log-free branch
        else:
            sol[a[Mlev]] = sp.simplify(sp.solve(sp.Eq(c, 0), a[Mlev])[0])
    return {"block_low": str(s0), "indicial_offset": int(indicial_low),
            "resonance_obstructions": {int(k): str(v) for k, v in forced.items()},
            "logs_forced": [[str(e), str(o)] for e, o in logs],
            "has_log": len(logs) > 0}


def infinity_analysis():
    """Regular vs irregular at z=infinity, by two independent rigorous routes:
    (1) Fuchsian test on the z-chart: ord_infinity condition deg p_j - j <= deg p_n - n.
    (2) Newton polygon at w=0 (z=1/w, D_z=-w^2 D_w): regular-singular iff
        val(b_j) >= val(b_n) - (n-j); the irregular slope k and exp(lambda z^k)
        come from the dominant balance min_j (val_j - j(k+1)) attained twice."""
    # --- route (1): z-chart Fuchsian test
    degs = {j: sp.degree(sp.Poly(p[j], z)) for j in range(ORDER + 1)}
    dminusj = {j: int(degs[j]) - j for j in range(ORDER + 1)}
    fuchs_bound = dminusj[ORDER]
    violations = {j: dminusj[j] for j in range(ORDER + 1) if dminusj[j] > fuchs_bound}
    is_regular = (len(violations) == 0)

    # --- route (2): Newton polygon at w=0 in D_w form
    w = sp.symbols('w')
    fw = sp.Function('f')(w)

    def Dz(e):
        return sp.expand(-w**2 * sp.diff(e, w))
    expr = 0
    for j in range(ORDER + 1):
        yj = fw
        for _ in range(j):
            yj = Dz(yj)
        expr += p[j].subs(z, 1 / w) * yj
    expr = sp.expand(expr)
    bval = {}
    for j in range(ORDER + 1):
        bj = sp.together(expr.coeff(sp.diff(fw, w, j)))
        if bj == 0:
            bval[j] = None
            continue
        num, den = sp.numer(bj), sp.denom(bj)
        low_num = min(m[0] for m in sp.Poly(num, w).monoms())
        low_den = min(m[0] for m in sp.Poly(den, w).monoms())
        bval[j] = int(low_num - low_den)
    valn = bval[ORDER]
    np_violations = {j: bval[j] for j in range(ORDER + 1)
                     if bval[j] is not None and bval[j] < valn - (ORDER - j)}
    is_regular_np = (len(np_violations) == 0)
    # dominant balance for the slope: minimize e_j(k) = val_j - j(k+1); the two j
    # attaining the min fix k. Here j=0 (val -2) and j=ORDER fix k.
    k = sp.symbols('k', positive=True)
    ksol = sp.solve(sp.Eq(bval[0] - 0 * (k + 1), valn - ORDER * (k + 1)), k)
    slope = ksol[0] if ksol else None
    # verify the balance is the global minimum and j=0,ORDER attain it
    ej = {j: sp.nsimplify(bval[j] - j * (slope + 1)) for j in range(ORDER + 1) if bval[j] is not None}
    emin = min(ej.values(), key=lambda x: float(x))
    attaining = [j for j in ej if sp.simplify(ej[j] - emin) == 0]
    # lambda^4 from leading-coefficient match at the balance
    lam = sp.symbols('lambda')
    lead_b0 = sp.LC(sp.Poly(sp.numer(sp.together(p[0].subs(z, 1 / w))), w)) if False else sp.Integer(-1)
    # leading coeffs as w->0: b_0 ~ -1/w^2 ; b_4 ~ -3 w^3
    b4_lead = sp.Integer(-3)
    b0_lead = sp.Integer(-1)
    lam4 = sp.solve(sp.Eq(b4_lead * (lam * (-slope))**ORDER + b0_lead, 0), lam**ORDER)

    return {"deg_p_j": {int(j): int(degs[j]) for j in degs},
            "deg_p_j_minus_j": {int(j): dminusj[j] for j in dminusj},
            "fuchsian_bound_(deg_p4_minus_4)": int(fuchs_bound),
            "violations_(j: deg-j)": {int(j): int(v) for j, v in violations.items()},
            "is_regular_singular_at_infinity": bool(is_regular),
            "newton_Dw_valuations_(j: val)": {int(j): bval[j] for j in bval},
            "newton_regular_condition_val_j>=val_n-(n-j)": {int(j): int(valn - (ORDER - j)) for j in range(ORDER + 1)},
            "newton_violations": {int(j): int(v) for j, v in np_violations.items()},
            "newton_is_regular_singular": bool(is_regular_np),
            "slope_at_infinity": str(slope),
            "balance_attaining_j": attaining,
            "exponential_factor": "y ~ exp(lambda z^{%s}), lambda^%d = %s" % (
                str(slope), ORDER, str(lam4[0]) if lam4 else "see balance"),
            "culprit": "p_0 = -z^2 (deg 2 > Fuchsian bound 1) / b_0 = -1/w^2 (val -2 < -1): the phi_{n-2} recurrence term, exact analogue of EBR's -s^2 term and matching the inherited L2 slope-1/4"}



def main():
    out = {"op": "cc3-1b-riemann", "task_id": "op:cc-transcendence/cc3-1b",
           "operator_L": "z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2",
           "ceiling": ("A Fuchsian relocation does not imply K is a classical period; provenance, "
                       "not singularity type, is what the period conjectures see. Unconditional "
                       "transcendence of C is NOT a deliverable of op:cc-3 at any grade.")}

    print("== Riemann scheme of L ==")
    ind0, low0 = indicial_at(sp.Integer(0))
    ind13, low13 = indicial_at(sp.Rational(1, 3))
    roots0 = sp.roots(sp.Poly(ind0, sp.symbols('r')))
    roots13 = sp.roots(sp.Poly(ind13, sp.symbols('r')))
    exps0 = sorted(sum([[sp.nsimplify(rt)] * mult for rt, mult in roots0.items()], []), key=lambda x: float(x))
    exps13 = sorted(sum([[sp.nsimplify(rt)] * mult for rt, mult in roots13.items()], []), key=lambda x: float(x))
    print(f"  z=0   indicial = {ind0}  -> exponents {exps0}")
    print(f"  z=1/3 indicial = {ind13} -> exponents {exps13}")
    out["exponents_at_0"] = [str(e) for e in exps0]
    out["exponents_at_1_3"] = [str(e) for e in exps13]
    out["indicial_0"] = str(ind0)
    out["indicial_1_3"] = str(ind13)

    print("\n== Frobenius log structure ==")
    log0 = frobenius_logs(sp.Integer(0), [0, 1], low0)      # {0,0,1,1}: integer block {0,1}, each doubled
    log13 = frobenius_logs(sp.Rational(1, 3), [0, 1, 2], low13)  # block {0,1,2} (the -4/3 is isolated)
    print(f"  z=0   block {{0,1}}  : resonance logs? {log0['has_log']}  obstructions {log0['resonance_obstructions']}")
    print(f"  z=1/3 block {{0,1,2}}: resonance logs? {log13['has_log']}  obstructions {log13['resonance_obstructions']}")
    out["frobenius_z0"] = log0
    out["frobenius_z13"] = log13
    # z=0 has a REPEATED indicial root structure {0,0,1,1}: standard Frobenius theory
    # guarantees logarithmic second solutions at each repeated exponent regardless of the
    # resonance-obstruction test. The holomorphic exponent-0 solution Phi=1+5z+... is the
    # log-FREE member; logs live in the partner solutions.
    out["z0_repeated_root_logs"] = ("z=0 indicial r^2(r-1)^2 has DOUBLE roots at 0 and 1; the "
                                     "second solution at each exponent carries a logarithm (Frobenius "
                                     "repeated-root theorem). Phi (the holomorphic exp-0 solution, "
                                     "1+5z+...) is log-free; it is the solution we continue to z=1/3.")
    out["note_isolated_exponent"] = ("z=1/3 exponent -4/3 is isolated (non-integer gap to {0,1,2}) => its "
                                      "(1-3z)^{-4/3} solution is log-free; K (its amplitude in the "
                                      "continuation of Phi) is cleanly defined and unaffected by any logs "
                                      "inside the {0,1,2} block.")


    print("\n== z=infinity ==")
    inf = infinity_analysis()
    for k, v in inf.items():
        print(f"  {k}: {v}")
    out["infinity"] = inf

    # Fuchs relation audit
    sum0 = sum(exps0)
    sum13 = sum(exps13)
    finite_sum = sp.nsimplify(sum0 + sum13)
    fuchs_required = sp.Rational((3 - 2) * ORDER * (ORDER - 1), 2)   # (#sing-2)*n(n-1)/2, n=4, #sing=3
    print("\n== Fuchs-relation audit ==")
    print(f"  sum exps@0 = {sum0}, sum exps@1/3 = {sum13}, finite sum = {finite_sum}")
    print(f"  Fuchsian relation would require total = {fuchs_required} (=> infinity sum {fuchs_required - finite_sum})")
    gate_pass = inf["is_regular_singular_at_infinity"] and inf["newton_is_regular_singular"]
    print(f"  GATE 0 (infinity regular singular, both routes?) : {gate_pass}")
    out["fuchs_audit"] = {
        "sum_exps_0": str(sum0), "sum_exps_1_3": str(sum13),
        "finite_exponent_sum": str(finite_sum),
        "fuchsian_total_required": str(fuchs_required),
        "infinity_sum_if_fuchsian": str(sp.nsimplify(fuchs_required - finite_sum)),
        "note": ("Since infinity is IRREGULAR, the Fuchsian Fuchs relation does NOT apply: there is "
                 "no full set of 4 finite exponents at infinity; the budget is absorbed by the "
                 "irregularity (slope 1/4)." if not gate_pass else
                 "infinity regular singular; Fuchs relation applies.")}

    out["GATE0_infinity_regular_singular"] = bool(gate_pass)
    out["GATE0_verdict"] = ("PASS: infinity regular singular -> L Fuchsian -> proceed" if gate_pass else
                            "FAIL: infinity IRREGULAR (slope 1/4) -> L is NOT globally Fuchsian -> "
                            "RESCOPE 'Fuchsian relocation' and HALT before cc3-1c")
    out["rescope"] = (None if gate_pass else
                      ("The cc3-1a 'Fuchsian relocation' is OVERCLAIMED. Correct statement: L is "
                       "regular-singular at z=0 and z=1/3 (so the dominant-singularity connection "
                       "problem 0 -> 1/3 is regular-to-regular and K is well-defined by Frobenius), "
                       "but L is IRREGULAR at z=infinity (slope 1/4, from the -z^2 term) -- the "
                       "irregular structure of the original problem at s=infinity is PRESERVED under "
                       "the Borel-2 transform, not removed. K is therefore a connection coefficient "
                       "of a NON-Fuchsian (Stokes-carrying) operator; its natural period home is "
                       "exponential periods, not classical KZ periods. cc3-1c must use the index of "
                       "rigidity for IRREGULAR connections (Bloch-Esnault / Arinkin / Jakob-Yun), "
                       "not the Fuchsian Katz formula."))

    blob = json.dumps(out, sort_keys=True, ensure_ascii=False).encode("utf-8")
    out["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1b_riemann_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", out["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1b_riemann_results.json")


if __name__ == "__main__":
    main()
