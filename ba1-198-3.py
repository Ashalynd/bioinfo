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

path = bio.io_utils.read_input()
output = path[0]
for p in path[1:]:
    output+= p[-1]
print output