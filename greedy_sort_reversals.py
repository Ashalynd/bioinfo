import sys, fileinput

def output(an_input):
	print "(%s)" % (" ".join([("+%s" % d ) if d>0 else str(d) for d in an_input]))

source = fileinput.input()
the_input = [int(dd) for dd in source.readline().strip()[1:-1].split()]

source.close()
#print the_input

k = 0
P = len(the_input)
approxReversalDistance = 0

while k<P:
#	print k, the_input[k]
	if abs(the_input[k])!=k+1:
		ke = k
		while abs(the_input[ke])!=k+1:
			ke+=1
		the_input[k:ke+1] = [-ki for ki in the_input[k:ke+1][::-1]]
		approxReversalDistance +=1
		output(the_input)
	if the_input[k]==-(k+1):
		the_input[k] = (k+1)
		approxReversalDistance +=1
		output(the_input)
	k+=1

print k, approxReversalDistance