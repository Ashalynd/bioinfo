import sys
from collections import Counter

letters = 'AGTC'
replaces = dict([(d,set(letters)-set(d)) for d in letters])

def mutate(str, level, maxlevel, cntr):
	cntr[str]=1
	if level>=maxlevel:
		return
	slen = len(str)
	for i in xrange(slen):
		for r in replaces[str[i]]:
			newstr = str[:i]+r+str[i+1:]
			mutate(newstr, level+1, maxlevel, cntr)

text = sys.argv[1]
k = int(sys.argv[2])
miss = int(sys.argv[3])

ctr = Counter()

lentext = len(text)

for pos in xrange(lentext-k):
	str = text[pos:pos+k]
#	print str
	newctr = Counter()
	mutate(str,0,miss,newctr)
	ctr+=newctr
#	print ctr

print ctr.most_common(1)
valmax = ctr.most_common(1)[0][1]
print valmax

entries = [v for (v,k) in ctr.iteritems() if k == valmax]

print " ".join(entries)

