from threading import Semaphore

class Lightswitch:
	def __init__(self):
		self.counter = 0
		self.mutex = Semaphore(1)
		self.sem = Semaphore(1)


	def enter(self):
		self.mutex.acquire()

		self.counter += 1
		if(self.counter == 1):
			self.sem.acquire()

		self.mutex.release()


	def leave(self):
		self.mutex.acquire()

		self.counter -= 1
		if(self.counter == 0):
			self.sem.release()

		self.mutex.release()