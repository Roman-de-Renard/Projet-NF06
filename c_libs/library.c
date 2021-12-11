#include <string.h>
#include <stdlib.h>
#include <stdio.h>

//Structures
struct plane{
    char *plane_type;
    int max_capacity;
};

struct day{
    int number_flights;
    struct flight *flights_of_the_day;
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
    int priority; // Allows for prioritisation of certain airlines
    struct plane *fleet;

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


void planing(struct airline *current_airline){
    int i, j, k;
    struct day *calendar;
    calendar = (struct day *) malloc(7*17*sizeof(struct day));
    for(i = 0; i < 17*7; i++) {
        calendar[i].available_planes = current_airline->fleet;
    }


    for(i = 0; i < current_airline->number_of_route; i++){
        //Pour les mensuels
        if(current_airline->route_list[i].frequency == 2){
            int start_day = 0;
            //Choix du jour de départ
            for(j = 0; j < 30; j++){
                if(len(calendar[j].flights_of_the_day) < start_day){
                    start_day = j;
                }
            }
            for(j = start_day; j < 7*17; j += 30){
                //Choix de l'avion
                for(k = 0; k < (sizeof(calendar[i].available_planes) / sizeof(struct plane)); k++){

                }

            }
        }

    }
}
