import ctypes
from .internal import _SDL, errcheck
from .enum import CEnum

def get_mouse_state():
    x = ctypes.c_int()
    y = ctypes.c_int()
    buttons = _SDL.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
    return x.value, y.value, buttons

def get_relative_mouse_state():
    x = ctypes.c_int()
    y = ctypes.c_int()
    buttons = _SDL.SDL_GetRelativeMouseState(ctypes.byref(x), ctypes.byref(y))
    return x.value, y.value, buttons

def get_relative_mouse_mode():
    return _SDL.SDL_GetRelativeMouseMode() == 1

def set_relative_mouse_mode(enabled):
    errcheck(_SDL.SDL_SetRelativeMouseMode(enabled))

def set_cursor_visibility(visible):
    errcheck(_SDL.SDL_ShowCursor(visible))

def is_cursor_visible():
    return errcheck(_SDL.SDL_ShowCursor(-1)) == 1

def warp_mouse_in_window(x, y, window=0):
    if window:
        window = window._handle
    _SDL.SDL_WarpMouseInWindow(window, x, y)

class Button(CEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    X1 = 4
    X2 = 5

    # masks for comparison against get_mouse_state return values
    LMASK = 1
    MMASK = 2
    RMASK = 4
    X1MASK = 8
    X2MASK = 16
