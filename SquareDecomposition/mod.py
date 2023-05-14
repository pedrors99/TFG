import numpy as np


class Mod:
    def __init__(self, x, p):
        self.x = x % p
        self.p = p

    def __add__(self, y):
        if isinstance(y, int):
            return Mod(self.x + y, self.p)
        if isinstance(y, Mod):
            assert(self.p == y.p)
            return Mod((self.x + y.x), self.p)
        else:
            self.assertFalse(True)

    def __sub__(self, y):
        if isinstance(y, int):
            return Mod(self.x - y, self.p)
        if isinstance(y, Mod):
            assert(self.p == y.p)
            return Mod((self.x - y.x), self.p)
        else:
            self.assertFalse(True)

    def __neg__(self):
        return Mod(self.p - self.x, self.p)

    def __eq__(self, y):
        return (self.x == y.x) and (self.p == y.p)

    def __mul__(self, y):
        if isinstance(y, int):
            return Mod(self.x * y, self.p)
        if isinstance(y, Mod):
            assert(self.p == y.p)
            return Mod((self.x * y.x), self.p)
        else:
            self.assertFalse(True)

    def inverse(self):
        q = np.empty(0)
        r = np.array([self.p, self.x])
        u = np.array([1, 0])
        v = np.array([0, 1])

        while True:
            q = np.append(q, int(r[len(r) - 2] / r[len(r) - 1]))
            r = np.append(r, int(r[len(r) - 2] % r[len(r) - 1]))
            if r[len(r)-1] == 0:
                break
            u = np.append(u, int(u[len(u)-2] - q[len(q)-1] * u[len(u)-1]))
            v = np.append(v, int(v[len(v)-2] - q[len(q)-1] * v[len(v)-1]))

        assert(r[len(r)-2] == 1)
        return Mod(v[len(v)-1], self.p)

    def __pow__(self, n):
        if self.x == 0 or self.x == 1:
            return Mod(self.x, self.p)
        else:
            if n == 0:
                return Mod(1, self.p)
            elif n < 0:
                self.x = self.inverse().x
                n = -n

            value = self.x

            for i in range(1, n):
                self.x = (self.x * value) % self.p
                if self.x == 1:
                    return Mod(value, self.p) ** (n % (i+1))

            return Mod(self.x, self.p)

    def __str__(self):
        return "{} (mod {})".format(self.x, self.p)