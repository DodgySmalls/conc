from threading import Semaphore
from langarmutex import LangarMutex

class LangarLightswitch:
	def __init__(self):
		self.counter = 0
		self.mutex = Semaphore(1)
		self.langarmutex = LangarMutex()


	def enter(self):
		self.mutex.acquire()

		self.counter += 1
		if(self.counter == 1):
			self.langarmutex.enter()

		self.mutex.release()


	def leave(self):
		self.mutex.acquire()

		self.counter -= 1
		if(self.counter == 0):
			self.langarmutex.leave()

		self.mutex.release()