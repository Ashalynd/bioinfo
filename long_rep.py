import bio.io_utils
import bio.triee

def do_work(source):
    text = source.next()
    text+='$'
    t = bio.triee.suffix_trie()
    t.preconstruct(text)
    te = bio.triee.suffix_tree()
    te.from_trie(t)
    result = [te.longest_repeat()]
    return bio.io_utils.gen_array(result)

bio.io_utils.generate_input_output(do_work, False)