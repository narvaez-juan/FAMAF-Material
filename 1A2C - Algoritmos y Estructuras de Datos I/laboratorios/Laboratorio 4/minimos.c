#include <stdio.h>
#include <limits.h>

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

int minimo_pares(int tam, int a[])
{
    int i = 0, min_pares = INT_MAX;

    while (i < tam) 
    {
        if (a[i] % 2 == 0 && a[i] < min_pares) 
        {
            min_pares = a[i];
        }

        i = i + 1;
    }

    return min_pares;
}

int minimo_impares(int tam, int a[])
{
    int i = 0, min_impares = INT_MAX;

    while (i < tam)
    {
        if (a[i] % 2 != 0 && a[i] < min_impares)
        {
            min_impares = a[i];
        }

        i = i + 1;
    }

    return min_impares;
}

int minimo_element(int min_par, int min_imp)
{
	int res;
	
    if (min_imp > min_par)
    {
        res = min_par;
    }
    else
    {
        res = min_imp;
    }
       
    return res;
}

int main(void) 
{
    int a[N];
    
    pedir_arreglo(N, a);

    int min_par = minimo_pares(N, a);
    int min_imp = minimo_impares(N, a);
    int min_elem = minimo_element(min_par, min_imp);

    printf("El minimo par es: %d\n", min_par);
    printf("El minimo impar es: %d\n", min_imp);
    printf("El elemento mínimo del arreglo es: %d\n", min_elem);

    return 0;
}
