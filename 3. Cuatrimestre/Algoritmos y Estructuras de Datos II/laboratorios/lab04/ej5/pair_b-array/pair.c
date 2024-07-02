#include <stdlib.h>
#include <stdio.h>
#include "pair.h"    /* TAD Par         */

pair_t pair_new(int x, int y) {
    pair_t new = {.values = {x, y}};
    return new;
}

int pair_first(pair_t p) {
    return p.values[0];
}

int pair_second(pair_t p) {
    return p.values[1];
}

pair_t pair_swapped(pair_t p) {
    pair_t pswap = {.values = {p.values[1], p.values[0]}};
    return pswap;
}

pair_t pair_destroy(pair_t p) {
    return p;
}