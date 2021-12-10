#ifndef PROJET_NF06_LIBRARY_H
#define PROJET_NF06_LIBRARY_H


typedef struct person person;

struct plane;

struct route;

struct airline;


int add_int(int a, int b);

float add_float(float a, float b);

void swap(void *a, void *b, size_t len);

int is_adult(person *p);

void print_hello();

void print_plane(struct plane airplane);

void print_flight(struct route air_route);

struct airline* plan_for_4_month(struct airline current_airline);

#endif //PROJET_NF06_LIBRARY_H
