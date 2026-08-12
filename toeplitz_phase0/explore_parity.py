import json
from mpmath import mp
import asympt

d = json.load(open("out/explore_data.json"))
mp.dps = 180
pts = {mp.mpf(k): mp.mpf(v) for k, v in d["data"].items()}
svals = sorted(pts)

K = 8
use = svals[-(K + 3):]
a, b, c, ds = asympt.fit(use, [pts[s] for s in use], K)
print("fitted d_k for K=8 (odd k should vanish if series is even):")
for i, v in enumerate(ds, 1):
    print(f"   d_{i} = {mp.nstr(v, 12)}")
