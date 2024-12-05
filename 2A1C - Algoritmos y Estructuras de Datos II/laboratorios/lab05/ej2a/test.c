#include <stdio.h>
#include <stdlib.h>

#include "stack.h"

int main(void) {

    stack s = stack_empty();
    stack_elem *arr = NULL;
    unsigned int size = stack_size(s);

    /* Check stack_push on empty stack */
    s = stack_push(s, 1);
    size = stack_size(s);
    if (size == 1) {
        printf("push works fine on empty stack, now it's size %u\n", size);
    } else {
        printf("pop doesn't works on empty stack, now it's size %u\n", size);
        stack_destroy(s);
        exit(EXIT_FAILURE);
    }

    /* Check stack_pop for stack size 1 */
    s = stack_pop(s);
    size = stack_size(s);
    if (size == 0) {
        printf("pop works fine for stack size 1, now it's size %u\n", size);
    } else {
        printf("pop doesn't works for stack size 1, now it's size %u\n", size);
        stack_destroy(s);
        exit(EXIT_FAILURE);
    }

    /* Check stack_to_array return NULL for empty stack */
    arr = stack_to_array(s);
    if (arr == NULL) {
        printf("stack_to_array return NULL for empty stack\n");
    } else {
        printf("stack_to_array doesn't return NULL for empty stack\n");
        stack_destroy(s);
        exit(EXIT_FAILURE);
    }

    /* Check stack_to_array gives elements on the correct order */
    s = stack_push(s, 0);
    s = stack_push(s, 1);
    s = stack_push(s, 2);
    s = stack_push(s, 3);
    
    arr = stack_to_array(s);
    size = stack_size(s);
    int i = (int) size - 1;
    stack_elem top = stack_top(s);
    printf("\nElements from top to last:\n");
    while (i >= 0) {
        top = stack_top(s);
        s = stack_pop(s);
        if (arr[i] != top) {
            printf("stack_to_array doesn't work as expected\n");
            stack_destroy(s);
            exit(EXIT_FAILURE);
        }
        printf("%d ", arr[i]);
        i--;
    }
    printf("\n");
    
    /* destroy stack and free memory */
    s = stack_destroy(s);
    free(arr);

    return EXIT_SUCCESS;
}