"""Build the full certified grid from nothing.  This is the `data` target.

Everything the analysis needs is regenerated here: no artifact from a previous
session is required, and no value is read from anywhere except a fresh
evaluation of the determinant.  The grid layout below is the revision-3 layout
recorded in ledger.md (L-015).

Layout and why it is shaped this way (measured, see L-013):
  * s in [30, 45] step 0.25   -- cheap points, each buying one correction order
  * s in [45, 89] step 2      -- the range extension that bought the most
                                 digits per point in revision 1
  * s in [91, 149] step 2     -- further range extension; the extrapolation to
                                 1/s^2 -> 0 is conditioning-limited, and
                                 raising s_max/s_min is what relieves it

Runtime is hours, not minutes.  `verify-fast` exists for the case where the
certified grid is already present and only the analysis needs re-deriving.
"""

from __future__ import annotations

import time

import extend_adaptive as EA

BLOCKS = [
    ("30", "45", "0.25"),
    ("45", "89", "2"),
    ("91", "149", "2"),
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
