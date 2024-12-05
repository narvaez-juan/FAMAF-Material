#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>

#include "command.h"
#include "parser.h"
#include "parsing.h"

static scommand parse_scommand(Parser p) {
    /* Devuelve NULL cuando hay un error de parseo en un scommand*/
    assert(p != NULL);
    scommand new_cmd = scommand_new();
    arg_kind_t arg_type;
    char *arg = parser_next_argument(p, &arg_type);

    while (arg != NULL) {
        if (arg_type == ARG_NORMAL) {
            scommand_push_back(new_cmd, arg);
        } else if (arg_type == ARG_INPUT) {
            scommand_set_redir_in(new_cmd, arg);
        } else if (arg_type == ARG_OUTPUT) {
            scommand_set_redir_out(new_cmd, arg);
        }
        arg = parser_next_argument(p, &arg_type);
    }

    if (scommand_is_empty(new_cmd) || arg_type == ARG_INPUT || 
    arg_type == ARG_OUTPUT) {
    	new_cmd = scommand_destroy(new_cmd);
        new_cmd = NULL;
    }

    return new_cmd;
}


pipeline parse_pipeline(Parser p) {
    /* Devuelve NULL cuando hay un error de parseo */
    assert(p != NULL && !parser_at_eof(p));
    pipeline result = pipeline_new();
    scommand cmd = NULL;
    bool error = false, another_pipe=true;
    bool is_background = false, is_garbage = false;

    // Parsea el primer scommand
    cmd = parse_scommand(p);
    error = (cmd == NULL);
    // Parsea scommands hasta no encontrar mas pipes
    while (another_pipe && !error) {
        pipeline_push_back(result, cmd);
        parser_skip_blanks(p);
        parser_op_pipe(p, &another_pipe);
        if (another_pipe) {
            cmd = parse_scommand(p);
            error = (cmd == NULL);
        }
    }

    // Setea pipeline wait si hubiera "&", y parsea lo sobrante 
    if (error) {
        parser_garbage(p, &is_garbage);
    } else {
    	parser_op_background(p, &is_background);
    	pipeline_set_wait(result, !is_background);
    	parser_garbage(p, &is_garbage);
    }
    
    // Si hubiera sobrante o un error, se considera comando invalido
    if (is_garbage || error) {
        result = pipeline_destroy(result);
        result = NULL;
		printf("Error: invalid command.\n");
    }
    
    return result;
}

