#include <stdio.h>
#include <assert.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

void imprimir_entero(char name, int x)
{
	printf("%c = %d\n", name, x);
	return;
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
	assert(x == X && y == Y && z == Z && X > 0 && Z > 0);

    aux_x = x;
    aux_y = y;

    if (x >= z)
    {
        x = y + z;
        y = aux_x + z;
        z = aux_x + aux_y;
    }
    else 
    {
        x = y;
        y = z;
        z = aux_x;
    }

    assert((X >= Z && (x == Y + Z && y == X + Z && z == X + Y)) || (X < Z && (x == Y && y == Z && z == X)));
    imprimir_entero('x', x);
    imprimir_entero('y', y);
    imprimir_entero('z', z);

    return 0;
}

/*
    ejecucion 1
        $> "Ingrese un valor para la variable x: 2"
        $> "Ingrese un valor para la variable y: 3"
        $> "Ingrese un valor para la variable z: 4"
        -- x = 3
        -- y = 4
        -- z = 2

    ejecucion 2   
        $> "Ingrese un valor para la variable x: 4"
        $> "Ingrese un valor para la variable y: 3"
        $> "Ingrese un valor para la variable z: 2"
        -- x = 5
        -- y = 6
        -- z = 7
*/