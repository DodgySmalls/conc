#!/usr/local/bin/python

import random
import time
from threading import Thread
from threading import Semaphore

class SharedData:
	def __init__(self):
		self.mutex = Semaphore(1)
		self.items = Semaphore(0)
		self.buffer = []

def producer(id, d):
	for i in range(10000):
		d.mutex.acquire()
		d.buffer.append(True)
		d.mutex.release()
		d.items.release()

def consumer(id, d):
	for i in range(10000):
		d.items.acquire()
		d.mutex.acquire()

		# importantly we can't use the items semaphore to select the last element
		# in many list implementations, since it might be inconsistent at this point
		# (another consumer might've waited on items before we got the mutex)
		# so we must check the list's length inside the critical section
		# in this case, we implicitly check the list length by accessing the last element
		val = d.buffer[-1]
		del(d.buffer[-1])

		d.mutex.release()

		#opportunity for parallel operation now that we've consumed the item

def main():

	print("BEGIN")

	s = SharedData()
	threads = []
	for i in range(50):
		threads.append(Thread(target=producer, args=(i,s,)))
		threads[i].daemon = True
		threads[i].start()
		#time.sleep(random.uniform(0.01, 0.3))

	for i in range(50):
		threads.append(Thread(target=consumer, args=(50 + i,s,)))
		threads[50+i].daemon = True
		threads[50+i].start()
		#time.sleep(random.uniform(0.01, 0.3))

	#unfortunate minor polling required to allow keyboard interrupts
	while threads:	
		threads[0].join(1000)
		if(not threads[0].isAlive()):
			del(threads[0])

	print("FINISHED")

if __name__ == "__main__":
	main()