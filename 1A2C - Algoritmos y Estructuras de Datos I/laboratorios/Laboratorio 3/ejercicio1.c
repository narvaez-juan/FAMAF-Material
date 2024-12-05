/* Ejercicio 1 */
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
	/* Solicita ingreso de valores para x, y, z */
	int x, y, z;	
	x = pedir_entero('x');
	y = pedir_entero('y');
	z = pedir_entero('z');
	
	/* Calcula las expresiones */
	int exp1 = x + y + 1;
	int exp2 = z * z + y * 45 - 15 * x;
	int exp3 = y - 2 == (x * 3 + 1) % 5;
	int exp4 = y / 2 * x;
	int exp5 = y < x * 5;
	
	/* Imprime las expresiones y sus resultados */
	printf("exp_1: x + y + 1 = %d\n", exp1);
	printf("exp_2: z * z + y * 45 - 15 * x = %d\n", exp2);
	printf("exp_3: y - 2 == (x * 3 + 1) %% 5 = %d\n", exp3);
	printf("exp_4: y / 2 * x = %d\n", exp4);
	printf("exp_5: y < x * 5 = %d\n", exp5);
	
	return 0;
}

/*
Ingrese el valor de x: 7
Ingrese el valor de y: 3
Ingrese el valor de z: 5
exp_1: x + y + 1 = 11
exp_2: z * z + y * 45 - 15 * x = 55
exp_3: y - 2 == (x * 3 + 1) % 5 = 0
exp_4: y / 2 * x = 7
exp_5: y < x * 5 = 1


Ingrese el valor de x: 1
Ingrese el valor de y: 10
Ingrese el valor de z: 8
exp_1: x + y + 1 = 12
exp_2: z * z + y * 45 - 15 * x = 499
exp_3: y - 2 == (x * 3 + 1) % 5 = 0
exp_4: y / 2 * x = 5
exp_5: y < x * 5 = 0


En la ultima expresion el tipo de resultado en 'C' es Int
*/
