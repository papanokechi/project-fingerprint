"""Phase 0.2: extract a, b, c from the certified data with an honest error bar.

    log det(I - K_s) = a s^2 + b log s + c + sum_k d_k s^{-k step} + R(s)

THE CENTRAL DISCIPLINE OF THIS FILE
-----------------------------------
mp.dps is NOT the accuracy of c.  The reported uncertainty on c is the
maximum of three independently measured quantities:

  (E1) ORDER TRUNCATION.  |c(K) - c(K-1)| over the last few orders of the
       Richardson sweep.  Measures the unmodelled tail of the asymptotic
       series.

  (E2) WINDOW SENSITIVITY.  |c(full window) - c(window with the smallest s
       dropped)|.  A tail that is being mistaken for a constant shows up here
       and not in (E1).

  (E3) DATA-NOISE AMPLIFICATION.  Perturb every input value by a random
       amount of size 10^-(certified digits) and refit, several times.  This
       measures how much the (badly conditioned) inverse-power design matrix
       amplifies the input uncertainty.  Estimating conditioning by argument
       instead of by measurement is exactly the kind of step that produces a
       confident wrong digit count.

The model class itself (even-only powers of 1/s) is not assumed: it is tested
by held-out prediction, and by checking that the odd coefficients of the
unrestricted fit are consistent with zero.
"""

from __future__ import annotations

import json
import random
from mpmath import mp

import asympt

DATA = "out/certified_data.json"
OUTPUT = "out/constant.json"


def load(path=DATA, headroom=350):
    """Load the certified grid.

    `headroom` is working precision ABOVE the certified digits of the data,
    and it is not decoration.  The design matrix contains columns s^-2 ...
    s^-2K over the full grid, whose dynamic range is (s_max/s_min)^(2K).  On
    the revision-3 grid (s_max/s_min ~ 5, K up to ~140) that is ~10^195 of
    pure range, all of which must be carried on top of the digits we actually
    want.  Too little headroom does not corrupt the answer silently -- it
    inflates E1 and E2, which is the honest direction -- but it wastes the
    data.

    NOTE, and this is not a stylistic point: mp.dps MUST be raised BEFORE the
    decimal strings are parsed.  An earlier version of this function parsed
    first and raised precision afterwards, which silently truncated 124-digit
    data to mpmath's 15-digit default; the order sweep then stalled around
    1e-10 and diverged past K=7, looking exactly like an ill-conditioning
    problem rather than the data-destruction it was.  The failure was caught
    only because an independent script that set mp.dps first reached 1e-38 on
    the same grid.
    """
    d = json.load(open(path))
    cert_digits = float(d["meta"]["min_certified_digits"])
    mp.dps = int(cert_digits) + headroom
    cert = mp.mpf(d["meta"]["min_certified_digits"])
    pts = {mp.mpf(r["s"]): mp.mpf(r["value"]) for r in d["rows"]}
    return d["meta"], pts, cert


def _digits(x):
    return mp.inf if x == 0 else -mp.log10(abs(x))


def select_points(svals, m: int):
    """m points spread evenly BY INDEX across the whole grid, endpoints included.

    Taking instead the m largest s (the obvious choice, and the one this code
    originally made) collapses the fit onto a tiny window at the top of the
    grid where the basis functions s^2, log s, 1, s^-2, ... are numerically
    almost linearly dependent.  That produced a design matrix so ill
    conditioned that the sweep diverged past K=4, with fitted a and b running
    away from -1/2 and -1/4 by many orders of magnitude.  Spanning the full
    window keeps the extrapolation to 1/s^2 = 0 conditioned.
    """
    if m <= 1:
        return [svals[-1]]
    N = len(svals)
    idx = sorted({round(i * (N - 1) / (m - 1)) for i in range(m)})
    if len(idx) != m:
        raise ValueError(f"grid too coarse to select {m} distinct points")
    return [svals[i] for i in idx]


def order_table(pts, step, Kmax, stride=1):
    """Sweep the number of correction orders K.

    `stride` skips orders on large grids, where the sweep costs O(K^3) per
    order and O(K^4) overall.  Skipping is safe in the honest direction: the
    successive difference then straddles `stride` orders, so it is an
    OVER-estimate of the per-order truncation change, never an under-estimate.
    """
    svals = sorted(pts)
    rows = []
    prev = None
    for K in range(0, Kmax + 1, stride):
        if K + 3 > len(svals):
            break
        use = select_points(svals, K + 3)
        a, b, c, ds = asympt.fit(use, [pts[s] for s in use], K, step)
        rows.append({"K": K, "a": a, "b": b, "c": c, "d": ds,
                     "dc": None if prev is None else abs(c - prev)})
        prev = c
    return rows


def odd_coefficient_test(pts, K=8):
    """Unrestricted (step=1) fit: are the odd 1/s coefficients consistent with 0?

    Returns (max |odd|, max |even|, ratio).  A small ratio is evidence FOR the
    even-only model; it is not a proof of it.
    """
    svals = sorted(pts)
    use = select_points(svals, K + 3)
    _, _, _, ds = asympt.fit(use, [pts[s] for s in use], K, 1)
    odd = [abs(ds[i]) for i in range(0, len(ds), 2)]      # d_1, d_3, ...
    even = [abs(ds[i]) for i in range(1, len(ds), 2)]     # d_2, d_4, ...
    mo, me = max(odd), max(even)
    return mo, me, (mo / me if me else mp.inf)


