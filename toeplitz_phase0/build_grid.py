"""Build the full certified grid from nothing.  This is the `data` target.

Everything the analysis needs is regenerated here: no artifact from a previous
session is required, and no value is read from anywhere except a fresh
evaluation of the determinant.  The grid layout below is the revision-3 layout
recorded in ledger.md (L-015).

Layout and why it is shaped this way (measured, see L-017):
  * s in [30, 45] step 0.25   -- 61 points
  * s in [45, 89] step 2      -- 22 further points
  * s in [91, 149] step 1     -- 59 further points

Total 142 points.  The controlling resource is the NUMBER of points, because
each one buys one more correction order K and the extraction is order-limited
rather than s_min-limited: refitting on s >= s_min for increasing s_min makes
the answer monotonically worse, since dropping low-s points destroys orders
faster than it improves per-order truncation (L-017).  The high-s blocks are
nonetheless placed at large s because that is where points are cheap relative
to the certified digits they yield, once the node count is chosen adaptively.

Runtime is hours, not minutes.  `verify-fast` exists for the case where the
certified grid is already present and only the analysis needs re-deriving.
"""

from __future__ import annotations

import time

import extend_adaptive as EA

BLOCKS = [
    ("30", "45", "0.25"),
    ("45", "89", "2"),
    ("91", "149", "1"),
]


def main():
    t0 = time.time()
    for s0, s1, ds in BLOCKS:
        print("\n" + "=" * 78)
        print(f"GRID BLOCK  s in [{s0}, {s1}] step {ds}")
        print("=" * 78, flush=True)
        EA.main(["build_grid.py", s0, s1, ds, "--refit"])
    print(f"\ngrid build complete in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
