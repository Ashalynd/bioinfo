"""
Solve the Suffix Tree Construction Problem.
"""
import bio.io_utils
import bio.triee

def do_work(source):
    text = source.next()
    for s in source: pass # eat source
    t = bio.triee.suffix_trie()
#    print "text", text
    t.construct(text + '$')
    tt = bio.triee.suffix_tree()
    tt.from_trie(t)
#    print tt.text
    return bio.io_utils.gen(tt.longest_repeat())

bio.io_utils.generate_input_output(do_work, False)
