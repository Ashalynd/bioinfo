"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.pattern

text, k = bio.io_utils.read_input()[:2]

k = int(k)
max_len = 4**k
frequent_patterns = set()
frequency_array = bio.pattern.frequency_array(text, k)
max_count = max(frequency_array)
for i in xrange(max_len):
    if frequency_array[i]==max_count:
        pattern = bio.pattern.number_to_pattern(i, k)
        frequent_patterns.add(pattern)

result = sorted(list(frequent_patterns))

if bio.io_utils.has_output():
    print bio.io_utils.compare_with_output(result)
else:
    bio.io_utils.emit_array(result)