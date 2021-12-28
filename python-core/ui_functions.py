from c_structures import *
from constants import *
import pandas as pd
pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999


def frame_planned_flights(calendar: ct.POINTER(Day), tocsv: bool=False, filename: str="") -> pd.DataFrame:
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
        planned_flights_dataframe.to_csv(filename, index=False)
    return planned_flights_dataframe
