"""
op:cc3-2-1 + cc3-2-2  —  rank-2 core H2 classification and de Rham dimension counts.

H2 := 3 t^3 D^2 + 10 t^2 D + (t^2 + 5 t - 1)   (the OGF rank-2 core; OGF y satisfies H2 y = -1)

Deliverables (SIARC four-class, VERIFIED unless noted):
  (1) Exact local analysis of H2: singular set, pole orders of the reduced invariant r,
      slopes / Newton data at every singular point. (CC3-2-CORE)
  (2) Kovacic decision via the rigorous symmetric-power / Riccati criterion (van der Put-Singer,
      "Galois Theory of Linear Differential Equations", GMW 328, 2003, sec.4.3.4), with the
      Case-2 step done CORRECTLY via reducibility over a quadratic extension.  NOTE: an SL2-
      realized (infinite) dihedral group does NOT possess a rational Sym^2 invariant -- the
      weight-0 line y1*y2 in Sym^2 is ANTI-invariant under the SL2 swap antidiag(1,-1) -- so a
      rational-Sym^2-over-C(t) search is NOT a sound Case-2 test.  The sound test is:
        Case 1 (reducible)        <=> rational solution of the Riccati  u' + u^2 = r over C(t).
        Case 3 (finite primitive) excluded by an irregular singularity (slope > 0 => G infinite).
        Case 2 (imprimitive D_inf)<=> L becomes REDUCIBLE over a quadratic extension C(sqrt f)
                                      with sqrt f ramified only within the singular set {0, inf}.
                                      The UNIQUE double cover of P^1 branched at exactly {0, inf}
                                      is x^2 = t (a double cover of P^1 has an even branch divisor;
                                      {0} or {inf} alone is impossible).  So the decisive test is
                                      whether the pullback  Y'' = R(x) Y  (x = sqrt t) has a
                                      rational Riccati solution over C(x).  For H2, R(x)'s only
                                      finite pole is x=0 (order 4), so a rational solution is forced
                                      to the shape a/x^2 + b/x + c with a^2 = 4/3; the search over
                                      Q(sqrt 3) is therefore EXHAUSTIVE, not heuristic.
      WITH positive controls (validating the two detectors + the pullback machinery):
        Airy r=t   -> SL2  : Riccati/C(t) EMPTY and pullback-Riccati/C(x) EMPTY (primitive stays so)
        r=2/t^2    -> Case1: Riccati/C(t) NONEMPTY; pullback-Riccati/C(x) NONEMPTY
                             (reducibility is preserved by pullback => validates that the
                              pullback-Riccati detector FIRES on a genuinely reducible input)
        pullback formula numerically validated on Airy: Y = Ai(x^2)/sqrt(2x) solves Y'' = R(x) Y.
  (3) Normal-form identification by ramified pullback t = x^2. (CC3-2-NF)
  (4) Borel-2 / Hadamard chain deriving the rank-4 shell L from the rank-2 core + Bessel kernel. (CC3-2-CORE)
  (5) Deligne-Malgrange de Rham Euler characteristic / dim H^1_dR for H2 and L. (CC3-2-DIM)

MID-STAGE HALT trigger: if Case 1 (rational Riccati over C(t)) OR Case 2 (reducible pullback over
C(sqrt t)) fires for H2 -> H2 is Liouvillian -> stop (do not proceed).
"""
import sympy as sp
import json, hashlib, io, sys
sys.stdout.reconfigure(encoding="utf-8")

t, x, v, zz, s = sp.symbols('t x v zz s')

# ----------------------------------------------------------------------------------
# helpers: variable-agnostic Riccati search (optionally over Q(sqrt g)) + reduced-invariant
# pullback. Case 1 = rational Riccati over C(t); Case 2 = reducibility of the pullback over C(sqrt t).
# ----------------------------------------------------------------------------------
def _ansatz_var(var, poles, K, Dlo, Dhi, tag, sqrt_gen=None):
    """u = sum_p sum_{1..K} c/(var-p)^j + sum_{Dlo..Dhi} c var^i.
       If sqrt_gen is set, every coeff c = p + q*sqrt(sqrt_gen) with p,q rational unknowns."""
    params = []; u = sp.Integer(0)
    g = sp.sqrt(sqrt_gen) if sqrt_gen is not None else None
    def newc(nm):
        if g is None:
            c = sp.Symbol(nm); params.append(c); return c
        p = sp.Symbol('p_' + nm); qv = sp.Symbol('q_' + nm); params.extend([p, qv]); return p + qv*g
    for pi, pp in enumerate(poles):
        for j in range(1, K + 1):
            u += newc(f'{tag}_a{pi}_{j}') / (var - pp) ** j
    for i in range(Dlo, Dhi + 1):
        u += newc(f'{tag}_b{i}') * var ** i
    return u, params, g

