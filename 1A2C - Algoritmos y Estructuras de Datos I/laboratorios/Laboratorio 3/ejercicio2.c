/* Ejercicio 2 */
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
	int x, y, z, b, w;
	x = pedir_entero('x');
	y = pedir_entero('y');
	z = pedir_entero('z');
	b = pedir_entero('b');
	w = pedir_entero('w');
	
	bool exp1 = x % 4 == 0;
	bool exp2 = x + y == 0 && y - x == (-1) * z;
	bool exp3 = !b && w;
	
	printf("exp_1: x %% 4 == 0 = %d\n", exp1);
	printf("exp_2: x + y == 0 && y - x == (-1) * z = %d\n", exp2);
	printf("exp_3: !b && w = %d\n", exp3);
	
	return 0; 
}

/*
Expresion	 							Valor
x % 4 == 0								True
x + y == 0 && y - x == (-1) * z 		True
not b && w 								False

*Recordar que true = 1, false = 0

Ingrese el valor de x: 4
Ingrese el valor de y: -4
Ingrese el valor de z: 8
Ingrese el valor de b: 1
Ingrese el valor de w: 1
exp_1: x % 4 == 0 = 1
exp_2: x + y == 0 && y - x == (-1) * z = 1
exp_3: !b && w = 0

Ingrese el valor de x: 8
Ingrese el valor de y: -8
Ingrese el valor de z: 16
Ingrese el valor de b: 1
Ingrese el valor de w: 1
exp_1: x % 4 == 0 = 1
exp_2: x + y == 0 && y - x == (-1) * z = 1
exp_3: !b && w = 0
*/
