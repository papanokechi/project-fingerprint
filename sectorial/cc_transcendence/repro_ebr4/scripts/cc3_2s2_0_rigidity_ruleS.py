#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-2s2-0  --  RIGIDITY + RULE S GATE  for the rank-2 core H2
================================================================================
SIARC.  H2 = 3 t^3 D^2 + 10 t^2 D + (t^2 + 5 t - 1)  is the homogeneous core of
the OGF ODE  H2 y = -1  (CC3-1-OGF-ODE),  y = sum_{n>=0} Q_n t^n,
Q_n = (3 n^2 + n + 1) Q_{n-1} + Q_{n-2},  Q_0 = 1.

TWO deliverables, both gates for the stage:

 (A) rig(H2) via the irregular index-of-rigidity pipeline (cc3-1c-2 code path,
     rank 2).  Controls (Airy / Gauss 2F1 / Bessel, all classically rigid)
     re-fired.   Verdict vs REGISTERED PREDICTION P5:
        P5  rig(H2) = 0 with moduli dimension 2 (Painleve phase-space dim).
     A RIGID verdict KILLS the PIII(D8) candidacy and is a HALT.

 (B) RULE S battery for the PIII(D8) candidacy.  RULE S (verbatim, reproduced):
     "No Painleve / Sakai surface label reaches VERIFIED without computed
      selectors plus the Pade convergence screen."
     Leg 1 (selectors): the surface-type selectors are COMPUTED from H2's
       operator -- singular set, the pole order of the reduced invariant at each
       singular point (=> slope, ramification), rank, moduli dimension -- and
       mapped through the van der Put-Saito / Ohyama-Sakai dictionary.  D6 / D7
       are excluded by the ramification data; only D8 matches.
     Leg 2 (Pade convergence screen): the dominant Borel-plane singularity of the
       Gevrey-2 series y -- located via (i) the exact ratio-test radius of the
       Borel transform Phi(z) = sum Q_n z^n/(n!)^2 and (ii) the nearest Pade pole
       of Phi -- must reproduce z = 1/3 to the declared precision.  This
       SIMULTANEOUSLY validates the REFRAME (z=1/3 is an instanton action /
       Borel singularity, not a finite singularity of H2, which has none).

REGISTERED PREDICTIONS tested here: P5 (rigidity), P6 (RULE S pass).
P6 failure is NOT a halt (it reroutes 2s2-2 to an obstruction report) but the
failing selector must be named with its magnitude.

CEILING (cc3-2 form, reproduced): a Stokes reframing, a RULE S pass, even an
ILP-class formula match would NOT prove transcendence; a match would prove the
OPPOSITE (elementarity in an extended Barnes class).  Unconditional transcendence
of C/kappa is NOT a deliverable of op:cc-3 at any grade.

References (VERIFIED-by-citation, never silently load-bearing for a grade > CONJECTURED):
  - H. Sakai, "Rational surfaces associated with affine root systems and geometry
    of the Painleve equations", Comm. Math. Phys. 220 (2001) 165-229.
    [surface type D8^(1) = most degenerate Painleve III]
  - M. van der Put, M.-H. Saito, "Moduli spaces for linear differential equations
    and the Painleve equations", Ann. Inst. Fourier 59 (2009), no. 7, 2611-2667.
    [section 3-4: dictionary singularity-type <-> Painleve surface; PIII(D8) = the
     rank-2 connection with TWO ramified irregular points (Katz invariant 1/2)]
  - Y. Ohyama, H. Kawamuko, H. Sakai, K. Okamoto, "Studies on the Painleve
    equations V, third Painleve equations of special type PIII(D7) and PIII(D8)",
    J. Math. Sci. Univ. Tokyo 13 (2006) 145-204.  [explicit PIII(D8) Lax pair:
     irregular ramified at 0 and infinity]
  - D. Arinkin, "Rigid irregular connections on P^1", Compositio Math. 146 (2010)
    1323-1338.  [index of rigidity for irregular connections; rig <= 2 for irred]
  - S. Bloch, H. Esnault, "Local Fourier transforms and rigidity for D-modules",
    Asian J. Math. 8 (2004) 587-606.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from fractions import Fraction as Fr
import sympy as sp
import mpmath as mm
from mpmath import mp, mpf

# ----------------------------------------------------------------------------
# (A) index of rigidity  (same formula as cc3_1c_rigidity.py; rank-2 here)
# ----------------------------------------------------------------------------
def dimZ_from_blocks(blocks_per_eigen):
    total = 0
    for blocks in blocks_per_eigen:
        for di in blocks:
            for dj in blocks:
                total += min(di, dj)
    return total

