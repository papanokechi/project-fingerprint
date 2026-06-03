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
def constant(name: str) -> "NamedConstant":
    table = {
        "pi": lambda: +mpmath.pi,
        "e": lambda: +mpmath.e,
        "ln2": lambda: mpmath.log(2),
        "ln3": lambda: mpmath.log(3),
        "pi_ln2": lambda: mpmath.pi * mpmath.log(2),
        "gamma": lambda: +mpmath.euler,
        "catalan": lambda: +mpmath.catalan,
        "zeta2": lambda: mpmath.zeta(2),
        "zeta3": lambda: mpmath.zeta(3),
        "pi2": lambda: mpmath.pi ** 2,
        "phi": lambda: +mpmath.phi,
        "one": lambda: mpmath.mpf(1),
        "neg_one": lambda: mpmath.mpf(-1),
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
    floor: float = field(init=False)
    eff_digits: float = field(init=False)
    clears_floor: bool = field(init=False)
    is_candidate: bool = field(init=False)

    def __post_init__(self) -> None:
        self.floor = bailey_floor(self.n_entries, self.maxcoeff)
        self.eff_digits = effective_digits(self.dps, self.tol)
        self.clears_floor = self.eff_digits >= self.floor + self.margin_digits
        # A coefficient vector is a CANDIDATE only if PSLQ returned something
        # AND the run's effective precision clears the Bailey floor + margin.
        self.is_candidate = bool(self.coeffs) and self.clears_floor

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
            f"-> verdict   : "
            + (
                "CANDIDATE (CONJECTURED; re-verify at higher precision)"
                if self.is_candidate
                else (
                    "NULL (no relation within tol/maxcoeff) -- successful null"
                    if not self.coeffs
                    else "REJECTED -- below precision floor; precision artifact"
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
) -> PslqResult:
    """Compute the basis to `dps` digits and run mpmath.pslq on it."""
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


def main() -> None:
    parser = argparse.ArgumentParser(description="PSLQ integer-relation harness (local-only).")
    parser.add_argument("--selftest", action="store_true", help="run the shakedown self-test and exit")
    parser.add_argument("--basis", nargs="+", help="named constants to test (e.g. pi e ln2)")
    parser.add_argument("--dps", type=int, default=100)
    parser.add_argument("--tol", type=str, default=None, help="tolerance (default: mpmath 3/4 precision)")
    parser.add_argument("--maxcoeff", type=int, default=1000)
    parser.add_argument("--maxsteps", type=int, default=100)
    parser.add_argument("--margin", type=int, default=DEFAULT_MARGIN_DIGITS)
    args = parser.parse_args()

    if args.selftest:
        ok = self_test(verbose=True)
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
        )
        print(res.report())
        return

    parser.print_help()


if __name__ == "__main__":
    main()
