import sys, fileinput

source = fileinput.input()

src = source.readline().strip()
num = source.readline().strip()

links = {}

backpointers = {}
backpointers[src]=(-1,0)

for line in source:
	if '->' not in line:
		break
	(link, weight) = line.strip().split(':')
	weight = int(weight)
	(start, end) = link.split('->')
	print start, end, weight
	if start not in links:
		links[start]= {"in":[],"out":[]}
	if end not in links:
		links[end] = {"in":[],"out":[]}
	links[start]["out"].append((end,weight))
	links[end]["in"].append((start, weight))

print src, num

print links

queue = [src]
last = 0
maxpath = 0

while len(queue)>0:
	next = queue[-1]
	queue = queue[:-1]
	if backpointers[next][1]>maxpath:
		last = next
		maxpath = backpointers[next][1]
	thelinks = links[next]["out"]
	for (l,w) in thelinks:
		dist = w+backpointers[next][1]
		if l not in backpointers or backpointers[l][1]<dist:
			backpointers[l]=(next,dist)
			queue.append(l)

print last, maxpath

last = num
print backpointers[last]

backtrack = [last]
while last!=src:
	last = backpointers[last][0]
	backtrack.append(last)

backtrack.reverse()
print backtrack

print "->".join([str(l) for l in backtrack])