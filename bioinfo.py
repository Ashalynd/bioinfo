import sys
import string
import operator


def prefix_tree_matching(trie, text):
	if len(text)==0:
		return ""
	cur_pos = 0
	cur_node = 1
	lt = len(text)
	while True:
		if cur_pos>=lt:
			print text
			return text
		symbol = text[cur_pos]
		if symbol in trie[cur_node]:
			cur_node = trie[cur_node][symbol]
			cur_pos+=1
		else:
			if cur_pos>0:
				print text[:cur_pos]
				return text[:cur_pos]
			else:
				print "no matches found"
			return ""

def tree_matching(trie, text, patterns):
	i = 0
	lt = len(text)
	nodes = []
	while i<len(text):
		result = prefix_tree_matching(trie, text[i:])
		if len(result)>0 and result in patterns:
			print i
			nodes.append(i)
		i+=1
	return nodes

def build_trie(trie, word):
	if len(word)==0:
		return trie
	cur_node = 1
	for letter in word:
		if not letter in trie[cur_node].keys():
			next_node = len(trie)
			trie[cur_node][letter]=next_node
			trie.append({})
			cur_node = next_node
		else:
			cur_node = trie[cur_node][letter]
	return trie

def print_trie(trie):
	lt = len(trie)
	for i in xrange(lt):
		for (k,v) in sorted(trie[i].iteritems(),key=operator.itemgetter(1)):
			print "%s %s %s" % (i, v, k)

# reads the permutation in brackets
def read_permutation(source):
	the_input = [int(dd) for dd in source.readline().strip()[1:-1].split()]
	return the_input

def read_permutations(source):
	the_inputs = source.readline().strip()[1:-1].split(')(')
	return [[int(dd) for dd in gene.split()] for gene in the_inputs]

def permutation_to_graph(permutation, graph):
	sz = len(permutation)
	for i in xrange(sz):
		j = (i+1) % sz
		abs_i = str(abs(permutation[i]))
		abs_j = str(abs(permutation[j]))
		vertex_i = abs_i+'e' if permutation[i]>0 else abs_i+'b'
		vertex_j = abs_j+'b' if permutation[j]>0 else abs_j+'e'
		if vertex_i not in graph:
			graph[vertex_i] = set()
		graph[vertex_i].add(vertex_j)
		if vertex_j not in graph:
			graph[vertex_j] = set()
		graph[vertex_j].add(vertex_i)
	return graph

def dfs(graph, marked, node):
	stack = []
	stack.append(node)
	while len(stack)>0:
		next_node = stack.pop()
		if next_node not in marked:
			marked.add(next_node)
			for child in graph[next_node]:
				stack.append(child)

def connected_components(graph):
	cc = 0
	marked = set()
	for node in graph:
		if node not in marked:
			cc+=1
			dfs(graph, marked, node)
	return cc

# converts the input (coming from file) into the list
def read_kmer_list(source):
	kmers = []
	for line in source:
		if line.strip() == 'Output:':
			break
		kmer = line.strip()
		kmers.append(kmer)
	return kmers

# gets the list, splits it into head and tail and counts inbound and outbound links
def make_graph_with_counts(kmers):
	graph_counts = {}
	graph = {}
	for kmer in kmers:
		(head, tail) = (kmer[:-1], kmer[1:])
		if head not in graph:
			graph[head] = set()
		graph[head].add(tail)
		if head not in graph_counts:
			graph_counts[head] = [0,0]
		graph_counts[head][1] +=1
		if tail not in graph_counts:
			graph_counts[tail] = [0,0]
		graph_counts[tail][0] +=1
	return (graph, graph_counts)

def readBlosum():
	blosum = {}
	fname = "BLOSUM62.txt"
	f = open(fname,"r")
	alphabet = f.readline().strip().split()
	for line in f.readlines():
		entries = line.strip().split()
		letter = entries[0]
		scores = [int(l) for l in entries[1:]]
		for (second, score) in zip(alphabet, scores):
			blosum[(letter,second)] = score
	return blosum

def dummyScores(match, miss):
	table = {}
	letters = string.ascii_uppercase
	seconds = string.ascii_uppercase
	for letter in letters:
		for second in seconds:
			table[(letter, second)] = miss if letter!=second else match
#	print table
	return table


def readScores(fname):
	table = {}
	f = open(fname,"r")
	alphabet = f.readline().strip().split()
	for line in f.readlines():
		entries = line.strip().split()
		letter = entries[0]
		scores = [int(l) for l in entries[1:]]
		for (second, score) in zip(alphabet, scores):
			table[(letter,second)] = score
	return table

