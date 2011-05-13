from photon import init, InitFlags, keyboard, video
from photon.events import poll_event, EventType, WindowEventType

def main():
    init(InitFlags.EVERYTHING)

    w = video.Window('keyboard test', 10, 10, 300, 300)
    running = True

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
            elif event.type == EventType.KEYDOWN:
                scan = event.key.keysym.scancode
                key = event.key.keysym.keycode
                print 'Key Pressed: %s (%s) | %s (%s)' % (
                    keyboard.get_scancode_name(scan), scan, 
                    keyboard.get_key_name(key), key)
                # enter -- check letter keys held
                if key == 13:
                    print sum(keyboard.get_keyboard_state()[4:30]), 'letter keys held'

if __name__ == '__main__':
    main()
