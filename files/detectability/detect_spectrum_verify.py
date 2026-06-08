#!/usr/bin/env python3
"""
Verification harness for the 'detectability spectrum' scoping memo.

Grounds every numeric/symbolic claim that appears in claims.jsonl:
  (1) class number h(Delta) via reduced binary-quadratic-form count
  (2) unit-group order w(K) for imaginary quadratic K
  (3) fundamental-discriminant test (QL15: Delta = -20, K = Q(sqrt(-5)))
  (4) splitting type of small primes via Kronecker symbol (Delta/p)
  (5) NON-CONSTANCY of h along a one-parameter family Delta(beta0)
      = the arithmetic engine of the no-channel theorem.

No external number-theory black boxes: class number is computed from the
definition (count of reduced primitive forms). Cross-checked against the
classical h=1 / h=2 / h=3 discriminant lists.

Run:  python detect_spectrum_verify.py
"""

from math import gcd, isqrt


def is_fundamental_discriminant(D: int) -> bool:
    if D >= 0 or D % 4 not in (0, 1):
        return False
    if D % 4 == 1:
        return is_squarefree(D)
    m = D // 4
    return (m % 4 in (2, 3)) and is_squarefree(m)


def is_squarefree(n: int) -> bool:
    n = abs(n)
    if n == 0:
        return False
    i = 2
    while i * i <= n:
        if n % (i * i) == 0:
            return False
        i += 1
    return True


def class_number_neg(D: int) -> int:
    """Form class number of the (possibly non-maximal) order of discriminant D<0.
    Counts reduced primitive positive-definite forms (a,b,c), b^2-4ac=D:
      -a < b <= a <= c, and b >= 0 if a == c.  Primitive: gcd(a,b,c)=1."""
    assert D < 0 and D % 4 in (0, 1), f"not a discriminant: {D}"
    count = 0
    a = 1
    while a * a <= -D / 3.0 + 1:
        # b has parity of D and |b| <= a
        b = -a + 1 if (a % 2) != (D % 2) else -a  # ensure b ~ D (mod 2)
        # normalize starting b to correct parity
        b = -a
        while (b - D) % 2 != 0:
            b += 1
        while b <= a:
            num = b * b - D
            if num % (4 * a) == 0:
                c = num // (4 * a)
                if a <= c:
                    if gcd(gcd(abs(a), abs(b)), abs(c)) == 1:
                        if (-a < b <= a <= c) and not (b < 0 and (a == b or a == c)):
                            count += 1
            b += 2
        a += 1
    return count


def kronecker(a: int, n: int) -> int:
    """Kronecker symbol (a/n)."""
    if n == 0:
        return 1 if a in (1, -1) else 0
    if n < 0:
        return kronecker(a, -1) * kronecker(a, -n)
    if n == -1 or n == 1:
        if n == 1:
            return 1
    result = 1
    if n % 2 == 0:
        if a % 2 == 0:
            return 0
        # (a/2)
        if a % 8 in (1, 7):
            two = 1
        else:
            two = -1
        while n % 2 == 0:
            n //= 2
            result *= two
    a %= n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def unit_order_w(D: int) -> int:
    """Order of the unit group of the imaginary quadratic order of discriminant D<0."""
    if D == -3:
        return 6
    if D == -4:
        return 4
    return 2


def split_type(D: int, p: int) -> str:
    s = kronecker(D, p)
    return {1: "split", -1: "inert", 0: "ramified"}[s]


