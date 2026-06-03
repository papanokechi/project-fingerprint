#!/usr/bin/env python3
"""Extract a 26-circle configuration from an evolved best_program.py.

Runs INSIDE the container (it executes evolved code via run_packing()). Writes a
JSON config the independent evaluator can re-check standalone.
"""
import importlib.util
import json
import sys

import numpy as np


def main() -> int:
    program_path, out_path = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location("best_program", program_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    centers, radii, reported_sum = module.run_packing()
    centers = np.asarray(centers, dtype=float)
    radii = np.asarray(radii, dtype=float)

    config = {
        "n": int(radii.shape[0]),
        "centers": centers.tolist(),
        "radii": [float(r) for r in radii.tolist()],
        "reported_sum": float(reported_sum),
        "source_program": program_path,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2)
    print(f"Extracted {config['n']} circles; reported_sum={config['reported_sum']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
