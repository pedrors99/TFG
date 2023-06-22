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
    """
    Algoritmo usado para construir la prueba de que dos compromisos esconden el mismo secreto. Estos dos compromisos son
    de la forma:
    E = g1^x + h1^r1
    F = g2^x + h2^r2

    :param x: Secreto escondido en los compromisos.
    :param n: Módulo.
    :param r1: Elemento requerido para construir el primer compromiso.
    :param r2: Elemento requerido para construir el segundo compromiso.
    :param g1: Base para construir el primer compromiso.
    :param g2: Base para construir el segundo compromiso.
    :param h1: Base para construir el primer compromiso.
    :param h2: Base para construir el segundo compromiso.
    :param b: Cota superior del intervalo al que pertenece x.
    :param params: Parámetros de seguridad.
    :param debug: Determina si imprimir información extra del funcionamiento por pantalla.
    :return: Prueba de que dos compromisos esconden el mismo secreto.
    """
    w = random.randint(1, 2 ** (params.l + params.t) * b - 1)
    eta1 = random.randint(1, 2 ** (params.l + params.t + params.s1) * n - 1)
    eta2 = random.randint(1, 2 ** (params.l + params.t + params.s2) * n - 1)
    omega1 = (Mod(g1, n) ** w * Mod(h1, n) ** eta1).x
    omega2 = (Mod(g2, n) ** w * Mod(h2, n) ** eta2).x
    c = utils.hash(utils.concat(omega1, omega2))
    D = w + c * x
    D1 = eta1 + c * r1
    D2 = eta2 + c * r2

    if debug:
        print("\t ---Prove Same Secret: Debug--- \t")
        print("x: {}, n: {}, r1: {}, r2: {}, g1: {}, g2: {}, h1: {}, h2: {}, b:{}, params.t: {}, params.l: {}, params.s1: {}, params.s2: {}".format(x, n, r1, r2, g1, g2, h1, h2, b, params.t, params.l, params.s1, params.s2))
        print("w: {}, eta1: {}, eta2: {}, omega1: {}, omega2: {}, c: {}, D: {}, D1: {}, D2: {}\n".format(w, eta1, eta2, omega1, omega2, c, D, D1, D2))

    return proofSS(c, D, D1, D2)


def verifySS(E, F, n, g1, g2, h1, h2, proof, debug=False):
    """
    Algoritmo utilizado para comprobar que dos compromisos esconden el mismo secreto.

    :param E: Primer compromiso.
    :param F: Segundo compromiso.
    :param n: Módulo.
    :param g1: Base del primer compromiso.
    :param g2: Base del segundo compromiso.
    :param h1: Base del primer compromiso.
    :param h2: Base del segundo compromiso.
    :param proof: Prueba de qye ambos compromisos esconden el mismo secreto.
    :param debug: Determina si imprimir información extra del funcionamiento por pantalla.
    :return: True o False, dependiendo de si la verificación es correcta o incorrecta respectivamente.
    """
    val1 = Mod(g1, n) ** proof.D * Mod(h1, n) ** proof.D1 * Mod(E, n) ** (-proof.c)
    val2 = Mod(g2, n) ** proof.D * Mod(h2, n) ** proof.D2 * Mod(F, n) ** (-proof.c)

    if debug:
        print("\t ---Verify Same Secret: Debug--- \t")
        print("E: {}, F: {}, n: {}, g1: {}, g2: {}, h1: {}, h2: {}, proof.c: {}, proof.D: {}, proof.D1: {}, proof.D2: {}".format(E, F, n, g1, g2, h1, h2, proof.c, proof.D, proof.D1, proof.D2))
        print("Cond1: {}, {} * {} * {}".format(val1, (Mod(g1, n) ** proof.D).x, (Mod(h1, n) ** proof.D1).x, (Mod(E, n) ** (-proof.c)).x))
        print("Cond2: {}, {} * {} * {}\n".format(val2, (Mod(g2, n) ** proof.D).x, (Mod(h2, n) ** proof.D2).x, (Mod(F, n) ** (-proof.c)).x))

    return utils.hash(utils.concat(val1.x, val2.x)) == proof.c


def proveSS_Flask(x, n, r1, r2, g1, g2, h1, h2, b, params, debug=False):
    """
    Mismo funcionamiento que proveSS, pero devolviendo parámetros extra para visualización.
    """
    w = random.randint(1, 2 ** (params.l + params.t) * b - 1)
    eta1 = random.randint(1, 2 ** (params.l + params.t + params.s1) * n - 1)
    eta2 = random.randint(1, 2 ** (params.l + params.t + params.s2) * n - 1)
    omega1 = (Mod(g1, n) ** w * Mod(h1, n) ** eta1).x
    omega2 = (Mod(g2, n) ** w * Mod(h2, n) ** eta2).x
    c = utils.hash(utils.concat(omega1, omega2))
    D = w + c * x
    D1 = eta1 + c * r1
    D2 = eta2 + c * r2

    ext_ss = {'w': int(w), 'int1': int(2 ** (params.l + params.t) * b - 1),
              'int2': int(2 ** (params.l + params.t + params.s1) * n - 1),
              'int3': int(2 ** (params.l + params.t + params.s2) * n - 1), 'eta1': int(eta1), 'eta2': int(eta2),
              'omega1': int(omega1), 'omega2': int(omega2)}

    if debug:
        print("\t ---Prove Same Secret: Debug--- \t")
        print("x: {}, n: {}, r1: {}, r2: {}, g1: {}, g2: {}, h1: {}, h2: {}, b:{}, params.t: {}, params.l: {}, params.s1: {}, params.s2: {}".format(x, n, r1, r2, g1, g2, h1, h2, b, params.t, params.l, params.s1, params.s2))
        print("w: {}, eta1: {}, eta2: {}, omega1: {}, omega2: {}, c: {}, D: {}, D1: {}, D2: {}\n".format(w, eta1, eta2, omega1, omega2, c, D, D1, D2))

    return proofSS(c, D, D1, D2), ext_ss


def verifySS_Flask(E, F, n, g1, g2, h1, h2, proof, debug=False):
    """
    Mismo funcionamiento que verifySS, pero devolviendo parámetros extra para visualización.
    """
    val1 = Mod(g1, n) ** proof.D * Mod(h1, n) ** proof.D1 * Mod(E, n) ** (-proof.c)
    val2 = Mod(g2, n) ** proof.D * Mod(h2, n) ** proof.D2 * Mod(F, n) ** (-proof.c)

    ext = {'val1': int(val1.x), 'val2': int(val2.x), 'val3': int(utils.hash(utils.concat(val1.x, val2.x))),
           'cond': utils.hash(utils.concat(val1.x, val2.x)) == proof.c}

    if debug:
        print("\t ---Verify Same Secret: Debug--- \t")
        print("E: {}, F: {}, n: {}, g1: {}, g2: {}, h1: {}, h2: {}, proof.c: {}, proof.D: {}, proof.D1: {}, proof.D2: {}".format(E, F, n, g1, g2, h1, h2, proof.c, proof.D, proof.D1, proof.D2))
        print("Cond1: {}, {} * {} * {}".format(val1, (Mod(g1, n) ** proof.D).x, (Mod(h1, n) ** proof.D1).x, (Mod(E, n) ** (-proof.c)).x))
        print("Cond2: {}, {} * {} * {}\n".format(val2, (Mod(g2, n) ** proof.D).x, (Mod(h2, n) ** proof.D2).x, (Mod(F, n) ** (-proof.c)).x))

    return (utils.hash(utils.concat(val1.x, val2.x)) == proof.c), ext
