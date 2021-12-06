#include <string.h>
#include <stdlib.h>


typedef struct person{
    char first_name[20];
    char last_name[20];
    int age;
}person ;


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