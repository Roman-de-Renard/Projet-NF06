import ctypes as ct


class Plane(ct.Structure):
    """
    Classe Plane, heritee de ctypes.Structure. Classe "wrapper" pour la structure "plane" de library.c, memes attributs.
    """
    _fields_ = [
        ("plane_type", ct.c_char_p),
        ("max_capacity", ct.c_int)
    ]

    def __init__(self, plane_type: str, max_capacity: int):
        """
        Methode d'initialisation de la classe.
        :param plane_type : str correspondant au type de l'avion. Converti en objet "bytes" par la methode.
        :param max_capacity : int correspondant a la capacite maximale de l'avion.
        Converti en ct.c_int par la methode
        """
        self.plane_type = bytes(plane_type, 'utf-8')
        self.max_capacity = ct.c_int(max_capacity)

    def __repr__(self):

        """
        Methode de print de la classe.
        :return Un str formatte avec le type et la capacite maximale de l'avion
        """
        face = "{}, capacite max {}".format(self.plane_type, self.max_capacity)
        return face


class Flight(ct.Structure):
    """
    Classe Flight, heritee de ctypes.Structure.
    Classe "wrapper" pour la structure "flight" de library.c, memes attributs.
    """
    _fields_ = [
        ("number", ct.c_char * 7),
        ("departure_city", ct.c_char_p),
        ("arrival_city", ct.c_char_p),
        ("attributed_plane", Plane),
        ("min_capacity", ct.c_int),
        ("max_capacity", ct.c_int)
    ]

    def __str__(self):
        """
        Methode de formatage en str de la classe.
        :return Un str formate contenant tous les attributs du vol.
        """
        face = "Vol {}, au depart de {} et arrivant a {}, dans un {} et avec une capacite de {} a {} passagers.".format(
            self.number, self.departure_city, self.arrival_city,
            self.attributed_plane, self.min_capacity, self.max_capacity)
        return face


class Day(ct.Structure):
    """
    Classe Day, heritee de ctypes.Structure.
    Classe "wrapper" pour la structure "day" de library.c, memes attributs.
    """
    _fields_ = [
        ("number_of_planned_flights", ct.c_int),
        ("flights_of_the_day", ct.POINTER(Flight)),
        ("number_of_available_planes", ct.c_int),
        ("available_planes", ct.POINTER(Plane))
    ]

    def __str__(self):
        """
        Methode de formatage en str de la classe.
        :return Un str formate contenant tous les attributs du jour.
        """
        face = ""
        face += "Il y a {} vols prevus ce jour : \n".format(self.number_of_planned_flights)
        for i in range(self.number_of_planned_flights):
            face += "   -{}\n".format(self.flights_of_the_day[i])
        face += "Il reste {} avions disponibles ce jour : \n".format(self.number_of_available_planes)
        for i in range(self.number_of_available_planes):
            face += "   -{}\n".format(self.available_planes[i])
        return face


class Route(ct.Structure):
    """
    Classe Route, heritee de ctypes.Structure.
    Classe "wrapper" pour la structure "route" de library.c, memes attributs.
    """
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
        """
        Methode d'initialisation de la classe.
        =>Tous les parametres de type int sont convertis en ct.c_int par la methode.
        =>Tous les parametres de type str sont convertis en bytes par la methode.
        :param frequency : int correspondant a la frequence de l'itineraire. Trois valeurs possibles :
            0 : quotidien
            1 : hebdomadaire
            2 : mensuel
        :param possible_planes : liste des Plane pouvant effectuer les vols d'un itineraire.
            Convertie en ct.Array par la methode.
        :param departure_city : str correspondant a la ville de depart de l'itineraire.
        :param arrival_city : str correspondant a la ville d'arrivee de l'itineraire.
        :param min_capacity : int correspondant a la capacite minimale des vols sur l'itineraire.
        :param max_capacity : int correspondant a la capacite maximale des vols sur l'itineraire.
        """
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
    """
    Classe Airline, heritee de ctypes.Structure.
    Classe "wrapper" pour la structure "airline" de library.c, memes attributs.
    """
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
        """
        Methode d'initialisation de la classe.
        =>Tous les parametres de type int sont convertis en ct.c_int par la methode.
         =>Tous les parametres de type str sont convertis en bytes par la methode.
        :param name : str contenant le nom de la compagnie aerienne.
        :param route_list: liste des Route de la compagnie
            Convertie en ct.Array par la methode.
        :param fleet : liste des Plane de la compagnie.
            Convertie en ct.Array par la methode.
        :param priority : indice de priorite de la compagnie.
            Permet de determiner sont ordre de priorite dans l'attribution des vols aux portes.
        :param dbd_calendar : liste de Day, correspond au calendrier de Day deja planifies pour la compagnie.
            Par defaut None.
        """
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
        """
        Methode de comparaison de la classe. Compare le self.priority des deux objets.
        :param other: autre Airline avec laquelle comparer self.
        :return: Booleen resultat de la comparaison
        """
        self.priority > other.priority


class Gate(ct.Structure):
    """
    Classe Gate, heritee de ctypes.Structure.
    Classe "wrapper" pour la structure "gate" de library.c, memes attributs.
    """
    _fields_ = [
        ("availability", ct.c_int * 24 * 119),
        ("assigned_flights", Flight * 24 * 119)
    ]

    def __init__(self, availability: list = None, assigned_flights: list = None):
        """
        Methode d'initialisation de la classe.
        :param availability: liste de NB_DAYS listes de 24 int, correspondant a la disponibilite de la porte.
            Converti en ct.Array par la methode. Par defaut None.
        :param assigned_flights: liste de NB_DAYS listes de 24 Flight, correspondant aux vols assignes de la porte.
            Converti en ct.Array par la methode. Par defaut None.
        """
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
