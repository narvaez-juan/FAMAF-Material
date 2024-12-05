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

int prim_iguales(int tam, int a[])
{
    int i = 0, prim_elem = a[0];

    while (prim_elem == a[i] && i < tam)
    {
        i = i + 1;
    }

    return i;
}

int main(void)
{
    int a[N], largo;
    int i = 0;

    pedir_arreglo(N, a);

    largo = prim_iguales(N, a);

    printf("Longitud de tramo inicial mas largo con elementos iguales: %d\n", largo);
    
    printf("[");
    while (i < largo)
    {
        printf("%d", a[i]);
        if (i != largo - 1)
        {
        	printf(", ");
        }
        
        i = i + 1;
    }
    printf("]");
    
    printf("\n");

    return 0;
}
