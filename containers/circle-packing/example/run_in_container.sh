#!/usr/bin/env bash
# In-container orchestration for the n=26 circle-packing shakedown (Task 03).
# Runs the search, extracts the best config (executing evolved code in-container),
# then runs the INDEPENDENT evaluator standalone on the saved config.
set -euo pipefail

EX=/work/example
OUT=/work/output
ITERS="${ITERS:-100}"

mkdir -p "$OUT"

echo "=== OpenEvolve pinned SHA (in image) ==="
cat /opt/OPENEVOLVE_SHA.txt

echo "=== Reachability: container -> host Ollama ==="
python - <<'PY'
import json, urllib.request
with urllib.request.urlopen("http://host.docker.internal:11434/v1/models", timeout=10) as r:
    print(json.load(r))
PY

echo "=== Running OpenEvolve: ${ITERS} iterations ==="
openevolve-run "$EX/initial_program.py" "$EX/evaluator.py" \
  --config "$EX/config.yaml" \
  --output "$OUT" \
  --iterations "$ITERS" \
  --log-level INFO

echo "=== Extracting best configuration ==="
python "$EX/extract_config.py" "$OUT/best/best_program.py" "$OUT/best_config.json"

echo "=== Independent evaluation (tol 1e-9) ==="
set +e
python /work/independent_evaluator.py "$OUT/best_config.json" --n 26 --tol 1e-9 > "$OUT/independent_eval_report.json"
RC=$?
set -e
cat "$OUT/independent_eval_report.json"
echo "independent_evaluator exit code: ${RC} (0=valid, 1=invalid)"
echo "DONE"
