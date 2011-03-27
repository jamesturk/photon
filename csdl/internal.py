import ctypes
_SDL = ctypes.cdll.LoadLibrary('/usr/local/lib/libSDL-1.3.so.0.0.0')

class SDLError(Exception):
    """ Exception representing an error in an SDL call """

def errcheck(result):
    if result < 0:
        msg = _SDL.SDL_GetError()
        _SDL.SDL_ClearError()
        raise SDLError(msg)
    return result

