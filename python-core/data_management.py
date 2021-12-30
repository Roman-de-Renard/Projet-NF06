from c_structures import *
from constants import *
import pandas as pd

pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999


def frame_planned_flights(calendar: ct.POINTER(Day), tocsv: bool = False, filename: str = "") -> pd.DataFrame:
    """
    Renvoie un DataFrame pandas à partir d'un calendar.
    Ce DataFrame constion toutes les information sur les vols planifiés
    :param calendar: le calendrier à transformer en dataframe
    :param tocsv: True pour exporter le dataframe vers un fichier CSV
    :param filename: le path et le nom du fichier CSV si tocsv est True
    :return: Le DataFrame contenant les vols planifiés du calendar
    """
    planned_flights = {
        "day": [],
        "number": [],
        "departure_city": [],
        "arrival_city": [],
        "plane_type": [],
        "plane_maxcap": [],
        "min_capacity": [],
        "max_capacity": []
    }
    for i in range(NB_DAYS):
        for j in range(calendar[i].number_of_planned_flights):
            planned_flights["day"].append(i)
            planned_flights["number"].append(calendar[i].flights_of_the_day[j].number.decode())
            planned_flights["departure_city"].append(calendar[i].flights_of_the_day[j].departure_city.decode())
            planned_flights["arrival_city"].append(calendar[i].flights_of_the_day[j].arrival_city.decode())
            planned_flights["plane_type"].append(calendar[i].flights_of_the_day[j].attributed_plane.plane_type.decode())
            planned_flights["plane_maxcap"].append(calendar[i].flights_of_the_day[j].attributed_plane.max_capacity)
            planned_flights["min_capacity"].append(calendar[i].flights_of_the_day[j].min_capacity)
            planned_flights["max_capacity"].append(calendar[i].flights_of_the_day[j].max_capacity)

    planned_flights_dataframe = pd.DataFrame(planned_flights)
    if tocsv:
        planned_flights_dataframe.to_csv(filename)
    return planned_flights_dataframe


def frame_available_planes(calendar: ct.POINTER(Day), tocsv: bool = False, filename: str = "") -> pd.DataFrame:
    """
    Renvoie un DataFrame pandas à partir d'un calendar.
    Ce DataFrame constion toutes les information sur les avions disponibles
    :param calendar: le calendrier à transformer en dataframe
    :param tocsv: True pour exporter le dataframe vers un fichier CSV
    :param filename: le path et le nom du fichier CSV si tocsv est True
    :return: Le DataFrame contenant les avions disponibles du calendar
    """
    available_planes = {
        "day": [],
        "plane_type": [],
        "max_capacity": []
    }
    for i in range(NB_DAYS):
        for j in range(calendar[i].number_of_available_planes):
            available_planes["day"].append(i)
            available_planes["plane_type"].append(calendar[i].available_planes[j].plane_type.decode())
            available_planes["max_capacity"].append(calendar[i].available_planes[j].max_capacity)

    available_planes_dataframe = pd.DataFrame(available_planes)
    if tocsv:
        available_planes_dataframe.to_csv(filename)
    return available_planes_dataframe


def calendar_from_dataframes(planned_flights_dataframe, available_planes_dataframe) -> ct.Array:
    calendar = (Day * NB_DAYS)()
    for i in range(NB_DAYS):
        day_flights_df = planned_flights_dataframe[planned_flights_dataframe["day"] == i]
        calendar[i].number_of_planned_flights = ct.c_int(day_flights_df.shape[0])
        calendar[i].flights_of_the_day = (Flight * day_flights_df.shape[0])()
        k = 0
        for j, row in day_flights_df.iterrows():
            print("i = ", i, "j = ", j, "\n", day_flights_df, "\n")
            calendar[i].flights_of_the_day[k].number = bytes(row["number"], 'utf-8')
            calendar[i].flights_of_the_day[k].departure_city = bytes(row["departure_city"], 'utf-8')
            calendar[i].flights_of_the_day[k].arrival_city = bytes(row["arrival_city"], 'utf-8')
            calendar[i].flights_of_the_day[k].attributed_plane.plane_type = \
                bytes(row["plane_type"], 'utf-8')
            calendar[i].flights_of_the_day[k].attributed_plane.max_capacity = \
                ct.c_int(row["plane_maxcap"])
            calendar[i].flights_of_the_day[k].min_capacity = ct.c_int(row["min_capacity"])
            calendar[i].flights_of_the_day[k].max_capacity = ct.c_int(row["max_capacity"])
            k += 1

        day_planes_df = available_planes_dataframe[available_planes_dataframe["day"] == i]
        calendar[i].number_of_available_flights = ct.c_int(day_planes_df.shape[0])
        calendar[i].available_planes = (Plane * day_planes_df.shape[0])()
        k = 0
        for j, row in day_planes_df.iterrows():
            print("i = ", i, "j = ", j, "\n", day_planes_df, "\n")
            calendar[i].available_planes[k].plane_type = bytes(row["plane_type"], 'utf-8')
            calendar[i].available_planes[k].max_capacity = ct.c_int(row["max_capacity"])
            k += 1

    return calendar