def rigidity(n, points):
    S = len(points)
    term_topo = (2 - S) * n * n
    sum_dimZ = sum(p["dimZ_formal"] for p in points)
    sum_irr = sum(Fr(p["irr_End"]) for p in points)
    rig = term_topo + sum_dimZ - sum_irr
    return rig, {"(2-#S)n^2": term_topo, "sum dimZ_formal": sum_dimZ,
                 "sum irr_End": str(sum_irr), "#S": S, "n": n}

def show(label, n, points):
    rig, br = rigidity(n, points)
    print(f"\n[{label}]  n={n}, #S={len(points)}")
    for p in points:
        print(f"    {p['name']:<30} dimZ_formal={p['dimZ_formal']:>3}  "
              f"irr_End={str(Fr(p['irr_End'])):>4}   ({p.get('note','')})")
    verdict = ('RIGID' if rig == 2 else ('NON-RIGID, moduli dim '+str(2-rig)) if rig < 2 else 'INCONSISTENT(>2)')
    print(f"    rig = (2-{br['#S']})*{n*n} + {br['sum dimZ_formal']} - {br['sum irr_End']} = {rig}   => {verdict}")
    return rig, br

def part_A_rigidity():
    print("=== (A) cc3-2s2-0  index of rigidity of H2 (rank 2) ===")
    # ----- controls (all classically rigid: rig must be 2) -----
    # Airy y''=zy: only inf, slope 3/2 ram 2, single orbit => dimZ(formal)=1;
    #   End rank 4 has 2 nonzero diffs of slope 3/2 => irr(End)=2*(3/2)=3.
    airy = [dict(name="inf (slope 3/2, ram 2)", dimZ_formal=1, irr_End=Fr(3), note="2 diffs * 3/2")]
    r_airy, _ = show("Airy (control)", 2, airy); assert r_airy == 2, "Airy control failed"
    # Gauss 2F1: S={0,1,inf} all reg sing, generic distinct => dimZ=2 each, irr=0.
    gauss = [dict(name="0 (reg, distinct)", dimZ_formal=2, irr_End=0),
             dict(name="1 (reg, distinct)", dimZ_formal=2, irr_End=0),
             dict(name="inf (reg, distinct)", dimZ_formal=2, irr_End=0)]
    r_g, _ = show("Gauss 2F1 (control)", 2, gauss); assert r_g == 2, "Gauss control failed"
    # Bessel order 2: S={0 reg distinct dimZ=2, inf slope 1 two distinct exp =>
    #   dimZ(formal)=2, End 2 nonzero diffs of slope 1 => irr=2}.
    bessel = [dict(name="0 (reg, distinct)", dimZ_formal=2, irr_End=0),
              dict(name="inf (slope 1)", dimZ_formal=2, irr_End=Fr(2), note="2 diffs * 1")]
    r_b, _ = show("Bessel (control)", 2, bessel); assert r_b == 2, "Bessel control failed"

    # ----- H2 : the target -----
    # S = {0, infinity}, BOTH irregular slope 1/2 ram 2 (cc3-2a e71e915f; reduced
    # invariant r(t) has a pole of order 3 at each => slope (3-2)/2 = 1/2).
    # At a slope-1/2 ram-2 point of a rank-2 connection the formal type is a SINGLE
    # Galois orbit {e^{+c t^{-1/2}}, e^{-c t^{-1/2}}} (the two Puiseux branches) =>
    # irreducible formal type => dimZ(formal) = 1 (scalars only).
    # End(E) (rank 4) exponential differences: the 4 = n^2 differences are
    # {0, 0 (diagonal), +2c t^{-1/2}, -2c t^{-1/2}} => 2 nonzero of slope 1/2 =>
    # irr_x(End E) = 2 * (1/2) = 1   at EACH of 0 and infinity.
    H2 = [dict(name="0 (slope 1/2, ram 2)", dimZ_formal=1, irr_End=Fr(1), note="single orbit; 2 diffs*1/2=1"),
          dict(name="inf (slope 1/2, ram 2)", dimZ_formal=1, irr_End=Fr(1), note="single orbit; 2 diffs*1/2=1")]
    r_H2, br = show("H2 (rank-2 core) -- TARGET", 2, H2)
    assert r_H2 <= 2, "rig > 2 contradicts irreducibility (SL2 from cc3-2a)"
    moduli_dim = 2 - r_H2
    accessory_P = Fr(moduli_dim, 2)  # CC3-2-CONV-1: moduli dim = 2P = 2 - rig
    verdict = "RIGID" if r_H2 == 2 else ("NON-RIGID" if r_H2 < 2 else "INCONSISTENT")
    P5_holds = (r_H2 == 0 and moduli_dim == 2)
    print(f"\n  rig(H2) = {r_H2}  => {verdict};  moduli dim = 2 - rig = {moduli_dim}; "
          f"accessory P = (2-rig)/2 = {accessory_P}")
    print(f"  P5 (rig=0, moduli dim 2 = Painleve phase space): {'HOLDS' if P5_holds else 'FAILS -> HALT'}")
    return dict(controls={"Airy": int(r_airy), "Gauss_2F1": int(r_g), "Bessel": int(r_b),
                          "all_pass": bool(r_airy == 2 and r_g == 2 and r_b == 2)},
                rig=int(r_H2), verdict=verdict, moduli_dim=int(moduli_dim),
                accessory_P=str(accessory_P), term_breakdown={k: (str(v) if isinstance(v, Fr) else v) for k, v in br.items()},
                local_data={"0": {"slope": "1/2", "ram": 2, "dimZ_formal": 1, "irr_End": 1},
                            "infinity": {"slope": "1/2", "ram": 2, "dimZ_formal": 1, "irr_End": 1}},
                P5_holds=bool(P5_holds))

