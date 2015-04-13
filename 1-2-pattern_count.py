"""
Implement PatternCount

Sample Input:
GCGCG
GCG
Sample Output:
2
"""

import bio.io_utils
import bio.pattern

text, pattern = bio.io_utils.read_input()[:2]
print "text: %s, pattern: %s" % (text, pattern)
count = bio.pattern.pattern_count(text, pattern)
print "count: %s" % count
