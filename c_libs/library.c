#include <string.h>
#include <stdlib.h>
#include <stdio.h>

//Structures
struct plane{
    char *plane_type;
    int max_capacity;
};

struct day{
    int number_of_planned_flights;
    struct flight *flights_of_the_day;
    int number_of_available_planes;
    struct plane *available_planes;
};

struct route{
    int frequency;
    int number_of_possible_planes;
    struct plane *possible_planes;
    char *departure_city;
    char *arrival_city;
    int min_capacity;
    int max_capacity;
};

struct flight{
    char number[7];
    char *departure_city;
    char *arrival_city;
    int index_of_plane;
    int min_capacity;
    int max_capacity;
};



struct airline{
    char *name;
    int number_of_route; // Length of flight_list
    struct route *route_list; // List of all flights of an airline
    int size_of_fleet; // Length of fleet
    struct plane *fleet;
    int priority; // Allows for prioritisation of certain airlines

};


//Functions and procedures

void print_plane(struct plane airplane) {
    printf("\nThe %s airplane has a max capacity of %d", airplane.plane_type, airplane.max_capacity);
}

void print_flight(struct route air_route) {
    //printf("\nThe flight id %s, with frequency id %d can be done by %d planes", air_route.number, air_route.frequency, air_route.number_of_possible_planes);
    int i;
    for(i = 0; i < air_route.number_of_possible_planes; i++) {
        print_plane(air_route.possible_planes[i]);
    }
    printf("\nThe flight has a min capacity of %d and a max capacity of %d", air_route.min_capacity, air_route.max_capacity);
}
void print_airline(struct airline current_airline)
{
    printf("\nThe company is %s, it has %d flight and a priority of %d", current_airline.name, current_airline.number_of_route,current_airline.priority);
}


void planning(struct airline *current_airline){
    int i, j, k;
    struct day *calendar;
    calendar = (struct day *) malloc(7*17*sizeof(struct day));
    for(j = 0; j < 17*7; j++) {
        calendar[j].available_planes = current_airline->fleet;
        calendar[j].number_of_planned_flights = 0;
        calendar[j].number_of_available_planes = current_airline->size_of_fleet;
    }


    for(i = 0; i < current_airline->number_of_route; i++){
        //Pour les mensuels
        if(current_airline->route_list[i].frequency == 2){
            int start_day = 0;
            //Choix du jour de départ
            for(j = 0; j < 30; j++){
                if(calendar[j].number_of_planned_flights < start_day){
                    start_day = j;
                }
            }
            for(j = start_day; j < 7*17; j += 30){
                //Choix de l'avion
                int chosen_plane_index = 0;
                int plane_is_assigned = 0;
                for(k = 0; k < calendar[j].number_of_available_planes; k++){
                    if(chosen_plane_index < calendar[j].available_planes[k].max_capacity){
                        chosen_plane_index = k;
                    }
                }
                calendar[j].number_of_planned_flights += 1;
                calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights - 1].
                for(k = chosen_plane_index; k < calendar[j].number_of_available_planes; k++){

                }

            }
        }

    }
}
