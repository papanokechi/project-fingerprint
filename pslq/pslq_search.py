#!/usr/bin/env python3
"""PSLQ integer-relation harness (Pillar B, local-only).

Output class is CONJECTURED, never PROVEN: a relation PSLQ returns is a
high-precision numerical coincidence until separately proven. This harness's
job is to (a) run mpmath.pslq on a named constant basis at a stated precision,
and (b) REFUSE to call a returned coefficient vector a "candidate" unless the
effective precision of the run clears the Bailey precision floor by a margin.

Bailey precision-floor rule (enforced here):
    To trust a relation whose coefficients are bounded by `maxcoeff` among an
    n-entry basis, the constants must be computed (and the relation validated)
    to at least n * log10(maxcoeff) decimal digits, plus a safety margin. A
    relation found with fewer EFFECTIVE digits than this floor is a precision
    artifact (e.g. 22/7 for pi), not a finding.

Effective precision of a run is min(working dps, digits implied by tol),
because a loose tol caps how many digits a returned relation is validated to,
regardless of how high mp.dps is set.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence

import mpmath
from mpmath import mp


DEFAULT_MARGIN_DIGITS = 10


# --------------------------------------------------------------------------
# Named constants. Each entry is a (name, nullary-callable) pair; the callable
# is evaluated at the CURRENT mp working precision so every constant is
# recomputed to the run's dps.
# --------------------------------------------------------------------------
def _r1_pcf(N: Optional[int] = None):
    """R1 = limit of the degree-(4,2) PCF (a_n=n^4-n^2-n-1, b_n=-n^2+n-1),
    evaluated at the CURRENT mp working precision. Family located in
    papanokechi/siarc-relay-bridge (T2A-R1-IDENTIFY); see pslq/constants/.

    Convergence is ~0.17 decimal digits/iteration, so the iteration count is
    scaled to the working precision (with margin) unless N is given explicitly.
    """
    if N is None:
        N = int(mp.dps * 7) + 300  # >= dps digits of accuracy, comfortable margin
    a4, a3, a2, a1, a0 = 1, 0, -1, -1, -1
    b2, b1, b0 = -1, 1, -1
    b_at_0 = mpmath.mpf(b0)
    b_at_1 = mpmath.mpf(b2 + b1 + b0)
    a_at_1 = mpmath.mpf(a4 + a3 + a2 + a1 + a0)
    P_prev2, P_prev1 = b_at_0, b_at_1 * b_at_0 + a_at_1
    Q_prev2, Q_prev1 = mpmath.mpf(1), b_at_1
    K = None
    for n in range(2, N + 1):
        an = a4 * n**4 + a3 * n**3 + a2 * n**2 + a1 * n + a0
        bn = b2 * n**2 + b1 * n + b0
        P_curr = bn * P_prev1 + an * P_prev2
        Q_curr = bn * Q_prev1 + an * Q_prev2
        K = P_curr / Q_curr
        if n % 16 == 0:
            mag = max(abs(P_curr), abs(Q_curr), mpmath.mpf(1))
            P_curr /= mag; Q_curr /= mag
            P_prev1 /= mag; Q_prev1 /= mag
        P_prev2, P_prev1 = P_prev1, P_curr
        Q_prev2, Q_prev1 = Q_prev1, Q_curr
    return K


def constant(name: str) -> "NamedConstant":
    table = {
        "pi": lambda: +mpmath.pi,
        "e": lambda: +mpmath.e,
        "ln2": lambda: mpmath.log(2),
        "log2": lambda: mpmath.log(2),
        "ln3": lambda: mpmath.log(3),
        "pi_ln2": lambda: mpmath.pi * mpmath.log(2),
        "gamma": lambda: +mpmath.euler,
        "catalan": lambda: +mpmath.catalan,
        "zeta2": lambda: mpmath.zeta(2),
        "zeta3": lambda: mpmath.zeta(3),
        "zeta5": lambda: mpmath.zeta(5),
        "pi2": lambda: mpmath.pi ** 2,
        "phi": lambda: +mpmath.phi,
        "one": lambda: mpmath.mpf(1),
        "neg_one": lambda: mpmath.mpf(-1),
        "R1": _r1_pcf,
    }
    if name.startswith("sqrt"):
        k = int(name[4:])
        return NamedConstant(name, (lambda k=k: mpmath.sqrt(k)))
    if name.startswith("atan1over"):
        # atan1over239 -> arctan(1/239)
        k = int(name[len("atan1over"):])
        return NamedConstant(name, (lambda k=k: mpmath.atan(mpmath.mpf(1) / k)))
    if name not in table:
        raise KeyError(f"unknown constant: {name!r}")
    return NamedConstant(name, table[name])


@dataclass
class NamedConstant:
    name: str
    fn: Callable[[], "mpmath.mpf"]


def make_basis(names: Sequence[str]) -> List[NamedConstant]:
    return [constant(n) if isinstance(n, str) else n for n in names]


# --------------------------------------------------------------------------
# Precision accounting
# --------------------------------------------------------------------------
def bailey_floor(n_entries: int, maxcoeff: int) -> float:
    """n * log10(maxcoeff) decimal digits."""
    return n_entries * math.log10(maxcoeff)


def effective_digits(dps: int, tol: Optional[object]) -> float:
    """Digits to which a relation is actually validated in this run.

    mpmath's default tol is 3/4 of the working precision. An explicitly
    supplied tol caps the validated precision at -log10(tol) digits, which is
    the whole point of the 22/7 false positive (loose tol -> few digits).
    """
    if tol is None:
        return 0.75 * dps
    tol_f = float(tol)
    if tol_f <= 0:
        return float(dps)
    return min(float(dps), -math.log10(tol_f))


@dataclass
class PslqResult:
    basis_names: List[str]
    n_entries: int
    dps: int
    tol: Optional[object]
    maxcoeff: int
    maxsteps: int
    margin_digits: int
    coeffs: Optional[List[int]]
    l_index: Optional[int] = None
    floor: float = field(init=False)
    eff_digits: float = field(init=False)
    clears_floor: bool = field(init=False)
    passes_l_filter: bool = field(init=False)
    is_candidate: bool = field(init=False)

    def __post_init__(self) -> None:
        self.floor = bailey_floor(self.n_entries, self.maxcoeff)
        self.eff_digits = effective_digits(self.dps, self.tol)
        self.clears_floor = self.eff_digits >= self.floor + self.margin_digits
        # Phantom-trap (L-coefficient) filter. When an l_index is given, the
        # entry at that position is the target limit L; a relation whose
        # coefficient on L is zero is satisfied by ANY value of L and signals
        # only a linear dependence WITHIN the rest of the basis (e.g. the
        # zeta(2)=pi^2/6 or 2*phi=sqrt5+1 traps). Such a relation is a PHANTOM,
        # not an identification of L, and must be rejected. When l_index is None
        # the filter is inactive (passes by definition).
        if self.l_index is None or not self.coeffs:
            self.passes_l_filter = True
        else:
            self.passes_l_filter = int(self.coeffs[self.l_index]) != 0
        # A coefficient vector is a CANDIDATE only if PSLQ returned something,
        # the run's effective precision clears the Bailey floor + margin, AND
        # (when an L target is named) it passes the phantom L-filter.
        self.is_candidate = (
            bool(self.coeffs) and self.clears_floor and self.passes_l_filter
        )

    def report(self) -> str:
        lines = [
            f"basis        : {self.basis_names}",
            f"n_entries    : {self.n_entries}",
            f"dps          : {self.dps}",
            f"tol          : {self.tol}",
            f"maxcoeff     : {self.maxcoeff}",
            f"maxsteps     : {self.maxsteps}",
            f"pslq coeffs  : {self.coeffs}",
            f"bailey floor : {self.floor:.3f} digits (n*log10(maxcoeff))",
            f"eff. digits  : {self.eff_digits:.3f} (min(dps, -log10(tol)))",
            f"margin req.  : +{self.margin_digits} digits",
            f"clears floor : {self.clears_floor}",
            f"L index      : {self.l_index}",
            f"L-filter     : "
            + (
                "INACTIVE (no L target named)"
                if self.l_index is None
                else (
                    f"PASS (coeff on L = {self.coeffs[self.l_index]} != 0)"
                    if (self.coeffs and self.passes_l_filter)
                    else (
                        "REJECT (coeff on L = 0 -> PHANTOM)"
                        if self.coeffs
                        else "n/a (no relation)"
                    )
                )
            ),
            f"-> verdict   : "
            + (
                "CANDIDATE (CONJECTURED; re-verify at higher precision)"
                if self.is_candidate
                else (
                    "NULL (no relation within tol/maxcoeff) -- successful null"
                    if not self.coeffs
                    else (
                        "REJECTED -- phantom (L-coefficient is zero)"
                        if not self.passes_l_filter
                        else "REJECTED -- below precision floor; precision artifact"
                    )
                )
            ),
        ]
        return "\n".join(lines)


def run_pslq(
    basis_names: Sequence[str],
    dps: int = 100,
    tol: Optional[object] = None,
    maxcoeff: int = 1000,
    maxsteps: int = 100,
    margin_digits: int = DEFAULT_MARGIN_DIGITS,
    l_index: Optional[int] = None,
) -> PslqResult:
    """Compute the basis to `dps` digits and run mpmath.pslq on it.

    `l_index`, when given, marks which basis entry is the target limit L; a
    returned relation with a zero coefficient on that entry is treated as a
    phantom (see PslqResult).
    """
    basis = make_basis(basis_names)
    saved_dps = mp.dps
    try:
        mp.dps = dps
        vec = [c.fn() for c in basis]
        coeffs = mpmath.pslq(vec, tol=tol, maxcoeff=maxcoeff, maxsteps=maxsteps)
    finally:
        mp.dps = saved_dps
    return PslqResult(
        basis_names=[c.name for c in basis],
        n_entries=len(basis),
        dps=dps,
        tol=tol,
        maxcoeff=maxcoeff,
        maxsteps=maxsteps,
        margin_digits=margin_digits,
        coeffs=list(coeffs) if coeffs else None,
        l_index=l_index,
    )


# --------------------------------------------------------------------------
# Self-test (shakedown gate): accept a true relation, reject a false positive.
# --------------------------------------------------------------------------
def self_test(verbose: bool = True) -> bool:
    ok = True

    # (1) TRUE relation: 2*sqrt(2) - sqrt(8) = 0 over [sqrt(2)..sqrt(8)].
    true_basis = [f"sqrt{n}" for n in range(2, 9)]
    r_true = run_pslq(true_basis, dps=100, tol=None, maxcoeff=1000)
    expected = [2, 0, 0, 0, 0, 0, -1]
    accepted_true = r_true.coeffs == expected and r_true.is_candidate
    ok = ok and accepted_true

    # (2) FALSE positive: pslq([-1, pi], tol=0.01) -> [22, 7], must be REJECTED.
    r_false = run_pslq(["neg_one", "pi"], dps=50, tol=mpmath.mpf("0.01"), maxcoeff=1000)
    got_2207 = r_false.coeffs == [22, 7]
    rejected_false = got_2207 and (not r_false.is_candidate)
    ok = ok and rejected_false

    if verbose:
        print("=== SELF-TEST 1: TRUE relation 2*sqrt(2) = sqrt(8) ===")
        print(r_true.report())
        print(f"expected coeffs : {expected}")
        print(f"ACCEPTED as candidate: {accepted_true}")
        print()
        print("=== SELF-TEST 2: FALSE positive pi ~ 22/7 at tol=0.01 ===")
        print(r_false.report())
        print(f"returned [22,7] : {got_2207}")
        print(f"REJECTED (not a candidate): {rejected_false}")
        print()
        print(f"SELFTEST {'PASS' if ok else 'FAIL'}")

    return ok


def phantom_test(verbose: bool = True) -> bool:
    """POSITIVE L-filter test: a basis containing a known linear dependence
    among the NON-L entries must surface a phantom relation (L-coefficient = 0)
    that the L-filter REJECTS.

    Basis: [R1, pi, zeta2, pi2, log2] with l_index=0 (R1 is the target L).
    zeta2 = pi^2/6 is an exact dependence among entries 2 and 3, so PSLQ returns
    a relation with zero coefficient on R1 -- the documented zeta(2)=pi^2/6
    phantom. The filter must mark it REJECTED (not a candidate).
    """
    ok = True
    basis = ["R1", "pi", "zeta2", "pi2", "log2"]
    r = run_pslq(basis, dps=120, tol=None, maxcoeff=1000, l_index=0)
    returned_relation = bool(r.coeffs)
    l_coeff_zero = returned_relation and int(r.coeffs[0]) == 0
    rejected = returned_relation and (not r.is_candidate) and (not r.passes_l_filter)
    ok = returned_relation and l_coeff_zero and rejected

    if verbose:
        print("=== L-FILTER POSITIVE TEST: zeta(2)=pi^2/6 phantom ===")
        print(r.report())
        print(f"relation returned     : {returned_relation}")
        print(f"L (R1) coefficient = 0: {l_coeff_zero}")
        print(f"REJECTED as phantom   : {rejected}")
        print()
        print(f"PHANTOMTEST {'PASS' if ok else 'FAIL'}")

    return ok


def main() -> None:
    parser = argparse.ArgumentParser(description="PSLQ integer-relation harness (local-only).")
    parser.add_argument("--selftest", action="store_true", help="run the shakedown self-test and exit")
    parser.add_argument("--phantomtest", action="store_true", help="run the L-filter phantom-rejection test and exit")
    parser.add_argument("--basis", nargs="+", help="named constants to test (e.g. pi e ln2)")
    parser.add_argument("--dps", type=int, default=100)
    parser.add_argument("--tol", type=str, default=None, help="tolerance (default: mpmath 3/4 precision)")
    parser.add_argument("--maxcoeff", type=int, default=1000)
    parser.add_argument("--maxsteps", type=int, default=100)
    parser.add_argument("--margin", type=int, default=DEFAULT_MARGIN_DIGITS)
    parser.add_argument("--l-index", type=int, default=None, dest="l_index",
                        help="index of the target limit L in --basis; relations with a zero L-coefficient are rejected as phantoms")
    args = parser.parse_args()

    if args.selftest:
        ok = self_test(verbose=True)
        raise SystemExit(0 if ok else 1)

    if args.phantomtest:
        ok = phantom_test(verbose=True)
        raise SystemExit(0 if ok else 1)

    if args.basis:
        tol = mpmath.mpf(args.tol) if args.tol is not None else None
        res = run_pslq(
            args.basis,
            dps=args.dps,
            tol=tol,
            maxcoeff=args.maxcoeff,
            maxsteps=args.maxsteps,
            margin_digits=args.margin,
            l_index=args.l_index,
        )
        print(res.report())
        return

    parser.print_help()


if __name__ == "__main__":
    main()
