import pygame as pg
from typing import Tuple

class Input:
    def __init__(self):
        self._prev_keys = pg.key.get_pressed()
        self._current_keys = self._prev_keys
        self._prev_mouse_buttons = pg.mouse.get_pressed()
        self._current_mouse = self._prev_mouse_buttons
        self._mouse_pos = pg.mouse.get_pos()
        
    def update(self) -> None:
        self._prev_keys = self._current_keys
        self._current_keys = pg.key.get_pressed()
        self._prev_mouse_buttons = self._current_mouse
        self._current_mouse = pg.mouse.get_pressed()
        self._mouse_pos = pg.mouse.get_pos()
        
    def is_key_down(self, key: int) -> bool:
        return self._current_keys[key]
    
    def was_key_pressed(self, key: int) -> bool:
        return self._current_keys[key] and not self._prev_keys[key]
    
    def was_key_released(self, key: int) -> bool:
        return not self._current_keys[key] and self._prev_keys[key]
    
    @property
    def mouse_pos(self) -> Tuple[int, int]:
        return self._mouse_pos
    
    def is_mouse_button_down(self, btn: int) -> bool:
        return self._current_mouse[btn]
    
    def was_mouse_button_pressed(self, btn: int) -> bool:
        return self._current_mouse[btn] and not self._current_mouse[btn]
    
    def was_mouse_button_released(self, btn: int) -> bool:
        return not self._current_mouse[btn] and self._current_mouse[btn]
    
# Quick manual test
if __name__ == "__main__":
    import time
    from ui.window import Window

    pg.init()
    win = Window(300, 200, "Input Test")
    input_mgr = Input()

    print("Press ESC to quit. Move mouse or press keys...")
    running = True
    while running and not win.should_close():
        win.tick(60)
        input_mgr.update()

        if input_mgr.was_key_pressed(pg.K_ESCAPE):
            print("Escape pressed, exiting.")
            running = False

        # Print mouse movement
        pos = input_mgr.mouse_pos
        print(f"Mouse at {pos}", end="\r")

        win.clear((30, 30, 30))
        win.present()

    win.destroy()
    pg.quit()