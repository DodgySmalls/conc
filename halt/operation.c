#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> 
#include <pthread.h>
#include <dispatch/dispatch.h>
#include "operation.h"

int launchOperation(pthread_t *tid, args_operation_t *args) {
	int err;
	if((err = pthread_create(tid, 0, operation, args)) != 0){
		printf(MSG_OPERATION_ERR_SPAWN_FAIL, err);
		fflush(stdout);
	}
	return err;
}

void * operation(void *pargs) {
	
	//enable thread to be cancelled
	int cancelType;
	pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, &cancelType);
	args_operation_t *oargs = (args_operation_t *)pargs;
	buffer_t *sharedMemory = ((args_operation_t *)pargs)->buffer;

	for(int cycle = 0; cycle < NUM_OPERATION_CYCLES; cycle++) {
		
		printf(" | Operation(%d) functioning\n", (int)pthread_self());
		fflush(stdout);

		dispatch_semaphore_wait(oargs->unsafe, DISPATCH_TIME_FOREVER);

			printf(" > Operation(%d) entering section where it is not safe to halt \n", (int)pthread_self());
			
			//take some resource

			//do some operation
			dispatch_semaphore_wait(sharedMemory->mutex, DISPATCH_TIME_FOREVER);
			usleep(MICRO(1));
			dispatch_semaphore_signal(sharedMemory->mutex);

			//release some resource

			printf(" < Operation(%d) leaving  section where it is not safe to halt \n", (int)pthread_self());
			
		dispatch_semaphore_signal(oargs->unsafe);
	}

	free(pargs);

	return NULL;
}