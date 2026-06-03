#!/usr/bin/env bash
# In-container orchestration for the cap-set shakedown (Task 04).
# Runs the search for one target dimension (CAP_N), extracts the best cap
# (executing evolved code in-container), then runs the INDEPENDENT evaluator
# standalone on the saved cap. Re-run once per dimension (n=3, n=4).
set -euo pipefail

EX="${EX:-/work/src/example}"
CAP_EVAL="${CAP_EVAL:-/work/src/cap_set_evaluator.py}"
OUT="${OUT:-/work/output}"
ITERS="${ITERS:-50}"
CAP_N="${CAP_N:-3}"
export CAP_N

mkdir -p "$OUT"

echo "=== OpenEvolve pinned SHA (in image) ==="
cat /opt/OPENEVOLVE_SHA.txt

echo "=== Target dimension: AG(${CAP_N},3) ==="

echo "=== Reachability: container -> host Ollama ==="
python - <<'PY'
import json, urllib.request
with urllib.request.urlopen("http://host.docker.internal:11434/v1/models", timeout=10) as r:
    print(json.load(r))
PY

echo "=== Running OpenEvolve: ${ITERS} iterations (n=${CAP_N}) ==="
openevolve-run "$EX/initial_program.py" "$EX/evaluator.py" \
  --config "$EX/config.yaml" \
  --output "$OUT" \
  --iterations "$ITERS" \
  --log-level INFO

echo "=== Extracting best cap ==="
python "$EX/extract_caps.py" "$OUT/best/best_program.py" "$OUT/best_cap.json"

echo "=== Independent evaluation (cap_set_evaluator.py, n=${CAP_N}) ==="
set +e
python "$CAP_EVAL" "$OUT/best_cap.json" --n "$CAP_N" > "$OUT/independent_eval_report.json"
RC=$?
set -e
cat "$OUT/independent_eval_report.json"
echo "cap_set_evaluator exit code: ${RC} (0=valid cap, 1=invalid)"
echo "DONE"
