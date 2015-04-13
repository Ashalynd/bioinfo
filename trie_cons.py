"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee

def do_work(source):
    t = bio.triee.trie()
    for s in source:
        t.append(s)
    return t.emit()

bio.io_utils.generate_input_output(do_work, True)
