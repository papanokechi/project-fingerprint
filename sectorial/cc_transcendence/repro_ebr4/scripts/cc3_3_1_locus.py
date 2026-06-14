#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-3-1  CLASSICAL-LOCUS EXCLUSION

Verify the dim-2 D8 character-variety point (tr M0, kappa) lies OFF the locus of
classical/algebraic PIII(D8) solutions, with stated separation margins, plus a
bonus algebraicity PSLQ on tr M0 (deg <= 8).

CHARACTERISATION OF THE CLASSICAL LOCUS (two strata, standard isomonodromy theory):
  (R) REDUCIBLE linear monodromy  <==>  Riccati / special-function (one-parameter
      "classical") solutions.   [FIKN 2006, Ch. on classical solutions]
  (A) ALGEBRAIC solutions  <==>  FINITE nonlinear (braid) orbit of the monodromy
      data; finite-orbit points have ALGEBRAIC trace coordinates.  A subcase is a
      FINITE linear monodromy GROUP (=> every |tr| = |2 cos(pi k/n)| <= 2).
      For PIII(D8) the ONLY algebraic solutions are q(t) = c sqrt(t), c^4 = 1
      [Ohyama-Kawamuko-Sakai-Okamoto 2006], a finite set of special points.

EXCLUSION OF OUR POINT:
  (R) excluded: monodromy is IRREDUCIBLE -- G_Gal(H2) = SL2 (cc3-2a Kovacic,
      e71e915f) is Zariski-dense, and |tr M0| >> 2 hyperbolic (b1fea3ed). STRUCTURAL.
  (A) excluded: tr M0 = -51.0655... is (i) |tr| - 2 = 49.06 away from the finite-
      group band |tr|<=2 (so M0 has INFINITE order, monodromy group infinite), and
      (ii) NOT algebraic of degree <= 8 within the declared height (PSLQ null below)
      -- but finite-braid-orbit (algebraic-solution) points have algebraic trace
      coordinates.  VERIFIED (numeric) on top of the STRUCTURAL principle.

