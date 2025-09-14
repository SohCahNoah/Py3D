from core.matrix import Matrix4
from core.vector import Vector3

class Camera:
    def __init__(
        self,
        position: Vector3,
        target: Vector3,
        up: Vector3,
        fov: float,
        aspect: float,
        near: float,
        far: float,
    ):
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        
    def get_view_matrix(self) -> Matrix4:
        forward = (self.target - self.position).normalized()
        right = forward.cross(self.up).normalized()
        up_true = right.cross(forward)

        m = [
            [ right.x,  right.y,  right.z, -right.dot(self.position) ],
            [ up_true.x,up_true.y,up_true.z,-up_true.dot(self.position) ],
            [-forward.x,-forward.y,-forward.z, forward.dot(self.position)],
            [ 0.0,       0.0,       0.0,       1.0                    ],
        ]
        return Matrix4(m)

    def get_projection_matrix(self) -> Matrix4:
        return Matrix4.perspective(self.fov, self.aspect, self.near, self.far)