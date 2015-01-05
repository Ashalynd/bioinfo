import sys, fileinput, bioinfo

acc = ""
source = fileinput.input()

v = source.readline().strip()
w = source.readline().strip()
indel = 5

source.close()

scores = bioinfo.dummyScores(5,-3)
(score, backtrack) = bioinfo.LCS(v,w, scores, indel)
#print backtrack
(acc, vv, ww) = bioinfo.outputLCS(backtrack, v, w, len(v), len(w), True)
distance = sum([1 for (vvv,www) in zip(vv,ww) if (vvv!=www or vvv=='-' or www=='-')])
#print acc
print score
print vv
print ww
print distance