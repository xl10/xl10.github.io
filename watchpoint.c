#if !defined(_GNU_SOURCE)
#define _GNU_SOURCE
#endif

#include <asm/unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/hw_breakpoint.h>
#include <linux/perf_event.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <ucontext.h>
#include <unistd.h>

#define NUM_VALUES 4
struct recordValues {
	char names[NUM_VALUES];
	unsigned long addresses[NUM_VALUES];
	unsigned long values[NUM_VALUES];
};

struct recordValues wp;

long perf_event_open(struct perf_event_attr *hw_event, pid_t pid, int cpu, int group_fd, unsigned long flags) {
  return syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
}

pid_t gettid() {
  return syscall(__NR_gettid);
}

// The iterator variable
volatile int i = 0;
volatile int j = 0;
volatile int k = 0;
volatile int m = 0;
volatile int n = 0;
int last_i = -1;

void initialize() {
	wp.addresses[0]= (unsigned long)&i;
	wp.values[0]= i;
	wp.names[0]= 'i';
	wp.addresses[1]= (unsigned long)&j;
	wp.values[1]= j;
	wp.names[1]= 'j';
	wp.addresses[2]= (unsigned long)&k;
	wp.values[2]= k;
	wp.names[2]= 'k';
	wp.addresses[3]= (unsigned long)&m;
	wp.values[3]= m;
	wp.names[3]= 'm';
	//wp.addresses[4]= (unsigned long)&n;
	//wp.values[4]= n;
	//wp.names[4]= 'n';
}

void first_handler(int signum, siginfo_t* info, void* p) {
#if 0
  if(i % 3 == 0) {
    print_header();
    fprintf(stderr, "first ");
  }
#endif
	// Check which value has been changed.
	int in;

	for(in = 0; in < NUM_VALUES; in++) {
		if(wp.values[in] != *((unsigned long *)wp.addresses[in])) {
			wp.values[in] = *((unsigned long *)wp.addresses[in]);
			fprintf(stderr, " Now watchpoint %d: change %c value %d\n", in, wp.names[in], wp.values[in]);
		}
	}
  last_i = i;
}

int create_watchpoint(uintptr_t address, int sig, int group) {
  // Perf event settings
  struct perf_event_attr pe = {
    .type = PERF_TYPE_BREAKPOINT,
    .size = sizeof(struct perf_event_attr),
    .bp_type = HW_BREAKPOINT_W,
    .bp_len = HW_BREAKPOINT_LEN_4,
    .bp_addr = (uintptr_t)address,
    .disabled = 1,
    .sample_period = 1,
  };
 
  /*
  int perf_event_open(struct perf_event_attr *attr,
                           pid_t pid, int cpu, int group_fd,
                           unsigned long flags);
   */ 
  // Create the perf_event for this thread on all CPUs with no event group
  int perf_fd = perf_event_open(&pe, 0, -1, group, 0);
  if(perf_fd == -1) {
    fprintf(stderr, "Failed to open perf event file: %s\n", strerror(errno));
    abort();
  }
  
  // Set the perf_event file to async mode
  if(fcntl(perf_fd, F_SETFL, fcntl(perf_fd, F_GETFL, 0) | O_ASYNC) == -1) {
    fprintf(stderr, "Failed to set perf event file to ASYNC mode: %s\n", strerror(errno));
    abort();
  }
  
  // Tell the file to send a SIGUSR1 when an event occurs
  if(fcntl(perf_fd, F_SETSIG, sig) == -1) {
    fprintf(stderr, "Failed to set perf event file's async signal: %s\n", strerror(errno));
    abort();
  }
  
  // Deliver the signal to this thread
  if(fcntl(perf_fd, F_SETOWN, gettid()) == -1) {
    fprintf(stderr, "Failed to set the owner of the perf event file: %s\n", strerror(errno));
    abort();
  }
  
  return perf_fd;
}

// Enable a setof watch points now
void enable_watchpoints(int fd) {
  // Start the event
  if(ioctl(fd, PERF_EVENT_IOC_ENABLE, 0) == -1) {
    fprintf(stderr, "Failed to enable perf event: %s\n", strerror(errno));
    abort();
  }
}

void disable_watchpoint(int fd) {
  // Start the event
  if(ioctl(fd, PERF_EVENT_IOC_DISABLE, 0) == -1) {
    fprintf(stderr, "Failed to disable perf event: %s\n", strerror(errno));
    abort();
  }
}

size_t get_watchpoint_count(int fd) {
  uint64_t count;
  read(fd, &count, sizeof(uint64_t));
  return count;
}

int main(int argc, char** argv) {
	initialize();
	
  // Create watchpoints
  int first_watchpoint = create_watchpoint((uintptr_t)&i, SIGTRAP, -1);
  create_watchpoint((uintptr_t)&j, SIGTRAP, first_watchpoint);
  create_watchpoint((uintptr_t)&k, SIGTRAP, first_watchpoint);
  create_watchpoint((uintptr_t)&m, SIGTRAP, first_watchpoint);
  //create_watchpoint((uintptr_t)&n, SIGTRAP, first_watchpoint);
  //int buzz_watchpoint = create_watchpoint((uintptr_t)&i, SIGUSR2);
  
  // Set a signal handler for SIGUSR1
  struct sigaction sa1 = {
    .sa_sigaction = first_handler,
    .sa_flags = SA_SIGINFO
  };
  
  if(sigaction(SIGTRAP, &sa1, NULL) == -1) {
    fprintf(stderr, "Failed to set SIGTRAP handler: %s\n", strerror(errno));
    abort();
  }
 
  // Start watchpoints
  enable_watchpoints(first_watchpoint);
  
  // Shortest firstbuzz implementation ever:
  for(i=0; i<15; i++) 
	{
		j++;
		k++;
		m++;
		n++;
	}
  
  // Disable watchpoints
  disable_watchpoint(first_watchpoint);
  
  // Add a final newline
  fprintf(stderr, "\n");
  
  // Read out the count of events
  fprintf(stderr, "Watchpoints tripped %lu times\n", get_watchpoint_count(first_watchpoint));
  
  return 0;
}


