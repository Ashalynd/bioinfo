"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee
import bio.burrows_wheeler as bw

def do_work(source):
    text = None
    patterns = None
    text = source.next()
    patterns = source.next().split()
    counts, letter_places = bw.count(text)
    for s in source:
        continue
    results = map(lambda p: bw.better_bwmatching(text, p, counts, letter_places), patterns)
    return bio.io_utils.gen_array(results)

bio.io_utils.generate_input_output(do_work, True, True)
