/*
  @file main.c
  @brief Main program function implementation
*/
#include <stdio.h>
#include <stdlib.h>

/** @brief structure which represent a person */
typedef struct _person {
    int age;
    char name_initial;
} person_t;

/**
 * @brief Main program function
 *
 * @return EXIT_SUCCESS when programs executes correctly, EXIT_FAILURE otherwise
 */
int main(void) {

    int x = 1;
    person_t m = {90, 'M'};
    int a[] = {0, 1, 2, 3};

    /* 
       Al finalizar la ejecución las variables deben tener los siguientes valores
       x = 9
       m = (100, F)
       a[1] = 42
    */

    int *ptox = NULL;
    person_t *ptom = NULL;

    ptox = &x;
    *ptox = 9;

    ptom = &m;
    ptom -> age = 100;
	ptom -> name_initial = 'F';

	ptox = &a[1];
	*ptox = 42;

    printf("x = %d\n", x);
    printf("m = (%d, %c)\n", m.age, m.name_initial);
    printf("a[1] = %d\n", a[1]);

    return EXIT_SUCCESS;
}