def main():
    print("=== (1)+(2) class number h(D) and unit order w, classical anchors ===")
    anchors = {
        -3: (1, 6), -4: (1, 4), -7: (1, 2), -8: (1, 2), -11: (1, 2),
        -15: (2, 2), -20: (2, 2), -23: (3, 2), -24: (2, 2),
        -47: (5, 2), -71: (7, 2), -163: (1, 2),
    }
    ok = True
    for D, (h_exp, w_exp) in sorted(anchors.items(), reverse=True):
        h = class_number_neg(D)
        w = unit_order_w(D)
        flag = "OK" if (h == h_exp and w == w_exp) else "MISMATCH"
        if flag != "OK":
            ok = False
        print(f"  D={D:5d}  h={h}  (exp {h_exp})   w={w} (exp {w_exp})   fund={is_fundamental_discriminant(D)}   [{flag}]")
    print(f"  anchors all-correct: {ok}")

    print("\n=== (3) QL15 field: Delta=-20 is fundamental, K=Q(sqrt(-5)), h=2 ===")
    print(f"  is_fundamental(-20) = {is_fundamental_discriminant(-20)}")
    print(f"  h(-20) = {class_number_neg(-20)}   w(-20) = {unit_order_w(-20)}")
    print(f"  -20 = 4 * -5, squarefree(-5) = {is_squarefree(-5)}  => K = Q(sqrt(-5))")

    print("\n=== (4) splitting of small primes for Delta=-20 (Kronecker (-20/p)) ===")
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        print(f"  p={p:3d}: ({-20}/{p}) = {kronecker(-20, p):+d}  -> {split_type(-20, p)}")

    print("\n=== (5) NON-CONSTANCY of h on a 1-param family  Delta(b0) = b1^2 - 4*b2*b0 ===")
    print("    (engine of the no-channel theorem: surface selectors are b0-free,")
    print("     yet h varies wildly along b0).  Two illustrative loci:")
    for (b1, b2, label) in [(0, 1, "a=x^2+b0   (Delta=-4 b0)"),
                            (2, 3, "a=3x^2+2x+b0 (Delta=4-12 b0)")]:
        seq = []
        seen = {}
        for b0 in range(1, 13):
            D = b1 * b1 - 4 * b2 * b0
            if D < 0 and D % 4 in (0, 1):
                h = class_number_neg(D)
                seq.append((b0, D, h))
                seen.setdefault(h, []).append(b0)
        hs = [h for _, _, h in seq]
        print(f"\n  locus {label}:")
        print("    " + "  ".join(f"b0={b0}:D={D},h={h}" for b0, D, h in seq))
        print(f"    distinct h-values realized: {sorted(set(hs))}")
        print(f"    h is non-constant: {len(set(hs)) > 1}")
        # explicit witness: two b0 with SAME surface (any Delta!=0) but DIFFERENT h
        if len(set(hs)) > 1:
            h_lo = min(seen); h_hi = max(seen)
            print(f"    witness: b0={seen[h_lo][0]} gives h={h_lo}, "
                  f"b0={seen[h_hi][0]} gives h={h_hi}  (same surface type, Delta!=0)")

    print("\n=== (6) unit-group special fields reachable as a quadratic disc ===")
    print("    w>2 occurs ONLY at Delta in {-3 (w=6), -4 (w=4)}; check reachability")
    for (b1, b2, label) in [(0, 1, "Delta=-4 b0"), (2, 3, "Delta=4-12 b0"),
                            (3, 3, "Delta=9-12 b0")]:
        hits = []
        for b0 in range(1, 40):
            D = b1 * b1 - 4 * b2 * b0
            if D in (-3, -4):
                hits.append((b0, D))
        print(f"  locus {label}: Delta in {{-3,-4}} at {hits if hits else 'NONE (integer b0<40)'}")


def symbolic_selectors_beta0_free():
    """SURFACE-TYPE half of the no-channel theorem, re-derived this session.

    ODE: (a y')' - x^2 y = 0, a = b2 x^2 + b1 x + b0, i.e. a y'' + a' y' - x^2 y = 0.
    Show every local selector that fixes the Sakai surface type is b0-free:
      (i)  indicial exponents at each finite root of a  ->  {0,0}
      (ii) irregular rank / exponential rate at x = oo  ->  rank 1, lambda = +-1/sqrt(b2)
    """
    import sympy as sp
    x, r, b2, b1, b0, x0, x1 = sp.symbols('x r b2 b1 b0 x0 x1')

    print("\n=== (7) SYMBOLIC: Sakai selectors are beta0-free (surface-type no-channel) ===")
    # finite singular points: write a via its (abstract) roots so b0 enters only through x0,x1
    a = b2 * (x - x0) * (x - x1)
    c = -x**2
    b = sp.diff(a, x)                     # b = a'  (self-adjoint)
    P = sp.simplify(b / a)               # coefficient of y'
    Q = sp.simplify(c / a)               # coefficient of y

    p0 = sp.simplify(sp.limit((x - x0) * P, x, x0))       # residue of P at the root
    qlead = sp.simplify(sp.limit((x - x0)**2 * Q, x, x0))  # (x-x0)^2 Q  -> needs >simple pole
    indicial = sp.expand(r * (r - 1) + p0 * r + qlead)
    print(f"  (i)  finite root: p0 = {p0}   qlead = {qlead}   indicial(r) = {indicial}")
    print(f"       indicial == r**2 ? {sp.simplify(indicial - r**2) == 0}  "
          f"=> exponents {{0,0}}, free of b0,b1,b2,x0,x1")

    # irregular point at infinity: leading exponential rate lambda^2 + P_inf*lambda + Q_inf = 0
    a2 = b2 * x**2 + b1 * x + b0
    Pinf = sp.limit(x * (sp.diff(a2, x) / a2), x, sp.oo)   # x*P -> leading 1/x coeff
    Qinf = sp.limit((-x**2) / a2, x, sp.oo)                # Q -> constant => rank-1 exp point
    lam = sp.symbols('lam')
    rate_poly = lam**2 + 0 * lam + Qinf                    # leading characteristic at oo
    roots = sp.solve(sp.Eq(rate_poly, 0), lam)
    print(f"  (ii) at oo: x*P -> {Pinf} (=>P~2/x, no exp contribution), "
          f"Q -> {Qinf} (constant => irregular rank 1)")
    print(f"       exp rates lambda = {roots}  = +-1/sqrt(b2), free of b0,b1")
    print("  => full singular configuration (2 Fuchsian {0,0} + rank-1 oo) is b0-INDEPENDENT")
    print("     while Delta = b1^2 - 4 b2 b0 (hence h, Cl, w, ramification, splitting) varies.")


if __name__ == "__main__":
    main()
    symbolic_selectors_beta0_free()
