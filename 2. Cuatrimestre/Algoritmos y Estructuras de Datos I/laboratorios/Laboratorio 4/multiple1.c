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
    int x, y, z;
    int X, Y;
    X = pedir_entero('x');
    Y = pedir_entero('y');
	x = X;
	y = Y;
	assert(x == X && y == Y);

    z = x;
    x = x + 1;
    y = z + y;
    
    assert(x == X + 1 && y == X + Y);
    printf("x = %d\n", x);
    printf("y = %d\n", y);

    return 0;
}