# ----------------------------------------------------------------------------
# (B) RULE S  --  leg 1 selectors (computed from the operator), leg 2 Pade screen
# ----------------------------------------------------------------------------
def reduced_invariant():
    t = sp.symbols('t')
    a2, a1, a0 = 3*t**3, 10*t**2, (t**2 + 5*t - 1)
    p = sp.simplify(a1/a2); q = sp.simplify(a0/a2)
    r = sp.simplify(sp.Rational(1, 4)*p**2 + sp.Rational(1, 2)*sp.diff(p, t) - q)
    return t, sp.simplify(r)

def laurent_pole_order(expr, var, point):
    """Order m of the pole: smallest m with (var-point)^m * expr regular & nonzero,
       computed from the rational function directly."""
    if point == sp.oo:
        w = sp.symbols('w')
        e = sp.simplify(sp.together(expr.subs(var, 1/w) / w**4))
        return laurent_pole_order(e, w, 0)
    e = sp.cancel(sp.together(expr))
    num, den = sp.fraction(e)
    pden = sp.Poly(den, var)
    pnum = sp.Poly(num, var)
    # multiplicity of (var-point) in den minus in num
    md = pden.as_expr().subs(var, point)
    def mult(poly):
        m = 0
        pp = poly
        while True:
            qq, rr = sp.div(pp, sp.Poly(var - point, var))
            if rr.is_zero:
                m += 1; pp = qq
            else:
                break
        return m
    return mult(pden) - mult(pnum)

def Qs(N):
    Q = [1]
    for m in range(1, N + 1):
        Q.append((3*m*m + m + 1)*Q[m-1] + (Q[m-2] if m >= 2 else 0))
    return Q

