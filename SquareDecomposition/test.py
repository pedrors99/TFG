import random
import numpy as np

from tqdm import tqdm
from mod import Mod
import matplotlib.pyplot as plt
import seaborn as sns
from with_tolerance import paramsWT, proveWT, verifyWT


def addError(n, g, h, b, proof):
    size = 29
    error = np.random.choice([0, 1], size, p=[0.75, 0.25])
    while np.all(error == 0):
        error = np.random.choice([0, 1], size, p=[0.75, 0.25])
    error_value = np.random.randint(low=-n, high=n, size=size)

    if error[0]:
        g = (g + error_value[0]) % n
    if error[1]:
        h = (h + error_value[1]) % n
    if error[2]:
        b = (b + error_value[2]) % n

    if error[3]:
        proof.Ea = (proof.Ea + error_value[3]) % n
    if error[4]:
        proof.Ea1 = (proof.Ea1 + error_value[4]) % n
    if error[5]:
        proof.Ea2 = (proof.Ea2 + error_value[5]) % n

    if error[6]:
        proof.Eb = (proof.Eb + error_value[6]) % n
    if error[7]:
        proof.Eb1 = (proof.Eb1 + error_value[7]) % n
    if error[8]:
        proof.Eb2 = (proof.Eb2 + error_value[8]) % n

    if error[9]:
        proof.proof_sa.E = (proof.proof_sa.E + error_value[9]) % n
    if error[10]:
        proof.proof_sa.F = (proof.proof_sa.F + error_value[10]) % n
    if error[11]:
        proof.proof_sa.proof_ss.c = (proof.proof_sa.proof_ss.c + error_value[11]) % n
    if error[12]:
        proof.proof_sa.proof_ss.D = (proof.proof_sa.proof_ss.D + error_value[12]) % n
    if error[13]:
        proof.proof_sa.proof_ss.D1 = (proof.proof_sa.proof_ss.D1 + error_value[13]) % n
    if error[14]:
        proof.proof_sa.proof_ss.D2 = (proof.proof_sa.proof_ss.D2 + error_value[14]) % n

    if error[15]:
        proof.proof_sb.E = (proof.proof_sb.E + error_value[15]) % n
    if error[16]:
        proof.proof_sb.F = (proof.proof_sb.F + error_value[16]) % n
    if error[17]:
        proof.proof_sb.proof_ss.c = (proof.proof_sb.proof_ss.c + error_value[17]) % n
    if error[18]:
        proof.proof_sb.proof_ss.D = (proof.proof_sb.proof_ss.D + error_value[18]) % n
    if error[19]:
        proof.proof_sb.proof_ss.D1 = (proof.proof_sb.proof_ss.D1 + error_value[19]) % n
    if error[20]:
        proof.proof_sb.proof_ss.D2 = (proof.proof_sb.proof_ss.D2 + error_value[20]) % n

    if error[21]:
        proof.proof_lia.c = (proof.proof_lia.c + error_value[21]) % n
    if error[22]:
        proof.proof_lia.D1 = (proof.proof_lia.D1 + error_value[22]) % n
    if error[23]:
        proof.proof_lia.D2 = (proof.proof_lia.D2 + error_value[23]) % n
    if error[24]:
        proof.proof_lia.C = (proof.proof_lia.C + error_value[24]) % n

    if error[25]:
        proof.proof_lib.c = (proof.proof_lib.c + error_value[25]) % n
    if error[26]:
        proof.proof_lib.D1 = (proof.proof_lib.D1 + error_value[26]) % n
    if error[27]:
        proof.proof_lib.D2 = (proof.proof_lib.D2 + error_value[27]) % n
    if error[28]:
        proof.proof_lib.C = (proof.proof_lib.C + error_value[28]) % n

    return g, h, b, proof


if __name__ == '__main__':
    t = 5
    l = 3
    s = 4

    n = 1213

    ns = [13, 59, 157, 331, 647, 991, 1223, 1607, 2543, 4391, 7457, 13009, 19381, 26891, 40031]

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for n in tqdm(ns, position=0, desc="Total Progress", bar_format='{l_bar}{bar:20}{r_bar}', colour='green'):
        for i in tqdm(range(200), position=1, desc="Progress with n = {}".format(n), bar_format='{l_bar}{bar:20}{r_bar}', colour='green', leave=False):
            a = random.randint(0, n-1)
            b = random.randint(a+1, n)

            x = random.randint(a, b)

            g = random.randint(1, n-1)
            h = (Mod(g, n) ** random.randint(0, 10)).x

            r = random.randint(-2 ** s * n - 1, 2 ** s * n + 1)
            E = (Mod(g, n) ** x * Mod(h, n) ** r).x

            params = paramsWT(t, l, s)

            proof = proveWT(x, n, g, h, r, a, b, E, params)
            result = verifyWT(n, g, h, b, proof, params)

            if result:
                tp += 1
            else:
                tp += 1

            g, h, b, proof = addError(n, g, h, b, proof)

            result = verifyWT(n, g, h, b, proof, params)

            if result:
                fp += 1
            else:
                tn += 1

    print("\nTrue Positives:  {}\t\tFalse Positives: {}\nFalse Negatives: {}\t\tTrue Negatives:  {}".format(tp, fp, fn, tn))
    data = [[tp, fp], [fn, tn]]
    ax = sns.heatmap(data, annot=True, cmap='Blues', fmt='d', cbar=False)
    ax.axes.set_xticklabels(["True", "False"])
    ax.axes.set_yticklabels(["True", "False"])
    plt.title("Confusion matrix")
    plt.xlabel("Number of Expected Results")
    plt.ylabel("Number of Obtained Results")
    plt.show()

