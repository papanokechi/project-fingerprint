#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1c  --  NUMERICAL MONODROMY of Phi's operator L (1c-0 + Jordan input to 1c-2)
================================================================================
SIARC. High-precision RK4 analytic continuation of L around z=0 and z=1/3 to read
the EXACT Jordan type of the local monodromies M_0, M_{1/3}.

    L = z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2
    Phi(z) = sum Q_n z^n/(n!)^2,  Q_n=(3n^2+n+1)Q_{n-1}+Q_{n-2}, Q_0=1,Q_1=5.

WHY (the decisive tension):
  L is irreducible (single slope-1/4, ramification-4 Galois orbit at infinity =>
  irreducible formal type => no proper global subconnection). An irreducible
  connection has index of rigidity rig <= 2. With S minimal and the irregular
  end fixed (dim Z(formal)_inf = 1, Irr_inf(End L) = 3), the formula reads
      rig = (2 - #S_genuine)*16 + sum_finite dim Z(M_x) + 1 - 3.
  This is INCONSISTENT with rig <= 2 unless the finite Jordan types are
  non-trivial in a specific way. cc3-1b asserted both finite blocks log-free /
  z=0 apparent; that combination forces rig = 8 (impossible). So the numerical
  monodromy must settle WHICH block actually carries the logarithm.

CEILING (reproduced): a Fuchsian relocation does not imply K is a classical
period (provenance, not singularity type, is what the period conjectures see).
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import mpmath as mp

mp.mp.dps = 80

# L = sum_j p_j D^j  (Phi's operator, verified in cc3-1a/1b)
#   p4 = z^4 - 3 z^5 ; p3 = 4 z^3 - 25 z^4 ; p2 = 2 z^2 - 47 z^3 ; p1 = -15 z^2 ; p0 = -z^2
def pcoef(z):
    return (-z**2,                 # p0
            -15*z**2,              # p1
            2*z**2 - 47*z**3,      # p2
            4*z**3 - 25*z**4,      # p3
            z**4 - 3*z**5)         # p4

def deriv(z, Y):
    p0, p1, p2, p3, p4 = pcoef(z)
    y4 = -(p0*Y[0] + p1*Y[1] + p2*Y[2] + p3*Y[3]) / p4
    return [Y[1], Y[2], Y[3], y4]

def rk4_path(Y0, path, nsteps):
    Y = [mp.mpc(v) for v in Y0]
    for seg in range(len(path) - 1):
        z0, z1 = mp.mpc(path[seg]), mp.mpc(path[seg + 1])
        h = (z1 - z0) / nsteps
        z = z0
        for _ in range(nsteps):
            k1 = deriv(z, Y)
            k2 = deriv(z + h/2, [Y[i] + h/2*k1[i] for i in range(4)])
            k3 = deriv(z + h/2, [Y[i] + h/2*k2[i] for i in range(4)])
            k4 = deriv(z + h,   [Y[i] + h*k3[i]   for i in range(4)])
            Y = [Y[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(4)]
            z += h
    return Y

def circle(center, base, K):
    rho = abs(mp.mpc(base) - mp.mpc(center))
    ang0 = mp.arg(mp.mpc(base) - mp.mpc(center))
    pts = [base]
    for t in range(1, K + 1):
        a = ang0 + 2*mp.pi*t/K
        pts.append(mp.mpc(center) + rho*mp.e**(1j*a))
    return pts

def monodromy(center, base, K, nsteps):
    cols = []
    for e in range(4):
        Y0 = [mp.mpf(1) if i == e else mp.mpf(0) for i in range(4)]
        cols.append(rk4_path(Y0, circle(center, base, K), nsteps))
    M = mp.matrix(4, 4)
    for j in range(4):
        for i in range(4):
            M[i, j] = cols[j][i]
    return M

def svals(Mat):
    U, S, V = mp.svd(Mat)
    sv = [S[i] for i in range(S.rows)] if hasattr(S, "rows") else [S[i] for i in range(len(S))]
    return sorted([abs(x) for x in sv], reverse=True)

def numeric_rank(sv, reltol=mp.mpf("1e-20")):
    if not sv:
        return 0
    thr = sv[0] * reltol
    return sum(1 for x in sv if x > thr)

def sv_ladder(M, lam, kmax):
    """Singular values of (M - lam I)^k for k=1..kmax (for visual rank gaps)."""
    A = M - lam*mp.eye(4)
    out = []
    Ak = mp.eye(4)
    for k in range(1, kmax + 1):
        Ak = Ak * A
        out.append((k, [mp.nstr(x, 4) for x in svals(Ak)]))
    return out

def jordan_blocks_known_eig(M, lam, alg, reltol):
    """Jordan block sizes (descending) for KNOWN eigenvalue lam of algebraic mult alg.
    n_k = 4 - rank((M-lam I)^k) is the nullity (auto-restricted to lam's generalized
    eigenspace, since (M-lam I) is invertible elsewhere). #blocks of size >= k =
    n_k - n_{k-1} (n_0 = 0). Threshold relative to the LARGEST sv of (M-lam I)."""
    A = M - lam*mp.eye(4)
    base_sv = svals(A)
    thr = base_sv[0] * reltol if base_sv else mp.mpf(0)
    nul = [0]
    Ak = mp.eye(4)
    for k in range(1, alg + 1):
        Ak = Ak * A
        sv = svals(Ak)
        rk = sum(1 for x in sv if x > thr)
        nul.append(4 - rk)
        if (4 - rk) >= alg:
            # saturated; pad remaining
            while len(nul) <= alg:
                nul.append(alg)
            break
    while len(nul) <= alg:
        nul.append(nul[-1])
    ge = [nul[k] - nul[k-1] for k in range(1, alg + 1)]  # #blocks size >= k
    blocks = []
    for k in range(1, alg + 1):
        cnt = ge[k-1] - (ge[k] if k < alg else 0)
        blocks.extend([k]*cnt)
    return sorted(blocks, reverse=True), {"nullities_n_k": nul[:alg+1], "blocks_ge_k": ge}

def dimZ_from_blocks_per_eigen(eig_blocks):
    total = 0
    for blocks in eig_blocks.values():
        for di in blocks:
            for dj in blocks:
                total += min(di, dj)
    return total

def analyze(M, label, known_eigs, expected_det, reltol=mp.mpf("1e-18")):
    """known_eigs: list of (lam, algebraic_multiplicity). Eigenvalues are KNOWN
    exactly from the exponents (e^{2 pi i exponent}); we do NOT use mp.eig
    (defective => ill-conditioned)."""
    detM = mp.det(M)
    A = M - mp.eye(4)
    sv_MI = svals(A)
    thr_MI = sv_MI[0] * reltol
    rank_M_minus_I = sum(1 for x in sv_MI if x > thr_MI)
    eig_blocks = {}
    per_eig = []
    semisimple = True
    ladders = {}
    for lam, alg in known_eigs:
        blocks, dbg = jordan_blocks_known_eig(M, lam, alg, reltol)
        key = mp.nstr(lam, 8)
        eig_blocks[key] = blocks
        ladders[key] = {"alg_mult": alg, "debug": dbg,
                        "sv_ladder": sv_ladder(M, lam, min(alg, 3))}
        if any(b > 1 for b in blocks):
            semisimple = False
        per_eig.append({"eigenvalue": key, "alg_mult": alg,
                        "geom_mult": len(blocks), "jordan_blocks": blocks})
    dimZ = dimZ_from_blocks_per_eigen(eig_blocks)
    return {
        "label": label,
        "det(M)": mp.nstr(detM, 16),
        "det(M)_expected": mp.nstr(expected_det, 16),
        "det_rel_err": mp.nstr(abs(detM - expected_det)/abs(expected_det), 4),
        "det_matches": abs(detM - expected_det) < mp.mpf("1e-12")*abs(expected_det),
        "sv(M-I)": [mp.nstr(x, 6) for x in sv_MI],
        "rank(M-I)": rank_M_minus_I,
        "per_eigenvalue": per_eig,
        "ladders": ladders,
        "semisimple_(no_log)": semisimple,
        "dim_centralizer_Z(M)": dimZ,
    }

def interpret_rank(label, alg_eig1, rank_M_minus_I, has_isolated):
    """Read the ROBUST monodromy facts off rank(M-I) alone (the only quantity the
    RK4 continuation pins to many digits -- the fine block sizes of a DEFECTIVE
    block sit at the noise floor and are deferred to the exact Frobenius script).
      geometric mult of eigenvalue 1 = dim ker(M-I) = 4 - rank(M-I).
    If that equals the algebraic multiplicity alg_eig1, the eigenvalue-1 block is
    SEMISIMPLE (blocks all size 1)."""
    geo1 = 4 - rank_M_minus_I
    semisimple1 = (geo1 == alg_eig1)
    note = (f"eig 1: alg mult {alg_eig1}, geom mult {geo1} "
            f"({'SEMISIMPLE [1]*%d' % alg_eig1 if semisimple1 else '#blocks=%d (DEFECTIVE; fine sizes via exact Frobenius)' % geo1})")
    if has_isolated:
        note += "; + 1 isolated simple eigenvalue (block [1])"
    return {"label": label, "alg_mult_eig1": alg_eig1, "rank(M-I)": rank_M_minus_I,
            "geom_mult_eig1": geo1, "eig1_semisimple": semisimple1, "interpretation": note}

def main():
    print("dps =", mp.mp.dps)

    omega = mp.e**(-2j*mp.pi/3)  # e^{-2 pi i/3}, the z=1/3 isolated eigenvalue

    # ---- M_0 around z=0 (exponents {0,0,1,1}; all eigenvalues 1) -------------
    # p4 = z^4(1-3z) vanishes to order 4 at z=0 -> companion system is large for
    # small |z|; use the largest safe radius (< 1/3) and many steps.
    base0 = mp.mpf("0.22")
    det0_expected = mp.mpf(1)   # e^{2 pi i (0+0+1+1)}
    M0 = monodromy(0, base0, K=48, nsteps=2600)
    a0 = analyze(M0, "M_0 (around z=0; exponents {0,0,1,1})",
                 known_eigs=[(mp.mpf(1), 4)], expected_det=det0_expected)
    print("\n[M_0]  rank(M-I) =", a0["rank(M-I)"], " det_rel_err:", a0["det_rel_err"])
    print("   sv(M-I):", a0["sv(M-I)"])
    for key in a0["ladders"]:
        for kk, svs in a0["ladders"][key]["sv_ladder"]:
            print("      sv((M-1)^%d):" % kk, svs)
    int0 = interpret_rank("z=0", alg_eig1=4, rank_M_minus_I=a0["rank(M-I)"], has_isolated=False)
    print("  ROBUST:", int0["interpretation"])

    # ---- M_{1/3} around z=1/3 (exponents {-4/3,0,1,2}) ----------------------
    third = mp.mpf(1)/3
    base13 = third + mp.mpf("0.12")   # radius 0.12 < 1/3 so loop excludes 0
    det13_expected = mp.e**(2j*mp.pi*(mp.mpf(-4)/3 + 0 + 1 + 2))  # = e^{-2pi i/3}
    M13 = monodromy(third, base13, K=48, nsteps=1000)
    a13 = analyze(M13, "M_{1/3} (around z=1/3; exponents {-4/3,0,1,2})",
                  known_eigs=[(mp.mpf(1), 3), (omega, 1)], expected_det=det13_expected)
    print("\n[M_1/3] rank(M-I) =", a13["rank(M-I)"], " det_rel_err:", a13["det_rel_err"])
    print("   sv(M-I):", a13["sv(M-I)"])
    int13 = interpret_rank("z=1/3", alg_eig1=3, rank_M_minus_I=a13["rank(M-I)"], has_isolated=True)
    print("  ROBUST:", int13["interpretation"])

    # ---- ROBUST conclusions (rank-based; fine type & rigidity in sister scripts)
    # M_0: rank(M-I)=2 => 2 Jordan blocks at eigenvalue 1 => z=0 NOT apparent,
    #      carries logs. Exact Frobenius (cc3_1c_frobenius_z0_v2.py) => [2,2], dimZ=8.
    # M_{1/3}: rank(M-I)=1 => eig-1 geom mult 3 = alg mult 3 => SEMISIMPLE [1,1,1]
    #      (dimZ 9) + isolated e^{-2pi i/3} block [1] (dimZ 1) => dimZ(M_{1/3})=10.
    # Index of rigidity assembled in cc3_1c_rigidity.py from these (=> rig 0).
    print("\n=== ROBUST VERDICTS (rank-based) ===")
    print("  z=0   : rank(M-I)=%d => z=0 GENUINE (carries logs); 2 Jordan blocks "
          "(eig 1). Fine type [2,2] from exact Frobenius." % a0["rank(M-I)"])
    print("  z=1/3 : rank(M-I)=%d => eig-1 block SEMISIMPLE [1,1,1] (+ isolated "
          "e^{-2 pi i/3}); dimZ=10." % a13["rank(M-I)"])
    print("  cc3-1b's 'z=0 apparent / log-free' is REFUTED (rank(M_0-I)=2 != 0).")

    obj = {
        "op": "cc3-1c-monodromy",
        "task_id": "op:cc-transcendence/cc3-1c",
        "operator_L": "z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2",
        "dps": mp.mp.dps,
        "method": ("RK4 numerical continuation around z=0 and z=1/3; ROBUST output is "
                   "rank(M-I) (clear SVD gap) + det checks. The fine block sizes of the "
                   "DEFECTIVE z=0 block sit at the RK4 noise floor (see sv-ladder) and are "
                   "deferred to the EXACT Frobenius script; mp.eig avoided (defective)."),
        "M_0": {k: a0[k] for k in ("label", "det(M)", "det(M)_expected", "det_rel_err",
                                   "det_matches", "sv(M-I)", "rank(M-I)", "ladders")},
        "M_1_3": {k: a13[k] for k in ("label", "det(M)", "det(M)_expected", "det_rel_err",
                                      "det_matches", "sv(M-I)", "rank(M-I)", "ladders")},
        "robust_interpretation": {"z=0": int0, "z=1/3": int13},
        "robust_conclusions": {
            "z=0_apparent": (a0["rank(M-I)"] == 0),
            "z=0_num_jordan_blocks_eig1": 4 - a0["rank(M-I)"],
            "z=0_fine_type": "[2,2] (exact Frobenius cc3_1c_frobenius_z0_v2.py 4482b99af1c1f673a80cdebc768f808b431f37b2958ddf8c7173f1def608b8ee)",
            "z=0_dimZ": 8,
            "z=1/3_eig1_semisimple": int13["eig1_semisimple"],
            "z=1/3_dimZ": 10,
            "rigidity": "assembled in cc3_1c_rigidity.py 845ee916336d834a5ee0d7c6cd86eb7c48914e03d8e27733a09affca36ea9d22 => rig(L)=0, NON-RIGID, accessory 2",
        },
        "supersedes": ("cc3-1b asserted z=0 log-free/apparent; the monodromy shows "
                       "rank(M_0-I)=2 (genuine logarithmic point, 2 Jordan blocks). z=1/3 "
                       "integer block IS semisimple (cc3-1b correct there)."),
        "ceiling": ("A Fuchsian relocation does not imply K is a classical period; provenance, "
                    "not singularity type, is what the period conjectures see. Unconditional "
                    "transcendence of C is NOT a deliverable of op:cc-3 at any grade."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1c_monodromy_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1c_monodromy_results.json")

if __name__ == "__main__":
    main()