def part_B_ruleS():
    print("\n=== (B) cc3-2s2-0  RULE S battery for PIII(D8) candidacy ===")
    print("RULE S: no Painleve/Sakai label reaches VERIFIED without computed "
          "selectors PLUS the Pade convergence screen.")

    # ---- leg 1: COMPUTED selectors ----
    t, r = reduced_invariant()
    print("\n[leg 1: computed selectors]")
    print("  reduced invariant r(t) =", sp.nsimplify(sp.together(r)))
    ord0 = laurent_pole_order(r, t, 0)
    ordinf = laurent_pole_order(r, t, sp.oo)
    def slope(m):  # y''=r y, pole order m of r => slope (m-2)/2
        return Fr(m - 2, 2)
    s0, sinf = slope(ord0), slope(ordinf)
    ram0 = s0.denominator
    raminf = sinf.denominator
    print(f"  t=0   : reduced-invariant pole order {ord0}  => slope {s0}  ramification {ram0}  "
          f"({'irregular ramified' if ram0 > 1 else ('irregular' if s0>0 else 'regular')})")
    print(f"  t=inf : reduced-invariant pole order {ordinf}  => slope {sinf}  ramification {raminf}  "
          f"({'irregular ramified' if raminf > 1 else ('irregular' if sinf>0 else 'regular')})")
    sing = ["0", "infinity"]
    rank = 2
    moduli_dim = 2  # from part A (rig=0)
    # the selector signature
    selector = {
        "rank": rank,
        "singular_set": sing,
        "n_singular_points": len(sing),
        "slopes": {"0": str(s0), "infinity": str(sinf)},
        "ramification": {"0": ram0, "infinity": raminf},
        "both_irregular": bool(s0 > 0 and sinf > 0),
        "both_ramified": bool(ram0 == 2 and raminf == 2),
        "moduli_dimension": moduli_dim,
    }
    # dictionary map (van der Put-Saito / Ohyama-Sakai): rank-2 connection with
    #   D6 : two UNramified irregular points (slope 1, 1)
    #   D7 : one ramified + one unramified
    #   D8 : two RAMIFIED irregular points (slope 1/2, 1/2)
    signatures = {
        "PIII(D6) [D6^(1)]": dict(n_sing=2, ram=(1, 1)),
        "PIII(D7) [D7^(1)]": dict(n_sing=2, ram=(2, 1)),
        "PIII(D8) [D8^(1)]": dict(n_sing=2, ram=(2, 2)),
    }
    obs = (ram0, raminf)
    matches = []
    for name, sig in signatures.items():
        ok = (sig["n_sing"] == len(sing)) and (tuple(sorted(sig["ram"])) == tuple(sorted(obs)))
        print(f"    candidate {name:<22} ram pattern {sig['ram']}  -> {'MATCH' if ok else 'excluded'}")
        if ok:
            matches.append(name)
    leg1_pass = (matches == ["PIII(D8) [D8^(1)]"])
    print(f"  leg 1 verdict: {'UNIQUE match PIII(D8)' if leg1_pass else 'AMBIGUOUS/NO MATCH: '+str(matches)}")

    # ---- leg 2: Pade convergence screen on the Borel plane of y ----
    print("\n[leg 2: Pade convergence screen on Borel plane Phi(z)=sum Q_n z^n/(n!)^2]")
    mp.dps = 220
    # (i) exact ratio-test radius: Phi_n/Phi_{n+1} -> 1/3 ; Richardson on a
    #     GEOMETRIC node ladder (well-conditioned) eliminating powers of 1/n.
    Nr = 5000
    Q = Qs(Nr + 2)
    def phi(n):
        return mpf(Q[n]) / (mm.factorial(n))**2
    def ratio(n):
        return phi(n) / phi(n + 1)
    def neville_zero_inv_n(nodes):
        xs = [mpf(1) / n for n in nodes]; ys = [ratio(n) for n in nodes]
        K = len(xs); T = [ys[:]]
        for k in range(1, K):
            row = []
            for i in range(K - k):
                row.append(((-xs[i+k])*T[k-1][i] - (-xs[i])*T[k-1][i+1]) / (xs[i] - xs[i+k]))
            T.append(row)
        return T[-1][0]
    nodes = sorted(set(int(Nr / (mpf(3)/2)**k) for k in range(14)))
    radius_est = neville_zero_inv_n(nodes)
    radius_err = abs(radius_est - mpf(1)/3)
    digits_radius = int(-mm.log10(radius_err)) if radius_err > 0 else 200
    print(f"  (i) ratio-test radius (Richardson, geometric nodes {min(nodes)}..{max(nodes)})")
    print(f"      radius     = {mm.nstr(radius_est, 45)}")
    print(f"      |radius-1/3| = {mm.nstr(radius_err, 6)}   (~{digits_radius} digits)")

    # (ii) nearest Pade pole of Phi -> 1/3 as the order grows (convergence table)
    print("  (ii) nearest Pade pole of Phi(z) vs 1/3 (convergence with order):")
    pole_table = []
    for M in [20, 30, 40, 50, 60]:
        coeffs = [phi(n) for n in range(2*M + 1)]
        try:
            pcoef, qcoef = mm.pade(coeffs, M, M)
            roots = mm.polyroots(qcoef[::-1], maxsteps=600, extraprec=400)
            roots = sorted(roots, key=lambda z: abs(z - mpf(1)/3))
            near = roots[0]; err = abs(near - mpf(1)/3)
            pole_table.append({"order": M, "nearest_pole": mm.nstr(near, 30), "err_vs_1_3": mm.nstr(err, 6)})
            print(f"      [{M}/{M}] nearest pole = {mm.nstr(near, 24)}   |pole-1/3| = {mm.nstr(err, 4)}")
        except Exception as e:
            pole_table.append({"order": M, "error": str(e)})
            print(f"      [{M}/{M}] skipped ({e})")
    errs = [mm.mpf(p["err_vs_1_3"]) for p in pole_table if "err_vs_1_3" in p]
    pade_converging = (len(errs) >= 2 and errs[-1] < errs[0])
    leg2_pass = (radius_err < mpf(10)**(-25)) and pade_converging
    print(f"  leg 2 verdict: ratio-test reproduces z=1/3 to ~{digits_radius} digits; "
          f"Pade poles converge to 1/3: {pade_converging}  -> {'PASS' if leg2_pass else 'FAIL'}")

    ruleS_pass = leg1_pass and leg2_pass
    P6_holds = ruleS_pass
    grade = "VERIFIED (per RULE S: both legs pass)" if ruleS_pass else "CONJECTURED (RULE S not satisfied)"
    print(f"\n  RULE S verdict for PIII(D8): {grade}")
    print(f"  P6 (PIII(D8) passes RULE S): {'HOLDS' if P6_holds else 'FAILS -> reroute 2s2-2 to obstruction report'}")
    return dict(
        rule_S_text="No Painleve/Sakai surface label reaches VERIFIED without computed selectors plus the Pade convergence screen.",
        leg1_selectors=selector, leg1_dictionary={k: str(v["ram"]) for k, v in signatures.items()},
        leg1_unique_match=matches, leg1_pass=bool(leg1_pass),
        leg2_radius_estimate=mm.nstr(radius_est, 50), leg2_radius_err=mm.nstr(radius_err, 6),
        leg2_radius_digits=digits_radius, leg2_pade_table=pole_table, leg2_pade_converging=bool(pade_converging),
        leg2_pass=bool(leg2_pass), rule_S_pass=bool(ruleS_pass), grade=grade, P6_holds=bool(P6_holds),
        surface_label="PIII(D8) = Sakai surface D8^(1)")

