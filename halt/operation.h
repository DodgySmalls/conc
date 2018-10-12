#pragma once

#include "buffer.h"

#define MICRO(sec) ((unsigned int)(sec * 1000000))

#define NUM_OPERATION_CYCLES 500

#define MSG_OPERATION_ERR_SPAWN_FAIL "err (%d) >> Failed to spawn operation"

/**
 * pthread argument struct
 * these arguments are always allocated to the heap,
 * the acquiring thread inherits the responsibility to free their arguments
 */
typedef struct{
	buffer_t *buffer;
	dispatch_semaphore_t unsafe;
} args_operation_t;

int launchOperation(pthread_t *, args_operation_t *);
void * operation(void *);