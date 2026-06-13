#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc4-0b  --  DEGREE / POLE BOUND RIGORIZATION  (the SL4 theorem's last gap)
================================================================================
SIARC four-class discipline. PROVEN = Lean only. The bound derivation below is a
short hand proof graded STRUCTURAL; the integer-exponent extraction is exact
symbolic (VERIFIED). No numerics.

PURPOSE.  cc4-0 settled PRIMITIVE by two rational-solution searches whose ansatz
degrees (deg 8 / deg 10, up to 336 unknowns under stress) were EMPIRICAL. This
op exhibits, for each route, the connection whose rational (horizontal) sections
the search enumerates, computes its INTEGER local exponents at every singular
point, and derives an a priori degree/pole bound B. If the bound-complete box was
already run (denominator pole orders >= the bounds AND numerator degree >= B), the
verdict is rigorous and CC4-0-ROUTE{1,2} upgrade to "bound-complete".

THE OBJECTS.
  Route 2 :  N2 = End(M) (x) eta,  eta = sqrt(s) = the rank-1 connection d-(1/2s).
             rational sections of N2 = { rational 4x4 Phi : Phi'=[A,Phi]+(1/2s)Phi }
             = Hom_{diff}(M, M(x)sqrt s).  cc4-0 found dim 0.
  Route 1 :  N1 = End(M~) over C(t), M~ = pullback under s=t^2.
             rational sections of N1 = eigenring of M~.  cc4-0 found dim 1.

THE BOUND (van Hoeij / Barkatou rational-solution theory; van der Put-Singer ch.4).
  M0, M_R are SEMISIMPLE (cc2-2d) => no logarithms => a rational section f expands
  at each regular singular point p in the Frobenius basis (s-p)^{rho_i} h_i with
  h_i holomorphic, h_i(0)!=0. Single-valuedness forces c_i=0 on every NON-integer
  exponent rho_i (those branches are multivalued). Hence:

     pole_order_p(f)  <=  max(0, -min{ rho_i in Z })          (finite p)
     deg-growth_oo(f) <=  -min{ e in Z achievable at oo }     (e = u-exponent, u=1/s)

  The End exponents at p are the pairwise DIFFERENCES rho_i - rho_j of the M
  exponents at p (residue of End = ad of residue of M); (x)eta shifts by eta's
  exponent at p. At oo the slope-0 part of End(M) carries the exponents of the
  ramified cyclic formal monodromy: a single ramification-r orbit contributes
  {0, 1/r, ..., (r-1)/r}. So:
     Route 2 (r=4 at oo) slope-0 End exps {0,1/4,1/2,3/4}; (x)sqrt s shifts by -1/2.
     Route 1 (r=2 at oo, double transposition) slope-0 End exps {0,0,1/2,1/2}.

  Numerator-degree bound B = deg(denominator) - min_achievable_integer_oo_exponent.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import hashlib
import sympy as sp

s, t = sp.symbols("s t")

# inherited M exponents (cc-1 bfb91bd...)
EXP0 = [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2)]
EXPR = [sp.Integer(0), sp.Integer(1), sp.Integer(2), sp.Rational(-11, 6)]
EXP0_t = [2*r for r in EXP0]            # pullback s=t^2 ramifies 0 -> {0,1,2,3}
EXPR_t = list(EXPR)                     # +-t_R unramified simple points


def diff_multiset(exps):
    """End(M) local exponents = all pairwise differences rho_i - rho_j."""
    return [sp.nsimplify(a - b) for a in exps for b in exps]


def integer_part(ms):
    return sorted({int(x) for x in ms if sp.nsimplify(x).is_integer})


def pole_bound(exps, shift=sp.Integer(0)):
    """max pole order of a rational section at a regular singular point p:
       = max(0, -min{ integer exponents of End(M)(x)eta at p })."""
    ms = [d + shift for d in diff_multiset(exps)]
    ints = integer_part(ms)
    mn = min(ints) if ints else 0
    return max(0, -mn), ints, [str(x) for x in sorted(set(ms), key=lambda z: float(z))]


def oo_degree_bound(slope0_exps, shift=sp.Integer(0)):
    """max growth g at oo for a rational section: g = -e_min, where e_min is the
       smallest integer u-exponent achievable (e in Z, e >= min exponent,
       e == some exponent mod Z)."""
    exps = [sp.nsimplify(e + shift) for e in slope0_exps]
    mn = min(exps)
    residues = {sp.nsimplify(e) % 1 for e in exps}        # exponents mod Z
    # integer e achievable: e in Z, e == 0 mod 1 must lie in residue set; e >= mn
    if (sp.Integer(0) % 1) not in residues:
        return None, None, [str(e) for e in sorted(exps, key=lambda z: float(z))]
    import math
    e_min = math.ceil(float(mn))
    # ensure e_min itself is admissible (>= mn and integer); ceil handles it
    g = max(0, -e_min)
    return g, e_min, [str(e) for e in sorted(exps, key=lambda z: float(z))]


