#!/usr/bin/env python3
"""Extract a cap from an evolved best_program.py (Task 04).

Runs INSIDE the container (executes evolved code via run_cap_construction()).
Writes a JSON config the independent cap_set_evaluator.py can re-check standalone.
"""
import importlib.util
import json
import sys


def main() -> int:
    program_path, out_path = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location("best_program", program_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    n, points = module.run_cap_construction()
    points = [[int(c) for c in p] for p in points]
    config = {
        "n": int(n),
        "points": points,
        "size": len(points),
        "source_program": program_path,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)
    print(f"Extracted cap: n={config['n']}, size={config['size']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
