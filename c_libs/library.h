/**
* \file library.h
* \author Martin Guérout et Roman Robin
* \date 30/12/2020
* Les fonctions C utilisées dans le cadre du projet de NF06 en automne 2021
*/


#ifndef PROJET_NF06_LIBRARY_H
#define PROJET_NF06_LIBRARY_H


/**
 * \struct plane
 * \brief structure représentant un avion
 *
 * La structure plane permet de représenter un avion par son type
 * et le nombre maximum de passagers qu'il peut prendre
 */
struct plane;

/**
 * \struct day
 * \brief structure représentant un jour
 *
 * La structure jour permet de représenter une journée des 4 mois par
 * le nombre d'avions planifiés, la liste des avions planifiés,
 * le nombre d'avion disponible et la liste d'avion disponible
 */
struct day;

/**
 * \struct route
 * \brief structure représentant une route que peut prendre un vol
 *
 * La structure route permet de représenter par sa fréquence, le nombre
 * d'avion possible pouvant prendre cette route, la liste de ces avions,
 * la ville de départ de la route, la ville d'arrivée, la capacité minimal
 * pour prendre cette route ett la capacité maximal
 */
struct route;

/**
 * \struct flight
 * \brief structure représentant un vol
 *
 * La structure flight permet de représenter un vol par son numéro,
 * sa ville de départ, sa ville d'arrivée, l'avion qui lui est
 * attribué, la capacité minimal et maximal pour décoller
 */
struct flight;

/**
 * \struct airline
 * \brief structure représentant un compagnie aérienne
 *
 * La structure airline permet de représenter une compagnie aérienne par son nom,
 * le nombre de route qu'elle dessert, la liste des routes qu'elle dessert, la taille
 * de sa flotte, la liste des avions de sa flotte, sa priorité et son plannig
 *
 */
struct airline;

/**
 * \struct gate
 * \brief structure représentant une porte
 *
 * La structure gate permet de représenter une porte par ses disponibilité
 * et la liste des avions qui sont assignés
 */
struct gate;


/**
 * Fonction plane_in_array:
 * Verifie la presence d'un avion dans un tableau d'avions, renvoie 1 si l'avion est present, sinon 0.
 * @param airplane : structure de type "plane" dont on veut vérifier la présence dans un tableau.
 * @param array_length : entier correspondant a la longueur du tableau.
 * @param airplane_array : tableau de "plane" dans lequel on veut verifier la presence de "airplane".
 * @return : entier de valeur 0 ou 1, assimilable a un booleen, 1 nous indique qu'il est dans le tableau, 0 l'inverse
 */
int plane_in_array(struct plane airplane, int array_length, struct plane *airplane_array);

/**
 * Fonction min :
 * Renvoie le minimum du couple de int (x, y) de ses paramètres.
*/
int min(int x, int y);

/**
 * La fonction planning permet de créer un emploi du temps pour chaque compagnie aérienne.
 * La compagnie qu'on lui passe est modifiée dans la fonction
 * @param current_airline la compagnie aérienne qu'on passe depuis Python
 * @return calendar le calendrier sur 4 mois
 */
struct day* planning(struct airline *current_airline);

/**
 * La fonction gate_assignment permet d'assigner aux portes les vols de chaque compagnie.
 * La liste des portes est modifiée dans la fonction
 * @param n_of_airlines le nombre d'éléments dans le tableau airlines
 * @param airlines le tableau des vols
 * @param n_of_gates le nombre d'éléments dans le tableau gate
 * @param gates les portes auxquelles on peut assigner des vols
 * @bug problème d'affichage à la sortie
 */
void gate_assignment(int n_of_airlines, struct airline *airlines, int n_of_gates, struct gate *gates);
#endif //PROJET_NF06_LIBRARY_H
