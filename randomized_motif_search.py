import sys, random

fname = sys.argv[1]
letters = ['A','C','G','T']
let_pos = {l:i for (i,l) in enumerate(letters)}
dna = []
ldna = 0
k = 0
t = 0
N = 1000

best_motifs = []
best_score = 0
best_line_score = 0
consensus = ""

def score(motifs):
	t_factor = 1.0/(len(motifs)+4)

	maxes = [[t_factor for l in letters] for i in range(k)]
	for motif in motifs:
#		print motif
		for (i,m) in enumerate(motif):
#			print i,m
			maxes[i][let_pos[m]]+=t_factor
#		print maxes
	consensus = ""
#	print motifs
#	print maxes
	for (i,m) in enumerate(maxes):
#		print m
		cur_letter = "A"
		cur_prob = m[0]
		for (j,prob) in enumerate(m):
#			print cur_letter, cur_prob, j, prob
			if prob>cur_prob:
				cur_letter = letters[j]
				cur_prob = prob
		consensus+=cur_letter
	score = 0
	partial_score = 0
	for motif in motifs:
		the_score = 0
		for (i,m) in enumerate(motif):
			the_score += (m!=consensus[i])
		if the_score > partial_score:
			partial_score = the_score
		score += the_score
#	print "score",motifs, score, partial_score, consensus
	return (score, partial_score, consensus)

def make_profile(motifs):
	t_factor = 1.0/(len(motifs)+4)
	profile = {l:[t_factor]*k for l in letters}
	for motif in motifs:
		for (i,m) in enumerate(motif):
			profile[m][i]+=t_factor
	return profile

def find_best_pattern(thedna, profile):
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

#	print "best_prob",best_prob
#	print "best_pattern",best_pattern, thedna
	return (best_pattern, best_prob)

f = open(fname)

(k, t) = [int(t) for t in f.readline().strip().split()]


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

(best_score, best_line_score, consensus) = score(best_motifs)

profile = make_profile(best_motifs)
print "profile",profile
print best_score, best_line_score, consensus


print "START"

for n in range(N):

	cur_motifs = []
	for thedna in dna:
		rstart = random.randint(0, ldna-1)
		cur_motifs.append(thedna[rstart:(rstart+k)])
	
	(cur_score, cur_line_score, cur_consensus) = score(cur_motifs)
	print "***", cur_score, cur_consensus, cur_motifs
	previous_best_score = cur_score
	can_recycle = True
	while can_recycle:
		profile = make_profile(cur_motifs)

		cur_motifs = []
		for thedna in dna:
#			print "cur_motifs",cur_motifs
			(best_pattern, best_prob) = find_best_pattern(thedna, profile)
#			print thedna, best_pattern, best_prob
			cur_motifs.append(best_pattern[0])

		(next_best_score, next_line_score, next_consensus) = score(cur_motifs)
#		print "next_best_score", next_best_score, "best_score", best_score, "line_score", next_line_score
		if next_best_score< best_score: # or next_best_score==best_score and best_line_score>next_line_score:
			print "!", next_best_score, next_consensus, cur_motifs
			best_score = next_best_score
			best_line_score = next_line_score
			consensus = next_consensus
			best_motifs = cur_motifs
		else:
			can_recycle = previous_best_score > next_best_score
		previous_best_score = next_best_score

print best_score, best_line_score, consensus
print best_motifs
for m in best_motifs:
	print m