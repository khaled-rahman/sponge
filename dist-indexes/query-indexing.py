import workload
import fnmatch
import types, sys, random

SIZE = 100
K = 3
Q = 100

DEBUG = False

def hashcode(v):
	global SIZE
	s = 0	
	for i in range(len(v)):
		s += ord(v[i]) 
	return s % SIZE

def oneBits(n):
	one = 0
	while n != 0:
		if n & 1 != 0:
			one += 1
		n >>= 1
	return one			
			
class DataItem:
	def __init__(self, key, dataitem):
		self.key = key
		self.dataitem = dataitem
				
	def hashcode(self):
		s = 0
		#for k, v in dataitem.items():
		#	s += hascode(k) + hashcode(v)
		# return s % SIZE				
		return hashcode(self.key)
	
	def __str__(self):
		return "[" + self.key + ", " + str(self.dataitem) + "]"
	
	def __repr__(self):
		return "[" + self.key + ", " + str(self.dataitem) + "]"
	
	def __eq__(self, another):
		return self.key == another.key

	def __hash__(self):
		return self.key.__hash__()
	
	def size(self):
		s = len(self.key)
		for k, v in self.dataitem.items():
			s += len(k) + len(v) if type(v) is types.StringType else 4
		return s	
	
	def contentsize(self):
		return self.dataitem['size']
						
class Query:
	def __init__(self, dataitem):
		self.dataitem = dataitem
		
	def hashcode(self):
		s = self.key()				
		return hashcode(s) % SIZE
	
			
	def __str__(self):
		return "[" + str(self.dataitem) + "]"
	
		
	def key(self):
		s = ''
		for k, v in self.dataitem.items():
			s = s + "::" + k + ":" + str(v)
		return s	
	
		
	"""
	def doesSatisfy(self, dataitem):
		satisfied = True		
		for k, v in self.dataitem.items():
			if type(v) is types.StringType and any(i in "+-*" for i in v):
				if DEBUG: print 'Checking for', k
				if v[len(v)-1] == '+':
					value = int(v[0:len(v)-1])
					if DEBUG: print value, dataitem.dataitem[k]
					if int(dataitem.dataitem[k]) < value:
						satisfied = False 	
				elif v[len(v)-1] == '-':
					value = int(v[0:len(v)-1])
					if int(dataitem.dataitem[k]) > value:
						satisfied = False		
				elif '-' in v:
					v1 = int(v.split('-')[0])
					v2 = int(v.split('-')[1])
					if int(dataitem.dataitem[k]) < v1 or int(dataitem.dataitem[k]) > v2:
						satisfied = False
				elif '*' in v:					
					satisfied = fnmatch.fnmatch(dataitem.dataitem[k], v)						
		
		return satisfied				
	"""
			
	def doesSatisfy(self, dataitem):
		for key, value in self.dataitem.items():
			if dataitem.dataitem[key] != value:
				return False
		return True
	
	def size(self):
		s = len(self.key)
		for k, v in self.dataitem.items():
			s += len(k) + (len(v) if type(v) is types.StringType else 4)
		return s	
						
class QueryNode:
	def __init__(self, Id):
		self.queries = {}
		self.Id = Id
	
	def insertDataItem(self, query, dataitem):
		if DEBUG: print self. Id, 'Recev ', dataitem.key, 'for', query, query.key()
		kq = query.key()
		if kq not in self.queries:
			self.queries[kq] = set()	
		self.queries[kq].add(dataitem)	
	
	def serveQuery(self, query):
		if DEBUG: print 'Node', self.Id, 'Query: ', query, query.key()
		if DEBUG: print self.queries.keys()
		
		kq = query.key()		
		if kq not in self.queries:
			if DEBUG: print 'Not in the list'
			return []
			
		result = []		
		for item in self.queries[kq]:
			if query.doesSatisfy(item):
				result.append(item.key)	
		return result		
	
	def size(self):
		s = 0
		for k, v in self.queries.items():
			s += len(k) + sum(d.size() for d in v)
		return s
	
	def count(self):
		return len(self.queries)
	
	def objectcount(self):
		s = 0
		for k, v in self.queries.items():
			s += len(v)
		return s

						
