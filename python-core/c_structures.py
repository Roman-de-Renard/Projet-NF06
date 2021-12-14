import ctypes as ct


class Plane(ct.Structure):
    _fields_ = [
        ("plane_type", ct.c_char_p),
        ("max_capacity", ct.c_int)
    ]

    def __repr__(self):
        face = "{}, capacite max {}".format(self.plane_type, self.max_capacity)
        return face


class Flight(ct.Structure):
    _fields_ = [
        ("number", ct.c_char * 7),
        ("departure_city", ct.c_char_p),
        ("arrival_city", ct.c_char_p),
        ("attributed_plane", Plane),
        ("min_capacity", ct.c_int),
        ("max_capacity", ct.c_int)
    ]

    def __str__(self):
        face = "Vol {}, au depart de {} et arrivant a {}, dans un {} et avec une capacite de {} a {} passagers.".format(
            self.number, self.departure_city, self.arrival_city,
            self.attributed_plane, self.min_capacity, self.max_capacity)
        return face


class Day(ct.Structure):
    _fields_ = [
        ("number_of_planned_flights", ct.c_int),
        ("flights_of_the_day", ct.POINTER(Flight)),
        ("number_of_available_planes", ct.c_int),
        ("available_planes", ct.POINTER(Plane))
    ]

    def __str__(self):
        face = ""
        face += "Il y a {} vols prevus ce jour : \n".format(self.number_of_planned_flights)
        for i in range(self.number_of_planned_flights):
            face += "   -{}\n".format(self.flights_of_the_day[i])
        face += "Il reste {} avions disponibles ce jour : \n".format(self.number_of_available_planes)
        for i in range(self.number_of_available_planes):
            face += "   -{}\n".format(self.available_planes[i])
        return face


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
