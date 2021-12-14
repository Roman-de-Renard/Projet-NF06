from pathlib import Path
from c_structures import *


def open_dll(name='libc_libs.dll'):
    # on remonte sur le dossier du projet
    lib_path = Path().absolute().parent
    # et on redescend l'arborescence dans le dossier du code C
    lib_path = lib_path / 'c_libs' / 'cmake-build-debug' / name
    # puis on ouvre la librairie partagée avec ctypes et on la retourne
    return ct.CDLL(lib_path.as_posix())


def assign_plane_value(airline_list, airline, flight, plane):  # permet d'assigner les valeurs d'entrée
    user_input = ""
    user_input1 = ""
    user_input2 = ""
    airline.flight_list = []
    airline.fleet = []
    airline.number_of_flight = 0
    while user_input != "n":
        user_input = input("Voulez vous créer une compagnie? (y/n)")
        if user_input == "n":
            break
        if user_input == "y":
            airline.name = input("entrer le nom de la compagnie: ")
            while user_input1 != "n":
                user_input1 = input("Voulez vous ajoutez un avion à la flotte? (y/n)")
                if user_input1 == "n":
                    break
                plane.type = input("Quel est le type de l'avion")
                plane.max_capacity = input("Quel est la capacité maximum de l'avion?")
                airline.fleet.append(plane)
            while user_input2 != "n":
                user_input2 = input("Voulez vous ajoutez un vol? (y/n)")
                if user_input2 == "n":
                    break
                airline.number_of_flight += 1
                flight.number = input("Entrez le numéro du vol")
                flight.frequency = int(input("Entrez la fréquence du vol"))
                flight.min_capacity = int(input("Entrez la capacite minimal du vol"))
                flight.max_capacity = int(input("Entrez la capacite maximal du vol"))
                airline.flight_list.append(flight)
        airline_list.append(airline)


if __name__ == '__main__':
    c_lib = open_dll()
    c_lib.planning.argtypes = [ct.POINTER(Airline)]
    c_lib.planning.restype = ct.POINTER(Day)
    # assign_plane_value(Airline, Flight, Plane)
    # foo = ct.c_int(3)
    # bar = ct.c_int(6)
    # print(c_lib.add_int(foo, bar))
    # print("Wesh alors")
    # print("Salut c'est moi, tchoupi")
    # c_lib.print_hello()
    planes = [Plane(b"Airbus A320", ct.c_int(258)),  # Les Plane qui existent (PAS UN ARGUMENT)
              Plane(b"Boeing 747", ct.c_int(182)),
              Plane(b"Airbus A380", ct.c_int(300)),
              Plane(b"Boeing 737", ct.c_int(155)),
              Plane(b"Cessna", ct.c_int(6))]  # b"foo" allows to convert the string into a bytes object

    c_planes = (Plane * len(planes))()
    for i, elem in enumerate(planes):
        c_planes[i] = elem
    cities = [b"Paris", b"Tokyo", b"London", b"Troyes"]
    c_cities = (ct.c_char_p * len(cities))()
    for i, elem in enumerate(cities):
        c_cities[i] = elem
    routes = [
        Route(0, 2, (Plane * 2)(c_planes[1], c_planes[3]), c_cities[0], c_cities[3],
              ct.c_int(150), ct.c_int(200)),
        Route(1, 1, (Plane * 1)(c_planes[3]), c_cities[1], c_cities[0],
              ct.c_int(250), ct.c_int(290)),
        Route(2, 3, (Plane * 3)(c_planes[4], c_planes[1], c_planes[3]), c_cities[0],
              c_cities[3], ct.c_int(2), ct.c_int(5))
    ]
    c_routes = (Route * len(routes))()
    for i, elem in enumerate(routes):
        c_routes[i] = elem
    test_airline = Airline(b"WTF Airways", ct.c_int(3), c_routes, ct.c_int(5), c_planes, ct.c_int(3),
                           ct.pointer(Day()))
    calendar = c_lib.planning(ct.byref(test_airline))
    for i in range(155):
        print(i, " : ", calendar[i].number_of_planned_flights)
