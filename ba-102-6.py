import sys
from collections import Counter

weights_filename = "integer_mass_table.txt"

int_weights = set()
spectrum = Counter()

leaderboard = [()]
leader_peptide = [()]
leader_score = 0
max_weight = None
scores = set()
N = 0

cyclos = {}
scores = {}

def verify_peptide(peptide):
	len_peptide = len(peptide)

	all_weights = Counter([0, sum(peptide)])

	peptide += peptide 

	for i in xrange(len_peptide):
		for j in xrange(len_peptide-1):
			nextone = sum(peptide[i:i+j+1])
			all_weights[nextone]+=1
	return all_weights

def get_cyclospectrum(peptide):
	if not peptide in cyclos:
		cyclos[peptide] = verify_peptide(peptide)
	return cyclos[peptide]

def score(pep):
	#print "score",pep
	ri = len(pep)
	for i in range(ri):
		cp = pep[i:]+pep[:i]
		if cp in scores:
			return scores[cp]
	score = 0
	cs = get_cyclospectrum(pep)
	for p in spectrum.keys():
		score+=min(spectrum[p],cs[p])
	scores[pep] = score
	return score

def get_weights():
	source_weights = open(weights_filename)
	for line in source_weights.readlines():
		(s, w) = line.strip().split()
		int_weights.add(int(w))

def expand():
	next_leaderboard = []
	next_scores = set()
	global leader_score
	global N
	global leaderboard
	global leader_peptide
	global max_weight
	print "expand",len(leaderboard), max_weight, max([sum(l) for l in leaderboard])
	for l in leaderboard:
		cur_weight = sum(l)
		iw = [w for w in int_weights if w<=(max_weight-cur_weight)]
		for w in iw:
			theweight = cur_weight+w
		#	print theweight, max_weight
			if theweight <= max_weight:
				curmem = l+(w,)
				curscore = score(curmem)
				next_leaderboard.append(curmem)
				next_scores.add(curscore)
		#		print next_scores
				if theweight == max_weight:
					if curscore>leader_score:
						leader_peptide = [curmem]
						leader_score = curscore
					elif curscore == leader_score:
						leader_peptide.append(curmem)
						print "leader_peptides", leader_peptide, leader_score
#	print "expanded",next_leaderboard
	scores = set()
	leaderboard = []
	while len(next_scores)>0 and len(leaderboard)<N:
#	for i in range(min(N, len(next_scores))):
#		print "i",i
		themax = max(next_scores)
		if (themax>0):
			scores.add(themax)
		next_scores.remove(themax)
#		print scores
		leaderboard +=[l for l in next_leaderboard if score(l) == themax]
		print leaderboard
#	print "cut", leaderboard


N = int(sys.argv[1])
fname = sys.argv[2]

f = open(fname)
spectrum = Counter([int(s.strip()) for s in f.read().strip().split()])
max_weight = max(spectrum.keys())

get_weights()

print N
print spectrum
print max_weight

while len(leaderboard)>0:
	expand()

print leader_peptide
for p in leader_peptide:
	print "-".join([str(r) for r in p])
