"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee
import bio.burrows_wheeler

def do_work(source):
    text = None
    patterns = None
    text = source.next()
    patterns = source.next().split()
    for s in source:
        continue
#    print text, patterns
    results = []
    text = bio.burrows_wheeler.reverse_bwt(text)
    for p in patterns:
        count = 0
        first_index = -1
        first_index = text.find(p)
        while first_index>=0:
            count+=1
            first_index = text.find(p, first_index+1)
        results.append(count)
    return bio.io_utils.gen_array(results)

bio.io_utils.generate_input_output(do_work, True, True)
