#ifndef PROJET_NF06_LIBRARY_H
#define PROJET_NF06_LIBRARY_H


typedef struct person person;

struct plane;

struct route;

struct flight;

struct airline;

struct day;

void print_plane(struct plane airplane);

void print_flight(struct route air_route);

struct airline* plan_for_4_month(struct airline current_airline);

#endif //PROJET_NF06_LIBRARY_H
