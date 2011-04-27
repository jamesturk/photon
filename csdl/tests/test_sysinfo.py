from .. import sysinfo

def test_get_platform():
    assert isinstance(sysinfo.get_platform(), str)

def test_cpu_info():
    assert sysinfo.get_cpu_cache_line_size() > 0
    assert sysinfo.get_cpu_count() > 0

def test_power_info():
    state, seconds, percent = sysinfo.get_power_info()
    assert state in ('UNKNOWN', 'ON_BATTERY', 'NO_BATTERY', 'CHARGING',
                     'CHARGED')
    assert isinstance(seconds, int)
    assert isinstance(percent, int)
