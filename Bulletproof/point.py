class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, n):
        self.x *= n
        self.y *= n
