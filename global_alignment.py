import sys, fileinput, bioinfo

acc = ""
source = fileinput.input()

v = source.readline().strip()
w = source.readline().strip()
indel = 5

source.close()

blosum = bioinfo.readBlosum()
(score, backtrack) = bioinfo.LCS(v,w, blosum, indel)
#print backtrack
(acc, vv, ww) = bioinfo.outputLCS(backtrack, v, w, len(v), len(w))
#print acc
print score
print vv
print ww