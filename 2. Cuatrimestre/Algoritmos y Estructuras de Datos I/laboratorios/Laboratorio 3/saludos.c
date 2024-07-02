/* Ejercicio 6.d */
#include <stdio.h>

void imprimir_hola(void)
{
    printf("hola\n");
    return;
}

void imprimir_chau(void)
{
    printf("chau\n");
    return;    
}

int main(void)
{
    imprimir_hola();
    imprimir_hola();
    imprimir_chau();
    imprimir_chau();

    return 0;
}