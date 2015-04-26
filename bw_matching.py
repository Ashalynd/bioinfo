"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee
import bio.burrows_wheeler

def do_work(source):
    text = None
    patterns = None
    bwt_text = source.next()
    patterns = source.next().split()
    for s in source:
        continue
    print text, patterns
    results = []
#    bwt_text = bio.burrows_wheeler.bwt(text)
    for p in patterns:
        result = bio.burrows_wheeler.bwmatching(bwt_text, p)
        results.append(result)
    return bio.io_utils.gen_array(results)

bio.io_utils.generate_input_output(do_work, True, True)