def route_bound(label, finite_pts, slope0_oo, oo_shift, boxes_run, denom_desc):
    pbounds = {}
    detail = {}
    for name, (exps, shift) in finite_pts.items():
        pb, ints, ms = pole_bound(exps, shift)
        pbounds[name] = pb
        detail[name] = {"End_exps_with_shift": ms, "integer_exps": ints, "pole_bound": pb}
    g, e_min, oo_ms = oo_degree_bound(slope0_oo, oo_shift)
    deg_denom = sum(pbounds.values())
    if g is None:
        B = None
        oo_note = ("NO integer u-exponent achievable at oo (all exps != 0 mod Z) "
                   "=> NO rational section can match oo => search vacuous.")
    else:
        B = deg_denom - e_min      # numerator degree bound
        oo_note = f"min achievable integer u-exponent e_min={e_min}, growth g={g}"
    return {
        "label": label,
        "finite_pole_bounds": pbounds,
        "finite_detail": detail,
        "oo_slope0_exps_with_shift": oo_ms,
        "oo_degree_growth_g": g,
        "oo_e_min": e_min,
        "oo_note": oo_note,
        "deg_denominator_bound": deg_denom,
        "numerator_degree_bound_B": B,
        "denominator": denom_desc,
        "boxes_run_in_cc4_0": boxes_run,
    }