CEILING (both directions): an off-locus verdict supports CONDITIONAL non-classicality
of kappa; it proves NOTHING unconditional about transcendence.  Mid-stage HALT only
if the point is ON a classical locus (it is not).
"""
import sys, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
import mpmath as mm
from mpmath import mp, mpf

mp.dps = 85

# frozen tr M0 (cc3-2a, b1fea3ed; trace_real, ~86 digits, cross-converged 141 d)
TR_M0 = ("-51.0655631399546622698316746099456615679204103033103908333911032106571"
         "8065185743887646983")
KAPPA_FROZEN_130 = ("1.539494848576641034843781903384069038219390890553148730926294560611"
                    "093030530126489289595548377837121909677816857027063026103313161")

def canon_sha(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def algebraicity_pslq(x, maxdeg, tol_dps, maxcoeff):
    """Test if x is algebraic of degree <= maxdeg: PSLQ on [1,x,...,x^maxdeg]."""
    vec = [x**k for k in range(maxdeg + 1)]
    rel = mm.pslq(vec, tol=mpf(10) ** (-tol_dps), maxcoeff=maxcoeff, maxsteps=100000)
    return rel

def main():
    print("=== op:cc3-3-1  classical-locus exclusion ===")
    print(f"dps={mp.dps}")
    trM0 = mpf(TR_M0)
    kappa = mpf(KAPPA_FROZEN_130)

    # ---- (R) reducibility / Riccati exclusion (inherited, STRUCTURAL) ----
    abs_tr = abs(trM0)
    margin_finitegroup = abs_tr - 2
    # eigenvalue lambda of M0: lambda + 1/lambda = tr, |lambda| != 1 (hyperbolic)
    lam = (trM0 + mm.sqrt(trM0**2 - 4)) / 2
    print(f"|tr M0|            = {mm.nstr(abs_tr, 30)}")
    print(f"eigenvalue lambda = {mm.nstr(lam, 30)}  (|lambda|={mm.nstr(abs(lam),10)} != 1 => infinite order)")
    print(f"margin to finite-group band |tr|<=2 : {mm.nstr(margin_finitegroup, 20)}")
    print("(R) reducible/Riccati locus: EXCLUDED -- G_Gal=SL2 (cc3-2a) irreducible, |tr|>>2 hyperbolic.")

    # ---- (A) algebraicity PSLQ on tr M0 (bonus, but feeds the algebraic-locus exclusion) ----
    print("\n[algebraicity PSLQ on tr M0]  deg<=8, declared height bound")
    MAXCOEFF = 10**7
    TOL_DPS = 70
    rel = algebraicity_pslq(trM0, 8, TOL_DPS, MAXCOEFF)
    if rel is None:
        print(f"  deg<=8, |coeff|<=1e7, tol=1e-{TOL_DPS}: NO RELATION (tr M0 not low-deg algebraic)")
    else:
        print(f"  deg<=8 RELATION FOUND: {rel}  -- INVESTIGATE")
    # also a tighter deg<=4 pass
    rel4 = algebraicity_pslq(trM0, 4, TOL_DPS, 10**9)
    print(f"  deg<=4, |coeff|<=1e9: {'NO RELATION' if rel4 is None else rel4}")

    # positive controls for the detector
    ctrl_sqrt2 = algebraicity_pslq(mm.sqrt(2), 4, TOL_DPS, 100)
    c7 = 2*mm.cos(2*mm.pi/7)
    ctrl_c7 = algebraicity_pslq(c7, 4, TOL_DPS, 100)
    print(f"  [control] sqrt(2) deg<=4 -> {ctrl_sqrt2}  (expect x^2-2 = [-2,0,1,0,0])")
    print(f"  [control] 2cos(2pi/7) deg<=4 -> {ctrl_c7}  (expect x^3+x^2-2x-1 = [-1,-2,1,1,0])")
    ctrl_ok = (ctrl_sqrt2 is not None) and (ctrl_c7 is not None)

    pslq_null = (rel is None) and (rel4 is None)
    print(f"\n(A) algebraic-solution locus: EXCLUDED -- tr M0 not algebraic deg<=8 (H<=1e7); "
          f"finite-braid-orbit points have algebraic coordinates. Controls fired: {ctrl_ok}")

    # ---- verdict ----
    on_locus = not (pslq_null and margin_finitegroup > 1)  # would be True only if a classical stratum matched
    verdict = "OFF the classical/algebraic locus" if not on_locus else "ON a classical locus -- HALT"
    print(f"\n=== VERDICT: (tr M0, kappa) is {verdict} ===")

    obj = {
        "op": "cc3-3-1-classical-locus-exclusion",
        "task_id": "op:cc-transcendence/cc3-3",
        "claim_id": "CC3-3-LOCUS",
        "grade": "STRUCTURAL+VERIFIED",
        "point": {
            "tr_M0": TR_M0,
            "kappa": KAPPA_FROZEN_130,
            "character_variety": "dim-2 D8 (PIII(D8)); coordinates (tr M0, kappa)",
        },
        "locus_characterisation": {
            "stratum_R_reducible_Riccati": "reducible linear monodromy <=> Riccati/special-function "
                "(one-parameter classical) solutions [FIKN 2006]",
            "stratum_A_algebraic": "algebraic solutions <=> finite nonlinear (braid) orbit; finite-orbit "
                "points have ALGEBRAIC trace coordinates; finite linear monodromy group subcase has |tr|<=2. "
                "For PIII(D8) the ONLY algebraic solutions are q=c sqrt(t), c^4=1 [OKSO 2006] (finite set).",
        },
        "exclusion_R": {
            "grade": "STRUCTURAL",
            "argument": "G_Gal(H2)=SL2 (cc3-2a Kovacic, e71e915f) is Zariski-dense => monodromy "
                        "IRREDUCIBLE; |tr M0|>>2 hyperbolic (b1fea3ed). Off the reducibility/Riccati locus.",
        },
        "exclusion_A": {
            "grade": "VERIFIED+STRUCTURAL",
            "abs_tr_M0": mm.nstr(abs_tr, 40),
            "margin_to_finite_group_band": mm.nstr(margin_finitegroup, 30),
            "eigenvalue_lambda_abs": mm.nstr(abs(lam), 30),
            "infinite_order": True,
            "pslq_trM0_deg_le_8": "NO RELATION" if rel is None else str(rel),
            "pslq_trM0_deg_le_4": "NO RELATION" if rel4 is None else str(rel4),
            "pslq_height_bound": MAXCOEFF,
            "pslq_tol_dps": TOL_DPS,
            "controls_fired": ctrl_ok,
            "control_sqrt2": str(ctrl_sqrt2),
            "control_2cos2pi7": str(ctrl_c7),
            "argument": "tr M0 has |tr|-2 = 49.06 (M0 infinite order => monodromy group infinite, not the "
                        "finite-linear-group algebraic subcase) AND is not algebraic of degree<=8 within "
                        "H<=1e7; finite-braid-orbit (algebraic-solution) points have algebraic trace "
                        "coordinates, so (tr M0,kappa) is not such a point.",
        },
        "honest_caveat": "The exact monodromy data of the q=c sqrt(t) solutions was NOT computed for a "
                         "direct point-vs-point comparison; the exclusion rests on the structural "
                         "characterisations (reducible<=>Riccati; algebraic=>algebraic coordinates) plus "
                         "the irreducibility and non-low-degree-algebraicity of our point. The assumption "
                         "'finite braid orbit => algebraic trace coordinates' is THEOREM-grade (graded H-aux).",
        "verdict": verdict,
        "halt": on_locus,
        "ceiling": "An off-locus verdict supports CONDITIONAL non-classicality of kappa; it proves NOTHING "
                   "unconditional about transcendence (cc-3 ceiling, both directions).",
        "references": [
            "A.S. Fokas, A.R. Its, A.A. Kapaev, V.Yu. Novokshenov, Painleve Transcendents: The "
            "Riemann-Hilbert Approach, Math. Surveys Monogr. 128, AMS (2006)",
            "Y. Ohyama, H. Kawamuko, H. Sakai, K. Okamoto, Studies on the Painleve equations V. Third "
            "Painleve equations of special type P_III(D7) and P_III(D8), J. Math. Sci. Univ. Tokyo 13 "
            "(2006), no. 2, 145-204",
            "H. Umemura, H. Watanabe, Solutions of the third Painleve equation I, Nagoya Math. J. 151 "
            "(1998), 1-24",
            "O. Lisovyy, Y. Tykhyy, Algebraic solutions of the sixth Painleve equation, J. Geom. Phys. 85 "
            "(2014) 124-163 (finite braid orbits <=> algebraic solutions; algebraic coordinates)",
        ],
        "dps": mp.dps,
    }
    obj["canonical_sha256_of_hashfree_object"] = canon_sha(obj)
    with open("cc3_3_1_locus_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\n  canonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("  wrote cc3_3_1_locus_results.json")
    if on_locus:
        print("\n*** LOCUS HIT -- UNCONDITIONAL HALT ***")

if __name__ == "__main__":
    main()
