import ctypes
from .internal import _SDL, errcheck

# Constants
class INIT(object):
    TIMER       = 0x00000001
    AUDIO       = 0x00000010
    VIDEO       = 0x00000020
    JOYSTICK    = 0x00000200
    HAPTIC      = 0x00001000
    NOPARACHUTE = 0x00100000
    EVERYTHING  = 0x0000FFFF

##### Error Handling

_SDL.SDL_GetError.restype = ctypes.c_char_p
def get_error():
    return _SDL.SDL_GetError()

def set_error(msg):
    _SDL.SDL_SetError(msg)

def clear_error():
    _SDL.SDL_ClearError()

##### Initialization

def init(flags):
    errcheck(_SDL.SDL_Init(flags))

def init_sub_system(flags):
    errcheck(_SDL.SDL_InitSubSystem(flags))

def quit_sub_system(flags):
    errcheck(_SDL.SDL_QuitSubSystem(flags))

def was_init(flags=0):
    errcheck(_SDL.SDL_WasInit(flags))

def quit():
    _SDL.SDL_Quit()

##### Version Info

class Version(ctypes.Structure):
    _fields_ = (
        ("major", ctypes.c_uint8),
        ("minor", ctypes.c_uint8),
        ("patch", ctypes.c_uint8)
    )

    def __str__(self):
        return '{0}.{1}.{2}'.format(self.major, self.minor, self.patch)

    def __repr__(self):
        return 'Version({0},{1},{2})'.format(self.major, self.minor,
                                             self.patch)

def get_version():
    v = Version()
    _SDL.SDL_GetVersion(ctypes.byref(v))
    return v

_SDL.SDL_GetRevision.restype = ctypes.c_char_p
def get_revision():
    return _SDL.SDL_GetRevision()

