#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "data.h"

void
print_data(data_t d) {
    printf("NOMBRE: %s\n"
           "EDAD  : %d años\n"
           "ALTURA: %d cm\n\n",
           d.name, d.age, d.height);
}

int main(void) {

    data_t messi = {"Leo Messi", 36, 169};
    print_data(messi);

    printf("name-size  : %lu bytes\n"
           "age-size   : %lu bytes\n"
           "height-size: %lu bytes\n"
           "data_t-size: %lu bytes\n\n",
            sizeof(messi.name),
            sizeof(messi.age),
            sizeof(messi.height),
            sizeof(messi));

    data_t *m = NULL;
    m = &messi;

    printf("name-direction   (uintptr_t): %lu\n"
           "age-direction    (uintptr_t): %lu\n"
           "height-direction (uintptr_t): %lu\n"
           "messi direction: (uintptr_t): %lu\n\n",
            (uintptr_t) &m->name,
            (uintptr_t) &m->age,
            (uintptr_t) &m->height,
            (uintptr_t) m);

    printf("name-direction   (%%p): %p\n"
           "age-direction    (%%p): %p\n"
           "height-direction (%%p): %p\n"
           "messi direction: (%%p): %p\n\n",
            (void *) &m->name,
            (void *) &m->age,
            (void *) &m->height,
            (void *) m);

    return EXIT_SUCCESS;
}

