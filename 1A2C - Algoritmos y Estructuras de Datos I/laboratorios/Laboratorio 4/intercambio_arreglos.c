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

void intercambiar(int tam, int a[], int i, int j) 
{
    tam = a[i];
    a[i] = a[j];
    a[j] = tam;
    
    return;
}

int main(void) {
    int n;
    printf("Ingrese el tamaño del arreglo: ");
    scanf("%d", &n);
    assert(n > 0);
    
    int a[n];
    
    pedir_arreglo(n, a);

    int i, j;
    printf("\nIngrese las posiciones que desea intercambiar (0 a %d):\n", n - 1);
    printf("Posición i: ");
    scanf("%d", &i);
    printf("Posición j: ");
    scanf("%d", &j);

    if (i < 0 || j < 0 || i >= n || j >= n) 
    {
        printf("Las posiciones estan fuera de rango.\n");
        printf("Deben estar entre 0 y %d.\n", n - 1);
    } 
    else 
    {
        intercambiar(n, a, i, j);

        printf("\nArreglo modificado:\n");
        
        imprimir_arreglo(n, a);
    }

    return 0;
}
