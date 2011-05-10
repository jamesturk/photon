from photon import init, InitFlags
from photon.video import Window
from photon.events import EventType, poll_event, WindowEventType
import time

def simple_timed_loop(draw_func):
    init(InitFlags.EVERYTHING)
    window = Window('timed sdloppy demo', 100, 100, 512, 512)
    running = True

    start_time = time.time()
    frames = 0

    while running:
        frames += 1
        if frames == 1000:
            print('FPS: {0:.2f}'.format(frames/(time.time()-start_time)))
            frames = 0
            start_time = time.time()

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

        draw_func(window)
