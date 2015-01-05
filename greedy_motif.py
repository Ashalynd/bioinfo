import sys

fname = sys.argv[1]
letters = []

best_prob = 0.0
best_pattern = []

f = open(fname)

dna = f.readline().strip()
k = int(f.readline().strip())

ldna = len(dna)-k+1

profile = {}

for l in f.readline().strip().split():
	letters.append(l)
	profile[l]=[]

for line in f.readlines():
	for (index,l) in enumerate(line.strip().split()):
		profile[letters[index]].append(float(l))

print profile

for i in range(ldna):
	prob = 1.0
	for j in range(k):
		prob *= profile[dna[i+j]][j]
		if (prob==0 or prob<best_prob):
			break
	if prob==best_prob:
		best_pattern.append(dna[i:i+k])
	if prob>best_prob:
		best_prob = prob
		best_pattern = [dna[i:i+k]]

print best_prob
print best_pattern