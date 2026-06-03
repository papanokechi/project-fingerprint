# EVOLVE-BLOCK-START
"""Constructor for a cap set in AG(n, 3) = (Z/3Z)^n.

A cap is a set of points with no three collinear. Over Z/3Z, three distinct
points a, b, c are collinear iff (a + b + c) == 0 (mod 3) componentwise, i.e. for
any two points a, b the forbidden third point is c = (-a - b) mod 3. The goal is
to construct as LARGE a cap as possible for the given dimension n.

Known maximal sizes (proven exact): n=1:2, n=2:4, n=3:9, n=4:20, n=5:45, n=6:112.

This seed uses a simple greedy scan in lexicographic order (a valid but typically
sub-maximal cap). Improve the construction to produce a larger valid cap.
"""
import itertools


def construct_cap(n):
    """Return a list of points (each a length-n tuple over {0,1,2}) forming a cap."""
    cap = []
    capset = set()
    for p in itertools.product(range(3), repeat=n):
        ok = True
        for q in cap:
            c = tuple((-p[k] - q[k]) % 3 for k in range(n))
            if c in capset:
                ok = False
                break
        if ok:
            cap.append(p)
            capset.add(p)
    return cap


# EVOLVE-BLOCK-END


# This part remains fixed (not evolved).
def run_cap_construction():
    """Entry point used by the evaluator. n is taken from the CAP_N env var."""
    import os

    n = int(os.environ.get("CAP_N", "3"))
    cap = construct_cap(n)
    return n, [list(p) for p in cap]


if __name__ == "__main__":
    n, pts = run_cap_construction()
    print(f"n={n}: constructed cap of size {len(pts)}")
