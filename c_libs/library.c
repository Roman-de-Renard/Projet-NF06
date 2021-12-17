#include <string.h>
#include <stdlib.h>
#include <stdio.h>


//Structures
struct plane {
    char *plane_type;
    int max_capacity;
};


struct day {
    int number_of_planned_flights;
    struct flight *flights_of_the_day;
    int number_of_available_planes;
    struct plane *available_planes;
};


struct route {
    int frequency;
    int number_of_possible_planes;
    struct plane *possible_planes;
    char *departure_city;
    char *arrival_city;
    int min_capacity;
    int max_capacity;
};


struct flight {
    char number[7];
    char *departure_city;
    char *arrival_city;
    struct plane attributed_plane;
    int min_capacity;
    int max_capacity;
};


struct airline {
    char *name;
    int number_of_route; // Length of flight_list
    struct route *route_list; // List of all flights of an airline
    int size_of_fleet; // Length of fleet
    struct plane *fleet;
    int priority; // Allows for prioritisation of certain airlines
    struct day *dbd_calendar;
};


struct gate {
    int availability[(17 * 7)][24];
    struct flight *assigned_flights[(17 *
                                     7)][24]; // On aura 2 fois le meme pointeur sur les 2 heures consécutives (permet des 9-11 par exemple)
};


//Functions and procedures

//void print_plane(struct plane airplane) {
//    printf("\nThe %s airplane has a max capacity of %d", airplane.plane_type, airplane.max_capacity);
//}
//
//void print_flight(struct route air_route) {
//    //printf("\nThe flight id %s, with frequency id %d can be done by %d planes", air_route.number, air_route.frequency, air_route.number_of_possible_planes);
//    int i;
//    for(i = 0; i < air_route.number_of_possible_planes; i++) {
//        print_plane(air_route.possible_planes[i]);
//    }
//    printf("\nThe flight has a min capacity of %d and a max capacity of %d", air_route.min_capacity, air_route.max_capacity);
//}
//void print_airline(struct airline current_airline)
//{
//    printf("\nThe company is %s, it has %d flight and a priority of %d", current_airline.name, current_airline.number_of_route,current_airline.priority);
//}


int plane_in_array(struct plane airplane, int array_length, struct plane *airplane_array) {
    int i;
    int is_in_array = 0;
    for (i = 0; i < array_length; i++) {
        if (airplane.max_capacity == airplane_array[i].max_capacity
            && airplane.plane_type == airplane_array[i].plane_type) {
            is_in_array = 1;
            break;
        }
    }
    return is_in_array;
}


int min(int x, int y) {
    return (x < y) ? x : y;
}


struct day *planning(struct airline *current_airline) {
    int i, j, k;
    struct day *calendar = malloc(7 * 17 * sizeof(struct day));
    for (j = 0; j < 17 * 7; j++) {
        calendar[j].flights_of_the_day = malloc(4 * sizeof(struct flight));
        calendar[j].number_of_available_planes = current_airline->size_of_fleet;
        calendar[j].available_planes = malloc(calendar[j].number_of_available_planes * sizeof(struct plane));
        for (k = 0; k < calendar[j].number_of_available_planes; k++) {
            calendar[j].available_planes[k] = current_airline->fleet[k];
        }
//        calendar[j].available_planes = current_airline->fleet;
        calendar[j].number_of_planned_flights = 0;
    }


