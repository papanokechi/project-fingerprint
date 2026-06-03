#!/usr/bin/env python3
"""Independent evaluator for the n-circle packing task (unit square, maximize sum of radii).

This file is DELIBERATELY SEPARATE from any program OpenEvolve evolves. Its sole job
is to take a saved configuration (centers + radii) and decide, by first principles,
whether the configuration is VALID and what its sum of radii is. It must never be
edited to make a particular configuration pass; a failing configuration is a finding.

Validity checks (all must hold):
  1. Containment: every circle lies fully inside the unit square, i.e.
     x - r >= -tol, x + r <= 1 + tol, y - r >= -tol, y + r <= 1 + tol.
  2. Non-overlap: for all i < j, dist(c_i, c_j) >= r_i + r_j - tol.
  3. Non-negativity: every radius r_i >= -tol.

The default tolerance is 1e-9 (stated explicitly, per the task spec).

Usage:
  python independent_evaluator.py <config.json> [--n 26] [--tol 1e-9]
  python independent_evaluator.py --selftest

Config file formats accepted (JSON):
  A) {"centers": [[x0, y0], ...], "radii": [r0, r1, ...]}
  B) {"x": [...], "y": [...], "radii": [...]}
  C) {"circles": [[x0, y0, r0], [x1, y1, r1], ...]}

Exit code is 0 if the configuration is valid, 1 if invalid or on error. The sum of
radii is always reported (even for invalid configs) so a near-miss is visible.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import List, Tuple

DEFAULT_TOL = 1e-9


def _load_config(path: str) -> Tuple[List[Tuple[float, float]], List[float]]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return _parse_config(data)


def _parse_config(data: dict) -> Tuple[List[Tuple[float, float]], List[float]]:
    if "circles" in data:
        circles = data["circles"]
        centers = [(float(c[0]), float(c[1])) for c in circles]
        radii = [float(c[2]) for c in circles]
        return centers, radii
    if "centers" in data and "radii" in data:
        centers = [(float(c[0]), float(c[1])) for c in data["centers"]]
        radii = [float(r) for r in data["radii"]]
        return centers, radii
    if "x" in data and "y" in data and "radii" in data:
        xs, ys, radii = data["x"], data["y"], data["radii"]
        centers = [(float(x), float(y)) for x, y in zip(xs, ys)]
        return centers, [float(r) for r in radii]
    raise ValueError(
        "Unrecognized config schema; expected 'circles', or 'centers'+'radii', "
        "or 'x'+'y'+'radii'."
    )


def evaluate(
    centers: List[Tuple[float, float]],
    radii: List[float],
    n_expected: int | None = None,
    tol: float = DEFAULT_TOL,
) -> dict:
    """Return a structured report of validity and sum of radii.

    The report dict contains: valid (bool), sum_radii (float), n (int),
    violations (list of human-readable strings), and per-check booleans.
    """
    violations: List[str] = []

    if len(centers) != len(radii):
        violations.append(
            f"count mismatch: {len(centers)} centers vs {len(radii)} radii"
        )
    n = len(radii)

    if n_expected is not None and n != n_expected:
        violations.append(f"expected n={n_expected} circles, got n={n}")

    # Check 3: non-negativity.
    negative_ok = True
    for i, r in enumerate(radii):
        if r < -tol:
            negative_ok = False
            violations.append(f"radius[{i}] = {r!r} < 0 (tol {tol})")

    # Check 1: containment within the unit square [0, 1] x [0, 1].
    containment_ok = True
    for i, ((x, y), r) in enumerate(zip(centers, radii)):
        if x - r < -tol:
            containment_ok = False
            violations.append(f"circle[{i}] crosses left edge: x-r = {x - r!r}")
        if x + r > 1 + tol:
            containment_ok = False
            violations.append(f"circle[{i}] crosses right edge: x+r = {x + r!r}")
        if y - r < -tol:
            containment_ok = False
            violations.append(f"circle[{i}] crosses bottom edge: y-r = {y - r!r}")
        if y + r > 1 + tol:
            containment_ok = False
            violations.append(f"circle[{i}] crosses top edge: y+r = {y + r!r}")

    # Check 2: pairwise non-overlap.
    overlap_ok = True
    for i in range(n):
        xi, yi = centers[i]
        ri = radii[i]
        for j in range(i + 1, n):
            xj, yj = centers[j]
            rj = radii[j]
            dist = math.hypot(xi - xj, yi - yj)
            if dist < ri + rj - tol:
                overlap_ok = False
                violations.append(
                    f"circles[{i},{j}] overlap: dist={dist!r} < "
                    f"r_i+r_j={ri + rj!r} (tol {tol})"
                )

    count_ok = (len(centers) == len(radii)) and (
        n_expected is None or n == n_expected
    )
    valid = bool(
        count_ok and negative_ok and containment_ok and overlap_ok
    )

    return {
        "valid": valid,
        "sum_radii": float(sum(radii)),
        "n": n,
        "tol": tol,
        "checks": {
            "count_ok": count_ok,
            "non_negative_ok": negative_ok,
            "containment_ok": containment_ok,
            "non_overlap_ok": overlap_ok,
        },
        "violations": violations,
    }


def _print_report(report: dict) -> None:
    print(json.dumps(report, indent=2, sort_keys=True))


def _selftest() -> int:
    """Self-tests using configurations whose validity is known by construction.

    These exercise the evaluator itself (NOT the search). They are not a circle-
    packing result and make no claim about the n=26 optimum.
    """
    failures = 0

    # (1) A trivially valid config: 4 disjoint circles of radius 0.25 centered in
    #     the four quadrant centers. They are mutually tangent-or-separated and
    #     fully inside the square.
    centers = [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]
    radii = [0.25, 0.25, 0.25, 0.25]
    rep = evaluate(centers, radii, n_expected=4)
    if not rep["valid"]:
        failures += 1
        print("SELFTEST FAIL: expected valid 4-circle config to pass", rep["violations"])
    if abs(rep["sum_radii"] - 1.0) > 1e-12:
        failures += 1
        print("SELFTEST FAIL: expected sum_radii == 1.0, got", rep["sum_radii"])

    # (2) Overlap must be caught: two unit-quadrant circles pushed together.
    rep = evaluate([(0.4, 0.5), (0.6, 0.5)], [0.25, 0.25], n_expected=2)
    if rep["valid"] or rep["checks"]["non_overlap_ok"]:
        failures += 1
        print("SELFTEST FAIL: expected overlap to be detected")

    # (3) Containment must be caught: a circle poking out the right edge.
    rep = evaluate([(0.95, 0.5)], [0.2], n_expected=1)
    if rep["valid"] or rep["checks"]["containment_ok"]:
        failures += 1
        print("SELFTEST FAIL: expected containment violation to be detected")

    # (4) Negative radius must be caught.
    rep = evaluate([(0.5, 0.5)], [-0.1], n_expected=1)
    if rep["valid"] or rep["checks"]["non_negative_ok"]:
        failures += 1
        print("SELFTEST FAIL: expected negative radius to be detected")

    # (5) Tangent circles (dist exactly r_i+r_j) must be accepted within tol.
    rep = evaluate([(0.25, 0.5), (0.75, 0.5)], [0.25, 0.25], n_expected=2)
    if not rep["checks"]["non_overlap_ok"]:
        failures += 1
        print("SELFTEST FAIL: tangent circles should be accepted")

    if failures == 0:
        print("SELFTEST PASS: all evaluator self-tests passed.")
        return 0
    print(f"SELFTEST: {failures} failure(s).")
    return 1


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", nargs="?", help="Path to a JSON config file.")
    parser.add_argument("--n", type=int, default=26, help="Expected number of circles.")
    parser.add_argument("--tol", type=float, default=DEFAULT_TOL, help="Numeric tolerance.")
    parser.add_argument("--selftest", action="store_true", help="Run evaluator self-tests.")
    args = parser.parse_args(argv)

    if args.selftest:
        return _selftest()

    if not args.config:
        parser.error("a config path is required unless --selftest is given")

    try:
        centers, radii = _load_config(args.config)
    except Exception as exc:  # noqa: BLE001 - report any load/parse failure plainly
        print(f"ERROR loading config: {exc}", file=sys.stderr)
        return 1

    report = evaluate(centers, radii, n_expected=args.n, tol=args.tol)
    _print_report(report)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
