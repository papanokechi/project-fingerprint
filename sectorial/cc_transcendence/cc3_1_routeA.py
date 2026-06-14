#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1  Route A  --  INTEGRAL REPRESENTATION (the centerpiece)
================================================================================
SIARC. Recurrence -> ODE duality -> convergent Borel-2 companion Phi -> a
Beta-kernel integral representation of G(s), numerically verified to >=100
digits; then the connection-coefficient C is reduced to Phi's local singular
data at the FUCHSIAN point z=1/3 (the "cleaner dual").

CEILING (standing rule, reproduced): a large G_Gal does NOT imply C
transcendental; an exponential-period classification does NOT imply C
transcendental; only a named-conjecture conditional (or out-of-scope new
technology) does. Unconditional transcendence of C is NOT a deliverable of
op:cc-3 at any grade.

Steps (every manipulation checked against the series):
 (1) OGF y(t)=sum Q_n t^n satisfies  3 t^3 y'' + 10 t^2 y' + (t^2+5t-1) y = -1.
 (2) Borel-2 companion  Phi(z)=sum Q_n z^n/(n!)^2 : radius 1/3, holomorphic;
     satisfies the homogeneous Fuchsian-at-0-and-1/3 operator
       L = z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 -15 z^2 D - z^2.
 (3) Beta-kernel identity  1/C(2n,n) = (2n+1) int_0^1 [t(1-t)]^n dt  gives
       G(s) = int_0^1 [ Phi(z) + 2 z Phi'(z) ] dt,   z = s t(1-t).
     Verified >=100 digits at interior s=1.
 (4) Exponents of Phi at z=1/3 are {0,1,2,-4/3}; saddle (t=1/2, z->1/3) gives
     gamma_G = rho + 1/2 with rho=4/3 -> gamma=11/6 (matches EBR exactly), and
       C_EBR = A = K * (4/3) sqrt(pi) / Gamma(7/3),
     i.e. transcendence of C is RELOCATED to transcendence of K = Phi's
     connection coefficient at the Fuchsian point z=1/3 (irregular->regular).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import hashlib
import mpmath as mp
import sympy as sp

# ----------------------------------------------------------------------------
# exact integer corpus
# ----------------------------------------------------------------------------
def build_Q(N):
    Q = [1, 5]
    while len(Q) <= N:
        n = len(Q)
        Q.append((3 * n * n + n + 1) * Q[n - 1] + Q[n - 2])
    return Q


def main():
    results = {"op": "cc3-1-routeA",
               "task_id": "op:cc-transcendence/cc3-1",
               "title": "Beta-kernel integral representation of G and reduction of C to a Fuchsian connection coefficient",
               "ceiling": ("Unconditional transcendence of C is NOT a deliverable; a large G_Gal "
                           "or exponential-period classification does not imply transcendence; only "
                           "a named-conjecture conditional (or new technology) does."),
               }

    # ---- (1) OGF ODE check -------------------------------------------------
    print("== (1) OGF ODE: 3 t^3 y'' + 10 t^2 y' + (t^2+5t-1) y = -1 ==")
    t = sp.symbols('t')
    NT = 56
    Q = build_Q(NT + 2)
    y = sum(sp.Integer(Q[n]) * t**n for n in range(NT + 1))
    expr = 3 * t**3 * sp.diff(y, t, 2) + 10 * t**2 * sp.diff(y, t) + (t**2 + 5 * t - 1) * y + 1
    ser = sp.Poly(sp.expand(expr), t)
    bad = [(k, c) for k, c in enumerate([ser.coeff_monomial(t**k) for k in range(NT - 3)]) if c != 0]
    ogf_ok = (len(bad) == 0)
    print(f"   coefficients t^0..t^{NT-4} all zero: {ogf_ok}   (nonzero: {bad[:3]})")
    results["ogf_ode"] = {"operator": "3 t^3 y'' + 10 t^2 y' + (t^2+5t-1) y = -1",
                          "verified_terms": NT - 4, "all_zero": bool(ogf_ok)}

    # ---- (2) Phi operator <-> recurrence identity (exact, symbolic) --------
    print("\n== (2) Phi(z)=sum Q_n z^n/(n!)^2 : operator L vs recurrence ==")
    n = sp.symbols('n')
    # coefficient of z^n in L[Phi] must equal
    #   n^2(n-1)^2 phi_n - (3n^2+n+1)(n-1)^2 phi_{n-1} - phi_{n-2}
    # from L = z^4(1-3z)D^4 + (4z^3-25z^4)D^3 + (2z^2-47z^3)D^2 -15 z^2 D - z^2.
    coeff_phi_n = (n * (n - 1) * (n - 2) * (n - 3)
                   + 4 * n * (n - 1) * (n - 2)
                   + 2 * n * (n - 1))
    coeff_phi_nm1 = (-3 * (n - 1) * (n - 2) * (n - 3) * (n - 4)
                     - 25 * (n - 1) * (n - 2) * (n - 3)
                     - 47 * (n - 1) * (n - 2)
                     - 15 * (n - 1))
    coeff_phi_nm2 = sp.Integer(-1)
    want_n = n**2 * (n - 1)**2
    want_nm1 = -(3 * n**2 + n + 1) * (n - 1)**2
    id_n = sp.simplify(coeff_phi_n - want_n) == 0
    id_nm1 = sp.simplify(coeff_phi_nm1 - want_nm1) == 0
    id_nm2 = (coeff_phi_nm2 == -1)
    L_ok = id_n and id_nm1 and id_nm2
    print(f"   phi_n coeff = n^2(n-1)^2 : {id_n}")
    print(f"   phi_(n-1) coeff = -(3n^2+n+1)(n-1)^2 : {id_nm1}")
    print(f"   phi_(n-2) coeff = -1 : {id_nm2}")
    print(f"   operator L reproduces the recurrence EXACTLY: {L_ok}")
    results["phi_operator"] = {
        "L": "z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2",
        "reproduces_recurrence": bool(L_ok)}

    # radius of convergence of Phi (ratio test on phi_n=Q_n/(n!)^2)
    mp.mp.dps = 30
    Qr = build_Q(400)
    fr = [mp.mpf(1)] * 401
    for i in range(1, 401):
        fr[i] = fr[i - 1] * i
    phi = [mp.mpf(Qr[k]) / (fr[k]**2) for k in range(401)]
    ratio = phi[400] / phi[399]      # -> 1/R_phi = 3
    Rphi = 1 / ratio
    print(f"   ratio phi_400/phi_399 = {mp.nstr(ratio,12)} -> radius ~ {mp.nstr(Rphi,12)} (expect 1/3)")
    results["phi_radius"] = {"ratio_phi_400_399": mp.nstr(ratio, 18),
                             "radius_estimate": mp.nstr(Rphi, 18), "expected": "1/3"}

    # ---- (3) Beta-kernel integral representation, >=100 digits -------------
    print("\n== (3) G(s) = int_0^1 [Phi(z)+2 z Phi'(z)] dt, z=s t(1-t) ; verify @ s=1 ==")
    mp.mp.dps = 130
    NTERM = 1200
    Qm = build_Q(NTERM + 1)
    fac = [mp.mpf(1)] * (2 * NTERM + 1)
    for i in range(1, 2 * NTERM + 1):
        fac[i] = fac[i - 1] * i
    # RHS integrand coefficients a_n = phi_n (2n+1)
    a = [(mp.mpf(Qm[k]) / (fac[k]**2)) * (2 * k + 1) for k in range(NTERM + 1)]
    g = [mp.mpf(Qm[k]) / fac[2 * k] for k in range(NTERM + 1)]

    def check_at(sval):
        # LHS: G(s) = sum_n Q_n/(2n)! s^n ; RHS: int_0^1 Horner(a, s t(1-t)) dt
        G_direct = mp.fsum(g[k] * sval**k for k in range(NTERM + 1))

        def integrand(tt):
            z = sval * tt * (1 - tt)
            acc = mp.mpf(0)
            for k in range(NTERM, -1, -1):
                acc = acc * z + a[k]
            return acc

        G_int = mp.quad(integrand, [0, mp.mpf(1) / 2, 1])
        d = abs(G_direct - G_int)
        dig = 1e9 if d == 0 else float(-mp.log10(d))
        return G_direct, G_int, d, dig

    int_checks = {}
    for sval in [mp.mpf(1), mp.mpf('1.25')]:
        Gd, Gi, d, dig = check_at(sval)
        print(f"   s={mp.nstr(sval,4)}: G_direct={mp.nstr(Gd,30)}  |diff|={mp.nstr(d,6)}  agree~{dig if dig<1e8 else '>'+str(mp.mp.dps)} digits")
        int_checks[mp.nstr(sval, 4)] = {
            "G_direct": mp.nstr(Gd, 105), "G_integral": mp.nstr(Gi, 105),
            "abs_diff": mp.nstr(d, 6),
            "agreement_digits": dig if dig < 1e8 else f">={mp.mp.dps}"}
    results["integral_representation"] = {
        "formula": "G(s) = int_0^1 [Phi(z) + 2 z Phi'(z)] dt, z = s t (1-t)",
        "validity": "|s| < R = 4/3 (z_max = s/4 < 1/3)",
        "dps": mp.mp.dps, "nterm": NTERM,
        "checks": int_checks,
    }

    # ---- (4) Exponents at z=1/3 and reduction of C -------------------------
    print("\n== (4) Frobenius exponents of Phi at z=1/3, and reduction of C ==")
    # indicial polynomial I(r) = r(r-1)(r-2)[ c (r-3) + p3(z0) ],
    # c = (d/dz p4)|_{1/3} = -1/27, p3(1/3) = 4/27 - 25/81 = -13/81.
    r = sp.symbols('r')
    c = sp.Rational(-1, 27)
    p3_at = sp.Rational(4, 27) - sp.Rational(25, 81)   # = -13/81
    indicial = r * (r - 1) * (r - 2) * (c * (r - 3) + p3_at)
    roots = sorted(sp.solve(sp.Eq(indicial, 0), r), key=lambda x: float(x))
    print(f"   p3(1/3) = {p3_at} ; indicial roots (exponents at z=1/3) = {roots}")
    rho = sp.Rational(4, 3)
    dominant = -rho
    gamma_from_saddle = rho + sp.Rational(1, 2)
    print(f"   dominant exponent = {dominant} (rho=4/3) ; saddle: gamma = rho+1/2 = {gamma_from_saddle} (EBR gamma=11/6: {gamma_from_saddle==sp.Rational(11,6)})")
    results["exponents_at_1_3"] = {
        "indicial": "r(r-1)(r-2)(-(r-3)/27 - 13/81)",
        "exponents": [str(x) for x in roots],
        "dominant": str(dominant),
        "rho": "4/3",
        "gamma_from_saddle": str(gamma_from_saddle),
        "matches_EBR_gamma_11_6": bool(gamma_from_saddle == sp.Rational(11, 6)),
    }

    # numerical confirmation that -4/3 is the dominant exponent:
    # Phi(z)*(1-3z)^{4/3} -> K (finite, nonzero) as z->1/3^-.
    print("\n   numerical exponent/amplitude check: Phi(z)*(1-3z)^{4/3} as z->1/3^- ...")
    mp.mp.dps = 60
    NE = 9000
    Qe = build_Q(NE + 1)
    fe = [mp.mpf(1)] * (NE + 1)
    for i in range(1, NE + 1):
        fe[i] = fe[i - 1] * i
    phie = [mp.mpf(Qe[k]) / (fe[k]**2) for k in range(NE + 1)]

    def Phi_val(zz):
        acc = mp.mpf(0)
        for k in range(NE, -1, -1):
            acc = acc * zz + phie[k]
        return acc

    samples = []
    epss = [mp.mpf('1e-2'), mp.mpf('5e-3'), mp.mpf('2.5e-3')]
    for eps in epss:
        zz = mp.mpf(1) / 3 - eps / 3        # 1-3z = eps
        val = Phi_val(zz) * eps**(mp.mpf(4) / 3)
        samples.append(val)
        print(f"      1-3z={mp.nstr(eps,4)} : Phi*(1-3z)^(4/3) = {mp.nstr(val,16)}")
    # Richardson on the eps^{4/3} leading correction (eps halves each step):
    p = mp.mpf(4) / 3
    fac1 = mp.mpf(2)**p - 1
    R1 = [samples[i + 1] + (samples[i + 1] - samples[i]) / fac1 for i in range(len(samples) - 1)]
    fac2 = mp.mpf(2)**(p + 1) - 1
    R2 = R1[-1] + (R1[-1] - R1[-2]) / fac2 if len(R1) >= 2 else R1[-1]
    K_num = R2
    # predicted K from saddle:  C_EBR = A = K*(4/3)*sqrt(pi)/Gamma(7/3)
    #   <=>  K = (3/4) * C_EBR * Gamma(7/3)/sqrt(pi)
    C_EBR = mp.mpf('3.0557068')        # 8-digit anchor from corpus (f3400831...)
    K_pred = mp.mpf(3) / 4 * C_EBR * mp.gamma(mp.mpf(7) / 3) / mp.sqrt(mp.pi)
    print(f"   K (Richardson-extrapolated, exponent 4/3) ~ {mp.nstr(K_num,10)}")
    print(f"   K (predicted from C_EBR via saddle)        = {mp.nstr(K_pred,10)}")
    rel = abs(K_num - K_pred) / abs(K_pred)
    print(f"   relative consistency = {mp.nstr(rel,4)}  (limited by series truncation near singularity)")
    results["C_reduction"] = {
        "statement": "C_EBR = A = K * (4/3) sqrt(pi)/Gamma(7/3); equivalently K = (3/4) C_EBR Gamma(7/3)/sqrt(pi)",
        "K_is": "connection coefficient of the FUCHSIAN operator L of Phi between z=0 (exponents {0,0,1,1}) and z=1/3 (exponents {0,1,2,-4/3})",
        "Gamma_quotient_factor": "(4/3) sqrt(pi)/Gamma(7/3)  (elementary)",
        "K_numeric_estimate": mp.nstr(K_num, 10),
        "K_numeric_method": "series of Phi near z=1/3 (NE=9000 terms), eps in {1e-2,5e-3,2.5e-3}, Richardson exponent 4/3",
        "K_predicted_from_C_EBR": mp.nstr(K_pred, 10),
        "relative_consistency": mp.nstr(rel, 4),
        "interpretation": ("transcendence of C is RELOCATED (not resolved) to the connection "
                           "coefficient K of a 4th-order Fuchsian operator; the irregular slope-1/4 "
                           "structure at s=infinity is bypassed for the dominant singularity, since "
                           "z=s t(1-t) <= s/4 reaches Phi's singularity z=1/3 only at s=R, t=1/2."),
        "grade": "STRUCTURAL (exact exponents + saddle) + VERIFIED (integral identity >=100 digits; K consistency low-precision)",
    }

    results["deliverable_type"] = "(b) integral/period representation + relocation of the obstruction (Fuchsian K)"
    results["obstruction_note"] = ("No closed elementary form for K (Phi's z=0->z=1/3 connection coefficient) "
                                   "is produced; this is the precise residual obstruction and the input to "
                                   "cc3-2 (exponential/Fuchsian period interpretation of K) and cc3-3 "
                                   "(named-conjecture conditional). Consistent with the 169-digit elementary nulls.")

    blob = json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
    results["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1_routeA_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", results["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1_routeA_results.json")


if __name__ == "__main__":
    main()
