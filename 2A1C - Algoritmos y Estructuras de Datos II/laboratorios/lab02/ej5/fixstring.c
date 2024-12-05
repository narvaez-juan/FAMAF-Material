#include <stdbool.h>
#include <assert.h>

#include "fixstring.h"

unsigned int fstring_length(fixstring s) {
    unsigned int length = 0;

    while (s[length] != '\0')
    {
        length++;
    }

    return length;
}

bool fstring_eq(fixstring s1, fixstring s2) {
    unsigned int s1_length = fstring_length(s1);
    unsigned int s2_length = fstring_length(s2);
    unsigned int i = 0;

    bool equal_fstrings = true;

    if (s1_length != s2_length)
    {
        equal_fstrings = false;
    }
    else
    {
        while (i < s1_length && equal_fstrings)
        {
            if (s1[i] != s2[i])
            {
                equal_fstrings = false;
            }
            i++;
        }
    }

    return equal_fstrings;
}

bool fstring_less_eq(fixstring s1, fixstring s2) {
    unsigned int fs1_len = fstring_length(s1);
    unsigned int fs2_len = fstring_length(s2);
    unsigned int min_length = fs1_len < fs2_len ? fs1_len : fs2_len;
    bool continue_cycle = true;
    bool less_eq_fstr = true;
    unsigned int i = 0;

    if (fstring_eq(s1, s2))
    {
        less_eq_fstr = true;
    }
    else
    {
        less_eq_fstr = fs1_len < fs2_len;

        while (i < min_length && continue_cycle)
        {
            if (s1[i] < s2[i])
            {
                less_eq_fstr = true;
                continue_cycle = false;
            }
            else if (s1[i] > s2[i])
            {
                less_eq_fstr = false;
                continue_cycle = false;
            }
            i++;
        }
    }

    return less_eq_fstr;
}

void fstring_set(fixstring s1, const fixstring s2) {
    int i=0;
    while (i<FIXSTRING_MAX && s2[i]!='\0') {
        s1[i] = s2[i];
        i++;
    }
    s1[i] = '\0';
}

void fstring_swap(fixstring s1,  fixstring s2) {
    fixstring aux;
    fstring_set(aux, s1);
    fstring_set(s1, s2);
    fstring_set(s2, aux);
}


