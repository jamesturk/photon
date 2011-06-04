from photon import init, InitFlags, mouse, video, keyboard
from photon.events import poll_event, EventType, WindowEventType

def main():
    init(InitFlags.EVERYTHING)

    w = video.Window('mouse test', 10, 10, 300, 300)
    running = True
    points = []

    while running:

        # event loop
        while True:
            event = poll_event()
            if not event:
                break
            elif event.type == EventType.QUIT:
                running = False
            elif event.type == EventType.WINDOWEVENT:
                if event.window.event == WindowEventType.CLOSE:
                    running = False
            elif event.type == EventType.MOUSEBUTTONDOWN:
                pass
            elif event.type == EventType.MOUSEBUTTONUP:
                x, y, buttons = mouse.get_mouse_state()
                points.append((x,y))
            elif event.type == EventType.KEYDOWN:
                if event.key.keysym.scancode == keyboard.Scancode.SPACE:
                    points = []
                elif event.key.keysym.scancode == keyboard.Scancode.BACKSPACE:
                    points.pop()

        w.renderer.set_draw_color(0,0,0,255)
        w.renderer.clear()
        w.renderer.set_draw_color(255,0,0,255)
        w.renderer.draw_lines(points)
        w.renderer.present()


if __name__ == '__main__':
    main()
