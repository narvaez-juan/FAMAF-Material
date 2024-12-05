#include "types.h"
#include "riscv.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "spinlock.h"
#include "proc.h"

uint64
sys_exit(void)
{
  int n;
  argint(0, &n);
  exit(n);
  return 0;  // not reached
}

uint64
sys_getpid(void)
{
  return myproc()->pid;
}

uint64
sys_fork(void)
{
  return fork();
}

uint64
sys_wait(void)
{
  uint64 p;
  argaddr(0, &p);
  return wait(p);
}

uint64
sys_sbrk(void)
{
  uint64 addr;
  int n;

  argint(0, &n);
  addr = myproc()->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

uint64
sys_sleep(void)
{
  int n;
  uint ticks0;

  argint(0, &n);
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(killed(myproc())){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

uint64
sys_kill(void)
{
  int pid;

  argint(0, &pid);
  return kill(pid);
}

// return how many clock tick interrupts have occurred
// since start.
uint64
sys_uptime(void)
{
  uint xticks;

  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}

//--------------------------------------------SEMAPHORE------------------------------------------------------------------//

typedef enum {CLOSE, OPEN} state_t;

struct sem {
  int value;
  state_t status;    
  struct spinlock lock;
};


struct sem semaphores[MAX_SEM]; 

//función para inicializar todos los semáforos del arreglo
int sem_init(void){
  for (unsigned int i = 0; i < MAX_SEM; i++){
    //inicializar el lock
	  initlock(&semaphores[i].lock, "sem");
    //inicializar semáforo
    semaphores[i].value = 0;
    semaphores[i].status = CLOSE;
  }
   return 0;
}


//int sem_open(int sem, int value) → Abre y/o inicializa el semáforo “sem” con un valor arbitrario “value”.
uint64 
sys_sem_open(void)
{
	int sem;
  int value;

  //captar argumentos
	argint(0, &sem);
	argint(1, &value);
	
	if (sem < 0 || sem >= MAX_SEM || semaphores[sem].value < 0 || semaphores[sem].status == OPEN){
    return 0;
  }
	
  //adquiero el lock
  acquire(&semaphores[sem].lock);

  //inicializar el semáforo
	semaphores[sem].value = value;
  semaphores[sem].status = OPEN;

  //liberar lock
  release(&semaphores[sem].lock);

	 return 1;
}

//int sem_close(int sem) →Libera el semáforo “sem”
uint64 
sys_sem_close(void){
  int sem;

  //captar argumentos
  argint(0,&sem);


  // si estoy por fuera de los índices
  if (sem < 0 || sem >= MAX_SEM){
    release(&semaphores[sem].lock);
    return 0;
  }

  //adquirir el lock para mutual exclusion
  acquire(&semaphores[sem].lock);



  //cerrar semáforo
  semaphores[sem].status = CLOSE;

  //liberar lock
  release(&semaphores[sem].lock);

  return 1;

}

//int sem_up(int sem) →Incrementa el semáforo ”sem” desbloqueando los procesos cuando su valor es 0.
uint64 
sys_sem_up (void){

  //capto argumentos
  int sem;
  argint(0,&sem);


  //adquirir el lock para mutual exclusion
  acquire(&semaphores[sem].lock);
 
  
  if (semaphores[sem].value == 0){
    wakeup(&semaphores[sem]); 
  }

  semaphores[sem].value++; 

  release(&semaphores[sem].lock); 
 

  return 1;


}

//int sem_down(int sem) →Decrementa el semáforo ”sem” bloqueando los procesos cuando su valor es 0. El valor del semaforo nunca puede ser menor a 0
uint64 
sys_sem_down(void)
{
  //capto argumentos 
	int sem;
  argint(0, &sem); 


  //adquirir el lock para mutual exclusion
  acquire(&semaphores[sem].lock);

   
  while(semaphores[sem].value == 0){    
   sleep(&semaphores[sem], &semaphores[sem].lock);                         
  }   
                                                                     
  semaphores[sem].value--;                                    
                                        
  release(&semaphores[sem].lock); 
  

  return 1;

}
