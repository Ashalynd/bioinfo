import sys, random
from bisect import bisect_left

fname = sys.argv[1]
letters = ['A','C','G','T']
let_pos = {l:i for (i,l) in enumerate(letters)}
dna = []
ldna = 0
k = 0
t = 0
N = 0
M = 20

best_motifs = []
best_score = 0
consensus = ""

# calculates the score (deviation from a stable pattern) for a combination of motifs with laplacian pseudocounts
def score(motifs):
	t_factor = 1.0/(len(motifs)+4)

	maxes = [[t_factor for l in letters] for i in range(k)]
	for motif in motifs:
		for (i,m) in enumerate(motif):
			maxes[i][let_pos[m]]+=t_factor
	consensus = ""
	for (i,m) in enumerate(maxes):
		#find the letter that is encountered most
		cur_letter = "A"
		cur_prob = m[0]
		for (j,prob) in enumerate(m):
			if prob>cur_prob:
				cur_letter = letters[j]
				cur_prob = prob
		consensus+=cur_letter
	score = 0
	for motif in motifs:
		the_score = 0
		for (i,m) in enumerate(motif):
			the_score += (m!=consensus[i])
		score += the_score
	return (score, consensus)

def make_profile(motifs):
	t_factor = 1.0/(len(motifs)+4)
	profile = {l:[t_factor]*k for l in letters}
	for motif in motifs:
		for (i,m) in enumerate(motif):
			profile[m][i]+=t_factor
	return profile

def find_best_pattern(thedna, profile):
#   finds best pattern in the given string, according to the given profile
#	print "find_best_pattern", thedna, profile
	best_prob = 0.0
	best_pattern = []

	for i in range(ldna):
		prob = 1.0
		for j in range(k):
			prob *= profile[thedna[i+j]][j]
			if (prob==0 or prob<best_prob):
				break
		if prob==best_prob:
			best_pattern.append(thedna[i:i+k])
		if prob>best_prob:
			best_prob = prob
			best_pattern = [thedna[i:i+k]]

	return (best_pattern, best_prob)


def find_probs(thedna, profile):
	probs = {thedna[i:i+k]:1.0 for i in range(ldna)}
	for prob in probs:
		for (i,p) in enumerate(prob):
			probs[prob] *= profile[p][i]
	the_factor = sum(probs.values())
	
	problist = []
	prev_prob = 0.0
	for prob in probs:
		next_prob = prev_prob + probs[prob]/the_factor
		prev_prob = next_prob
		problist.append((next_prob, prob))
	return problist

def find_random_element(problist):
	r = random.random()
#	print "r:",r
	prob_indexes = map(lambda ll:ll[0],problist)
	kmer_index = bisect_left(prob_indexes, r)
	return problist[kmer_index][1]

f = open(fname)

(k, t, N) = [int(t) for t in f.readline().strip().split()]


for i in range(t):
	dna.append(f.readline().strip())

f.close()

ldna = len(dna[0])-k+1
 
best_motifs = []

best_motifs = []
random_motifs = []
for thedna in dna:
	rstart = random.randint(0, ldna-1)
	best_motifs.append(thedna[rstart:(rstart+k)])
print "best_motifs",best_motifs

(best_score, consensus) = score(best_motifs)

profile = make_profile(best_motifs)
print "profile",profile
print best_score, consensus

probs = find_probs(dna[0],profile)
print probs
print find_random_element(probs)


print "START"

for m in range(M):

	random_motifs = []
	for thedna in dna:
		rstart = random.randint(0, ldna-1)
		random_motifs.append(thedna[rstart:(rstart+k)])

	cur_motifs = random_motifs

	for n in range(N):

		j = random.randint(0,t-1)
		cur_profile = make_profile(cur_motifs[:j]+cur_motifs[(j+1):])
		cur_probs = find_probs(dna[j], cur_profile)
		cur_motif = find_random_element(cur_probs)
		cur_motifs = cur_motifs[:j]+[cur_motif]+cur_motifs[(j+1):]

		(cur_score, cur_consensus) = score(cur_motifs)
		print "***", cur_score, cur_consensus, cur_motifs

		if cur_score<best_score:
			print "!", cur_score, cur_consensus, cur_motifs
			best_score = cur_score
			consensus = cur_consensus
			best_motifs = cur_motifs

print best_score, consensus
print best_motifs
for m in best_motifs:
	print m