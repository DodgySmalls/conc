#!/usr/local/bin/python

import random
import time
from threading import Thread
from threading import Semaphore
from langarmutex import LangarMutex

class SharedData:
	def __init__(self):
		self.lmutex = LangarMutex()

def operation(id, d):
	
	d.lmutex.enter()
	
	print "(" + str(id) + ") ENTER"
	time.sleep(random.uniform(0.01, 0.5))
	print "(" + str(id) + ") EXIT"

	d.lmutex.leave()


def main():
	s = SharedData()
	threads = []
	for i in range(50):
		threads.append(Thread(target=operation, args=(i,s,)))
		threads[i].daemon = True
		threads[i].start()
		time.sleep(random.uniform(0.001, 0.3))

	#unfortunate minor polling required to allow keyboard interrupts
	while threads:	
		threads[0].join(1000)
		if(not threads[0].isAlive()):
			del(threads[0])

	print "finished"

if __name__ == "__main__":
	main()