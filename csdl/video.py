import ctypes
from .internal import _SDL, errcheck
from .enum import CEnum

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
# these are included in docs but not SDL_renderer.h
#        ('mod_modes', ctypes.c_uint32),
#        ('blend_modes', ctypes.c_uint32),
#        ('scale_modes', ctypes.c_uint32),
        ('num_texture_formats', ctypes.c_uint32),
        ('texture_formats', ctypes.c_uint32*16),
        ('max_texture_width', ctypes.c_int),
        ('max_texture_height', ctypes.c_int)
    )

    def __repr__(self):
        return "<RendererInfo '{0}'>".format(self.name)

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
        return (r.value, g.value, b.value, a.value)

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


class WindowFlags(CEnum):
    FULLSCREEN    = 0x00000001
    OPENGL        = 0x00000002
    SHOWN         = 0x00000004
    HIDDEN        = 0x00000008
    BORDERLESS    = 0x00000010
    RESIZABLE     = 0x00000020
    MINIMIZED     = 0x00000040
    MAXIMIZED     = 0x00000080
    INPUT_GRABBED = 0x00000100
    INPUT_FOCUS   = 0x00000200
    MOUSE_FOCUS   = 0x00000400
    FOREIGN       = 0x00000800

_SDL.SDL_GetWindowTitle.restype = ctypes.c_char_p

class Window(object):

    def __init__(self, title, x, y, w, h, flags=0):
        self._handle = errcheck(_SDL.SDL_CreateWindow(title, x, y, w, h,
                                                      flags))
        self.renderer = Renderer(self._handle)

    def destroy(self):
        _glcontext = getattr(self, '_glcontext', None)
        if _glcontext:
            _SDL.SDL_GL_DeleteContext(_glcontext)
        _SDL.SDL_DestroyWindow(self._handle)

    @property
    def gl_context(self):
        if not hasattr(self, '_glcontext'):
            self._glcontext = _SDL.SDL_GL_CreateContext(self._handle)
        return self._glcontext

    def swap():
        _SDL.SDL_GL_SwapWindow(self._handle)

    def make_context_current():
        errcheck(_SDL.SDL_GL_MakeCurrent(self._handle, self._glcontext))

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
        return w.value, h.value

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
    return mode.value

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
            _display_mode_list[display_index].append(mode.value)
    return _display_mode_list[display_index]

def get_desktop_display_mode(display_index):
    mode = DisplayMode()
    errcheck(_SDL.SDL_GetDesktopDisplayMode(display_index, ctypes.byref(mode)))
    return mode.value

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
            return result.value

    def intersects(self, other):
        return _SDL.SDL_HasIntersection(ctypes.pointer(self),
                                        ctypes.pointer(other)) == 1

    def intersection(self, other):
        result = Rect()

        # returns True if an intersection is found
        if _SDL.SDL_IntersectRect(ctypes.pointer(self), ctypes.pointer(other),
                                  ctypes.byref(result)):
            return result.value

    def union(self, other):
        result = Rect()
        _SDL.SDL_UnionRect(ctypes.pointer(self), ctypes.pointer(other),
                           ctypes.byref(result))
        return result.value

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

    def __repr__(self):
        return 'Point({0}, {1})'.format(self.x, self.y)

def get_display_bounds(display_index):
    rect = Rect()
    errcheck(_SDL.SDL_GetDisplayBounds(display_index, ctypes.byref(rect)))
    return rect.value


def gl_extension_supported(extension):
    return _SDL.SDL_GL_ExtensionSupported(extension) == 1

class GL_Attr(CEnum):
    SDL_GL_RED_SIZE = 0
    SDL_GL_GREEN_SIZE = 1
    SDL_GL_BLUE_SIZE = 2
    SDL_GL_ALPHA_SIZE = 3
    SDL_GL_BUFFER_SIZE = 4
    SDL_GL_DOUBLEBUFFER = 5
    SDL_GL_DEPTH_SIZE = 6
    SDL_GL_STENCIL_SIZE = 7
    SDL_GL_ACCUM_RED_SIZE = 8
    SDL_GL_ACCUM_GREEN_SIZE = 9
    SDL_GL_ACCUM_BLUE_SIZE = 10
    SDL_GL_ACCUM_ALPHA_SIZE = 11
    SDL_GL_STEREO = 12
    SDL_GL_MULTISAMPLEBUFFERS = 13
    SDL_GL_MULTISAMPLESAMPLES = 14
    SDL_GL_ACCELERATED_VISUAL = 15
    SDL_GL_RETAINED_BACKING = 16
    SDL_GL_CONTEXT_MAJOR_VERSION = 17
    SDL_GL_CONTEXT_MINOR_VERSION = 18

def gl_get_attribute(attr):
    attrvalue = ctypes.c_int()
    errcheck(_SDL.SDL_GL_GetAttribute(attr, ctypes.byref(attrvalue)))
    return attrvalue.value

def gl_set_attribute(attr, value):
    errcheck(_SDL.SDL_GL_SetAttribute(attr, value))

def gl_get_swap_interval():
    return errcheck(_SDL.SDL_GL_GetSwapInterval())

def gl_set_swap_interval(interval):
    # 0: immediate
    # 1: sync w/ vtrace
    return errcheck(_SDL.SDL_GL_SetSwapInterval(interval))
