#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-2s2-2b  --  GAUGE DICTIONARY: H2 -> standard D8 Lax form  (symbolic)
================================================================================
SIARC.  Build the explicit, step-by-step verifiable transformation from the
rank-2 core H2 to a standard PIII(D8)=D8^(1) linear (Lax) form, then apply the
composite map to kappa's defining datum.  Every algebraic step is a sympy-checked
identity.  Where the chain meets a step that is NOT a symbolic gauge (the
isomonodromy-time inverse problem), the OBSTRUCTION STATEMENT is the deliverable
and op:cc3-2s2-2c proceeds in SURVEY mode (per spec).

NAMED HAZARD (reproduced in every crossing paragraph): tau-function connection
constants  !=  Lax-solution Stokes data.  kappa is built below as a Lax-side
Stokes multiplier of the linear problem; the ILT/Gavrylenko-Lisovyy theorems
(2c) compute a tau-side connection constant.  The two are different objects on
the same monodromy manifold; the bridge between them is exactly the 2c question.

CHAIN (all maps explicit; residuals must be 0):
  H2 y = 3 t^3 y'' + 10 t^2 y' + (t^2 + 5 t - 1) y = 0
  (i)   scalar gauge  y = t^{-5/3} u   removes the first-derivative term:
            u'' = r(t) u,   r = 1/(3 t^3) - 5/(9 t^2) - 1/(3 t).
        [r = (1/4)P^2 + (1/2)P' - Q with P=10/(3t), Q=(t^2+5t-1)/(3t^3).]
  (ii)  ramified pullback  t = x^2  then gauge  Y(t)=Ytil(x), Ytil = x^{1/2} w:
            w'' = R(x) w,   R = 4/(3 x^4) - 53/(36 x^2) - 4/3.
        Two rank-1 irregular points (x=0 order-4 pole; x=infinity const -4/3)
        -- the symmetric DCHE / D8 local shape (cc3-2 CORE-NF).
  (iii) companion 2x2 first-order system  W=(w, w')^T:
            dW/dx = B(x) W,   B(x) = [[0, 1],[R(x), 0]].
        B has irregular singular points of Poincare rank 1 at x=0 and x=infinity
        -- the standard D8 Lax SHAPE (2x2, two rank-1 irregular points).
  Composite gauge from the ORIGINAL H2 solution y to w (with t=x^2):
            y = x^{-17/6} w        (= t^{-5/3} * x^{1/2}, since u=Y=x^{1/2}w).

DICTIONARY OUTPUT:
  A meromorphic SCALAR gauge multiplies BOTH formal solutions at an irregular
  point by the same factor, hence leaves the Stokes MATRICES (the ratios of
  formal solutions across a Stokes ray) INVARIANT.  Therefore the off-diagonal
  Stokes multiplier of B(x) at x=0 equals the Stokes multiplier of H2 at t=0.
  kappa (2s2-1: Gamma(4/3) A0, the Borel-plane amplitude / Stokes constant of y
  across arg(t)=0) is thus, up to the standard amplitude<->multiplier conversion
  factor (a Gamma-quotient in the formal exponents alpha_pm, alpha_++alpha_-=3/2),
  an OFF-DIAGONAL STOKES MULTIPLIER s_* of the companion D8 system B at x=0,
  evaluated at the 2a monodromy point (tr(M0) = -51.06556313995466226983...).

  =>  kappa = s_*(B; x=0) x [explicit elementary factor F],
      F a Gamma-quotient in {alpha_+, alpha_-} (formal-monodromy exponents),
      derivable from the Borel-amplitude<->Stokes-multiplier normalization.

OBSTRUCTION (documented; routes 2c to survey mode):
  Matching B(x) to a SPECIFIC published PARAMETRIZED PIII(D8) Lax matrix
  A(lambda, s) (Ohyama-Kawamuko-Sakai-Okamoto; FIKN) requires fixing the
  isomonodromy TIME s and the transcendent value (the PIII(D8) solution at s)
  for which the isomonodromic A(lambda,s) coincides with our FROZEN, non-
  deforming B(x).  That is an inverse-monodromy (Riemann-Hilbert) determination
  -- TRANSCENDENTAL, not a finite symbolic gauge.  Hence the dictionary lands
  rigorously at the companion-system level (a bona fide D8-shape Lax form) but
  the named-published-coordinate identification is NOT closed symbolically.
  => 2c is SURVEY mode: inventory which Stokes/tau coordinate the theorems cover
     and whether kappa's coordinate (a Lax-side x=0 Stokes multiplier) is among
     them, WITHOUT asserting a parametrized match.

Standard-form locators (SHAPE cited here; exact-matrix transcription deferred to
2c, where a formula would be used numerically and must be transcribed verbatim):
  - Ohyama, Kawamuko, Sakai, Okamoto, J. Math. Sci. Univ. Tokyo 13 (2006) 145-204
    (PIII(D8) Lax pair; 2x2, two rank-1 irregular points).
  - Fokas, Its, Kapaev, Novokshenov, "Painleve Transcendents: The RH Approach,"
    AMS Math. Surveys Monogr. 128 (2006), PIII chapter (2x2 linear system, Stokes
    structure at 0 and infinity).
  - Its, Lisovyy, Prokhorov, Comm. Math. Phys. (2018) (tau connection constants;
    the tau-side object -- the 2c hazard).
  - van der Put & Saito, Ann. Inst. Fourier 59 (2009) 2611-2667 (moduli of the
    Painleve linear problems; D8 = both points ramified).

CEILING (both directions, verbatim): a gauge dictionary that places kappa as a
D8 Stokes multiplier proves NOTHING about transcendence; a subsequent closed
form would argue the OPPOSITE (elementarity in an extended class).  Unconditional
transcendence of C/kappa is NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import sympy as sp

def canon_hash(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def main():
    t, x = sp.symbols('t x', positive=True)

    print("=== cc3-2s2-2b  gauge dictionary H2 -> D8 Lax form (symbolic) ===")

    # ---- step (i): scalar gauge y = t^{-5/3} u removes y' term -> u''=r u ----
    # H2 in normalized form y'' + P y' + Q y = 0
    P = sp.Rational(10,3)/t
    Q = (t**2 + 5*t - 1)/(3*t**3)
    r_reduced = sp.simplify(sp.Rational(1,4)*P**2 + sp.Rational(1,2)*sp.diff(P,t) - Q)
    r_target = 1/(3*t**3) - sp.Rational(5,9)/t**2 - 1/(3*t)
    res_i = sp.simplify(r_reduced - r_target)
    print(f"[i]   reduction P=10/(3t), Q=(t^2+5t-1)/(3t^3) => r = {sp.nsimplify(r_target)}")
    print(f"      residual r_reduced - r_target = {res_i}   (expect 0)")

    # Direct check: y=t^{-5/3} u satisfies H2 iff u''=r u.  Substitute and verify.
    u = sp.Function('u')
    y_sub = t**sp.Rational(-5,3)*u(t)
    H2y = 3*t**3*sp.diff(y_sub,t,2) + 10*t**2*sp.diff(y_sub,t,1) + (t**2+5*t-1)*y_sub
    # divide by 3 t^3 * t^{-5/3} and substitute u'' = r u
    H2y_norm = sp.simplify(H2y / (3*t**3*t**sp.Rational(-5,3)))
    # replace u'' by r*u
    H2y_red = H2y_norm.subs(sp.diff(u(t),t,2), r_target*u(t))
    res_i2 = sp.simplify(H2y_red)
    print(f"      direct gauge check: (H2[t^-5/3 u]/(3t^3 t^-5/3))|_(u''=r u) = {res_i2}   (expect 0)")

    # ---- step (ii): pullback t=x^2 then gauge Ytil=x^{1/2} w -> w''=R w ----
    # Y(t)=u solves Y''=rY. With t=x^2: Ytil(x)=Y(x^2). Build Ytil'' - (1/x)Ytil' - 4x^2 r(x^2) Ytil = 0,
    # then reduce with Pbar=-1/x, Qbar=-4x^2 r(x^2):  R = 1/4 Pbar^2 + 1/2 Pbar' - Qbar.
    r_of_x2 = r_target.subs(t, x**2)
    Pbar = -1/x
    Qbar = -4*x**2*r_of_x2
    R_reduced = sp.simplify(sp.Rational(1,4)*Pbar**2 + sp.Rational(1,2)*sp.diff(Pbar,x) - Qbar)
    R_target = 4/(3*x**4) - sp.Rational(53,36)/x**2 - sp.Rational(4,3)
    res_ii = sp.simplify(R_reduced - R_target)
    print(f"[ii]  pullback t=x^2, gauge Ytil=x^(1/2) w => R = {sp.nsimplify(R_target)}")
    print(f"      residual R_reduced - R_target = {res_ii}   (expect 0)")

    # verify the intermediate equation Ytil'' - (1/x)Ytil' - 4x^2 r Ytil = 0 from t=x^2
    Yf = sp.Function('Y'); Ytil = sp.Function('Ytil')
    # chain rule: d/dx = 2x d/dt ; build Ytil'' in terms of Y',Y'' then sub Y''=rY
    Yp = sp.Symbol('Yp'); Ypp = sp.Symbol('Ypp')  # Y'(t), Y''(t)
    Ytil_xx = 2*Yp + 4*x**2*Ypp            # d^2/dx^2 [Y(x^2)] = 2 Y'(t) + 4x^2 Y''(t)
    Ytil_x  = 2*x*Yp
    # symbolic identity check via Y''=rY: substitute Ypp -> r*Yval
    inter2 = sp.simplify((Ytil_xx).subs(Ypp, r_of_x2*sp.Symbol('Yval')) - (1/x)*Ytil_x
                         - 4*x**2*r_of_x2*sp.Symbol('Yval'))
    # inter2 should reduce to 2*Yp - (1/x)*2x*Yp = 2Yp - 2Yp = 0
    print(f"      intermediate-eq residual (after Y''=rY): {sp.simplify(inter2)}   (expect 0)")

    # ---- composite gauge factor: y = t^{-5/3} u, u=Y=x^{1/2} w, t=x^2 ----
    composite = sp.simplify((x**2)**sp.Rational(-5,3) * x**sp.Rational(1,2))  # x^{-10/3}*x^{1/2}
    print(f"[iii] companion B(x)=[[0,1],[R,0]]; composite gauge y = {composite} * w  (= x^(-17/6) w)")
    comp_ok = sp.simplify(composite - x**sp.Rational(-17,6)) == 0
    print(f"      composite gauge factor == x^(-17/6) : {comp_ok}")

    # ---- formal exponents at x=0 of B (info; alpha_+ + alpha_- = 3/2 inherited) ----
    print("[dict] kappa = s_*(B; x=0) x F,  F a Gamma-quotient in alpha_pm "
          "(alpha_+ + alpha_- = 3/2); s_* gauge-invariant under the scalar chain above.")

    all_zero = all(z == 0 for z in [res_i, res_i2, res_ii, sp.simplify(inter2)]) and comp_ok
    print(f"\n[VERDICT] gauge chain (i)-(iii) symbolic residuals all zero: {all_zero}")
    print("[VERDICT] published-Lax match A(lambda,s): OBSTRUCTED (isomonodromy-time "
          "inverse problem, transcendental) => 2c in SURVEY mode.")

    results = {
        "op": "cc3-2s2-2b-dictionary",
        "task_id": "op:cc-transcendence/cc3-2s2-2",
        "chain": {
            "i_scalar_gauge": {
                "map": "y = t^{-5/3} u", "result": "u'' = r u",
                "r": "1/(3 t^3) - 5/(9 t^2) - 1/(3 t)",
                "derivation": "r = (1/4)P^2 + (1/2)P' - Q, P=10/(3t), Q=(t^2+5t-1)/(3 t^3)",
                "residual_r": str(res_i), "direct_gauge_residual": str(res_i2),
            },
            "ii_ramified_pullback": {
                "map": "t = x^2, then Ytil = x^{1/2} w", "result": "w'' = R w",
                "R": "4/(3 x^4) - 53/(36 x^2) - 4/3",
                "intermediate_eq": "Ytil'' - (1/x) Ytil' - 4 x^2 r(x^2) Ytil = 0",
                "residual_R": str(res_ii), "intermediate_residual": str(sp.simplify(inter2)),
                "local_shape": "two rank-1 irregular points (x=0 order-4 pole, x=inf const -4/3); "
                               "symmetric DCHE = D8 local shape",
            },
            "iii_companion_system": {
                "map": "W=(w,w')^T, dW/dx = B W, B=[[0,1],[R,0]]",
                "shape": "2x2 first-order, irregular Poincare rank 1 at x=0 and x=infinity "
                         "= standard PIII(D8) Lax SHAPE",
                "composite_gauge_y_to_w": "y = x^{-17/6} w  (t=x^2)",
                "composite_check": bool(comp_ok),
            },
        },
        "dictionary_statement": {
            "kappa_is": "an off-diagonal Stokes multiplier s_* of the companion D8 system B at x=0, "
                        "at the 2a monodromy point tr(M0) = -51.06556313995466226983167460994566...",
            "elementary_factor": "kappa = s_*(B; x=0) x F; F = Gamma-quotient in formal exponents "
                                 "alpha_pm (alpha_+ + alpha_- = 3/2), from the Borel-amplitude<->Stokes-"
                                 "multiplier normalization. Scalar gauges leave Stokes MATRICES invariant, "
                                 "so s_* is intrinsic to the t=0 / x=0 irregular point.",
            "grade": "STRUCTURAL for the gauge chain (i)-(iii) (symbolic, residual 0); the "
                     "amplitude<->multiplier factor F is derivable (Gamma in alpha_pm); the "
                     "named-published-coordinate match is OBSTRUCTED (below).",
        },
        "obstruction": {
            "statement": "Matching B(x) to a specific published parametrized PIII(D8) Lax A(lambda,s) "
                         "requires fixing the isomonodromy time s and the transcendent value for which "
                         "the isomonodromic A(lambda,s) equals our FROZEN non-deforming B(x): an inverse-"
                         "monodromy (Riemann-Hilbert) determination, TRANSCENDENTAL, not a finite gauge.",
            "consequence": "dictionary lands rigorously at companion-system (D8-shape) level; 2c proceeds "
                           "in SURVEY mode (inventory coverage, no parametrized match asserted).",
        },
        "named_hazard_tau_vs_lax": "kappa is a LAX-side Stokes multiplier (linear-problem monodromy data). "
            "ILT/Gavrylenko-Lisovyy theorems compute a TAU-side connection constant. Different objects on "
            "the same D8 monodromy manifold; the bridge is the 2c question. Named in every crossing step.",
        "standard_form_locators_SHAPE_only": [
            "Ohyama-Kawamuko-Sakai-Okamoto, J. Math. Sci. Univ. Tokyo 13 (2006) 145-204 (PIII(D8) Lax pair)",
            "Fokas-Its-Kapaev-Novokshenov, AMS Surveys Monogr. 128 (2006), PIII chapter (2x2 linear system)",
            "Its-Lisovyy-Prokhorov, Comm. Math. Phys. (2018) (tau connection constants -- tau-side, 2c hazard)",
            "van der Put & Saito, Ann. Inst. Fourier 59 (2009) 2611-2667 (moduli of Painleve linear problems)",
        ],
        "exact_matrix_transcription": "DEFERRED to 2c (where a formula is used numerically and must be "
            "transcribed verbatim from the located source).",
        "ceiling": "A gauge dictionary placing kappa as a D8 Stokes multiplier proves NOTHING about "
                   "transcendence; a closed form would argue the OPPOSITE (elementarity in an extended "
                   "class). Unconditional transcendence of C/kappa is NOT a deliverable at any grade.",
        "all_symbolic_residuals_zero": bool(all_zero),
    }
    results["canonical_sha256_of_hashfree_object"] = canon_hash(results)
    with open("cc3_2s2_2b_dictionary_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", results["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_2s2_2b_dictionary_results.json")

if __name__ == "__main__":
    main()
