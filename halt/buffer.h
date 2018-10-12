#pragma once

#include <dispatch/dispatch.h>

//Use simple constant buffer sizes to remove unnecessary complexity
#define LEN_BUFFER 100

typedef struct {
	int data[LEN_BUFFER];
	uint8_t size;
	dispatch_semaphore_t mutex;
} buffer_t;

void buffer_init(buffer_t *);