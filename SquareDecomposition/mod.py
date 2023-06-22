import numpy as np


class Mod:
    """
    Clase que representa un elemento en un módulo.
    """
    def __init__(self, x, p):
        self.x = x % p
        self.p = p

    def __add__(self, y):
        """
        Suma de dos elementos.

        :param y: Elemento a sumar.
        :return: Resultado de la suma, x+y (mod n)..
        """
        if isinstance(y, int):
            return Mod(self.x + y, self.p)
        if isinstance(y, Mod):
            assert(self.p == y.p)
            return Mod((self.x + y.x), self.p)
        else:
            self.assertFalse(True)

    def __sub__(self, y):
        """
        Diferencia de dos elementos.

        :param y: Elemento a restar.
        :return: Resultado de la diferencia, x-y (mod n)..
        """
        if isinstance(y, int):
            return Mod(self.x - y, self.p)
        if isinstance(y, Mod):
            assert(self.p == y.p)
            return Mod((self.x - y.x), self.p)
        else:
            self.assertFalse(True)

    def __neg__(self):
        """
        Cálculo de opuestos.

        :return: Opuesto, -x (mod n)..
        """
        return Mod(self.p - self.x, self.p)

    def __eq__(self, y):
        """
        Igualdad en valor entre dos elementos.

        :param y: Elemento a comparar.
        :return: Resultado de la igualdad, x==y (mod n).
        """
        return (self.x == y.x) and (self.p == y.p)

    def __mul__(self, y):
        """
        Multiplicación de dos elementos.

        :param y: Elemento a multiplicar.
        :return: Resultado de la multiplicación, x*y (mod n).
        """
        if isinstance(y, int):
            return Mod(self.x * y, self.p)
        if isinstance(y, Mod):
            assert(self.p == y.p)
            return Mod((self.x * y.x), self.p)
        else:
            self.assertFalse(True)

    def inverse(self):
        """
        Cálculo de inversos utilizando el algoritmo extendido de Euclides.

        :return: Inverso de x, x^(-1) (mod n).
        """
        if self.x != 0:
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

            assert(r[len(r)-2] == 1), "Error al calcular el inverso de {}".format(self)
            return Mod(v[len(v)-1], self.p)
        else:
            return self

    def __pow__(self, n):
        """
        Cálculo de potencias.

        :param n: Exponente.
        :return: Resultado de la potencia, x^n (mod n).
        """
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
        """
        Función para imprimir un objeto de la clase por pantalla.

        :return: String con los valores del objeto.
        """
        return "{} (mod {})".format(self.x, self.p)
