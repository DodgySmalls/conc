#pragma once

#include <dispatch/dispatch.h>
#include "lightswitch.h"

//Use simple constant buffer sizes to remove unnecessary complexity
#define LEN_BUFFER 100

#define BUFFER_T_DEFAULT {.size = 0, .mu = PTHREAD_COND_INITIALIZER}
typedef struct {
	int data[LEN_BUFFER];
	uint8_t size;
	lightswitch_t readSwitch;
	dispatch_semaphore_t turnstile;
} buffer_t;

void buffer_init(buffer_t *);