#include <stdio.h>
#include <assert.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

void hola_hasta(int n)
{
    int i = 0;

    while (i < n)
    {
        printf("hola\n");
        i = i + 1;
    }
    
    return;
}

int main(void)
{
    int n = pedir_entero('n');
    assert(n > 0);
    hola_hasta(n);

    return 0;
}