    for (i = 0; i < current_airline->number_of_route; i++) { // Pour tout  i, itinéraire
        //Attribution de day_interval
        int day_interval;
        switch (current_airline->route_list[i].frequency) {
            case 0:
                day_interval = 1;
                break;
            case 1:
                day_interval = 7;
                break;
            case 2:
                day_interval = 30;
                break;
            default:
                day_interval = 1;
                break;
        }
        //Choix du jour de départ
        int start_day = 0;
        for (j = 0; j < day_interval; j++) { // Pour les day_interval premiers jours
            if (calendar[j].number_of_planned_flights < calendar[start_day].number_of_planned_flights) {
                start_day = j;
            }
        }
        for (j = start_day; j < 7 * 17; j += day_interval) { // Tout les day_interval jours, en partant de start_day
            if (calendar[j].number_of_planned_flights < 4 && calendar[j].number_of_available_planes >=
                                                             1) { // Si on a pas deja 4 vols et qu'on a au moins un avion dispo
                // Choix de l'avion
                struct plane attributed_plane;
                attributed_plane.plane_type = malloc(128 * sizeof(char));
                attributed_plane.max_capacity = 0;
                int chosen_plane_index; // For deletion in available_planes
                for (k = 0; k < calendar[j].number_of_available_planes; k++) {
                    if (abs(calendar[j].available_planes[k].max_capacity -
                            current_airline->route_list[i].max_capacity) <
                        abs(attributed_plane.max_capacity - current_airline->route_list[i].max_capacity)
                        && plane_in_array(calendar[j].available_planes[k],
                                          current_airline->route_list[i].number_of_possible_planes,
                                          current_airline->route_list[i].possible_planes)) {
                        attributed_plane = calendar[j].available_planes[k];
                        chosen_plane_index = k;
                    }
                }
                if (attributed_plane.max_capacity != 0) { // Si on a reussi a attribuer un avion
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].attributed_plane = attributed_plane;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].min_capacity = current_airline->route_list[i].min_capacity;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].departure_city = malloc(
                            128 * sizeof(char));
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].departure_city = current_airline->route_list[i].departure_city;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].arrival_city = malloc(
                            128 * sizeof(char));
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].arrival_city = current_airline->route_list[i].arrival_city;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].max_capacity = min(
                            current_airline->route_list->max_capacity, attributed_plane.max_capacity);
                    sprintf(calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].number, "%c%c%03d%d",
                            current_airline->name[0], current_airline->name[1], j,
                            calendar[j].number_of_planned_flights);
                    for (k = chosen_plane_index + 1; k < calendar[j].number_of_available_planes; k++) {
                        calendar[j].available_planes[k - 1] = calendar[j].available_planes[k];
                    }
                    calendar[j].number_of_available_planes -= 1;
//                    calendar[j].available_planes = (struct plane *) realloc(calendar[j].available_planes, calendar[j].number_of_available_planes * sizeof(struct plane));
                    calendar[j].number_of_planned_flights += 1;
                } else { printf("Jour %d : Echec de l'attribution d'avion\n", j); }
            }
        }
    }
    current_airline->dbd_calendar = malloc(17 * 7 * sizeof(struct day));
    current_airline->dbd_calendar = calendar;
    return calendar;
}

struct gate *gate_assignment(int n_of_airlines, struct airline *airlines, int n_of_gates, struct gate *gates) {
    int i, j, k, h, gate_ind;
    for (i = 0; i < n_of_airlines; i++) {
        for (j = 0; j < 17 * 7; j++) {
            h = 0;
            gate_ind = 0;
            for (k = 0; k < airlines->dbd_calendar[j].number_of_planned_flights; k++) {
                if (gates[gate_ind].availability[j][h] == 0) {
                    gates[gate_ind].availability[j][h] = 1;
                    gates[gate_ind].assigned_flights[j][h] = &airlines->dbd_calendar[j].flights_of_the_day[k];
                }
                else {
                    gate_ind += 1;
                    if (gate_ind == n_of_gates+1) {
                        h += 1;
                        gate_ind = 0;
                        if (h == 25) {
                            for (k = k; k < airlines->dbd_calendar[j].number_of_planned_flights - 1; k++) {
                                airlines->dbd_calendar[j].flights_of_the_day[k] = airlines->dbd_calendar[j].flights_of_the_day[
                                        k + 1];
                                airlines->dbd_calendar[j].number_of_planned_flights -= 1;
                            }
                        }

                    }
                }
            }
        }
        for (i = 0; i < n_of_gates; i++) {
            for (j = 0; j < 17 * 7; j++) {
                for (k = 0; k < 24; k++) {
                    if (gates[i].availability[j][k] == 1)
                        printf("Occupied gate %d on day %d hour %d\n", i, j, k);
                }
            }
        }
    }
    return gates;
}
