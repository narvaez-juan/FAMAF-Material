#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

#include "array_helpers.h"
#include "sort_helpers.h"
#include "sort.h"


static unsigned int partition(int a[], unsigned int izq, unsigned int der) {
    /* Permutes elements of a[izq..der] and returns pivot such that:
     - izq <= pivot <= der
     - elements in a[izq,pivot) all 'go_before' (according to function goes_before) a[pivot]
     - a[pivot] 'goes_before' all the elements in a(pivot,der]
    */

    unsigned int ppiv = izq;
    unsigned int i = izq + 1;
    unsigned int j = der;

    while (i <= j)
    {
        if (goes_before(a[i], a[ppiv])) {
            i++;
        } else if (goes_before(a[ppiv], a[j])) {
            j--;
        } else if (goes_before(a[ppiv], a[i]) && goes_before(a[j], a[ppiv])) {
            swap(a, i, j);
        }
    }

    swap(a, ppiv, j);
    ppiv = j;

    return ppiv;
}

static void quick_sort_rec(int a[], unsigned int izq, unsigned int der) {
    unsigned int ppiv;

    if (der > izq)
    {
        ppiv = partition(a, izq, der);
        if (ppiv == 0){
            quick_sort_rec(a, izq, 0u);
        } else {
            quick_sort_rec(a, izq, ppiv - 1u);
        }
        quick_sort_rec(a, ppiv + 1, der);
    }
}

void quick_sort(int a[], unsigned int length) {
    quick_sort_rec(a, 0, (length == 0) ? 0 : length - 1);
}

