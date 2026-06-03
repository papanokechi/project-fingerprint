"""OpenEvolve scoring evaluator for the cap-set constructor (Task 04).

Runs the (possibly evolved) program in a subprocess, retrieves (n, points), and
scores it. Score = cap size if the points form a valid cap, else 0.0. Invalid
sets MUST score zero (never as if valid). This is OpenEvolve's internal scoring
evaluator; the INDEPENDENT re-check is cap_set_evaluator.py, run standalone on the
saved best cap.
"""
import os
import pickle
import subprocess
import sys
import tempfile
import time
import traceback


def is_cap(n, points):
    """(is_valid, size, first_violating_triple_or_None). Validates structure too."""
    norm = []
    for p in points:
        if len(p) != n:
            return False, len(points), ("bad_length", p)
        coords = tuple(int(c) for c in p)
        for c in coords:
            if c not in (0, 1, 2):
                return False, len(points), ("bad_coord", p)
        norm.append(coords)
    pointset = set(norm)
    if len(pointset) != len(norm):
        return False, len(norm), ("duplicate", None)
    pl = list(pointset)
    for i in range(len(pl)):
        a = pl[i]
        for j in range(i + 1, len(pl)):
            b = pl[j]
            c = tuple((-a[k] - b[k]) % 3 for k in range(n))
            if c in pointset and c != a and c != b:
                return False, len(pointset), (a, b, c)
    return True, len(pointset), None


def run_with_timeout(program_path, timeout_seconds=120):
    """Execute the program in a subprocess and return (n, points)."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        script = f"""
import sys, os, pickle, traceback, importlib.util
sys.path.insert(0, os.path.dirname({program_path!r}))
try:
    spec = importlib.util.spec_from_file_location("program", {program_path!r})
    program = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(program)
    n, points = program.run_cap_construction()
    with open({temp_file.name!r} + ".results", "wb") as f:
        pickle.dump({{"n": int(n), "points": [list(p) for p in points]}}, f)
except Exception as e:
    traceback.print_exc()
    with open({temp_file.name!r} + ".results", "wb") as f:
        pickle.dump({{"error": str(e)}}, f)
"""
        temp_file.write(script.encode())
        temp_file_path = temp_file.name
    results_path = f"{temp_file_path}.results"
    try:
        process = subprocess.Popen(
            [sys.executable, temp_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            if stdout:
                print(f"Subprocess stdout: {stdout.decode(errors='replace')}")
            if stderr:
                print(f"Subprocess stderr: {stderr.decode(errors='replace')}")
            if process.returncode != 0:
                raise RuntimeError(f"Process exited with code {process.returncode}")
            if not os.path.exists(results_path):
                raise RuntimeError("Results file not found")
            with open(results_path, "rb") as f:
                results = pickle.load(f)
            if "error" in results:
                raise RuntimeError(f"Program failed: {results['error']}")
            return results["n"], results["points"]
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise TimeoutError(f"Process timed out after {timeout_seconds}s")
    finally:
        for path in (temp_file_path, results_path):
            if os.path.exists(path):
                os.unlink(path)


def evaluate(program_path):
    start = time.time()
    expected_n = int(os.environ.get("CAP_N", "3"))
    try:
        n, points = run_with_timeout(program_path, timeout_seconds=120)
        if n != expected_n:
            print(f"Dimension mismatch: program returned n={n}, expected {expected_n}")
            return {"validity": 0.0, "size": 0.0, "combined_score": 0.0,
                    "eval_time": float(time.time() - start)}
        valid, size, violation = is_cap(n, points)
        if not valid:
            print(f"Invalid cap (n={n}): {violation}")
        score = float(size) if valid else 0.0
        print(f"Evaluation: n={n}, valid={valid}, size={size}, "
              f"score={score}, time={time.time()-start:.2f}s")
        return {
            "validity": 1.0 if valid else 0.0,
            "size": float(size) if valid else 0.0,
            "combined_score": score,
            "eval_time": float(time.time() - start),
        }
    except Exception as e:
        print(f"Evaluation failed: {e}")
        traceback.print_exc()
        return {"validity": 0.0, "size": 0.0, "combined_score": 0.0,
                "eval_time": float(time.time() - start)}
