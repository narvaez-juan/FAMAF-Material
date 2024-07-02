#include <stdio.h>

struct comp_t {
int menores;
int iguales;
int mayores;
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

struct comp_t cuantos(int tam, int a[], int elem)
{
    int i = 0;

    struct comp_t num;
    num.mayores = 0;
    num.iguales = 0;
    num.menores = 0;

    while (i < tam)
    {   
        if (a[i] > elem)
        {
            num.mayores = num.mayores + 1;
        }
        else if (a[i] < elem)
        {
            num.menores = num.menores + 1;
        }
        else
        {
            num.iguales = num.iguales + 1;
        }

        i = i + 1;
    }
    
    return num;
}

int main(void)
{
    int tam, elem;
    printf("Ingrese tamaño de elementos del arreglo: ");
    scanf("%d", &tam);
    printf("Ingrese el elemento a comparar: ");
    scanf("%d", &elem);

    int a[tam];

    pedir_arreglo(tam, a);

    struct comp_t equis = cuantos(tam, a, elem);

    printf("Cantidad de elementos mayores a %d: %d\n", elem, equis.mayores);   
    printf("Cantidad de elementos iguales a %d: %d\n", elem, equis.iguales);
    printf("Cantidad de elementos menores a %d: %d\n", elem, equis.menores);    

    return 0;
}