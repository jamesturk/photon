from nose.tools import with_setup, raises

from ..internal import _SDL, errcheck, Version, SDLError

def setup_func():
    _SDL.SDL_ClearError()

@with_setup(setup_func)
def test_errcheck_noerr():
    # set an error to ensure that errors aren't cleared
    _SDL.SDL_SetError("test")
    assert errcheck(2) == 2   # positive values should pass through
    assert errcheck(0) == 0   # as should zero
    assert _SDL.SDL_GetError() == "test"

@raises(SDLError)
@with_setup(setup_func)
def test_errcheck_err():
    _SDL.SDL_SetError("err!")
    try:
        errcheck(-1)    # negative values should trigger the SDLError
    except SDLError as e:
        assert str(e) == "err!"
        raise           # reraise error
