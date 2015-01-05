import sys, fileinput
import bioinfo

source = fileinput.input()

kmers = bioinfo.read_kmer_list(source)
source.close()

#print kmers

"""
for kmerset in kmers.values():
	for kmer in kmerset:
		tail = kmer[1:]
		if tail in kmers:
			if kmer not in graph:
				graph[kmer] = set()
			graph[kmer].update(kmers[tail])
"""

(graph, graph_counts) = bioinfo.make_graph_with_counts(kmers)

walked_graph_counts = {kmer:[0,0] for kmer in graph_counts}

#print graph
#print graph_counts
#print walked_graph_counts

#for head in sorted(graph.keys()):
#	for tail in sorted(graph[head]):
#		print "%s -> %s" % (head, tail)

middles = []
contigs = []
for head in sorted(graph.keys()):
	if graph_counts[head]==[1,1]:
		middles.append(head)
		continue
	while walked_graph_counts[head][1]<graph_counts[head][1]:
		the_head = head
		contig = the_head
		while True:
			tails = [t for t in graph[the_head] if walked_graph_counts[t][0]<graph_counts[t][0]]
			if len(tails)==0:
				break
			the_tail = tails[0]
			walked_graph_counts[the_head][1]+=1
			walked_graph_counts[the_tail][0]+=1
			contig+=the_tail[-1]
			the_head = the_tail
			if graph_counts[the_head]!=[1,1]:
				break
		contigs.append(contig)

for contig in contigs:
	print contig
#print middles




