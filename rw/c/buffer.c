#include "buffer.h"

void buffer_init(buffer_t *b) {
	b->size = 0;
	b->turnstile = dispatch_semaphore_create(1);
	lightswitch_init(&(b->readSwitch));
}