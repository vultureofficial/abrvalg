#ifndef _SDL_H_

#include <SDL2/SDL.h>
#include "data_types.h"
#include "io.h"

class sdl {
    public:
    sdl() {}
    ~sdl() {} 

    void init() {
        SDL_Init(SDL_INIT_EVERYTHING); 
    }

    SDL_Window *create_window(string title, i32 width, i32 height) {
        SDL_Window *window = SDL_CreateWindow(
            title.c_str(),                  // window title
            SDL_WINDOWPOS_UNDEFINED,           // initial x position
            SDL_WINDOWPOS_UNDEFINED,           // initial y position
            width,                               // width, in pixels
            height,                               // height, in pixels
            SDL_WINDOW_RESIZABLE                  // flags - see below
        );

        return window == NULL ? NULL : window; 
    }


    void destroy_window(SDL_Window *window) {
        //Destroy window
        SDL_DestroyWindow( window );
    }


    void quit() {
        //Quit SDL subsystems
        return SDL_Quit();
    }

    void delay(i32 milliseconds) {
        SDL_Delay((u32) milliseconds);
    }

    string geterror() {
        string error(SDL_GetError());
        return error;
    }

};


#endif // !_SDL_H_