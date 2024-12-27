#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "array_helpers.h"

unsigned int array_from_file(int array[],
                             unsigned int max_size,
                             const char *filepath) {
    /* Read array from file into another array and returns length */ 

    FILE *file = fopen(filepath, "r");
    if (file == NULL)
    {
        printf("Could not open file\n");
        exit(EXIT_FAILURE);
    }

    unsigned int length = 0;

    int n = fscanf(file, " %u ", &length);

    if (n != 1)
    {
        printf("Could not take length from file\n");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    if (length > max_size)
    {
        printf("Too long array\n");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    for (unsigned int i = 0; i < length; i++)
    {
        int n = fscanf(file, " %d ", &array[i]);

        if (n != 1)
        {
            printf("Could not read integers from file\n");
            fclose(file);
            exit(EXIT_FAILURE);
        }
    }

    return length;
}

void array_dump(int a[], unsigned int length) {
    /* Print the array in the following format: [ a, b, c] */
    printf("[");
    for (unsigned int i = 0; i < length; i++)
    {
        printf(" %i", a[i]);
        if (i != length - 1)
        {
            printf(",");
        }
    }
    printf("]\n");
}

bool array_is_sorted(int a[], unsigned int length) {
    /* Returns if array is sorted or not */
    int tmp = a[0];
    unsigned int i = 0;
    bool sorted = true;

    while (i < length && sorted)
    {
        sorted = tmp <= a[i];
        tmp = a[i];
        i++;
    }

    return sorted;
}