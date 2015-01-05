import sys, fileinput

acc = ""


def LCS(v, w):
	lv = len(v)
	lw = len(w)
	s = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	backtrack = [[ None for mm in range(lw+1)] for nn in range(lv+1)]
	for i in range(lv+1):
		s[i][0] = 0
	for j in range(lw+1):
		s[0][j] = 0
	for i in range(1,lv+1):
		for j in range(1,lw+1):
			s[i][j] = max(s[i-1][j], s[i][j-1], s[i-1][j-1]+(1 if v[i-1]==w[j-1] else 0))
			if s[i][j]==s[i][j-1]:
				backtrack[i][j]='-'
			if s[i][j]==s[i-1][j-1]:
				backtrack[i][j]='\\'
			if s[i][j]==s[i-1][j]:
				backtrack[i][j] = '|'
	return s[lv][lw], backtrack

def outputLCS(backtrack, v, i, j):
	global acc
	while True:
		if i==0 or j==0:
			return
		if backtrack[i][j]=='|':
			i -=1
			#outputLCS(backtrack, v, i-1, j)
			continue
		elif backtrack[i][j]=='-':
			j-=1
			continue
			#outputLCS(backtrack, v, i, j-1)
		else:
			#outputLCS(backtrack, v, i-1, j-1)
			acc = v[i-1]+acc
			i-=1
			j-=1
			continue

source = fileinput.input()

v = source.readline().strip()
w = source.readline().strip()

source.close()

(s, backtrack) = LCS(v,w)
print s
print backtrack
outputLCS(backtrack, v, len(v), len(w))
print acc