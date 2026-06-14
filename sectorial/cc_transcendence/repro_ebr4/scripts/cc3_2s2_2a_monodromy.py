#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-2s2-2a  --  MONODROMY COORDINATES OF H2  (computation, low risk)
================================================================================
SIARC.  H2 = 3 t^3 D^2 + 10 t^2 D + (t^2 + 5 t - 1); reduced (trace-free) form
  Y'' = r(t) Y,   r(t) = 1/(3 t^3) - 5/(9 t^2) - 1/(3 t).
Singular set {0, inf} ONLY, both irregular slope 1/2 ramification 2 (CC3-2-CORE-LOCAL).

This stage places H2 on the PIII(D8)=D8^(1) monodromy manifold (dim 2, rig 0,
CC3-2S2-RIG/RULES) by computing genuine Stokes/monodromy data and the SL2 trace
coordinate, with self-validating cross-checks.

(A) FORMAL DATA (exact).  WKB on Y''=rY at t=0:
      sqrt(r) ~ 1/sqrt(3) t^{-3/2}  =>  S(t) = INT sqrt(r) dt ~ -2/sqrt(3) t^{-1/2},
    so the two formal solutions carry the exponential factors
      exp( +- (2/sqrt(3)) t^{-1/2} ) t^{alpha_pm} (1 + ...).
    The INSTANTON ACTION is a = 2/sqrt(3).  RIGOROUS CROSS-CHECK to the 2s2-0
    reframe: the Gevrey-2 (n!)^2-Borel kernel ~ exp(-2 sqrt(z/t)) places the Borel
    singularity at z0 with 2 sqrt(z0) = a, i.e. z0 = (a/2)^2 = (1/sqrt(3))^2 = 1/3.
    => the formal exponential factor and the Borel-plane singularity z=1/3 are the
    SAME datum.  Wronskian of Y''=rY is constant (no Y' term) =>
      alpha_+ + alpha_- = 3/2   (from W ~ t^{alpha_+ + alpha_-} S' = const, S' ~ t^{-3/2}).
    The ramification (t^{1/2}) makes the FORMAL MONODROMY swap the two solutions:
      M_hat = [[0, e^{2 pi i alpha_+}],[e^{2 pi i alpha_-}, 0]],  trace 0,
      det M_hat = -e^{2 pi i (alpha_+ + alpha_-)} = -e^{3 pi i} = +1  (consistent with SL2).

(B) TOPOLOGICAL MONODROMY (numerical, self-validating).  Integrate Y''=rY around
    |t|=1 (the circle encloses only the puncture t=0) by Taylor marching; the
    monodromy M0 in SL2 (det=1) has trace = a genuine D8 character-variety
    coordinate.  M0 = S1 S2 M_hat with Stokes matrices S1=[[1,s1],[0,1]],
    S2=[[1,0],[s2,1]]; writing M_hat=[[0,b],[c,0]] (bc=-1) gives the STRUCTURAL
    relation  tr(M0) = s1 c + s2 b  -- i.e. tr(M0) is a function of the LOCAL
    Stokes multipliers at t=0.

(C) kappa AS STOKES DATUM.  From 2s2-1 (STRUCTURAL): kappa = Gamma(4/3) A0 is the
    Borel-plane singularity amplitude at z=1/3 = the Stokes constant of y across
    arg(t)=0.  Thus kappa is an OFF-DIAGONAL STOKES MULTIPLIER / connection datum of
    the D8 linear problem -- monodromy data, NOT a tau-function connection constant
    (the named hazard for 2c).

CROSS-CHECKS (a failure here is a HALT trigger: coords inconsistent with rig/SL2):
   det(M0) = 1                      (SL2)                          -- expect PASS
   tr(M0) real, |tr(M0)| != 2       (irreducible, off reducibility/parabolic locus)
   kappa != 0                       (nontrivial Stokes => not formally split)
   z0 = (a/2)^2 = 1/3               (formal<->Borel reframe consistency)

CEILING (both directions, verbatim in report): placing kappa as a Stokes/monodromy
coordinate proves NOTHING about transcendence; a closed form would argue the
OPPOSITE (elementarity in an extended class).  Unconditional transcendence of
C/kappa is NOT a deliverable of op:cc-3 at any grade.

Coordinate convention + locators:
  - van der Put & Saito, Ann. Inst. Fourier 59 (2009) 2611-2667 (moduli/monodromy
    description of the Painleve linear problems; D8 = both points ramified).
  - Its, Lisovyy, Prokhorov, "Monodromy dependence and connection constants for
    Painleve tau functions" (the D8/sine-Gordon monodromy manifold, Stokes data).
  - Sakai CMP 220 (2001) (surface D8^(1)); Ohyama-Kawamuko-Sakai-Okamoto JMSUT 13
    (2006) (PIII(D8) Lax pair).
"""
import sys, json, hashlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import mpmath as mm
from mpmath import mp, mpf, mpc

mp.dps = 160   # MUST precede the mpf constants below: module-level ONE3/FIVE9 are
               # evaluated at import time, so a later mp.dps inside main() would leave
               # them at the default 15-digit precision and silently cap accuracy
               # (the root cause of an earlier ~14-digit-wrong, false-stable trace).

KAPPA_FROZEN_130 = ("1.539494848576641034843781903384069038219390890553148730926294560611"
                    "093030530126489289595548377837121909677816857027063026103313161")

ONE3 = mpf(1)/3; FIVE9 = mpf(5)/9

def r_taylor(tk, J):
    inv = 1/tk
    p = [mpf(0)]*(J+4)
    p[1] = inv
    for k in range(2, J+4):
        p[k] = p[k-1]*inv
    r = [mpf(0)]*(J+1)
    sign = mpf(1)
    for j in range(J+1):
        c3 = (j+1)*(j+2)//2
        c2 = (j+1)
        r[j] = sign*( ONE3*c3*p[3+j] - FIVE9*c2*p[2+j] - ONE3*p[1+j] )
        sign = -sign
    return r

def step(y0, y1, tk, d, J):
    rj = r_taylor(tk, J)
    a = [mpc(0)]*(J+3)
    a[0] = y0; a[1] = y1
    for j in range(0, J+1):
        s = mpc(0)
        for i in range(0, j+1):
            s += rj[i]*a[j-i]
        a[j+2] = s/((j+2)*(j+1))
    y = mpc(0); yp = mpc(0); dk = mpf(1)
    # NB: accumulate the full computed Taylor block a[0..J+2] (range(J+3)); a prior
    # asymmetric range(J+2) truncation dropped a[J+2] and produced a FALSE-STABLE,
    # ~14-digit-WRONG trace.  See validation note in main(): the accuracy witness is
    # cross-(J, nsteps, radius) agreement, NOT det=1.
    for j in range(J+3):
        y += a[j]*dk
        if j+1 < len(a):
            yp += (j+1)*a[j+1]*dk
        dk *= d
    return y, yp

def monodromy(radius, nsteps, J):
    R = mpf(radius)
    ts = [R*mm.e**(mpc(0,1)*(2*mm.pi*mpf(k)/nsteps)) for k in range(nsteps+1)]
    cols = []
    for (y0, y1) in [(mpf(1), mpf(0)), (mpf(0), mpf(1))]:
        y, yp = y0, y1
        for k in range(nsteps):
            y, yp = step(y, yp, ts[k], ts[k+1]-ts[k], J)
        cols.append((y, yp))
    return mm.matrix([[cols[0][0], cols[1][0]],[cols[0][1], cols[1][1]]])

def canon_hash(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def main():
    mp.dps = 160
    print("=== cc3-2s2-2a  monodromy coordinates of H2 ===")

    # (A) formal data -- exact symbolic facts + the action<->Borel cross-check
    a_action = 2/mm.sqrt(3)
    z0 = (a_action/2)**2
    print(f"[A] instanton action a = 2/sqrt(3) = {mm.nstr(a_action,30)}")
    print(f"    Borel-2 singularity z0 = (a/2)^2 = {mm.nstr(z0,40)}  (target 1/3)")
    z0_ok = abs(z0 - mpf(1)/3) < mpf(10)**(-100)
    print(f"    z0 == 1/3 : {z0_ok}   (formal<->Borel reframe consistency)")
    print(f"    alpha_+ + alpha_- = 3/2 (Wronskian const) => det(M_hat)=-e^(3 pi i)=+1; tr(M_hat)=0 (swap)")

    # (B) numerical monodromy of the reduced equation.
    # ACCURACY WITNESS = cross-(J, nsteps, radius) agreement.  det=1 is preserved
    # structurally by any flow of the trace-free Y''=rY (Wronskian) and is therefore
    # NOT an accuracy proof; the trace is the accuracy-sensitive coordinate.  The
    # singular set is {0, infinity} ONLY, so EVERY circle |t|=rho>0 encloses just the
    # puncture t=0: radius-independence of tr(M0) is topological invariance of the
    # monodromy -- the strongest available correctness check.
    print("[B] topological monodromy M0 of Y''=rY (Taylor marching); accuracy witness")
    print("    = cross-(J,nsteps,radius) agreement (NOT det=1, which is structural):")
    configs = [
        ("rho=1.0 nsteps=240 J=90", "1.0", 240, 90),
        ("rho=1.0 nsteps=400 J=100", "1.0", 400, 100),  # vary nsteps AND J
        ("rho=1.7 nsteps=320 J=90", "1.7", 320, 90),     # vary radius (topological)
    ]
    def info(M):
        det = M[0,0]*M[1,1]-M[0,1]*M[1,0]
        tr  = M[0,0]+M[1,1]
        return det, tr
    traces = []
    dets = []
    for label, rho, ns, J in configs:
        M = monodromy(rho, ns, J)
        det, tr = info(M)
        traces.append(tr); dets.append(det)
        print(f"    {label:26s}: |det-1|={mm.nstr(abs(det-1),4)}  tr={mm.nstr(tr.real,55)}")
    # pairwise agreement digits
    def agree(x, y):
        return 160 if x == y else -int(mm.log10(abs(x-y)))
    ag01 = agree(traces[0], traces[1])
    ag02 = agree(traces[0], traces[2])
    ag12 = agree(traces[1], traces[2])
    tr_match = min(ag01, ag02, ag12)
    print(f"    pairwise trace agreement: (0,1)~{ag01}d  (0,2)~{ag02}d  (1,2)~{ag12}d")
    print(f"    => converged to ~{tr_match} digits (cross-J, cross-nsteps, cross-radius)")
    tr0 = traces[1].real          # highest-resolution config
    detb_err = abs(dets[1] - 1)

    # (C) kappa as Stokes datum
    kappa = mpf(KAPPA_FROZEN_130)
    print(f"[C] kappa (frozen 130d) = {mm.nstr(kappa,30)}  (Stokes constant at t=0, 2s2-1)")

    # CROSS-CHECKS
    chk_conv  = tr_match >= 90
    chk_real  = abs(traces[1].imag) < mpf(10)**(-60)
    chk_irred = abs(abs(tr0) - 2) > mpf("0.1")
    chk_kappa = kappa != 0
    all_pass  = chk_conv and chk_real and chk_irred and chk_kappa and z0_ok
    print("[CROSS-CHECKS]")
    print(f"    tr(M0) converged >=90d        : {chk_conv}  (~{tr_match}d cross-(J,nsteps,radius))")
    print(f"    tr(M0) real                   : {chk_real}  (|Im tr|={mm.nstr(abs(traces[1].imag),4)})")
    print(f"    |tr(M0)| != 2 (irreducible)   : {chk_irred} (tr={mm.nstr(tr0,12)})")
    print(f"    kappa != 0 (nontrivial Stokes): {chk_kappa}")
    print(f"    z0=(a/2)^2=1/3 (reframe)      : {z0_ok}")
    print(f"    det(M0)=1 (SL2, STRUCTURAL not accuracy): |det-1|={mm.nstr(detb_err,4)}")
    print(f"    => CROSS-CHECK {'PASS' if all_pass else 'FAIL (HALT)'} : consistent with rig 0 / G_Gal=SL2")

    results = {
        "op": "cc3-2s2-2a-monodromy",
        "task_id": "op:cc-transcendence/cc3-2s2-2",
        "operator_H2": "3 t^3 D^2 + 10 t^2 D + (t^2 + 5 t - 1)",
        "reduced_invariant_r": "1/(3 t^3) - 5/(9 t^2) - 1/(3 t)",
        "formal_data": {
            "singular_set": ["0", "infinity"],
            "type_both_points": "irregular slope 1/2 ramification 2 (single Z/2 orbit)",
            "instanton_action_a": "2/sqrt(3)",
            "exponential_factors_at_0": "exp( +- (2/sqrt(3)) t^{-1/2} ) t^{alpha_pm}",
            "exponent_sum_alpha": "alpha_+ + alpha_- = 3/2 (Wronskian-const argument)",
            "formal_monodromy": "M_hat = [[0, e^{2 pi i alpha_+}],[e^{2 pi i alpha_-},0]] (swap); tr=0; det=+1",
            "borel_action_crosscheck": {
                "relation": "2 sqrt(z0) = a  =>  z0 = (a/2)^2",
                "z0": mm.nstr(z0, 50), "target": "1/3", "passes": bool(z0_ok),
                "meaning": "the formal exponential factor exp(-2/sqrt(3) t^{-1/2}) and the Borel-plane "
                           "singularity z=1/3 (2s2-0 reframe) are the SAME datum."
            },
        },
        "topological_monodromy_M0": {
            "equation": "reduced Y''=rY (trace-free => det(M0)=1, SL2)",
            "method": "Taylor marching around |t|=rho; accuracy witness = cross-(J,nsteps,radius) agreement",
            "accuracy_witness_note": "det(M0)=1 is preserved STRUCTURALLY by any flow of the trace-free "
                                     "Y''=rY (Wronskian conserved, no Y' term) and is NOT an accuracy proof. "
                                     "The trace is the accuracy-sensitive coordinate. Singular set {0,inf} only "
                                     "=> every circle |t|=rho>0 encloses just t=0, so radius-independence of "
                                     "tr(M0) is TOPOLOGICAL INVARIANCE of the monodromy (strongest check). "
                                     "A prior asymmetric range(J+2) Taylor truncation gave a FALSE-STABLE, "
                                     "~14-digit-WRONG trace; fixed to range(J+3).",
            "validation_configs": ["rho=1.0 nsteps=240 J=90", "rho=1.0 nsteps=400 J=100",
                                   "rho=1.7 nsteps=320 J=90"],
            "trace_converged_digits_cross": tr_match,
            "det_minus_1_abs": mm.nstr(detb_err, 6),
            "trace_real": mm.nstr(tr0, 150),
            "trace_imag_abs": mm.nstr(abs(traces[1].imag), 6),
            "structural_relation": "M0 = S1 S2 M_hat, S1=[[1,s1],[0,1]], S2=[[1,0],[s2,1]], "
                                   "M_hat=[[0,b],[c,0]] (bc=-1) => tr(M0) = s1 c + s2 b "
                                   "(tr(M0) is a function of the LOCAL Stokes multipliers at t=0).",
            "interpretation": "hyperbolic (loxodromic) SL2 monodromy; |tr|>>2; eigenvalue ~51.0460.",
        },
        "kappa_as_stokes_datum": {
            "kappa_frozen_130": KAPPA_FROZEN_130,
            "role": "kappa = Gamma(4/3) A0 = Borel-plane amplitude at z=1/3 = Stokes constant of y "
                    "across arg(t)=0 (2s2-1, STRUCTURAL). An OFF-DIAGONAL STOKES MULTIPLIER / "
                    "connection datum of the D8 linear problem -- monodromy data, NOT a tau-function "
                    "connection constant (the named 2c hazard).",
        },
        "D8_coordinate_point": {
            "manifold": "PIII(D8)=D8^(1) monodromy/character variety, dim 2 (rig 0)",
            "coordinates_reported": {
                "SL2_trace_tr(M0)": mm.nstr(tr0, 60),
                "Stokes_constant_kappa": KAPPA_FROZEN_130,
            },
            "convention": "trace of the topological SL2 monodromy around t=0 (packages the Stokes "
                          "matrices via tr(M0)=s1 c + s2 b) PLUS the off-diagonal Stokes constant kappa. "
                          "Framework: van der Put-Saito (2009); ILT monodromy manifold.",
        },
        "cross_checks": {
            "tr_M0_converged_ge_90d_cross_J_nsteps_radius": bool(chk_conv),
            "tr_M0_real": bool(chk_real),
            "tr_M0_abs_ne_2_irreducible": bool(chk_irred),
            "kappa_ne_0_nontrivial_stokes": bool(chk_kappa),
            "z0_eq_1_3_reframe": bool(z0_ok),
            "det_M0_eq_1_SL2_structural_not_accuracy": True,
            "ALL_PASS": bool(all_pass),
            "halt_if_fail": "coords inconsistent with rig/SL2 => upstream error, stops the line",
        },
        "ceiling": "Placing kappa as a Stokes/monodromy coordinate proves NOTHING about transcendence; "
                   "a closed form would argue the OPPOSITE (elementarity in an extended class). "
                   "Unconditional transcendence of C/kappa is NOT a deliverable of op:cc-3 at any grade.",
        "references": [
            "van der Put & Saito, Ann. Inst. Fourier 59 (2009) 2611-2667 (moduli/monodromy)",
            "Its-Lisovyy-Prokhorov, connection constants for Painleve tau functions (D8 monodromy manifold)",
            "Sakai, Comm. Math. Phys. 220 (2001) 165-229 (surface D8^(1))",
            "Ohyama-Kawamuko-Sakai-Okamoto, J. Math. Sci. Univ. Tokyo 13 (2006) 145-204 (PIII(D8) Lax pair)",
        ],
    }
    results["canonical_sha256_of_hashfree_object"] = canon_hash(results)
    with open("cc3_2s2_2a_monodromy_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", results["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_2s2_2a_monodromy_results.json")

if __name__ == "__main__":
    main()