class QueryOverlay:
	def __init__(self):
		self.qnodes = [QueryNode(i) for i in range(SIZE)]
		self.traffic = 0
		
	def updatestat(self):
		self.traffic += 1
	
	def getstat(self):
		return self.traffic
		
			
	def insertDataItem(self, query, dataitem):
		index = query.hashcode()
		if DEBUG: print "Putting query", query, "at query node", index
		self.qnodes[index].insertDataItem(query, dataitem)
		self.updatestat()
			
	def serveQuery(self, query):
		index = query.hashcode()
		if DEBUG: print 'Requesting items for', query, 'from query node', index 
		self.updatestat()
		return self.qnodes[index].serveQuery(query) 	

		
class ContentNode:
	def __init__(self, Id, qoverlay):
		self.dataitems = {}
		self.Id = Id
		self.qoverlay = qoverlay
	
	def putItem(self, dataitem):
		self.dataitems[dataitem.key] = dataitem
		
		# push possible queries onto query nodes
		keys = []
		values = []
		for k, v in dataitem.dataitem.items():
			keys.append(k)
			values.append(v)
		
		n = len(dataitem.dataitem) 
		
		# Pushing indexes onto the overlay
		for i in range(1, 2 ** n):
			query = {}
			if oneBits(i) > K:
				continue
			for pos in range(n):
				if i & (1 << pos):				
					query[keys[pos]] = values[pos]

			self.qoverlay.insertDataItem(Query(query), dataitem)				
			
	def getItem(self, key):
		if key not in self.dataitems.keys():
			return key
		return self.Id, self.dataitems[key]	
		
	def size(self):
		s = 0
		for k, v in self.dataitems.items():
			s += v.size() / 1000.0 + v.contentsize()
		return s # in KB
	
	def count(self):
		return len(self.dataitems)
				
class ContentOverlay:
	def __init__(self, qoverlay):
		self.cnodes = [ContentNode(i, qoverlay) for i in range(SIZE)]
	
	def putItem(self, dataitem):
		index = hashcode(dataitem.key)
		if DEBUG: print "Putting item", dataitem, "at content node", index
		self.cnodes[index].putItem(dataitem)
	
	def getItem(self, key):
		index = hashcode(key)
		return self.cnodes[index].getItem(key)


class Client:
	def __init__(self):
		self.qoverlay = QueryOverlay()
		self.coverlay = ContentOverlay(self.qoverlay)
		random.seed(100)
	
	def do(self, N):
		for i in range(N):
			key, dataitem = workload.generateDataitem()
			d = DataItem(key, dataitem)
			self.coverlay.putItem(d)
		"""	
		for i in range(SIZE):
			print N, K, i, 'Q:', self.qoverlay.qnodes[i].count(), self.qoverlay.qnodes[i].objectcount(), 
			print self.qoverlay.qnodes[i].size() / 1000.0, 'KB', 
			print 'D:', self.coverlay.cnodes[i].count(), self.coverlay.cnodes[i].size() / 1000.0, 'MB'
		"""
										
		for i in range(Q):
			q = Query(workload.generateQuery(K))	
										
			result = self.qoverlay.serveQuery(q)
			#print "Query results: records", len(result), self.qoverlay.getstat()
			assert len(result) == len(workload.answerQuery(q.dataitem))
			#print "Exact results: records", len(workload.answerQuery(q.dataitem))
			#print
			
		print 'N', N, 'K', K, 'Q', Q, 'DTHTraffic', self.qoverlay.getstat()
			
		#for r in result:
		#	cnode, obj = self.coverlay.getItem(r.key)
		#	if DEBUG: print 'From', cnode, obj

def main():
	global K, Q
	if len(sys.argv) < 4:
		print 'Usage: <script> N (#objects) K(#max attributes) Q(#Query)'
		sys.exit(0)
	
	N = int(sys.argv[1])
	K = int(sys.argv[2])
	Q = int(sys.argv[3])
	
	client = Client()
	client.do(N)
			
if __name__ == "__main__":	
	main()

