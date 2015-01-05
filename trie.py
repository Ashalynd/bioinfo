import fileinput, sys, bioinfo

source = fileinput.input()

trie = [{},{}]

for line in source:
	if line.strip() == 'Output:':
		break
	trie = bioinfo.build_trie(trie, line.strip())

source.close()

#print trie

bioinfo.print_trie(trie)