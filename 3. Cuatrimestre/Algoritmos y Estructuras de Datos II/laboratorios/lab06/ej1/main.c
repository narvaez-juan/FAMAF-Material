/* First, the standard lib includes, alphabetically ordered */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "abb.h" /* TAD abb */


void print_help(char *program_name) {
    /* Print the usage help of this program. */
    printf("Usage: %s <input file path>\n\n",
           program_name);
}

char *parse_filepath(int argc, char *argv[]) {
    /* Parse the filepath given by command line argument. */
    char *result = NULL;

    if (argc < 2) {
        print_help(argv[0]);
        exit(EXIT_FAILURE);
    }

    result = argv[1];

    return (result);
}

abb abb_from_file(const char *filepath) {
    FILE *file = NULL;
    abb read_tree;

    read_tree = abb_empty();
    file = fopen(filepath, "r");
    if (file == NULL) {
        fprintf(stderr, "File does not exist.\n");
        exit(EXIT_FAILURE);
    }
    unsigned int i = 0u;
    unsigned int size = 0u;
    int res = 0;
    res = fscanf(file, " %u ", &size);
    if (res != 1) {
        fprintf(stderr, "Invalid format.\n");
        exit(EXIT_FAILURE);
    }
    while (i < size) {
        abb_elem elem;
        res = fscanf(file," %d ", &(elem));
        if (res != 1) {
            fprintf(stderr, "Invalid array.\n");
            exit(EXIT_FAILURE);
        }
        read_tree = abb_add(read_tree, elem);

       ++i;
    }
    fclose(file);
    return read_tree;
}

int main(int argc, char *argv[]) {
    char *filepath = NULL;
    unsigned int option = 0u;

    /* parse the filepath given in command line arguments */
    filepath = parse_filepath(argc, argv);

    /* parse the file to obtain an abb with the elements */
    abb tree = abb_from_file(filepath);
    
    do {
        fprintf(stdout, "\nChoose an option: \n"
                "1. Print the tree on screen\n"
                "2. Add an element\n"
                "3. Remove an element\n"
                "4. Check element existence\n"
                "5. Print tree length\n"
                "6. Print root, max and min of the tree\n"
                "7. Exit the program\n\n");
        fscanf(stdin, "%u", &option);
        printf("\n");

        abb_elem node_to_add;
        abb_elem node_to_remove;
        abb_elem node_exist;
        unsigned int order;

        switch (option)
        {
            case 1:
                do {
                    fprintf(stdout, "\nSelect order to print tree: \n"
                            "1. Print in order\n"
                            "2. Print pre order\n"
                            "3. Print post order\n");    
                    fscanf(stdin, "%u", &order);
                    printf("\n");
                    switch (order)
                    {
                        case 1:
                            abb_dump(tree, ABB_IN_ORDER);
                            printf("\n\n");
                            break;
                        case 2:
                            abb_dump(tree, ABB_PRE_ORDER);
                            printf("\n\n");
                            break;
                        case 3:
                            abb_dump(tree, ABB_POST_ORDER);
                            printf("\n\n");
                            break;
                        default:
                            printf("\nInvalid value for order.\n"
                                   "Please choose a valid option.\n\n");
                    }
                } while (order < 1 || order > 3);
                break;
            case 2:
                fprintf(stdout, "Element to add: ");    
                fscanf(stdin, "%d", &node_to_add);
                tree = abb_add(tree, node_to_add);
                break;
            case 3:
                fprintf(stdout, "Element to remove: ");    
                fscanf(stdin, "%d", &node_to_remove);
                tree = abb_remove(tree, node_to_remove);
                break;
            case 4:
                bool does_exist;
                fprintf(stdout, "Element to check existence: ");    
                fscanf(stdin, "%d", &node_exist);
                does_exist = abb_exists(tree, node_exist);
                does_exist ? printf("\nElement does exist.\n") 
                           : printf("\nElement doesn't exist.\n");
                break;
            case 5:
                printf("Tree length is: %u\n", abb_length(tree));
                break;
            case 6:
                if (!abb_is_empty(tree)) {
                    printf(" root: %d\n minimum:%d\n maximum:%d\n", 
                                                    abb_root(tree),
                                                    abb_min(tree),
                                                    abb_max(tree));
                } else {
                    printf("\nÁrbol vacío\n");
                }
                break;
            case 7:
                tree = abb_destroy(tree);
                printf("\nExiting.\n");
                break;
            default:
                printf("\nInvalid option.\n"
                        "Please choose a valid option.\n\n");
        }
    } while (option != 7);
    tree = abb_destroy(tree);
    return (EXIT_SUCCESS);
}
