import sys, fileinput

source = fileinput.input()

graph = {}

kmers = {}

for line in source:
	kmer = line.strip()
	head = kmer[:-1]
	if head not in kmers:
		kmers[head] = set()
	kmers[head].add(kmer)

for kmerset in kmers.values():
	for kmer in kmerset:
		tail = kmer[1:]
		if tail in kmers:
			if kmer not in graph:
				graph[kmer] = set()
			graph[kmer].update(kmers[tail])

for head in sorted(graph.keys()):
	for tail in sorted(graph[head]):
		print "%s -> %s" % (head, tail)


