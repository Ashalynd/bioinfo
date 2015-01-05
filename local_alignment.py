import sys, fileinput, bioinfo

acc = ""
source = fileinput.input()

v = source.readline().strip()
w = source.readline().strip()
indel = 5

source.close()

blosum = bioinfo.readScores("PAM250_1.txt")
(score, backtrack, global_i, global_j) = bioinfo.LCS_local(v,w, blosum, indel)
#print backtrack
(acc, vv, ww) = bioinfo.outputLCS(backtrack, v, w, global_i, global_j)
#print acc
print score
print vv
print ww