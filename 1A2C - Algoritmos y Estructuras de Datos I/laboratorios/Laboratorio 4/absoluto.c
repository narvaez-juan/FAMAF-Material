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
    int x, r;
    int X;
    X = pedir_entero('x');
    x = X;
    assert(x == X);
    
	if (x >= 0)
    {
        r = x;
    }
    else
    {
        r = -x;
    }
	
	assert(r >= 0 && (r == X || r == -X));
    printf("Su valor absoluto es: %d\n", r);

    return 0;
}
