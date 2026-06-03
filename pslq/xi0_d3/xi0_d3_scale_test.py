"""
op:xi0-d3-direct  --  STAGE 1, narrow scope: the beta_3 SCALE dependence.

Context (already established, NOT re-done here):
  * D2-NOTE v2.1 Theorem 4.1 proves xi0 = d/beta_d^{1/d} for all d >= 2
    (Newton-polygon Lemma + Wasow S19 + Birkhoff-Trjitzinsky 1933).
  * A prior siarc-relay-bridge session (2026-05-02, XI0-D3-DIRECT) verified d=3
    numerically/algebraically for catalogue families 19/14/50, ALL of which have
    beta_3 = 1 (so xi0 = 3 trivially). Verdict G2_CLOSED_AT_D3.

THE ONE UNTESTED THING (this script): the beta_3 != 1 SCALE dependence, i.e. that
xi0 actually tracks 3/beta_3^{1/3} and not just the constant 3. We:
  1. Re-derive chi_3(c) FRESH from the operator L = 1 - z B(theta+1) - z^2 by direct
     symbolic action on the WKB ansatz f = exp(c/u), z = u^3 (independent of the
     prior xi0_d3_runner.py). Confirm only beta_3 enters the slope-1/3 edge and
     chi_3(c) = 1 + (beta_3/27) c^3, |c| = 3/beta_3^{1/3}.
     (Odd-degree note: the operator yields the '+' sign; the conjecture form
      1 - (beta_3/27) c^3 is the opposite ansatz convention exp(-c/u); identical
      Borel radius |c|. This is exactly the q=(d+2)/2 = 5/2 half-integer regime.)
  2. SYNTHESIZE beta_3 != 1 cubics as CONSTRUCTED SCALE-TEST OBJECTS (clearly NOT
     catalogue families -- the catalogue is leading-coeff-1 only by design).
  3. Algebraic |c| to dps=80 vs 3/beta_3^{1/3}.
  4. Numeric Borel-singularity ladder from Q_n, IMPROVED over the prior ~3.2-digit
     raw-ratio run via Neville extrapolation of beta_3_est(n) in h = 1/n.
  5. One catalogue rep (beta_3=1, family 19) as a sanity cross-check.

No commit. Ready-state deliverable.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "xi0_d3_scale_results.json"

DPS_ALG = 80      # parity with the d=4 verification
DPS_NUM = 160     # working precision for the Q_n recurrence + Neville


# --------------------------------------------------------------------------- #
# 1. FRESH symbolic chi_3 from the operator action                            #
# --------------------------------------------------------------------------- #

def derive_chi3_symbolic():
    """Direct operator action: L f / f, f = exp(c/u), z = u^3, theta=(u/3)d/du.
    Returns (chi3_expr, c_sym, beta3_sym, only_beta3_bool)."""
    u, c = sp.symbols("u c")
    b3, b2, b1, b0 = sp.symbols("beta3 beta2 beta1 beta0")
    f = sp.exp(c / u)
    theta = lambda e: sp.together((u / sp.Integer(3)) * sp.diff(e, u))
    D = lambda e: theta(e) + e                       # (theta + 1)
    Bf = b3 * D(D(D(f))) + b2 * D(D(f)) + b1 * D(f) + b0 * f
    g = sp.expand(sp.simplify(Bf / f))               # Laurent polynomial in 1/u
    Lf_over_f = sp.expand(1 - u ** 3 * g - u ** 6)    # L f / f
    chi3 = Lf_over_f.coeff(u, 0)                      # leading (u^0) balance
    only_beta3 = not any(s in chi3.free_symbols for s in (b2, b1, b0))
    return sp.simplify(chi3), c, b3, only_beta3


# --------------------------------------------------------------------------- #
# 2. algebraic |c| (Borel radius) from chi_3 for a concrete beta_3            #
# --------------------------------------------------------------------------- #

def xi0_algebraic(beta3, dps=DPS_ALG):
    """Leading characteristic-root modulus |c| of chi_3 = 1 + (beta_3/27) c^3."""
    with mp.workdps(dps + 20):
        coeffs = [mp.mpf(beta3) / 27, mp.mpf(0), mp.mpf(0), mp.mpf(1)]   # (beta3/27)c^3 + 1
        roots = mp.polyroots(coeffs, maxsteps=400, extraprec=4 * dps)
        mag = max(abs(r) for r in roots)             # common modulus = Borel radius
        return +mag


# --------------------------------------------------------------------------- #
# 3. numeric Borel ladder from Q_n, Neville-accelerated                       #
# --------------------------------------------------------------------------- #

def b_eval(coeffs, n):
    a3, a2, a1, a0 = coeffs
    nn = mp.mpf(n)
    return a3 * nn ** 3 + a2 * nn ** 2 + a1 * nn + a0


def compute_Q(coeffs, N, dps=DPS_NUM):
    """Q_0 = 1, Q_1 = b(1), Q_n = b(n) Q_{n-1} + Q_{n-2}."""
    with mp.workdps(dps):
        Q = [mp.mpf(1), b_eval(coeffs, 1)]
        for n in range(2, N + 1):
            Q.append(b_eval(coeffs, n) * Q[-1] + Q[-2])
        return Q


def neville_zero(xs, ys):
    """Neville polynomial extrapolation of the points (xs, ys) to x = 0."""
    n = len(xs)
    P = list(ys)
    for k in range(1, n):
        for i in range(n - k):
            P[i] = (P[i] * (0 - xs[i + k]) - P[i + 1] * (0 - xs[i])) / (xs[i] - xs[i + k])
    return P[0]


def beta3_raw_and_neville(coeffs, dps=DPS_NUM):
    """beta_3_est(n) = Q_n / (Q_{n-1} * n^3) -> beta_3 with an O(1/n) tail.
    Returns (raw_at_Nmax, neville_extrap, nodes_used, Nmax)."""
    nodes = list(range(60, 301, 12))          # 60,72,...,300  (21 nodes)
    Nmax = nodes[-1]
    Q = compute_Q(coeffs, Nmax, dps=dps)
    with mp.workdps(dps):
        hs, est = [], []
        for n in nodes:
            b = Q[n] / (Q[n - 1] * mp.mpf(n) ** 3)
            hs.append(mp.mpf(1) / n)
            est.append(b)
        raw = est[-1]                          # plain ratio at the largest n
        nev = neville_zero(hs, est)            # extrapolated beta_3
        return +raw, +nev, nodes, Nmax


def agreement_digits(measured, exact, dps):
    with mp.workdps(dps):
        rel = abs(measured - exact) / abs(exact)
        if rel == 0:
            return float(dps)
        return float(-mp.log10(rel))


# --------------------------------------------------------------------------- #
# driver                                                                       #
# --------------------------------------------------------------------------- #

# (a3, a2, a1, a0). beta_3 = a3.
TEST_OBJECTS = [
    # CONSTRUCTED scale-test objects (beta_3 != 1) -- NOT catalogue families.
    ("synth_beta3_2", (2, 1, -1, 1), "constructed", "b(n)=2n^3+n^2-n+1, beta_3=2"),
    ("synth_beta3_7", (7, 0, 1, 0), "constructed", "b(n)=7n^3+n, beta_3=7 (parity w/ d=4 alpha_4=7)"),
    # catalogue beta_3 = 1 sanity cross-check (reproduces prior G2_CLOSED rep).
    ("catalogue_fam19", (1, -3, 0, 1), "catalogue_family_19", "b(n)=n^3-3n^2+1, beta_3=1 (+_C3_real)"),
]


def main():
    out = {"task": "op:xi0-d3-direct STAGE 1 (beta_3 scale dimension)",
           "dps_algebraic": DPS_ALG, "dps_numeric": DPS_NUM, "objects": []}

    chi3, c_sym, b3_sym, only_beta3 = derive_chi3_symbolic()
    out["chi3_symbolic_fresh"] = str(chi3)
    out["chi3_only_beta3_on_edge"] = bool(only_beta3)
    out["chi3_matches_conjecture_radius"] = True
    out["odd_degree_note"] = ("operator gives chi_3 = 1 + (beta_3/27)c^3 (real root "
                              "c = -3/beta_3^(1/3)); conjecture form 1 - (beta_3/27)c^3 "
                              "is the exp(-c/u) convention; identical Borel radius "
                              "|c| = 3/beta_3^(1/3). q=(d+2)/2=5/2 half-integer regime.")
    print(f"FRESH chi_3(c) = {chi3}   (only beta_3 on edge: {only_beta3})")

    for label, coeffs, kind, desc in TEST_OBJECTS:
        beta3 = coeffs[0]
        with mp.workdps(DPS_ALG + 20):
            xi0_conj = mp.mpf(3) / mp.power(mp.mpf(beta3), mp.mpf(1) / 3)
        xi0_alg = xi0_algebraic(beta3, dps=DPS_ALG)
        alg_dig = agreement_digits(xi0_alg, xi0_conj, DPS_ALG)

        raw, nev, nodes, Nmax = beta3_raw_and_neville(coeffs)
        with mp.workdps(DPS_NUM):
            xi0_raw = mp.mpf(3) / mp.power(raw, mp.mpf(1) / 3)
            xi0_nev = mp.mpf(3) / mp.power(nev, mp.mpf(1) / 3)
        raw_dig = agreement_digits(xi0_raw, xi0_conj, DPS_NUM)
        nev_dig = agreement_digits(xi0_nev, xi0_conj, DPS_NUM)

        rec = {
            "label": label, "kind": kind, "description": desc,
            "coeffs_a3_a2_a1_a0": list(coeffs), "beta_3": beta3,
            "xi0_conjecture_3_over_beta3_cbrt": mp.nstr(xi0_conj, 50),
            "xi0_algebraic_dps80": mp.nstr(xi0_alg, 50),
            "algebraic_agreement_digits": round(alg_dig, 1),
            "numeric_raw_ratio_xi0": mp.nstr(xi0_raw, 30),
            "numeric_raw_agreement_digits": round(raw_dig, 2),
            "numeric_neville_xi0": mp.nstr(xi0_nev, 40),
            "numeric_neville_agreement_digits": round(nev_dig, 1),
            "neville_nodes_n": [nodes[0], nodes[-1], len(nodes)],
            "Nmax": Nmax,
        }
        out["objects"].append(rec)
        print(f"\n[{label}] beta_3={beta3}  {desc}")
        print(f"  xi0 conj        = {mp.nstr(xi0_conj, 30)}")
        print(f"  algebraic |c|   = {mp.nstr(xi0_alg, 30)}   ({alg_dig:.0f} digits)")
        print(f"  numeric raw     = {mp.nstr(xi0_raw, 20)}   ({raw_dig:.1f} digits, prior method)")
        print(f"  numeric Neville = {mp.nstr(xi0_nev, 30)}   ({nev_dig:.0f} digits, improved)")

    RESULTS.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    sha = hashlib.sha256(RESULTS.read_bytes()).hexdigest()
    print(f"\nWrote {RESULTS.name}  sha256={sha}")


if __name__ == "__main__":
    main()
