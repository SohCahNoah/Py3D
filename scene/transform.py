from typing import Optional
from core.vector import Vector3
from core.matrix import Matrix4
from core.quaternion import Quaternion

class Transform:
    def __init__(
        self,
        position: Optional[Vector3] = None,
        rotation: Optional[Quaternion] = None,
        scale: Optional[Vector3] = None,
    ):
        self.position = position or Vector3(0.0, 0.0, 0.0)
        self.rotation = rotation or Quaternion(1.0, 0.0, 0.0, 0.0)
        self.scale = scale or Vector3(1.0, 1.0, 1.0)
    
    def matrix(self) -> Matrix4:
        T = Matrix4.translation(
            self.position.x,
            self.position.y,
            self.position.z
        )
        
        w, x, y, z = (
            self.rotation.w,
            self.rotation.x,
            self.rotation.y,
            self.rotation.z
        )
        
        xx, yy, zz = x*x, y*y, z*z
        xy, xz, yz = x*y, x*z, y*z
        wx, wy, wz = w*x, w*y, w*z
        
        rot = [
            [1 - 2*(yy + zz), 2*(xy - wz),     2*(xz + wy),     0.0],
            [2*(xy + wz),     1 - 2*(xx + zz), 2*(yz - wx),     0.0],
            [2*(xz - wy),     2*(yz + wx),     1 - 2*(xx + yy), 0.0],
            [0.0,             0.0,             0.0,             1.0]
        ]
        R = Matrix4(rot)
        
        S = Matrix4.scale(
            self.scale.x,
            self.scale.y,
            self.scale.z
        )
        
        return T @ R @ S
    
    def __repr__(self):
        return (
            f"Transform(\n"
            f"  position={self.position},\n"
            f"  rotation={self.rotation},\n"
            f"  scale={self.scale}\n"
            f")"
        )