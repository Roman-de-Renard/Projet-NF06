from pathlib import Path
from c_structures import *
from constants import *
import data_management


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
    c_lib.gate_assignment.argtypes = (ct.c_long, ct.POINTER(Airline), ct.c_long, ct.POINTER(Gate))
    c_lib.gate_assignment.restype = ct.POINTER(Gate)

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
    test_airlines = [Airline("WTF Airways", routes, planes, 1), Airline("SHIT", routes, planes, 3)
                     ]
    test_airlines.sort()


    # ---------------Test run of c_lib.planning---------------
    calendar = c_lib.planning(ct.pointer(test_airlines[0]))
    for i in range(17 * 7):
        print(i, " : ", test_airlines[0].dbd_calendar[i])

    # ---------------Test run of data_management---------------
    calendar_flights_dataframe = data_management.frame_planned_flights(calendar, True,
                                                                       "D:/Documents/NF06/Projet-NF06/planning.csv")
    calendar_planes_dataframe = data_management\
        .frame_available_planes(calendar, True, "D:/Documents/NF06/Projet-NF06/available_planes.csv")
    calendar2 = data_management.calendar_from_dataframes(calendar_flights_dataframe, calendar_planes_dataframe)
    print(calendar2)

    # # ---------------Creation of objects necessary for test of gate assignment----------------
    # empty_availability = [[0] * 24 for i in range(NB_DAYS)]
    # empty_flights = [[ct.pointer(Flight()) for _ in range(24)] for _ in range(NB_DAYS)]
    # Gate_0 = Gate()
    # Gate_0.availability = (ct.POINTER(ct.c_int) * NB_DAYS)()
    # for i, day in enumerate(empty_availability):
    #     Gate_0.availability[i] = (ct.c_int * 24)()
    #     for j, hour in enumerate(day):
    #         Gate_0.availability[i][j] = hour
    # Gate_0.assigned_flights = (ct.POINTER(ct.POINTER(Flight)) * NB_DAYS)()
    # for i, day in enumerate(empty_flights):
    #     Gate_0.assigned_flights[i] = (ct.POINTER(Flight) * 24)()
    #     for j, hour in enumerate(day):
    #         Gate_0.assigned_flights[i][j] = hour
    # Gate_1 = Gate()
    # Gate_1.availability = (ct.POINTER(ct.c_int) * NB_DAYS)()
    # for i, day in enumerate(empty_availability):
    #     Gate_1.availability[i] = (ct.c_int * 24)()
    #     for j, hour in enumerate(day):
    #         Gate_1.availability[i][j] = hour
    # Gate_1.assigned_flights = (ct.POINTER(ct.POINTER(Flight)) * NB_DAYS)()
    # for i, day in enumerate(empty_flights):
    #     Gate_1.assigned_flights[i] = (ct.POINTER(Flight) * 24)()
    #     for j, hour in enumerate(day):
    #         Gate_1.assigned_flights[i][j] = hour
    # gates = [
    #     Gate_0,
    #     Gate_1
    # ]
    # c_gates = (Gate * len(gates))(*gates)
    # c_test_airlines = (Airline * len(test_airlines))(*test_airlines)
    #
    # # ---------------Test run of c_lib.gate_assignment---------------
    # new_c_gates = c_lib.gate_assignment(len(test_airlines), c_test_airlines, len(gates), c_gates)
    # print(type(c_gates))
    # for i in range(2): #on vérifie que la fonction renvoie bien les information en python
    #     for j in range(119):
    #         for k in range(24):
    #             print("Door {}, day {}, hour {} : Availability : {}".format(i, j, k, new_c_gates[i].availability[j][k]))
    Gate_0 = Gate()
    Gate_1 = Gate()
    gates = [
        Gate_0,
        Gate_1
    ]
    c_gates = (Gate * len(gates))(*gates)
    c_test_airlines = (Airline * len(test_airlines))(*test_airlines)

    # ---------------Test run of c_lib.gate_assignment---------------
    c_gates = c_lib.gate_assignment(len(test_airlines), c_test_airlines, len(gates), c_gates)
    print(type(c_gates))
    for i in range(2):  # on vérifie que la fonction renvoie bien les information en python
        for j in range(119):
            for k in range(24):
                print("Door {}, day {}, hour {} : Availability : {}".format(i, j, k, c_gates[i].availability[j][k]))
