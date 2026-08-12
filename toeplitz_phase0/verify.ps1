<#
.SYNOPSIS
  Windows equivalent of the Makefile targets (no `make` on this machine).

.EXAMPLE
  .\verify.ps1 test          structural smoke tests only          (~1 min)
  .\verify.ps1 analysis      re-derive c, gate, PSLQ from grid    (~20 min)
  .\verify.ps1 verify-fast   smoke tests + analysis               (~20 min)
  .\verify.ps1 kernel        0.1 convergence tables               (~15 min)
  .\verify.ps1 data          rebuild the certified grid           (HOURS)
  .\verify.ps1 verify        everything, from nothing but mpmath  (HOURS)

  `verify` re-derives every claim tagged VERIFIED in ledger.md starting from
  nothing but mpmath: it does not read any stored artifact.  It regenerates
  and overwrites out/certified_data.json.

  `verify-fast` re-derives everything downstream of the certified grid.  It
  therefore re-derives c, its error budget, the calibration gate and the PSLQ
  verdicts, but takes the grid as given.

  There is deliberately no clean target: session rule, no file deletion
  without operator approval.  Superseded grids are snapshotted, never removed.
#>
param([ValidateSet("test", "kernel", "data", "analysis", "verify", "verify-fast")]
      [string]$Target = "verify")

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path out)) { New-Item -ItemType Directory out | Out-Null }

function Step([string]$script) {
    Write-Host ""
    Write-Host ("=" * 78) -ForegroundColor Cyan
    Write-Host "RUN  python $script" -ForegroundColor Cyan
    Write-Host ("=" * 78) -ForegroundColor Cyan
    & python $script
    if ($LASTEXITCODE -ne 0) {
        throw "$script exited with code $LASTEXITCODE (gate failure halts the pipeline by design)"
    }
}

switch ($Target) {
    "test"        { Step test_smoke.py }
    "kernel"      { Step verify_kernel.py }
    "data"        { Step build_grid.py }
    "analysis"    { Step fit_constant.py; Step gate.py; Step run_pslq.py }
    "verify-fast" { Step test_smoke.py
                    Step fit_constant.py; Step gate.py; Step run_pslq.py }
    "verify"      { Step test_smoke.py
                    Step verify_kernel.py
                    Step build_grid.py
                    Step fit_constant.py; Step gate.py; Step run_pslq.py }
}

Write-Host ""
Write-Host "target '$Target' completed" -ForegroundColor Green
