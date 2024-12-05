#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/*  
    Utilizar fork, open, close y dup para crear dos procesos y redireccionar
    la salida estándar de cada uno a un archivo lala.txt, donde cada uno imprima
    un mensaje conteniendo su PID.

    Pensar en qué orden realizar las llamadas, y asegurarse de cerrar todos los 
    file descriptors abiertos.
*/

int main(void) {
    char *filename = "lala.txt";

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

    // Forkeamos e imprimimos en el archivo
    int fork_result = fork();
    int pid = getpid();
    if (fork_result == -1) {
        printf("fork failed\n");
    } else if (fork_result == 0) {
        printf("I'm the child with pid = %d\n", pid);
    } else {
        printf(
            "I'm the parent with pid = %d and my child's pid is = %d\n",
            pid,
            fork_result
        );
    }

    return 0;
}