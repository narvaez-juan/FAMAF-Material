#include <stdlib.h>
#include <stdio.h>
#include "pair.h"    /* TAD Par         */

struct s_pair_t {
    elem fst;
    elem snd;
};

pair_t pair_new(elem x, elem y) {
    pair_t new = malloc(sizeof(pair_t));
    if (new == NULL) {
        fprintf(stdout, "Not enough memory\n");
        exit(EXIT_FAILURE);
    }
    new->fst = x;
    new->snd = y;
    return new;
}

elem pair_first(pair_t p) {
    return p->fst;
}

elem pair_second(pair_t p) {
    return p->snd;
}

pair_t pair_swapped(pair_t p) {
    pair_t pswap = pair_new(p->snd, p->fst);
    return pswap;
}

pair_t pair_destroy(pair_t p) {
    free(p);
    return NULL;
}