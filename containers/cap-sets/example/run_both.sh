#!/usr/bin/env bash
# Run the cap-set shakedown for BOTH target dimensions sequentially (Task 04).
# Sequential, not parallel: a single CPU-bound Ollama model serializes requests, so
# concurrent dimensions would only contend. Each dimension writes to its own output
# subdir so the host can read both results.
set -euo pipefail

ITERS="${ITERS:-50}"

echo "########## DIMENSION n=3 (known max 9) ##########"
OUT=/work/output/n3 CAP_N=3 ITERS="$ITERS" bash /work/src/example/run_in_container.sh

echo "########## DIMENSION n=4 (known max 20) ##########"
OUT=/work/output/n4 CAP_N=4 ITERS="$ITERS" bash /work/src/example/run_in_container.sh

echo "########## BOTH DIMENSIONS DONE ##########"
