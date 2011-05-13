import ctypes
from .internal import _SDL

# SDL_GetKeyboardFocus
# have this return a Window() object

_SDL.SDL_GetKeyboardState.restype = ctypes.POINTER(ctypes.c_uint8)
_keyboard_state = None
def get_keyboard_state():
    # index by scancode
    global _keyboard_state
    if not _keyboard_state:
        _keyboard_state = _SDL.SDL_GetKeyboardState(None)
    return _keyboard_state

def get_mod_state():
    return _SDL.SDL_GetModState()

def set_mod_state(modstate):
    _SDL.SDL_SetModState(modstate)

def get_key_from_scancode(scancode):
    return _SDL.SDL_GetKeyFromScancode(scancode)

def get_scancode_from_key(keycode):
    return _SDL.SDL_GetScancodeFromKey(keycode)

_SDL.SDL_GetKeyName.restype = ctypes.c_char_p
def get_key_name(keycode):
    return _SDL.SDL_GetKeyName(keycode)

_SDL.SDL_GetScancodeName.restype = ctypes.c_char_p
def get_scancode_name(scancode):
    return _SDL.SDL_GetScancodeName(scancode)

def start_text_input():
    _SDL.SDL_StartTextInput()

def stop_text_input():
    _SDL.SDL_StopTextInput()

def set_text_input_rect(rect):
    _SDL.SDL_SetTextInputRect(rect)
