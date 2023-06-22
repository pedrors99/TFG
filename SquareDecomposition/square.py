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


def proveS(x, n, E, r1, g, h, b, params, debug=False):
    """
    Algoritmo que construye la prueba de que un compromiso esconde un cuadrado.

    :param x: Secreto escondido por el compromiso.
    :param n: Módulo.
    :param E: Compromiso que esconde el secreto.
    :param r1: Elemento requerido para construir el compromiso.
    :param g: Base del compromiso.
    :param h: Base del compromiso.
    :param b: Cota superior del intervalo al que pertenece x.
    :param params: Parámetros de seguridad.
    :param debug: Determina si imprimir información extra del funcionamiento por pantalla.
    :return: Prueba de que el compromiso esconde un cuadrado.
    """
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
    """
    Verificación de que un compromiso esconde un cuadrado.

    :param n: Módulo.
    :param g: Base del compromiso.
    :param h: Base del compromiso.
    :param proof: Prueba de que el compromiso esconde un cuadrado.
    :param debug: Determina si imprimir información extra del funcionamiento por pantalla.
    :return: True o False, dependiendo de si la verificación es correcta o incorrecta respectivamente.
    """
    if debug:
        print("\t ---Verify Square: Debug--- \t")
        print("n: {}, g: {}, h: {}, proof.E: {}, proof.F: {}, proof.proof_ss.c: {}, proof.proof_ss.D: {}, proof.proof_ss.D1: {}, proof.proof_ss.D2: {}\n".format(n, g, h, proof.E, proof.F, proof.proof_ss.c, proof.proof_ss.D, proof.proof_ss.D1, proof.proof_ss.D2))

    return verifySS(proof.E, proof.F, n, proof.F, g, h, h, proof.proof_ss, debug)


def proveS_Flask(x, n, E, r1, g, h, b, params, debug=False):
    """
    Mismo funcionamiento que proveS, pero devolviendo parámetros extra para visualización.
    """
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


def verifyS_Flask(n, g, h, proof, debug=False):
    """
    Mismo funcionamiento que verifyS, pero devolviendo parámetros extra para visualización.
    """
    if debug:
        print("\t ---Verify Square: Debug--- \t")
        print("n: {}, g: {}, h: {}, proof.E: {}, proof.F: {}, proof.proof_ss.c: {}, proof.proof_ss.D: {}, proof.proof_ss.D1: {}, proof.proof_ss.D2: {}\n".format(n, g, h, proof.E, proof.F, proof.proof_ss.c, proof.proof_ss.D, proof.proof_ss.D1, proof.proof_ss.D2))

    return verifySS(proof.E, proof.F, n, proof.F, g, h, h, proof.proof_ss, debug)

