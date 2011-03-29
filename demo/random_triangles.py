#!/usr/bin/env python
from demo_utils import simple_timed_loop
import random

def draw(window):
    window.renderer.set_draw_color(0,0,0,255)
    window.renderer.clear()
    window.renderer.set_draw_color(255,0,0,255)
    for i in xrange(1000):
        window.renderer.set_draw_color(random.randint(0,255),
                                       random.randint(0,255),
                                       random.randint(0,255))
        p1 = (random.randint(0,512), random.randint(0, 512))
        p2 = (random.randint(0,512), random.randint(0, 512))
        p3 = (random.randint(0,512), random.randint(0, 512))
        window.renderer.draw_lines([p1, p2, p3, p1])
    window.renderer.present()

if __name__ == '__main__':
    simple_timed_loop(draw)
