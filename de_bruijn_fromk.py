import sys, fileinput

source = fileinput.input()

graph = {}

kmers = {}

for line in source:
	kmer = line.strip()
	if kmer == 'Output:':
		break
	head = kmer[:-1]
	tail = kmer[1:]
	if head not in graph:
		graph[head] = set()
	graph[head].add(tail)

for head in sorted(graph.keys()):
	print "%s -> %s" % (head, ",".join([tail for tail in sorted(graph[head])]))
