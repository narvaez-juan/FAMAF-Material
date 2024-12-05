#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/param.h"
#include <stddef.h>


int main(int argc, char *argv[]) {

  int rally = atoi(argv[1]);

    // Validación de argumentos
    if(argc != 2){
        printf("ERROR\n");
        exit(0);
    }

    if(rally < 1){
        printf("ERROR\n");
        exit(0); 
    }

    int sem_parent = 0;
    int sem_child = 1;
    
    // Inicialización de semáforos
    while (sem_open(sem_parent, 1) == 0){
        sem_parent++;  //si devuelve 0, es un semáforo que ya está en uso, entonces avanza a uno disponible
    }

    while (sem_open(sem_child, 0) == 0){
        sem_child++;
    }

    int pid = fork();

    if (pid < 0){
        printf("Failed to fork\n");
        exit(0);
    } else if (pid == 0){ // Proceso hijo
        for (int i = 0; i < rally ; i++) {
            sem_down(sem_parent);
            printf("ping\n");
            sem_up(sem_child);
        }
    } else { // Proceso padre
        for (int i = 0; i < rally ; i++) {
            sem_down(sem_child);
            printf("\tpong\n");
            sem_up(sem_parent);
        }
        wait(NULL); // Espera a que el hijo termine
    }

    sem_close(sem_parent);
    sem_close(sem_child);

    exit(0);
  
}