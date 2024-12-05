#include <assert.h>
#include <glib.h> 
#include <stdbool.h> 
#include <stdio.h>
#include <stdlib.h>

#include "command.h"
#include "strextra.h"


/* TAD SCOMMAND */
/*
    Contiene una lista con los argumentos del comando ej: ls -l ej1.c, 
    sería ["ls", "-l", "ej1.c", NULL].
    Contiene también el nombre del archivo al que se leerá la entrada y/o
    el nombre del archivo al que se redirigirá la salida del comando.
*/
struct scommand_s {
    GSList * arg_name;
    char* input; 
    char* output;
};


scommand scommand_new(void) {
    scommand com = NULL;
    com = malloc(sizeof(struct scommand_s)); 
    com->arg_name = NULL;
    com->input= NULL;
    com->output = NULL;
    assert(com != NULL && scommand_is_empty (com) &&
    scommand_get_redir_in (com) == NULL &&
    scommand_get_redir_out (com) == NULL);
    return com;

}


scommand scommand_destroy(scommand self) {  
    assert(self != NULL);
    while (!scommand_is_empty(self)) {    
        scommand_pop_front(self);        
    }
    g_slist_free(self->arg_name);
    self->arg_name = NULL;
    free(self->input);
    free(self->output);
    self->input = NULL;
    self->output = NULL;
    free(self);
    self = NULL;
    assert(self == NULL);
    return self;
}


void scommand_push_back(scommand self, char * argument) {
    assert(self!=NULL && argument!=NULL);
    self->arg_name = g_slist_append(self->arg_name, argument); 
    assert(!scommand_is_empty(self));
}

void scommand_pop_front(scommand self) {
    assert(self!=NULL && !scommand_is_empty(self));
    free(g_slist_nth_data(self->arg_name, 0));
    self->arg_name = g_slist_remove(self->arg_name, 
                                    g_slist_nth_data(self->arg_name, 0));
}


void scommand_set_redir_in(scommand self, char * filename) {
    assert(self != NULL);
    free(self->input);
    self->input = filename;
}

void scommand_set_redir_out(scommand self, char * filename) {
    assert(self != NULL);
    free(self->output);
    self->output = filename;
}

bool scommand_is_empty(const scommand self) {
    assert(self != NULL); 
    bool res = self->arg_name == NULL; 
    return res;
}

unsigned int scommand_length(const scommand self) {
    assert(self != NULL);
    unsigned int length;
    length = g_slist_length(self->arg_name);
    assert((length == 0) == scommand_is_empty(self));
    return length;
}

char * scommand_front(const scommand self) {
    assert(self != NULL && !scommand_is_empty(self));
    char *res;
    res = g_slist_nth_data(self->arg_name,0);
    assert(res != NULL);
    return res;
}

char * scommand_get_redir_in(const scommand self) {
    assert(self != NULL); 
    return (self->input);
}

char * scommand_get_redir_out(const scommand self) {
    assert(self != NULL); 
    return (self->output);
}


char *scommand_to_string(const scommand self) {
    assert(self != NULL);
    char *res = strdup("");
    assert(res != NULL);
    GSList *l = self->arg_name;

    // Convierte cada argumento a string y los concatena
    while (l != NULL) {
        char *arg = (char *)l->data;
        char *new_res = strmerge(res, arg);
        free(res);
        res = strmerge(new_res, " ");
        free(new_res);                                 
        assert(res != NULL);
        l = g_slist_next(l);
    }

    // Si el último caracter es un espacio, lo elimino
    size_t len = strlen(res);
    if (len > 0 && res[len - 1] == ' ') {
        res[len - 1] = '\0'; 
    }

    // Agrego " < " si existe output
    if (self->input != NULL) {
        char *input_str = strmerge(" < ", self->input);
        char *new_res = strmerge(res, input_str);
        free(res);
        free(input_str);
        res = new_res;
        assert(res != NULL);
    }

    // Agrego " > " si existe output
    if (self->output != NULL) {
        char *output_str = strmerge(" > ", self->output);
        char *new_res = strmerge(res, output_str);
        free(res);
        free(output_str);
        res = new_res;
        assert(res != NULL);
    }

    return res;
}


/* TAD PIPELINE */
struct pipeline_s {
    GSList* scmd;
    bool wait;
};

pipeline pipeline_new(void) {
    pipeline new = malloc(sizeof(struct pipeline_s));
    new->scmd = NULL;
    new->wait = true;
    assert(new != NULL && pipeline_is_empty(new) && pipeline_get_wait(new));
    return new;
}


pipeline pipeline_destroy(pipeline self) {
    assert(self != NULL);
    while (!pipeline_is_empty(self)) {
        pipeline_pop_front(self); 
    }
    g_slist_free(self->scmd);
    self->scmd = NULL;
    free(self);
    self = NULL;
    assert(self == NULL);
    return self;
}

void pipeline_push_back(pipeline self, scommand sc) {
    assert(self != NULL && sc != NULL);
    self->scmd = g_slist_append(self->scmd,sc); 
    assert(!pipeline_is_empty(self));
}


void pipeline_pop_front(pipeline self) {
    assert(self != NULL && !pipeline_is_empty(self));
    scommand_destroy(g_slist_nth_data(self->scmd, 0));
    self->scmd = g_slist_remove(self->scmd, 
                                g_slist_nth_data(self->scmd, 0));
}

void pipeline_set_wait(pipeline self, const bool w) {
    assert(self != NULL);
    self->wait = w;
}


bool pipeline_is_empty(const pipeline self) {
    assert(self != NULL);
    bool res;
    res = self->scmd == NULL;
    return res;
}


unsigned int pipeline_length(const pipeline self) {
    assert(self != NULL);
    unsigned int length;
    length = g_slist_length(self->scmd);
    assert((length == 0) == pipeline_is_empty(self));
    return length;
}

scommand pipeline_front(const pipeline self) {
    assert(self != NULL && !pipeline_is_empty(self));
    assert(g_slist_nth_data(self->scmd, 0) != NULL);
    return g_slist_nth_data(self->scmd, 0);
}

bool pipeline_get_wait(const pipeline self) {
    assert(self != NULL); 
    bool res;
    res = self->wait;
    return res;
}


static char* pipeline_to_string_aux(char* chars, const scommand self) {
    assert(chars != NULL && self != NULL);
    char* str_scmd = scommand_to_string(self);
    chars = strmerge(chars, str_scmd);              
    free(str_scmd);
    str_scmd = NULL;
    return (chars);
}


char * pipeline_to_string(const pipeline self) {
    assert(self != NULL); 
    char * res = strdup("");
    GSList *com = self->scmd;
    if (com != NULL) {
        // Convierte a string el primer scommand
        res = pipeline_to_string_aux(res, g_slist_nth_data(com, 0));
        com = g_slist_next(com);

        // Mientras haya scommands, concantena "|" y el siguiente scommand 
        while (com != NULL) {
            res = strmerge(res, " | ");
            res = pipeline_to_string_aux(res,g_slist_nth_data(com, 0));
            com = g_slist_next(com);
        }

        // Si el pipeline tiene que esperar, añade "&" al final del string
        if (!pipeline_get_wait(self)) {
            res = strmerge(res, " &");
        }
    }
    assert(pipeline_is_empty(self) || 
            pipeline_get_wait(self) ||
            strlen(res)>0); 
    return res;
}