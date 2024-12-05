#include <stdlib.h>
#include <stdio.h>

void absolute(int x, int y) {
    if (x >= 0) {
        y = x;
    } else {
        y = -x;
    }
}

int main(void) {
    int a=0, res=0;
    
    a = -10;
    absolute(a, res);
    printf("%i\n", res);

    return EXIT_SUCCESS;
}

/* Se imprime el valor de res que es 0 puesto que absolute no se pasa la direccion de 
memoria de las variables a y res, sino los valores de estos, por lo que se modifica 
los valores en el alcance de la funcion de absolute mas no en la de main. */