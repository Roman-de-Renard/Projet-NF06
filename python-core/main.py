"""
 :file main.py
 :author Martin Guérout et Roman Robin
 :date 30/12/2020
 Code principal utilisées dans le cadre du projet de NF06 en automne 2021

"""

from pathlib import Path
from c_structures import *
from constants import *
import data_management


def open_dll(name='libc_libs.dll'):
    """
    fonction permettant d'utiliser les fonction de la librairie partagée
    :param name:nom du dossier contenant la librairie partagée
    :return:le chemin vers le fichier ouvert et prêt à utiliser
    """
    lib_path = Path().absolute().parent
    lib_path = lib_path / 'c_libs' / 'cmake-build-debug' / name
    return ct.CDLL(lib_path.as_posix())


def input_plane():
    return Plane(input("Type de l'avion : "), int(input("Capacité maximale de l'avion")))


def input_airline():
    fleet = []
    routes = []
    name = input("Nom de la compagnie aérienne : ")
    priority = int(input("Niveau de priorité de la compagnie aérienne (entier) : "))
    user_input = ""
    while user_input != "n":
        user_input = input("Ajouter un avion a la flotte ? y/n : ")
        if user_input == "y":
            fleet.append(input_plane())
    user_input = ""
    while user_input != "n":
        user_input = input("Ajouter un itinéraire à la compagnie ? y/n : ")
        if user_input == "y":
            frequency = int(input("Fréquence de l'itinéraire (0=quotidien, 1=hebdomadaire, 2=mensuel) : "))
            possible_planes = []
            user_input_2 = ""
            while user_input_2 != "n":
                user_input_2 = input("Ajouter un avion possible pour l'itinéraire ? y/n : ")
                if user_input_2 == "y":
                    possible_planes.append(input_plane())
            depcity = input("Nom de la ville de départ : ")
            arrcity = input("Nom de la ville d'arrivée : ")
            mincap = int(input("Capacité minimale d'opération de l'itinéraire"))
            maxcap = int(input("Capacité maximale d'opération de l'itinéraire"))
            routes.append(Route(frequency, possible_planes, depcity, arrcity, mincap, maxcap))
    return Airline(name, routes, fleet, priority)


def testing():
    # ---------------Creation of test airlines and its parameters--------------
    planes = [Plane("Airbus A320", 258),
              Plane("Boeing 747", 182),
              Plane("Airbus A380", 300),
              Plane("Boeing 737", 155),
              Plane("Cessna", 6)]
    cities = ["Paris", "Tokyo", "London", "Troyes"]
    routes = [
        Route(0, [planes[1], planes[3]], cities[0], cities[2], 150, 200),
        Route(1, [planes[0], planes[2]], cities[0], cities[1], 250, 290),
        Route(2, [planes[4], planes[1], planes[3]], cities[0],
              cities[3], 2, 5)
    ]

    test_airlines = [Airline("WTF Airways", routes, planes, 1)
                     ]
    test_airlines.sort()

    # ---------------Test run of c_lib.planning---------------
    for i in range(len(test_airlines)):
        calendar = c_lib.planning(ct.pointer(test_airlines[i]))
    for i in range(17 * 7):
        print(i, " : ", test_airlines[0].dbd_calendar[i])

    # ---------------Test run of data_management---------------
    # calendar_flights_dataframe = data_management.frame_planned_flights(calendar, True,
    #                                                                    "D:/Documents/NF06/Projet-NF06/planning.csv")
    # calendar_planes_dataframe = data_management\
    #     .frame_available_planes(calendar, True, "D:/Documents/NF06/Projet-NF06/available_planes.csv")
    # calendar2 = data_management.calendar_from_dataframes(calendar_flights_dataframe, calendar_planes_dataframe)
    # print(calendar2)

    # # ---------------Test run of c_lib.gate_assignment---------------

    Gate_0 = Gate()
    Gate_1 = Gate()
    gates = [
        Gate_0,
        Gate_1
    ]
    c_gates = (Gate * len(gates))(*gates)
    c_test_airlines = (Airline * len(test_airlines))(*test_airlines)

    # ---------------Test run of c_lib.gate_assignment---------------
    c_lib.gate_assignment(len(test_airlines), c_test_airlines, len(gates), c_gates)

    for i in range(2):  # on vérifie que la fonction renvoie bien les information en python
        for j in range(119):
            for k in range(24):
                print("Door {}, day {}, hour {} : Availability : {}".format(i, j, k, c_gates[i].availability[j][k]))


if __name__ == '__main__':
    c_lib = open_dll()
    c_lib.planning.argtypes = [ct.POINTER(Airline)]
    c_lib.planning.restype = ct.POINTER(Day)
    c_lib.gate_assignment.argtypes = (ct.c_long, ct.POINTER(Airline), ct.c_long, ct.POINTER(Gate))
    c_lib.gate_assignment.restype = ct.POINTER(Gate)

    airlines = []
    uinput = ""
    while uinput != "n":
        uinput = input("Voulez-vous ajouter une compagnie aérienne ? y / n : ")
        if uinput == "y":
            airlines.append(input_airline())
    airlines.sort()
    c_airlines = (Airline * len(airlines))(*airlines)

    for i in range(len(airlines)):
        c_lib.planning(c_airlines[i])

    uinput = input("Voulez-vous enregistrer les plannings dans des fichiers .csv ? y/n : ")
    if uinput == "y":
        uinput1 = input("Chemin du dossier dans lequel les enregistrer (utilisant '/, y compris celui de fin) : ")
        for i in range(len(airlines)):
            data_management.frame_planned_flights(c_airlines[i].dbd_calendar, tocsv=True,
                                                  filename=uinput1+c_airlines[i].name+"-planned_flights.csv")
            data_management.frame_available_planes(c_airlines[i].dbd_calendar, tocsv=True,
                                                   filename=uinput1+c_airlines[i].name+"-available_planes.csv")

