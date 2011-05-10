import ctypes
from .internal import _SDL

_SDL.SDL_GetPerformanceCounter.restype = ctypes.c_uint64
_SDL.SDL_GetPerformanceFrequency.restype = ctypes.c_uint64
_SDL.SDL_GetTicks.restype = ctypes.c_uint32


def get_performance_counter():
    return _SDL.SDL_GetPerformanceCounter()

def get_performance_frequency():
    return _SDL.SDL_GetPerformanceFrequency()

def get_ticks():
    return _SDL.SDL_GetTicks()

