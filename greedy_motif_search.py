import sys

fname = sys.argv[1]
letters = ['A','C','G','T']
let_pos = {l:i for (i,l) in enumerate(letters)}
dna = []
ldna = 0
k = 0
t = 0

best_motifs = []
best_score = 0
best_line_score = 0
consensus = ""

def score(motifs):
	t_factor = 1.0/len(motifs)

	maxes = [[0.0 for l in letters] for i in range(k)]
	for motif in motifs:
		print motif
		for (i,m) in enumerate(motif):
			print i,m
			maxes[i][let_pos[m]]+=t_factor
		print maxes
	consensus = ""
	print motifs
	print maxes
	for (i,m) in enumerate(maxes):
		print m
		cur_letter = "A"
		cur_prob = m[0]
		for (j,prob) in enumerate(m):
			print cur_letter, cur_prob, j, prob
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
	print "score",motifs, score, partial_score, consensus
	return (score, partial_score, consensus)

def make_profile(motifs):
	t_factor = 1.0/len(motifs)
	profile = {l:[0.0]*k for l in letters}
	for motif in motifs:
		for (i,m) in enumerate(motif):
			profile[m][i]+=t_factor
	return profile

def find_best_pattern(thedna, profile):
	print "find_best_pattern", thedna, profile
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

	print "best_prob",best_prob
	print "best_pattern",best_pattern, thedna
	return (best_pattern, best_prob)

f = open(fname)

(k, t) = [int(t) for t in f.readline().strip().split()]


for i in range(t):
	dna.append(f.readline().strip())

f.close()

ldna = len(dna[0])-k+1

best_motifs = [thedna[:k] for thedna in dna]
(best_score, best_line_score, consensus) = score(best_motifs)

print best_motifs

print make_profile(best_motifs[:1])
print best_score, best_line_score, consensus

for i in range(ldna):
	cur_motifs = [dna[0][i:i+k]]

	for thedna in dna[1:]:
		print "cur_motifs",cur_motifs
		profile = make_profile(cur_motifs)
		print "profile",profile
		(best_pattern, best_prob) = find_best_pattern(thedna, profile)
		print thedna, best_pattern, best_prob
		cur_motifs.append(best_pattern[0])

	(next_best_score, next_line_score, next_consensus) = score(cur_motifs)
	print "next_best_score", next_best_score, "best_score", best_score, "line_score", next_line_score
	if next_best_score< best_score: # or next_best_score==best_score and best_line_score>next_line_score:
		print "!", next_best_score, next_consensus
		best_score = next_best_score
		best_line_score = next_line_score
		consensus = next_consensus
		best_motifs = cur_motifs

print best_score, best_line_score, consensus
print best_motifs
for m in best_motifs:
	print m