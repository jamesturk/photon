from nose.tools import with_setup, raises
from .. import init, InitFlags
from ..internal import SDLError
from ..events import *

def get_mm_event():
    mm_event = MouseMotionEvent(type=EventType.MOUSEMOTION,
                                window_id=1, state=1,
                                x=31, y=14, x_rel=1, y_rel=1)
    return Event(type=EventType.MOUSEMOTION, motion=mm_event)

def setup_clean_queue():
    init(InitFlags.VIDEO)
    flush_events(EventType.FIRSTEVENT, EventType.LASTEVENT)

@with_setup(setup_clean_queue)
def test_has_events():
    assert not has_events(EventType.FIRSTEVENT, EventType.LASTEVENT)
    push_event(get_mm_event())
    assert has_events(EventType.FIRSTEVENT, EventType.LASTEVENT)

@with_setup(setup_clean_queue)
def test_has_event():
    assert not has_event(EventType.MOUSEMOTION)
    push_event(get_mm_event())
    assert has_event(EventType.MOUSEMOTION)

@with_setup(setup_clean_queue)
def test_poll_event():
    # push 3 on
    push_event(get_mm_event())
    push_event(get_mm_event())
    push_event(get_mm_event())

    # pull 4 off, last should be None
    first = poll_event()
    second = poll_event()
    third = poll_event()
    too_many = poll_event()

    assert first and second and third
    assert not too_many

@with_setup(setup_clean_queue)
def test_wait_event_timeout():
    # push one on
    push_event(get_mm_event())

    # pull two off, should timeout for second one
    first = wait_event(1)
    too_many = wait_event(1)

    assert first
    assert not too_many

def test_register_events():
    first = register_events(100)
    assert first == EventType.USEREVENT
    next = register_events(1)
    assert next == first+100

@raises(SDLError)
def test_register_events_exception():
    too_many = register_events(100000)
