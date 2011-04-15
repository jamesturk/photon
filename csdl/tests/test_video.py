from csdl import init, InitFlags
from csdl import video
from nose.tools import with_setup
import time

def video_setup():
    init(InitFlags.VIDEO)

def test_get_render_drivers():
    driver_list = video.get_render_drivers()
    assert driver_list

    software = None
    for drv in driver_list:
        if drv.name == 'software':
            software = drv

    # software renderer should always be available
    assert software
    # texture formats should be non-zero
    assert all(software.texture_formats[0:software.num_texture_formats])

    assert repr(software) == "<RendererInfo 'software'>"

def test_rect_basics():
    r1 = video.Rect(0,0,10,10)
    r2 = video.Rect(0,0,10,10)

    # __eq__
    assert r1 == r2

    # is_empty
    assert video.Rect(1,2,3,0).is_empty()
    assert video.Rect(1,2,0,4).is_empty()
    assert not video.Rect(1,2,3,4).is_empty()

    # __repr__
    assert repr(r1) == 'Rect(0, 0, 10, 10)'


@with_setup(video_setup)
def test_window_title():
    w = video.Window("window_title_test", 10, 10, 50, 50)
    assert w.title == "window_title_test"
    w.title = "something completely different"
    assert w.title == "something completely different"
    w.destroy()

@with_setup(video_setup)
def test_window_size():
    w = video.Window("window_size_test", 10, 10, 50, 50)
    assert w.size == (50, 50)
    w.resize(100, 120)
    assert w.size == (100, 120)
    w.destroy()

@with_setup(video_setup)
def test_window_position():
    w = video.Window('window_position_test', 10, 10, 50, 50)
    assert w.position == (10, 10)
    w.move(100, 110)
    assert w.position == (100, 110)
    w.destroy()

@with_setup(video_setup)
def test_screensaver():
    enabled = video.is_screensaver_enabled()

    if enabled:
        video.disable_screensaver()
        assert not video.is_screensaver_enabled()
        video.enable_screensaver()
        assert video.is_screensaver_enabled()
    else:
        video.enable_screensaver()
        assert video.is_screensaver_enabled()
        video.disable_screensaver()
        assert not video.is_screensaver_enabled()


@with_setup(video_setup)
def test_video_info():
    # make sure both aren't blank
    assert video.get_num_video_displays()
    assert video.get_current_video_driver()

@with_setup(video_setup)
def test_gl_info():
    w = video.Window('window_position_test', 10, 10, 50, 50,
                     video.WindowFlags.OPENGL)

    for attr in video.GL_Attr:
        print('{0}: {1}'.format(repr(attr)[1:-1],
                               video.gl_get_attribute(attr)))
    print 'GL Swap Interval:', video.gl_get_swap_interval()

