import random
import math
from dataclasses import dataclass

from mod import Mod
from square import proveS, verifyS, proofS, proveS_Flask
from interval import proveLI, verifyLI, proofLI, proveLI_Flask


@dataclass
class paramsWT:
    t: int
    l: int
    s: int


@dataclass
class proofWT:
    Ea: int
    Eb: int
    Ea1: int
    Ea2: int
    Eb1: int
    Eb2: int
    proof_sa: proofS
    proof_sb: proofS
    proof_lia: proofLI
    proof_lib: proofLI


def proveWT(x, n, g, h, r, a, b, E, params, debug=False):
    Ea = (Mod(E, n) * (Mod(g, n) ** a).inverse()).x
    Eb = (Mod(g, n) ** b * Mod(E, n).inverse()).x

    xa = x - a
    xb = b - x

    xa1 = math.floor(math.sqrt(x - a))
    xa2 = xa - xa1 ** 2

    xb1 = math.floor(math.sqrt(b - x))
    xb2 = xb - xb1 ** 2

    loop = True
    while loop:
        ra1 = random.randint(-2 ** params.s * n + 1, 2 ** params.s * n - 1)
        ra2 = r - ra1

        if -2 ** params.s * n + 1 < ra2 < 2 ** params.s * n - 1:
            loop = False

    rb1 = random.randint(-abs(r), abs(r))
    rb2 = -r - rb1

    Ea1 = (Mod(g, n) ** (xa1 ** 2) * Mod(h, n) ** ra1).x
    Ea2 = (Mod(g, n) ** xa2 * Mod(h, n) ** ra2).x
    Eb1 = (Mod(g, n) ** (xb1 ** 2) * Mod(h, n) ** rb1).x
    Eb2 = (Mod(g, n) ** xb2 * Mod(h, n) ** rb2).x

    proof_sa = proveS(xa1, n, ra1, g, h, b, params)
    proof_sb = proveS(xb1, n, rb1, g, h, b, params)

    proof_lia = proveLI(xa2, n, g, h, ra2, b, params)
    proof_lib = proveLI(xb2, n, g, h, rb2, b, params)

    if debug:
        print("\t ---Prove with tolerance: Debug--- \t")
        print("x: {}, n: {}, g: {}, h: {}, r: {}, a: {}, b: {}, E: {}, params.t: {}, params.l: {}, params.s: {}".format(x, n, g, h, r, a, b, E, params.t, params.l, params.s))
        print("Ea: {}, Ea1: {}, Ea2: {}, Eb: {}, Eb1: {}, Eb2: {}".format(Ea, Ea1, Ea2, Eb, Eb1, Eb2))
        print("xa: {}, xa1: {}, xa2: {}, xb: {}, xb1: {}, xb2: {}, ra1: {}, ra2: {}, rb1: {}, rb2: {}".format(xa, xa1, xa2, xb, xb1, xb2, ra1, ra2, rb1, rb2))
        print("ProveSa: E: {}, F: {}, c: {}, D: {}, D1: {}, D2: {}".format(proof_sa.E, proof_sa.F, proof_sa.proof_ss.c, proof_sa.proof_ss.D, proof_sa.proof_ss.D1, proof_sa.proof_ss.D2))
        print("ProveSb: E: {}, F: {}, c: {}, D: {}, D1: {}, D2: {}".format(proof_sb.E, proof_sb.F, proof_sb.proof_ss.c, proof_sb.proof_ss.D, proof_sb.proof_ss.D1, proof_sb.proof_ss.D2))
        print("ProveLIa: C: {}, D1: {}, D2: {}, c: {}".format(proof_lia.C, proof_lia.D1, proof_lia.D2, proof_lia.c))
        print("ProveLIb: C: {}, D1: {}, D2: {}, c: {} \n".format(proof_lib.C, proof_lib.D1, proof_lib.D2, proof_lib.c))

    return proofWT(Ea, Eb, Ea1, Ea2, Eb1, Eb2, proof_sa, proof_sb, proof_lia, proof_lib)


