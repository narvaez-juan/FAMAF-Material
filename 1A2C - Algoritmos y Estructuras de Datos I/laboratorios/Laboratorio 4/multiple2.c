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
    int X, Y, Z;
    int aux_x, aux_y;
    X = pedir_entero('x');
    Y = pedir_entero('y');
    Z = pedir_entero('z');
    x = X;
	y = Y;
	z = Z;
	assert(x == X && y == Y && z == Z);
	
	aux_x = x;
	aux_y = y;
	x = y;
	y = y + aux_x + z;
	z = aux_y + aux_x;
	
	assert(x == Y && (y == Y + X + Z) && (z == Y + X));
	printf("x = %d, y = %d, z = %d\n", x, y, z);

    return 0;
}
