/* Ejercicio 5.b.1 */
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
	int x, y, i;
	x = pedir_entero('x');
	y = pedir_entero('y');
	i = pedir_entero('i');
	
	i = 0;
	
	while (x >= y)
	{
		x = x - y;
		i = i + 1;
		printf("x: %d, y: %d, i: %d\n", x, y, i);
	}

	return 0;
}

/*
ejecucion 1
	usuario ingresa x: 13, y: 3, i: 0
	
	luego de iter 1
		σ1.0: (x -> 10, y -> 3, i -> 1)
	luego de iter 2
		σ1.1: (x -> 7, y -> 3, i -> 2)
	luego de iter 3
		σ1.2: (x -> 4, y -> 3, i -> 3)
	luego de iter 4
		σ1.3: (x -> 1, y -> 3, i -> 4)
		
*/

/* ejercicio 5.b.3 
ejecucion 2
	usuario ingresa x: 31, y: 6, i: 4
	
	luego de iter 1
		σ1.0: (x -> 25, y -> 6, i -> 1)
	luego de iter 2
		σ1.0: (x -> 19, y -> 6, i -> 2)
	luego de iter 3
		σ1.0: (x -> 13, y -> 6, i -> 3)
	luego de iter 4
		σ1.0: (x -> 7, y -> 6, i -> 4)
	luego de iter 4
		σ1.0: (x -> 1, y -> 6, i -> 5)

Este programa devuelve el divisor (i) y resto (x) de la division
entre x e y
*/
