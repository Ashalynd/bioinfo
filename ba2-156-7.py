import sys
from collections import Counter

letters = 'AGTC'
replaces = dict([(d,set(letters)-set(d)) for d in letters])
inverses = {'A':'T','G':'C','T':'A','C':'G'}

def mutate(str, level, maxlevel, theset):
	theset.add(str)
	if level>=maxlevel:
		return
	slen = len(str)
	for i in xrange(slen):
		for r in replaces[str[i]]:
			newstr = str[:i]+r+str[i+1:]
			mutate(newstr, level+1, maxlevel, theset)

def get_mutation(kmer, mutated_kmers):
	if kmer not in mutated_kmers:
		mutated = set()
		mutate(kmer, 0, d, mutated)
		mutated_kmers[kmer] = mutated
	return mutated_kmers[kmer]

kmers = set()
motifs = set()
mutated_kmers = {}
a_mutateds = {}
fname = sys.argv[1]
f = open(fname)
(k,d) = [int(i) for i in f.readline().strip().split()]
print k,d
dna = [line.strip() for line in f.readlines()]
print dna
f.close()

for l in dna:
	thelen = len(l)-k+1
	for i in range(thelen):
		kmer = l[i:i+k]
		if kmer not in kmers:
			kmers.add(kmer)
			mutated = get_mutation(kmer, mutated_kmers)
			for mkmer in mutated:
				if not mkmer in a_mutateds:
					a_mutated = get_mutation(mkmer, mutated_kmers)
					a_mutateds[mkmer]=a_mutated

for am in a_mutateds:
	found = True
	for l in dna:
		thelen = len(l)-k+1
		foundHere = False
		for i in range(thelen):
			kmer = l[i:i+k]
			if kmer in a_mutateds[am]:
				foundHere = True
				break
		found = found and foundHere
		if not found:
			break
	if found:
		motifs.add(am)

result = [t for t in motifs]
result.sort()
print " ".join(result)
