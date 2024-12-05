#include <stdio.h>
#include <stdbool.h>

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

bool todos_pares(int tam, int a[])
{
    int i = 0;
    bool b = true;

    while (i < tam)
    {
        if (a[i] % 2 != 0) 
        {
            b = false;
            break;
        }

        i = i + 1;
    }

    return b;
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


int main(void) {
    int a[N];
    
    pedir_arreglo(N, a);
    
    int opcion;
    printf("\nElija una opción:\n");
    printf("1. Verificar que todos los elementos sean pares\n");
    printf("2. Verificar que existe al menos un multiplo de m\n");
    printf("Usted escoge: ");
    scanf("%d", &opcion);
    
    if (opcion == 1) 
    {
        if (todos_pares(N, a)) 
        {
            printf("Todos los elementos son pares.\n");
        } 
        else 
        {
            printf("No todos los elementos son pares.\n");
        }
    } 
    else if (opcion == 2) 
    {
        int m;
        printf("Ingrese un valor para m: ");
        scanf("%d", &m);
        
        if (existe_multiplo(m, N, a)) 
        {
            printf("Existe al menos un múltiplo de %d en el arreglo.\n", m);
        } 
        else 
        {
            printf("No existe ningún múltiplo de %d en el arreglo.\n", m);
        }
    } 
    else 
    {
        printf("Opción no válida.\n");
    }
    
    return 0;
}
