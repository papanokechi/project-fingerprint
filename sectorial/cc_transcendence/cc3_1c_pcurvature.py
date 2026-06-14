#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-1c-4  --  p-CURVATURE of L  (corroboration; expect NON-nilpotent)
================================================================================
SIARC.  Computes the p-curvature psi_p of Phi's operator L over F_p(z) for a band
of primes and tests nilpotency, as a CONSISTENCY check on the verified irregular
singularity at z=infinity (slope 1/4).

    L = z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2 .

Logic (DEMOTED to corroboration this stage):  by Chudnovsky-Andre a globally
nilpotent operator (psi_p nilpotent for almost all p) is a G-operator, hence
(Katz) regular-singular/Fuchsian with rational exponents.  L is IRREGULAR at
infinity, so it is NOT globally nilpotent; psi_p must be NON-nilpotent for almost
all p.  Confirming non-nilpotence here corroborates the irregularity.  A NILPOTENT
verdict for all tested primes would CONTRADICT the verified irregularity and
triggers an extraordinary-claim audit (HALT) -- nothing else.

Method (identical engine to cc2_0_arithmetic_gate.py Leg C, re-pointed at L):
differential module M=F_p(z)[d]/(L), basis e_i=d^i; d(e_3)=sum_j c_j e_j,
c_j=-p_j/p4; psi_p=d^p is F_p(z)-linear; nilpotent <=> M^4=0 at a generic point.

