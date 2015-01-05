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
		print i, snippet[3*i:3*(i+1)],p_dict[pep[i]]
		if snippet[3*i:3*(i+1)] not in p_dict[pep[i]]:
			return False
	return True

read_rdict(dictname)

fname = sys.argv[1]
source = open(fname)

peptide = sys.argv[2]
r_peptide = peptide[::-1]
len_pep = len(peptide)
len_snippet = len_pep*3

#dna = source.readline().strip()


peptide_dict = dict([(aa,set([k for k,v in dna_dict.items() if v==aa])) for aa in set(peptide)])
r_peptide_dict = dict([(aa,set([k for k,v in dna_rdict.items() if v==aa])) for aa in set(peptide)])

print peptide_dict
print r_peptide_dict

prevline = ''

while 1:
	if len(prevline)<len_snippet:
		line = source.readline().strip()
		prevline += line
	if len(prevline)<len_snippet:
		break
	snippet = prevline[:len_snippet]
	if check_snippet(snippet, peptide, peptide_dict) or check_snippet(snippet, r_peptide, r_peptide_dict):
		dna_snippets.append(snippet)
		print snippet
	prevline = prevline[1:]


for snippet in dna_snippets:
	print snippet
print len(dna_snippets)