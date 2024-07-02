#include <stdlib.h>

#include "strfuncs.h"


size_t string_length(const char *str) {
    size_t i = 0;
    while (str[i] != '\0') {
        i++;
    }
    return i;
}


char *string_filter(const char *str, char c) {
    char *filtered = NULL;
    int iterator = 0;
    int counter = 0;
    int length_filtered = 0;
    while (str[iterator] != '\0') {
        if (str[iterator] == c) {
            counter++;
        }
        iterator++;
    }
    length_filtered = iterator - counter;
    filtered = malloc(sizeof(char) * (length_filtered + 1));
    iterator = 0;
    counter = 0;
    while (str[iterator] != '\0') {
        if (str[iterator] != c) {
            filtered[counter] = str[iterator];
            counter++;
        }
        iterator++;
    }
    filtered[counter] = '\0';
    return filtered;
}


bool string_is_symmetric(const char *str) {
    bool symmetric = true;
    size_t length = string_length(str);
    int i = 0;
    size_t j = length - 1;
    while (i < ((int) length / 2) && symmetric) {
        if (str[i] != str[j]) {
            symmetric = false;
        }
        i++;
        j--;
    }
    return symmetric;
}