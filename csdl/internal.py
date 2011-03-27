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

# moved here so events.SysWMmsg can get at it
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
