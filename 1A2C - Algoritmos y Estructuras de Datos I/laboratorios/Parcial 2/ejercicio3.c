#include <stdio.h>
#include <stdbool.h>
#include <limits.h>
#include <assert.h>

#define N 4

struct datos{
    bool es_divisible_por_2;
    int menor_divisible_por_2;
};

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

struct datos hay_divisible(int tam, int a[])
{
    int i = 0, min_par = INT_MAX;
    bool b = false;
    struct datos r;

    while (i < tam)
    {
        if (a[i] % 2 == 0 && a[i] < min_par)
        {
            b = true;
            min_par = a[i];
        }
    }

    r.es_divisible_por_2 = b;
    r.menor_divisible_por_2 = min_par;

    return r;
}

int main(void)
{   
    int a[N];
    assert(N > 1);
    struct datos x;
    
    pedir_arreglo(N, a);

    x = hay_divisible(N, a);
    
    print("x.es_divisible_por_2 = %i\n", x.es_divisible_por_2);
    print("x.menor_divisible_por_2 = %i\n", x.menor_divisible_por_2);

    return 0;
}

/*
    ejecucion 1
        $> "Ingrese valor para la posicion 0 del array: 1"
        $> "Ingrese valor para la posicion 1 del array: 2"
        $> "Ingrese valor para la posicion 2 del array: 3"
        $> "Ingrese valor para la posicion 3 del array: 4"
        -- x.es_divisible_por_2 = 1
        -- x.menor_divisible_por_2 = 2

    ejecucion 2    
        $> "Ingrese valor para la posicion 0 del array: 5"
        $> "Ingrese valor para la posicion 1 del array: 3"
        $> "Ingrese valor para la posicion 2 del array: 6"
        $> "Ingrese valor para la posicion 3 del array: 8"
        -- x.es_divisible_por_2 = 1
        -- x.menor_divisible_por_2 = 6
*/