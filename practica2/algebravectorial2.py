import math

class Vector3D:
    def __init__(self, x, y, z): 
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):  
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):  
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):  
        return self.__mul__(scalar)  

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            raise ValueError("No se puede normalizar un vector cero")
        return Vector3D(self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)

    def __str__(self): 
        return f"({self.x}, {self.y}, {self.z})"

a = Vector3D(1, 2, 3)
b = Vector3D(4, 5, 6)

print("Suma de vectores:", a + b)  
print("Multiplicación por escalar:", 2 * a) 
print("Longitud de a:", a.magnitude())  
print("Normal de a:", a.normalize())  
print("Producto escalar:", a.dot(b)) 
print("Producto vectorial:", a.cross(b))  