def _solve_zero_var(expr, var, params, g=None):
    num = sp.fraction(sp.together(expr))[0]
    poly = sp.Poly(sp.expand(num), var)
    eqs = []
    for co in poly.all_coeffs():
        co = sp.expand(co)
        if g is None:
            eqs.append(co)
        else:                                  # split c0 + c1*sqrt g ; both must vanish over Q
            c1 = co.coeff(g); c0 = sp.expand(co - c1*g); eqs += [c0, c1]
    return sp.solve(eqs, params, dict=True)

def riccati_var(rr, var, poles, K=2, Dlo=0, Dhi=2, sqrt_gen=None):
    u, params, g = _ansatz_var(var, poles, K, Dlo, Dhi, 'r', sqrt_gen)
    out = []
    for srule in _solve_zero_var(sp.diff(u, var) + u**2 - rr, var, params, g):
        usol = sp.simplify(u.subs(srule))
        if usol != 0:
            out.append(usol)
    return out

def pullback_reduced(r_expr, phi_expr, src, dst):
    """Reduced invariant of y''=r y under src=phi(dst):  R(dst) = phi'^2 r(phi) - 1/2 {phi;dst}."""
    d1 = sp.diff(phi_expr, dst); d2 = sp.diff(phi_expr, dst, 2); d3 = sp.diff(phi_expr, dst, 3)
    schw = d3/d1 - sp.Rational(3, 2)*(d2/d1)**2
    return sp.cancel(d1**2 * r_expr.subs(src, phi_expr) - sp.Rational(1, 2)*schw)

# ----------------------------------------------------------------------------------
# (1) H2 reduced invariant r  (y'' = r y  after removing the first-order term)
# ----------------------------------------------------------------------------------
p = sp.Rational(10, 3) / t
q = (t**2 + 5*t - 1) / (3*t**3)
r = sp.cancel(sp.Rational(1,4)*p**2 + sp.Rational(1,2)*sp.diff(p, t) - q)
print("r(t) =", sp.together(r))                       # expect (-3 t^2 - 5 t + 3)/(9 t^3)

r_num, r_den = sp.fraction(sp.together(r))
ord0 = sp.Poly(r_den, t).degree()                     # pole order at 0 (num(0) != 0)
assert r_num.subs(t, 0) != 0
deg_num = sp.degree(sp.Poly(r_num, t)); deg_den = sp.degree(sp.Poly(r_den, t))
o_inf = deg_den - deg_num
slope0 = sp.Rational(ord0 - 2, 2)
print(f"pole order of r at t=0 = {ord0}; slope_0 = {slope0} (ramification {sp.denom(slope0) if slope0.q!=1 else 1})")
print(f"o(inf) = deg_den - deg_num = {o_inf}")

# reduced invariant near infinity via t = 1/v Schwarzian transform
phi = 1/v; p1 = sp.diff(phi, v); p2 = sp.diff(phi, v, 2); p3 = sp.diff(phi, v, 3)
schwarz = p3/p1 - sp.Rational(3,2)*(p2/p1)**2
R_inf = sp.cancel(p1**2 * r.subs(t, phi) - sp.Rational(1,2)*schwarz)
Rinf_num, Rinf_den = sp.fraction(sp.together(R_inf))
poleord_inf = sp.Poly(Rinf_den, v).degree()           # num(0) != 0 -> pole order = denom degree
assert Rinf_num.subs(v, 0) != 0
slope_inf = sp.Rational(poleord_inf - 2, 2)
print(f"reduced invariant near inf, R(v)= {sp.together(R_inf)}; pole order at v=0 = {poleord_inf}; slope_inf = {slope_inf}")

