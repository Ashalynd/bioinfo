import sys

k = int(sys.argv[1])
d = int(sys.argv[2])

dna = sys.argv[3]

ldna = len(dna)-(2*k+d)+1

pairs = []

for i in range(ldna):
	pairs.append((dna[i:i+k],dna[i+k+d:i+2*k+d]))

print ",".join(["(%s|%s)" % p for p in sorted(pairs)])