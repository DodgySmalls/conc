from threading import Semaphore
from threading import Lock

class MultiplexType:
	EXCLUSIVE = 1
	SHARED = 2

class CooperativeMutex:
	def __init__(self):
		self.mutex = Lock()
		self.access = Lock()
		self.sharedusers = {}

	def lock(self, caller, cmtype=MultiplexType.EXCLUSIVE):
		if(cmtype == MultiplexType.SHARED):
			self.mutex.acquire()

			self.sharedusers[caller] = cmtype
			if(len(self.sharedusers) == 1):
				self.access.acquire()

			self.mutex.release()
		else:
			self.access.acquire()

	def unlock(self, caller):
		self.mutex.acquire()

		cmtype = self.sharedusers.get(caller, MultiplexType.EXCLUSIVE)

		if(cmtype == MultiplexType.SHARED):
			del(self.sharedusers[caller])
			if(len(self.sharedusers) == 0):
				self.access.release()
		else:
			self.access.release()

		self.mutex.release()