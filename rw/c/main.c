#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> 
#include <pthread.h>
#include <dispatch/dispatch.h>
#include <time.h>
#include "reader.h"
#include "writer.h"
#include "buffer.h"

//constant values
#define NUM_READERS 5
#define NUM_WRITERS 5

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

	//Spawn threads
	pthread_t *readerTids = (pthread_t *) malloc(sizeof(pthread_t)*NUM_READERS);
	pthread_t *writerTids = (pthread_t *) malloc(sizeof(pthread_t)*NUM_WRITERS);

	for(int i = 0; i < NUM_READERS; i++) {
		args_reader_t *threadArgs = (args_reader_t *)malloc(sizeof(args_reader_t));
		threadArgs->buffer = sharedMemory;
		if(launchReader(readerTids + i, threadArgs)){
			exit(0);
		}
	}

	for(int i = 0; i < NUM_WRITERS; i++) {
		args_writer_t *threadArgs = (args_writer_t *)malloc(sizeof(args_writer_t));
		threadArgs->buffer = sharedMemory;
		if(launchWriter(writerTids + i, threadArgs)){
			exit(0);
		}
	}

	//Join
	for(int i = 0; i < NUM_READERS; i++) {
		pthread_join(readerTids[i], NULL);
	}
	for(int i = 0; i < NUM_WRITERS; i++) {
		pthread_join(writerTids[i], NULL);
	}

	//Conclude Timing
	gettimeofday(&endTime, NULL);
	printf("Total time = %f seconds\n", (double) (endTime.tv_usec - startTime.tv_usec) / 1000000 + (double) (endTime.tv_sec - startTime.tv_sec));
	fflush(stdout);

	//Cleanup
	free(readerTids);

	//Notify Success
	printf(MSG_DONE);
}