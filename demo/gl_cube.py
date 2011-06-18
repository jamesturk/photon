from photon import init, InitFlags, video
from photon.video import Window
from photon.events import EventType, poll_event, WindowEventType
import time

vertices = [-1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0]
colors = [0.0,  1.0,  0.0,  1.0,
          0.0,  1.0,  0.0,  1.0,
          1.0,  0.0,  0.0,  1.0,
          1.0,  0.0,  0.0,  1.0,
          1.0,  0.0,  0.0,  1.0,
          1.0,  0.0,  0.0,  1.0,
          0.0,  0.0,  1.0,  1.0,
          1.0,  0.0,  1.0,  1.0]
indices = [0, 4, 5, 0, 5, 1,
           1, 5, 6, 1, 6, 2,
           2, 6, 7, 2, 7, 3,
           3, 7, 4, 3, 4, 0,
           4, 7, 6, 4, 6, 5,
           3, 0, 1, 3, 1, 2]

def main():
    init(InitFlags.EVERYTHING)

    window = Window('gl cube demo', 100, 100, 512, 512,
                    video.WindowFlags.OPENGL)

    video.gl_set_attribute(video.GL_Attr.SDL_GL_MULTISAMPLEBUFFERS, 1)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_MULTISAMPLESAMPLES, 4)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_DOUBLEBUFFER, 1)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_DEPTH_SIZE, 24)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_RED_SIZE, 8)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_GREEN_SIZE, 8)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_BLUE_SIZE, 8)
    video.gl_set_attribute(video.GL_Attr.SDL_GL_ALPHA_SIZE, 8)

    window.gl_context
    video.gl_set_swap_interval(1)

    from OpenGL.GL import *
    from OpenGL.GLU import gluPerspective

    # setup gl perspective
    glClearDepth(1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glViewport(0, 0, 512, 512)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 512/512, 0.1, 100)
    glViewport(0, 0, 512, 512)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    running = True
    start_time = time.time()
    frames = 0

    cube_rotation = 0

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

        # setup state
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -10)
        glRotatef(cube_rotation, 1, 1, 1)

        # draw cube
        glFrontFace(GL_CW)
        glVertexPointer(3, GL_FLOAT, 0, vertices)
        glColorPointer(4, GL_FLOAT, 0, colors)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_BYTE, indices)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glLoadIdentity()
        cube_rotation -= 0.15

        window.swap()


if __name__ == '__main__':
    main()
