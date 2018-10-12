#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> 
#include <pthread.h>
#include <dispatch/dispatch.h>
#include "reader.h"

int launchReader(pthread_t *tid, args_reader_t *args) {
	int err;
	if((err = pthread_create(tid, 0, reader, args)) != 0){
		printf(MSG_READER_ERR_SPAWN_FAIL, err);
		fflush(stdout);
	}
	return err;
}

void * reader(void *pargs) {
	buffer_t *sharedMemory = ((args_reader_t *)pargs)->buffer;
	int percept[LEN_BUFFER];
	uint8_t size = 0;

	//sleep to simulate longer init period
	usleep(MICRO((rand() % 10) * 0.1));

	for(int cycle = 0; cycle < NUM_READER_CYCLES; cycle++) {
		dispatch_semaphore_wait(sharedMemory->turnstile, DISPATCH_TIME_FOREVER);
		dispatch_semaphore_signal(sharedMemory->turnstile);

		lightswitch_enter(&sharedMemory->readSwitch);

			printf("R:(%d) ENTER >\n", (int)pthread_self());
			fflush(stdout);

			//slow memcpy
			for(int i = 0; i < sharedMemory->size; i++) {
				percept[i] = sharedMemory->data[i];
				size = sharedMemory->size;
			}

			//pretend operation is heavier
			usleep(MICRO((rand() % 5) * 0.01));

			printf("R:(%d) EXIT <\n", (int)pthread_self());
			fflush(stdout);

		lightswitch_leave(&sharedMemory->readSwitch);

		//sleep until a new operation should occur
		usleep(MICRO((rand() % 10) * 0.001));
	}

	free(pargs);

	return NULL;
}