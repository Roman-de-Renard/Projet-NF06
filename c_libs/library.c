/**
* \file library.c
* \author Martin Guérout et Roman Robin
* \date 30/12/2020
* Code des fonctions C utilisées dans le cadre du projet de NF06 en automne 2021
*/


#include <string.h>
#include <stdlib.h>
#include <stdio.h>



struct plane {
    char *plane_type;/**< chaine de caractères représentant le type de l'avion */
    int max_capacity;/**< entier représentant la capacité maximal de l'avion */
};


struct day {
    int number_of_planned_flights;/**< entier représentant le nombre de vols planifiés dans une journée */
    struct flight *flights_of_the_day;/**< liste représentant les vols planifiés dans une journéee */
    int number_of_available_planes;/**< entier représentant le nombre d'avion disponible dans une journée */
    struct plane *available_planes;/**< liste représentant les avions disponibles de la journée */
};


struct route {
    int frequency;/**< entier représentant la fréquence de la route */
    int number_of_possible_planes;/**< entier représentant le nombre d'avion disponible pour prendre une route */
    struct plane *possible_planes;/**< liste d'avion disponible pour prendre la route */
    char *departure_city;/**< chaine de caractères représentant la ville de départ de la route */
    char *arrival_city;/**< chaine de caractères représentant la ville d'arrivée de la route */
    int min_capacity;/**< entier représentant la capacité minimal pour prendre la route */
    int max_capacity;/**< entier représentant la capacité maximal de l'avion */
};


struct flight {
    char number[7];/**< chaine de caractères représentant le numéro du vol */
    char *departure_city;/**< chaine de caractères représentant la ville de départ du vol */
    char *arrival_city;/**< chaine de caractères représentant la ville d'arrivée du vol */
    struct plane attributed_plane;/**< structure plane représentant l'avion associé au vol */
    int min_capacity;/**< entier représentant  */
    int max_capacity;
};


struct airline {
    char *name;
    int number_of_route; // Length of flight_list
    struct route *route_list; // List of all flights of an airline
    int size_of_fleet; // Length of fleet
    struct plane *fleet;
    int priority; // Allows for prioritisation of certain airlines
    struct day *dbd_calendar;
};


struct gate {
    int availability[(17 * 7)][24];
    struct flight *assigned_flights[(17 *7)][24];
};


int plane_in_array(struct plane airplane, int array_length, struct plane *airplane_array) {

    int i;
    int is_in_array = 0;
    for (i = 0; i < array_length; i++) {
        if (airplane.max_capacity == airplane_array[i].max_capacity
            && airplane.plane_type == airplane_array[i].plane_type) {
            is_in_array = 1;
            break;
        }
    }
    return is_in_array;
}


int min(int x, int y) {
    return (x < y) ? x : y;
}


struct day *planning(struct airline *current_airline) {
    int i, j, k;
    struct day *calendar = malloc(7 * 17 * sizeof(struct day));
    for (j = 0; j < 17 * 7; j++) {
        calendar[j].flights_of_the_day = malloc(4 * sizeof(struct flight));
        calendar[j].number_of_available_planes = current_airline->size_of_fleet;
        calendar[j].available_planes = malloc(calendar[j].number_of_available_planes * sizeof(struct plane));
        for (k = 0; k < calendar[j].number_of_available_planes; k++) {
            calendar[j].available_planes[k] = current_airline->fleet[k];
        }
        calendar[j].number_of_planned_flights = 0;
    }


    for (i = 0; i < current_airline->number_of_route; i++) { // Pour tout  i, itinéraire
        //On itere sur tous les itineraires de la compagnie aerienne
        //Attribution de day_interval
        int day_interval;
        switch (current_airline->route_list[i].frequency) {
            // On determine ici la frequence d'iteration des vols en fonction de la valeur donnee dans l'itineraire
            case 0:
                day_interval = 1;
                break;
            case 1:
                day_interval = 7;
                break;
            case 2:
                day_interval = 30;
                break;
            default:
                day_interval = 1;
                break;
        }
        //Choix du jour de départ
        int start_day = 0;
        for (j = 0; j < day_interval; j++) { // Pour les day_interval premiers jours
//          Calcul du jour de depart de l'iteration d'attribution des vols. On choisi le premier des jours les plus
//           vides dans l'intervalle [0, frequence du vol[.
            if (calendar[j].number_of_planned_flights < calendar[start_day].number_of_planned_flights) {
                start_day = j;
            }
        }
        for (j = start_day; j < 7 * 17; j += day_interval) { // Tout les day_interval jours, en partant de start_day
            if (calendar[j].number_of_planned_flights < 4 && calendar[j].number_of_available_planes >=
                                                             1) { // Si on a pas deja 4 vols et qu'on a au moins un avion dispo
//                On itere tous les x jours selon la frequence, depuis le jour de depart et jusqu'a 119,
//                tout en ignorant les jours ou 4 vols sont deja planifies*/
                // Choix de l'avion
                struct plane attributed_plane;
                attributed_plane.plane_type = malloc(128 * sizeof(char));
                attributed_plane.max_capacity = 0;
                int chosen_plane_index; // For deletion in available_planes
                for (k = 0; k < calendar[j].number_of_available_planes; k++) {
//                    On choisi l'avion disponible et pouvant effectuer le vol dont la capacite maximale est la plus
//                     proche de celle du vol, tout en restant au dessus de sa capacite minimale
                    if (abs(calendar[j].available_planes[k].max_capacity -
                            current_airline->route_list[i].max_capacity) <
                        abs(attributed_plane.max_capacity - current_airline->route_list[i].max_capacity)
                        && plane_in_array(calendar[j].available_planes[k],
                                          current_airline->route_list[i].number_of_possible_planes,
                                          current_airline->route_list[i].possible_planes)) {
                        attributed_plane = calendar[j].available_planes[k];
                        chosen_plane_index = k;
                    }
                }
                if (attributed_plane.max_capacity != 0) { // Si on a reussi a attribuer un avion
//                    Si un avion a ete attribue au vol, on ajoute le vol a la liste des vols planifies dans le
//                     calendrier, et on genere son numero d'identification
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].attributed_plane = attributed_plane;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].min_capacity = current_airline->route_list[i].min_capacity;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].departure_city = malloc(
                            128 * sizeof(char));
                    strcpy(calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].departure_city, current_airline->route_list[i].departure_city);
//                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].departure_city = current_airline->route_list[i].departure_city;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].arrival_city = malloc(
                            128 * sizeof(char));
                    strcpy(calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].arrival_city, current_airline->route_list[i].arrival_city);
