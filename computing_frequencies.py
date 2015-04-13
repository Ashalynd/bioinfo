"""
 Implement ComputingFrequencies to generate a frequency array.
    Input: A DNA string Text followed by an integer k.
    Output: FrequencyArray(Text).
"""
import bio.io_utils
import bio.pattern

text, k = bio.io_utils.read_input()[:2]

k = int(k)
frequency_array = bio.pattern.frequency_array(text, k)

if bio.io_utils.has_output():
    print bio.io_utils.output
    print bio.io_utils.compare_with_output(frequency_array)
else:
    bio.io_utils.emit_array(frequency_array)