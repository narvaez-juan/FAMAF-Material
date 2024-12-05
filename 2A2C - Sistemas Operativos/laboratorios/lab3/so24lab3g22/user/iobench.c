#include "../kernel/types.h"
#include "../kernel/stat.h"
#include "user.h"
#include "../kernel/fs.h"
#include "../kernel/fcntl.h"
#include "../kernel/syscall.h"
#include "../kernel/param.h"
#include "../kernel/memlayout.h"
#include "../kernel/riscv.h"

#define IO_OPSIZE 64
#define IO_EXPERIMENT_LEN 512

static char data[IO_OPSIZE];


int
io_ops()
{
    int rfd, wfd;

    int pid = getpid();

    // Crear un path unico de archivo
    char path[] = "12iops";
    path[0] = '0' + (pid / 10);
    path[1] = '0' + (pid % 10);

    wfd = open(path, O_CREATE | O_WRONLY);

    for(int i = 0; i < IO_EXPERIMENT_LEN; ++i){
      write(wfd, data, IO_OPSIZE);
    }

    close(wfd);

    rfd = open(path, O_RDONLY);

    for(int i = 0; i < IO_EXPERIMENT_LEN; ++i){
      read(rfd, data, IO_OPSIZE);
    }

    close(rfd);
    return 2 * IO_EXPERIMENT_LEN;
}

void
iobench(int N, int pid)
{
  memset(data, 'a', sizeof(data));
  uint64 start_tick, end_tick, elapsed_ticks, metric_total_iops = 0, iops_per_tick;
  uint64 first_tick, tick_start_per_cycle;
  int total_iops;

  int *measurements = malloc(sizeof(int) * N);

	first_tick = uptime();
  for (int i = 0; i < N; i++){
    start_tick = uptime();

    // Realizar escrituras y lecturas de archivos
    total_iops = io_ops();

    end_tick = uptime();
    elapsed_ticks = end_tick - start_tick;
    metric_total_iops = total_iops;  // Cambiar esto por la métrica adecuada
    iops_per_tick = total_iops / elapsed_ticks;
    measurements[i] = iops_per_tick;
    tick_start_per_cycle = start_tick - first_tick;
    printf("PID\t%d\t[iobench]\tcycle\t%d\tiops_per_tick\t%d\telapsed_ticks\t%d\t"
						"start_tick\t%d\n",pid, i, iops_per_tick, elapsed_ticks, tick_start_per_cycle);
  }
  int average = 0;
  for (int i = 0; i < N; i++)
  {
    average = average + measurements[i];
  }
  average = average / N;
  printf("PID\t%d\tAverage iops_per_tick:\t%d\tTotal_iops:\t%d\tio_exp_length\t%d\n", 
  			pid, average, metric_total_iops, IO_EXPERIMENT_LEN);
}

int
main(int argc, char *argv[])
{
  int N, pid;
  if (argc != 2) {
    printf("Uso: benchmark N\n");
    exit(1);
  }

  N = atoi(argv[1]);  // Número de repeticiones para los benchmarks
  pid = getpid();
  iobench(N, pid);

  exit(0);
}
