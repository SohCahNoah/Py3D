from ui.window import Window

def main():
    width, height = 400, 300
    win = Window(width, height, "Window/Buffer Test")

    while not win.should_close():
        # 1) Handle events & cap FPS
        dt = win.tick(60)

        # 2) Clear to a bluish color
        win.clear((50, 50, 100))

        # 3) Draw something directly into the framebuffer:
        #    here we'll paint a red diagonal line
        for i in range(min(width, height)):
            win.framebuffer[i, i] = (255, 0, 0)

        # 4) Present to screen
        win.present()

    win.destroy()

if __name__ == "__main__":
    main()