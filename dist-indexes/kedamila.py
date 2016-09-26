import random

SIZE = 8
K = 50

def distance (v1, v2):
	return v1 ^ v2

def higherBitPos(v):
	mask = (1 << (SIZE - 1))
	for pos in range(SIZE, 0, -1):	
		if (v & mask) == 0:
			mask >>= 1	
		else:
			return pos
	return 0	
	
class Node:
	def __init__(self, Id):
		self.Id = Id
		self.bucket = {} 		
	
	def __hash__(self):
		return self.Id
	
	def __eq__(self, another):
		return self.Id == another.Id
	
	def getBucketIndex(self, n):	
		mask = 1 << (SIZE - 1)
		for pos in range(8, 0, -1):
			if self.Id & mask != n & mask:
				return pos
			mask >>= 1	
		return -1		
		
	def __cmp__(self, n):
		if distance(0, self.Id) < distance(0, n.Id):
			return -1
		if distance(0, self.Id) > distance(0, n.Id):	
			return 1
		return 0	
	
					
	def addNewNode(self, newNode):
		bckindex = self.getBucketIndex(newNode.Id)
		if bckindex not in self.bucket:
			self.bucket[bckindex] = []
		
		if newNode not in self.bucket[bckindex]:				
			self.bucket[bckindex].append(newNode)
		
		print self, 'Add', newNode, 'at', bckindex			
	
	def joinByPeer(self, peer):								
		nodelist = peer.findNode(self.Id)
		print "Node", self.Id, "got", nodelist 
		for node in nodelist:
			self.addNewNode(node)

		# Add this node to the list
		peer.addNewNode(self)		
					
	def findNode(self, node):		
		lookupid = node.Id										
		dist = distance(self.Id, lookupid)
		print self, lookupid, dist
		if dist == 0:
			return [self]
			
		print "Finding", lookupid, "thru", self.Id, "dist", dist
		
		bckindex = self.getBucketIndex(lookupid)		
		nodelist = []
		
		# Check whether bckindex is in the bucket
		if bckindex in self.bucket:
			for node in self.bucket[bckindex]:
				lookedup = node.findNode(lookupid)
			 	for nn in lookedup:
					nodelist.append(nn)

		# Check whether K entries in the list
		# If not, add other nodes from the bucket
		if len(nodelist) < K:
			for bck in self.bucket:
				if bck != bckindex:
					for nn in self.bucket[bck]:
						nodelist.append(nn)									

		nodelist = sorted(nodelist)		
		return nodelist[0:K]

	def __repr__(self):
		return str(self.Id)
	
	def __str__(self):
		return str(self.Id)
		
			
	def printBucket(self):
		s = 'Node: ' + str(self.Id) + '\n'	
		for k, v in self.bucket.items():
			s += str(k) + '=>' + str(v) + '\n'
		print s
		
		
if __name__ == "__main__":
	n0 = Node(0)
	print n0
	
	nodes = []	
	for i in range(10):
		n = Node(i)	
		nodes.append(n)
		n.joinByPeer(n0)
	
	n0.printBucket()
	for node in nodes:
		node.printBucket()	
	
	print
	print
	print nodes[5].findNode(6)
															
