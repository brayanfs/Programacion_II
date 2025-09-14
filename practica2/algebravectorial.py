import math

class Vector:
    def __init__(self, x, y, z):  
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):  
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):  
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):  
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __repr__(self):  
        return f"Vector({self.x}, {self.y}, {self.z})"

class AlgebraVectorial:
    def __init__(self, a, b): 
        self.a = a
        self.b = b

    def perpendicular(self, method='dot'):
        if method == 'dot':
            return self.a.dot(self.b) == 0
        elif method == 'magnitude':
            return (self.a + self.b).magnitude() ** 2 == self.a.magnitude() ** 2 + self.b.magnitude() ** 2
        elif method == 'add_sub':
            return (self.a + self.b).magnitude() == (self.a - self.b).magnitude()
        elif method == 'sub_add':
            return (self.a - self.b).magnitude() == (self.b - self.a).magnitude()

    def paralela(self, method='cross'):
        if method == 'cross':
            return self.a.cross(self.b).magnitude() == 0
        elif method == 'scalar':
            
            try:
                return self.a.x / self.b.x == self.a.y / self.b.y == self.a.z / self.b.z
            except ZeroDivisionError:
                return False

    def proyeccion(self):
        scalar = self.a.dot(self.b) / self.b.magnitude() ** 2
        return self.b * scalar

    def componente(self):
        return self.a.dot(self.b) / self.b.magnitude()


a = Vector(1, 2, 3)
b = Vector(4, 5, 6)

algebra = AlgebraVectorial(a, b)

print("¿Son perpendiculares?", algebra.perpendicular())
print("¿Son paralelos?", algebra.paralela())
print("Proyección de a sobre b:", algebra.proyeccion())

print("Componente de a en b:", algebra.componente())
