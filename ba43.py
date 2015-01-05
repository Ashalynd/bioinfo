import sys
from collections import Counter
fname = sys.argv[1]
f = open(fname)
data = f.readline().strip()
mlen = len(data)
(k, L, t) = [int(x) for x in f.readline().strip().split()]
print k, L, t

#spot = data[:L]
elements = Counter()
clumped = set()
ib = 0
#print ib, type(ib)
for i in xrange(L-k):
	element = data[i:i+k]
	elements[element]+=1
while i<mlen-k:
	clumped = clumped.union(set([key for key,v in elements.iteritems() if v>=t]))
#	print ib, type(ib)
	gone_away = data[ib:(ib+k)]
	elements[gone_away]-=1
	i+=1
	ib+=1
	added = data[i:i+k]
	elements[added]+=1
print " ".join([str(a) for a in clumped])