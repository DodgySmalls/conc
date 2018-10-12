#include "buffer.h"

void buffer_init(buffer_t *b) {
	b->size = 0;
	b->mutex = dispatch_semaphore_create(1);
}