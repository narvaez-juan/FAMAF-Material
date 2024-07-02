/* Ejercicio 5.b.2 */
#include <stdio.h>
#include <stdbool.h>

int pedir_entero(char name)
{
	int entero;
	printf("Ingrese un valor para la variable %c: ", name);
	scanf("%d", &entero);
	return entero;
}

int main(void)
{
	int x, i, res;
	x = pedir_entero('x');
	i = pedir_entero('i');
	printf("Ingrese un valor para la variable res: ");
	scanf("%d", &res);
	
	res = (bool) res;
	
	i = 2;
	res = true;
	
	while (i < x && res)
	{
		res = res && (x % i != 0);
		i = i + 1;
		printf("x: %d, i: %d, res: %d\n", x, i, res);
	}

	return 0;
}

/*
ejecucion 1
	usuario ingresa x: 5, i: 0, res: 0
	
	luego de iter 1
		σ1.0: (x -> 5, i -> 3, res -> 1)
	luego de iter 2
		σ1.1: (x -> 5, i -> 4, res -> 1)
	luego de iter 3
		σ1.2: (x -> 5, i -> 5, res -> 1)
		
*/

/* ejercicio 5.b.3 
ejecucion 2
	usuario ingresa x: 6, i: 4, res: 2
	
	luego de iter 1
		σ1.0: (x -> 6, i -> 3, res -> 0)

Este programa itera hasta encontrar un numero i que dividido por
x de resto 0 o hasta que dicho numero i sea igual o mayor que x
*/
