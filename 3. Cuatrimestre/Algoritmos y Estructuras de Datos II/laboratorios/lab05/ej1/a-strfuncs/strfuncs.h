#ifndef _STR_FUNCS
#define _STR_FUNCS

#include <stdbool.h>


/* Returns the length of string <str> */
size_t string_length(const char *str);

/* Returns a filtered string with the <c> char removed */
char *string_filter(const char *str, char c);

/* Returns true if string is symmetric, false otherwise */
bool string_is_symmetric(const char *str);


#endif