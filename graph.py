import sys, fileinput


def countPath(the_graph, cur_node, start_node):
	if cur_node == start_node:
		return 1
	links = the_graph[cur_node]
	return sum([countPath(the_graph, link, start_node) for link in links])


source = fileinput.input()

graph = {}

for line in source:
	(s,t) = [int(i) for i in line.strip().split()]
	if s not in graph:
		graph[s] = set()
	graph[s].add(t)

print graph

res = sum([countPath(graph, link, 1) for link in graph[1]])

print res