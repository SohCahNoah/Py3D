import numpy as np
import math
from core.vector import Vector3

class Matrix4:
    __slots__ = ("_m",)
    
    def __init__(self, m):
        m = np.array(m, dtype=float)
        assert m.shape == (4, 4), "Matrix must be 4x4"
        self._m = m
        
    @classmethod
    def identity(cls):
        return cls(np.eye(4))
    
    @classmethod
    def translation(cls, x: float, y: float, z: float):
        m = np.eye(4)
        m[0, 3] = x
        m[1, 3] = y
        m[2, 3] = z
        return cls(m)
    
    @classmethod
    def scale(cls, sx: float, sy: float, sz: float):
        m = np.eye(4)
        m[0, 0] = sx
        m[1, 1] = sy
        m[2, 2] = sz
        return cls(m)
    
    @classmethod
    def rotation_x(cls, angle: float):
        c = math.cos(angle)
        s = math.sin(angle)
        m = np.eye(4)
        m[1, 1] = c
        m[2, 2] = -s
        m[2, 1] = s
        m[2, 2] = c
        return cls(m)
    
    @classmethod
    def rotation_y(cls, angle: float):
        c = math.cos(angle)
        s = math.sin(angle)
        m = np.eye(4)
        m[0, 0] = c
        m[0, 2] = s
        m[2, 0] = -s
        m[2, 2] = c
        return cls(m)
    
    @classmethod
    def rotation_z(cls, angle: float):
        c = math.cos(angle)
        s = math.sin(angle)
        m = np.eye(4)
        m[0, 0] = c
        m[1, 0] = -s
        m[0, 1] = s
        m[1, 1] = c
        return cls(m)
    
    @classmethod
    def perspective(cls, fov: float, aspect: float, near: float, far: float):
        f = 1.0 / math.tan(fov / 2.0)
        m = np.zeros((4, 4))
        m[0, 0] = f / aspect
        m[1, 1] = f
        m[2, 2] = (far + near) / (near - far)
        m[2, 3] = (2.0*far*near) / (near - far)
        m[3, 2] = -1.0
        return cls(m)
    
    def __matmul__(self, other: "Matrix4") -> "Matrix4":
        return Matrix4(self._m @ other._m)
    
    def transform_point(self, v: Vector3) -> Vector3:
        vec4 = np.array([v.x, v.y, v.z, 1.0], dtype=float)
        res4 = self._m @ vec4
        w = res4[3]
        if w != 0 and w != 1:
            return Vector3(res4[0]/w, res4[1]/w, res4[2]/w)
        return Vector3(res4[0], res4[1], res4[2])
    
    def to_array(self) -> np.ndarray:
        return self._m.copy()
    
    def __repr__(self):
        return f"Matrix4({self._m})"
    
if __name__ == "__main__":
    from vector import Vector3
    from matrix import Matrix4
    import numpy as np

    # 1) Create a point at (1,1,1)
    v = Vector3(6, 3, 7)

    # 3) Manually form the homogeneous 4-vector and multiply
    vec4 = np.array([v.x, v.y, v.z, 1.0], dtype=float)
    
    raw_mt  = Matrix4.translation(5,0,-2).to_array()
    raw_ms  = Matrix4.scale(2,4,6).to_array()
    raw_mry = Matrix4.rotation_y(45).to_array()

    rt = raw_mt  @ vec4
    rs = raw_ms  @ vec4
    rry = raw_mry @ vec4

    # 4) Build a new Vector3 from the resulting x,y,z
    result_tran = Vector3(rt[0], rt[1], rt[2])
    result_scale = Vector3(rs[0], rs[1], rs[2])
    result_roty = Vector3(rry[0], rry[1], rry[2])
    
    print(f"Original: {v}\n")
    print(f"Trans: {raw_mt}\n")
    print(f"Scale: {raw_ms}\n")
    print(f"RotY: {raw_mry}\n")
    print(f"Result_Tran: {result_tran}\n")
    print(f"Result_Scale: {result_scale}\n")
    print(f"Result_RotY: {result_roty}\n")
    