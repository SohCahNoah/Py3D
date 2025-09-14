from ui.window import Window
from core.vector import Vector3
from render.rasterizer import Rasterizer

def main():
    # 1) Create a window + buffers
    width, height = 400, 300
    win = Window(width, height, "Rasterizer Test")

    # 2) Instantiate the rasterizer
    r = Rasterizer(width, height)

    # 3) Define a single triangle in screen space (z=0.5)
    v0 = Vector3( 50,  50, 0.5)
    v1 = Vector3(350,  50, 0.5)
    v2 = Vector3(200, 250, 0.5)
    color = (200, 100,  50)  # RGB

    # 4) Main loop: clear, draw, present
    while not win.should_close():
        dt = win.tick(60)
        win.clear((20, 20, 20))  # dark gray background

        r.draw_triangle(v0, v1, v2, color,
                        win.framebuffer, win.depthbuffer)

        win.present()

    win.destroy()

if __name__ == "__main__":
    main()