def LCS(v, w, scores, indel):
	#indel is positive because it's supposed to be subtracted
	lv = len(v)
	lw = len(w)
	s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	backtrack = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	for i in range(lv+1):
		s[i][0] = -i*indel
	for j in range(lw+1):
		s[0][j] = -j*indel
	for i in range(1,lv+1):
		for j in range(1,lw+1):
			(local_max_ind, local_max) = (0, -1000)
			for (ind, sc) in zip (range(3), [s[i-1][j] - indel, s[i][j-1] - indel, s[i-1][j-1]+scores[(v[i-1],w[j-1])]]):
				if sc >= local_max:
					local_max_ind = ind
					local_max = sc
			s[i][j] = local_max
			if local_max_ind == 0:
				backtrack[i][j]='|'
			if local_max_ind == 1:
				backtrack[i][j]='-'
			if local_max_ind == 2:
				backtrack[i][j] = '\\'
#	print s
	return s[lv][lw], backtrack

def LCS_local(v, w, scores, indel):
	#indel is positive because it's supposed to be subtracted
	lv = len(v)
	lw = len(w)
	s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	backtrack = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	for i in range(lv+1):
		s[i][0] = -i*indel
	for j in range(lw+1):
		s[0][j] = -j*indel

	global_max = 0
	global_i = lv
	global_j = lw

	for i in range(1,lv+1):
		for j in range(1,lw+1):
			(local_max_ind, local_max) = (0, -1000)
			for (ind, sc) in zip (range(3), [s[i-1][j] - indel, s[i][j-1] - indel, s[i-1][j-1]+scores[(v[i-1],w[j-1])]]):
				if sc >= local_max:
					local_max_ind = ind
					local_max = sc
			if local_max<0:
				local_max = 0
				local_max_ind = 3
			s[i][j] = local_max
			if local_max>global_max:
				global_max = local_max
				global_i = i
				global_j = j
			if local_max_ind == 0:
				backtrack[i][j]='|'
			if local_max_ind == 1:
				backtrack[i][j]='-'
			if local_max_ind == 2:
				backtrack[i][j] = '\\'
			if local_max_ind == 3:
				backtrack[i][j] = '*'
#	print s
	return s[global_i][global_j], backtrack, global_i, global_j


def LCS_fitting(v, w, scores, indel, overlap = False):
	#indel is positive because it's supposed to be subtracted
	lv = len(v)
	lw = len(w)
	s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	backtrack = [[ "" for mm in range(lw+1)] for nn in range(lv+1)]
	s[0][0]=0
	for i in range(1,lv+1):
		s[i][0] = -i*indel
	for j in range(1,lw+1):
		s[0][j] = -j*indel

	global_max = 0
	global_i = lv
	global_j = lw

	for i in range(1,lv+1):
		for j in range(1,lw+1):
			(local_max_ind, local_max) = (0, -1000)
			arr = [s[i-1][j] - indel, s[i][j-1] - indel, s[i-1][j-1]+scores[(v[i-1],w[j-1])]]
			if j==1:
				arr.append(scores[(v[i-1],w[j-1])])
			for (ind, sc) in zip (range(len(arr)),arr):
				if sc >= local_max:
					local_max_ind = ind
					local_max = sc
			s[i][j] = local_max
			end_condition = ((not overlap) and j==lw) or (overlap and i==lv)
			if local_max>global_max and end_condition:
				global_max = local_max
				global_i = i
				global_j = j
				print global_max, global_i, global_j
			if local_max_ind == 0:
				backtrack[i][j]='|'
			if local_max_ind == 1:
				backtrack[i][j]='-'
			if local_max_ind == 2:
				backtrack[i][j] = '\\'
			if local_max_ind == 3:
				backtrack[i][j] = '*'
#	for (bb,ss) in zip(backtrack, s):
#		print "\t".join(["%s:%s" % (bbb,sss) for (bbb,sss) in zip(bb,ss)])
#	for r in backtrack:
#		print "\t".join(r)
#	for r in s:
#		print "\t".join([str(rr) for rr in r])
	print global_i, global_j
	return s[global_i][global_j], backtrack, global_i, global_j


def outputLCS(backtrack, v, w, i, j, fitting = False):
	acc = ""
	vv = ""
	ww = ""
	while True:
		if backtrack[i][j]=='*' and not fitting:
			return (acc, vv, ww)
		if i==0 or j==0:
			if i==0:
				ww = "".join(w[:j]) + ww
				vv = '-' * j + vv
			if j==0 and not fitting:
				vv = "".join(v[:i]) + vv
				ww = '-' * i + ww
			return (acc, vv, ww)
		if backtrack[i][j]=='|':
			i -=1
			vv = v[i] + vv
			ww = '-' + ww
			#outputLCS(backtrack, v, i-1, j)
			continue
		elif backtrack[i][j]=='-':
			j-=1
			vv = '-' + vv
			ww = w[j] + ww
			continue
			#outputLCS(backtrack, v, i, j-1)
		else:
			#outputLCS(backtrack, v, i-1, j-1)
			acc =v[i-1] + acc
			vv = v[i-1] + vv
			ww = w[j-1] + ww
			i-=1
			j-=1
			continue
