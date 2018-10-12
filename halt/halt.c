#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> 
#include <pthread.h>
#include <dispatch/dispatch.h>
#include <time.h>
#include "operation.h"
#include "buffer.h"

//const console messages
#define MSG_DONE "COMPLETE\n\n"

int main(int argc, char *argv[]) {

	//Initialize RNG, we aren't looking for determinism here so time(NULL)
	srand(time(NULL));

	//Initialize Timing
	struct timeval startTime, endTime;
	gettimeofday(&startTime, NULL);

	//Allocate buffer
	buffer_t *sharedMemory = (buffer_t *) malloc(sizeof(buffer_t));
	buffer_init(sharedMemory);

	//Spawn thread
	pthread_t *opTid = (pthread_t *) malloc(sizeof(pthread_t));

	args_operation_t *threadArgs = (args_operation_t *)malloc(sizeof(args_operation_t));
	threadArgs->buffer = sharedMemory;
	threadArgs->unsafe = dispatch_semaphore_create(1);
	
	if(launchOperation(opTid, threadArgs)){
		exit(0);
	}

	//Wait some time before deciding we want to cancel that operation
	usleep(MICRO(5.5));

	dispatch_semaphore_wait(threadArgs->unsafe, DISPATCH_TIME_FOREVER);

		printf("Cancelling operation thread...\n");fflush(stdout);

		pthread_cancel(*opTid);

		printf("Cancelled operation thread\n");fflush(stdout);

	//Unfortunately, pthread_cancel is "friendly" and won't stop our thread while it's blocked
	//We could be more aggressive and use pthread_kill(*opTid, SIG_)
	dispatch_semaphore_signal(threadArgs->unsafe);

	//Join
	pthread_join(*opTid, NULL);
	
	printf("Sleeping main for 5 seconds to demonstrate operation has halted.\n");fflush(stdout);
	printf("Notice however that the operation did continue into the critical section\n");fflush(stdout);
	usleep(MICRO(5.0));

	//Conclude Timing
	gettimeofday(&endTime, NULL);
	printf("Total time = %f seconds\n", (double) (endTime.tv_usec - startTime.tv_usec) / 1000000 + (double) (endTime.tv_sec - startTime.tv_sec));
	fflush(stdout);

	//Cleanup
	free(opTid);
	free(threadArgs);
	free(sharedMemory);

	//Notify Success
	printf(MSG_DONE);
}