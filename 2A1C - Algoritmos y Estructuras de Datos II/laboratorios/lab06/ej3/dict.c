#include <assert.h>
#include <stdlib.h>

#include "dict.h"
#include "key_value.h"

struct _node_t {
    dict_t left;
    dict_t right;
    key_t key;
    value_t value;
};

static bool invrep(dict_t d) {
    bool inv = true;
    if (d != NULL) {
        if (d->left != NULL) {
            inv &= (key_less(d->left->key, d->key));
        }
        if (d->right != NULL) {
            inv &= (key_less(d->key, d->right->key));
        }   
        inv &= invrep(d->left);
        inv &= invrep(d->right);
    }
    return inv;
}

dict_t dict_empty(void) {
    dict_t dict = NULL;
    assert(invrep(dict) && dict_length(dict) == 0);
    return dict;
}

dict_t dict_add(dict_t dict, key_t word, value_t def) {
    assert(invrep(dict));
    if (dict == NULL) {
        dict = malloc(sizeof(struct _node_t));
        dict->key = word;
        dict->value = def;
        dict->left = NULL;
        dict->right = NULL;
    } else if (key_eq(dict->key, word)) {
        dict->value = def;
    } else if (key_less(word, dict->key)) {
        dict->left = dict_add(dict->left, word, def);
    } else {
        dict->right = dict_add(dict->right, word, def);
    }
    assert(invrep(dict) && key_eq(def, dict_search(dict, word)));
    return dict;
}

value_t dict_search(dict_t dict, key_t word) {
    assert(invrep(dict));
    key_t def;
    if (dict == NULL) {
        def = NULL;
    } else {
        if (key_eq(dict->key, word)) {
            def = dict->value;
        } else if (key_less(word, dict->key)) {
            def = dict_search(dict->left, word);
        } else {
            def = dict_search(dict->right, word);
        }
    }
    assert((def != NULL) == (dict_exists(dict, word)));
    return def;
}

bool dict_exists(dict_t dict, key_t word) {
    assert(invrep(dict));
    bool exists = false;
    if (dict != NULL) 
    {
        if (key_eq(dict->key, word)) {
            exists = true;
        } else if (key_less(word, dict->key)) {
            exists = dict_exists(dict->left, word);
        } else {
            exists = dict_exists(dict->right, word);
        }
    }
    assert(invrep(dict));
    return exists;
}

unsigned int dict_length(dict_t dict) {
    assert(invrep(dict));
    unsigned int length = 0u;
    if (dict != NULL) {
        length += 1 + dict_length(dict->left) + dict_length(dict->right);
    }
    assert(invrep(dict));
    return length;
}

dict_t dict_remove(dict_t dict, key_t word) {
    assert(invrep(dict));
    if (dict != NULL) {
        if (key_eq(word, dict->key)) {
            dict_t tmp = NULL;
            if (dict->left == NULL) {
                tmp = dict;
                dict = dict->right;
                tmp->key = key_destroy(tmp->key);
                tmp->value = value_destroy(tmp->value);
                free(tmp);
                tmp = NULL;
            } else if (dict->right == NULL) {
                tmp = dict;
                dict = dict->left;
                tmp->key = key_destroy(tmp->key);
                tmp->value = value_destroy(tmp->value);
                free(tmp);
                tmp = NULL;
            } else {
                tmp = dict->right;
                while(tmp && tmp->left != NULL) { tmp = tmp->left; }
                dict->key = tmp->key;
                dict->right = dict_remove(dict->right, tmp->key);
            }
        } else if (key_less(word, dict->key)) {
            dict->left = dict_remove(dict->left, word);
        } else {
            dict->right = dict_remove(dict->right, word);
        }
    }
    assert(invrep(dict) && !dict_exists(dict, word));
    return dict;
}

dict_t dict_remove_all(dict_t dict) {
    assert(invrep(dict));
    if (dict != NULL) {
        dict->key = key_destroy(dict->key);
        dict->value = value_destroy(dict->value);
        dict->left = dict_remove_all(dict->left);
        dict->right = dict_remove_all(dict->right);
        free(dict);
        dict = NULL;
    }
    assert(invrep(dict) && dict_length(dict) == 0);    
    return dict;
}

void dict_dump(dict_t dict, FILE *file) {
    assert(invrep(dict) && file != NULL);
    if (dict != NULL) {
        dict_dump(dict->left,file);
        key_dump(dict->key,file);
        fprintf(file," : ");
        value_dump(dict->value,file);
        fprintf(file,"\n");
        dict_dump(dict->right,file);
    }
}

dict_t dict_destroy(dict_t dict) {
    assert(invrep(dict));
    if (dict != NULL) {
        dict_remove_all(dict);
        dict = NULL;
    }
    assert(dict == NULL);
    return dict;
}
