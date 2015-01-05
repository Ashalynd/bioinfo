import sys

word = sys.argv[1]

dict = {'A':'T','G':'C','T':'A','C':'G'}

addword = [dict[w] for w in word[::-1]]

print "".join(addword)