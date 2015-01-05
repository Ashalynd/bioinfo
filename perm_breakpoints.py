import sys, fileinput, bioinfo

source = fileinput.input()
the_input = bioinfo.read_permutation(source)
source.close()

print the_input

P = len(the_input)
k = 1
breakpoints = (0 if the_input[0]==1 else 1)
start_k = 0
sign_k = (-1 if the_input[start_k]<0 else 1)
while k<P:
	if (the_input[k]-the_input[start_k])!=(k-start_k)*sign_k:
		breakpoints+=1
		print start_k, k, the_input[k], breakpoints
		start_k=k
	k+=1
if the_input[P-1]!= P:
	breakpoints+=1
print breakpoints
