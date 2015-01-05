import sys
from collections import Counter

weights_filename = "integer_mass_table.txt"

weights = {}

int_weights = set()

spectrum = Counter()

active_weighs = set()

result = set()

cyclos = {}

def get_weights():
	source_weights = open(weights_filename)
	for line in source_weights.readlines():
		(s, w) = line.strip().split()
		int_weights.add(int(w))

def verify_peptide(peptide):
	len_peptide = len(peptide)
	if spectrum[sum(peptide)]==0:
		return None

	all_weights = Counter([0, sum(peptide)])

	peptide += peptide 

	for i in xrange(len_peptide):
		for j in xrange(len_peptide-1):
			nextone = sum(peptide[i:i+j+1])
			if spectrum[nextone]<=all_weights[nextone]:
				return None
			all_weights[nextone]+=1
	return all_weights

def get_cyclospectrum(peptide):
	if not peptide in cyclos:
		cyclos[peptide] = verify_peptide(peptide)
	return cyclos[peptide]

def seq_cyclopeptides(t):
#	print "seq_cyclopeptides", t
	if t in result:
		return
	for tt in set(t):
		if t.count(tt)>spectrum[tt]:
			return
	if get_cyclospectrum(t) == spectrum:
		print "-".join(str(tt) for tt in t)
		result.add(t)
		return
	for w in active_weights:
		seq_cyclopeptides(t+(w,))


get_weights()
print int_weights

spectrum = Counter([int(s.strip()) for s in sys.argv[1:]])

print spectrum

active_weights = int_weights.intersection(set(spectrum.keys()))
print active_weights

seq_cyclopeptides(())

print result
print " ".join("-".join(str(tt) for tt in t) for t in result)
