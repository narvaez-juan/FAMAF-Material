#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/* 	
	Pensar en cómo utilizar las llamadas a sistema open, dup y close para poder
	redireccionar la salida estándar del proceso actual 
*/

int main(void) {
	char *filename = "lala.txt";

	// Abrir archivo con permisos de lectura/escritura, creandolo si no existe
   	int fd = open(filename, O_CREAT | O_RDWR | O_TRUNC, S_IRWXU);
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

	// Esto se imprimira en el archivo, en lugar de STDOUT_FILENO
	printf("Esta salida será redirigida al archivo lala.txt\n");

	return 0;
}
