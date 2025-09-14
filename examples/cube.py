# examples/rotating_cube.py
import math
import pygame

from core.vector       import Vector3
from core.quaternion   import Quaternion
from ui.window         import Window
from ui.input          import Input
from render.rasterizer import Rasterizer
from scene.mesh        import Mesh
from scene.camera      import Camera

# ---- settings ----
ENABLE_CULLING = True       # robust culling (can flip inequality once if your stack inverts)
CLEAR_COLOR    = (20, 20, 20)

DRAW_EDGES     = True
DRAW_VERTS     = True
EDGE_COLOR     = (255, 255, 255)
EDGE_WIDTH     = 1
VERT_COLOR     = (255, 255, 255)
VERT_RADIUS    = 2
# ------------------

def quat_mul(a: Quaternion, b: Quaternion) -> Quaternion:
    return Quaternion(
        a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z,
        a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
        a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
        a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w,
    )

def quat_conj(q: Quaternion) -> Quaternion:
    return Quaternion(q.w, -q.x, -q.y, -q.z)

def rotate_vec(q: Quaternion, v: Vector3) -> Vector3:
    # v' = q * (0,v) * q*
    vq = Quaternion(0.0, v.x, v.y, v.z)
    rq = quat_mul(quat_mul(q, vq), quat_conj(q))
    return Vector3(rq.x, rq.y, rq.z)

def project_view_to_screen(vc: Vector3, fov_rad: float, aspect: float, near: float, far: float, w: int, h: int):
    """
    Manual perspective. Camera looks down -Z; visible points have vc.z < -near.
    """
    z = vc.z
    if z >= -near:
        return None

    f = 1.0 / math.tan(0.5 * fov_rad)

    x_ndc = (vc.x * f / aspect) / (-z)
    y_ndc = (vc.y * f)          / (-z)

    # OpenGL-like z in [-1,1]
    A = (far + near) / (near - far)
    B = (2.0 * far * near) / (near - far)
    z_ndc = (A * z + B) / (-z)

    x = (x_ndc * 0.5 + 0.5) * (w - 1)
    y = (1.0 - (y_ndc * 0.5 + 0.5)) * (h - 1)
    return Vector3(x, y, z_ndc)

def main():
    width, height = 800, 600
    win    = Window(width, height, "Rotating Cube (wireframe overlay)")
    raster = Rasterizer(width, height)
    inp    = Input()

    pygame.font.init()
    font = pygame.font.SysFont(None, 20)

    cube = Mesh.create_cube(1.0)

    cam = Camera(
        position=Vector3(0, 0, 5),
        target=  Vector3(0, 0, 0),
        up=      Vector3(0, 1, 0),
        fov=     math.radians(60),
        aspect=  width / height,
        near=    0.1,
        far=     100.0,
    )

    V = cam.get_view_matrix()  # fixed camera
    ax = ay = az = 0.0

    fps_t = 0.0
    fps_n = 0
    fps   = 0.0

    while not win.should_close():
        dt = win.tick(60)
        inp.update()
        if inp.was_key_pressed(pygame.K_ESCAPE):
            break

        # FPS
        fps_t += dt; fps_n += 1
        if fps_t >= 0.5:
            fps = fps_n / fps_t; fps_t = 0.0; fps_n = 0

        # rotation
        ax += dt * math.radians(30)
        ay += dt * math.radians(45)
        az += dt * math.radians(60)
        hx, hy, hz = 0.5*ax, 0.5*ay, 0.5*az
        qx = Quaternion(math.cos(hx), math.sin(hx), 0.0, 0.0)
        qy = Quaternion(math.cos(hy), 0.0, math.sin(hy), 0.0)
        qz = Quaternion(math.cos(hz), 0.0, 0.0, math.sin(hz))
        q  = quat_mul(qz, quat_mul(qy, qx))

        win.clear(CLEAR_COLOR)

        total = len(cube.faces)
        culled = off = drawn = 0

        # Collect overlay primitives for this frame
        edges_to_draw = []   # list[( (x1,y1), (x2,y2) )]
        verts_to_draw = []   # list[(x,y)]

        for f_ix, (i0, i1, i2) in enumerate(cube.faces):
            # object -> rotate (world) -> view
            v0w = rotate_vec(q, cube.vertices[i0])
            v1w = rotate_vec(q, cube.vertices[i1])
            v2w = rotate_vec(q, cube.vertices[i2])

            v0 = V.transform_point(v0w)
            v1 = V.transform_point(v1w)
            v2 = V.transform_point(v2w)

            # robust back-face: normal·to_camera <= 0 ⇒ back-facing
            e1 = v1 - v0
            e2 = v2 - v0
            n  = e1.cross(e2)                       # view-space normal
            to_cam = Vector3(-v0.x, -v0.y, -v0.z)   # camera at origin in view space
            facing = n.x*to_cam.x + n.y*to_cam.y + n.z*to_cam.z
            if ENABLE_CULLING and facing <= 0.0:
                culled += 1
                continue

            # project
            p0 = project_view_to_screen(v0, cam.fov, cam.aspect, cam.near, cam.far, width, height)
            p1 = project_view_to_screen(v1, cam.fov, cam.aspect, cam.near, cam.far, width, height)
            p2 = project_view_to_screen(v2, cam.fov, cam.aspect, cam.near, cam.far, width, height)
            if (p0 is None) or (p1 is None) or (p2 is None):
                off += 1
                continue

            xs = (p0.x, p1.x, p2.x); ys = (p0.y, p1.y, p2.y)
            if (max(xs) < 0) or (min(xs) > width-1) or (max(ys) < 0) or (min(ys) > height-1):
                off += 1
                continue

            # filled triangle
            raster.draw_triangle(p0, p1, p2, cube.colors[f_ix], win.framebuffer, win.depthbuffer)
            drawn += 1

            # overlay edges & vertices for this triangle
            if DRAW_EDGES:
                edges_to_draw.append(((p0.x, p0.y), (p1.x, p1.y)))
                edges_to_draw.append(((p1.x, p1.y), (p2.x, p2.y)))
                edges_to_draw.append(((p2.x, p2.y), (p0.x, p0.y)))
            if DRAW_VERTS:
                verts_to_draw.extend([(p0.x, p0.y), (p1.x, p1.y), (p2.x, p2.y)])

        # present filled framebuffer
        surf = pygame.surfarray.make_surface(win.framebuffer.swapaxes(0, 1))
        win.screen.blit(surf, (0, 0))

        # draw wireframe overlay on top
        if DRAW_EDGES:
            for (x1, y1), (x2, y2) in edges_to_draw:
                pygame.draw.line(win.screen, EDGE_COLOR, (int(x1), int(y1)), (int(x2), int(y2)), EDGE_WIDTH)
        if DRAW_VERTS:
            for (x, y) in verts_to_draw:
                pygame.draw.circle(win.screen, VERT_COLOR, (int(x), int(y)), VERT_RADIUS)

        # HUD
        hud = f"FPS {fps:.1f} | total {total} culled {culled} off {off} drawn {drawn} | cull={'on' if ENABLE_CULLING else 'off'}"
        win.screen.blit(font.render(hud, True, (255,255,255)), (10,10))

        pygame.display.flip()

    win.destroy()

if __name__ == "__main__":
    main()
