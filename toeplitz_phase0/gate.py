"""Phase 0.3: CALIBRATION GATE.

Tests the extracted constant c against the candidate closed form

    c  =?=  (1/12) log 2 + 3 zeta'(-1)

supplied by the operator in the task statement.  Both pieces are COMPUTED here
by mpmath; nothing is transcribed.  The *form* of the candidate is tagged
CONJECTURED and stays that way until the operator confirms the reference
(Dyson / Widom, with rigorous proof attributed to Krasovsky and to
Deift-Its-Krasovsky) -- see open_questions.md, item OS-1.

GATE RULE: agreement of fewer than 12 digits => HALT.  In that event the
conclusion is that the pipeline is wrong, not the literature; this script
exits non-zero and prints a diagnosis checklist.

A subtlety the gate deliberately checks: agreement should be consistent with
sigma_c from the fit.  Agreement much BETTER than sigma_c would mean sigma_c
is over-conservative; agreement much WORSE means the error bar is a lie.  Both
are reported.
"""

from __future__ import annotations

import json
import sys
from mpmath import mp

GATE_DIGITS = 12
CONST = "out/constant.json"
OUTPUT = "out/gate.json"


def candidate(dps):
    """(1/12) log 2 + 3 zeta'(-1), computed at precision dps."""
    with mp.workdps(dps + 15):
        v = mp.log(2) / 12 + 3 * mp.zeta(-1, 1, 1)
    with mp.workdps(dps):
        return +v


def main():
    d = json.load(open(CONST))
    nd = int(d["honest_digits_c"])
    work = max(60, nd + 40)
    mp.dps = work

    c = mp.mpf(d["c_full"])
    sigma = mp.mpf(d["sigma_c"])
    tgt = candidate(work)

    diff = abs(c - tgt)
    agree = mp.inf if diff == 0 else -mp.log10(diff)

    print("=" * 78)
    print("PHASE 0.3  CALIBRATION GATE")
    print("=" * 78)
    print(f"  c   (VERIFIED, this session, {nd} honest digits)")
    print(f"      = {mp.nstr(c, min(nd + 2, 60))}")
    print(f"  sigma_c                       = {mp.nstr(sigma, 6)}")
    print(f"  candidate (CONJECTURED form) (1/12)log2 + 3 zeta'(-1)")
    print(f"      = {mp.nstr(tgt, min(nd + 2, 60))}")
    print(f"  |c - candidate|               = {mp.nstr(diff, 6)}")
    print(f"  AGREEMENT                     = {mp.nstr(agree, 8)} digits")
    print(f"  gate threshold                = {GATE_DIGITS} digits")

    consistent = diff <= 10 * sigma
    print(f"\n  agreement vs error bar: |c - candidate| {'<=' if consistent else '>'}"
          f" 10*sigma_c  -> {'CONSISTENT' if consistent else 'INCONSISTENT'}")
    if not consistent:
        print("    WARNING: the quoted sigma_c does not cover the observed"
              " discrepancy; the error budget is understating something.")

    passed = agree >= GATE_DIGITS
    out = {
        "c": mp.nstr(c, min(nd + 2, 80)),
        "candidate": mp.nstr(tgt, min(nd + 2, 80)),
        "abs_diff": mp.nstr(diff, 8),
        "agreement_digits": mp.nstr(agree, 8),
        "gate_threshold": GATE_DIGITS,
        "passed": bool(passed),
        "sigma_consistent": bool(consistent),
        "honest_digits_c": nd,
    }
    json.dump(out, open(OUTPUT, "w"), indent=1)

    if passed:
        print("\n  GATE PASSED.  The pipeline reproduces the known constant.")
        return 0

    print("\n  *** GATE FAILED -- HALT ***")
    print("  The literature is not the suspect.  Diagnosis checklist:")
    print("   1. normalisation of s (interval [-1,1] with kernel sin(s(x-y))/(pi(x-y))")
    print("      versus interval (-s,s) with kernel sin(u-v)/(pi(u-v)) -- these agree,")
    print("      but a factor-of-2 convention in s shifts c by a multiple of log 2;")
    print("   2. b should come out as -1/4; if it is -1/2 the log term is misassigned;")
    print("   3. node count too small at the largest s (check convergence.json);")
    print("   4. fit window includes s too small for the asymptotic regime;")
    print("   5. even-only model imposed where odd terms are actually present.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
