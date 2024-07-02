#ifndef _LIST_H
#define _LIST_H

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

/* List as a pointer to structs to guarantee encapsulation */
typedef int list_elem;
typedef struct node_of_T *list;

/*              */
/* Constructors */
/*              */

list empty();
/* Create an empty list */

list addl(list_elem e, list l);
/* Adds element e to the beginning of list l */

/*              */
/*  Operations  */
/*              */

bool is_empty(list l);
/* Return true if l is empty */

list_elem head(list l);
/* Return the first element of the list l */
/* PRE: not is_empty(l) */

list tail(list l);
/* Removes the first element of the list l */
/* PRE: not is_empty(l) */

list addr(list l, list_elem e);
/* Adds element e to the end of list l */

int length(list l);
/* Returns the number of elements in the list l */

list concat(list l1, list l2);
/* Adds all the elements of l2 to the end of l1 in the same order */

list_elem index(list l, int n);
/* Returns the n'th element of the list l */
/* PRE: length(l) > n */

list take(list l, int n);
/* Leaves only the first n elements in l, removing the rest */

list drop(list l, int n);
/* Removes the first n elements from l */

list copy_list(list l);
/* Copy all elements from l to the new list */

/*           */
/*  Destroy  */
/*           */

list destroy(list l);
/* Free memory if necessary */


#endif