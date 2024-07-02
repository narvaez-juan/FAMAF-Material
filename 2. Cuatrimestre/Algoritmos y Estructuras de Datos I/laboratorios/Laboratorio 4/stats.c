#include <stdio.h>
#include <assert.h>

struct datos_t {
float maximo;
float minimo;
float promedio;
};

void pedir_arreglo(int n_max, float a[])
{
    int i = 0;

    while (i < n_max)
    {
        printf("Ingrese float para la posicion %d del array: ", i);
        scanf("%f", &a[i]);
        i = i + 1;
    }

    return;
}

struct datos_t stats(int tam, float a[])
{
    struct datos_t arreglox;
    arreglox.maximo = a[0];
    arreglox.minimo = a[0];
    arreglox.promedio = 0;

    int i = 0;
    float sum = 0;

    while (i < tam)
    {
        if (arreglox.maximo < a[i])
        {
            arreglox.maximo = a[i];
        } 
        else if (arreglox.minimo > a[i])
        {
            arreglox.minimo = a[i];
        }

        sum = sum + a[i];
        i = i + 1;
    }

    arreglox.promedio = sum / tam;

    return arreglox;
}

int main(void)
{
    int tam;
    printf("Ingrese tamaño de elementos del arreglo: ");
    scanf("%d", &tam);
    assert(tam > 0);

    float a[tam];

    pedir_arreglo(tam, a);

    struct datos_t datarray = stats(tam, a);

    printf("El maximo del arreglo a es: %f\n", datarray.maximo);    
    printf("El minimo del arreglo a es: %f\n", datarray.minimo);
    printf("El promedio del arreglo a es: %f\n", datarray.promedio);    

    return 0;
}
