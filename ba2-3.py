import sys

dictname = "RNA_codon_table_1.txt"
fname = sys.argv[1]
fresname = (fname.split())[0]+".res.txt"

rdict = {}

rdict_file = open(dictname)

for line in rdict_file.readlines():
	ss = line.strip().split()
	ss += [''] * (2-len(ss))
	rdict[ss[0]]=ss[1]

print rdict

source = open(fname)
target = open(fresname,"w")
triplet = source.read(3)
while triplet!='':
	result = rdict[triplet]
	target.write(result)
	sys.stdout.write(result)
	triplet = source.read(3).strip()

sys.stdout.write("\n")
source.close()
target.close()

