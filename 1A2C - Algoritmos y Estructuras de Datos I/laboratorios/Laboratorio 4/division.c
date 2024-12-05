#include <stdio.h>
#include <assert.h>

struct div_t {
int cociente;
int resto;
};

struct div_t division(int x, int y)
{
   struct div_t xy;

   xy.cociente = x / y;
   xy.resto = x % y;

   return xy;
}

int main(void)
{
    int num, div;
    printf("Ingrese un valor para numerador: ");
    scanf("%d", &num);
    printf("Ingrese un valor para divisor: ");
    scanf("%d", &div);
    assert(num >= 0 && div > 0);

    struct div_t div0 = division(num, div);

    printf("%d es cociente\n", div0.cociente);
    printf("%d es resto\n", div0.resto);

    return 0;
}
