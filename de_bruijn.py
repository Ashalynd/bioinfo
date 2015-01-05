import sys, fileinput

source = fileinput.input()

graph = {}

kmers = {}

k = int(source.readline().strip())
dna = source.readline().strip()

source.close()

for i in range(len(dna)-k+1):
	kmer = dna[i:i+k]
	head = kmer[:-1]
	tail = kmer[1:]
	if head not in graph:
		graph[head] = set()
	graph[head].add(tail)

for head in sorted(graph.keys()):
	print "%s -> %s" % (head, ",".join([tail for tail in graph[head]]))
