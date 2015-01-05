import sys
fname = sys.argv[1]
f = open(fname)
text = f.readline().strip()

themin = 0
curmin = 0
pp = []

i = 0
lentext = len(text)
while i<lentext:
	if text[i] == 'C':
		curmin -=1
	elif text[i] == 'G':
		curmin+=1
	if curmin<themin:
		pp = [ i+1 ]
		themin = curmin
	elif curmin == themin:
		pp.append(i+1)
	i+=1

print themin
print " ".join([str(p) for p in pp])