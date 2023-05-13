import random
from dataclasses import dataclass

import utils
from mod import Mod


@dataclass
class paramsSS:
    t: int
    l: int
    s1: int
    s2: int


@dataclass
class proofSS:
    c: int
    D: int
    D1: int
    D2: int


def proveSS(x, n, r1, r2, g1, g2, h1, h2, b, params, debug=False):
    w = random.randint(1, 2 ** (params.l + params.t) * b - 1)
    eta1 = random.randint(1, 2 ** (params.l + params.t + params.s1) * n - 1)
    eta2 = random.randint(1, 2 ** (params.l + params.t + params.s2) * n - 1)
    omega1 = (Mod(g1, n) ** w * Mod(h1, n) ** eta1).x
    omega2 = (Mod(g2, n) ** w * Mod(h2, n) ** eta2).x
    c = hash(utils.concat(omega1, omega2))
    D = w + c * x
    D1 = eta1 + c * r1
    D2 = eta2 + c * r2

    if debug:
        print("\t ---Prove Same Secret: Debug--- \t")
        print("x: {}, n: {}, r1: {}, r2: {}, g1: {}, g2: {}, h1: {}, h2: {}, b:{}, params.t: {}, params.l: {}, params.s1: {}, params.s2: {}".format(x, n, r1, r2, g1, g2, h1, h2, b, params.t, params.l, params.s1, params.s2))
        print("w: {}, eta1: {}, eta2: {}, omega1: {}, omega2: {}, c: {}, D: {}, D1: {}, D2: {}\n".format(w, eta1, eta2, omega1, omega2, c, D, D1, D2))

    return proofSS(c, D, D1, D2)


def verifySS(E, F, n, g1, g2, h1, h2, proof, debug=False):
    cond1 = Mod(g1, n) ** proof.D * Mod(h1, n) ** proof.D1 * Mod(E, n) ** (-proof.c)
    cond2 = Mod(g2, n) ** proof.D * Mod(h2, n) ** proof.D2 * Mod(F, n) ** (-proof.c)

    if debug:
        print("\t ---Verify Same Secret: Debug--- \t")
        print("E: {}, F: {}, n: {}, g1: {}, g2: {}, h1: {}, h2: {}, proof.c: {}, proof.D: {}, proof.D1: {}, proof.D2: {}".format(E, F, n, g1, g2, h1, h2, proof.c, proof.D, proof.D1, proof.D2))
        print("Cond1: {}, {} * {} * {}".format(cond1, (Mod(g1, n) ** proof.D).x, (Mod(h1, n) ** proof.D1).x, (Mod(E, n) ** (-proof.c)).x))
        print("Cond2: {}, {} * {} * {}\n".format(cond2, (Mod(g2, n) ** proof.D).x, (Mod(h2, n) ** proof.D2).x, (Mod(F, n) ** (-proof.c)).x))

    return hash(utils.concat(cond1.x, cond2.x)) == proof.c


def proveSS_Flask(x, n, r1, r2, g1, g2, h1, h2, b, params, debug=False):
    """
    Mismo funcionamiento que proveSS, pero devolviendo parámetros extra para visualización.
    """
    w = random.randint(1, 2 ** (params.l + params.t) * b - 1)
    eta1 = random.randint(1, 2 ** (params.l + params.t + params.s1) * n - 1)
    eta2 = random.randint(1, 2 ** (params.l + params.t + params.s2) * n - 1)
    omega1 = (Mod(g1, n) ** w * Mod(h1, n) ** eta1).x
    omega2 = (Mod(g2, n) ** w * Mod(h2, n) ** eta2).x
    c = hash(utils.concat(omega1, omega2))
    D = w + c * x
    D1 = eta1 + c * r1
    D2 = eta2 + c * r2

    ext_ss = {'w': int(w), 'eta1': int(eta1), 'eta2': int(eta2), 'omega1': int(omega1), 'omega2': int(omega2)}

    if debug:
        print("\t ---Prove Same Secret: Debug--- \t")
        print("x: {}, n: {}, r1: {}, r2: {}, g1: {}, g2: {}, h1: {}, h2: {}, b:{}, params.t: {}, params.l: {}, params.s1: {}, params.s2: {}".format(x, n, r1, r2, g1, g2, h1, h2, b, params.t, params.l, params.s1, params.s2))
        print("w: {}, eta1: {}, eta2: {}, omega1: {}, omega2: {}, c: {}, D: {}, D1: {}, D2: {}\n".format(w, eta1, eta2, omega1, omega2, c, D, D1, D2))

    return proofSS(c, D, D1, D2), ext_ss
