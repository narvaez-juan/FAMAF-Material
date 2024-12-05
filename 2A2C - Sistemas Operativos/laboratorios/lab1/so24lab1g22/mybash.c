#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "builtin.h"
#include "command.h"
#include "execute.h"
#include "obfuscated.h"
#include "parser.h"
#include "parsing.h"


static void show_prompt(void) {
    printf ("mybash> ");
    fflush (stdout);
}

int main(int argc, char *argv[]) {

    pipeline pipe;
    Parser input;
    bool quit = false;

    input = parser_new(stdin);
    while (!quit) {
        ping_pong_loop(NULL);
        show_prompt();
        pipe = parse_pipeline(input);
        quit = parser_at_eof(input);

        if(pipe != NULL) {
            execute_pipeline(pipe);
            pipeline_destroy(pipe);
        }
    }
    parser_destroy(input); input = NULL;
    return EXIT_SUCCESS;
}

