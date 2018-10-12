#pragma once

#include <dispatch/dispatch.h>

typedef struct {
	uint counter;
	dispatch_semaphore_t mutex;
	dispatch_semaphore_t sem;
} lightswitch_t;

void lightswitch_init(lightswitch_t *);
void lightswitch_enter(lightswitch_t *);
void lightswitch_leave(lightswitch_t *);