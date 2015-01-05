import sys, bioinfo, fileinput

source = fileinput.input()
text = source.readline().strip()
patterns = set()

trie = [{},{}]

#for line in source:
while True:
	line = source.readline()
	if not line:
		break
	pattern = line.strip()
	if pattern == 'Output:':
		break
	patterns.add(pattern)
	trie = bioinfo.build_trie(trie, pattern)

source.close()

bioinfo.print_trie(trie)
print patterns

nodes = bioinfo.tree_matching(trie, text, patterns)
print " ".join([str(n) for n in nodes])