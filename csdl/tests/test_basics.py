import csdl
from nose.tools import with_setup

def test_error_handling():
    # blank by default
    assert csdl.get_error() == ""

    # check set
    csdl.set_error("test!")
    assert csdl.get_error() == "test!"

    # check again, shouldn't clear
    assert csdl.get_error() == "test!"

    # clear again
    csdl.clear_error()
    assert csdl.get_error() == ""

@with_setup(csdl.quit)
def test_init():
    csdl.init(csdl.InitFlags.EVERYTHING)
    # everything should include these
    assert csdl.was_init(csdl.InitFlags.TIMER|csdl.InitFlags.AUDIO|
                         csdl.InitFlags.VIDEO|csdl.InitFlags.JOYSTICK|
                         csdl.InitFlags.HAPTIC)

@with_setup(csdl.quit)
def test_quit():
    csdl.init(csdl.InitFlags.EVERYTHING)
    csdl.quit()
    assert csdl.was_init(0) == 0

@with_setup(csdl.quit)
def test_init_sub_system():
    csdl.init_sub_system(csdl.InitFlags.TIMER)
    assert csdl.was_init(csdl.InitFlags.TIMER)

@with_setup(csdl.quit)
def test_quit_sub_system():
    csdl.init_sub_system(csdl.InitFlags.TIMER)
    assert csdl.was_init(csdl.InitFlags.TIMER)
    csdl.quit_sub_system(csdl.InitFlags.TIMER)
    assert not csdl.was_init(csdl.InitFlags.TIMER)

def test_version():
    v = csdl.get_version()
    assert repr(v).startswith('Version')
    assert str(v).startswith('1.3')
    assert v.major == 1 and v.minor == 3

def test_revision():
    assert csdl.get_revision().startswith('hg')
