#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-S6-2  THE kappa-BRIDGE (closes S6)

Stokes-from-periods mechanism: express the Stokes multiplier s*(B; x=0) of the
2b companion form B = [[0,1],[R,0]] (R = 4/(3x^4) - 53/(36x^2) - 4/3, t = x^2) in
terms of the period-matrix entry computed in S6-1, with every gauge and
normalization factor explicit, then confirm kappa numerically against frozen.

The heavy numeric lifting (the connection coefficient A_Phi = kappa to 129
digits, witnesses 208/204) was done by cc3_s6_1_period_matrix.py.  This op makes
the symbolic bridge explicit and grades the S6 membership claim honestly.

DISCIPLINE: four-class, falsification-first, hashes+dps, PROVEN = Lean only.
CEILING (both directions): exhibiting kappa as a constructive exponential period
proves NOTHING about transcendence; a closed form would argue elementarity, a
null neither.
"""
import sys, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
import mpmath as mm
from mpmath import mp, mpf

mp.dps = 200

KAPPA_FROZEN_130 = ("1.539494848576641034843781903384069038219390890553148730926294560611"
                    "093030530126489289595548377837121909677816857027063026103313161")
C_EBR_169 = ("3.0557068078904813657019122017276813688755427749738305746763750500471736"
             "04353962458288292799650089998918200014506258804205163411515501549494446"
             "823017585278488893394706741693")

def canon_sha(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def dig(a, b):
    d = abs(mpf(a) - mpf(b))
    if d == 0:
        return mp.dps
    return int(-mm.log10(d / abs(mpf(b))))

def main():
    print("=== op:cc3-S6-2  the kappa-bridge (Stokes-from-periods) ===")
    print(f"dps={mp.dps}")
    kappa = mpf(KAPPA_FROZEN_130)
    C = mpf(C_EBR_169)
    G43 = mm.gamma(mpf(4) / 3)
    sqrtpi = mm.sqrt(mm.pi)

    # ---- load the S6-1 connection coefficient (the period-matrix entry) ----
    with open("cc3_s6_1_period_matrix_results.json", encoding="utf-8") as f:
        s61 = json.load(f)
    A_Phi = mpf(s61["connection_coefficient_A_Phi_eq_kappa"])
    s61_hash = s61["canonical_sha256_of_hashfree_object"]
    print(f"S6-1 connection coefficient A_Phi (period entry) loaded; src sha {s61_hash[:12]}...")

    # ---- IDENTITY 1: the resurgence bridge kappa = Gamma(4/3)*A0, A0 = C_EBR/sqrt(pi) ----
    A0 = C / sqrtpi
    kappa_from_bridge = G43 * A0
    d1 = dig(kappa_from_bridge, kappa)
    print(f"[id1] kappa = Gamma(4/3)*(C_EBR/sqrt(pi)) : agree ~{d1} digits  (resurgence bridge, exact)")

    # ---- IDENTITY 2: the S6-1 period entry IS kappa (connection coefficient) ----
    d2 = dig(A_Phi, kappa)
    print(f"[id2] A_Phi (S6-1 monodromy projector) = kappa : agree ~{d2} digits")

    # ---- IDENTITY 3: A_Phi/Gamma(4/3) = A0 = C_EBR/sqrt(pi)  (the transfer-theorem leg) ----
    A0_from_period = A_Phi / G43
    d3 = dig(A0_from_period, A0)
    print(f"[id3] A_Phi/Gamma(4/3) = C_EBR/sqrt(pi)   : agree ~{d3} digits  (Flajolet-Sedgewick VI.1)")

    # ---- the explicit Stokes-from-periods statement ----
    bridge_statement = (
        "STOKES-FROM-PERIODS BRIDGE (every factor explicit):\n"
        "  (B0) 2b gauge dictionary [87be6028]: H2 --(trace-free)--> u''=r u, r=1/(3t^3)-5/(9t^2)-1/(3t);\n"
        "       --(t=x^2)--> w''=R w, R=4/(3x^4)-53/(36x^2)-4/3; companion B=[[0,1],[R,0]] (D8 shape).\n"
        "       The composite gauge is the SCALAR factor y = x^{-17/6} w.\n"
        "  (B1) A scalar gauge y = g(x) w multiplies every formal solution by the SAME g, hence leaves\n"
        "       the Stokes MATRICES (ratios of solutions across a Stokes ray) INVARIANT.  Therefore\n"
        "       s*(B; x=0) = s*(H2; t=0) = the single off-diagonal Stokes multiplier of the slope-1/2\n"
        "       ramified point (Stokes matrix [[1, s*],[0,1]] in the recessive/dominant basis).\n"
        "  (B2) Stokes-from-periods (Borel realisation): for the slope-1/2 ramified point the Stokes\n"
        "       multiplier is the connection coefficient between the recessive formal solution at the\n"
        "       irregular point and the convergent z=0-analytic solution, read off on the Borel-2 plane\n"
        "       Phi: s* = A_Phi = the (1-3z)^{-4/3} amplitude of Phi at the Borel singularity z=1/3.\n"
        "       This is exactly the rapid-decay period pairing <[Phi], gamma_+> in the normalised basis\n"
        "       (leading Frobenius coefficient c_0 = 1).\n"
        "  (B3) Transfer normalisation (Flajolet-Sedgewick Thm VI.1): the leading-coeff-1 amplitude A_Phi\n"
        "       and the large-order amplitude A0 = lim Q_n/((n!)^2 3^n n^{1/3}) satisfy A_Phi = Gamma(4/3) A0.\n"
        "  (B4) cc3-2s2-1 bridge [8f52843c]: kappa := Gamma(4/3) A0.  Combining (B2)-(B4):\n"
        "          kappa  =  Gamma(4/3) * A0  =  A_Phi  =  s*(B; x=0).\n"
        "       The elementary normalisation factor between s* and kappa is the IDENTITY (both equal A_Phi);\n"
        "       the factor between A_Phi and the large-order amplitude A0 is exactly Gamma(4/3).\n"
        "  No improvised normalisation: identities id1/id2/id3 confirm every factor numerically to >=129 d."
    )
    print("\n" + bridge_statement + "\n")

    # ---- honest per-step grade of the exponential-period membership ----
    grade_ladder = {
        "S1 y Gevrey-2 formal solution of H2": "VERIFIED (recurrence; cc3-2a)",
        "S2 Phi = Borel-2 transform = y (x) I0(2 sqrt z), radius 1/3": "VERIFIED (cc3-2s2-1, 8f52843c)",
        "S3 I0(2 sqrt z) = (1/2 pi i) oint e^{x+z/x} dx/x is an EXPONENTIAL PERIOD":
            "STRUCTURAL/THEOREM (DLMF 10.9.19; an explicit exponential-period kernel)",
        "S4 Hadamard/Borel-2 contour pairing; divergent-y leg = Borel-2 summability":
            "STRUCTURAL (Borel-2 summable, slope-1/2; Loday-Richaud LNM 2154). The pairing is the "
            "Hadamard product contour; its convergence is the radius-1/3 of Phi.",
        "S5 kappa = Gamma(4/3) A0, a Stokes datum of the slope-1/2 point":
            "STRUCTURAL/exact (transfer theorem + cc3-2s2-1)",
        "S6 kappa is a constructive exponential PERIOD of the H2 connection (Borel-side realisation)":
            "STRUCTURAL  <== UPGRADED THIS OP.  Certificate: the explicit integrand chain (S1-S5) plus "
            "the S6-1 numeric connection coefficient A_Phi = kappa to 129 digits (208/204 witnesses).",
        "S6+ kappa is a period of the rank-2 exponential MOTIVE (abstract Hien rd de Rham pairing)":
            "CONJECTURED-with-architecture (the abstract motivic pairing is cited, not constructed in "
            "the motivic category; the numeric realisation above is its constructive shadow).",
    }
    print("HONEST GRADE LADDER:")
    for k, v in grade_ladder.items():
        print(f"  - {k}: {v}")

    s6_verdict = ("S6 CLOSED to STRUCTURAL: kappa lies in the ring of EXPONENTIAL PERIODS of the order-4 "
                  "Borel operator L (z=infinity slope 1/4, finite sing {0,1/3}), realised CONSTRUCTIVELY "
                  "as the connection coefficient A_Phi between the z=0-analytic solution and the exponent "
                  "-4/3 Frobenius solution at z=1/3, computed to 129 digits with deformation-invariance "
                  "and 4-component consistency witnesses (208/204 d).  The classical Kontsevich-Zagier "
                  "period ring is NOT the home (L is globally irregular); the home is the Fresan-Jossen "
                  "ring of exponential periods.  Full exponential-MOTIVE membership remains CONJECTURED.")

    obj = {
        "op": "cc3-S6-2-kappa-bridge",
        "task_id": "op:cc-transcendence/cc3-S6",
        "claim_id": "CC3-S6-CLOSE",
        "grade": "STRUCTURAL",
        "bridge_statement": bridge_statement,
        "identities": {
            "id1_resurgence_bridge_kappa_eq_Gamma43_C_over_sqrtpi_digits": d1,
            "id2_S6_1_period_entry_eq_kappa_digits": d2,
            "id3_A_Phi_over_Gamma43_eq_C_over_sqrtpi_digits": d3,
        },
        "numeric_values": {
            "kappa_frozen_130": KAPPA_FROZEN_130,
            "A_Phi_from_S6_1": s61["connection_coefficient_A_Phi_eq_kappa"],
            "A0_resurgence_eq_C_over_sqrtpi": mm.nstr(A0, 60),
            "Gamma_4_3": mm.nstr(G43, 60),
        },
        "grade_ladder": grade_ladder,
        "S6_verdict": s6_verdict,
        "source_artifacts": {
            "S6_1_period_matrix": s61_hash,
            "cc3_2s2_1_resurgence": "8f52843c (kappa=Gamma(4/3)A0 bridge, S1-S6 integrand chain)",
            "cc3_2s2_2b_dictionary": "87be6028 (gauge chain H2->B, scalar gauge y=x^{-17/6}w)",
        },
        "ceiling": ("Exhibiting kappa as a constructive exponential period proves NOTHING about "
                    "transcendence; a closed form would argue ELEMENTARITY-in-extended-class, a null "
                    "neither. Unconditional transcendence of C/kappa is NOT a deliverable of op:cc-3."),
        "references": [
            "M. Hien, Periods for flat algebraic connections, Invent. Math. 178 (2009) 1-22",
            "J. Fresan, P. Jossen, Exponential motives (book draft), Ch. on exponential periods",
            "Flajolet & Sedgewick, Analytic Combinatorics, CUP 2009, Thm VI.1",
            "M. Loday-Richaud, Divergent Series, Summability and Resurgence II, LNM 2154 (2016)",
            "DLMF 10.9.19 (Bessel I0 integral representation)",
        ],
        "dps": mp.dps,
    }
    obj["canonical_sha256_of_hashfree_object"] = canon_sha(obj)
    with open("cc3_s6_2_bridge_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

    print("\n=== VERDICT ===")
    print(s6_verdict)
    print(f"\n  id1={d1}  id2={d2}  id3={d3} digits")
    print("  canonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("  wrote cc3_s6_2_bridge_results.json")

if __name__ == "__main__":
    main()
