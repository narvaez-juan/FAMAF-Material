/* Ejercicio 4.b */
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

    printf("x: %d, y: %d ,z: %d, m:  %d)", x, y, z, m);

    return 0;
}

/*
ejecucion 1
    σ0 (x -> 5, y -> 4, z -> 8, m -> 10)

    σ1 (x -> 5, y -> 4, z -> 8, m -> 4)

    σ2 (x -> 5, y -> 4, z -> 8, m -> 8)

ejecucion 2
    σ0 (x -> 2, y -> 3, z -> 4, m -> 1)
    
    σ1 (x -> 2, y -> 3, z -> 4, m -> 2)
    
    σ0 (x -> 2, y -> 3, z -> 4, m -> 2)

    Este programa compara valores y guarda el valor mas pequeño en la variable m
    El valor final de la variable m es el valor mas pequeño entre x, y, z
*/