"""
Solve the Suffix Tree Construction Problem.
"""
import bio.io_utils
import bio.triee

def read_int_cs_list(source):
    return [int(p.strip()) for p in source.next().split(',')]

def do_work(source):
    text = source.next()
    suffix_array = read_int_cs_list(source)
    lcp = read_int_cs_list(source)
    for s in source: pass # eat source
    t = bio.triee.suffix_tree()
    t.from_suffix_array(text, suffix_array, lcp)
    return t.emit_edges_as_text()

bio.io_utils.generate_input_output(do_work, True, True)
