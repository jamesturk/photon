import pyglet
from pyglet.gl import *
import random
import time

N_TRIANGLES = 1000

window = pyglet.window.Window()

frames = 0
start_time = time.time()

@window.event
def on_draw():
    global frames
    global start_time
    frames += 1
    if frames == 1000:
        print('FPS {0:.2f}'.format(frames/(time.time()-start_time)))
        frames = 0
        start_time = time.time()

    window.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    for x in range(N_TRIANGLES):
        glColor3ub(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        glBegin(GL_LINE_LOOP)
        glVertex2f(random.randint(0,512), random.randint(0,512))
        glVertex2f(random.randint(0,512), random.randint(0,512))
        glVertex2f(random.randint(0,512), random.randint(0,512))
        glEnd()

pyglet.app.run()
