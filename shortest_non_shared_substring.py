"""
Solve the Suffix Tree Construction Problem.
"""
import bio.io_utils
import bio.triee

def all_variants(text, resultset):
    for i in range(len(text)):
        for j in range(i+1, len(text)):
            resultset.add(text[i:j])


def do_work(source):
    text1 = source.next()
    text2 = source.next()
    for s in source: pass # eat source
    t = bio.triee.suffix_trie()
    t.construct(text1 + '#' + text2 + '$')
    tt = bio.triee.suffix_tree()
    tt.from_trie(t)
#    print tt.text
    repeats = tt.all_repeats(True)
    print "repeats", repeats
    all_repeats = set()
    all_repeats.update(repeats)
    for rep in repeats: all_variants(rep, all_repeats)
    print "all_repeats", all_repeats
    uniques = tt.all_uniques(bio.triee.constants.BLUE)
    new_uniques = set()
    for elem in uniques:
        hashpos = elem.find('#')
        new_elem = elem[:hashpos] if hashpos>=0 else elem
        if not new_elem: continue
        all_variants(new_elem, new_uniques)
#    print "new_uniques", new_uniques
    new_uniques = new_uniques.difference(all_repeats)
    new_uniques = sorted(list(new_uniques), key = lambda elem: len(elem))
    print "new_new_uniques", new_uniques[:100]
    return bio.io_utils.gen(new_uniques[0])

bio.io_utils.generate_input_output(do_work, False, False)
