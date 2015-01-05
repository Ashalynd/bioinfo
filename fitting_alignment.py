import sys, fileinput, bioinfo

acc = ""
source = fileinput.input()

v = source.readline().strip()
w = source.readline().strip()
indel = 1

source.close()

scores = bioinfo.dummyScores(1,-1)
#print scores
(score, backtrack, global_i, global_j) = bioinfo.LCS_fitting(v,w, scores, indel)
#print backtrack
(acc, vv, ww) = bioinfo.outputLCS(backtrack, v, w, global_i, global_j, True)
#print acc
print score
print vv
print ww