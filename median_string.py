import sys
import bio.io_utils

letters = ['A','C','G','T']

k = 0
ldna = 0
pattern = []
dna = []

best_pattern = []
best_score = 0

def shift(s):
	if s==[3]*k:
		return False
	index = k-1
	while index>=0:
		if s[index]<3:
			s[index]+=1
			return s
		else:
			s[index]=0
			index-=1
	return False

def makestring(s):
	return "".join([letters[ss] for ss in s])

def diff(pat):
	global best_score
	global best_pattern
#	print pat
	score = 0
	for thedna in dna:
		l_best_score = k #best score in the given line
		for i in range(ldna-k+1):
			thescore = 0 #score on the given position
			for j in range(k):
				thescore+=(thedna[i+j]!=pat[j])
				if thescore>l_best_score:
					break
			if thescore<l_best_score:
				l_best_score = thescore
		score+=l_best_score
		if score>best_score:
			return
#	print pat, score
	if score == best_score:
		best_pattern.append(pat)
	if score < best_score:
		best_pattern = [pat]
		best_score = score
		print pat, best_score



#fname = sys.argv[1]

#f = open(fname)

#k = int(f.readline().strip())

#dna = [l.strip() for l in f.readlines()]
input = bio.io_utils.read_input()

dna = input[1:]
k = int(input[0])

print k
print dna

ldna = len(dna[0])
pattern = [0]*k
best_score = k*len(dna)

#sss = shift([1,2,3])
#print sss, makestring(sss)
#print shift([3,3,3])
#sss = shift([3,1,3])
#print sss, makestring(sss)
#sss = shift([3,3,0])
#print sss, makestring(sss)

while pattern:
	pat = makestring(pattern)
	diff(pat)
	pattern = shift(pattern)

print best_score
print best_pattern

