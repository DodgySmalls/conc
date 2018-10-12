#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> 
#include <pthread.h>
#include <dispatch/dispatch.h>
#include "writer.h"

int launchWriter(pthread_t *tid, args_writer_t *args) {
	int err;
	if((err = pthread_create(tid, 0, writer, args)) != 0){
		printf(MSG_WRITER_ERR_SPAWN_FAIL, err);
		fflush(stdout);
	}
	return err;
}

void * writer(void *pargs) {
	buffer_t *sharedMemory = ((args_writer_t *)pargs)->buffer;
	int percept[LEN_BUFFER];
	uint8_t size = 0;

	//sleep to simulate longer init period
	usleep(MICRO((rand() % 10) * 0.1));

	for(int cycle = 0; cycle < NUM_WRITER_CYCLES; cycle++) {
		dispatch_semaphore_wait(sharedMemory->turnstile, DISPATCH_TIME_FOREVER);

			dispatch_semaphore_wait(sharedMemory->readSwitch.sem, DISPATCH_TIME_FOREVER);
				
				printf("W:(%d) ENTER >\n", (int)pthread_self());
				fflush(stdout);

				if(rand() % 2 && sharedMemory->size < LEN_BUFFER) {
					sharedMemory->data[sharedMemory->size] = rand() % 10;
					sharedMemory->size++;
				}

				if(sharedMemory->size > 0) {
					sharedMemory->data[(rand() % sharedMemory->size)] = rand() % 10;
				}

				//slow memcpy
				for(int i = 0; i < sharedMemory->size; i++) {
					percept[i] = sharedMemory->data[i];
					size = sharedMemory->size;
				}

				//pretend operation is heavier
				usleep(MICRO((rand() % 5) * 0.01));

				printf("W:(%d) EXIT <\n", (int)pthread_self());
				fflush(stdout);
			
			//we signal this semaphore after releasing the turnstile

		dispatch_semaphore_signal(sharedMemory->turnstile);

		dispatch_semaphore_signal(sharedMemory->readSwitch.sem);

		//pretend operation is heavier
		usleep(MICRO((rand() % 50) * 0.001));
	}

	free(pargs);

	return NULL;
}