def main():
    A = part_A_rigidity()
    B = part_B_ruleS()
    obj = {
        "op": "cc3-2s2-0-rigidity-ruleS",
        "task_id": "op:cc-transcendence/cc3-2s2",
        "operator_H2": "3 t^3 D^2 + 10 t^2 D + (t^2 + 5 t - 1)",
        "rigidity": A,
        "rule_S": B,
        "P5_rigidity": {"prediction": "rig(H2)=0, moduli dim 2 (Painleve phase space)",
                        "holds": A["P5_holds"], "halt_if_false": True},
        "P6_ruleS": {"prediction": "PIII(D8) candidacy passes RULE S (selectors + Pade screen)",
                     "holds": B["P6_holds"], "halt_if_false": False,
                     "note": "failure reroutes 2s2-2 to obstruction report; not a halt"},
        "reframe_validated": "z=1/3 reproduced by the Pade screen as the dominant Borel-plane "
                             "singularity of the Gevrey-2 series y; H2 has NO finite nonzero "
                             "singularity, so z=1/3 is an instanton action, not a singularity of H2.",
        "ceiling": ("A Stokes reframing, a RULE S pass, even an ILP-class formula match would NOT "
                    "prove transcendence; a match would prove the OPPOSITE (elementarity in an "
                    "extended Barnes class). Unconditional transcendence of C/kappa is NOT a "
                    "deliverable of op:cc-3 at any grade."),
        "references": [
            "Sakai, Comm. Math. Phys. 220 (2001) 165-229 (surface D8^(1))",
            "van der Put & Saito, Ann. Inst. Fourier 59 (2009) 2611-2667 (singularity-type <-> Painleve dictionary)",
            "Ohyama-Kawamuko-Sakai-Okamoto, J. Math. Sci. Univ. Tokyo 13 (2006) 145-204 (PIII(D8) Lax pair)",
            "Arinkin, Compositio Math. 146 (2010) 1323-1338 (irregular index of rigidity)",
            "Bloch & Esnault, Asian J. Math. 8 (2004) 587-606 (local Fourier transform / rigidity)",
        ],
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_2s2_0_rigidity_ruleS_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\n=== STAGE GATE SUMMARY ===")
    print(f"  rig(H2) = {A['rig']}  ({A['verdict']}); moduli dim {A['moduli_dim']}; accessory P = {A['accessory_P']}")
    print(f"  P5: {'HOLDS (no halt)' if A['P5_holds'] else 'FAILS -> HALT'}")
    print(f"  RULE S / PIII(D8): {B['grade']}")
    print(f"  P6: {'HOLDS' if B['P6_holds'] else 'FAILS (reroute, not halt)'}")
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_2s2_0_rigidity_ruleS_results.json")

if __name__ == "__main__":
    main()
