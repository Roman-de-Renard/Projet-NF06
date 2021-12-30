#ifndef PROJET_NF06_LIBRARY_H
#define PROJET_NF06_LIBRARY_H


typedef struct person person;

struct plane;

struct day;

struct route;

struct flight;

struct airline;

struct gate;

//void print_plane(struct plane airplane);

//void print_flight(struct route air_route);

int plane_in_array(struct plane airplane, int array_length, struct plane *airplane_array);

int min(int x, int y);

struct day* planning(struct airline *current_airline);

void gate_assignment(int n_of_airlines, struct airline *airlines, int n_of_gates, struct gate *gates);
#endif //PROJET_NF06_LIBRARY_H
