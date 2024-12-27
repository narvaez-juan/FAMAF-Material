/* First, the standard lib includes, alphabetically ordered */
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

/* Maximum allowed length of the array */
#define MAX_SIZE 100000

unsigned int array_from_stdin(int array[],
                             unsigned int max_size) {
    /* Read array from stdin array and returns length */ 

    unsigned int length = 0;
    int fscanf_value;

    printf("Enter length: ");
    fscanf_value = fscanf(stdin, " %u ", &length); 
    if (fscanf_value == EOF) 
    {
        printf("\ninput must be exactly one argument\n");
        exit(EXIT_FAILURE);
    }

    if (length > max_size) 
    {
        printf("invalid length\n");
        exit(EXIT_FAILURE);
    }

    for (unsigned int i = 0; i < length; i++) 
    {
        fscanf_value = fscanf(stdin, "%d", &array[i]);
        if (fscanf_value == EOF) {
            length = i;
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


int main(void) {
    
    /* create an array of MAX_SIZE elements */
    int array[MAX_SIZE];
    
    /* parse the file to fill the array and obtain the actual length */
    unsigned int length = array_from_stdin(array, MAX_SIZE);
    
    /* dumping the array */
    array_dump(array, length);
    
    return EXIT_SUCCESS;
}
