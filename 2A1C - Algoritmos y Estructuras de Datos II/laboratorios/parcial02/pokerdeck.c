#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#include <assert.h>

#include "pokerdeck.h"

struct s_pokerdck {
    struct s_node *first;
    struct s_node *last;
    unsigned int suit_counts[CARD_SUITS];
    unsigned int size;
};

struct s_node {
    cardnum_t num;
    cardsuit_t suit;
    struct s_node *nextcard;
};

typedef struct s_node * node_t;

// Auxiliar dump functions
static void dump_suit(cardsuit_t suit) {
    printf("%s", suit==spades   ? "♠️  ":
                 suit==hearts   ? "♥️  ":
                 suit==diamonds ? "♦️  ":
                 suit==clubs    ? "♣️  ": "???");
}

static void dump_num(cardnum_t num) {
    if (1 < num && num < 11) {
        printf("%-2d", num);
    } else {
        printf("%-2s", num==1 ? "A":
                       num==11 ? "J":
                       num==12 ? "Q":
                       num==13 ? "K": "???");

    }
}

// Representation invariant
static bool invrep(pokerdeck deck) {
    bool valid=true;
    if (deck != NULL) {
        node_t p = deck->first;
        while (p != NULL && valid) {
            valid = (p->num >= 1) && (p->num <= 13);
            valid = (p->suit == spades) || (p->suit == hearts) || (p->suit == diamonds) || (p->suit == clubs);
            p = p->nextcard;
        }
    }       
    return valid;
}

// Creates a single node in dynamic memory with a given card
static node_t create_node(cardnum_t num, cardsuit_t suit) {
    node_t newnode=NULL;
    newnode = malloc(sizeof(struct s_node));
    assert(newnode != NULL);
    newnode->num = num;
    newnode->suit = suit;
    newnode->nextcard = NULL;
    assert(newnode!=NULL);
    return newnode;
}

// Destroy a single node
static node_t destroy_node(node_t node) {
    free(node);
    node = NULL;
    assert(node==NULL);
    return node;
}

// Public functions of the Abstract Data Type
pokerdeck pokerdeck_empty(void) {
    pokerdeck pd = malloc(sizeof(struct s_pokerdck));
    assert(pd != NULL);
    pd->first = NULL;
    pd->last = NULL;
    pd->size = 0;
    for (int i = 0; i < CARD_SUITS; i++) {
        pd->suit_counts[i] = 0;
    }
    assert(pokerdeck_is_empty(pd) && invrep(pd));
    return pd;
}


bool pokerdeck_is_empty(pokerdeck deck) {
    assert(invrep(deck));
    bool is_empty = false;
    is_empty = (deck->first == NULL);
    assert(invrep(deck));
    return is_empty;
}


pokerdeck pokerdeck_add(pokerdeck deck, cardnum_t num, cardsuit_t suit) {
    assert(invrep(deck));
    node_t new_node = create_node(num, suit);
    new_node->nextcard = NULL;
    if (pokerdeck_is_empty(deck)) {
        deck->first = new_node;
    } else {
        deck->last->nextcard = new_node;
    }
    deck->last = new_node;
    deck->suit_counts[suit]++;
    deck->size++;
    assert(invrep(deck) && !pokerdeck_is_empty(deck));
    return deck;
}


pokerdeck pokerdeck_push(pokerdeck deck, cardnum_t num, cardsuit_t suit) {
    assert(invrep(deck));
    node_t newnode = create_node(num, suit);
    newnode->nextcard = deck->first;
    deck->first = newnode;
    deck->suit_counts[suit]++;
    deck->size++;
    assert(invrep(deck) && !pokerdeck_is_empty(deck));
    return deck;
}

pokerdeck pokerdeck_pop(pokerdeck deck, cardnum_t *popped_num, cardsuit_t *popped_suit) {
    assert(invrep(deck) && !pokerdeck_is_empty(deck));
    node_t aux = deck->first;
    deck->first = deck->first->nextcard;
    if (popped_num!=NULL) *popped_num=aux->num;
    if (popped_suit!=NULL) *popped_suit=aux->suit;
    deck->suit_counts[aux->suit]--;
    deck->size--;
    aux = destroy_node(aux);
    assert(invrep(deck));
    return deck;
}

unsigned int pokerdeck_length(pokerdeck deck) {
    assert(invrep(deck));
    unsigned int length = deck->size;
    assert(invrep(deck) && pokerdeck_is_empty(deck) == (length == 0));
    return length;
}

pokerdeck pokerdeck_remove(pokerdeck deck, cardnum_t num, cardsuit_t suit) {
    assert(invrep(deck));
    if (!pokerdeck_is_empty(deck)) {
        node_t prev = NULL;
        node_t curr = deck->first;

        while (curr != NULL) {
            if (curr->num == num && curr->suit == suit) {
                if (prev == NULL) {
                    deck->first = curr->nextcard;
                } else {
                    prev->nextcard = curr->nextcard;
                }

                if (deck->last == curr) {
                    deck->last = prev;
                }
                deck->suit_counts[suit]--;
                deck->size--;
                destroy_node(curr); // Liberar memoria del nodo encontrado
                break; // Salir del bucle una vez se remueva el nodo
            }
            prev = curr;
            curr = curr->nextcard;
        }
    }
    assert(invrep(deck));
    return deck;
}


unsigned int pokerdeck_count(pokerdeck deck, cardsuit_t suit) {
    assert(invrep(deck));
    unsigned int count = deck->suit_counts[suit];
    assert(invrep(deck) && pokerdeck_is_empty(deck) == (count == 0));
    return count;
}

struct card * pokerdeck_to_array(pokerdeck deck) {
    assert(invrep(deck));
    unsigned int length = pokerdeck_length(deck);
    struct card *array = NULL;
    if (length != 0) {
        array = malloc(length * sizeof(struct card));
        assert(array != NULL);
        node_t current = deck->first;
        for (unsigned int i = 0; i < length; i++) {
            array[i].num = current->num;
            array[i].suit = current->suit;
            current = current->nextcard;
        }
    }

    assert(invrep(deck) && (pokerdeck_length(deck) == 0) == (array == NULL));
    return array;
}

void card_dump(cardnum_t num, cardsuit_t suit) {
    printf("|");
    dump_num(num);
    printf(" ");
    dump_suit(suit);
    printf("|");
}

void pokerdeck_dump(pokerdeck deck) {
    assert(invrep(deck));
    node_t node = deck->first;
    while (node != NULL) {
        card_dump(node->num, node->suit);
        printf(" ");
        node = node->nextcard;
    }
    printf("\n");
}

pokerdeck pokerdeck_destroy(pokerdeck deck) {
    assert(invrep(deck));
    while (!pokerdeck_is_empty(deck)) {
        node_t aux = deck->first;
        deck->first = deck->first->nextcard;
        destroy_node(aux);
    }
    free(deck);
    deck = NULL;
    assert(deck == NULL);
    return deck;
}

