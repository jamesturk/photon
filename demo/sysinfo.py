from __future__ import print_function
from csdl import sysinfo

def main():
    print('Platform:', sysinfo.get_platform())
    print('CPU count:', sysinfo.get_cpu_count())
    print('CPU cache line size:', sysinfo.get_cpu_cache_line_size())
    print(' has 3DNow:', sysinfo.has_3DNow())
    print(' has AltiVec:', sysinfo.has_AltiVec())
    print(' has MMX:', sysinfo.has_MMX())
    print(' has RDTSC:', sysinfo.has_RDTSC())
    print(' has SSE:', sysinfo.has_SSE())
    print(' has SSE2:', sysinfo.has_SSE2())
    print(' has SSE3:', sysinfo.has_SSE3())
    print(' has SSE4.1:', sysinfo.has_SSE41())
    print(' has SSE4.2:', sysinfo.has_SSE42())
    state, seconds, percent = sysinfo.get_power_info()
    print('Power:', state, end=' ')
    if seconds:
        print(seconds, 's remaining', sep='', end=' ')
    else:
        print('unknown time', end=' ')
    if percent:
        print(percent, '%', sep='')
    else:
        print('unknown %')

if __name__ == '__main__':
    main()