//                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].arrival_city = current_airline->route_list[i].arrival_city;
                    calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].max_capacity = min(
                            current_airline->route_list->max_capacity, attributed_plane.max_capacity);
                    sprintf(calendar[j].flights_of_the_day[calendar[j].number_of_planned_flights].number, "%c%c%03d%d",
                            current_airline->name[0], current_airline->name[1], j,
                            calendar[j].number_of_planned_flights);
                    for (k = chosen_plane_index + 1; k < calendar[j].number_of_available_planes; k++) {
                        calendar[j].available_planes[k - 1] = calendar[j].available_planes[k];
                    }
                    calendar[j].number_of_available_planes -= 1;
                    calendar[j].number_of_planned_flights += 1;
                } else { printf("Jour %d : Echec de l'attribution d'avion\n", j); }
            }
        }
    }
//    On attribue le calendrier a la compagnie aerienne, et on le renvoit
    current_airline->dbd_calendar = malloc(17 * 7 * sizeof(struct day));
    current_airline->dbd_calendar = calendar;

    return calendar;
}

void gate_assignment(int n_of_airlines, struct airline *airlines, int n_of_gates, struct gate *gates) {

    int i, j, k, h, gate_ind;
    struct gate *new_gates;
    new_gates = malloc(n_of_gates*sizeof(struct gate));
    for (i = 0; i < n_of_gates; i++){
        for (j = 0; j < 17*7; j++){
            for (h = 0; h < 24; h++){
                new_gates[i].availability[j][h] = gates[i].availability[j][h];
                new_gates[i].assigned_flights[j][h] = gates[i].assigned_flights[j][h];

            }
        }
    }

    for (i = 0; i < n_of_airlines; i++) {
        for (j = 0; j < 119; j++) {
            h = 0;
            gate_ind = 0;
            for (k = 0; k < airlines[i].dbd_calendar[j].number_of_planned_flights; k++) { // Pour chaque vol :
                if (new_gates[gate_ind].availability[j][h] !=1) { // Si la h-ieme heure est libre
                    new_gates[gate_ind].assigned_flights[j][h] = &airlines[i].dbd_calendar[j].flights_of_the_day[k];
                    new_gates[gate_ind].assigned_flights[j][h + 1] = &airlines[i].dbd_calendar[j].flights_of_the_day[k];
                    new_gates[gate_ind].availability[j][h] = 1;
                    new_gates[gate_ind].availability[j][h + 1] = 1;
                } else {
                    gate_ind += 1;
                    k -= 1;
                    if (gate_ind == n_of_gates) {
                        h += 2;
                        gate_ind = 0;
                        if (h == 24) {
                            int n;
                            for (n = k; n < airlines->dbd_calendar[j].number_of_planned_flights - 1; n++) {
                                airlines[i].dbd_calendar[j].flights_of_the_day[n] = airlines[i].dbd_calendar[j].flights_of_the_day[
                                        n + 1];
                                airlines[i].dbd_calendar[j].number_of_planned_flights -= 1;
                            }
                        }
                    }
                }
            }
        }
    }

    for (i = 0; i < n_of_gates; i++){
        for (j = 0; j < 17*7; j++){
            for (h = 0; h < 24; h++){
                gates[i].availability[j][h]= new_gates[i].availability[j][h];
                gates[i].assigned_flights[j][h] = new_gates[i].assigned_flights[j][h];

            }
        }
    }

    for (i = 0; i < n_of_gates; i++){
        printf("\n");
        for (j = 0; j < 17*7; j++){
            printf("\n");
            for (h = 0; h < 24; h++){
                printf("%d",gates[i].availability[j][h]);

            }
        }
    }
}
