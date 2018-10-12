#include "lightswitch.h"

void lightswitch_init(lightswitch_t *ls) {
	ls->counter = 0;
	ls->mutex = dispatch_semaphore_create(1);
	ls->sem = dispatch_semaphore_create(1);
}

void lightswitch_enter(lightswitch_t *ls) {
	dispatch_semaphore_wait(ls->mutex, DISPATCH_TIME_FOREVER);
		ls->counter = ls->counter + 1;
		if(ls->counter == 1) {
			dispatch_semaphore_wait(ls->sem, DISPATCH_TIME_FOREVER);
		}
	dispatch_semaphore_signal(ls->mutex);
}

void lightswitch_leave(lightswitch_t *ls) {
	dispatch_semaphore_wait(ls->mutex, DISPATCH_TIME_FOREVER);
		ls->counter = ls->counter - 1;
		if(ls->counter == 0) {
			dispatch_semaphore_signal(ls->sem);
		}
	dispatch_semaphore_signal(ls->mutex);
}