import ctypes as ct


class flight(ct.Structure):
    _fields_ = [
        ("number", ct.c_char * 7),
        ("frequency", ct.c_int),
        ()
    ]
