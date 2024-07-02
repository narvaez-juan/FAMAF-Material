#include <stdio.h>
#include <assert.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

int main(void)
{
    int x, y, min;
    int X, Y;
    X = pedir_entero('x');
    Y = pedir_entero('y');
    x = X;
    y = Y;
    assert(x == X && y == Y);

    if (x >= y)
    {
        min = Y;
    }
    else
    {
        min = X;
    }
    
    assert((X < Y && min == X) || (X >= Y && min == Y));
    printf("El minimo es: %d\n", min);

    return 0;
}
