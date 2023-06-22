import random
from dataclasses import dataclass

import utils
from mod import Mod


@dataclass
class paramsLI:
    t: int
    l: int
    s: int


@dataclass
class proofLI:
    C: int
    D1: int
    D2: int
    c: int


def proveLI(x, n, g, h, r, b, params, debug=False):
    """
    Algoritmo que construye la prueba de que un número comprometido pertenece a un intervalo I, donde:
                 I = [-2^(params.t + params.l) * b, 2^(params.t + params.l) * b)

    :param x: Número comprometido.
    :param n: Módulo.
    :param g: Base para el compromiso que esconde a x.
    :param h: Base para el compromiso que esconde a x.
    :param r: Elemento para construir el compromiso que esconde a x.
    :param b: Cota superior del intervalo que contiene a x.
    :param params: Parámetros de seguridad.
    :param debug: Determina si imprimir información extra del funcionamiento por pantalla.
    :return: Prueba de que el número comprometido pertenece al intervalo.
    """
    loop = True

    while loop:
        w = random.randint(0, int(2 ** (params.t + params.l) * b))
        eta = random.randint(-2 ** (params.t + params.l + params.s) * n + 1, 2 ** (params.t + params.l + params.s) * n - 1)

        omega = (Mod(g, n) ** w * Mod(h, n) ** eta).x
        C = utils.hash(omega)
        c = C % (2 ** params.t)
        D1 = w + x * c
        D2 = eta + r * c

        if c * b <= D1 <= 2 ** (params.t + params.l) * b - 1:
            loop = False

    if debug:
        print("\t ---Prove Interval: Debug--- \t")
        print("x: {}, n: {}, g: {}, h: {}, r: {}, b: {}, params.t: {}, params.l: {}, params.s: {}".format(x, n, g, h, r, b, params.t, params.l, params.s))
        print("w: {}, eta: {}, omega: {}, C: {}, D1: {}, D2: {}, c: {}\n".format(w, eta, omega, C, D1, D2, c))

    return proofLI(C, D1, D2, c)


def verifyLI(E, n, g, h, b, proof, params, debug=False):
    """
    Verificación de la prueba de que un secreto pertenece a un intervalo.

    :param E: Compromiso que esconde el secreto.
    :param n: Módulo.
    :param g: Base del compromiso.
    :param h: Base del compromiso.
    :param b: Cota superior del intervalo que contiene al secreto.
    :param proof: Prueba de que el secreto pertenece al intervalo.
    :param proof: Prueba de qye ambos compromisos esconden el mismo secreto.
    :param debug: Determina si imprimir información extra del funcionamiento por pantalla.
    :return: True o False, dependiendo de si la verificación es correcta o incorrecta respectivamente.
    """
    cond1 = (proof.c * b <= proof.D1 <= 2 ** (params.t + params.l) * b - 1)
    cond2 = (proof.C == utils.hash((Mod(g, n) ** proof.D1 * Mod(h, n) ** proof.D2 * Mod(E, n) ** (-proof.c)).x))

    if debug:
        print("\t ---Verify Interval: Debug--- \t")
        print("E: {}, n: {}, g: {}, h: {}, b: {}, proof.C: {}, proof.D1: {}, proof.D2: {}, proof.c: {}, params.t: {}, params.l: {}, params.s: {}".format(E, n, g, h, b, proof.C, proof.D1, proof.D2, proof.c, params.t, params.l, params.s))
        print("Cond1: {}, {} <= {} <= {}".format(cond1, proof.c * b, proof.D1, 2 ** (params.t + params.l) * b - 1))
        print("Cond2: {}, {} = {}\n".format(cond2, proof.C, utils.hash((Mod(g, n) ** proof.D1 * Mod(h, n) ** proof.D2 * Mod(E, n) ** (-proof.c)).x)))

    return cond1 and cond2


def proveLI_Flask(x, n, g, h, r, b, params, debug=False):
    """
    Mismo funcionamiento que proveLI, pero devolviendo parámetros extra para visualización.
    """
    loop = True

    while loop:
        w = random.randint(0, int(2 ** (params.t + params.l) * b - 1))
        eta = random.randint(-2 ** (params.t + params.l + params.s) * n + 1, 2 ** (params.t + params.l + params.s) * n - 1)

        omega = (Mod(g, n) ** w * Mod(h, n) ** eta).x
        C = utils.hash(omega)
        c = C % (2 ** params.t)
        D1 = w + x * c
        D2 = eta + r * c

        if c * b <= D1 <= 2 ** (params.t + params.l) * b - 1:
            loop = False

    ext_li = {'w': int(w), 'eta': int(eta), 'omega': int(omega), 'int1': int(2 ** (params.t + params.l) * b - 1),
              'int2': -2 ** (params.t + params.l + params.s) * n + 1, 'int3': 2 ** (params.t + params.l + params.s) * n - 1,
              'int4': int(c * b)}

    if debug:
        print("\t ---Prove Interval: Debug--- \t")
        print("x: {}, n: {}, g: {}, h: {}, r: {}, b: {}, params.t: {}, params.l: {}, params.s: {}".format(x, n, g, h, r, b, params.t, params.l, params.s))
        print("w: {}, eta: {}, omega: {}, C: {}, D1: {}, D2: {}, c: {}\n".format(w, eta, omega, C, D1, D2, c))

    return proofLI(C, D1, D2, c), ext_li


def verifyLI_Flask(E, n, g, h, b, proof, params, debug=False):
    """
    Mismo funcionamiento que verifyLI, pero devolviendo parámetros extra para visualización.
    """
    cond1 = (proof.c * b <= proof.D1 <= 2 ** (params.t + params.l) * b - 1)
    cond2 = (proof.C == utils.hash((Mod(g, n) ** proof.D1 * Mod(h, n) ** proof.D2 * Mod(E, n) ** (-proof.c)).x))

    if debug:
        print("\t ---Verify Interval: Debug--- \t")
        print("E: {}, n: {}, g: {}, h: {}, b: {}, proof.C: {}, proof.D1: {}, proof.D2: {}, proof.c: {}, params.t: {}, params.l: {}, params.s: {}".format(E, n, g, h, b, proof.C, proof.D1, proof.D2, proof.c, params.t, params.l, params.s))
        print("Cond1: {}, {} <= {} <= {}".format(cond1, proof.c * b, proof.D1, 2 ** (params.t + params.l) * b - 1))
        print("Cond2: {}, {} = {}\n".format(cond2, proof.C, utils.hash((Mod(g, n) ** proof.D1 * Mod(h, n) ** proof.D2 * Mod(E, n) ** (-proof.c)).x)))

    ext = {'cond1': cond1, 'cond2': cond2, 'val1': int(proof.c * b), 'val2': int(2 ** (params.t + params.l) * b - 1),
           'val3': utils.hash((Mod(g, n) ** proof.D1 * Mod(h, n) ** proof.D2 * Mod(E, n) ** (-proof.c)).x), 'E': E}

    return (cond1 and cond2), ext
