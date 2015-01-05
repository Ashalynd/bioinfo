import sys, fileinput
from heapq import *

fi = fileinput.input()

k = int(fi.readline().strip())
dna = fi.readline().strip()
fi.close()

#print k, dna

kmers = []

ldna = len(dna)-k+1
for i in range(ldna):
	heappush(kmers,dna[i:i+k])

while kmers:
	kmer = heappop(kmers)
	print kmer
