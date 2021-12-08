import ctypes as ct


class Plane(ct.Structure):
    _fields_ = [
        ("plane_type", ct.c_char_p),
        ("max_capacity", ct.c_int)
    ]


class Flight(ct.Structure):
    _fields_ = [
        ("number", ct.c_char * 7),
        ("frequency", ct.c_int),
        ("number_of_possible_planes", ct.c_int),
        ("possible_planes", ct.POINTER(Plane)),  # Might become a problem, pointer to only the first element
        ("min_capacity", ct.c_int),
        ("max_capacity", ct.c_int)
    ]

    # def __init__(self, f, n):
    #     # self.number = ct.c_char_p()
    #     self.number_of_possible_planes = ct.c_int(f)


class Airline(ct.Structure):
    _fields_ = [
        ("name", ct.c_char_p),
        ("number_of_flights", ct.c_int),
        # ("fleet", ct.POINTER(Plane)),
        ("flight_list", ct.POINTER(Flight)),
        ("priority", ct.c_int)
    ]
