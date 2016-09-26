class TrieNode:
	def __init__(self):
		self.values = {}
		
class Trie:
	def __init__(self):
		self.root = TrieNode()
		self.size = 0
		
	def put(self, code):
		node = self.root
		exists = True
		for i in range(len(code)):
			codeValue = code[i]
			
			try:
				node = node.values[codeValue]
			except KeyError as err:
				exists = False
				newNode = TrieNode()
				node.values[codeValue] = newNode
				node = newNode
		if exists:
			raise Exception("Item is already in the trie!!!")
		else:
			self.size = self.size + 1	
					
	def contains(self, code):
		node = self.root
		for i in range(len(code)):
			codeValue = code[i]			
			try:
				node = node.values[codeValue]
			except KeyError as err:
				return False
		return True
					
	def getSize(self):
		return self.size

