# Phase 0 pipeline: sine-kernel Fredholm determinant asymptotics.
#
#   make verify        full rebuild from nothing but mpmath (HOURS): re-derives
#                      every claim tagged VERIFIED in ledger.md.  Reads no
#                      stored artifact.
#   make verify-fast   everything downstream of the certified grid (~20 min):
#                      re-derives c, its error budget, the calibration gate and
#                      the PSLQ verdicts, taking the grid as given.
#   make kernel        0.1 convergence tables only (~15 min).
#   make data          rebuild the certified grid only (HOURS).
#   make test          structural smoke tests only (~1 min).
#
# There is deliberately NO clean target.  Session rule: no file deletion
# without operator approval.  Superseded grids are snapshotted next to the
# working file (out/certified_data.*.json), never removed, so that a later
# analysis can show the constant did not move when the data got better.

PY := python

.PHONY: verify verify-fast test kernel data analysis

verify: test kernel data analysis

verify-fast: test analysis

test:
	$(PY) test_smoke.py

# 0.1 convergence tables in BOTH node count and mp.dps, plus the structural
# cross-checks (GL exactness, parity factorisation, backend agreement).
kernel:
	$(PY) verify_kernel.py

# The certified production grid: every point certified by node doubling AND a
# +20-digit precision increase.
data:
	$(PY) build_grid.py

# 0.2 extraction with the honest error budget, 0.3 calibration gate,
# 0.4 PSLQ harness with adversarial null controls.
# The gate exits non-zero on failure, which stops make -- by design.
analysis:
	$(PY) fit_constant.py
	$(PY) gate.py
	$(PY) run_pslq.py
