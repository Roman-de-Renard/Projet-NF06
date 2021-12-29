import ctypes as ct


class Plane(ct.Structure):
    _fields_ = [
        ("plane_type", ct.c_char_p),
        ("max_capacity", ct.c_int)
    ]

    def __init__(self, plane_type: str, max_capacity: int):
        self.plane_type = bytes(plane_type, 'utf-8')
        self.max_capacity = ct.c_int(max_capacity)

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

    # def __init__(self, number: str, departure_city: str, arrival_city: str,
    #              attributed_plane: Plane, min_capacity: int, max_capacity: int):
    #     self.number = bytes(number, 'utf-8')
    #     self.departure_city = bytes(departure_city, 'utf-8')
    #     self.arrival_city = bytes(arrival_city, 'utf-8')
    #     self.attributed_plane = attributed_plane
    #     self.min_capacity = ct.c_int(min_capacity)
    #     self.max_capacity = ct.c_int(max_capacity)

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

    def __init__(self, frequency: int, possible_planes: list, departure_city: str,
                 arrival_city: str, min_capacity: int, max_capacity: int):
        self.frequency = ct.c_int(frequency)
        self.number_of_possible_planes = ct.c_int(len(possible_planes))
        self.possible_planes = (Plane * len(possible_planes))()
        for i, elem in enumerate(possible_planes):
            self.possible_planes[i] = elem
        self.departure_city = bytes(departure_city, 'utf-8')
        self.arrival_city = bytes(arrival_city, 'utf-8')
        self.min_capacity = ct.c_int(min_capacity)
        self.max_capacity = ct.c_int(max_capacity)


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

    def __init__(self, name: str, route_list: list, fleet: list, priority: int, dbd_calendar: list = None):
        self.name = bytes(name, 'utf-8')
        self.number_of_route = ct.c_int(len(route_list))
        self.route_list = (Route * len(route_list))()
        for i, elem in enumerate(route_list):
            self.route_list[i] = elem
        self.size_of_fleet = ct.c_int(len(fleet))
        self.fleet = (Plane * len(fleet))()
        for i, elem in enumerate(fleet):
            self.fleet[i] = elem
        self.priority = ct.c_int(priority)
        if dbd_calendar:
            self.dbd_calendar = (Day * (17 * 7))()
            for i, elem in enumerate(dbd_calendar):
                self.dbd_calendar[i] = elem
        else:
            self.dbd_calendar = ct.pointer(Day())

    def __lt__(self, other):
        return self.priority > other.priority


class Gate(ct.Structure):
    _fields_ = [
        ("availability", ct.c_int * 24 * 119),
        ("assigned_flights", Flight * 24 * 119)
    ]

    def __init__(self, availability: list = None, assigned_flights: list = None):
        if not availability:
            availability = [[ct.c_int(0)] * 24 for i in range(17 * 7)]
        if not assigned_flights:
            assigned_flights = [[Flight()] * 24 for i in range(17 * 7)]

        self.availability = (ct.c_int * 24 * (17 * 7))()
        self.assigned_flights = (Flight * 24 * (17 * 7))()
        for i in range(17 * 7):
            for j in range(24):
                self.availability[i][j] = availability[i][j]
                self.assigned_flights[i][j] = assigned_flights[i][j]
        # print("Created gate")
