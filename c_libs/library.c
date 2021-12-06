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
    printf("Hello world, i'm a C function");
}
