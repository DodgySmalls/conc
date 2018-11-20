#!/usr/local/bin/python

class Message:
	def __init__(self, order, trail):
		self.order = order
		self.trail = trail

	def copy(self):
		trail = [t for t in self.trail]
		return Message(self.order, trail)

	def __str__(self):
		return "Message:<" + str(self.order) + "," + str(self.trail) + ">"

class General:
	m = 2
	G = []
	Num = 7

	def __init__(self, index, loyal):
		self.index = index
		self.loyal = loyal
		self.messages = []
		self.result = "?"
		self.inferenceroot = Inference(None, None)

	def forwardMessage(self, message, receiver):
		#print "forwardMessage " + str(self.index) + " --> " + str(receiver) + " " + str(message)

		#spec specifies that traitorous _lieutenants_ send false messages to even indexed peers 
		if(not self.loyal and receiver%2 == 0 and self.index != 0):
			m = message.copy()
			m.order = not m.order
			m.trail.append(self.index)
			General.G[receiver].receiveMessage(m)
		else:
			m = message.copy()
			m.trail.append(self.index)
			General.G[receiver].receiveMessage(m)


	def receiveMessage(self, message):
		self.messages.append(message)
		if(len(message.trail) >= General.m + 1):
			#don't respond
			#print("message was long enough " + str(message))
			x = 1
		else:
			for g in General.G:
				#transmit this message to everyone else not yet on the path with myself appended to path
				if(g.index not in message.trail and g.index != self.index):
					self.forwardMessage(message, g.index)
		self.infer(message)

	def infer(self, message):
		current = self.inferenceroot
		for l in message.trail:
			if(not current.children.has_key(l)):
				current.children[l] = Inference(current, None)
			current = current.children[l]

		current.value = message.order
		current.resolve()



	def __str__(self):
		string = "General:" + str(self.index)
		if(self.loyal):
			string += " is loyal\n"
		else:
			string += " is traitor\n"
		for message in self.messages:
			string += "    " + str(message) + "\n"
		return string


class Inference:
	def __init__(self, parent, value):
		self.value = value
		self.parent = parent
		self.children = {}
		self.depth = 0
		self.resolved = False

		p = self.parent
		while p != None:
			p = p.parent
			self.depth += 1

	def resolve(self):
		if(self.depth == General.m + 1):
			self.resolved = True
			self.parent.resolve()
		else:
			if(len(self.children) == General.Num - self.depth - 1):
				for childIndex in self.children:
					child = self.children[childIndex]
					if(not child.resolved):
						return

				self.value = Inference.majority(self.children, [self.value])
				self.resolved = True
				self.parent.resolve()

	@classmethod
	def majority(cls, inferences, extra):
		positivecount = 0
		negativecount = 0
		for inferencekey in inferences:
			i = inferences[inferencekey]
			if(i.value):
				positivecount += 1
			else:
				negativecount += 1
		for i in extra:
			if(i):
				positivecount += 1
			else:
				negativecount += 1

		if(positivecount > negativecount):
			return True
		else:
			return False


if __name__ == "__main__":
	#Example of manual run with verbose state output

	for x in range(General.Num):
		General.G.append(General(x, True))

	General.G[3].loyal = False
	General.G[4].loyal = False

	for g in General.G:
		if(g.index != 0):
			General.G[0].forwardMessage(Message(False, []), g.index)

	for g in General.G:
		if(g.index != 0):
			print g
			if(g.inferenceroot.children[0].resolved):
				print g.inferenceroot.children[0].value
			print "\n-------\n"