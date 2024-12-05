#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/*
    Usar todas las syscalls anteriores para ejecutar 10 programas
    que esperen durante 5 segundos de manera concurrente (todos al
    mismo tiempo), y que imprima “listo” después de que todos los
    procesos hijos terminan de ejecutarse.
*/

int main(void) {
    char *cmd = "sleep";
    char *argv[3];

    argv[0] = cmd;
    argv[1] = "5";
    argv[2] = NULL;

    pid_t pid;
    int i;

    for (i = 0; i < 10; i++) {
        pid = fork();

        if (pid == -1) {
            // Si ocurre un error al crear el proceso
            perror("fork");
            exit(EXIT_FAILURE);
        }

        if (pid == 0) {
            // Código del proceso hijo
            execvp(cmd, argv);
            perror("execvp");
            exit(EXIT_FAILURE);
        }
    }

    // Esperar a que todos los procesos hijos terminen
    for (i = 0; i < 10; i++) {
        wait(NULL);
    }

    // Una vez que todos los hijos hayan terminado
    printf("Listo\n");

    return 0;
}