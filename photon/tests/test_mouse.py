from .. import init, InitFlags
from ..internal import SDLError
from ..mouse import (get_relative_mouse_mode, set_relative_mouse_mode,
                     set_cursor_visibility, is_cursor_visible)
from nose.tools import with_setup

def init_everything():
    init(InitFlags.EVERYTHING)

@with_setup(init_everything)
def test_relative_mouse_mode():
    try:
        set_relative_mouse_mode(True)
        assert get_relative_mouse_mode() == True
        set_relative_mouse_mode(False)
        assert get_relative_mouse_mode() == False
    except SDLError:
        pass  # sometimes this method isn't supported

@with_setup(init_everything)
def test_cursor_visiblity():
    assert is_cursor_visible() == True
    set_cursor_visibility(False)
    assert is_cursor_visible() == False
    set_cursor_visibility(True)
    assert is_cursor_visible() == True

