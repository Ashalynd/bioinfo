"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee
import bio.burrows_wheeler

def do_work(source):
    text = None
    patterns = None
    text = source.next()+'$'
    patterns = [s for s in source]
    for s in source:
        continue
    bwt_text, suffix_array = bio.burrows_wheeler.bwt(text, True)
#    print text, patterns
    results = []
#    bwt_text = bio.burrows_wheeler.bwt(text)
    for p in patterns:
        result = bio.burrows_wheeler.bwmatching(bwt_text, p, suffix_array)
#        print "pattern", p, "result", result
        results.extend(result)
    results = sorted([str(s) for s in list(set(results))])
    return bio.io_utils.gen_array(results)

bio.io_utils.generate_input_output(do_work, False)
