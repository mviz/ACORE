"""

Author: Yathi

Description:
	The Base NPC class from which both Humans and Critters are derived
	We could have other kinds of NPCs also derived from this base class!

Changelog:
May 27th: Created the file.
June 23rd: Changed the resource sturcture to the vector model.
"""

from random import random


class NPC(object):
	"""docstring for NPC"""
	def __init__(self, name):
		super(NPC, self).__init__()
		self.name = name
		self.A = [] #The actions
		self.resourceName = ["Health", "Reputation", "Proximity"]
		self.resourceVector = [1, 1, 0.3]
		self.newResourceVector = []
		self.resourceWeights = [random(), random(), random()]
		self.beingPassed = False
		self.beingProtested = False
		self.emoName = ["Joy", "Hope", "Fear", "Sorrow"]
		self.emotion = [0, 0, 0, 0]
		self.nextAction = "Wait"
		self.sayHello()
	#TestMethod
	def sayHello(self):
		print self.name , "Hello"
		return self.name

	def getAction(self):
		return self.nextAction

	def getWeights(self):
		return [round(Weight, 2) for Weight in self.resourceWeights]

	def getResources(self):
		return self.resourceVector

	def getNewResources(self):
		return self.newResourceVector

	def getEmotion(self):
		return [':'.join(emo) for emo in zip(self.emoName, [str(emoval) for emoval in self.emotion])]

	def returnEmotion(self):
		if self.nextAction == "Pass":
			#For Reputation
			Joy = 0
			Hope = 0
			Fear = 0
			Sorrow = 0
			expectation_repu = 0.95
			expectation_proxi = 0.95
			self.newResourceVector = [1, 0.5, self.resourceVector[2]+0.3]
			for indx, resource in enumerate(self.resourceVector):
				desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
				if (desire > 0) and (expectation_repu == 1):
					Joy += desire
				elif (desire > 0) and (expectation_repu < 1):
					Hope += desire * expectation_repu
				elif (desire < 0) and (expectation_repu == 1):
					Fear += desire
				elif (desire < 0) and (expectation_repu < 1):
					Sorrow += desire * expectation_repu

			self.emotion = [Joy, Hope, Fear, Sorrow]

		elif self.nextAction == "Wait" and self.beingPassed:
			Joy = 0
			Hope = 0
			Fear = 0
			Sorrow = 0
			expectation_repu = 0.95
			expectation_proxi = 0.95
			self.newResourceVector = [1, 1, self.resourceVector[2]-0.3]
			for indx, resource in enumerate(self.resourceVector):
				desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
				if (desire > 0) and (expectation_repu == 1):
					Joy += desire
				elif (desire > 0) and (expectation_repu < 1):
					Hope += desire * expectation_repu
				elif (desire < 0) and (expectation_repu == 1):
					Fear += desire
				elif (desire < 0) and (expectation_repu < 1):
					Sorrow += desire * expectation_repu

			self.emotion = [Joy, Hope, Fear, Sorrow]
		elif self.nextAction == "Protest":
			Joy = 0
			Hope = 0
			Fear = 0
			Sorrow = 0
			expectation_repu = 0.95
			expectation_proxi = 0.95
			self.newResourceVector = [1, 0.85, self.resourceVector[2]]
			self.resourceVector[2] = self.resourceVector[2] - 0.3
			for indx, resource in enumerate(self.resourceVector):
				desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
				if (desire > 0) and (expectation_repu == 1):
					Joy += desire
				elif (desire > 0) and (expectation_repu < 1):
					Hope += desire * expectation_repu
				elif (desire < 0) and (expectation_repu == 1):
					Fear += desire
				elif (desire < 0) and (expectation_repu < 1):
					Sorrow += desire * expectation_repu

			self.emotion = [Joy, Hope, Fear, Sorrow]


		return self.emotion

	def finalAction(self):
		if self.nextAction == "Pass":
			if self.beingProtested:
				if random() > 0.5:
					Joy = 0
					Hope = 0
					Fear = 0
					Sorrow = 0
					expectation_repu = 1
					expectation_proxi = 1
					self.resourceVector[2] = self.resourceVector[2] + 0.3
					self.resourceVector[1] = 0.85

					for indx, resource in enumerate(self.resourceVector):
						desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
						if (desire > 0) and (expectation_repu == 1):
							Joy += desire
						elif (desire > 0) and (expectation_repu < 1):
							Hope += desire * expectation_repu
						elif (desire < 0) and (expectation_repu == 1):
							Fear += desire
						elif (desire < 0) and (expectation_repu < 1):
							Sorrow += desire * expectation_repu

					self.emotion = [Joy, Hope, Fear, Sorrow]
				else:
					Joy = 0
					Hope = 0
					Fear = 0
					Sorrow = 0
					expectation_repu = 1
					expectation_proxi = 1
					desire_repu = (0.85 - self.resourceVector[1])*self.resourceWeights[1]
					desire_proxi = (0)*self.resourceWeights[2]
					self.resourceVector[1] = 0.85

					for indx, resource in enumerate(self.resourceVector):
						desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
						if (desire > 0) and (expectation_repu == 1):
							Joy += desire
						elif (desire > 0) and (expectation_repu < 1):
							Hope += desire * expectation_repu
						elif (desire < 0) and (expectation_repu == 1):
							Fear += desire
						elif (desire < 0) and (expectation_repu < 1):
							Sorrow += desire * expectation_repu

					self.emotion = [Joy, Hope, Fear, Sorrow]
			else:
				if random() > 0.9:
					Joy = 0
					Hope = 0
					Fear = 0
					Sorrow = 0
					expectation_repu = 1
					expectation_proxi = 1
					desire_repu = (0.85 - self.resourceVector[1])*self.resourceWeights[1]
					desire_proxi = (0.3)*self.resourceWeights[2]
					self.resourceVector[2] = self.resourceVector[2] + 0.3
					self.resourceVector[1] = 0.85

					for indx, resource in enumerate(self.resourceVector):
						desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
						if (desire > 0) and (expectation_repu == 1):
							Joy += desire
						elif (desire > 0) and (expectation_repu < 1):
							Hope += desire * expectation_repu
						elif (desire < 0) and (expectation_repu == 1):
							Fear += desire
						elif (desire < 0) and (expectation_repu < 1):
							Sorrow += desire * expectation_repu

					self.emotion = [Joy, Hope, Fear, Sorrow]
				else:
					Joy = 0
					Hope = 0
					Fear = 0
					Sorrow = 0
					expectation_repu = 1
					expectation_proxi = 1
					desire_repu = (0.85 - self.resourceVector[1])*self.resourceWeights[1]
					desire_proxi = (0)*self.resourceWeights[2]
					self.resourceVector[1] = 0.85

					for indx, resource in enumerate(self.resourceVector):
						desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
						if (desire > 0) and (expectation_repu == 1):
							Joy += desire
						elif (desire > 0) and (expectation_repu < 1):
							Hope += desire * expectation_repu
						elif (desire < 0) and (expectation_repu == 1):
							Fear += desire
						elif (desire < 0) and (expectation_repu < 1):
							Sorrow += desire * expectation_repu

					self.emotion = [Joy, Hope, Fear, Sorrow]
		elif self.nextAction == "Wait" and self.beingPassed:
			Joy = 0
			Hope = 0
			Fear = 0
			Sorrow = 0
			expectation_repu = 1
			expectation_proxi = 1
			desire_proxi = (-0.3)*self.resourceWeights[2]
			self.resourceVector[2] = self.resourceVector[2] - 0.3

			for indx, resource in enumerate(self.resourceVector):
				desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
				if (desire > 0) and (expectation_repu == 1):
					Joy += desire
				elif (desire > 0) and (expectation_repu < 1):
					Hope += desire * expectation_repu
				elif (desire < 0) and (expectation_repu == 1):
					Fear += desire
				elif (desire < 0) and (expectation_repu < 1):
					Sorrow += desire * expectation_repu
				self.emotion = [Joy, Hope, Fear, Sorrow]
		elif self.nextAction == "Protest":
			Joy = 0
			Hope = 0
			Fear = 0
			Sorrow = 0
			expectation_repu = 1
			expectation_proxi = 1
			desire_repu = (0.85 - self.resourceVector[1])*self.resourceWeights[1]
			desire_proxi = (0.3)*self.resourceWeights[2]

			for indx, resource in enumerate(self.resourceVector):
				desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
				if (desire > 0) and (expectation_repu == 1):
					Joy += desire
				elif (desire > 0) and (expectation_repu < 1):
					Hope += desire * expectation_repu
				elif (desire < 0) and (expectation_repu == 1):
					Fear += desire
				elif (desire < 0) and (expectation_repu < 1):
					Sorrow += desire * expectation_repu

				self.emotion = [Joy, Hope, Fear, Sorrow]

	def passCost(self):
		return ((1-self.resourceVector[0])*self.resourceWeights[0] + 
			(0.5 - self.resourceVector[1])*self.resourceWeights[1] + 
			(0.3)*self.resourceWeights[2])

	def waitCost(self):
		if self.beingPassed:
			return (-0.3)*self.resourceWeights[2]
		else:
			return 0

	def protestCost(self):
		return ((1-self.resourceVector[0])*self.resourceWeights[0] + 
			(0.85 - self.resourceVector[1])*self.resourceWeights[1])

	def bestAction(self):
		if self.beingPassed:
			if self.protestCost() > self.waitCost():
				self.nextAction = "Protest"
		else:
			if self.passCost() > self.waitCost():
				self.nextAction = "Pass"
		return self.nextAction


class human(NPC):
	"""docstring for human"""
	def __init__(self, name):
		super(human, self).__init__(name)