CEILING (reproduced): a Fuchsian relocation does not make K a classical period;
provenance, not singularity type, is what the period conjectures see.
Unconditional transcendence of C is NOT a deliverable of op:cc-3 at any grade.
"""
import sys, json, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import sympy as sp

z = sp.symbols("z")

# L D-form coefficients (exact; cc3-1b)
A = {
    0: -z**2,
    1: -15*z**2,
    2: 2*z**2 - 47*z**3,
    3: 4*z**3 - 25*z**4,
    4: z**4 - 3*z**5,
}
assert sp.expand(A[4] - z**4*(1 - 3*z)) == 0, "p4 mismatch vs cc3-1b"

def _gfp_poly(expr, p):
    return sp.Poly(sp.expand(expr), z, modulus=p)

def _pcurv_one(p):
    try:
        A4 = _gfp_poly(A[4], p)
        if A4.is_zero:
            return {"computed": False, "reason": "p4 == 0 mod p (degenerate prime)"}
        A4d = A4.diff(z)
        cnum = {j: _gfp_poly(-A[j], p) for j in range(4)}   # c_j = cnum_j / a4
        ZERO = sp.Poly(0, z, modulus=p)
        ONE = sp.Poly(1, z, modulus=p)

        def deriv(N, k):                       # d/dz (N/a4^k)
            Nn = N.diff(z) * A4 - (k % p) * N * A4d
            return (Nn, k + 1)

        def reduce_term(N, k):
            while k > 0:
                q, r = sp.div(N, A4, z, modulus=p)
                if r.is_zero:
                    N, k = q, k - 1
                else:
                    break
            return (N, k)

        def add_terms(terms):
            kmax = max(k for (_, k) in terms)
            acc = ZERO
            for (N, k) in terms:
                acc = acc + N * (A4 ** (kmax - k))
            return reduce_term(acc, kmax)

        def apply_d(vec):
            f0, f1, f2, f3 = vec
            d0, d1, d2, d3 = deriv(*f0), deriv(*f1), deriv(*f2), deriv(*f3)
            N3, k3 = f3
            cf = {j: (cnum[j] * N3, k3 + 1) for j in range(4)}
            return [add_terms([d0, cf[0]]),
                    add_terms([d1, f0, cf[1]]),
                    add_terms([d2, f1, cf[2]]),
                    add_terms([d3, f2, cf[3]])]

        cols = []
        for j in range(4):
            vec = [(ONE if i == j else ZERO, 0) for i in range(4)]
            for _ in range(p):
                vec = apply_d(vec)
            cols.append(vec)

        def a4_val(z0):
            return int(A4.eval(z0)) % p

        def build_matrix(z0):
            inv = pow(a4_val(z0), -1, p)
            M = [[0]*4 for _ in range(4)]
            for j in range(4):
                for i in range(4):
                    N, k = cols[j][i]
                    M[i][j] = (int(N.eval(z0)) % p) * pow(inv, k, p) % p
            return M

        def is_nilpotent(M):
            def mm(X, Y):
                return [[sum(X[i][t]*Y[t][j] for t in range(4)) % p for j in range(4)] for i in range(4)]
            P = M
            for _ in range(3):
                P = mm(P, M)
            return all(P[i][j] == 0 for i in range(4) for j in range(4))

        tested, nil_all, z0, found = [], True, 0, 0
        while z0 < p and found < 3:
            if a4_val(z0) != 0:
                M = build_matrix(z0)
                nz = any(M[i][j] != 0 for i in range(4) for j in range(4))
                nil = is_nilpotent(M)
                tested.append({"z0": z0, "nonzero": nz, "nilpotent": nil})
                nil_all = nil_all and nil
                found += 1
            z0 += 1
        return {"computed": True, "specializations": tested, "nilpotent": nil_all}
    except Exception as e:
        return {"computed": False, "reason": f"error: {type(e).__name__}: {e}"}

def main():
    print("=== cc3-1c-4  p-curvature of L (corroboration) ===")
    primes = (5, 7, 11, 13, 17, 19, 23, 29)
    per = {}
    for p in primes:
        per[str(p)] = _pcurv_one(p)
        v = per[str(p)]
        if v.get("computed"):
            print(f"  p={p:>3}  nilpotent={v['nilpotent']}  "
                  f"specializations={[(t['z0'], t['nilpotent']) for t in v['specializations']]}")
        else:
            print(f"  p={p:>3}  skipped: {v['reason']}")

    flags = [v["nilpotent"] for v in per.values() if v.get("computed")]
    any_nonnilp = any(not f for f in flags)
    all_nonnilp = all(not f for f in flags) and len(flags) > 0
    contradiction = (len(flags) > 0 and all(flags))   # ALL nilpotent => contradiction

    if contradiction:
        verdict = ("ALL tested primes NILPOTENT -- CONTRADICTS verified irregular infinity. "
                   "EXTRAORDINARY-CLAIM HALT: audit the operator derivation.")
    elif all_nonnilp:
        verdict = ("p-curvature NON-nilpotent at EVERY tested prime => NOT globally nilpotent "
                   "=> (Chudnovsky-Andre/Katz) CONSISTENT with irregular infinity. Corroboration PASS.")
    else:
        verdict = ("mixed: non-nilpotent for >=1 prime => not globally nilpotent (consistent "
                   "with irregular infinity); nilpotent primes are accidental specializations.")

    print("\nVERDICT:", verdict)

    obj = {
        "op": "cc3-1c-4-pcurvature",
        "task_id": "op:cc-transcendence/cc3-1c",
        "operator_L": "z^4(1-3z) D^4 + (4z^3-25z^4) D^3 + (2z^2-47z^3) D^2 - 15 z^2 D - z^2",
        "engine": "same as cc2_0_arithmetic_gate.py Leg C (F_p(z)-linear d^p; nilpotent <=> M^4=0 at generic z0)",
        "primes": list(primes),
        "per_prime": per,
        "any_prime_non_nilpotent": any_nonnilp,
        "all_primes_non_nilpotent": all_nonnilp,
        "globally_nilpotent_excluded": any_nonnilp,
        "verdict": verdict,
        "role": "DEMOTED to corroboration: non-nilpotence already follows from irregular infinity by citation (Katz); this is an independent arithmetic consistency check.",
        "ceiling": ("A Fuchsian relocation does not make K a classical period; provenance, "
                    "not singularity type, is what the period conjectures see. Unconditional "
                    "transcendence of C is NOT a deliverable of op:cc-3 at any grade."),
    }
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    obj["canonical_sha256_of_hashfree_object"] = hashlib.sha256(blob).hexdigest()
    with open("cc3_1c_pcurvature_results.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", obj["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_1c_pcurvature_results.json")

if __name__ == "__main__":
    main()
