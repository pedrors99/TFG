import math
from dataclasses import dataclass

from mod import Mod
from with_tolerance import proveWT, verifyWT, proofWT


@dataclass
class paramsSD:
    t: int
    l: int
    s: int


@dataclass
class proofSD:
    E_: int
    proof_wt: proofWT


def proveSD(x, n, g, h, r, a, b, E, params, debug=False):
    T = 2 * (params.t + params.l + 1) + abs(b - a)

    x_ = 2 ** T * x
    r_ = 2 ** T * r
    E_ = (Mod(E, n) ** (2 ** T)).x

    a_ = int(2 ** T * a - 2 ** ((params.t + params.l + T) / 2 - 1) * math.floor(math.sqrt(b - a)))
    b_ = int(2 ** T * b + 2 ** ((params.t + params.l + T) / 2 - 1) * math.floor(math.sqrt(b - a)))

    proof_wt = proveWT(x_, n, g, h, r_, a_, b_, E_, params, debug)
    return proofSD(E_, proof_wt)


def verifySD(n, g, h, a, b, E, proof, params, debug=False):
    T = 2 * (params.t + params.l + 1) + abs(b - a)
    if proof.E_ == (E ** (2 ** T)):
        return verifyWT(n, g, h, b, proof.proof_wt, params, debug)
    else:
        return False