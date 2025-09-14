from core.vector import Vector3

class Mesh:
    def __init__(
        self,
        vertices: list[Vector3],
        faces: list[tuple[int, int, int]],
        colors: list[tuple[int, int, int]]
    ):
        assert len(faces) == len(colors), "One color per face is required"
        self.vertices = vertices
        self.faces = faces
        self.colors = colors
        
    @staticmethod
    def create_cube(size: float = 1.0) -> "Mesh":
        h = size / 2.0
        vertices = [
            Vector3(-h, -h, -h),  # 0
            Vector3( h, -h, -h),  # 1
            Vector3( h,  h, -h),  # 2
            Vector3(-h,  h, -h),  # 3
            Vector3(-h, -h,  h),  # 4
            Vector3( h, -h,  h),  # 5
            Vector3( h,  h,  h),  # 6
            Vector3(-h,  h,  h),  # 7
        ]
        
        faces = [
            # back (z = -h)
            (0, 1, 2), (0, 2, 3),
            # front (z = +h)
            (5, 4, 7), (5, 7, 6),
            # left (x = -h)
            (4, 0, 3), (4, 3, 7),
            # right (x = +h)
            (1, 5, 6), (1, 6, 2),
            # bottom (y = -h)
            (4, 5, 1), (4, 1, 0),
            # top (y = +h)
            (3, 2, 6), (3, 6, 7),
        ]
        
        face_colors = [
            (255,   0,   0),  # back: red
            (255,   0,   0),
            (  0, 255,   0),  # front: green
            (  0, 255,   0),
            (  0,   0, 255),  # left: blue
            (  0,   0, 255),
            (255, 255,   0),  # right: yellow
            (255, 255,   0),
            (255,   0, 255),  # bottom: magenta
            (255,   0, 255),
            (  0, 255, 255),  # top: cyan
            (  0, 255, 255),
        ]
        
        return Mesh(vertices, faces, face_colors)