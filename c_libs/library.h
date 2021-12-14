#ifndef PROJET_NF06_LIBRARY_H
#define PROJET_NF06_LIBRARY_H


typedef struct person person;

struct plane;

struct day;

struct route;

struct flight;

struct airline;

//void print_plane(struct plane airplane);

//void print_flight(struct route air_route);

int plane_in_array(struct plane airplane, int array_length, struct plane *airplane_array);

int min(int x, int y);

struct day* planning(struct airline *current_airline);

#endif //PROJET_NF06_LIBRARY_H
