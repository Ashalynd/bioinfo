import sys
pattern = sys.argv[1]
fname = sys.argv[2]
f = open(fname)
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