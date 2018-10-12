#!/usr/local/bin/python

import random
import time
from threading import Thread
from threading import Lock
from cooperativemutex import *

class SharedData:
	def __init__(self):
		self.turnstile = Lock()
		self.cmutex = CooperativeMutex()


def writer(id, d):
	d.turnstile.acquire()
	d.cmutex.lock(id, MultiplexType.EXCLUSIVE)

	print("W:(" + str(id) + ") ENTER >")
	time.sleep(random.uniform(0.01, 0.05))
	print("W:(" + str(id) + ") EXIT <")

	d.turnstile.release()
	d.cmutex.unlock(id)


def reader(id, d):
	d.turnstile.acquire()
	d.turnstile.release()

	d.cmutex.lock(id, MultiplexType.SHARED)
	print("R:(" + str(id) + ") ENTER >")
	time.sleep(random.uniform(0.01, 0.05))
	print("R:(" + str(id) + ") EXIT <")
	d.cmutex.unlock(id)



def main():
	s = SharedData()
	threads = []
	for i in range(1000):
		rtt = random.uniform(0.0, 2.0)

		if(rtt <= 1.0):		
			threads.append(Thread(target=reader, args=(i,s,)))
		else:
			threads.append(Thread(target=writer, args=(i,s,)))

		threads[i].daemon = True
		threads[i].start()
		time.sleep(random.uniform(0.001, 0.1))

	#unfortunate minor polling required to allow keyboard interrupts
	while threads:	
		threads[0].join(1000)
		if(not threads[0].isAlive()):
			del(threads[0])


if __name__ == "__main__":
	main()