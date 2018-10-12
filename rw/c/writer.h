#pragma once

#include "buffer.h"

#define MICRO(sec) ((unsigned int)(sec * 1000000))

#define NUM_WRITER_CYCLES 100

#define MSG_WRITER_ERR_SPAWN_FAIL "err (%d) >> Failed to spawn writer"

/**
 * pthread argument struct
 * these arguments are always allocated to the heap,
 * the acquiring thread inherits the responsibility to free their arguments
 */
typedef struct{
	buffer_t *buffer;
} args_writer_t;

int launchWriter(pthread_t *, args_writer_t *);
void * writer(void *);