"""Phase 0.4 driver: run the gated PSLQ harness with adversarial null controls.

Order of operations matters here and is deliberate:

  1. Establish that every basis constant is itself VERIFIED (recomputed at
     +30 digits, agreeing).
  2. MEASURE the spurious-relation threshold by running the identical harness
     against random targets across a range of precisions.  This is done BEFORE
     looking at the real target, so the acceptance criterion cannot be tuned
     after seeing the answer.
  3. Only then search around c, and only then run the two required controls.
  4. If a control fails, the basis is overcomplete at the available precision.
     We do not lower the bar: we shrink the basis along a fixed, pre-declared
     nesting and re-run the whole gate.

TWO PRECISION CONSTRAINTS THAT THE SPEC IMPLIES BUT DOES NOT SPELL OUT
----------------------------------------------------------------------
Criterion (a) demands reconfirmation at P+30 with identical coefficients.
A PSLQ run at P+30 digits consumes P+30 digits of the target.  So the search
precision is bounded by the honest digit count D of c:

        P + 30 <= D - margin        =>       P <= D - 33.

Running the search at P = D - 3 and then "reconfirming" at P + 30 = D + 27 is
not a reconfirmation: it feeds PSLQ 27 digits of arithmetic noise and will
always return NO RELATION.  That is a guaranteed-fail protocol, not a test,
and reporting its failure as evidence against the relation would be an error.

Null control (i) perturbs the target to c*(1+1e-20).  For that control to have
any discriminating power the search must be able to RESOLVE the perturbation.
The perturbation is an absolute change of |c|*1e-20, and PSLQ is run with
tol = 10^-(P-GUARD), so the requirement is

        |c| * 10^-20  >  10^-(P - GUARD)   =>   P  >  20 + GUARD + log10|c|.

With GUARD = 8 and |c| ~ 0.44 this is P >= 28, not P >= 20.  The weaker
condition was assumed first and was wrong: at D = 58 the driver picked
P = D - 33 = 25, giving tol = 1e-17 against a perturbation of 4.4e-21, and
control (i) "failed" purely because it was run below its own resolution while
criteria (a), (b) and control (ii) all passed.  A control that cannot see the
thing it perturbs is not evidence about the basis.

P is therefore chosen per basis as the SMALLEST admissible precision,

        P = max( measured spurious threshold,  control-(i) floor ),

since every digit spent on the search is a digit unavailable to the
reconfirmation at P+30.  A reportable positive result then needs

        D  >=  max( T(basis), 20 + GUARD + log10|c| ) + 30 + margin.

A search at the maximum usable precision P_max = D - 3 is also run and logged,
explicitly labelled DIAGNOSTIC: it can exhibit a relation but can never be
reportable, because it cannot satisfy (a).

Every PSLQ call, successful or not, is written to out/pslq_calls.json.
"""

from __future__ import annotations

import json
from mpmath import mp

import constants
import pslq_harness as H

CONST = "out/constant.json"
OUTPUT = "out/pslq_result.json"

#: Pre-declared nesting, largest first.  Fixed before any search is run so
#: that shrinking cannot be steered by what happens to work.
NESTING = [
    ["1", "log2", "logpi", "gamma", "zeta'(-1)", "zeta(3)/pi^2", "Catalan", "log(1+sqrt2)"],
    ["1", "log2", "logpi", "gamma", "zeta'(-1)", "zeta(3)/pi^2"],
    ["1", "log2", "gamma", "zeta'(-1)"],
    ["1", "log2", "zeta'(-1)"],
]
MAXCOEFF = 10 ** 4
RECONFIRM_BUMP = 30
PERTURB_DIGIT = 20
GUARD = 8          # must match pslq_harness.pslq_search's tol = 10^-(dps-guard)
MARGIN = 3


