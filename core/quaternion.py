import math
import numpy as np
from core.vector import Vector3
from core.matrix import Matrix4

class Quaternion:
    __slots__ = ("w", "x", "y", "z")

    def __init__(self, w: float, x: float, y: float, z: float):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def from_axis_angle(cls, axis: Vector3, angle_degrees: float) -> "Quaternion":
        # Compute half-angle
        theta = math.radians(angle_degrees) / 2
        s = math.sin(theta)
        # Ensure axis is unit-length
        axis_n = axis.normalized()
        q = cls(
            math.cos(theta),
            axis_n.x * s,
            axis_n.y * s,
            axis_n.z * s
        )
        # Normalize to correct any drift
        return q.normalized()

    def normalized(self) -> "Quaternion":
        norm = math.sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)
        return Quaternion(self.w / norm,
                          self.x / norm,
                          self.y / norm,
                          self.z / norm)

    def conjugate(self) -> "Quaternion":
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        # Raw Hamilton product, no normalization here
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

    def to_matrix4(self) -> Matrix4:
        w, x, y, z = self.w, self.x, self.y, self.z
        # Build equivalent 4×4 rotation matrix
        return Matrix4(np.array([
            [1 - 2*(y*y + z*z),     2*(x*y - z*w),     2*(x*z + y*w), 0],
            [    2*(x*y + z*w), 1 - 2*(x*x + z*z),     2*(y*z - x*w), 0],
            [    2*(x*z - y*w),     2*(y*z + x*w), 1 - 2*(x*x + y*y), 0],
            [                0,                 0,                 0, 1]
        ]))

    def rotate_vector(self, v: Vector3) -> Vector3:
        # Rotate a Vector3: q * (0, v) * q⁻¹
        qv = Quaternion(0, v.x, v.y, v.z)
        qr = self * qv * self.conjugate()
        return Vector3(qr.x, qr.y, qr.z)

    def __repr__(self) -> str:
        return f"Quaternion(w={self.w:.3f}, x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"

if __name__ == "__main__":
    from vector import Vector3
    from quaternion import Quaternion
    import numpy as np

    # 1) Create a quaternion: rotate 45° about the Y axis
    q = Quaternion.from_axis_angle(Vector3(0, 1, 0), 45)

    # 2) Define your original vector
    v = Vector3(6, 3, 7)

    # 3) Rotate via quaternion sandwich
    v_rot_q = q.rotate_vector(v)

    # 4) Rotate via the equivalent 4×4 matrix
    raw_mat = q.to_matrix4().to_array()                        # numpy.ndarray (4×4)
    vec4    = np.array([v.x, v.y, v.z, 1.0], dtype=float)      # homogeneous vector
    v_rot_m_arr = raw_mat @ vec4                               # ndarray @ ndarray
    v_rot_m     = Vector3(v_rot_m_arr[0], v_rot_m_arr[1], v_rot_m_arr[2])

    # 5) Print results
    print("Quaternion:", q)
    print("Rotated by quat:", v_rot_q)
    print("Rotated by mat4:", v_rot_m)
