import sys
fname = sys.argv[1]
f = open(fname)
pattern = f.readline().strip()
text = f.readline().strip()
print pattern
print text

index = -1
index=text.find(pattern,index+1)
a = []
while index>=0:
	a.append(str(index))
	index = text.find(pattern,index+1)
print " ".join(a)