<#
.SYNOPSIS
  Windows equivalent of the Makefile targets (no `make` on this machine).

.EXAMPLE
  .\verify.ps1 test          structural smoke tests only          (~1 min)
  .\verify.ps1 audit         mechanical guard audit (L-049/L-055)  (~5 sec)
  .\verify.ps1 mutate        mutation test: are the checks live?  (~3 min)
  .\verify.ps1 trans         derive A, theta, beta from the ODE   (~2 min)
  .\verify.ps1 ode           discover + verify the sigma ODE      (~20 min)
  .\verify.ps1 tail          recursion, fit-free c, b=8 PSLQ      (~5 min)
  .\verify.ps1 predict       M=600 recursion, s=200/250, 0.869*s law (~20 min)
  .\verify.ps1 analysis      re-derive c, gate, PSLQ from grid    (~20 min)
  .\verify.ps1 verify-fast   smoke tests + analysis + tail        (~25 min)
  .\verify.ps1 kernel        0.1 convergence tables               (~15 min)
  .\verify.ps1 data          rebuild the certified grid           (HOURS)
  .\verify.ps1 verify        everything, from nothing but mpmath  (HOURS)

  `verify` re-derives every claim tagged VERIFIED in ledger.md starting from
  nothing but mpmath: it does not read any stored artifact.  It regenerates
  and overwrites out/certified_data.json.

  `ode` re-runs the L-036 discovery from scratch -- it does NOT take the
  discovered relation as given, it re-finds it by nullspace search and then
  re-confirms it out of sample.  `tail` re-derives the L-037 coefficients by
  two independent implementations, re-extracts c without any fit (L-038), and
  re-runs the b=8 PSLQ vetting (L-039).

  `verify-fast` re-derives everything downstream of the certified grid.  It
  therefore re-derives c, its error budget, the calibration gate and the PSLQ
  verdicts, but takes the grid as given.

  There is deliberately no clean target: session rule, no file deletion
  without operator approval.  Superseded grids are snapshotted, never removed.
#>
param([ValidateSet("test", "audit", "mutate", "trans", "kernel", "data", "analysis", "ode", "tail", "predict",
                   "verify", "verify-fast")]
      [string]$Target = "verify")

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path out)) { New-Item -ItemType Directory out | Out-Null }

function Step([string]$script) {
    Write-Host ""
    Write-Host ("=" * 78) -ForegroundColor Cyan
    Write-Host "RUN  python $script" -ForegroundColor Cyan
    Write-Host ("=" * 78) -ForegroundColor Cyan
    & python $script.Split(" ")[0] @($script.Split(" ") | Select-Object -Skip 1)
    if ($LASTEXITCODE -ne 0) {
        throw "$script exited with code $LASTEXITCODE (gate failure halts the pipeline by design)"
    }
}

switch ($Target) {
    "test"        { Step test_smoke.py }
    "audit"       { Step assertion_audit.py }
    "mutate"      { Step mutation_test.py }
    "trans"       { Step trans_series.py }
    "kernel"      { Step verify_kernel.py }
    "data"        { Step build_grid.py }
    "ode"         { Step "sigma_ode.py 120 4 70"; Step "sigma_ode_verify.py 80" }
    "tail"        { Step "sigma_recursion.py 60"
                    Step "sigma_recursion_fast.py 400 --check"
                    Step "sigma_recursion_check.py"
                    Step "direct_c.py out/sigma_recursion_fast.json"
                    Step run_pslq_b8.py }
    "predict"     { Step "sigma_recursion_fast.py 600"
                    Step "highs_points.py 200 250"
                    Step prediction_test.py
                    Step excess_structure.py }
    "analysis"    { Step fit_constant.py; Step gate.py; Step run_pslq.py }
    "verify-fast" { Step assertion_audit.py
                    Step test_smoke.py
                    Step fit_constant.py; Step gate.py; Step run_pslq.py
                    Step "sigma_recursion.py 60"
                    Step "sigma_recursion_fast.py 400 --check"
                    Step "sigma_recursion_check.py"
                    Step "direct_c.py out/sigma_recursion_fast.json"
                    Step run_pslq_b8.py
                    Step trans_series.py }
    "verify"      { Step assertion_audit.py
                    Step test_smoke.py
                    Step verify_kernel.py
                    Step build_grid.py
                    Step fit_constant.py; Step gate.py; Step run_pslq.py
                    Step "sigma_ode.py 120 4 70"; Step "sigma_ode_verify.py 80"
                    Step "sigma_recursion.py 60"
                    Step "sigma_recursion_fast.py 400 --check"
                    Step "sigma_recursion_check.py"
                    Step "direct_c.py out/sigma_recursion_fast.json"
                    Step run_pslq_b8.py
                    Step sigma_sign_trap.py
                    Step excess_structure.py
                    Step trans_series.py
                    Step mutation_test.py }
}

Write-Host ""
Write-Host "target '$Target' completed" -ForegroundColor Green
