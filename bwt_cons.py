"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee
import bio.burrows_wheeler

def do_work(source):
    text = None
    for s in source:
        if not text: text = s
    bwt_text = bio.burrows_wheeler.bwt(text)
    return bio.io_utils.gen(bwt_text)

bio.io_utils.generate_input_output(do_work, True, True)