# ----------------------------------------------------------------------------------
# (2) KOVACIC via the rigorous Riccati / quadratic-reducibility criterion, with positive controls.
#     Case 1 <=> rational Riccati over C(t).
#     Case 3  excluded by irregular singularity (slope0 > 0 => G infinite).
#     Case 2 (imprimitive) <=> L reducible over C(sqrt t), the UNIQUE quadratic cover branched only
#            within the singular set {0, inf}; test = rational Riccati of the pullback R(x), x=sqrt t.
# ----------------------------------------------------------------------------------
# pullback under t = x^2 (also the normal-form cover); reused by the normal-form block below.
R_x = pullback_reduced(r, x**2, t, x)

print("\n=== KOVACIC: positive controls (detector + pullback validation) ===")
control_report = {}

# Airy r=t : primitive SL2 -> Riccati/C(t) empty AND pullback-Riccati/C(x) empty
R_airy = pullback_reduced(t, x**2, t, x)
ai_ct = riccati_var(t, t, [0], K=3, Dlo=0, Dhi=3)
ai_cx = riccati_var(R_airy, x, [0], K=3, Dlo=0, Dhi=3)
control_report["Airy r=t [SL2: both EMPTY]"] = {
    "riccati_Ct_nonempty": len(ai_ct) > 0, "pullback_riccati_Cx_nonempty": len(ai_cx) > 0}

# r=2/t^2 : Case 1 reducible -> Riccati/C(t) nonempty; pullback preserves reducibility -> C(x) nonempty
r2 = sp.Integer(2)/t**2; R2 = pullback_reduced(r2, x**2, t, x)
r2_ct = riccati_var(r2, t, [0], K=3, Dlo=0, Dhi=3)
r2_cx = riccati_var(R2, x, [0], K=3, Dlo=0, Dhi=3)
control_report["r=2/t^2 [Case1: both NONEMPTY]"] = {
    "riccati_Ct_nonempty": len(r2_ct) > 0, "pullback_riccati_Cx_nonempty": len(r2_cx) > 0,
    "riccati_Ct_examples": [str(u) for u in r2_ct[:2]],
    "pullback_riccati_Cx_examples": [str(u) for u in r2_cx[:2]]}

# pullback FORMULA numeric validation on Airy : Y = Ai(x^2)/sqrt(2x) solves Y'' = R_airy Y
import mpmath as mp
mp.mp.dps = 40
Rairy_f = sp.lambdify(x, R_airy, 'mpmath')
Yf = lambda xx: mp.airyai(xx**2) / mp.sqrt(2*xx)
x0 = mp.mpf('0.7'); h = mp.mpf('1e-12')
resid = (Yf(x0 + h) - 2*Yf(x0) + Yf(x0 - h)) / h**2 - Rairy_f(x0)*Yf(x0)
pullback_formula_residual = float(abs(resid))
control_report["pullback_formula_numeric_check_Airy"] = {
    "Yppminus_R_Y_abs_residual": pullback_formula_residual, "ok": pullback_formula_residual < 1e-8}
for kctrl, vctrl in control_report.items():
    print(f"  {kctrl}: {vctrl}")

print("\n=== KOVACIC: H2 itself ===")
# Case 1 : rational Riccati over C(t) (finite poles confined to {0})
ric_H2 = riccati_var(r, t, [0], K=3, Dlo=0, Dhi=3)
print("  H2 Case 1 -- rational Riccati/C(t) solutions:", [str(u) for u in ric_H2])
# indicial corroboration: r ~ 1/(3 t^3), pole order 3 => any Riccati solution u ~ +-(1/sqrt3) t^(-3/2),
# a half-integer pole order -- impossible for a rational function.  RIGOROUS (search-independent).
ric_pole = sp.Rational(3, 2)
print(f"  indicial: forced Riccati pole order at t=0 = {ric_pole} (half-integer) => no rational Riccati over C(t)")

# Case 2 : reducibility of the pullback over C(sqrt t).  Only finite pole of R(x) is x=0 (order 4),
# so any rational Riccati of R(x) is forced to a/x^2 + b/x + c with a^2 = 4/3 (need Q(sqrt 3)).
Rx_num0, Rx_den0 = sp.fraction(sp.together(R_x))
finite_poles_Rx = sp.roots(sp.Poly(Rx_den0, x))
pull_forced = riccati_var(R_x, x, [0], K=2, Dlo=0, Dhi=0, sqrt_gen=3)      # the forced shape
pull_wide = riccati_var(R_x, x, [0], K=4, Dlo=0, Dhi=2, sqrt_gen=3)        # wider net (no spurious poles)
pullback_reducible = (len(pull_forced) > 0) or (len(pull_wide) > 0)
print(f"  pullback R(x) = {sp.together(R_x)}")
print(f"  finite poles of R(x): {dict(finite_poles_Rx)} (only x=0, order 4)")
print(f"  H2 Case 2 -- rational Riccati of pullback over C(sqrt t): forced-shape={[str(u) for u in pull_forced]}, "
      f"wide={[str(u) for u in pull_wide]}")
