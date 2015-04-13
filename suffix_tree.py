"""
Solve the Suffix Tree Construction Problem.
"""
import bio.io_utils
import bio.triee

def do_work(source):
    text = source.next()
    t = bio.triee.suffix_trie()
    t.preconstruct(text)
    print [tt for tt in t.emit()]
    paths = t.non_branching_paths()
    return t.emit_paths(paths, True)

bio.io_utils.generate_input_output(do_work, True)
