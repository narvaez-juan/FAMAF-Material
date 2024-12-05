/* Ejercicio 6.b */
#include <stdio.h>
#include <stdbool.h>

bool pedir_booleano(char name)
{
	int booleano;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &booleano);
	return booleano;
}

void imprimir_booleano(char name, bool x)
{
	if (x)
	{
		printf("%c = verdadero\n",name);
		return;
	}
	
	printf("%c = falso\n",name);
	return;
}

int main(void)
{
	bool b;
	b = pedir_booleano('b');
	imprimir_booleano('b', b);
	
	return 0;
}
