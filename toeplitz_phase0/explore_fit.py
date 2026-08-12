import json
from mpmath import mp
import asympt

d = json.load(open("out/explore_data.json"))
mp.dps = 180
pts = {mp.mpf(k): mp.mpf(v) for k, v in d["data"].items()}
svals = sorted(pts)

print("order-K sweep, using the K+3 largest s values")
prev = None
for K in range(0, 15):
    use = svals[-(K + 3):]
    if len(use) < K + 3:
        break
    a, b, c, ds = asympt.fit(use, [pts[s] for s in use], K)
    diff = "-" if prev is None else mp.nstr(abs(c - prev), 4)
    print(f"K={K:3d}  a={mp.nstr(a,12):>18} b={mp.nstr(b,12):>16} "
          f"c={mp.nstr(c,30):>34}  dc={diff}")
    prev = c
