# render/rasterizer.py

import numpy as np
import math

class Rasterizer:
    __slots__ = ("width", "height")

    def __init__(self, width: int, height: int):
        self.width  = width
        self.height = height

    @staticmethod
    def edge(ax: float, ay: float,
             bx: float, by: float,
             px: float, py: float) -> float:
        return (px - ax) * (by - ay) - (py - ay) * (bx - ax)

    def draw_triangle(
        self,
        v0, v1, v2,
        color: tuple[int, int, int],
        framebuffer: np.ndarray,
        depthbuffer: np.ndarray,
    ) -> None:
        v0x, v0y, v0z = v0.x, v0.y, v0.z
        v1x, v1y, v1z = v1.x, v1.y, v1.z
        v2x, v2y, v2z = v2.x, v2.y, v2.z

        # Compute full 2D area (we no longer cull here)
        area = self.edge(v0x, v0y, v1x, v1y, v2x, v2y)
        if abs(area) < 1e-6:
            return  # completely degenerate

        inv_area = 1.0 / area

        # Bounding box
        min_x = max(int(math.floor(min(v0x, v1x, v2x))), 0)
        max_x = min(int(math.ceil (max(v0x, v1x, v2x))), self.width  - 1)
        min_y = max(int(math.floor(min(v0y, v1y, v2y))), 0)
        max_y = min(int(math.ceil (max(v0y, v1y, v2y))), self.height - 1)

        # Raster loop
        for y in range(min_y, max_y + 1):
            py = y + 0.5
            for x in range(min_x, max_x + 1):
                px = x + 0.5

                w0 = self.edge(v1x, v1y, v2x, v2y, px, py)
                w1 = self.edge(v2x, v2y, v0x, v0y, px, py)
                w2 = self.edge(v0x, v0y, v1x, v1y, px, py)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    w0 *= inv_area
                    w1 *= inv_area
                    w2 *= inv_area

                    z = w0 * v0z + w1 * v1z + w2 * v2z
                    if z < depthbuffer[y, x]:
                        depthbuffer[y, x] = z
                        framebuffer[y, x] = color
