#include <stdio.h>
#include <stdbool.h>

#define N 4

typedef char clave_t;
typedef int valor_t;

struct asoc {
clave_t clave;
valor_t valor;
};

void pedir_arreglo(int n_max, struct asoc a[])
{
    int i = 0;

    while (i < n_max)
    {
        printf("Ingrese clave para a[%d]: ", i);
        scanf(" %c", &a[i].clave);
        printf("Ingrese valor para a[%d]: ", i);
        scanf("%d", &a[i].valor);

        i = i + 1;
    }

    return;
}

bool asoc_existe(int tam, struct asoc a[], clave_t c)
{
    int i = 0;
    bool b = false;

    while (i < tam)
    {
        if (a[i].clave == c)
        {
            b = true;
            break;
        }

        i = i + 1;
    }

    return b;
}

int main(void)
{
    struct asoc a[N];
    bool existe;
    char clave;

    pedir_arreglo(N, a);

    printf("\nIngrese clave para verificar si se encuentra en el arreglo: ");
    scanf(" %c", &clave);

    existe = asoc_existe(N, a, clave);

    if (existe)
    {
        printf("La clave existe en el arreglo de asociaciones.\n");        
    }
    else 
    {
        printf("La clave no existe en el arreglo de asociaciones.\n");
    }

    return 0;
}
