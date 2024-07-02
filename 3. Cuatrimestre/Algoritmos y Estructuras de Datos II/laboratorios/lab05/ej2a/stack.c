#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "stack.h"
 
/* Stack data type implementation */
struct _s_stack 
{
    stack_elem elem;
    struct _s_stack *next;
};

bool invrep(stack s) {
    return s != NULL;
}

/* Stack functions implementation */

stack stack_empty() {
    stack s = NULL;
    return s;
}

stack stack_push(stack s, stack_elem e) {
    stack p = malloc(sizeof(struct _s_stack));
    if (p == NULL) {
        fprintf(stderr, "Not enough memory for push.\n");
        exit(EXIT_FAILURE);
    }
    p->elem = e;
    p->next = s;
    return p;
}

stack stack_pop(stack s) {
    assert(invrep(s) && "cannot pop an empty stack.\n");
    stack p = s;
    s = s->next;
    free(p);
    return s;
}

unsigned int stack_size(stack s) {
    unsigned int size = 0;
    stack p = s;
    while (!stack_is_empty(p)) {
        p = p->next;
        size++;
    }
    return size;
}

stack_elem stack_top(stack s) {
    assert(invrep(s) && "cannot return top element on empty stack.\n");
    return s->elem;
}

bool stack_is_empty(stack s) {
    return (s == NULL);
}

stack_elem *stack_to_array(stack s) {
    unsigned int size = stack_size(s);
    stack_elem *array = NULL;
    if (size != 0) {
        array = calloc(size, sizeof(stack_elem));
        stack p = s;
        if (array == NULL) {
            fprintf(stderr, "Not enough memory for array.\n");
            exit(EXIT_FAILURE);
        }
        int i = (int) size - 1;
        while (i >= 0 && !stack_is_empty(p)) {
            array[i] = p->elem;
            p = p->next;
            i--;
        }
    }
    return array;
}

stack stack_destroy(stack s) {
    stack p = s;
    while (!stack_is_empty(s)) {
        p = s;
        s = s->next;
        free(p);
    }
    return s;
}
