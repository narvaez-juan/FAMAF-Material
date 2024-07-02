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
	/* programa 1.b */
	int x, y;
	x = pedir_entero('x');
	y = pedir_entero('y');
	
	x = x + y;

	y = y + y;
	
	printf("x: %d, y: %d\n", x, y);
	
	return 0;
}

/*
ejecucion 1
	usuario ingresa x = 2, y = 5 
	produce salida x = 7, y = 10 
	
ejecucion 2
	usuario ingresa x = 3, y = 1 
	produce salida x = 4, y = 2
	
ejecucion 3
	usuario ingresa x = -4, y = -2 
	produce salida x = -6, y = -4
*/
