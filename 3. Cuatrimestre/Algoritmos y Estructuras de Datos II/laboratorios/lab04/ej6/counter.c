#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "counter.h"

struct _counter {
    unsigned int count;
};

counter counter_init(void) {
    counter c = malloc(sizeof(counter));
    if (c == NULL) {
        fprintf(stderr, "Not enough memory to initialize a counter.\n");
        exit(EXIT_FAILURE);
    }
    c->count = 0u;
    return c;
}

void counter_inc(counter c) {
    c->count = c->count + 1u;
}

bool counter_is_init(counter c) {
    return (c->count == 0u);
}

void counter_dec(counter c) {
    assert(!counter_is_init(c));
    c->count = c->count - 1u;
}

counter counter_copy(counter c) {
    counter c2 = counter_init();
    c2->count = c->count;
    return c2;
}

void counter_destroy(counter c) {
    free(c);
}
