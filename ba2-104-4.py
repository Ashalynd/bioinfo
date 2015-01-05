import sys
from collections import Counter

input = [int(p) for p in sys.argv[1:]]
input.sort()

print input

output = []

l = len(input)
for i in xrange(1,l):
	for j in xrange(i):
		diff = input[i]-input[j]
		if diff>0:
			output.append(diff)

output.sort()
print " ".join([str(t) for t in output])
