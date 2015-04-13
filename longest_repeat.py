"""
Find the longest repeat in the text, using suffix tree.
"""

import bio.io_utils
import bio.triee

def do_work(source):
    text = ''
    for s in source:
        text.append(s)
    print "text", text
#    t = bio.triee.suffix_trie()
#    t.preconstruct(text)
#    te = bio.triee.suffix_tree()
#    te.from_trie(t)
    yield '!!!'
#        yield te.longest_repeat()

bio.io_utils.generate_input_output(do_work, False)