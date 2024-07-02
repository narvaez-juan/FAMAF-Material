#include <stdlib.h>  /* EXIT_SUCCESS... */
#include <stdio.h>   /* printf()...     */
#include "pair.h"    /* TAD Par         */

pair_t pair_new(int x, int y) {
    pair_t new = {.fst = x, .snd = y};
    return new;
}

int pair_first(pair_t p) {
    return p.fst;
}

int pair_second(pair_t p) {
    return p.snd;
}

pair_t pair_swapped(pair_t p) {
    pair_t pswap = {.fst = p.snd, .snd = p.fst};
    return pswap;
}

pair_t pair_destroy(pair_t p) {
    return p;
}