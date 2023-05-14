import random
from dataclasses import dataclass

from mod import Mod
from same_secret import proveSS, paramsSS, verifySS, proveSS_Flask


@dataclass
class paramsS:
    t: int
    l: int
    s: int


@dataclass
class proofS:
    E: int
    F: int
    proof_ss: proveSS


def proveS(x, n, r1, g, h, b, params, debug=False):
    E = (Mod(g, n) ** (Mod(x, n) ** 2).x * Mod(h, n) ** r1).x
    r2 = random.randint(-2 ** params.s * n + 1, 2 ** params.s * n - 1)
    F = (Mod(g, n) ** x * Mod(h, n) ** r2).x
    r3 = r1 - r2 * x
    params_ss = paramsSS(params.t, params.l, params.s, params.s)

    if debug:
        print("\t ---Prove Square: Debug--- \t")
        print("x: {}, n: {}, r1: {}, g: {}, h: {}, b: {}, params.t: {}, params.l: {}, params.s: {}".format(x, n, r1, g, h, b, params.t, params.l, params.s))
        print("r2: {}, r3: {}, E: {}, F: {}\n".format(r2, r3, E, F))

    proof = proveSS(x, n, r3, r2, F, g, h, h, b, params_ss, debug)
    return proofS(E, F, proof)


def verifyS(n, g, h, proof, debug=False):
    if debug:
        print("\t ---Verify Square: Debug--- \t")
        print("n: {}, g: {}, h: {}, proof.E: {}, proof.f: {}, proof.proof_ss.c: {}, proof.proof_ss.D: {}, proof.proof_ss.D1: {}, proof.proof_ss.D2: {}".format(n, g, h, proof.E, proof.F, proof.proof_ss.c, proof.proof_ss.D, proof.proof_ss.D1, proof.proof_ss.D2))

    return verifySS(proof.E, proof.F, n, proof.F, g, h, h, proof.proof_ss, debug)


def proveS_Flask(x, n, r1, g, h, b, params, debug=False):
    """
    Mismo funcionamiento que proveS, pero devolviendo parámetros extra para visualización.
    """
    E = (Mod(g, n) ** (Mod(x, n) ** 2).x * Mod(h, n) ** r1).x
    r2 = random.randint(-2 ** params.s * n + 1, 2 ** params.s * n - 1)
    F = (Mod(g, n) ** x * Mod(h, n) ** r2).x
    r3 = r1 - r2 * x
    params_ss = paramsSS(params.t, params.l, params.s, params.s)

    proof, ext_ss = proveSS_Flask(x, n, r3, r2, F, g, h, h, b, params_ss, debug)
    ext_s = {'E': int(E), 'F': int(F), 'r2': int(r2), 'r3': int(r3)}

    if debug:
        print("\t ---Prove Square: Debug--- \t")
        print("x: {}, n: {}, r1: {}, g: {}, h: {}, b: {}, params.t: {}, params.l: {}, params.s: {}".format(x, n, r1, g, h, b, params.t, params.l, params.s))
        print("r2: {}, r3: {}, E: {}, F: {}\n".format(r2, r3, E, F))
    return proofS(E, F, proof), ext_s, ext_ss