def verifyWT(n, g, h, b, proof, params, debug=False):
    if debug:
        print("\t ---Verify with tolerance: Debug--- \t")
        print("Ea2: {}, Ea: {}, Ea1: {}, {} == {}".format(proof.Ea2, proof.Ea, proof.Ea1, proof.Ea2, (Mod(proof.Ea, n) * Mod(proof.Ea1, n).inverse()).x))
        print("Eb2: {}, Eb: {}, Eb1: {}, {} == {}".format(proof.Eb2, proof.Eb, proof.Eb1, proof.Eb2, (Mod(proof.Eb, n) * Mod(proof.Eb1, n).inverse()).x))
        print("bs: {} and {}".format(verifyS(n, g, h, proof.proof_sa), verifyS(n, g, h, proof.proof_sb)))
        print("bli: {} and {}\n".format(verifyLI(proof.Ea2, n, g, h, b, proof.proof_lia, params), verifyLI(proof.Eb2, n, g, h, b, proof.proof_lib, params)))

    if proof.Ea2 == (Mod(proof.Ea, n) * Mod(proof.Ea1, n).inverse()).x and proof.Eb2 == (Mod(proof.Eb, n) * Mod(proof.Eb1, n).inverse()).x:
        bs = verifyS(n, g, h, proof.proof_sa, debug) and verifyS(n, g, h, proof.proof_sb, debug)
        bli = verifyLI(proof.Ea2, n, g, h, b, proof.proof_lia, params, debug) and verifyLI(proof.Eb2, n, g, h, b, proof.proof_lib, params, debug)
        return bs and bli
    else:
        return False


def proveWT_Flask(x, n, g, h, r, a, b, E, params, debug=False):
    """
    Mismo funcionamiento que proveWT, pero devolviendo parámetros extra para visualización.
    """
    Ea = (Mod(E, n) * (Mod(g, n) ** a).inverse()).x
    Eb = (Mod(g, n) ** b * Mod(E, n).inverse()).x

    xa = x - a
    xb = b - x

    xa1 = math.floor(math.sqrt(x - a))
    xa2 = xa - xa1 ** 2

    xb1 = math.floor(math.sqrt(b - x))
    xb2 = xb - xb1 ** 2

    loop = True
    while loop:
        ra1 = random.randint(-2 ** params.s * n + 1, 2 ** params.s * n - 1)
        ra2 = r - ra1

        if -2 ** params.s * n + 1 < ra2 < 2 ** params.s * n - 1:
            loop = False

    rb1 = random.randint(-abs(r), abs(r))
    rb2 = -r - rb1

    Ea1 = (Mod(g, n) ** (xa1 ** 2) * Mod(h, n) ** ra1).x
    Ea2 = (Mod(g, n) ** xa2 * Mod(h, n) ** ra2).x
    Eb1 = (Mod(g, n) ** (xb1 ** 2) * Mod(h, n) ** rb1).x
    Eb2 = (Mod(g, n) ** xb2 * Mod(h, n) ** rb2).x

    proof_sa, ext_sa, ext_ssa = proveS_Flask(xa1, n, ra1, g, h, b, params)
    proof_sb, ext_sb, ext_ssb = proveS_Flask(xb1, n, rb1, g, h, b, params)

    theta = math.floor(2 * math.sqrt(b-a))

    proof_lia, ext_lia = proveLI_Flask(xa2, n, g, h, ra2, theta, params)
    proof_lib, ext_lib = proveLI_Flask(xb2, n, g, h, rb2, theta, params)

    ext_wt = {'xa': xa, 'xb': xb, 'ra1': ra1, 'ra2': ra2, 'rb1': rb1, 'rb2': rb2, 'xa1': xa1, 'xa2': xa2, 'xb1': xb1,
              'xb2': xb2}

    if debug:
        print("\t ---Prove with tolerance: Debug--- \t")
        print("x: {}, n: {}, g: {}, h: {}, r: {}, a: {}, b: {}, E: {}, params.t: {}, params.l: {}, params.s: {}".format(x, n, g, h, r, a, b, E, params.t, params.l, params.s))
        print("Ea: {}, Ea1: {}, Ea2: {}, Eb: {}, Eb1: {}, Eb2: {}".format(Ea, Ea1, Ea2, Eb, Eb1, Eb2))
        print("xa: {}, xa1: {}, xa2: {}, xb: {}, xb1: {}, xb2: {}, ra1: {}, ra2: {}, rb1: {}, rb2: {}".format(xa, xa1, xa2, xb, xb1, xb2, ra1, ra2, rb1, rb2))
        print("ProveSa: E: {}, F: {}, c: {}, D: {}, D1: {}, D2: {}".format(proof_sa.E, proof_sa.F, proof_sa.proof_ss.c, proof_sa.proof_ss.D, proof_sa.proof_ss.D1, proof_sa.proof_ss.D2))
        print("ProveSb: E: {}, F: {}, c: {}, D: {}, D1: {}, D2: {}".format(proof_sb.E, proof_sb.F, proof_sb.proof_ss.c, proof_sb.proof_ss.D, proof_sb.proof_ss.D1, proof_sb.proof_ss.D2))
        print("ProveLIa: C: {}, D1: {}, D2: {}, c: {}".format(proof_lia.C, proof_lia.D1, proof_lia.D2, proof_lia.c))
        print("ProveLIb: C: {}, D1: {}, D2: {}, c: {} \n".format(proof_lib.C, proof_lib.D1, proof_lib.D2, proof_lib.c))

    return proofWT(Ea, Eb, Ea1, Ea2, Eb1, Eb2, proof_sa, proof_sb, proof_lia, proof_lib), ext_wt, ext_sa, ext_ssa,\
        ext_sb, ext_ssb, ext_lia, ext_lib


