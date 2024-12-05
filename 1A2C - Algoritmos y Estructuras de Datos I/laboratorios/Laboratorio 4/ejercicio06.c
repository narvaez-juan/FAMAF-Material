#include <stdio.h>
#include <assert.h>

void pedir_arreglo(int n_max, int a[])
{
    int i = 0;

    while (i < n_max)
    {
        printf("Ingrese valor para la posicion %d del array: ", i);
        scanf("%d", &a[i]);
        i = i + 1;
    }

    return;
}

void imprimir_arreglo(int n_max, int a[])
{
    int i = 0;

    while (i < n_max)
    {
        printf("El valor del arreglo en la posicion %d = %d\n", i, a[i]);
        i = i + 1;
    } 

    return;
}

int main(void)
{
    int n;
    printf("Ingrese valor para el maximo tamaño del arreglo: ");
    scanf("%d", &n);
    assert(n >= 0);

    int a[n];

    pedir_arreglo(n, a);

    imprimir_arreglo(n, a);

    return 0;
}