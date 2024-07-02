#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "list.h"

/* List data type implementation */
struct node_of_T
{
    list_elem elem;
    struct node_of_T *next;
};


/* List functions implementation */

list empty() {
    list l = NULL;
    return l;
}

list addl(list_elem e, list l) {
    list p = malloc(sizeof(struct node_of_T));
    if (p == NULL) {
        fprintf(stderr, "Not enough memory.\n");
        exit(EXIT_FAILURE);
    }
    p->elem = e;
    p->next = l;
    l = p;
    return l;
}

bool is_empty(list l) {
    return (l == NULL);
}

list_elem head(list l) {
    assert(!is_empty(l) && "l is an empty list.\n");
    return l->elem;
}

list tail(list l) {
    assert(!is_empty(l) && "l is an empty list.\n");
    list p = l;
    l = l->next;
    free(p);
    return l;
}

list addr(list l, list_elem e) {
    list node = malloc(sizeof(struct node_of_T));
    if (node == NULL) {
        fprintf(stderr, "Not enough memory.\n");
        exit(EXIT_FAILURE);
    }
    node->elem = e;
    node->next = NULL;
    if (!is_empty(l)) 
    {
        list p = l;
        while (p->next != NULL) {
            p = p->next;
        }
        p->next = node;
    } 
    else 
    {
        l = node;
    }
    return l;
}

int length(list l) {
    int len = 0;
    list p = l;
    while (p != NULL) {
        p = p->next;
        len++;
    }
    return len;
}

list concat(list l1, list l2) {
    list l = NULL;
    if (!is_empty(l1)) {
        l = l2;
    } else {
        l = l1;
        while (l->next != NULL) {
            l = l->next; 
        }
        l->next = l2;
    }
    return l;
}

list_elem index(list l, int n) {
    assert(length(l) > n && "indexed element doesn't exist.\n");
    int i = 0;
    list p = l;
    while (i < n) {
        p = p->next;
        i++;
    }
    return p->elem;
}

list take(list l, int n) {
    list p = NULL;
    list q = NULL;
    int i = 0;
    p = l;
    if (n == 0) {
        while (!is_empty(l)) {
            p = l;
            l = l->next;
            free(p);
        }
    }
    else {
        while(p != NULL && i < n) {
            p = p->next;
            i++;
        }
        
        while(p != NULL) {
            q = p;
            p = p->next;
            free(q);
        }
    }
    return l;
}


list drop(list l, int n) {
    list p = NULL;
    int i = 0;
    if (!is_empty(l) && 0 < n) {
        while (l != NULL && i < n) {
            p = l;
            l = l->next;
            free(p);
            i++;
        }
    }
    return l;
}

list copy_list(list l) {
    list copy = empty();
    list p = l;
    while (p != NULL) {
		copy = addr(copy, p->elem);
		p = p->next;
	}
	return copy;
}

/*           */
/*  Destroy  */
/*           */

list destroy(list l) {
    list p = l;
    while (!is_empty(l)) {
        p = l;
        l = l->next;
        free(p);
    }
    return l;
}