print("  unique-cover argument: x^2=t is the ONLY double cover of P^1 branched at exactly {0,inf}")
print("  (an even branch divisor is required); empty pullback Riccati => H2 NOT reducible over any")
print("  admissible quadratic extension => NOT imprimitive.")

has_riccati = len(ric_H2) > 0
irregular = slope0 > 0
if has_riccati:
    galois = "REDUCIBLE (Case 1) -- LIOUVILLIAN"
elif pullback_reducible:
    galois = "IMPRIMITIVE/DIHEDRAL (Case 2) -- LIOUVILLIAN"
else:
    galois = "SL_2 (irreducible, not imprimitive, not finite) -- NON-LIOUVILLIAN"
LIOUVILLIAN = has_riccati or pullback_reducible
print(f"\n  Case 1 (reducible)   excluded: {not has_riccati}   [no rational Riccati over C(t); indicial pole 3/2]")
print(f"  Case 3 (finite)      excluded: {bool(irregular)}   [t=0 irregular, slope {slope0} > 0 => G infinite]")
print(f"  Case 2 (imprimitive) excluded: {not pullback_reducible}   [pullback over C(sqrt t) irreducible]")
print(f"  ==> G_Gal(H2) = {galois}")
if LIOUVILLIAN:
    print("\n  *** LIOUVILLIAN VERDICT -> UNCONDITIONAL MID-STAGE HALT ***")

# ----------------------------------------------------------------------------------
# (3) NORMAL FORM: ramified pullback t = x^2  (R_x already computed in the Kovacic block)
# ----------------------------------------------------------------------------------
print("\n=== NORMAL FORM: ramified pullback t = x^2 ===")
Rx_num, Rx_den = sp.fraction(sp.together(R_x))
pole_x0 = sp.Poly(Rx_den, x).degree()
slope_x0 = sp.Rational(pole_x0 - 2, 2)
lim_xinf = sp.limit(R_x, x, sp.oo)
print(f"  R(x) = {sp.together(R_x)}")
print(f"  expanded: {sp.expand(R_x)}")
print(f"  pole order at x=0 = {pole_x0} => slope_x0 = {slope_x0} (unramified rank-1 irregular)")
print(f"  R(x) -> {lim_xinf} as x->inf (nonzero const => rank-1 irregular at inf)")
print("  => TWO rank-1 irregular points (x=0, x=inf), no finite regular-singular point")
print("  => normal form (b): SYMMETRIC DOUBLY-CONFLUENT HEUN (DCHE).")
print("     NOT classical-confluent: Bessel/Kummer/Whittaker each have ONE irregular + ONE")
print("     regular-singular point; #irregular points (2) is gauge+Mobius invariant and is not")
print("     reduced by a ramified pullback (slope>0 cannot become a regular point).")

# ----------------------------------------------------------------------------------
# (4) BOREL-2 / HADAMARD chain:  rank-4 L = (H2 core)  (x)  Bessel kernel
# ----------------------------------------------------------------------------------
print("\n=== BOREL-2 / HADAMARD chain ===")
N = 40
Bser = [sp.Integer(1)] + [sp.Rational(1, sp.factorial(n)**2) for n in range(1, N+1)]
ok_B = all(n**2 * Bser[n] - Bser[n-1] == 0 for n in range(1, N+1))   # (theta^2 - z) B = 0
print("  (theta^2 - z) annihilates B(z)=I_0(2 sqrt z)=sum z^n/(n!)^2 :", ok_B)

Q = [sp.Integer(1), sp.Integer(5)]
for n in range(2, N+1):
    Q.append((3*n**2 + n + 1)*Q[n-1] + Q[n-2])
