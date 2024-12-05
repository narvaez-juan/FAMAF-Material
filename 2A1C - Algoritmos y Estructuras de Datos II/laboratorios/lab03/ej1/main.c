#include <stdlib.h>
#include <stdio.h>

#define MAX_SIZE 1000

static void dump(char a[], unsigned int length) {
    printf("\"");
    for (unsigned int j=0u; j < length; j++) {
        printf("%c", a[j]);
    }
    printf("\"");
    printf("\n\n");
}

unsigned int data_from_file(const char *path,
                            unsigned int indexes[],
                            char letters[],
                            unsigned int max_size) {
    /* Read data from file and return the length of file */

    unsigned int length = 0;
    FILE *file = fopen(path, "r");

    if (file == NULL)
    {
        fprintf(stderr, "Couldn't open file\n");
        exit(EXIT_FAILURE);
    }

    int l_integer;
    char l_char;

    while (fscanf(file, "%i -> *%c*\n", &l_integer, &l_char) == 2)
    {
        if (length >= max_size)
        {
            fprintf(stderr, "Too large file element\n");
            fclose(file);
            exit(EXIT_FAILURE);
        }

        indexes[length] = l_integer;
        letters[length] = l_char;
        length++;
    }
    fclose(file);

    return length;
}

static void sort(char sorted[],
                unsigned int indexes[],
                char letters[],
                unsigned int length) {
    /* Sort the array storing in sorted letters based on index */

    for (unsigned int i = 0; i < length; i++) {
        unsigned int j = 0;
        
        while (j < length && indexes[j] != i) 
        {
            j++;
        }

        if (j >= length) {
            fprintf(stderr, "Out-of-range index\n");
            exit(EXIT_FAILURE);
        }

        sorted[i] = letters[j];
    }
}


int main(int argc, char *argv[]) {
    if (argc != 2)
    {
        fprintf(stderr, "Use: %s <file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *path = argv[1];
    unsigned int indexes[MAX_SIZE];
    char letters[MAX_SIZE];
    char sorted[MAX_SIZE];
    unsigned int length=0; 

    length = data_from_file(path, indexes, letters, MAX_SIZE);

    /* sort the array of char */
    sort(sorted, indexes, letters, length);

    /* dump the array*/
    dump(sorted, length);

    return EXIT_SUCCESS;
}
