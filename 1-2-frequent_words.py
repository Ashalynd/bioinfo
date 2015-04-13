"""
Solve the Frequent Words Problem.
     Input: A string Text and an integer k.
     Output: All most frequent k-mers in Text.

Sample Input:
     ACGTTGCATGTCGCATGATGCATGAGAGCT
     4

Sample Output:
     CATG GCAT
"""

import bio.io_utils
import bio.pattern

text, k = bio.io_utils.read_input()[:2]
k = int(k)
print "text: %s, f: %s" % (text, k)
kmers = {}
search_len = len(text)-k+1
max_count = 0
for i in xrange(search_len):
    pattern = text[i:k+i]
    if not pattern in kmers:
        count = bio.pattern.pattern_count(text[i:], pattern)
        if max_count<count: max_count = count
        kmers[pattern] = count
result = [kmer for kmer in kmers if kmers[kmer]==max_count]
bio.io_utils.emit_array(result)