def control_sensitivity_floor(c):
    """Smallest P at which null control (i) can actually discriminate.

    Control (i) perturbs the target to c*(1+1e-20), an ABSOLUTE change of
    |c|*1e-20.  PSLQ is run with tol = 10^-(P-GUARD).  If the perturbation is
    smaller than the tolerance, PSLQ cannot see it, returns the same relation
    for the perturbed target as for the true one, and the control fails --
    not because the basis is overcomplete, but because the control was run
    below its own resolution.  That is a broken control, and reporting its
    failure as evidence about the basis would be wrong.

    Requiring |c| * 10^-20 > 10^-(P-GUARD) gives

        P  >  20 + GUARD + log10|c|.

    This was found empirically: at D=58 the driver chose P = D-33 = 25, giving
    tol = 1e-17 against a perturbation of 4.4e-21, and control (i) duly failed
    while control (ii) passed and criteria (a),(b) passed.
    """
    return int(mp.ceil(PERTURB_DIGIT + GUARD + mp.log10(abs(c)))) + MARGIN


def main():
    d = json.load(open(CONST))
    D = int(d["honest_digits_c"])
    P_max = D - MARGIN
    mp.dps = D + 60
    c = mp.mpf(d["c_full"])
    ctrl_floor = control_sensitivity_floor(c)

    print("=" * 78)
    print("PHASE 0.4  PSLQ HARNESS")
    print("=" * 78)
    print(f"  honest digits in c, D            : {D}")
    print(f"  control-(i) sensitivity floor    : P >= {ctrl_floor}")
    print(f"  reconfirmation budget            : P + {RECONFIRM_BUMP} <= {P_max}")
    print(f"  diagnostic precision P_max       : {P_max}  "
          "(cannot satisfy criterion (a))")
    print(f"  coefficient sup-norm threshold   : {MAXCOEFF}")
    print("\n  P is chosen per basis as the SMALLEST admissible precision,")
    print("  P = max(measured spurious threshold, control-(i) floor),")
    print("  because every digit spent on the search is a digit unavailable")
    print("  for the reconfirmation at P+30.")

    print("\n[1] basis constants recomputed at +30 digits")
    for nm, dg in constants.check_constants(max(P_max, 30)):
        print(f"    {nm:<14} agrees to {mp.nstr(dg, 6)} digits")
    _, _, dg = constants.glaisher_cross_check(max(P_max, 30))
    print(f"    zeta'(-1) vs 1/12 - log(Glaisher): agrees to {mp.nstr(dg,6)} digits")

    result = {"honest_digits_c": D, "P_max": P_max,
              "control_sensitivity_floor": ctrl_floor,
              "maxcoeff": MAXCOEFF, "stages": []}

    for names_wanted in NESTING:
        names, vals = constants.basis_values(P_max + 60, names_wanted)
        m = len(names)
        print("\n" + "-" * 78)
        print(f"[basis of {m}] {names}")
        print("-" * 78)

        print("  [2] spurious-relation threshold (random targets, blind to c)")
        # Step 1 through the band where the threshold actually lands.  L-030:
        # a step-5 sweep here resolves T only to +/-5 and made a FALSE linear
        # law T = 5b+10 look exact, because the sampling interval equalled the
        # fitted slope.  Since T is spent directly out of the digit budget
        # (P >= T, and P+30 <= D-3), a 5-digit over-estimate of T costs 5
        # digits of reconfirmation headroom and can skip a basis needlessly.
        sweep = sorted({x for x in
                        {10, 15, 20} | set(range(22, 56)) | {60, 70, 80, P_max}
                        if 5 <= x <= P_max + 40})
        thr, table = H.spurious_threshold(sweep, names, vals,
                                          maxcoeff=MAXCOEFF, trials=3)
        for row in table:
            print(f"      dps={row['dps']:<5} random targets={row['random_targets']} "
                  f"relations found={row['relations_found']}")
        print(f"    -> spurious relations persist below dps {thr}; "
              f"basis usable only for P >= {thr}")

        P = max(thr if thr is not None else 10 ** 6, ctrl_floor)
        budget_ok = (P + RECONFIRM_BUMP) <= P_max
        print(f"    -> P = max({thr}, {ctrl_floor}) = {P}; "
              f"needs P+{RECONFIRM_BUMP} = {P + RECONFIRM_BUMP} <= {P_max}  "
              f"-> {'OK' if budget_ok else 'INSUFFICIENT PRECISION'}")
        if not budget_ok:
            print(f"    -> this basis needs c to >= {P + RECONFIRM_BUMP + MARGIN} "
                  f"honest digits; have {D}.")

        print(f"  [3] DIAGNOSTIC search at P_max={P_max} "
              "(not reportable by construction)")
        diag = H.pslq_search(c, P_max, names, vals, maxcoeff=MAXCOEFF,
                             kind=f"DIAGNOSTIC P_max={P_max}")
        if diag is not None:
            print(f"      {H.format_relation(diag, names)}")

        if budget_ok:
            print(f"  [4] gated search at P={P}, reconfirmation at P+{RECONFIRM_BUMP}")
            verdict = H.vet_relation(c, P, names, vals, maxcoeff=MAXCOEFF,
                                     bump=RECONFIRM_BUMP)
            print("  [5] null controls")
            nulls = H.null_controls(c, P, names, vals, maxcoeff=MAXCOEFF)
            print(f"      null controls {'PASS' if nulls['passed'] else 'FAIL'}")
        else:
            verdict = {"reportable": False, "relation": None,
                       "reasons": [f"skipped: P+{RECONFIRM_BUMP} exceeds the "
                                   f"{D} honest digits available"]}
            nulls = {"perturbed": None, "random": None, "passed": False}
            print("  [4,5] SKIPPED: running them here would be a guaranteed-fail "
                  "protocol, not a test.")

        stage = {
            "basis": names,
            "basis_size": m,
            "P": P,
            "precision_budget_ok": budget_ok,
            "spurious_threshold_dps": thr,
            "spurious_table": table,
            "diagnostic_relation": None if diag is None else [int(x) for x in diag],
            "diagnostic_pretty": None if diag is None else H.format_relation(diag, names),
            "relation": verdict["relation"],
            "criteria_ab": verdict["reportable"],
            "reasons": verdict["reasons"],
            "null_perturbed": None if nulls["perturbed"] is None
                              else [int(x) for x in nulls["perturbed"]],
            "null_random": None if nulls["random"] is None
                           else [int(x) for x in nulls["random"]],
            "null_controls_passed": nulls["passed"],
        }
        if diag is not None:
            stage["diagnostic_residual"] = mp.nstr(H.residual(diag, c, vals, P_max), 6)
        if verdict["relation"] is not None:
            stage["relation_pretty"] = H.format_relation(verdict["relation"], names)
            stage["relation_residual"] = mp.nstr(
                H.residual(verdict["relation"], c, vals, P), 6)

        reportable = verdict["reportable"] and nulls["passed"] and budget_ok
        stage["REPORTABLE"] = reportable
        result["stages"].append(stage)

        if reportable:
            print(f"\n  >>> REPORTABLE at basis size {m}: (a) reconfirmed at "
                  f"P+{RECONFIRM_BUMP} with identical coefficients, (b) sup-norm "
                  "within threshold, (c) both null controls empty, and P is at or "
                  "above the measured spurious threshold.")
            print(f"      {stage['relation_pretty']}")
            result["final"] = stage
            break
        print(f"\n  >>> NOT reportable at basis size {m}; "
              "shrinking basis per the pre-declared nesting.")
    else:
        print("\n  No basis in the nesting produced a reportable relation.")
        result["final"] = None

    H.flush_log()
    json.dump(result, open(OUTPUT, "w"), indent=1)
    print("\nwrote", OUTPUT, "and", H.LOG)


if __name__ == "__main__":
    main()
