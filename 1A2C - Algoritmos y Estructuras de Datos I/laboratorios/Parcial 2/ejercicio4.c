#include <stdio.h>
#include <stdbool.h>

struct lienzo {
    int l1;
    int l2;
    int l3;
    int l4;
};

struct tipo_lienzo {
    bool es_figura;
    bool es_paisajes;
    bool ninguno_anteriores;
};

struct tipo_lienzo verificar_lienzo(struct lienzo t)
{
    struct tipo_lienzo r;
    r.es_paisajes = t.l1 == t.l3 && t.l2 == t.l4;
    r.es_figura = r.es_paisajes && t.l1 == t.l2;
    r.ninguno_anteriores = !(r.es_figura || r.es_paisajes);

    return r;
}

int main(void)
{   
    struct lienzo x;
    struct tipo_lienzo tx;

    printf("Ingrese valor para l1: ");
    scanf("%d", &x.l1);
    printf("Ingrese valor para l2: ");
    scanf("%d", &x.l2);
    printf("Ingrese valor para l3: ");
    scanf("%d", &x.l3);
    printf("Ingrese valor para l4: ");
    scanf("%d", &x.l4);

    tx = verificar_lienzo(x);

    print("tx.es_figura = %d\n");
    print("tx.es_paisajes = %d\n");
    print("tx.ninguno_anteriores = %d\n");

    return 0;
}

/*
    ejecucion 1
        $> "Ingrese valor para l1: 3"
        $> "Ingrese valor para l2: 3"
        $> "Ingrese valor para l3: 3"
        $> "Ingrese valor para l4: 3"
        -- tx.es_figura = 1
        -- tx.es_paisajes = 1
        -- tx.ninguno_anteriores = 0

    ejecucion 2    
        $> "Ingrese valor para l1: 4"
        $> "Ingrese valor para l2: 3"
        $> "Ingrese valor para l3: 2"
        $> "Ingrese valor para l4: 1"
        -- tx.es_figura = 0
        -- tx.es_paisajes = 0
        -- tx.ninguno_anteriores = 1
*/