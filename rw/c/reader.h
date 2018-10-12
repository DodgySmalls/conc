#pragma once

#include "buffer.h"

#define MICRO(sec) ((unsigned int)(sec * 1000000))

#define NUM_READER_CYCLES 100

#define MSG_READER_ERR_SPAWN_FAIL "err (%d) >> Failed to spawn reader"

/**
 * pthread argument struct
 * these arguments are always allocated to the heap,
 * the acquiring thread inherits the responsibility to free their arguments
 */
typedef struct{
	buffer_t *buffer;
} args_reader_t;

int launchReader(pthread_t *, args_reader_t *);
void * reader(void *);