#include <assert.h>
#include <glib.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include "builtin.h"
#include "command.h"
#include "execute.h"
#include "tests/syscall_mock.h"


static void change_fd_in(scommand scmd) {
    /* Cambia donde redirigir la entrada si el scommand lo especifica */
    char *sc_input = scommand_get_redir_in(scmd); 
    if (sc_input != NULL) {
        int fd_in = open(sc_input, O_RDONLY,0);
        if (fd_in < 0) {
            perror("open redir_in");
            exit(EXIT_FAILURE);
        }
        if (dup2(fd_in, STDIN_FILENO) < 0) {
            perror("dup2 redir_in");
            close(fd_in);
            exit(EXIT_FAILURE);
        }
        close(fd_in);
    }
}

static void change_fd_out(scommand scmd) {
    /* Cambia donde redirigir la salida si el scommand lo especifica */
    char *sc_output = scommand_get_redir_out(scmd);
    if (sc_output != NULL) {
        int fd_out = open(sc_output, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd_out < 0) {
            perror("open redir_out");
            exit(EXIT_FAILURE);
        }
        if (dup2(fd_out, STDOUT_FILENO) < 0) {
            perror("dup2 redir_out");
            close(fd_out);
            exit(EXIT_FAILURE);
        }
        close(fd_out);
    }
}


static void run_external_command(scommand cmd) {
    assert(cmd != NULL && !scommand_is_empty(cmd));

    // Cambia archivos de redirección de input/output si el comando lo pidiera  
    change_fd_in(cmd);
    change_fd_out(cmd);
    
    // Obtiene el número de argumentos
    unsigned int len = scommand_length(cmd);

    // Asigna el espacio para el array de argumentos
    char **argv = calloc(len + 1, sizeof(char *));
    if (argv == NULL) {
        perror("calloc");
        exit(EXIT_FAILURE);
    }

    // Rellena el array con argumentos
    for (unsigned int i = 0; i < len; i++) {
        argv[i] = strdup(scommand_front(cmd));
        if (argv[i] == NULL) {
            perror("strdup");
            exit(EXIT_FAILURE);
        }
        scommand_pop_front(cmd);
    }
    argv[len] = NULL;

    // Ejecuta el comando
    execvp(argv[0], argv);

    // Si execvp falla, imprime un mensaje y termina el proceso
    perror(argv[0]);
    exit(EXIT_FAILURE);
}


static void run_command (scommand cmd){
    /* Ejecuta un comando sea interno o externo */
    assert(cmd != NULL);
    if (builtin_is_internal(cmd)) {
        builtin_run(cmd);
        exit(EXIT_SUCCESS);
    } else if (!scommand_is_empty(cmd)) {
        run_external_command(cmd);
    } else {
        exit(EXIT_SUCCESS);
    }
}


static unsigned int single_command_pipeline(pipeline apipe) {
    /* Ejecuta un pipeline de 1 solo comando  */
    unsigned int child_running = 0u;
    if (builtin_alone(apipe)){
        scommand cmd = pipeline_front(apipe);
        builtin_run(cmd);
    } else {
        pid_t pid = fork();
        if (pid < 0){
            perror("fork");
            return child_running;
        } else if (pid == 0) {
            run_command(pipeline_front(apipe));
        } else {
            child_running++;
        }
    }
    return child_running;
}


static unsigned int multiple_commands(pipeline apipe) {
    /* Ejecuta un pipeline de multiples comandos */
    assert(apipe != NULL && pipeline_length(apipe) >= 2u);

    unsigned int child_run = 0u;
    unsigned int numberOfPipes = pipeline_length(apipe) - 1u;

    // Reserva memoria para los descriptores de archivo de los pipes
    int* pipesfd = calloc(2 * numberOfPipes, sizeof(int));
    if (pipesfd == NULL) {
        perror("calloc");
        return child_run;
    }

    // Crea los pipes necesarios
    for (unsigned int i = 0u; i < numberOfPipes; i++) {
        if (pipe(pipesfd + i * 2) < 0) {
            perror("pipe");
            // Cierra los pipes abiertos y libera memoria en caso de error
            for (unsigned int j = 0u; j < 2u * i; j++) {
                close(pipesfd[j]);
            }
            free(pipesfd);
            return child_run;
        }
    }

    // Ejecuta comandos en el pipeline
    unsigned int j = 0u;
    while (!pipeline_is_empty(apipe)) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            break;
        }

        if (pid == 0) {
            // Configura la redirección de salida para el comando actual
            if (pipeline_length(apipe) > 1u) {
                if (dup2(pipesfd[j + 1], STDOUT_FILENO) < 0) {
                    perror("dup2");
                    exit(EXIT_FAILURE);
                }
            }

            // Configura la redirección de entrada para el comando actual
            if (j > 0) {
                if (dup2(pipesfd[j - 2], STDIN_FILENO) < 0) {
                    perror("dup2");
                    exit(EXIT_FAILURE);
                }
            }

            // Cierra todos los descriptores de archivo
            for (unsigned int i = 0u; i < 2u * numberOfPipes; i++) {
                close(pipesfd[i]);
            }

            // Ejecuta el comando
            run_command(pipeline_front(apipe));
            exit(EXIT_SUCCESS);
        } else {
            pipeline_pop_front(apipe);
            j += 2u;
            child_run++;
        }
    }

    // Cierra todos los descriptores de archivo en el proceso padre
    for (unsigned int i = 0u; i < 2u * numberOfPipes; i++) {
        close(pipesfd[i]);
    }

    // Libera memoria
    free(pipesfd);

    return child_run;
}

static unsigned int execute_foreground (pipeline apipe) {
    /* Ejecuta pipelines de comandos en primer plano */
    assert(apipe != NULL);
    unsigned int lenght = pipeline_length(apipe);
    unsigned int child_run = 0u;
    if (lenght == 1) {
        child_run = single_command_pipeline(apipe);
    } else if (lenght >= 2) {
        child_run = multiple_commands(apipe);
    }
    return child_run;
}


void execute_pipeline(pipeline apipe) {
    assert(apipe != NULL);

    // Si el pipeline está vacío, no hacer nada
    if (pipeline_length(apipe) == 0) {
        return;
    }

    // Obtiene el primer comando simple (para manejar redirecciones)
    scommand cmd = pipeline_front(apipe);

    // Ejecuta en foreground o background
    if (pipeline_get_wait(apipe)) {
        // Ejecuta en foreground
        unsigned int child_run = execute_foreground(apipe);

        // Espera que todos los hijos terminen
        while (child_run > 0u) {
            wait(NULL);
            child_run--;
        }
    } else {
        // Ejecuta en background
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            return;
        } else if (pid == 0) {
            // Redirecciona archivos de entrada/salida si se especifica
            change_fd_in(cmd);
            change_fd_out(cmd);

            // Ejecuta el comando
            execute_foreground(apipe);

            // Termina el proceso hijo
            exit(EXIT_SUCCESS);
        } else {
            // Proceso padre: NO espera a los hijos en background
            printf("Proceso en segundo plano, PID: %d\n", pid);
        }
    }
}

