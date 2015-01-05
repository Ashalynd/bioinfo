import sys, fileinput, bioinfo

source = fileinput.input()

genome_p = bioinfo.read_permutations(source)
genome_q = bioinfo.read_permutations(source)

source.close()

print genome_p
print genome_q

graph = {}

for p in genome_p:
	bioinfo.permutation_to_graph(p, graph)

for q in genome_q:
	bioinfo.permutation_to_graph(q, graph)

print graph

cc = bioinfo.connected_components(graph)

print cc
print len(graph)/2 - cc