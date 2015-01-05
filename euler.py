import sys, fileinput

def walk_graph(graph, walked_graph, num_edges, cycle):
#	print cycle, num_edges
	if len(cycle) == num_edges:
		return cycle
#find the starting node
	start = 0
	node = cycle[start]
	while start<len(cycle):
		node = cycle[start]
		if len(walked_graph[node])<len(graph[node]):
			break
		start+=1
#refurbish cycle
	cycle = cycle[start:]+cycle[:start]
	if len(cycle)==1:
		cycle = []
	
	while len(cycle)<num_edges and len(graph[node])>len(walked_graph[node]):
		cycle.append(node)
		next_node = [ii for ii in graph[node] if ii not in walked_graph[node]][0]
		walked_graph[node].add(next_node)
		node = next_node

#	print cycle

	return walk_graph(graph, walked_graph, num_edges, cycle)

source = fileinput.input()


graph = {}
walked_graph = {}
num_edges = 0

for line in source:
	if '->' not in line:
		break
	(s,t) = [l.strip() for l in line.strip().split('->')]
	nodes = set(t.split(','))
	graph[s] = nodes
	num_edges += len(nodes)
	walked_graph[s] = set()

source.close()

#print graph
#print walked_graph

cycle = walk_graph(graph, walked_graph, num_edges, [graph.keys()[0]])

cycle.append(cycle[0])

print '->'.join(cycle)