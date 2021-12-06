#ifndef PROJET_NF06_LIBRARY_H
#define PROJET_NF06_LIBRARY_H

typedef struct person person;

int add_int(int a, int b);

float add_float(float a, float b);

void swap(void *a, void *b, size_t len);

int is_adult(person *p);

void print_hello();

#endif //PROJET_NF06_LIBRARY_H