def noise_sensitivity(pts, K, step, cert_digits, trials=6, seed=20260812):
    """(E3) Refit with inputs randomised at the certified noise floor."""
    rng = random.Random(seed)
    svals = sorted(pts)
    use = select_points(svals, K + 3)
    base = asympt.fit(use, [pts[s] for s in use], K, step)[2]
    eps = mp.mpf(10) ** (-cert_digits)
    worst = mp.mpf(0)
    for _ in range(trials):
        ys = [pts[s] + eps * mp.mpf(rng.uniform(-1, 1)) for s in use]
        c = asympt.fit(use, ys, K, step)[2]
        worst = max(worst, abs(c - base))
    return worst


def choose_order(rows, cert_digits):
    """Select the order at the flattest part of the sweep.

    Scoring by the successive difference at a single K rewards a lucky dip:
    near the truncation floor the sweep is noisy and some individual order
    will happen to reproduce the previous one closely.  We instead score each
    K by the WORST successive difference over a window of three consecutive
    SWEPT orders (consecutive in the table, which may be strided), so the
    selected K has to sit on a genuine plateau, and the score itself is then a
    defensible (E1).  Returns (K, score).
    """
    floor = mp.mpf(10) ** (-cert_digits)
    seq = [r for r in rows if r["dc"] is not None]
    best, bestval = None, None
    for i, r in enumerate(seq):
        if r["K"] < 4:
            continue
        window = [x["dc"] for x in seq[i:i + 3]]
        if len(window) < 2:
            continue
        v = max(max(window), floor)
        if bestval is None or v < bestval:
            best, bestval = r["K"], v
    if best is None and seq:
        best, bestval = seq[-1]["K"], seq[-1]["dc"]
    elif best is None:
        best, bestval = 4, mp.mpf(1)
    return best, bestval


def main():
    meta, pts, cert = load()
    svals = sorted(pts)
    print(f"grid: {len(svals)} points, s in [{mp.nstr(svals[0],6)}, "
          f"{mp.nstr(svals[-1],6)}], min certified digits per point = {mp.nstr(cert,8)}")

    # --- model-class evidence ------------------------------------------------
    mo, me, ratio = odd_coefficient_test(pts, K=8)
    print(f"\n[model class] unrestricted fit: max|odd d_k| = {mp.nstr(mo,6)}, "
          f"max|even d_k| = {mp.nstr(me,6)}, ratio = {mp.nstr(ratio,6)}")

    # --- order sweeps --------------------------------------------------------
    stride = 1 if len(svals) <= 100 else 2
    print(f"\n[order sweep, even-only model, stride {stride}]")
    rows = order_table(pts, 2, len(svals) - 3, stride)
    for r in rows:
        dc = "-" if r["dc"] is None else mp.nstr(r["dc"], 4)
        print(f"  K={r['K']:3d}  a={mp.nstr(r['a'],14):>18}  b={mp.nstr(r['b'],14):>18}"
              f"  c={mp.nstr(r['c'],36):>40}  |dc|={dc}")

    Kbest, e_order = choose_order(rows, cert)
    rec = [r for r in rows if r["K"] == Kbest][0]
    a, b, c = rec["a"], rec["b"], rec["c"]
    print(f"\nselected K = {Kbest}  (flattest 3-order window)")

    # --- error budget --------------------------------------------------------
    sub = {s: pts[s] for s in svals[1:]}
    rows2 = order_table(sub, 2, len(sub) - 3, stride)
    K2 = min(Kbest, max(r["K"] for r in rows2))
    c_shift = min((r for r in rows2 if r["K"] <= K2),
                  key=lambda r: abs(r["K"] - K2))["c"]
    e_window = abs(c - c_shift)

    e_noise = noise_sensitivity(pts, Kbest, 2, cert)

    sigma = max(e_order, e_window, e_noise)
    print("\n[error budget on c]")
    print(f"  (E1) order truncation      : {mp.nstr(e_order,6)}  -> {mp.nstr(_digits(e_order),6)} digits")
    print(f"  (E2) window sensitivity    : {mp.nstr(e_window,6)}  -> {mp.nstr(_digits(e_window),6)} digits")
    print(f"  (E3) data-noise amplified  : {mp.nstr(e_noise,6)}  -> {mp.nstr(_digits(e_noise),6)} digits")
    print(f"  ADOPTED sigma_c            : {mp.nstr(sigma,6)}")
    print(f"  HONEST DIGITS IN c         : {int(_digits(sigma))}   "
          f"(working precision was {mp.dps} dps -- a different number)")

    # --- held-out falsification ---------------------------------------------
    held = svals[len(svals) // 2]
    res, _ = asympt.holdout_residual(pts, min(Kbest, len(svals) - 4), held, 2)
    print(f"\n[held-out test] s={mp.nstr(held,6)} excluded from fit, "
          f"|prediction - computed| = {mp.nstr(res,6)}")

    nd = int(_digits(sigma))
    out = {
        "a": mp.nstr(a, 30), "b": mp.nstr(b, 30),
        "c": mp.nstr(c, max(10, nd + 5)),
        "c_full": mp.nstr(c, 200),
        "K": Kbest, "step": 2, "sweep_stride": stride,
        "sigma_c": mp.nstr(sigma, 6),
        "honest_digits_c": nd,
        "e_order": mp.nstr(e_order, 6),
        "e_window": mp.nstr(e_window, 6),
        "e_noise": mp.nstr(e_noise, 6),
        "odd_even_ratio": mp.nstr(ratio, 6),
        "holdout_residual": mp.nstr(res, 6),
        "min_certified_digits_per_point": mp.nstr(cert, 8),
        "grid_points": len(svals),
    }
    json.dump(out, open(OUTPUT, "w"), indent=1)
    print("\nwrote", OUTPUT)


if __name__ == "__main__":
    main()
