#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-2s2-2c  --  FORMULA COVERAGE for kappa's D8 coordinate  (SURVEY mode)
================================================================================
SIARC.  2b returned an OBSTRUCTION (no symbolic match of the companion D8 system
B(x) to a parametrized published PIII(D8) Lax A(lambda,s): the isomonodromy-time
inverse problem is transcendental).  Per spec, 2c therefore runs in SURVEY mode:
inventory the solved D8 connection problems, state EXACTLY what each theorem
computes and in which coordinates, separate THEOREM / conjecture / folklore with
locators, and return the three-way verdict (i) COVERED / (ii) ADJACENT /
(iii) NOT COVERED -- WITHOUT asserting a parametrized match.

NAMED HAZARD (reproduced in EVERY crossing paragraph below): tau-function
connection constants != Lax-solution Stokes data.  kappa is a LAX-side Stokes
multiplier (2a/2b: off-diagonal Stokes multiplier of B at x=0).  The ILT and
Gavrylenko-Lisovyy theorems compute a TAU-side connection constant / tau function
as a Barnes-G / Fredholm function OF the monodromy data.  kappa is an INPUT
(argument) to those formulas, never their OUTPUT.

This script asserts NO closed form for kappa and evaluates NO literature formula
numerically (none is instantiable at our point -- see verdict).  Hence there is
no FIRE and no HALT.  It re-confirms only the FROZEN bridge as an anchor.

CEILING (both directions, verbatim): even a COVERED verdict with a closed form
would prove the OPPOSITE of transcendence (elementarity in an extended class);
a NOT COVERED / NULL proves neither.  Unconditional transcendence of C/kappa is
NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import mpmath as mm
from mpmath import mp, mpf

mp.dps = 175

KAPPA_FROZEN_130 = ("1.539494848576641034843781903384069038219390890553148730926294560611"
                    "093030530126489289595548377837121909677816857027063026103313161")
C_EBR_169 = ("3.055706807890481365701912201727681368875542774973830574676375050047"
             "173604353962458288292799650089998918200014506258804205163411515501549494446823017585278488893394706741693")

