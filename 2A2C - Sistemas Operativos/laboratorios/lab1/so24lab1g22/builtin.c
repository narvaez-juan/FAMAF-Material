#include <assert.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "builtin.h"
#include "command.h"
#include "strextra.h"
#include "tests/syscall_mock.h"

const char *built_in_cmds[] = {"cd", "help", "exit"};
const unsigned int BUILTIN_LIST_SIZE = 3;


bool builtin_is_internal(scommand cmd) {
    assert(cmd != NULL);
    char *cmd_name = scommand_front(cmd);
    for (unsigned int i = 0; i < BUILTIN_LIST_SIZE; i++) {
        if (!strcmp(cmd_name, built_in_cmds[i])) {
            return true;
        }
    }
    return false;
}


bool builtin_alone(pipeline p) {
    assert(p != NULL);
    return (pipeline_length(p) == 1) && (builtin_is_internal(pipeline_front(p)));
}


void builtin_run(scommand cmd) {
    assert(builtin_is_internal(cmd));

    // cd built_in command
    if (!strcmp(scommand_front(cmd), built_in_cmds[0])) {
        
        unsigned int cmd_len = scommand_length(cmd);
        int rc = 0;

        if (cmd_len > 2u) {
            rc = -1;
            printf("cd: too many arguments\n");

        } else if (cmd_len == 2u){

            scommand_pop_front(cmd);
            char *home_path = getenv("HOME");
            char *input_path = strmerge("", scommand_front(cmd));
            char *full_path = NULL;
            assert(home_path != NULL);

            if (input_path[0] == '~' && input_path[1] == '/') {
                unsigned int len = strlen(input_path);
                char *tmp = malloc(len + 1);
                tmp = strncpy(tmp, input_path + 1, len);
                tmp[len] = '\0';
                full_path = strmerge(home_path, tmp);
                rc = chdir(full_path);
                free(tmp);
            } else if (input_path[0] == '~' && strlen(input_path) == 1) {
                rc = chdir(home_path);
            } else {
                rc = chdir(input_path);
            }
            if (rc == -1) {
                printf("cd: failure calling chdir\n");
            }
        
        } else {
            char *home_path = getenv("HOME");
            rc = chdir(home_path);
            if (rc == -1) {
                printf("cd: failure calling chdir\n");
            }
        }

    // help built_in command
    } else if (!strcmp(scommand_front(cmd), built_in_cmds[1])) {

        printf( "This is a simple command line interpreter called MyBash. \n"
                "Authors: Juan Narvaez, Nicolás Contrera, María José Aranda, Matías Gabriel García Casas.\n"
                    "You can use these commands: 1) 'cd', 2) 'help', 3) 'exit'\n"
                    "1) 'cd <pathname>' let you change the current directory\n"
                    "2) 'help' short description of available command\n"
                    "3) 'exit' terminates mybash.\n");
    
    // exit built_in command
    } else if (!strcmp(scommand_front(cmd), built_in_cmds[2])) {
        exit(EXIT_SUCCESS);
    }
}