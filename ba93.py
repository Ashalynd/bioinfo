import sys
fname = sys.argv[1]
f = open(fname)
pattern = f.readline().strip()
text = f.readline().strip()
miss = int(f.readline().strip())

lp = len(pattern)
lt = len(text)
print lp, lt

pos = []

i = 0

while i <= lt-lp:
	j = 0
	diff = 0
	while j<lp:
		if text[i+j]!=pattern[j]:
			diff+=1
			if diff>miss:
				break
		j+=1
	if diff<=miss:
		pos.append(str(i))
	i+=1

print " ".join(pos)
