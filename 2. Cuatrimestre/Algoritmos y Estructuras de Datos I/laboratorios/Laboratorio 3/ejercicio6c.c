/* Ejercicio 6.c */
#include <stdio.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

int main(void)
{
    int x, y, z, m;
    x = pedir_entero('x');
    y = pedir_entero('y');
    z = pedir_entero('z');
    m = pedir_entero('m');

    if (x < y)
    {
        m = x;
    }
    else 
    {
        m = y;
    }

    if (m < z)
    {
        ;
    }
    else
    {
        m = z;
    }

    printf("o2: (x -> %d, y -> %d, z -> %d, m -> %d)", x, y, z, m);

    return 0;
}

/*
Las ventajas de esta nueva version es que nos ahorramos lineas de codigo al reusar
una funcion que asigna valores a una variable.

Podria escribir otra funcion que retornara la variable con el valor mas pequeño
entre otras variables.

La funcion de pedir enteros lo podria usar en cualquier otro ejercicio en el que
necesito que el usuario me de un valor para una variable.
*/