from .. import init, InitFlags, timer
import time

def init_timer():
    init(InitFlags.TIMER)

def test_performance_counter():
    init_timer()
    first = timer.get_performance_counter()
    time.sleep(1.1)
    second = timer.get_performance_counter()
    freq = timer.get_performance_frequency()
    assert second > first
    assert second/freq > first/freq

def test_get_ticks():
    init_timer()
    first = timer.get_ticks()
    time.sleep(0.1)
    second = timer.get_ticks()
    assert second > first
    # delay should safely put it in this range
    assert 50 < second - first < 500

