import ctypes as ct
from pathlib import Path
from c_structures import *


def open_dll(name='libc_libs.dll'):
    # on remonte sur le dossier du projet
    lib_path = Path().absolute().parent
    # et on redescend l'arborescence dans le dossier du code C
    lib_path = lib_path / 'c_libs' / 'cmake-build-debug' / name
    # puis on ouvre la librairie partagée avec ctypes et on la retourne
    return ct.CDLL(lib_path.as_posix())


# def assign_plane_value(airline, flight):
#     global user_input
#     user_input: ""
#     airline.flight_list=()
#     while user_input != "n":
#         user_input = input("Voulez vous créer une compagnie? (y/n)")
#         if user_input == "y":
#             airline.name=input("entrer le nom de la caompagnie: ")
#             airline.number_of_flight=int(input("Combien de vol cette compagnie a?: "))
#             for i in range(0,airline.number_of_flight):
#                 flight.number=input("Entrez le numéro du vol")
#                 flight.frequency=int(input("Entrez la fréquence du vol"))
#                 n=int(input("Combien d'avion sont disponible pour assurer le vol"))


if __name__ == '__main__':
    c_lib = open_dll()

    foo = ct.c_int(3)
    bar = ct.c_int(6)
    print(c_lib.add_int(foo, bar))
    print("Wesh alors")
    print("Salut c'est moi, tchoupi")
    c_lib.print_hello()
    our_plane = Plane(b"Airbus A320", ct.c_int(258))  # b"foo" allows to convert the string into a bytes object
    # (necessary for ctypes)
    c_lib.print_plane(our_plane)
    listofplanes = (Plane * 2)(Plane(b"Airbus A320", ct.c_int(258)), Plane(b"Boeing 747", ct.c_int(196)))
    our_flight = Flight(b"4402FE", ct.c_int(1), ct.c_int(2), listofplanes, ct.c_int(150), ct.c_int(300))
    c_lib.print_flight(our_flight)  # It works !
