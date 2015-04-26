"""
Construct the suffix array of a string.
"""
import bio.io_utils
import bio.triee

def do_work(source):
    text = None
    for s in source:
        if not text: text = s
    len_text = len(text)
    suffixes = sorted([text[i:] for i in xrange(len_text)])
    lens = [len_text-len(entry) for entry in suffixes]
    return bio.io_utils.gen_array(lens, ', ')

bio.io_utils.generate_input_output(do_work, True)
