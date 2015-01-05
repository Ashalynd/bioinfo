import sys

weights_filename = "integer_mass_table.txt"

weights = {}

source_weights = open(weights_filename)
for line in source_weights.readlines():
	(s, w) = line.strip().split()
	weights[s] = int(w)

#weights = dict([(line.strip().split()) for line in open(weights_filename).readlines()])

peptide = sys.argv[1]

len_peptide = len(peptide)

all_weights = [ 0 ]

peptide += peptide 

for i in xrange(len_peptide):
	for j in xrange(len_peptide-1):
		all_weights.append(sum([weights[p] for p in peptide[i:i+j+1]]))

all_weights.append(sum([weights[p] for p in peptide[:len_peptide]]))

all_weights.sort()
print " ".join(str(s) for s in all_weights)