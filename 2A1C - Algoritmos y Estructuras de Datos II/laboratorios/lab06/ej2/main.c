#include <stdio.h>
#include "string.h"

int main(void) {
    string str1 = string_create("Hola mundo!");
    string str2 = string_create("Hello world!");

    bool is_equal = string_eq(str1, str2);
    bool is_less = string_less(str1, str2);

    is_equal ? printf("str1 = str2\n") : printf("str != str2\n");
    is_less ? printf("str1 < str2\n") : printf("str >= str2\n");

    str1 = string_destroy(str1);
    str2 = string_destroy(str2);
    
    return EXIT_SUCCESS;
}