def main():
    res = {
        "op": "cc4-0b",
        "task_id": "op:cc-transcendence/cc4-0b",
        "inherits": {"cc4_0_sha":
                     "a378b781809b4e26caf353cbd4196f7669c557ee1c3a7ef03adaf5ed4ed9fe64"},
        "objective": ("Derive a priori numerator-degree / pole bounds B for the two "
                      "cc4-0 rational-solution searches; confirm the bound-complete "
                      "box was run (B<=20) so the SL4 verdict is rigorous."),
        "method": ("M0,M_R semisimple (no logs) => single-valuedness kills non-integer "
                   "exponent branches => pole_p <= -min{integer End(x)eta exps}; "
                   "oo growth <= -min achievable integer u-exponent. Exact symbolic."),
    }

    # ---- Route 2: End(M)(x)sqrt(s) over C(s) ----
    # eta=sqrt(s) exponents: +1/2 at s=0, 0 at s=R (analytic nonzero), -1/2 at oo (u-exp)
    r2 = route_bound(
        "Route 2: End(M)(x)sqrt(s) over C(s)",
        finite_pts={
            "s=0": (EXP0, sp.Rational(1, 2)),
            "s=R=4/3": (EXPR, sp.Integer(0)),
        },
        slope0_oo=[sp.Integer(0), sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4)],
        oo_shift=sp.Rational(-1, 2),
        boxes_run=[
            {"denom": "s^1(4-3s)^2", "pole_orders": [1, 2], "deg_max": 8,
             "hom_dim": 0, "note": "twist box (1,2,8)"},
            {"denom": "s^2(4-3s)^3", "pole_orders": [2, 3], "deg_max": 12,
             "hom_dim": 0, "note": "twist box (2,3,12)"},
        ],
        denom_desc="s^{p0}(4-3s)^{pR}",
    )

    # ---- Route 1: End(M~) over C(t), s=t^2 ----
    r1 = route_bound(
        "Route 1: End(M~) eigenring over C(t)",
        finite_pts={
            "t=0": (EXP0_t, sp.Integer(0)),
            "t=+t_R": (EXPR_t, sp.Integer(0)),
            "t=-t_R": (EXPR_t, sp.Integer(0)),
        },
        slope0_oo=[sp.Integer(0), sp.Integer(0), sp.Rational(1, 2), sp.Rational(1, 2)],
        oo_shift=sp.Integer(0),
        boxes_run=[
            {"denom": "t^2(3t^2-4)^1", "pole_orders": [2, 1, 1], "deg_max": 6,
             "eigenring_dim": 1, "note": "UNDER-bounded box (2,1,6): denom too small, "
             "not bound-complete on its own"},
            {"denom": "t^3(3t^2-4)^2", "pole_orders": [3, 2, 2], "deg_max": 10,
             "eigenring_dim": 1, "note": "bound-complete box (3,2,10)"},
        ],
        denom_desc="t^{p0}(3t^2-4)^{pR}  (the two factors of 3t^2-4 are +-t_R)",
    )

    res["route2"] = r2
    res["route1"] = r1

    # ---- bound-completeness check ----
    def box_covers(box, pole_bounds_list, B):
        deg_ok = box["deg_max"] >= B
        # pole orders in the box denominator must be >= the per-point bounds
        pole_ok = all(p >= b for p, b in zip(sorted(box["pole_orders"], reverse=True),
                                             sorted(pole_bounds_list, reverse=True)))
        return deg_ok and pole_ok

    B2 = r2["numerator_degree_bound_B"]
    B1 = r1["numerator_degree_bound_B"]
    pb2 = list(r2["finite_pole_bounds"].values())   # [1,2]
    pb1 = list(r1["finite_pole_bounds"].values())   # [3,2,2]

    r2_box = r2["boxes_run_in_cc4_0"][0]   # s^1(4-3s)^2 d8
    r1_box = r1["boxes_run_in_cc4_0"][1]   # t^3(3t^2-4)^2 d10
    r2_complete = box_covers(r2_box, pb2, B2)
    r1_complete = box_covers(r1_box, pb1, B1)

    res["bound_completeness"] = {
        "route2_B": B2, "route2_pole_bounds": pb2,
        "route2_boundcomplete_box": r2_box["denom"] + f" deg<= {r2_box['deg_max']}",
        "route2_box_covers_bound": bool(r2_complete),
        "route2_hom_dim_in_box": r2_box["hom_dim"],
        "route1_B": B1, "route1_pole_bounds": pb1,
        "route1_boundcomplete_box": r1_box["denom"] + f" deg<= {r1_box['deg_max']}",
        "route1_box_covers_bound": bool(r1_complete),
        "route1_eigenring_dim_in_box": r1_box["eigenring_dim"],
        "all_bounds_le_20": bool((B2 is not None and B2 <= 20)
                                 and (B1 is not None and B1 <= 20)),
    }

    res["verdict"] = {
        "B_route2": B2, "B_route1": B1, "rerun_needed": False,
        "statement": (
            f"Route 2 numerator-degree bound B2={B2} (poles <=1 at 0, <=2 at R, no growth "
            f"at oo); Route 1 bound B1={B1} (poles <=3 at t=0, <=2 at +-t_R, no growth). "
            f"Both <= 20. The bound-complete boxes [s(4-3s)^2 deg<=8] (Hom dim 0) and "
            f"[t^3(3t^2-4)^2 deg<=10] (eigenring dim 1) STRICTLY contain B2,B1 and match "
            f"the pole bounds, so the cc4-0 PRIMITIVE verdict is bound-complete (rigorous). "
            f"CC4-0-ROUTE2-PRIMITIVE / ROUTE1-PRIMITIVE upgrade to bound-complete; "
            f"G_Gal(L2)^0 = SL4 is citable as UNCONDITIONAL STRUCTURAL."),
        "grade": "STRUCTURAL (exact integer-exponent extraction + single-valuedness "
                 "degree bound; van Hoeij/Barkatou + van der Put-Singer ch.4)",
    }
    res["hand_proof"] = (
        "Let f be a rational horizontal section of N (= End(M)(x)eta, Route 2; = End(M~), "
        "Route 1). N is regular-singular at the finite points with End-exponents equal to "
        "the pairwise differences of the M-exponents there (residue of End = ad of residue "
        "of M), shifted by eta's exponent. Since M0 and M_R are SEMISIMPLE there are no "
        "logarithmic terms, so near a finite singular point p, f = sum_i c_i (s-p)^{rho_i} "
        "h_i(s-p) with h_i holomorphic units and rho_i the End-exponents. f single-valued "
        "(rational) forces c_i=0 whenever rho_i not in Z. Hence the pole order of f at p is "
        "at most -min{ rho_i in Z }. At oo, f rational has slope 0, so its leading u=1/s "
        "exponent e lies in the slope-0 spectrum of N; the slope-0 part of End(M) is the "
        "rank-(deg) cyclic piece of the ramified formal monodromy with exponents "
        "{0,1/r,...,(r-1)/r} (r=4 Route 2, r=2 Route 1), shifted by eta. e must be an "
        "integer (f rational) and >= the minimal exponent, giving the growth bound. The "
        "numerator degree is then bounded by deg(denominator) - e_min. Computed: B2=3, B1=7."
    )

    print("== op:cc4-0b  DEGREE / POLE BOUND RIGORIZATION ==")
    for r, B in (("Route 2", B2), ("Route 1", B1)):
        rr = r2 if r == "Route 2" else r1
        print(f"\n[{r}] {rr['label']}")
        print("  finite pole bounds:", rr["finite_pole_bounds"])
        print("  oo slope-0 exps (shifted):", rr["oo_slope0_exps_with_shift"],
              "| growth g =", rr["oo_degree_growth_g"])
        print("  => numerator-degree bound B =", B, "  (deg denom =",
              rr["deg_denominator_bound"], ")")
    bc = res["bound_completeness"]
    print("\n[bound-completeness]")
    print("  Route 2 box", bc["route2_boundcomplete_box"], "covers B2:",
          bc["route2_box_covers_bound"], "| Hom dim =", bc["route2_hom_dim_in_box"])
    print("  Route 1 box", bc["route1_boundcomplete_box"], "covers B1:",
          bc["route1_box_covers_bound"], "| eigenring dim =", bc["route1_eigenring_dim_in_box"])
    print("  all bounds <= 20:", bc["all_bounds_le_20"])
    print("\n", res["verdict"]["statement"])

    blob = json.dumps(res, sort_keys=True, ensure_ascii=False).encode("utf-8")
    sha = hashlib.sha256(blob).hexdigest()
    res["canonical_sha256_of_hashfree_object"] = sha
    with open("cc4_0b_bounds_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", sha)
    print("wrote cc4_0b_bounds_results.json")


if __name__ == "__main__":
    main()
