import sys

weights_filename = "integer_mass_table.txt"

weights = {}

weight_counts = {0:1}
int_weights = set()

def get_weights():
	source_weights = open(weights_filename)
	for line in source_weights.readlines():
		(s, w) = line.strip().split()
		weights[s] = int(w)
		int_weights.add(int(w))


def count_peptides(weight):
	if weight<0:
		return 0
	if weight not in weight_counts:
#		weight_counts[weight] = sum([count_peptides(weight-v) for (k,v) in weights.iteritems()])
		weight_counts[weight] = sum([count_peptides(weight-v) for v in int_weights])
	return weight_counts[weight]
#	else cnt
#	if (weight==0):
#		return 1
#	elif (weight<0):
#		return 0


get_weights()
print int_weights
weight = int(sys.argv[1])

cnt = count_peptides(weight)
print weight, cnt
