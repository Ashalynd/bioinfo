"""
Find all occurrences of a pattern in a string.
     Input: Two strings, Pattern and Genome.
     Output: All starting positions where Pattern appears as a substring of Genome.

If genome is stored separately, should be called like that:
python 1-3-pattern_matching.py <(echo 'CTTGATCAT' && cat data/Vibrio_cholerae.txt)
"""
import bio.io_utils

pattern, genome = bio.io_utils.read_input()

index = -1
index=genome.find(pattern,index+1)
a = []
while index>=0:
	a.append(index)
	index = genome.find(pattern,index+1)

bio.io_utils.emit_or_compare(sorted(a))