from pathlib import Path
from c_structures import *


def open_dll(name='libc_libs.dll'):
    # on remonte sur le dossier du projet
    lib_path = Path().absolute().parent
    # et on redescend l'arborescence dans le dossier du code C
    lib_path = lib_path / 'c_libs' / 'cmake-build-debug' / name
    # puis on ouvre la librairie partagée avec ctypes et on la retourne
    return ct.CDLL(lib_path.as_posix())


def assign_plane_value(airline, flight, plane):  # permet d'assigner les valeurs d'entrée
    user_input = ""
    user_input1 = ""
    user_input2 = ""
    airline_list = []
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
    # assign_plane_value(Airline, Flight, Plane)
    # foo = ct.c_int(3)
    # bar = ct.c_int(6)
    # print(c_lib.add_int(foo, bar))
    # print("Wesh alors")
    # print("Salut c'est moi, tchoupi")
    # c_lib.print_hello()
    our_plane = [(Plane(b"Airbus A320", ct.c_int(258)),
                  Plane(b"Boeing 747", ct.c_int(196)))]  # b"foo" allows to convert the string into a bytes object
    # # (necessary for ctypes)
    # c_lib.print_plane(our_plane)
    list_of_planes = [Plane(b"Airbus A320", ct.c_int(170)), Plane(b"Boeing 747", ct.c_int(196))]
    c_planes = (Plane * len(list_of_planes))()
    # listofplanes = l()
    for i, elem in enumerate(list_of_planes):
        c_planes[i] = elem

    # for i, p in enumerate(our_plane:
    #     listofplanes[i] = p
    our_flight = Flight(b"4402FE", ct.c_int(1), ct.c_int(2), c_planes, ct.c_int(150), ct.c_int(300))
    c_lib.print_flight(our_flight)  # It works !
