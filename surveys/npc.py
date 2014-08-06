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
		self.resourceVector = []
		self.newResourceVector = []
		self.resourceWeights = [random(), random(), random()]
		self.emoName = ["Joy", "Hope", "Sorrow", "Fear"]
		self.emotion = [0, 0, 0, 0]
		self.nextAction = "Wait"
		self.sayHello()
	
	def sayHello(self):
		return self.name

	def getAction(self):
		return self.nextAction

	def getWeights(self):
		return [round(Weight, 2) for Weight in self.resourceWeights]

	def getResources(self):
		return self.resourceVector

	def getNewResources(self):
		return self.newResourceVector

	def showResource(self):
		#To show the resources combined with the name
		return [':'.join(reso) for reso in zip(self.resourceName, [str(round(resoval, 2)) for resoval in self.resourceVector])]

	def showNR(self):
		#To show the new resources with the names
		return [':'.join(reso) for reso in zip(self.resourceName, [str(round(resoval, 2)) for resoval in self.newResourceVector])]		

	def getEmotion(self):
		return [':'.join(emo) for emo in zip(self.emoName, [str(round(emoval,2)) for emoval in self.emotion])]

	def passCost(self):
		return ((1-self.resourceVector[0])*self.resourceWeights[0] +
			(0.5 - self.resourceVector[1])*self.resourceWeights[1] +
			(0.3)*self.resourceWeights[2])

	def waitCost(self):
		return (-0.3)*self.resourceWeights[2]

	def protestCost(self):
		return ((1-self.resourceVector[0])*self.resourceWeights[0] +
			(0.85 - self.resourceVector[1])*self.resourceWeights[1])

	def actionCost(self):
		return ((self.newResourceVector[0]-self.resourceVector[0])*self.resourceWeights[0] +
			(self.newResourceVector[1] - self.resourceVector[1])*self.resourceWeights[1] +
			(self.newResourceVector[2]- self.resourceVector[2])*self.resourceWeights[2])

	def decidePass(self, position):
		if self.passCost() > 0:
			if position != 0:
				self.nextAction = "Pass"

	def decideProtest(self, beingPassed):
		if beingPassed:
			if self.protestCost() > self.waitCost():
				self.nextAction = "Protest"

	def sanityCheck(self, indx, notbeingPassed):
		if self.nextAction == "Protest" and notbeingPassed:
			if self.passCost() > 0:
				self.nextAction = 'Pass'
			else:
				self.nextAction = 'Wait'

	def computeEmotion(self, expectation):
		for indx, resource in enumerate(self.resourceVector):
			desire = (self.newResourceVector[indx] - resource)*self.resourceWeights[indx]
			if (desire > 0) and (expectation == 1):
				self.emotion[0] += desire           #The Joy Emotion
			elif (desire > 0) and (expectation < 1):
				self.emotion[1] += desire * expectation    #The Hope Emotion
			elif (desire < 0) and (expectation == 1):
				self.emotion[2] += desire           #The Sorrow Emotion
			elif (desire < 0) and (expectation < 1):
				self.emotion[3] += desire * expectation    #The Fear Emotion


class human(NPC):
	"""docstring for human"""
	def __init__(self, name):
		super(human, self).__init__(name)
