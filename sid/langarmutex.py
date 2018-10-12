from threading import Semaphore

'''
	An OOP interpretation of a no-starve-mutex. 	
	A LangarMutex allows for a resource to be mutually exclusive without
	ever allowing a thread to starve, though it is batch FIFO not thread FIFO,
	meaning the order of control within a batch is not guaranteeself.

	A Langar is a Sikh kitchen within a Gurdwara (temple)
	where all may come to share in a vegetarian meal, hence they cannot starve.

	However, as a mutually-exclusive Langar (a programming interpretation)
	the hypothetical Langar has only one plate with which to serve food,
	meaning only one person (thread) may eat (execute) at a time.
'''
class LangarMutex:
	def __init__(self, **kwargs):
		self.lobby = 0					#the waiting room
		self.messhall = 0				#the room filled with hungry threads
		self.messdoor = Semaphore(1)	#the door into the mess-hall
		self.plate = Semaphore(0)		#only the one holding the plate may eat
		self.mutex = Semaphore(1)		#used for atomic access to counters
		if('warmup' in kwargs):
			self.warmup = kwargs['warmup']
		else:
			self.warmup = 0.0

	''' 
		LangarMutex.enter()
			Blocking function
			When control is returned the executing thread 
			is guaranteed mutual exclusion.

			It is the responsibility of the calling thread 
			to release the LangarMutex with the (inverse) leave() call.
	'''
	def enter(self):
		if(self.warmup >= 0.001):							#it may be cold outside the Langar
			time.sleep(random.uniform(0.001, self.warmup))	#hence entering may require some time to warm up 

		#any thread may freely enter the lobby at any time,
		#they must post their arrival safely to the lobby counter
		self.mutex.acquire()
		self.lobby += 1
		self.mutex.release()

		#a thread must wait until their batch is allowed into the mess to proceed
		self.messdoor.acquire()
		self.messhall += 1

		self.mutex.acquire()
		self.lobby -= 1

		#when the last thread from the lobby enters the messhall, the plate is made available
		#otherwise the door is opened so that more threads from the lobby may enter
		if self.lobby == 0:
			self.mutex.release()
			self.plate.release()
		else:
			self.mutex.release()
			self.messdoor.release()

		#each thread in the mess-hall eventually acquires the plate (enters the critical section)
		self.plate.acquire()
		self.messhall -= 1	#piggyback the knowledge that this line is in the critical section to avoid an extra mutex use

	'''
		LangarMutex.leave()
			Non-blocking function
			Releases mutual exclusion

			It is the responsibility of the calling thread
			to only call leave() from within a critical section of an (inverse) enter() call
	'''
	def leave(self):
		#if there are more threads in the messhall, the plate is made available
		#when the last thread leaves the messhall, the door from lobby to mess-hall is opened
		if self.messhall == 0:
			self.messdoor.release()
		else:
			self.plate.release()


