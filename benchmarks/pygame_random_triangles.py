import pygame
import time
import random

N_TRIANGLES = 1000

def main():
    pygame.init()

    surface = pygame.display.set_mode((512,512))

    running = True
    frames = 0
    start_time = time.time()

    while running:

        frames += 1
        if frames == 1000:
            print('FPS {0:.2f}'.format(frames/(time.time()-start_time)))
            frames = 0
            start_time = time.time()


        surface.fill((0,0,0))
        for i in xrange(N_TRIANGLES):
            p1 = (random.randint(0,512), random.randint(0, 512))
            p2 = (random.randint(0,512), random.randint(0, 512))
            p3 = (random.randint(0,512), random.randint(0, 512))
            pygame.draw.lines(surface, (random.randint(0,255), 
                                        random.randint(0,255), 
                                        random.randint(0,255)),
                              True, [p1,p2,p3]
                             )
        pygame.display.flip()


main()
