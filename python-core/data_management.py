from c_structures import *
from constants import *
import pandas as pd

pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999


def frame_planned_flights(calendar: ct.POINTER(Day), tocsv: bool = False, filename: str = "") -> pd.DataFrame:
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

"""
def calendar_from_dataframes(planned_flights_dataframe, available_planes_dataframe) -> ct.Array:
    calendar = (Day * NB_DAYS)()
    for i in range(NB_DAYS):
        day_flights_df = planned_flights_dataframe[planned_flights_dataframe["day"] == i]
        calendar[i].number_of_planned_flights = ct.c_int(day_flights_df.shape[0])
        calendar[i].flights_of_the_day = (Flight * day_flights_df.shape[0])()
        for j in range(day_flights_df.index[0], day_flights_df.index[0] + day_flights_df.shape[0]):
            print("i = ", i, "j = ", j, "\n", day_flights_df, "\n")
            calendar[i].flights_of_the_day[j].number = bytes(day_flights_df.loc[j]["number"], 'utf-8')
            calendar[i].flights_of_the_day[j].departure_city = bytes(day_flights_df.loc[j]["departure_city"], 'utf-8')
            calendar[i].flights_of_the_day[j].arrival_city = bytes(day_flights_df.loc[j]["arrival_city"], 'utf-8')
            calendar[i].flights_of_the_day[j].attributed_plane.plane_type = \
                bytes(day_flights_df.loc[j]["plane_type"], 'utf-8')
            calendar[i].flights_of_the_day[j].attributed_plane.max_capacity = \
                ct.c_int(day_flights_df.loc[j]["plane_maxcap"])
            calendar[i].flights_of_the_day[j].min_capacity = ct.c_int(day_flights_df.loc[j]["min_capacity"])
            calendar[i].flights_of_the_day[j].max_capacity = ct.c_int(day_flights_df.loc[j]["max_capacity"])

        day_planes_df = available_planes_dataframe[available_planes_dataframe["day"] == i]
        calendar[i].number_of_available_flights = ct.c_int(day_planes_df.shape[0])
        calendar[i].available_planes = (Plane * day_planes_df.shape[0])()
        for j in range(day_planes_df.index[0], day_planes_df.index[0] + day_planes_df.shape[0]):
            print("i = ", i, "j = ", j, "\n", day_planes_df, "\n")
            calendar[i].available_planes[j].plane_type = bytes(day_planes_df.loc[j]["plane_type"], 'utf-8')
            calendar[i].available_planes[j].max_capacity = ct.c_int(day_planes_df.loc[j]["max_capacity"])

    return calendar"""
