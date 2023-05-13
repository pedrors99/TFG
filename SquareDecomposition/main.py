import random

from mod import Mod
from same_secret import paramsSS, proveSS, verifySS
from square import paramsS, proveS, verifyS
from interval import paramsLI, proveLI, verifyLI
from with_tolerance import paramsWT, proveWT, verifyWT
from square_decomposition import paramsSD, proveSD, verifySD


if __name__ == '__main__':
    t = 5
    l = 3
    s1 = 4
    s2 = 6

    x = 13
    n = 221

    a = 0
    b = 30

    r1 = random.randint(-2 ** s1 * n + 1, 2 ** s1 * n - 1)
    r2 = random.randint(-2 ** s2 * n + 1, 2 ** s2 * n - 1)

    g1 = 7
    h1 = 21
    E = (Mod(g1, n) ** x * Mod(h1, n) ** r1).x

    g2 = 14
    h2 = 28
    F = (Mod(g2, n) ** x * Mod(h2, n) ** r2).x

    print("Proving same secret...")
    params_ss = paramsSS(t, l, s1, s2)
    proof_ss = proveSS(x, n, r1, r2, g1, g2, h1, h2, b, params_ss)
    print("Verifying same secret...")
    secret = verifySS(E, F, n, g1, g2, h1, h2, proof_ss)
    print("Same Secret:", secret, "\n")

    print("Checking square...")
    params_s = paramsS(t, l, s1)
    proof_s = proveS(x, n, r1, g1, h1, b, params_s)
    print("Verifying square...")
    square = verifyS(n, g1, h1, proof_s)
    print("Square:", square, "\n")

    print("Checking interval...")
    params_li = paramsLI(t, l, s1)
    proof_li = proveLI(x, n, g1, h1, r1, b, params_li)
    print("Verifying interval...")
    interval = verifyLI(E, n, g1, h1, b, proof_li, params_li)
    print("Interval:", interval, "\n")

    print("Checking with tolerance...")
    params_wt = paramsWT(t, l, s1)
    proof_wt = proveWT(x, n, g1, h1, r1, a, b, E, params_wt)
    print("Verifying with tolerance...")
    tolerance = verifyWT(n, g1, h1, b, proof_wt, params_wt, False)
    print("Interval:", tolerance, "\n")

    """
    print("Checking Square Decomposition...")
    params_sd = paramsSD(t, l, s1)
    proof_sd = proveSD(x, n, g1, h1, r1, a, b, E, params_sd)
    print("Verifying Square Decomposition...")
    square_decomposition = verifySD(n, g1, h1, a, b, E, proof_sd, params_sd, False)
    print("Square Decomposition:", square_decomposition, "\n")
"""