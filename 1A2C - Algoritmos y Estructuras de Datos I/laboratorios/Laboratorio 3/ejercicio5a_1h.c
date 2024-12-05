/* Ejercicio 5.b */
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
    /* programa 1.h */
	int i;
	i = pedir_entero('i');

    while (i != 0)
    {
        i = i - 1;
    }

    return 0;
}