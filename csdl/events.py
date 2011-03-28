import ctypes
from .internal import _SDL, Version, errcheck, SDLError
from .enum import CEnum

class EventType(CEnum):
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

# a few typedefs
Keycode = ctypes.c_int32
Scancode = ctypes.c_int32  # enum, not sure about this one
GestureID = ctypes.c_int64
TouchID = ctypes.c_int64
FingerID = ctypes.c_int64

class SysWMType(CEnum):
    UNKNOWN = 0
    WINDOWS = 1
    X11 = 2
    DIRECTFB = 2
    COCOA = 3
    UIKIT = 4

# TODO: see what can be done to make SysWMmsg work
class _SysWMUnion(ctypes.Union):
    _fields_ = (
        ('dummy', ctypes.c_int),
    )

class SysWMmsg(ctypes.Structure):
    _fields_ = (
        ('version', Version),
        ('subsystem', ctypes.c_int),
        ('msg', _SysWMUnion),
    )

class Keysym(ctypes.Structure):
    _fields_ = (
        ('scancode', Scancode),
        ('keycode', Keycode),
        ('mod', ctypes.c_uint16),
        ('unicode', ctypes.c_uint32),
    )

class WindowEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('event', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('_padding3', ctypes.c_uint8),
        ('data1', ctypes.c_int),
        ('data2', ctypes.c_int),
    )

class KeyboardEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('state', ctypes.c_uint8),
        ('repeat', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('_padding3', ctypes.c_uint8),
        ('keysym', Keysym),
    )

class TextEditingEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('text', ctypes.c_char*32),
        ('start', ctypes.c_int),
        ('length', ctypes.c_int),
    )

class TextInputEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('text', ctypes.c_char*32),
    )

class MouseMotionEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('state', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('_padding3', ctypes.c_uint8),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('x_rel', ctypes.c_int),
        ('y_rel', ctypes.c_int),
    )

class MouseButtonEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('button', ctypes.c_uint8),
        ('state', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
    )

class MouseWheelEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
    )

class JoyAxisEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('which', ctypes.c_uint8),
        ('axis', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('value', ctypes.c_int),
    )

class JoyBallEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('which', ctypes.c_uint8),
        ('ball', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('xrel', ctypes.c_int),
        ('yrel', ctypes.c_int),
    )

class JoyHatEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('which', ctypes.c_uint8),
        ('hat', ctypes.c_uint8),
        ('value', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
    )

class JoyButtonEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('which', ctypes.c_uint8),
        ('button', ctypes.c_uint8),
        ('state', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
    )

class TouchFingerEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('touch_id', TouchID),
        ('finger_id', FingerID),
        ('state', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
        ('_padding3', ctypes.c_uint8),
        ('x', ctypes.c_uint16),
        ('y', ctypes.c_uint16),
        ('dx', ctypes.c_int16),
        ('dy', ctypes.c_int16),
        ('pressure', ctypes.c_uint16),
    )

class TouchButtonEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('touch_id', TouchID),
        ('state', ctypes.c_uint8),
        ('button', ctypes.c_uint8),
        ('_padding1', ctypes.c_uint8),
        ('_padding2', ctypes.c_uint8),
    )

class MultiGestureEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('touch_id', TouchID),
        ('d_theta', ctypes.c_float),
        ('d_dist', ctypes.c_float),
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('num_fingers', ctypes.c_uint16),
        ('padding', ctypes.c_uint16),
    )

class DollarGestureEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('touch_id', TouchID),
        ('gesture_id', GestureID),
        ('num_fingers', ctypes.c_uint32),
        ('error', ctypes.c_float),
        # these are commented out in the header, maybe coming soon
        #('x', ctypes.c_float),
        #('y', ctypes.c_float),
    )

class QuitEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
    )

class UserEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window_id', ctypes.c_uint32),
        ('code', ctypes.c_int),
        ('data1', ctypes.c_void_p),
        ('data2', ctypes.c_void_p),
    )

class SysWMEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('msg', ctypes.POINTER(SysWMmsg)),
    )

class ActiveEvent(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('gain', ctypes.c_uint8),
        ('state', ctypes.c_uint8),
    )

class ResizeEvent(ctypes.Structure):
    _fields_ = (
        ('types', ctypes.c_uint32),
        ('w', ctypes.c_int),
        ('h', ctypes.c_int),
    )

class Event(ctypes.Union):
    _fields_ = (
        ('type', ctypes.c_uint32),
        ('window', WindowEvent),
        ('key', KeyboardEvent),
        ('edit', TextEditingEvent),
        ('text', TextInputEvent),
        ('motion', MouseMotionEvent),
        ('button', MouseButtonEvent),
        ('wheel', MouseWheelEvent),
        ('jaxis', JoyAxisEvent),
        ('jball', JoyBallEvent),
        ('jbutton', JoyButtonEvent),
        ('quit', QuitEvent),
        ('user', UserEvent),
        ('syswm', SysWMEvent),
        ('tfinger', TouchFingerEvent),
        ('tbutton', TouchButtonEvent),
        ('mgesture', MultiGestureEvent),
        ('dgesture', DollarGestureEvent),
        ('active', ActiveEvent),
        ('resize', ResizeEvent),
    )

# not implemented:
# SDL_AddEventWatch,SDL_DelEventWatch - void*
# SDL_FilterEvents,SDL_SetEventFilter,SDL_GetEventFilter - void*

def pump_events():
    _SDL.SDL_PumpEvents()

def peep_events(events, num_events, action, min_type, max_type):
    return errcheck(_SDL>SDL_PeepEvents(events, numevents, action,
                                        min_type, max_type))

def has_event(type):
    return _SDL.SDL_HasEvent(type) == 1

def has_events(min_type, max_type):
    return _SDL.SDL_HasEvents(min_type, max_type) == 1

def flush_event(type):
    _SDL.SDL_FlushEvent(type)

def flush_events(min_type, max_type):
    _SDL.SDL_FlushEvents(min_type, max_type)

def poll_event():
    event = Event()
    retval = _SDL.SDL_PollEvent(ctypes.byref(event))
    if retval:
        return event

def wait_event(timeout=0):
    event = Event()

    if timeout:
        retval = _SDL.SDL_WaitEventTimeout(ctypes.byref(event), timeout)
    else:
        retval = _SDL.SDL_WaitEvent(ctypes.byref(event))

    if retval:
        return event

def push_event(event):
    return errcheck(_SDL.SDL_PushEvent(ctypes.byref(event)))

def event_state(type, state):
    errcheck(_SDL.SDL_EventState(type, state))

def register_events(num_events):
    registered = _SDL.SDL_RegisterEvents(num_events)
    if registered < 0:
        raise SDLError("out of available event ids for register_events")
    return registered
