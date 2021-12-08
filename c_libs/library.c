#include <string.h>
#include <stdlib.h>
#include <stdio.h>


//Structures

typedef struct person{
    char first_name[20];
    char last_name[20];
    int age;
}person ;

struct plane{
    char *plane_type;
    int max_capacity;
};

struct flight{
    char number[7];
    int frequency;
    int number_of_possible_planes;
    struct plane *possible_planes;
    int min_capacity;
    int max_capacity;
};

struct airline{
    char *name;
    int number_of_flights; // Length of flight_list
    struct flight *flight_list; // List of all flights of an airline
    int priority; // Allows for prioritisation of certain airlines
};


//Functions and procedures
int add_int(int a, int b) {
    return a + b;
}

float add_float(float a, float b) {
    return a + b;
}

void swap(void *a, void *b, size_t len) {
    void *tmp = malloc(len);
    memcpy(tmp, a, len);
    memcpy(a, b, len);
    memcpy(b, tmp, len);
    free(tmp);
}

int is_adult(person *p) {
    return p->age >= 18;
}

void print_hello() {
    printf("\nHello world, i'm a C function");
}

void print_plane(struct plane airplane) {
    printf("\nThe %s airplane has a max capacity of %d", airplane.plane_type, airplane.max_capacity);
}

void print_flight(struct flight air_route) {
    printf("\nThe flight id %s, with frequency id %d can be done by %d planes", air_route.number, air_route.frequency, air_route.number_of_possible_planes);
    int i;
    for(i = 0; i < air_route.number_of_possible_planes; i++) {
        print_plane(air_route.possible_planes[i]);
    }
    printf("\nThe flight has a min capacity of %d and a max capacity of %d", air_route.min_capacity, air_route.max_capacity);
}

struct airline* plan_for_4_months(struct airline current_airline){


}
void planing(struct airline curent_airline){
    int i;
    struct flight months_table[17][7][4];
    for (i=0;i<curent_airline.number_of_flights;i++)
    {

    }
}
