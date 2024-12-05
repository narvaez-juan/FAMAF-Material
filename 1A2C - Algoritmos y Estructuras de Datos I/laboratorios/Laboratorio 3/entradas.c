/* Ejercicio 6.a */
#include <stdio.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

void imprimir_entero(char name, int x)
{
	printf("%c = %d\n",name, x);
	return;
}

int main(void)
{
	int n;
	n = pedir_entero('n');
	imprimir_entero('n', n);
	
	return 0;
}
