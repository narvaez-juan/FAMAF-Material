#include <stdio.h>
#include <stdbool.h>

char pedir_char(char name)
{
	char letra;
	printf("Ingrese una letra para la variable %c: ", name);
	scanf("%c", &letra);
	return letra;
}

bool es_vocal(char letra)
{
	bool b;
	
    if (letra == 'A' || letra == 'E' || letra == 'I' || letra == 'O' || letra == 'U'
    || letra == 'a' || letra == 'e' || letra == 'i' || letra == 'o' || letra == 'u')
    {
        b = true;
    }
    else
    {
        b = false;
    }
    
    return b;
}

int main(void)
{
    char c;
    c = pedir_char('c');

    if (es_vocal(c))
    {
        printf("%c es vocal\n", c);
    }
    else
    {
        printf("%c no es vocal\n", c);
    }

    return 0;
}