def verifyWT_Flask(n, g, h, b, proof, params, debug=False):
    """
    Mismo funcionamiento que verifyWT, pero devolviendo parámetros extra para visualización.
    """
    if debug:
        print("\t ---Verify with tolerance: Debug--- \t")
        print("Ea2: {}, Ea: {}, Ea1: {}, {} == {}".format(proof.Ea2, proof.Ea, proof.Ea1, proof.Ea2, (Mod(proof.Ea, n) * Mod(proof.Ea1, n).inverse()).x))
        print("Eb2: {}, Eb: {}, Eb1: {}, {} == {}".format(proof.Eb2, proof.Eb, proof.Eb1, proof.Eb2, (Mod(proof.Eb, n) * Mod(proof.Eb1, n).inverse()).x))
        print("bs: {} and {}".format(verifyS(n, g, h, proof.proof_sa), verifyS(n, g, h, proof.proof_sb)))
        print("bli: {} and {}\n".format(verifyLI(proof.Ea2, n, g, h, b, proof.proof_lia, params), verifyLI(proof.Eb2, n, g, h, b, proof.proof_lib, params)))

    cond1 = proof.Ea2 == (Mod(proof.Ea, n) * Mod(proof.Ea1, n).inverse()).x
    cond2 = proof.Eb2 == (Mod(proof.Eb, n) * Mod(proof.Eb1, n).inverse()).x

    if cond1 and cond2:
        cond3 = verifyS(n, g, h, proof.proof_sa, debug)
        cond4 = verifyS(n, g, h, proof.proof_sb, debug)

        cond5 = verifyLI(proof.Ea2, n, g, h, b, proof.proof_lia, params, debug)
        cond6 = verifyLI(proof.Eb2, n, g, h, b, proof.proof_lib, params, debug)

        bs = cond3 and cond4
        bli = cond5 and cond6

        ext = {'cond1': cond1, 'cond2': cond2, 'cond3': cond3, 'cond4': cond4, 'cond5': cond5, 'cond6': cond6}

        return (bs and bli), ext
    else:
        return False
