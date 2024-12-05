#include <stdio.h>

typedef struct _persona {
    char *nombre;
    int edad;
    float altura;
    float peso;
} persona_t;

float peso_promedio(unsigned int longitud, persona_t arr[])
{
    unsigned int i = 0;
    float sum = 0, prom = 0;
    
    while (i < longitud)
    {
        sum = sum + arr[i].peso;
        i = i + 1;
    }

    prom = sum / longitud;

    return prom;
}

persona_t persona_de_mayor_edad(unsigned int longitud, persona_t arr[])
{
    unsigned int iterator = 0, index = 0;
    int max = arr[0].edad;

    while (iterator < longitud)
    {
        if (max < arr[iterator].edad)
        {
            max = arr[iterator].edad;
            index = iterator;
        }

        iterator = iterator + 1;
    }

    return arr[index];
}

persona_t persona_de_menor_altura(unsigned int longitud, persona_t arr[])
{
    unsigned int iterator = 0, index = 0;
    float min = arr[0].altura;

    while (iterator < longitud)
    {
        if (min > arr[iterator].altura)
        {
            min = arr[iterator].altura;
            index = iterator;
        }

        iterator = iterator + 1;
    }

    return arr[index];
}

int main(void)
{
    persona_t p1 = {.nombre="Paola", .edad=21, .altura=1.85, .peso=75};
    persona_t p2 = {.nombre="Luis", .edad=54, .altura=1.75, .peso=69};
    persona_t p3 = {.nombre="Julio", .edad=40, .altura=1.70, .peso=80};

    unsigned int longitud = 3;

    persona_t arr[] = {p1, p2, p3};

    printf("El peso promedio es %f\n", peso_promedio(longitud, arr));

    persona_t p = persona_de_mayor_edad(longitud, arr);
    printf("El nombre de la persona con mayor edad es %s\n", p.nombre);

    p = persona_de_menor_altura(longitud, arr);
    printf("El nombre de la persona con menor altura es %s\n", p.nombre);

    return 0;
}