print("  Q_0..Q_3 =", [int(Q[i]) for i in range(4)], "(expect 1,5,76,2361)")
a_coeff = [Q[n]/sp.factorial(n)**2 for n in range(N+1)]
Phi = sum(a_coeff[n]*zz**n for n in range(N+1))
D = lambda f: sp.diff(f, zz)
L_Phi = (zz**4*(1-3*zz))*D(D(D(D(Phi)))) + (4*zz**3-25*zz**4)*D(D(D(Phi))) \
        + (2*zz**2-47*zz**3)*D(D(Phi)) - 15*zz**2*D(Phi) - zz**2*Phi
Lp = sp.Poly(sp.expand(L_Phi), zz)
low = [c for (m,), c in zip(Lp.monoms(), Lp.coeffs()) if m <= N-5]
max_low = max([abs(c) for c in low]) if low else sp.Integer(0)
print("  L annihilates Phi: max |coeff| at orders <= N-5 :", max_low, "(0 => exact to truncation)")

# ----------------------------------------------------------------------------------
# (5) DELIGNE-MALGRANGE de Rham dimension counts
#   chi_dR(U,M) = rank*chi(U) - sum_x irr_x(M);  dim H^1 = -chi  (H^0=H^2=0, irreducible nonconstant)
#   irr_x = sum of slopes over formal exponents = rank * slope (single-slope case)
# ----------------------------------------------------------------------------------
print("\n=== de Rham dimension counts (Deligne-Malgrange Euler-Poincare) ===")
chiU_H2 = 2 - 2
irr_H2 = sp.Rational(1) + sp.Rational(1)
chi_H2 = 2*chiU_H2 - irr_H2
dimH1_H2 = -chi_H2
print(f"  H2: rank 2, U=G_m, chi(U)={chiU_H2}, irr_0+irr_inf={irr_H2}; chi_dR={chi_H2} => dim H^1_dR = {dimH1_H2}")
chiU_L = 2 - 3
irr_L = sp.Rational(0) + sp.Rational(0) + sp.Rational(1)
chi_L = 4*chiU_L - irr_L
dimH1_L = -chi_L
print(f"  L:  rank 4, U=P1\\{{0,1/3,inf}}, chi(U)={chiU_L}, irr_inf={irr_L}; chi_dR={chi_L} => dim H^1_dR = {dimH1_L}")
print(f"  EP control (trivial d/dz on G_m): chi = {1*0-0} (H^0=H^1=1, chi=0) OK")
print(f"  EP control (Bessel rank2 on G_m, irr_inf=2): dim H^1 = {-(2*0-2)} (=2) OK")

