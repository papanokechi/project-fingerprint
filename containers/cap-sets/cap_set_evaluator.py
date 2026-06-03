#!/usr/bin/env python3
"""Independent evaluator for cap sets in AG(n,3) = (Z/3Z)^n  (Task 04).

A *cap* is a set of points in (Z/3Z)^n with no three collinear. Over Z/3Z three
DISTINCT points a, b, c are collinear iff  a + b + c == 0 (mod 3) componentwise.
Equivalently, for any two distinct points a, b the unique third point completing
the line is  c = (-a - b) mod 3 ; the set is a cap iff that c is never also in the
set. (For a != b, c is automatically distinct from both a and b.)

This program is INDEPENDENT of any evolved program and of OpenEvolve's own scoring
evaluator. It re-checks a saved cap standalone so a result is verifiable without
re-running the search. It must never be edited to make a configuration pass.

Usage:
  python cap_set_evaluator.py CONFIG.json [--n N]
  python cap_set_evaluator.py --selftest

CONFIG.json schema:
  {"n": <int>, "points": [[c0, c1, ...], ...]}   # each entry in {0,1,2}, length n

Exit code: 0 if the points form a valid cap, 1 otherwise (or on input error).
"""
import argparse
import json


def third_point(a, b):
    """Unique point completing the line through distinct a, b in (Z/3Z)^n."""
    return tuple((-a[k] - b[k]) % 3 for k in range(len(a)))


def evaluate_cap(n, points):
    """Validate points and check the cap property.

    Returns a dict: is_valid_cap (bool), size (int), n (int), and on failure a
    'reason' plus (for a collinearity failure) the first violating triple.
    """
    if not isinstance(points, list) or len(points) == 0:
        return {"is_valid_cap": False, "size": 0, "n": n,
                "reason": "points must be a non-empty list"}

    norm = []
    for idx, p in enumerate(points):
        if not isinstance(p, (list, tuple)) or len(p) != n:
            return {"is_valid_cap": False, "size": len(points), "n": n,
                    "reason": f"point {idx} has wrong length (expected {n}): {p}"}
        coords = []
        for c in p:
            if c not in (0, 1, 2):
                return {"is_valid_cap": False, "size": len(points), "n": n,
                        "reason": f"point {idx} has coordinate not in {{0,1,2}}: {p}"}
            coords.append(int(c))
        norm.append(tuple(coords))

    pointset = set(norm)
    if len(pointset) != len(norm):
        return {"is_valid_cap": False, "size": len(norm), "n": n,
                "reason": "duplicate points present (a cap is a set of distinct points)"}

    pl = list(pointset)
    for i in range(len(pl)):
        a = pl[i]
        for j in range(i + 1, len(pl)):
            b = pl[j]
            c = third_point(a, b)
            if c in pointset and c != a and c != b:
                triple = sorted([a, b, c])
                return {"is_valid_cap": False, "size": len(pointset), "n": n,
                        "reason": "three collinear points (a+b+c == 0 mod 3)",
                        "first_violating_triple": [list(t) for t in triple]}

    return {"is_valid_cap": True, "size": len(pointset), "n": n,
            "reason": "no three collinear; all points distinct and in {0,1,2}^n"}


# --- known caps used by the self-test (extracted by exhaustive backtracking) ---
CAP9_AG3 = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0),
            (1, 0, 1), (1, 1, 2), (1, 2, 2), (2, 1, 2)]              # max cap, n=3
CAP4_AG2 = [(0, 0), (1, 0), (0, 1), (1, 1)]                         # max cap, n=2
CAP20_AG4 = [(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1),
             (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
             (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 2), (1, 0, 2, 2),
             (1, 1, 0, 2), (1, 2, 0, 2), (2, 0, 1, 2), (2, 1, 0, 2),
             (2, 1, 1, 0), (2, 1, 1, 1), (2, 1, 2, 2), (2, 2, 1, 2)]  # max cap, n=4
AG2_FULL = [(x, y) for x in range(3) for y in range(3)]            # all 9 points


def selftest():
    cases = []

    # 1. known 9-cap in AG(3,3) -> valid, size 9
    r = evaluate_cap(3, [list(p) for p in CAP9_AG3])
    cases.append(("known 9-cap AG(3,3) -> valid size 9",
                  r["is_valid_cap"] is True and r["size"] == 9, r))

    # 2. that 9-cap plus a point completing a line -> INVALID, names the triple.
    #    9 is the proven maximum for n=3, so ANY external point creates a line.
    extra = (2, 2, 2)
    assert extra not in set(CAP9_AG3)
    r = evaluate_cap(3, [list(p) for p in CAP9_AG3] + [list(extra)])
    cases.append(("9-cap + external point -> INVALID + triple",
                  r["is_valid_cap"] is False and "first_violating_triple" in r, r))

    # 3. full AG(2,3) (all 9 points) -> INVALID (contains lines)
    r = evaluate_cap(2, [list(p) for p in AG2_FULL])
    cases.append(("full AG(2,3) all 9 points -> INVALID",
                  r["is_valid_cap"] is False, r))

    # 4. known 4-cap in AG(2,3) -> valid, size 4
    r = evaluate_cap(2, [list(p) for p in CAP4_AG2])
    cases.append(("known 4-cap AG(2,3) -> valid size 4",
                  r["is_valid_cap"] is True and r["size"] == 4, r))

    # bonus: known 20-cap in AG(4,3) -> valid, size 20 (confirms evaluator accepts
    # a true n=4 maximum; complements the rejection cases above)
    r = evaluate_cap(4, [list(p) for p in CAP20_AG4])
    cases.append(("known 20-cap AG(4,3) -> valid size 20 (bonus)",
                  r["is_valid_cap"] is True and r["size"] == 20, r))

    all_ok = True
    for name, ok, detail in cases:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        extra = ""
        if "first_violating_triple" in detail:
            extra = f"  triple={detail['first_violating_triple']}"
        print(f"  [{status}] {name} (got is_valid_cap={detail['is_valid_cap']}, "
              f"size={detail['size']}){extra}")
    print(f"SELFTEST {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


def main():
    ap = argparse.ArgumentParser(description="Independent cap-set evaluator for AG(n,3).")
    ap.add_argument("config", nargs="?", help="JSON file with {n, points}")
    ap.add_argument("--n", type=int, default=None, help="assert this dimension n")
    ap.add_argument("--selftest", action="store_true", help="run built-in self-tests")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.config:
        ap.error("CONFIG.json required unless --selftest")

    with open(args.config, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    points = data.get("points")
    n = args.n if args.n is not None else data.get("n")
    if n is None:
        print(json.dumps({"is_valid_cap": False, "reason": "n not provided"}))
        return 1
    if args.n is not None and data.get("n") is not None and int(data["n"]) != int(args.n):
        print(json.dumps({"is_valid_cap": False, "n": int(args.n),
                          "reason": f"dimension mismatch: file n={data['n']} vs --n {args.n}"}))
        return 1

    result = evaluate_cap(int(n), points)
    print(json.dumps(result, indent=2))
    return 0 if result["is_valid_cap"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
