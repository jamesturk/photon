import ctypes
_SDL = ctypes.cdll.LoadLibrary('/usr/local/lib/libSDL-1.3.so.0.0.0')

# Constants
class INIT(object):
    TIMER       = 0x00000001
    AUDIO       = 0x00000010
    VIDEO       = 0x00000020
    JOYSTICK    = 0x00000200
    HAPTIC      = 0x00001000
    NOPARACHUTE = 0x00100000
    EVERYTHING  = 0x0000FFFF

class Event(object):
    FIRSTEVENT  = 0

    QUIT        = 0x100

    WINDOWEVENT = 0x200
    SYSWMEVENT  = 0x201

    KEYDOWN     = 0x300
    KEYUP       = 0x301
    TEXTEDITING = 0x302
    TEXTINPUT   = 0x303

    MOUSEMOTION     = 0x400
    MOUSEBUTTONDOWN = 0x401
    MOUSEBUTTONUP   = 0x402
    MOUSEWHEEL      = 0x403

    INPUTMOTION       = 0x500
    INPUTBUTTONDOWN   = 0x501
    INPUTBUTTONUP     = 0x502
    INPUTWHEEL        = 0x503
    INPUTPROXIMITYIN  = 0x504
    INPUTPROXIMITYOUT = 0x505

    JOYAXISMOTION  = 0x600
    JOYBALLMOTION  = 0x601
    JOYHATMOTION   = 0x602
    JOYBUTTONDOWN  = 0x603
    JOYBUTTONUP    = 0x604

    FINGERDOWN      = 0x700
    FINGERUP        = 0x701
    FINGERMOTION    = 0x702
    TOUCHBUTTONDOWN = 0x703
    TOUCHBUTTONUP   = 0x704

    DOLLARGESTURE   = 0x800
    DOLLARRECORD    = 0x801
    MULTIGESTURE    = 0x802

    CLIPBOARDUPDATE = 0x900

    USEREVENT = 0x8000
    LASTEVENT = 0xFFFF


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


#### System Information

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

_render_driver_list = []
def get_render_drivers():
    if not _render_driver_list:
        num = _SDL.SDL_GetNumRenderDrivers()
        for i in xrange(num):
            rinfo = RendererInfo()
            errcheck(_SDL.SDL_GetRenderDriverInfo(i, ctypes.byref(rinfo)))
            _render_driver_list.append(rinfo)
    return _render_driver_list

class Renderer(object):

    def __init__(self, window, index=-1, flags=0):
        self._renderer = errcheck(_SDL.SDL_CreateRenderer(window, index, flags))

    def get_info(self):
        rinfo = RendererInfo()
        errcheck(_SDL.SDL_GetRendererInfo(self._renderer, ctypes.byref(rinfo)))
        return rinfo

    def set_draw_color(self, r, g, b, a=255):
        errcheck(_SDL.SDL_SetRenderDrawColor(self._renderer, r, g, b, a))

    @property
    def draw_color(self):
        r = ctypes.c_uint8()
        g = ctypes.c_uint8()
        b = ctypes.c_uint8()
        a = ctypes.c_uint8()
        errcheck(_SDL.SDL_GetRenderDrawColor(self._renderer, ctypes.byref(r),
                                             ctypes.byref(g), ctypes.byref(b),
                                             ctypes.byref(a)))
        return (r,g,b,a)

    @property
    def viewport(self):
        rect = Rect()
        _SDL.SDL_RenderGetViewport(self._renderer, ctypes.byref(rect))
        return rect

    @viewport.setter
    def viewport(self, rect):
        _SDL.SDL_RenderSetViewport(self._renderer, ctypes.pointer(rect))

    def clear(self):
        errcheck(_SDL.SDL_RenderClear(self._renderer))

    def present(self):
        errcheck(_SDL.SDL_RenderPresent(self._renderer))

    def draw_line(self, x1, y1, x2, y2):
        errcheck(_SDL.SDL_RenderDrawLine(self._renderer, x1, y1, x2, y2))

    def draw_lines(self, points):
        PtArray = Point*len(points)
        _sdl_points = PtArray(*[Point(*pt) for pt in points])
        errcheck(_SDL.SDL_RenderDrawLines(self._renderer, _sdl_points,
                                          len(points)))

    def draw_point(self, x, y):
        errcheck(_SDL.SDL_RenderDrawPoint(self._renderer, x, y))

    def draw_points(self, points):
        PtArray = Point*len(points)
        _sdl_points = PtArray(*[Point(*pt) for pt in points])
        errcheck(_SDL.SDL_RenderDrawPoints(self._renderer, _sdl_points,
                                          len(points)))

    def draw_rect(self, rect):
        _SDL.SDL_RenderDrawRect(self._renderer, ctypes.pointer(rect))

    def draw_rects(self, rects):
        RectArray = Rect*len(rects)
        rects = RectArray(*rects)
        _SDL.SDL_RenderDrawRects(self._renderer, rects, len(rects))

    def fill_rect(self, rect):
        _SDL.SDL_RenderFillRect(self._renderer, ctypes.pointer(rect))

    def fill_rects(self, rects):
        RectArray = Rect*len(rects)
        rects = RectArray(*rects)
        _SDL.SDL_RenderFillRects(self._renderer, rects, len(rects))

