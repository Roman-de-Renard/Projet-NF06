#include <string.h>
#include <stdlib.h>
#include <stdio.h>

//Structures
struct plane{
    char *plane_type;
    int max_capacity;
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
    int min_capacity;
    int max_capacity;
};



struct airline{
    char *name;
    int number_of_route; // Length of flight_list
    struct route *flight_route; // List of all flights of an airline
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

struct airline* plan_for_4_months(struct airline current_airline){


}

void planing(struct airline curent_airline){
    int i;
    struct route months_table[17][7][4];
    for (i=0;i<curent_airline.number_of_route;i++)
    {

    }
}
