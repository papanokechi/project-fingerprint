import time
from mpmath import mp
import sinekernel as sk

for s in (10, 20, 30, 40):
    print(f"--- s = {s} ---")
    prev = None
    for n in (60, 80, 120, 160, 200, 240):
        t = time.time()
        try:
            v = sk.log_det(s, n, 120)
        except ArithmeticError as e:
            print(f"  n={n:4d}: FAIL {e}")
            continue
        d = "-" if prev is None else f"{mp.nstr(abs(v-prev),3)}"
        print(f"  n={n:4d} dps=120: logdet={mp.nstr(v,25):>30}  |diff|={d:>12}  {time.time()-t:5.1f}s")
        prev = v
