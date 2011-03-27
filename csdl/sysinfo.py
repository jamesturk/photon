_SDL.SDL_GetPlatform.restype = ctypes.c_char_p

def get_platform():
    return _SDL.SDL_GetPlatform()

def get_cpu_cache_line_size():
    return _SDL.SDL_GetCPUCacheLineSize()

def get_cpu_count():
    return _SDL.SDL_GetCPUCount()

def has_3DNow():
    return _SDL.SDL_Has3DNow() == 1

def has_AltiVec():
    return _SDL.SDL_HasAltiVec() == 1

def has_MMX():
    return _SDL.SDL_HasMMX() == 1

def has_RDTSC():
    return _SDL.SDL_HasRDTSC() == 1

def has_SSE():
    return _SDL.SDL_HasSSE() == 1

def has_SSE2():
    return _SDL.SDL_HasSSE2() == 1

def has_SSE3():
    return _SDL.SDL_HasSSE3() == 1

def has_SSE41():
    return _SDL.SDL_HasSSE3() == 1

def has_SSE42():
    return _SDL.SDL_HasSSE42() == 1

def get_power_info():
    seconds = ctypes.c_int()
    percent = ctypes.c_int()
    state = _SDL.SDL_GetPowerInfo(ctypes.byref(seconds),
                                  ctypes.byref(percent))
    state = {0: 'UNKNOWN', 1: 'ON_BATTERY', 2: 'NO_BATTERY', 3: 'CHARGING',
             4: 'CHARGED'}[state]
    return state, seconds.value, percent.value


