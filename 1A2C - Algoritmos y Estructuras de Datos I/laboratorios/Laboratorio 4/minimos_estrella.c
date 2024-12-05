#include <stdio.h>
#include <stdbool.h>
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

bool existe_multiplo(int m, int tam, int a[])
{
    int i = 0;
    bool b = false;

    while (i < tam) 
    {
        if (a[i] % m == 0) 
        {
            b = true;
            break;
        }

        i = i + 1;
    }
    
    return b;
}

bool existe_par(int tam, int a[])
{
    bool b = existe_multiplo(2, tam, a);

    return b;
}

bool existe_impar(int tam, int a[])
{
    int i = 0;
    bool b = false;

    while (i < tam)
    {
        if (a[i] % 2 != 0)
        {
            b = true;
            break;
        }
        
        i = i + 1;
    }

    return b;
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
    int min_par, min_imp, min_elem;
    min_par = INT_MAX, min_imp = INT_MAX;
    
    pedir_arreglo(N, a);
    
    if (existe_par(N, a))
    {
		min_par = minimo_pares(N, a);
		printf("El minimo par es: %d\n", min_par);
    }
    else
    {
		printf("No existe elementos pares en el arreglo\n");
    }

    if (existe_impar(N, a))
    {
		min_imp = minimo_impares(N, a);
    	printf("El minimo impar es: %d\n", min_imp);
    }
    else
    {
		printf("No existe elementos impares en el arreglo\n");
    }

	min_elem = minimo_element(min_par, min_imp);
    printf("El elemento mínimo del arreglo es: %d\n", min_elem);

    return 0;
}
