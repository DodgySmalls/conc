#!/usr/local/bin/python

import random
import time
from threading import Thread
from threading import Semaphore
from langarlightswitch import LangarLightswitch
from langarmutex import LangarMutex

class SharedData:
	def __init__(self):
		self.insertMutex = LangarMutex()
		self.searchSwitch = LangarLightswitch() #self.noSearcher = Semaphore(1)
		self.insertSwitch = LangarLightswitch() #self.noInserter = Semaphore(1)


def inserter(id, d):
	d.insertSwitch.enter()
	d.insertMutex.enter()

	print "I:(" + str(id) + ") entered critical section"
	time.sleep(random.uniform(0.1, 0.5))
	print "I:(" + str(id) + ") is exiting critical section"

	d.insertMutex.leave()
	d.insertSwitch.leave()


def searcher(id, d):
	d.searchSwitch.enter()

	print "S:(" + str(id) + ") entered critical section"
	time.sleep(random.uniform(0.1, 0.5))
	print "S:(" + str(id) + ") is exiting critical section"

	d.searchSwitch.leave()


def deleter(id, d):
	d.searchSwitch.langarmutex.enter()
	d.insertSwitch.langarmutex.enter()

	print "D:(" + str(id) + ") entered critical section"
	time.sleep(random.uniform(0.1, 0.5))
	print "D:(" + str(id) + ") is exiting critical section"

	d.insertSwitch.langarmutex.leave()
	d.searchSwitch.langarmutex.leave()


def main():
	s = SharedData()
	threads = []
	for i in range(100):
		rtt = random.uniform(0.0, 3.0)

		if(rtt <= 1.0):		
			threads.append(Thread(target=inserter, args=(i,s,)))
		elif(rtt > 1.0 and rtt <= 2.0):
			threads.append(Thread(target=searcher, args=(i,s,)))
		else:
			threads.append(Thread(target=deleter, args=(i,s,)))

		threads[i].daemon = True
		threads[i].start()
		time.sleep(random.uniform(0.001, 0.3))

	#unfortunate minor polling required to allow keyboard interrupts
	while threads:	
		threads[0].join(1000)
		if(not threads[0].isAlive()):
			del(threads[0])


if __name__ == "__main__":
	main()