def canon_hash(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def main():
    print("=== cc3-2s2-2c  formula coverage for kappa (SURVEY mode) ===")

    # ---- anchor: re-confirm the frozen bridge kappa = Gamma(4/3) C_EBR/sqrt(pi) ----
    A0 = mpf(C_EBR_169)/mm.sqrt(mm.pi)
    kappa_bridge = mm.gamma(mpf(4)/3)*A0
    agree = -int(mm.log10(abs(kappa_bridge - mpf(KAPPA_FROZEN_130))))
    print(f"[anchor] kappa = Gamma(4/3) C_EBR/sqrt(pi): agrees frozen-130 to ~{agree} digits")
    print("[anchor] => kappa's ONLY known closed form is in terms of C_EBR (the OPEN constant);")
    print("         this is circular and NOT an independent elementary/Barnes reduction.")

    # ---- literature inventory ----
    inventory = [
        {
            "id": "ILT-tau-connection-constant",
            "reference": "Its, Lisovyy, Prokhorov, 'Monodromy dependence and connection constants "
                         "for Painleve tau functions', Comm. Math. Phys. 363 (2018) 1-58; with the "
                         "PIII(D6)/(D8) and degenerate cases in Its-Lisovyy-Tykhyy and the Painleve/CFT line.",
            "what_it_computes": "the CONNECTION CONSTANT chi of a Painleve tau function: the explicit "
                                "constant prefactor relating the t->0 and t->infinity asymptotic "
                                "expansions of tau(t), given as a product of Barnes G- and Gamma-functions "
                                "of the monodromy data.",
            "coordinates": "monodromy data (formal-monodromy exponents / Stokes data) as ARGUMENTS; "
                           "output = Barnes-G expression IN those arguments.",
            "grade": "THEOREM (for the cases proved; the connection-constant program is rigorous).",
            "relation_to_kappa": "TAU-SIDE object. kappa (LAX-side Stokes multiplier) is an INPUT to such "
                                 "a formula, NOT its output. [tau-vs-Lax hazard: named.] No instantiation at "
                                 "our point is possible without first fixing our PIII(D8) member (2b obstruction).",
        },
        {
            "id": "GL-Fredholm-tau",
            "reference": "Gavrylenko, Lisovyy, 'Fredholm determinant and Nekrasov sum representations of "
                         "isomonodromic tau functions', Comm. Math. Phys. 363 (2018) 1-58 (and CMP 2016/2018 "
                         "companion); Cafasso-Gavrylenko-Lisovyy for irregular/Painleve III-V.",
            "what_it_computes": "the isomonodromic tau function as a Fredholm determinant det(1-K) of an "
                                "integral operator K assembled FROM the monodromy data; plus Nekrasov-type "
                                "combinatorial series.",
            "coordinates": "monodromy data -> tau function (a function ON the monodromy manifold).",
            "grade": "THEOREM.",
            "relation_to_kappa": "TAU-SIDE object. Again monodromy (the kappa-analog) is INPUT; tau is OUTPUT. "
                                 "[tau-vs-Lax hazard: named.] Provides no closed form FOR a Stokes multiplier.",
        },
        {
            "id": "linear-ODE-forward-connection-problem",
            "reference": "General irregular-connection theory (Sibuya; Fokas-Its-Kapaev-Novokshenov, AMS "
                         "Surveys Monogr. 128 (2006)); rigid local systems (Katz, 'Rigid Local Systems', 1996).",
            "what_it_computes": "Stokes multipliers of a given 2nd-order ODE in closed form ONLY for RIGID "
                                "local data (hypergeometric / Bessel / Airy / Kummer), where the connection "
                                "matrix is a Gamma-quotient.",
            "coordinates": "the ODE's local data -> Stokes/connection matrix.",
            "grade": "THEOREM for rigid cases; OPEN (transcendental) in general.",
            "relation_to_kappa": "H2 is NON-RIGID (rig(H2)=0, CC3-2S2-RIG), so it is NOT in the rigid "
                                 "closed-form catalogue. Computing kappa from H2 is exactly the (generically "
                                 "unsolved) connection problem. LAX-side, but no closed-form theorem applies.",
        },
    ]
    for item in inventory:
        print(f"\n[{item['id']}] grade={item['grade']}")
        print(f"    computes: {item['what_it_computes'][:96]}...")
        print(f"    vs kappa: {item['relation_to_kappa'][:96]}...")

    # ---- three-way verdict ----
    verdict = {
        "choice": "(iii) NOT COVERED",
        "reasoning": [
            "The solved D8 problems (ILT connection constant; Gavrylenko-Lisovyy Fredholm/Nekrasov) all "
            "compute a TAU-SIDE quantity (connection constant chi, or tau itself) as a Barnes-G / Fredholm "
            "function OF the monodromy data. kappa is a LAX-SIDE Stokes multiplier serving as an INPUT to "
            "those formulas; it is never their OUTPUT. [tau-vs-Lax: named.]",
            "No theorem outputs a closed form for a Stokes multiplier of a NON-RIGID 2nd-order ODE; H2 is "
            "non-rigid (rig=0), so it is outside the rigid (hypergeometric/Bessel) closed-form catalogue.",
            "Even ADJACENT use of ILT is blocked: instantiating the connection-constant formula at OUR "
            "point requires fixing the PIII(D8) member (the 2b obstruction: isomonodromy-time inverse "
            "problem, transcendental). And even instantiated, ILT would yield the tau-connection-constant, "
            "a DIFFERENT coordinate than kappa.",
            "kappa's only known closed form is kappa = Gamma(4/3) C_EBR/sqrt(pi) (frozen, re-confirmed here "
            "to ~129 digits), which is CIRCULAR: C_EBR is the open constant. No INDEPENDENT elementary or "
            "Barnes reduction is provided by the literature.",
        ],
        "precise_gap": "Which coordinate: the x=0 off-diagonal Stokes multiplier s_*(B) of the companion D8 "
                       "linear system (= kappa up to a Gamma(alpha_pm) amplitude<->multiplier factor). What "
                       "the literature solves instead: the tau-side connection constant chi(monodromy) and "
                       "the tau function det(1-K)(monodromy). The missing object is a closed form FOR the "
                       "Lax-side Stokes multiplier of our specific non-rigid member.",
        "no_candidate_closed_form": True,
        "no_formula_evaluated_numerically": True,
        "FIRE": False,
        "HALT": False,
    }
    print("\n[VERDICT] ", verdict["choice"])
    for r in verdict["reasoning"]:
        print("   -", r[:110], "...")
    print("[VERDICT] no candidate closed form for kappa => no numerical evaluation, no FIRE, no HALT.")
    print("[ROUTING] 2s2-3 runs a STANDARD (non-formula-motivated) log-space Barnes battery; expected NULL.")

    results = {
        "op": "cc3-2s2-2c-coverage",
        "task_id": "op:cc-transcendence/cc3-2s2-2",
        "mode": "SURVEY (2b obstruction: no parametrized published-Lax match)",
        "anchor_bridge": {
            "identity": "kappa = Gamma(4/3) * C_EBR / sqrt(pi)",
            "frozen_kappa_130": KAPPA_FROZEN_130,
            "agreement_digits": agree,
            "note": "kappa's only known closed form is in terms of C_EBR (the OPEN constant) => circular, "
                    "not an independent reduction.",
        },
        "literature_inventory": inventory,
        "named_hazard_tau_vs_lax": "kappa is LAX-side (Stokes multiplier / monodromy data). ILT & "
            "Gavrylenko-Lisovyy compute TAU-side objects (connection constant chi, tau function) as "
            "Barnes-G/Fredholm functions OF the monodromy. kappa is INPUT, never OUTPUT. Named in every "
            "crossing paragraph above.",
        "three_way_verdict": verdict,
        "transcribed_formulas_used_numerically": "NONE (survey mode; no formula instantiable at our point).",
        "ceiling": "A COVERED closed form would argue ELEMENTARITY (extended class), not transcendence; a "
                   "NOT COVERED/NULL proves neither. Unconditional transcendence of C/kappa is NOT a "
                   "deliverable of op:cc-3 at any grade.",
    }
    results["canonical_sha256_of_hashfree_object"] = canon_hash(results)
    with open("cc3_2s2_2c_coverage_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", results["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_2s2_2c_coverage_results.json")

if __name__ == "__main__":
    main()
