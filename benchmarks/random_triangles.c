#include "SDL/SDL.h"
#include <stdlib.h>

int main(int argc, char **argv) {
    SDL_Init(SDL_INIT_EVERYTHING);

    SDL_Window* window = SDL_CreateWindow("demo window", 100, 100, 512, 512, 0);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, 0);

    int i;
    SDL_Point p1, p2, p3;
    SDL_Event event;

    int start_time = SDL_GetTicks();
    int frames=0;

    int running=1;

    while(running) {
        frames++;
        if(frames == 1000) {
            printf("FPS %f\n", (float)frames/(SDL_GetTicks()-start_time)*1000);
            frames = 0;
            start_time = SDL_GetTicks();
        }

        while(SDL_PollEvent(&event)) {
            if(event.type == SDL_WINDOWEVENT) {
                if(event.window.event == SDL_WINDOWEVENT_CLOSE) {
                    running=0;
                }
            }
        }

        // draw
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);

        for(i=0; i < 20; ++i) {
            SDL_SetRenderDrawColor(renderer, rand()%255, rand()%255, rand()%255, 255);
            p1.x = rand()%512;
            p1.y = rand()%512;
            p2.x = rand()%512;
            p2.y = rand()%512;
            p3.x = rand()%512;
            p3.y = rand()%512;
            SDL_Point points[4] = { p1, p2, p3, p1 };
            SDL_RenderDrawLines(renderer, points, 4);
        }
        SDL_RenderPresent(renderer);
    }
}
