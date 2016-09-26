import sys, random

class Powerlaw:
	def __init__(self, n):
		# 1 with prob 1/1^2
		# 2 with prob 1/2^2
		# 3 with prob 1/3^2
		# etc
		
		self.totalp = 0.0		
		for i in range(1, n + 1):
			self.totalp += 1.0 / (i * i)
		
	def next(self):					
		P = random.uniform(0, 1.0)
		i = 1
		pp = (1 / (i * i)) / self.totalp
		while pp < P:
			i += 1
			pp = pp + (1.0 / (i * i)) / self.totalp  
		return i - 1

class Uniform:
	def __init__(self, n):
		self.n = n
	
	def next(self):
		return random.randint(0, self.n - 1)	
		

databanks = {}
databanks['category'] = ['Games', 'News', 'Books']
databanks['subcategory'] = ['Arcade', 'Block', 'Card']
databanks['releaseyear'] = [2000, 2001]
databanks['platform'] = ['Android', 'iOS', 'Windows8']
databanks['version'] = [2.01, 2.02, 4.04, 6.01]
databanks['size'] = [s for s in range(100, 10000, 100)]
databanks['language'] = ['Eng', 'Bng', 'Spn', 'De']
databanks['country'] = ['us', 'eng', 'bd', 'in', 'kr']
databanks['keyword'] = ['abc', 'def', 'rere', 'sf']

generators = {}
generators['category'] = Powerlaw(len(databanks['category']))
generators['subcategory'] = Uniform(len(databanks['subcategory']))
generators['releaseyear'] = Uniform(len(databanks['releaseyear']))
generators['platform'] = Powerlaw(len(databanks['platform']))
generators['version'] = Uniform(len(databanks['version']))
generators['size'] = Powerlaw(len(databanks['size']))
generators['language'] = Powerlaw(len(databanks['language']))
generators['country'] = Uniform(len(databanks['country']))
generators['keyword'] = Uniform(len(databanks['keyword']))

random.seed(100)

ID = 1
K = 4
dataitems = {}	
prob = {}
prob['category'] = 0.9
prob['subcategory'] = 0.2
prob['releaseyear'] = 0.4
prob['platform'] = 0.9
prob['version'] = 0.5
prob['size'] = 0.0
prob['language'] = 0.3
prob['country'] = 0.4
prob['keyword'] = 0.1

def generateDataitem():
	global ID
	dataitem = {}
	key  = str(random.randint(0, 2 ** 31 - 1))
	ID = ID + 1
	for attr in databanks.keys():
		dataitem[attr] = databanks[attr][generators[attr].next()]
	#print dataitem
	dataitems[key] = dataitem
	return key, dataitem

def satisfy(dataitem, query):	
	for k, v in query.items():
		if dataitem[k] != v:
			return False
	return True			
	

def generateQuery(K):
	query = {}
	for key in databanks.keys():
		if prob[key] < random.uniform(0, 1.0):
			query[key] = databanks[key][generators[key].next()]
		if len(query) == K:
			break		
	return query	


def answerQuery(query):
	result = []
	for key, obj in dataitems.items():
		if	satisfy(obj, query):
			result.append(key)
	return result
	
				
def main():
	for i in range(1000):
		k, d = generateDataitem()
					
	for i in range(10):
		q = generateQuery(K)
		print len(answerQuery(q))	


if __name__ == "__main__":
	main()		
			
