from csdl import init, INIT
from csdl.video import Window, Rect
import random
import time

def main():
    init(INIT.EVERYTHING)
    window = Window('test', 100, 100, 512, 512, 0)

    while True:
        window.renderer.set_draw_color(0,0,0,255)
        window.renderer.clear()
        window.renderer.set_draw_color(255,0,0,255)
        for i in xrange(20):
            window.renderer.set_draw_color(random.randint(0,255),
                                           random.randint(0,255),
                                           random.randint(0,255))
            r = Rect(random.randint(0,512), random.randint(0, 512),
                     random.randint(0,300), random.randint(0, 300))
            s = Rect(random.randint(0,512), random.randint(0, 512),
                     random.randint(0,300), random.randint(0, 300))
            t = Rect(random.randint(0,512), random.randint(0, 512),
                     random.randint(0,300), random.randint(0, 300))
            window.renderer.fill_rects([r,s,t])
        window.renderer.present()
        time.sleep(.001)
main()
