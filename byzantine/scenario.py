#!/usr/local/bin/python

from byzantine import *

class Scenario:
	def __init__(self, m, n, nT, o):
		if(m >= nT and n >= (3 * nT) + 1):
			self.expectation = o
		self.order = o

		General.m = m
		General.G = []
		General.Num = n
		
		root = SimpleNode(None, None)
		Scenario.generateFullBinaryTree(root, n)
		paths = []
		Scenario.allPaths(root, paths)

		self.generalLists = []
		for p in paths:
			g = Scenario.pathToGeneralList(p)
			if(Scenario.countTraitors(g) == nT):
				self.generalLists.append(g)

		self.run()

	def run(self):
		print "Running " + str(len(self.generalLists)) + " scenarios"
		for l in self.generalLists:
			General.G = l
			#for g in General.G:
			#	print g
			General.Num = len(l)

			for g in General.G:
				if(g.index != 0):
					General.G[0].forwardMessage(Message(self.order, []), g.index)

			# the initial general always comes to a consensus of the given order per spec
			l = [self.order]
			for g in General.G:
				if(g.index != 0):
					if(g.inferenceroot.children[0].resolved):
						l.append(g.inferenceroot.children[0].value)
					else:
						print "ERR, inferences not resolved"

			if(hasattr(self, "expectation")):
				index = 0

				for i in l:
					if i != self.expectation:
						print "Err, general " + str(index) + " came to consensus with wrong value"
					index += 1
			else:
				print("scenario unsolvable, generals have resolved values that will not come to consensus")

	@classmethod
	def countTraitors(cls, G):
		traitors = 0
		for g in G:
			if(not g.loyal):
				traitors += 1
		return traitors

	@classmethod
	def generateFullBinaryTree(cls, parent, n):
		parent.true = SimpleNode(parent, True)
		parent.false = SimpleNode(parent, False)
		if(n > 1):
			Scenario.generateFullBinaryTree(parent.true, n-1)
			Scenario.generateFullBinaryTree(parent.false, n-1)

	@classmethod
	def allPaths(cls, root, pathlist):
		if(root.true is not None):
			Scenario.allPaths(root.true, pathlist)
		if(root.false is not None):
			Scenario.allPaths(root.false, pathlist)

		if(root.true is None and root.false is None):
			l = []
			l.append(root)
			p = root
			while p.parent is not None:
				l.append(p.parent)
				p = p.parent
			pathlist.append(l)

	# helper method for printing
	@classmethod
	def pathToLoyaltyList(cls, p):
		l = []
		for n in p:
			if n.value is None:
				continue
			l.append(n.value)
		return l

	@classmethod
	def pathToGeneralList(cls, p):
		index = 0
		l = []
		for n in p:
			if n.value is None:
				continue
			l.append(General(index, n.value))
			index += 1
		return l

class SimpleNode:
	def __init__(self, parent, value):
		self.parent = parent
		self.value = value
		self.true = None
		self.false = None

if __name__ == "__main__":

	s = Scenario(1, 4, 1, True)
	s = Scenario(1, 4, 1, False)
	s = Scenario(2, 7, 2, True)
	s = Scenario(2, 7, 2, False)
	s = Scenario(3, 10, 3, True)
	s = Scenario(3, 10, 3, False)