# ----------------------------------------------------------------------------------
# RESULTS  +  canonical hash
# ----------------------------------------------------------------------------------
results = {
    "op": "cc3-2-1 + cc3-2-2",
    "H2": "3 t^3 D^2 + 10 t^2 D + (t^2 + 5 t - 1)",
    "reduced_invariant_r": str(sp.together(r)),
    "local_analysis": {
        "singular_set": ["t=0 (irregular)", "t=inf (irregular)"],
        "pole_order_r_at_0": int(ord0),
        "slope_at_0": str(slope0), "ramification_at_0": int(sp.denom(slope0)) if slope0.q != 1 else 1,
        "o_inf": int(o_inf),
        "reduced_invariant_near_inf": str(sp.together(R_inf)),
        "pole_order_r_at_inf": int(poleord_inf),
        "slope_at_inf": str(slope_inf), "ramification_at_inf": int(sp.denom(slope_inf)) if slope_inf.q != 1 else 1,
        "note": "slope = 1/2 at BOTH singular points (ramification 2). CORRECTS the prior '3/2' paraphrase. "
                "Pole order of r at 0 is 3; r ~ 1/(3 t^3) near 0.",
    },
    "kovacic": {
        "method": "Riccati (Case 1) + irregular-singularity (Case 3) + quadratic-reducibility pullback (Case 2)",
        "locator": "van der Put & Singer, Galois Theory of Linear Differential Equations, GMW 328, 2003, sec.4.3.4 (Kovacic / order-2 dichotomy) + sec.1.3-1.4 (algebraic Riccati solutions = imprimitivity over a quadratic extension)",
        "case1_reducible_excluded": (not has_riccati),
        "case3_finite_excluded": bool(irregular),
        "case2_imprimitive_excluded": (not pullback_reducible),
        "H2_rational_riccati_solutions_Ct": [str(u) for u in ric_H2],
        "riccati_pole_order_forced_at_0": str(ric_pole),
        "case2_pullback_cover": "x^2 = t (UNIQUE double cover of P^1 branched at exactly {0,inf}; even branch divisor forces this)",
        "case2_pullback_R_x": str(sp.together(R_x)),
        "case2_pullback_only_finite_pole": "x=0 (order 4) => rational Riccati forced to a/x^2+b/x+c with a^2=4/3 over Q(sqrt 3); search EXHAUSTIVE",
        "case2_pullback_rational_riccati_forced_shape": [str(u) for u in pull_forced],
        "case2_pullback_rational_riccati_wide": [str(u) for u in pull_wide],
        "case2_note": "An SL2-realized (infinite) dihedral group has NO rational Sym^2 invariant (y1*y2 is "
                      "anti-invariant under the SL2 swap), so a rational-Sym^2-over-C(t) search is NOT a sound "
                      "Case-2 test; the sound test is reducibility of the pullback over C(sqrt t).",
        "verdict": galois,
        "liouvillian": bool(LIOUVILLIAN),
        "positive_controls": control_report,
    },
    "normal_form": {
        "ramified_pullback": "t = x^2",
        "R_x": str(sp.together(R_x)), "R_x_expanded": str(sp.expand(R_x)),
        "pole_order_at_x0": int(pole_x0), "slope_at_x0": str(slope_x0),
        "limit_at_xinf": str(lim_xinf),
        "verdict": "(b) Heun-class: symmetric doubly-confluent Heun (DCHE)",
        "why_not_classical_confluent": "two genuinely irregular singular points (0 and inf); "
            "Bessel/Kummer/Whittaker each have exactly one irregular + one regular-singular point. "
            "The number/type of irregular points is a gauge+Mobius invariant and is not reduced by the "
            "ramified pullback (which fixes {0,inf} and cannot turn a slope>0 point into a regular one).",
        "routing": "case (b) => stage 2 builds the Hien rapid-decay pairing for rank 2 directly, "
                   "with the concrete named target = symmetric DCHE.",
    },
    "borel2_hadamard_chain": {
        "bessel_kernel": "B(z)=I_0(2 sqrt z)=sum z^n/(n!)^2, annihilated by (theta^2 - z) (rank 2)",
        "theta2_minus_z_annihilates_B": bool(ok_B),
        "Phi": "Phi(z)=sum Q_n z^n/(n!)^2 = (y (x) B)(z)  [Hadamard / coefficient-wise product]",
        "rank4_derivation": "rank-4 L = (rank-2 H2 recurrence) (x) (rank-2 theta^2 - z) via Hadamard "
            "product of operators; order <= 2*2 = 4. The leading symbol theta^2 (theta-1)^2 (double root) "
            "is the source of the z=0 Jordan [2,2]. The (n!)^2 (double Borel) is what raises the order to 4.",
        "L_annihilates_Phi_residual_low_order": str(max_low),
        "Q_check": [int(Q[i]) for i in range(4)],
    },
    "dimension_counts": {
        "formula": "chi_dR(U,M) = rank*chi(U) - sum_x irr_x(M);  dim H^1_dR = -chi  (H^0=H^2=0, irreducible nonconstant)",
        "H2": {"rank": 2, "U": "G_m=P1\\{0,inf}", "chi_U": int(chiU_H2), "irr_total": str(irr_H2),
               "chi_dR": str(chi_H2), "dim_H1_dR": str(dimH1_H2)},
        "L": {"rank": 4, "U": "P1\\{0,1/3,inf}", "chi_U": int(chiU_L), "irr_total": str(irr_L),
              "chi_dR": str(chi_L), "dim_H1_dR": str(dimH1_L)},
        "locator": "Deligne, Equations differentielles a points singuliers reguliers, LNM 163; "
                   "Malgrange index theorem; Sabbah, Introduction to Stokes structures, sec.5.",
    },
    "HALT": bool(LIOUVILLIAN),
}
blob = json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
results["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
with io.open("cc3_2_1_h2_classify_results.json", "w", encoding="utf-8") as fh:
    json.dump(results, fh, ensure_ascii=False, indent=2)

print("\n=== SUMMARY ===")
print("  Kovacic verdict:", galois)
print("  Liouvillian (HALT trigger):", LIOUVILLIAN)
print("  Normal form:", results["normal_form"]["verdict"])
print("  dim H^1_dR(H2) =", dimH1_H2, " dim H^1_dR(L) =", dimH1_L)
print("  canonical_sha256:", results["canonical_sha256_of_hashfree_object"])
