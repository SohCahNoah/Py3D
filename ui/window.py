import pygame as pg
import numpy as np

class Window:
    def __init__(self, width: int, height: int, title: str = "3D Engine"):
        pg.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.framebuffer = np.zeros((height, width, 3), dtype=np.uint8)
        self.depthbuffer = np.full((height, width), np.inf, dtype=np.float32)
        self._should_close = False
        
    def tick(self, fps: int = 60) -> float:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._should_close = True
    
        dt_ms = self.clock.tick(fps)
        return dt_ms / 1000.0
    
    def should_close(self) -> bool:
        return self._should_close
    
    def clear(self, color: tuple[int, int, int] = (0, 0, 0)):
        self.framebuffer[:] = color
        self.depthbuffer[:] = np.inf
        
    def present(self):
        surf = pg.surfarray.make_surface(self.framebuffer.swapaxes(0,1))
        self.screen.blit(surf, (0, 0))
        pg.display.flip()
        
    def destroy(self):
        pg.quit()