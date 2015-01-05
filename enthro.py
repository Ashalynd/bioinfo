import sys, math
from collections import Counter

fname = sys.argv[1]

mm = []

f = open(fname)
counted = False

for l in f.readlines():
	therow = l.strip().split()
	if not counted:
		mm = [Counter() for i in range(len(therow))]
		counted = True
	for (index,r) in enumerate(therow):
		mm[index][r.upper()]+=1

f.close()
print mm

enthropy = 0.0
enthropies = [0.0]*len(mm)
counter = 0

for m in mm:
	for (k,v) in m.iteritems():
		p = 0.1*v
		enthropies[counter] += (p*math.log(p)/math.log(2))
	enthropy-=enthropies[counter]
	counter+=1

print enthropies
print enthropy