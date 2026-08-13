
def main(s_int):
    coeffs = load_coeffs("x.json")
    orders = sorted(coeffs)
    best = search(coeffs)
    M, cv, omit = best
    saturated = bool(M >= orders[-1] or 2 * s_int > orders[-1])
    print(saturated)
