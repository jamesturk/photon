from .. import init, InitFlags
from ..keyboard import (get_mod_state, set_mod_state, get_key_from_scancode,
                        get_scancode_from_key, get_key_name, get_scancode_name,
                        Scancode, Keycode)
from nose.tools import with_setup

_keys = [
    # scancode, keycode, name
    (Scancode.RETURN, Keycode.RETURN, 'Return'),
    (Scancode.A, Keycode.a, 'A'),
    (Scancode.KP_PLUS, Keycode.KP_PLUS, 'Keypad +'),
    (Scancode.LSHIFT, Keycode.LSHIFT, 'Left Shift')
]

def init_everything():
    init(InitFlags.EVERYTHING)

@with_setup(init_everything)
def test_mod_state():
    pass # TODO

@with_setup(init_everything)
def test_get_key_from_scancode():
    for scan, key, name in _keys:
        assert get_key_from_scancode(scan) == key

@with_setup(init_everything)
def test_get_scancode_from_key():
    for scan, key, name in _keys:
        assert get_scancode_from_key(key) == scan

@with_setup(init_everything)
def test_get_key_name():
    for scan, key, name in _keys:
        assert get_key_name(key) == name

@with_setup(init_everything)
def test_get_scancode_name():
    for scan, key, name in _keys:
        assert get_scancode_name(scan) == name
