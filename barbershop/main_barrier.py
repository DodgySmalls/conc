#!/usr/local/bin/python

import random
import time
from threading import Thread
from threading import Semaphore
from threading import Barrier
from threading import Lock

class SharedData:
	def __init__(self):
		self.n = 4
		self.customers = 0
		self.mutex = Lock()
		self.barberAttention = Lock()
		self.haircutStart = Barrier(2, timeout=None)
		self.haircutFinished = Barrier(2, timeout=None)

def customer(id, d):
	d.mutex.acquire()
	if d.customers == d.n:
		d.mutex.release()
		print("(" + str(id) + ") balked") #LBS: balk()
		return
	d.customers += 1
	d.mutex.release()

	print("(" + str(id) + ") is waiting for the barber")

	d.barberAttention.acquire()
	d.haircutStart.wait()
	d.barberAttention.release()


	#LBS: getHairCut()
	print("(" + str(id) + ")        ENTERED critical section")
	time.sleep(random.uniform(0.2, 1))
	print("(" + str(id) + ")        is exiting critical section")

	d.haircutFinished.wait()
	

	d.mutex.acquire()
	d.customers -= 1
	d.mutex.release()

	time.sleep(random.uniform(0.1, 0.2))
	
def barber(id, d):
	while(True):
		d.haircutStart.wait()

		#LBS: cutHair()
		print("(" + str(id) + ")-BARBER ENTERED critical section")
		time.sleep(random.uniform(0.2, 1))
		print("(" + str(id) + ")-BARBER is exiting critical section")

		d.haircutFinished.wait()


def main():
	s = SharedData()

	threads = []
	barberThread = Thread(target=barber, args=(99,s,))
	barberThread.daemon = True
	barberThread.start()

	for i in range(50):
		threads.append(Thread(target=customer, args=(i,s,)))
		threads[i].daemon = True
		threads[i].start()
		time.sleep(random.uniform(0.01, 0.3))


	#unfortunate minor polling required to allow keyboard interrupts
	while threads:	
		threads[0].join(1000)
		if(not threads[0].isAlive()):
			del(threads[0])

	print("finished")

if __name__ == "__main__":
	main()