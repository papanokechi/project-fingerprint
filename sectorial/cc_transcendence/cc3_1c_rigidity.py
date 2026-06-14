#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1c-2  --  IRREGULAR INDEX OF RIGIDITY of L  (the fork decider)
================================================================================
SIARC.  Assembles the index of rigidity of Phi's operator L from the EXACT local
data established in cc3-1b (Riemann scheme) and cc3-1c (monodromy + Frobenius):

  rig(E) = (2 - #S) n^2  +  sum_{x in S} dimZ(formal_type)_x  -  sum_{x in S} irr_x(End E)

with the convention  rig = 2 - dim H^1(P^1, j_{!*} End E),  so  rigid  <=>  rig = 2,
and for an IRREDUCIBLE connection  rig <= 2  always.  At a regular-singular point
dimZ(formal)_x = dimZ(M_x) (centraliser of the local monodromy) and irr_x = 0.

References (VERIFIED-by-citation, never silently load-bearing):
  - S. Bloch, H. Esnault, "Local Fourier transforms and rigidity for D-modules",
    Asian J. Math. 8 (2004) 587-606  (irregular Euler-characteristic / rigidity).
  - D. Arinkin, "Rigid irregular connections on P^1", Compositio Math. 146 (2010)
    1323-1338  (index of rigidity for irregular connections; rig <= 2 for irred).
  - K. Jakob, Z. Yun, classification of rigid irregular connections (local datum
    bookkeeping: slopes, formal types, centraliser dimensions).
  - N. Katz, "Rigid Local Systems", Ann. of Math. Studies 139 (1996)  -- the
    FUCHSIAN rigidity theory; cited only to contrast (it does NOT apply: L is
    irregular at infinity).

The three Fuchsian/irregular POSITIVE CONTROLS (Airy, Gauss 2F1, Bessel) are all
classically rigid; the script asserts the formula returns rig=2 for each before
trusting it on L2 and L.

CEILING (reproduced): a Fuchsian relocation does not make K a classical period;
provenance, not singularity type, is what the period conjectures see; rigidity, if
found, only sharpens the period home.  Unconditional transcendence of C is NOT a
deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from fractions import Fraction as Fr

def dimZ_from_blocks(blocks_per_eigen):
    """dim of the centraliser of a matrix whose Jordan block sizes, grouped by
    eigenvalue, are given.  For one eigenvalue with block sizes d_1..d_r,
    dimZ = sum_{i,j} min(d_i,d_j).  Distinct eigenvalues add."""
    total = 0
    for blocks in blocks_per_eigen:
        for di in blocks:
            for dj in blocks:
                total += min(di, dj)
    return total

def rigidity(n, points):
    """points: list of dicts with keys
         'name', 'dimZ_formal' (int), 'irr_End' (Fraction or int).
       #S = len(points).  Returns rig and the term breakdown."""
    S = len(points)
    n2 = n * n
    term_topo = (2 - S) * n2
    sum_dimZ = sum(p["dimZ_formal"] for p in points)
    sum_irr = sum(Fr(p["irr_End"]) for p in points)
    rig = term_topo + sum_dimZ - sum_irr
    return rig, {"(2-#S)n^2": term_topo, "sum dimZ_formal": sum_dimZ,
                 "sum irr_End": str(sum_irr), "#S": S, "n": n}

def show(label, n, points):
    rig, br = rigidity(n, points)
    print(f"\n[{label}]  n={n}, #S={len(points)}")
    for p in points:
        print(f"    {p['name']:<26} dimZ_formal={p['dimZ_formal']:>3}  "
              f"irr_End={str(Fr(p['irr_End'])):>4}   ({p.get('note','')})")
    print(f"    rig = (2-{br['#S']})*{n*n} + {br['sum dimZ_formal']} - {br['sum irr_End']} "
          f"= {rig}   => {'RIGID' if rig==2 else ('NON-RIGID, accessory '+str(2-rig)) if rig<2 else 'INCONSISTENT(>2)'}")
    return rig, br

def main():
    print("=== cc3-1c-2  Irregular index of rigidity (formula + controls) ===")

    # ---------- POSITIVE CONTROLS (all classically rigid: rig must be 2) ----------
    # Airy  y'' = z y :  only singularity infinity, slope 3/2, ram 2, irreducible
    # formal type => dimZ(formal)_inf = 1; End(E) rank 4 has 2 nonzero exponential
    # differences of slope 3/2 => irr_inf(End) = 2*(3/2) = 3.
    airy = [dict(name="infinity (slope 3/2)", dimZ_formal=1, irr_End=Fr(3),
                 note="2 diffs * 3/2")]
    r_airy, _ = show("Airy (control)", 2, airy)
    assert r_airy == 2, "Airy control failed"

    # Gauss 2F1 : S={0,1,infinity}, all regular singular, generic (distinct
    # eigenvalues) local monodromy => dimZ(M_x)=2 each, irr=0.
    gauss = [dict(name="0 (reg, distinct)", dimZ_formal=2, irr_End=0),
             dict(name="1 (reg, distinct)", dimZ_formal=2, irr_End=0),
             dict(name="infinity (reg, distinct)", dimZ_formal=2, irr_End=0)]
    r_g, _ = show("Gauss 2F1 (control)", 2, gauss)
    assert r_g == 2, "Gauss control failed"

    # Bessel (order 2): S={0 (reg sing, exponents +-nu distinct => dimZ=2),
    # infinity (slope 1, two distinct exponentials e^{+- i z})}.  At infinity the
    # formal type is a sum of two distinct rank-1 pieces => dimZ(formal)=2, and
    # End has 2 nonzero differences of slope 1 => irr=2.
    bessel = [dict(name="0 (reg, distinct)", dimZ_formal=2, irr_End=0),
              dict(name="infinity (slope 1)", dimZ_formal=2, irr_End=Fr(2),
                   note="2 diffs * 1")]
    r_b, _ = show("Bessel (control)", 2, bessel)
    assert r_b == 2, "Bessel control failed"

    # ---------- L2 (the EBR Borel operator, internal consistency) ----------
    # n=4. S={0, 4/3, infinity}.  cc2-2d: M_0 semisimple {1,-1,1,-1} (eigenvalues
    # 1,1 and -1,-1, each semisimple) => blocks [1,1] & [1,1] => dimZ=2^2+2^2=8;
    # M_R pseudo-reflection {1,1,1,e^{i pi/3}} semisimple => eig 1 blocks [1,1,1]
    # (9) + e^{i pi/3} block [1] (1) => dimZ=10.  infinity slope 1/4 ram 4 single
    # orbit => dimZ(formal)=1, irr(End)=12*(1/4)=3 (12/4 split).
    L2 = [dict(name="s=0 (semisimple {1,-1})", dimZ_formal=dimZ_from_blocks([[1,1],[1,1]]),
               irr_End=0, note="dimZ=2^2+2^2=8"),
          dict(name="s=4/3 (pseudo-reflection)", dimZ_formal=dimZ_from_blocks([[1,1,1],[1]]),
               irr_End=0, note="dimZ=3^2+1=10"),
          dict(name="infinity (slope 1/4, ram 4)", dimZ_formal=1, irr_End=Fr(3),
               note="12 diffs * 1/4 = 3")]
    r_L2, _ = show("L2 (EBR Borel op, internal check)", 4, L2)

    # ---------- L (Phi's operator) -- the target ----------
    # n=4. S={0, 1/3, infinity}.
    #  z=0:    exponents {0,0,1,1}; monodromy unipotent (eig 1, alg mult 4).
    #          EXACT Frobenius (cc3_1c_frobenius_z0_v2.py, 4482b99a...): Jordan [2,2]
    #          => dimZ = sum min over [2,2] = 8.  (numerical: rank(M0-I)=2 confirms 2 blocks)
    #  z=1/3:  exponents {-4/3,0,1,2}; eig 1 (mult 3) semisimple [1,1,1] (rank(M-I)=1,
    #          cc3_1c_monodromy.py) + isolated eig e^{-2pi i/3} (mult 1) block [1]
    #          => dimZ = 3^2 + 1 = 10.
    #  inf:    slope 1/4, ram 4, single Galois orbit (lambda^4=-256/3) => irreducible
    #          formal type, dimZ(formal)=1; End(E) has 12 nonzero exponential diffs of
    #          slope 1/4 => irr(End) = 12*(1/4) = 3  (the 12/4 split).
    z0_blocks = [[2, 2]]
    z13_blocks = [[1, 1, 1], [1]]
    L = [dict(name="z=0 (Jordan [2,2], logs)", dimZ_formal=dimZ_from_blocks(z0_blocks),
              irr_End=0, note="Frobenius EXACT: [2,2], dimZ=8"),
         dict(name="z=1/3 (ss [1,1,1] + omega)", dimZ_formal=dimZ_from_blocks(z13_blocks),
              irr_End=0, note="rank(M-I)=1 => dimZ=10"),
         dict(name="infinity (slope 1/4, ram 4)", dimZ_formal=1, irr_End=Fr(3),
              note="12 diffs * 1/4 = 3")]
    r_L, br_L = show("L (Phi operator) -- TARGET", 4, L)

    # irreducibility sanity: irreducible => rig <= 2
    irred_ok = (r_L <= 2)
    print("\nirreducibility sanity (irreducible => rig <= 2):",
          "OK" if irred_ok else "VIOLATED -- ERROR IN LOCAL DATA")
    assert irred_ok, "rig > 2 contradicts irreducibility"

    verdict = "RIGID" if r_L == 2 else ("NON-RIGID" if r_L < 2 else "INCONSISTENT")
    accessory = 2 - r_L

    obj = {
        "op": "cc3-1c-2-rigidity",
        "task_id": "op:cc-transcendence/cc3-1c",
        "formula": "rig = (2-#S) n^2 + sum_x dimZ(formal)_x - sum_x irr_x(End E); rigid <=> rig=2",
        "convention": "rig = 2 - dim H^1(P^1, j_{!*} End E); irreducible => rig <= 2",
        "controls": {
            "Airy": {"rig": int(r_airy), "expected": 2},
            "Gauss_2F1": {"rig": int(r_g), "expected": 2},
            "Bessel": {"rig": int(r_b), "expected": 2},
            "all_pass": bool(r_airy == 2 and r_g == 2 and r_b == 2),
        },
        "L2_internal_check": {"rig": int(r_L2), "note": "EBR Borel operator; non-rigid, accessory 2"},
        "L": {
            "n": 4, "singular_set": ["0", "1/3", "infinity"],
            "local_data": {
                "z=0": {"exponents": [0, 0, 1, 1], "jordan_eig1": [2, 2], "dimZ": dimZ_from_blocks(z0_blocks),
                        "source": "exact Frobenius cc3_1c_frobenius_z0_v2.py 4482b99af1c1f673a80cdebc768f808b431f37b2958ddf8c7173f1def608b8ee"},
                "z=1/3": {"exponents": ["-4/3", 0, 1, 2], "jordan_eig1": [1, 1, 1],
                          "isolated_eig": "e^{-2 pi i/3}", "dimZ": dimZ_from_blocks(z13_blocks),
                          "source": "numerical monodromy cc3_1c_monodromy.py rank(M-I)=1"},
                "infinity": {"slope": "1/4", "ramification": 4, "lambda4": "-256/3",
                             "dimZ_formal": 1, "irr_End": 3, "split": "12 nonzero diffs * 1/4 = 3"},
            },
            "term_breakdown": {k: (str(v) if isinstance(v, Fr) else v) for k, v in br_L.items()},
            "index_of_rigidity": int(r_L),
            "verdict": verdict,
            "accessory_parameter_count_2_minus_rig": int(accessory),
        },
        "irreducibility": "single slope-1/4 ramification-4 Galois orbit at infinity => irreducible formal type => no proper global subconnection => irreducible; consistent with rig <= 2.",
        "supersedes_cc3_1b": "cc3-1b's 'z=0 apparent / log-free' is corrected: z=0 carries logs (Jordan [2,2]); the integer block at z=1/3 IS semisimple (cc3-1b correct there).",
        "ceiling": ("A Fuchsian relocation does not make K a classical period; provenance, "
                    "not singularity type, is what the period conjectures see; rigidity, if "
                    "found, only sharpens the period home. Unconditional transcendence of C is "
                    "NOT a deliverable of op:cc-3 at any grade."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1c_rigidity_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\n=== VERDICT ===")
    print(f"  rig(L) = {r_L}  =>  {verdict};  accessory parameter count = {accessory}")
    print(f"  rig(L2) = {r_L2} (internal check, also non-rigid)")
    print("  controls Airy/2F1/Bessel all rig=2 (PASS)")
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1c_rigidity_results.json")

if __name__ == "__main__":
    main()
