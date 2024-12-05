#include <stdio.h>
#include <stdbool.h>

int pedir_entero_positivo()
{
	int n;
	
	printf("Ingrese valor no negativo para n: ");
    scanf("%d", &n);

    while (n <= 0)
    {
        printf("Ingrese un nuevo valor, debe ser no negativo: ");
        scanf("%d", &n);
    }
    
    return n;
}

bool es_primo(int n)
{
    int i = 2;
    bool primo = true;

    while (i < n && primo)
    {
        if (n % i == 0)
        {
            primo = false;
        }

        i = i + 1;
    }

    return primo;
}

int nesimo_primo(int nesimo)
{
    int n = 1;
    int valor = 2;
    int ultimo_primo = 2;
    
    while (n != nesimo)
    {
    	valor = valor + 1;
    	
    	if (es_primo(valor))
    	{
    		ultimo_primo = valor;
    		n = n + 1;
    	}
    }
    
    return ultimo_primo;
}

int main(void)
{
    int n, valor;
    
    n = pedir_entero_positivo();
    valor = nesimo_primo(n);

    printf("El %d-simo primo es: %d\n", n, valor);

    return 0;
}
