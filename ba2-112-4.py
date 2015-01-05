import sys
from collections import Counter
import math

minval = 57
maxval = 200

cyclos = {}
scores = {}

spectrum = Counter()
elements = []
leaderboard = [()]
leader_peptide = [()]
leader_score = 0
max_weight = None
N = 0
M = 0

#runs a convolution of spectrum to get M most frequent elements
def get_M(M, spectrum):
	allweights = Counter()

	l = len(spectrum)
	for i in xrange(1,l):
		for j in xrange(i):
			diff = spectrum[i]-spectrum[j]
			if diff>=minval and diff<=maxval:
				allweights[diff]+=1

	elements = []

	weight_counts = set(allweights.values())
	while len(elements)<M and len(weight_counts)>0:
		themax = max(weight_counts)
		elements+=([k for k in allweights if allweights[k]==themax])
		print elements
		print len(elements)
		weight_counts.remove(themax)
	return elements

#calculates cyclospectrum for the given peptide
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
		iw = [w for w in elements if w<=(max_weight-cur_weight)]
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


fname = sys.argv[1]
f = open(fname)
#M = int(f.readline().strip())
#N = int(f.readline().strip())
M = int(sys.argv[2])
N = int(sys.argv[3])
i_spectrum = []
f_spectrum = [float(p.strip()) for p in f.readline().strip().split()]
f_spectrum.sort()
for ff in f_spectrum[:-1]:
#	if ff-math.floor(ff)>0.5:
	i_spectrum.append(int(math.floor(ff)))
#	else:
	i_spectrum.append(int(math.floor(ff)-1))
ff = f_spectrum[-1]
#if ff-math.floor(ff)>0.5:
#	i_spectrum.append(int(math.ceil(ff)))
#else:
i_spectrum.append(int(math.floor(ff)))
i_spectrum.sort()
max_weight = i_spectrum[-1]
spectrum = Counter(i_spectrum)

print spectrum
print M
print N
print max_weight

elements = get_M(M, i_spectrum)

print elements

while len(leaderboard)>0:
	expand()

print leader_peptide
for p in leader_peptide:
	print "-".join([str(r) for r in p])