_SDL.SDL_GetWindowTitle.restype = ctypes.c_char_p

class Window(object):

    def __init__(self, title, x, y, w, h, flags=0):
        self._handle = errcheck(_SDL.SDL_CreateWindow(title, x, y, w, h,
                                                      flags))
        self.renderer = Renderer(self._handle)

    def destroy(self):
        _SDL.SDL_DestroyWindow(self._handle)

    @property
    def display(self):
        return errcheck(_SDL.SDL_GetWindowDisplay(self._handle))

    def get_display_mode(self):
        mode = DisplayMode()
        errcheck(_SDL.SDL_GetWindowDisplayMode(self._handle,
                                               ctypes.byref(mode)))
        return mode

    def get_flags(self):
        return _SDL.SDL_GetWindowFlags(self._handle)

    @property
    def grab(self):
        return _SDL.SDL_GetWindowGrab(self._handle) == 1

    @grab.setter
    def grab(self, grab_mode):
        _SDL.SDL_SetWindowGrab(self._handle, 1 if grab_mode else 0)

    @property
    def id(self):
        return _SDL.SDL_GetWindowID(self._handle)

    @property
    def pixel_format(self):
        return errcheck(_SDL.SDL_GetWindowPixelFormat(self._handle))

    @property
    def position(self):
        x = ctypes.c_int()
        y = ctypes.c_int()
        _SDL.SDL_GetWindowPosition(self._handle, ctypes.byref(x),
                                   ctypes.byref(y))
        return x.value, y.value

    def move(self, x, y):
        _SDL.SDL_SetWindowPosition(self._handle, x, y)

    @property
    def size(self):
        w = ctypes.c_int()
        h = ctypes.c_int()
        _SDL.SDL_GetWindowSize(self._handle, ctypes.byref(w),
                               ctypes.byref(h))
        return w,h

    def resize(self, w, h):
        _SDL.SDL_SetWindowSize(self._handle, w, h)

    @property
    def title(self):
        return _SDL.SDL_GetWindowTitle(self._handle)

    @title.setter
    def title(self, title_str):
        _SDL.SDL_SetWindowTitle(self._handle, title_str)

    def hide(self):
        _SDL.SDL_HideWindow(self._handle)

    def maximize(self):
        _SDL.SDL_MaximizeWindow(self._handle)

    def minimize(self):
        _SDL.SDL_MinimizeWindow(self._handle)

    def raise_window(self):
        _SDL.SDL_RaiseWindow(self._handle)

    def restore(self):
        _SDL.SDL_RestoreWindow(self._handle)

    def show(self):
        _SDL.SDL_ShowWindow(self._handle)

def disable_screensaver():
    _SDL.SDL_DisableScreenSaver()

def enable_screensaver():
    _SDL.SDL_EnableScreenSaver()

def is_screensaver_enabled():
    return _SDL.SDL_IsScreenSaverEnabled() == 1

def get_current_display_mode(display):
    mode = DisplayMode()
    errcheck(_SDL.SDL_GetCurrentDisplayMode(display, ctypes.byref(mode)))
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
    errcheck(_SDL.SDL_GetDesktopDisplayMode(display_index, ctypes.byref(mode)))
    return mode

class Rect(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('width', ctypes.c_int),
        ('height', ctypes.c_int),
    )

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and
                self.width == other.width and self.height == other.height)

    @staticmethod
    def enclose_points(points, clip=None):
        PtArray = Point*len(points)
        _sdl_points = PtArray(*[Point(*pt) for pt in points])
        result = Rect()

        # returns True if a rect is created
        if _SDL.SDL_EnclosePoints(_sdl_points, len(points),
                                  ctypes.pointer(clip) if clip else None,
                                  ctypes.byref(result)):
            return result

    def intersects(self, other):
        return _SDL.SDL_HasIntersection(ctypes.pointer(self),
                                        ctypes.pointer(other)) == 1

    def intersection(self, other):
        result = Rect()

        # returns True if an intersection is found
        if _SDL.SDL_IntersectRect(ctypes.pointer(self), ctypes.pointer(other),
                                  ctypes.byref(result)):
            return result

    def union(self, other):
        result = Rect()
        _SDL.SDL_UnionRect(ctypes.pointer(self), ctypes.pointer(other),
                           ctypes.byref(result))
        return result

    def intersects_line(self, x1, y1, x2, y2):
        return _SDL.SDL_IntersectRectAndLine(ctypes.pointer(self),
                                             ctypes.pointer(x1),
                                             ctypes.pointer(y1),
                                             ctypes.pointer(x2),
                                             ctypes.pointer(y2)) == 1

    def is_empty(self):
        return self.width <= 0 or self.height <= 0

    def __repr__(self):
        return 'Rect({0}, {1}, {2}, {3})'.format(self.x, self.y,
                                                 self.width, self.height)

class Point(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
    )

def get_display_bounds(display_index):
    rect = Rect()
    errcheck(_SDL.SDL_GetDisplayBounds(display_index, ctypes.byref(rect)))
    return rect
