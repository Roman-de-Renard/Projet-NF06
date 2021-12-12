import ctypes as ct


class Plane(ct.Structure):
    _fields_ = [
        ("plane_type", ct.c_char_p),
        ("max_capacity", ct.c_int)
    ]


class Flight(ct.Structure):
    _fields_ = [
        ("number", ct.c_char * 7),
        ("departure_city", ct.c_char_p),
        ("arrival_city", ct.c_char_p),
        ("attributed_plane", Plane),
        ("min_capacity", ct.c_int),
        ("max_capacity", ct.c_int)
    ]


class Day(ct.Structure):
    _fields_ = [
        ("number_of_planned_flights", ct.c_int),
        ("flights_of_the_day", ct.POINTER(Flight)),
        ("number_of_available_planes", ct.c_int),
        ("available_planes", ct.POINTER(Plane))
    ]


class Route(ct.Structure):
    _fields_ = [
        ("frequency", ct.c_int),
        ("number_of_possible_planes", ct.c_int),
        ("possible_planes", ct.POINTER(Plane)),
        ("departure_city", ct.c_char_p),
        ("arrival_city", ct.c_char_p),
        ("min_capacity", ct.c_int),
        ("max_capacity", ct.c_int)
    ]


class Airline(ct.Structure):
    _fields_ = [
        ("name", ct.c_char_p),
        ("number_of_route", ct.c_int),
        ("route_list", ct.POINTER(Route)),
        ("size_of_fleet", ct.c_int),
        ("fleet", ct.POINTER(Plane)),
        ("priority", ct.c_int),
        ("dbd_calendar", ct.POINTER(Day))
    ]
