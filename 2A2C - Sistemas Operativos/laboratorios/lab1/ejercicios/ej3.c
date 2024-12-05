#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/*  
    Implementar un programa que ejecute el comando cat /proc/cpuinfo 
    y redirija la salida estándar al archivo cpuinfo.txt
*/

int main(void) {
    char *filename = "cpuinfo.txt";
    char *cmd = "cat";
    char *argv[3];

    // Abrir archivo con permisos de lectura/escritura, creandolo si no existe
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, S_IRWXU);
    if (fd < 0) {
        perror("open");
        exit(1);
    }

    // Duplicar fd para que stdout (fd 1) apunte al archivo
    if (dup2(fd, STDOUT_FILENO) < 0) {
        perror("dup2");
        close(fd);
        exit(1);
    }

    // Cerramos el fd original
    close(fd);

    // Guardamos los argumentos en argv
    argv[0] = cmd;
    argv[1] = "/proc/cpuinfo";
    argv[2] = NULL;
    
    // Ejecutamos
    execvp(cmd, argv);

    return 1;
}