import ctypes
_SDL = ctypes.cdll.LoadLibrary('/usr/local/lib/libSDL-1.3.so.0.0.0')

def get_power_info():
    seconds = ctypes.c_int()
    percent = ctypes.c_int()
    _SDL.SDL_GetPowerInfo(ctypes.byref(seconds),
                          ctypes.byref(percent))
    return seconds.value, percent.value

# Constants
SDL_INIT_TIMER       = 0x00000001
SDL_INIT_AUDIO       = 0x00000010
SDL_INIT_VIDEO       = 0x00000020
SDL_INIT_JOYSTICK    = 0x00000200
SDL_INIT_HAPTIC      = 0x00001000
SDL_INIT_NOPARACHUTE = 0x00100000
SDL_INIT_EVERYTHING  = 0x0000FFFF

##### Error Handling

class SDLError(Exception):
    """ Exception representing an error in an SDL call """

_SDL.SDL_GetError.restype = ctypes.c_char_p
def get_error():
    return _SDL.SDL_GetError()

def set_error(msg):
    _SDL.SDL_SetError(msg)

def clear_error():
    _SDL.SDL_ClearError()

def errcheck(result):
    if result < 0:
        msg = _SDL.SDL_GetError()
        _SDL.SDL_ClearError()
        raise SDLError(msg)
    return result

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
        return '{0}.{1}.{2}'.format(self.major,
                                    self.minor,
                                    self.patch)


def get_version():
    v = Version()
    _SDL.SDL_GetVersion(ctypes.byref(v))
    return v

_SDL.SDL_GetRevision.restype = ctypes.c_char_p
def get_revision():
    return _SDL.SDL_GetRevision()


#### video

class DisplayMode(ctypes.Structure):
    _fields_ = (
        ('format', ctypes.c_uint32),
        ('width', ctypes.c_int),
        ('height', ctypes.c_int),
        ('refresh_rate', ctypes.c_int),
        ('driver_data', ctypes.c_void_p)
    )

    def __repr__(self):
        return '{0}x{1} @{2}Hz ({3})'.format(self.width,
                                             self.height,
                                             self.refresh_rate,
                                             get_pixel_format_name(self.format)
                                            )

class RendererInfo(ctypes.Structure):
    _fields_ = (
        ('name', ctypes.c_char_p),
        ('flags', ctypes.c_uint32),
        ('mod_modes', ctypes.c_uint32),
        ('blend_modes', ctypes.c_uint32),
        ('scale_modes', ctypes.c_uint32),
        ('num_texture_formats', ctypes.c_uint32),
        ('texture_formats', ctypes.c_uint32*50),
        ('max_texture_width', ctypes.c_int),
        ('max_texture_height', ctypes.c_int)
    )

class Renderer(object):

    def __init__(self, window, index=-1, flags=0):
        self._renderer = errcheck(_SDL.SDL_CreateRenderer(window, index, flags))

    def get_info(self):
        rinfo = RendererInfo()
        errcheck(_SDL.SDL_GetRendererInfo(self._renderer, ctypes.byref(rinfo)))
        return rinfo

    def set_draw_color(self, r, g, b, a=255):
        errcheck(_SDL.SDL_SetRenderDrawColor(self._renderer, r, g, b, a))

    def clear(self):
        errcheck(_SDL.SDL_RenderClear(self._renderer))

    def present(self):
        errcheck(_SDL.SDL_RenderPresent(self._renderer))

    def draw_line(self, x1, y1, x2, y2):
        errcheck(_SDL.SDL_RenderDrawLine(self._renderer, x1, y1, x2, y2))

class Window(object):

    def __init__(self, title, x, y, w, h, flags=0):
        self._handle = errcheck(_SDL.SDL_CreateWindow(title, x, y, w, h,
                                                      flags))
        self.renderer = Renderer(self._handle)

    def destroy(self):
        _SDL.SDL_DestroyWindow(self._handle)



def disable_screensaver():
    _SDL.SDL_DisableScreenSaver()

def enable_screensaver():
    _SDL.SDL_EnableScreenSaver()

def is_screensaver_enabled():
    return _SDL.SDL_IsScreenSaverEnabled() == 1

def get_current_display_mode(display):
    mode = DisplayMode()
    result = _SDL.SDL_GetCurrentDisplayMode(display, ctypes.byref(mode))
    if result == 0:
        return mode

_SDL.SDL_GetPixelFormatName.restype = ctypes.c_char_p
def get_pixel_format_name(format):
    return _SDL.SDL_GetPixelFormatName(format)

_SDL.SDL_GetCurrentVideoDriver.restype = ctypes.c_char_p
def get_current_video_driver():
    return _SDL.SDL_GetCurrentVideoDriver()

def get_num_video_displays():
    return _SDL.SDL_GetNumVideoDisplays()

_video_driver_list = []
_SDL.SDL_GetVideoDriver.restype = ctypes.c_char_p
def get_video_drivers():
    if not _video_driver_list:
        num = _SDL.SDL_GetNumVideoDrivers()
        for i in xrange(num):
            _video_driver_list.append(_SDL.SDL_GetVideoDriver(i))
    return _video_driver_list

_display_mode_list = {}
def get_display_modes(display_index):
    if not display_index in _display_mode_list:
        _display_mode_list[display_index] = []
        num = _SDL.SDL_GetNumDisplayModes(display_index)
        for i in xrange(num):
            mode = DisplayMode()
            _SDL.SDL_GetDisplayMode(display_index, i, ctypes.byref(mode))
            _display_mode_list[display_index].append(mode)
    return _display_mode_list[display_index]

def get_desktop_display_mode(display_index):
    mode = DisplayMode()
    _SDL.SDL_GetDesktopDisplayMode(display_index, ctypes.byref(mode))
    return mode
