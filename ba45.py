import sys
from collections import Counter

fname = sys.argv[1]
k = int(sys.argv[2])
L = int(sys.argv[3])
t = int(sys.argv[4])
print k, L, t

CHUNK_SIZE = L*2

print CHUNK_SIZE

elements = Counter()
clumped = set()

f = open(fname)
data = f.read(CHUNK_SIZE)
mlen = len(data)

ib = 0
ctr = CHUNK_SIZE
for i in xrange(L-k):
	element = data[i:i+k]
	elements[element]+=1
	if elements[element]>=t:
		clumped.add(element)
		del elements[element]
while i<mlen-k:
#	oldlen = len(clumped)
#	clumped = clumped.union(set([key for key,v in elements.iteritems() if v>=t]))
#	if len(clumped)>oldlen:
#		print ctr, len(clumped)
	gone_away = data[ib:(ib+k)]
	elements[gone_away]-=1
	if elements[gone_away]==0:
		del elements[gone_away]
	i+=1
	ib+=1
	added = data[i:i+k]
#	if added not in clumped:
	elements[added]+=1
	if elements[added]>=t:
		clumped.add(added)
		del elements[added]
		print ctr, len(clumped)
	if i >= mlen-k:
		nextdata = f.read(CHUNK_SIZE)
		ctr += CHUNK_SIZE
		data = data[ib:]+nextdata
		mlen = len(data)
		i-=ib
		ib=0

print " ".join([str(a) for a in clumped])
print len(clumped)