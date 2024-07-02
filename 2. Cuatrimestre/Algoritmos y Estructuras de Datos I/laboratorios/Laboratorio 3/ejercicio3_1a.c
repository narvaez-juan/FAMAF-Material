/* Ejercicio 3 */
#include <stdio.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

int main(void)
{	
	/* programa 1.a */
	int x;
	x = pedir_entero('x');
	
	x = 5;
	printf("x: %d\n", x);
	
	return 0;
}

/*
ejecucion 1
	usuario ingresa x = 1
	produce salida x = 5
	
ejecucion 2
	usuario ingresa x = 4
	produce salida x = 5
	
ejecucion 3
	usuario ingresa x = -3
	produce salida x = 5
	
*/
