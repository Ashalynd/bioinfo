import sys

comp_dict = {'A':'T','G':'C','T':'A','C':'G'}
dictname = "RNA_codon_table_1.txt"

rdict = {}
dna_dict = {}
dna_rdict = {}

dna_snippets = []
peptide = ''
r_peptide = ''
len_pep = 0
peptide_dict = []
r_peptide_dict = []

def read_rdict(dictname):
	rdict_file = open(dictname)
	for line in rdict_file.readlines():
		ss = line.strip().split()
		ss += [''] * (2-len(ss))
		rdict[ss[0]]=ss[1]
		dnacodon = ss[0].replace("U","T")
		dna_dict[dnacodon] = ss[1]
		dna_rdict[complement(dnacodon)] = ss[1]

def complement(word):
	addword = [comp_dict[w] for w in word[::-1]]
	return "".join(addword)

def check_snippet(snippet, pep, p_dict):
#	print "check_snippet", snippet, pep, p_dict
	for i in xrange(len_pep):
#		print i, snippet[3*i:3*(i+1)]
		if snippet[3*i:3*(i+1)] not in p_dict[pep[i]]:
			return False
	return True

read_rdict(dictname)

fname = sys.argv[1]
source = open(fname)

dna = source.readline().strip()
if len(sys.argv)>2:
	peptide = sys.argv[2]
else:
	peptide = source.readline().strip()

print peptide 

r_peptide = peptide[::-1]
len_pep = len(peptide)
len_snippet = len_pep*3

peptide_dict = dict([(aa,set([k for k,v in dna_dict.items() if v==aa])) for aa in set(peptide)])
r_peptide_dict = dict([(aa,set([k for k,v in dna_rdict.items() if v==aa])) for aa in set(peptide)])

print peptide_dict
print r_peptide_dict


len_dna_check = len(dna)-len(peptide)*3+1
for i in xrange(len_dna_check):
	snippet = dna[i:(i+len_snippet)]
	if check_snippet(snippet, peptide, peptide_dict) or check_snippet(snippet, r_peptide, r_peptide_dict):
		dna_snippets.append(snippet)

for snippet in dna_snippets:
	print snippet
print len(dna_snippets)