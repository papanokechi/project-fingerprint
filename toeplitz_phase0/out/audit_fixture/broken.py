
def main():
    coeffs = load_coeffs("x.json")
    orders = sorted(coeffs)
    for s_int in (149, 200, 250):
        best = search(coeffs)
        M, cv, omit = best
        saturated = M >= orders[-1]
        print(saturated)
