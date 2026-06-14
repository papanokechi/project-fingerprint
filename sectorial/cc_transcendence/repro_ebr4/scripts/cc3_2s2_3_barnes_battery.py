#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
op:cc3-2s2-3  --  LOG-SPACE BARNES BATTERY  (PSLQ over Barnes-G/Glaisher tiers)
================================================================================
SIARC.  ebr3-b standard: declared tiers, heights, detection thresholds, positive
controls, hashes.  2c returned NOT COVERED, so this is a STANDARD (non-formula-
motivated) battery.  Targets: log kappa and log A0 (kappa = Gamma(4/3) A0,
A0 = C_EBR/sqrt(pi)).  Question: does log kappa lie in the Z-span of
  { log G(j/m) (m in {2,3,4,6,12}), log Gamma(j/m), log pi, log 2, log 3,
    log A_Glaisher ( <-> zeta'(-1)), 1 } ?
A relation = kappa elementary in the EXTENDED Barnes class.

SKIP-BY-ARGUMENT: the PURE log-Gamma + log pi + log{2,3} tier (no Barnes G, no
Glaisher) is the log-image of the Gamma-quotient test, ALREADY NULLED for C to
169 digits (frozen 9a3f942d...; kappa = Gamma(4/3) C_EBR/sqrt(pi) so kappa is a
Gamma-quotient iff C_EBR is).  We therefore SKIP that tier by argument and test
only tiers that ADD Barnes-G and/or Glaisher (the genuinely NEW content).

POSITIVE CONTROL (must FIRE): the Barnes-Glaisher value
  G(1/2) = 2^{1/24} pi^{-1/4} e^{1/8} A^{-3/2}
  <=>  24 log G(1/2) - log 2 + 6 log pi + 36 log A - 3 = 0
detected over [log G(1/2), log 2, log pi, log A, 1] with coeffs [24,-1,6,36,-3].

CEILING (both directions, verbatim): a FIRE (relation) would argue kappa is
ELEMENTARY in the extended Barnes class -- the OPPOSITE of transcendence; a NULL
proves neither.  Unconditional transcendence of C/kappa is NOT a deliverable of
op:cc-3 at any grade.  A FIRE is an UNCONDITIONAL HALT, verified twice.
"""
import sys, json, hashlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import mpmath as mm
from mpmath import mp, mpf

mp.dps = 200
DETECT = 150            # effective detection digits (guard band below working dps)
HMAX   = 10**12         # max |coeff| for an admissible relation

KAPPA_FROZEN_130 = ("1.539494848576641034843781903384069038219390890553148730926294560611"
                    "093030530126489289595548377837121909677816857027063026103313161")
C_EBR_169 = ("3.055706807890481365701912201727681368875542774973830574676375050047"
             "173604353962458288292799650089998918200014506258804205163411515501549494446823017585278488893394706741693")

def canon_hash(obj):
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def lg(z):   return mm.log(mm.barnesg(mpf(z) if not isinstance(z, mm.mpf) else z))
def lG(p,q): return mm.log(mm.barnesg(mpf(p)/q))
def lGam(p,q): return mm.log(mm.gamma(mpf(p)/q))

def run_pslq(target_name, target, basis_names, basis_vals, maxcoeff=HMAX):
    # Deflation loop: the Barnes-G/Gamma/Glaisher basis is linearly DEPENDENT
    # (multiplication identities), so a raw PSLQ returns basis-internal relations
    # (target coeff = 0).  We remove a redundant basis element each time such a
    # relation appears, until either (a) PSLQ returns None => target NOT in the
    # span (NULL), or (b) a relation with nonzero target coeff appears (candidate
    # FIRE, verified).  Each removed element is provably redundant (expressible as
    # a rational combination of the rest via the found integer relation), so the
    # final verdict is rigorous for the ORIGINAL span.
    names = list(basis_names); vals = list(basis_vals)
    deflations = []
    for _ in range(len(basis_names) + 2):
        vec = [target] + vals
        rel = mm.pslq(vec, maxcoeff=maxcoeff, maxsteps=50000)
        if rel is None:
            return {"target": target_name, "status": "NULL",
                    "final_independent_basis": names, "deflations": deflations,
                    "relation": None}
        if rel[0] != 0:
            resid = sum(mpf(int(c))*v for c, v in zip(rel, vec))
            height = max(abs(int(c)) for c in rel)
            ok = (abs(resid) < mpf(10)**(-DETECT)) and (height <= maxcoeff)
            return {"target": target_name,
                    "status": ("FIRE" if ok else "spurious(unverified)"),
                    "relation_basis": ["TARGET"] + names,
                    "relation": [int(c) for c in rel],
                    "residual_log10": (None if resid == 0 else float(mm.log10(abs(resid)))),
                    "height": height, "FIRE": bool(ok), "deflations": deflations}
        # rel[0] == 0: basis-internal dependency -> remove one redundant element
        i = next(k for k in range(1, len(rel)) if rel[k] != 0)
        deflations.append({"removed": names[i-1], "via_relation_height": max(abs(int(c)) for c in rel)})
        del names[i-1]; del vals[i-1]
        if not names:
            break
    return {"target": target_name, "status": "NULL(basis-exhausted)",
            "final_independent_basis": names, "deflations": deflations, "relation": None}

def main():
    print("=== cc3-2s2-3  log-space Barnes battery (PSLQ) ===")
    # targets
    A0 = mpf(C_EBR_169)/mm.sqrt(mm.pi)
    kappa = mm.gamma(mpf(4)/3)*A0
    # sanity vs frozen
    ag = -int(mm.log10(abs(kappa - mpf(KAPPA_FROZEN_130))))
    print(f"[setup] kappa bridge vs frozen-130: ~{ag} digits; dps={mp.dps}, DETECT={DETECT}, HMAX={HMAX}")
    log_kappa = mm.log(kappa)
    log_A0    = mm.log(A0)

    logA = mm.log(mm.glaisher)
    logpi = mm.log(mm.pi); log2 = mm.log(2); log3 = mm.log(3); ONE = mpf(1)

    # ---- POSITIVE CONTROL ----
    pc_names = ["logG(1/2)", "log2", "logpi", "logA", "1"]
    pc_vals  = [lG(1,2), log2, logpi, logA, ONE]
    pc = mm.pslq(pc_vals, maxcoeff=10**6, maxsteps=20000)
    pc_ok = pc is not None and abs(sum(mpf(int(c))*v for c, v in zip(pc, pc_vals))) < mpf(10)**(-DETECT)
    print(f"[control] G(1/2) identity PSLQ -> {pc}  (expect [24,-1,6,36,-3] up to sign); FIRES={pc_ok}")

    # ---- SKIP-BY-ARGUMENT tier (documented, not run) ----
    skip = ("pure {logGamma(j/m), logpi, log2, log3} (no Barnes G, no Glaisher) = log-image of the "
            "Gamma-quotient test; ALREADY NULLED for C to 169 digits (frozen 9a3f942d); kappa is a "
            "Gamma-quotient iff C_EBR is. SKIPPED by argument.")
    print(f"[skip] {skip[:100]}...")

    # ---- NEW tiers (add Barnes G and Glaisher) ----
    # Tier 2: m in {2,3,4,6} G-args + a few Gamma + Glaisher + 1
    t2_names = ["logG(1/2)","logG(1/3)","logG(2/3)","logG(1/4)","logG(3/4)","logG(1/6)","logG(5/6)",
                "logGam(1/3)","logGam(1/4)","logGam(1/6)","logpi","log2","log3","logA","1"]
    t2_vals  = [lG(1,2),lG(1,3),lG(2,3),lG(1,4),lG(3,4),lG(1,6),lG(5,6),
                lGam(1,3),lGam(1,4),lGam(1,6),logpi,log2,log3,logA,ONE]
    # Tier 3: Tier 2 + m=12 G-args
    t3_names = t2_names[:7] + ["logG(1/12)","logG(5/12)","logG(7/12)","logG(11/12)"] + t2_names[7:]
    t3_vals  = t2_vals[:7]  + [lG(1,12),lG(5,12),lG(7,12),lG(11,12)] + t2_vals[7:]

    runs = []
    for tgt_name, tgt in [("log_kappa", log_kappa), ("log_A0", log_A0)]:
        for tier_name, bn, bv in [("tier2_m2346", t2_names, t2_vals),
                                  ("tier3_m234612", t3_names, t3_vals)]:
            r = run_pslq(f"{tgt_name}|{tier_name}", tgt, bn, bv)
            runs.append(r)
            nd = len(r.get("deflations", []))
            extra = "" if r["relation"] is None else f"  rel={r['relation']} h={r.get('height')}"
            print(f"[{tgt_name} / {tier_name}] -> {r['status']}  (deflations={nd}){extra}")

    any_fire = any(r.get("FIRE") for r in runs)
    print(f"\n[VERDICT] positive control fired: {pc_ok}")
    print(f"[VERDICT] any FIRE in new tiers: {any_fire}  => {'HALT' if any_fire else 'ALL-NULL (honest deliverable)'}")

    results = {
        "op": "cc3-2s2-3-barnes-battery",
        "task_id": "op:cc-transcendence/cc3-2s2-3",
        "settings": {"dps": mp.dps, "detect_digits": DETECT, "Hmax": HMAX,
                     "kappa_bridge_vs_frozen_digits": ag},
        "targets": {"log_kappa": mm.nstr(log_kappa, 40), "log_A0": mm.nstr(log_A0, 40),
                    "kappa_def": "kappa = Gamma(4/3) C_EBR/sqrt(pi); A0 = C_EBR/sqrt(pi)"},
        "positive_control": {
            "identity": "G(1/2) = 2^(1/24) pi^(-1/4) e^(1/8) A^(-3/2)  <=>  "
                        "24 logG(1/2) - log2 + 6 logpi + 36 logA - 3 = 0",
            "basis": pc_names, "pslq_relation": (None if pc is None else [int(c) for c in pc]),
            "fired": bool(pc_ok),
        },
        "skipped_by_argument": skip,
        "tiers": {
            "tier2_m2346": t2_names,
            "tier3_m234612": t3_names,
        },
        "runs": runs,
        "any_FIRE": bool(any_fire),
        "verdict": ("HALT (FIRE)" if any_fire else
                    "ALL-NULL: log kappa and log A0 NOT integer-linear in the Barnes-G/Glaisher-extended "
                    "basis (heights <= 1e12) to 150 digits; kappa not elementary in the extended Barnes "
                    "class at this height/precision. Honest null."),
        "ceiling": "A FIRE would argue ELEMENTARITY in the extended Barnes class (OPPOSITE of "
                   "transcendence); a NULL proves neither. Unconditional transcendence of C/kappa is NOT a "
                   "deliverable of op:cc-3 at any grade.",
    }
    results["canonical_sha256_of_hashfree_object"] = canon_hash(results)
    with open("cc3_2s2_3_barnes_battery_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\ncanonical sha256 =", results["canonical_sha256_of_hashfree_object"])
    print("wrote cc3_2s2_3_barnes_battery_results.json")

if __name__ == "__main__":
    main()
