import numpy as np
import math

class Vector3:
    __slots__ = ("_v",)
    
    def __init__(self, x: float, y: float, z: float):
        self._v = np.array([x,y,z], dtype=float)
    
    @property
    def x(self) -> float:
        return self._v[0]
    
    @property
    def y(self) -> float:
        return self._v[1]
    
    @property
    def z(self) -> float:
        return self._v[2]
    
    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(*(self._v + other._v))
    
    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(*(self._v - other._v))
    
    def __mul__(self, scalar: float) -> "Vector3":
        return Vector3(*(self._v * scalar))
    
    def dot(self, other: "Vector3") -> float:
        return float(self._v @ other._v)
    
    def cross(self, other: "Vector3") -> "Vector3":
        return Vector3(*np.cross(self._v, other._v))
    
    def length(self) -> float:
        x, y, z = self._v
        return math.sqrt(x*x + y*y + z*z)
    
    def normalized(self) -> "Vector3":
        norm = self.length()
        if norm:
            return Vector3(*(self._v / norm))
        return Vector3(0.0, 0.0, 0.0)
    
    def to_array(self) -> np.ndarray:
        return self._v.copy()
    
    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"