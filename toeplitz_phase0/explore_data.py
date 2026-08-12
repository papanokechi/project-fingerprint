import json, time
from mpmath import mp
import sinekernel as sk

DPS = 220
data = {}
t0 = time.time()
for k in range(4, 21):
    s = 2 * k                     # s = 8, 10, ..., 40
    n = 2 * int((3 * s + 60) / 2)
    t = time.time()
    v = sk.log_det(s, n, DPS)
    data[str(s)] = mp.nstr(v, 200)
    print(f"s={s:3d} n={n:4d}  {time.time()-t:6.1f}s  {mp.nstr(v,20)}", flush=True)
json.dump({"dps": DPS, "data": data}, open("out/explore_data.json", "w"), indent=1)
print("total", time.time() - t0)
