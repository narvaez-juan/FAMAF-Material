#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include "stack.h"


/* Stack data type implementation */
struct _s_stack {
    stack_elem *elems;      // Arreglo de elementos
    unsigned int size;      // Cantidad de elementos en la pila
    unsigned int capacity;  // Capacidad actual del arreglo elems
};

bool invrep_not_null(stack s) {
    return (s != NULL);
}

bool invrep_size(stack s) {
    return (s->size > 0);
}

/* Stack functions implementation */

stack stack_empty() {
    stack s = NULL;
    s = malloc(sizeof(struct _s_stack));
    if (s == NULL) {
        fprintf(stderr, "Not enough memory for push.\n");
        exit(EXIT_FAILURE);
    }
    s->elems = NULL;
    s->size = 0;
    s->capacity = 0;
    return s;
}

stack stack_push(stack s, stack_elem e) {
    assert(invrep_not_null(s));
    if (s->size == s->capacity) {
        if (s->capacity == 0) {
            s->capacity = 1;
        } else {
            s->capacity *= 2;
        }
        s->elems = (stack_elem *) realloc(s->elems, sizeof(stack_elem) * s->capacity);
    }
    s->elems[s->size] = e;
    s->size++;
    assert(invrep_size(s) && "size is not greater than zero after push.\n");
    return s;
}

stack stack_pop(stack s) {
    assert(invrep_size(s) && "cannot pop an empty stack.\n");
    s->size--;
    return s;
}

unsigned int stack_size(stack s) {
    
    return s->size;
}

stack_elem stack_top(stack s) {
    assert(invrep_size(s) && "cannot return top element on empty stack.\n");
    return s->elems[s->size - 1];
}

bool stack_is_empty(stack s) {
    assert(invrep_not_null(s));
    return (s->size == 0);
}

stack_elem *stack_to_array(stack s) {
    assert(invrep_not_null(s));
    unsigned int size = stack_size(s);
    stack_elem *array = NULL;
    if (size != 0) {
        array = calloc(size, sizeof(stack_elem));
        if (array == NULL) {
            fprintf(stderr, "Not enough memory for array.\n");
            exit(EXIT_FAILURE);
        }
        int i = (int) size - 1;
        int j = 0;
        while (i >= 0 && !stack_is_empty(s)) {
            array[j] = s->elems[i];
            i--;
            j++;
        }
    }
    return array;
}

stack stack_destroy(stack s) {
    free(s->elems);
    free(s);
    return NULL;
}