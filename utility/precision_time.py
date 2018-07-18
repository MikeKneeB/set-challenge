import ctypes, os

CLOCK_MONOTONIC_RAW = 4 # see <linux/time.h> here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h

#prepare ctype timespec structure of {long, long}
class timespec(ctypes.Structure):
    _fields_ =\
    [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]

#Configure Python access to the clock_gettime C library, via ctypes:
#Documentation:
#-ctypes.CDLL: https://docs.python.org/3.2/library/ctypes.html
#-librt.so.1 with clock_gettime: https://docs.oracle.com/cd/E36784_01/html/E36873/librt-3lib.html #-
#-Linux clock_gettime(): http://linux.die.net/man/3/clock_gettime
librt = ctypes.CDLL('librt.so.1', use_errno=True)
clock_gettime = librt.clock_gettime
#specify input arguments and types to the C clock_gettime() function
# (int clock_ID, timespec* t)
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

def monotonic_time():
    "return a timestamp in seconds (sec)"
    t = timespec()
    #(Note that clock_gettime() returns 0 for success, or -1 for failure, in
    # which case errno is set appropriately)
    #-see here: http://linux.die.net/man/3/clock_gettime
    if clock_gettime(CLOCK_MONOTONIC_RAW , ctypes.pointer(t)) != 0:
        #if clock_gettime() returns an error
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    return t.tv_sec + t.tv_nsec*1e-9 #sec

def micros():
    "return a timestamp in microseconds (us)"
    return monotonic_time()*1e6 #us

def millis():
    "return a timestamp in milliseconds (ms)"
    return monotonic_time()*1e3 #ms 
