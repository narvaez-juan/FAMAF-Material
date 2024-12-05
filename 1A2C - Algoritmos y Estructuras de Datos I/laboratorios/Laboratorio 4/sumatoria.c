#include <stdio.h>

#define N 5

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

int sumatoria(int tam, int a[])
{
    int i, sum;
    i = 0, sum = 0;

    while (i < tam)
    {
        sum = sum + a[i];
        i = i + 1;
    } 

    return sum;
}

int main(void)
{
    int a[N], sum;

    pedir_arreglo(N, a);

    sum = sumatoria(N, a);

    printf("El resultado de la sumatoria es: %d\n", sum);

    return 0;
}
