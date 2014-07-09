"""

Author: Yathi


Changelog:
May 27th: Created the file.
May 29th: Add the calculateThreat function
"""

from npc import NPC

def calculateThreat(npc):
	threat = 0
	for resource in npc.T:
		threat += npc.rank(resource)
	return threat



