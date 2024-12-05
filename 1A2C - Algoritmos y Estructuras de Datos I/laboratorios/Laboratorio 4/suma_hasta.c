#include <stdio.h>
#include <assert.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

int suma_hasta(int n)
{
    int suma_gauss = (n*(n+1))/2; 
    return suma_gauss;
}

int main(void)
{
    int x;
    x = pedir_entero('x');
    assert(x > 0);
    printf("%d\n", suma_hasta(x));

    return 0;
}