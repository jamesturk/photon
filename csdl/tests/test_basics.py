from .. import (get_error, set_error, clear_error,
                InitFlags, init, quit, was_init,
                init_sub_system, quit_sub_system,
                get_version, get_revision)
from nose.tools import with_setup

def test_error_handling():
    # blank by default
    assert get_error() == ""

    # check set
    set_error("test!")
    assert get_error() == "test!"

    # check again, shouldn't clear
    assert get_error() == "test!"

    # clear again
    clear_error()
    assert get_error() == ""

@with_setup(quit)
def test_init():
    init(InitFlags.EVERYTHING)
    # everything should include these
    assert was_init(InitFlags.TIMER|InitFlags.AUDIO|
                    InitFlags.VIDEO|InitFlags.JOYSTICK|
                    InitFlags.HAPTIC)

@with_setup(quit)
def test_quit():
    init(InitFlags.EVERYTHING)
    quit()
    assert was_init(0) == 0

@with_setup(quit)
def test_init_sub_system():
    init_sub_system(InitFlags.TIMER)
    assert was_init(InitFlags.TIMER)

@with_setup(quit)
def test_quit_sub_system():
    init_sub_system(InitFlags.TIMER)
    assert was_init(InitFlags.TIMER)
    quit_sub_system(InitFlags.TIMER)
    assert not was_init(InitFlags.TIMER)

def test_version():
    v = get_version()
    assert repr(v).startswith('Version')
    assert str(v).startswith('1.3')
    assert v.major == 1 and v.minor == 3

def test_revision():
    assert get_revision().startswith('hg')
