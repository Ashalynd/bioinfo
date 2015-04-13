"""
Implement algorithms for finding frequent patterns using frequency array
"""
import bio.io_utils
import bio.triee

def do_work(source):
    text = source.next()
    t = bio.triee.trie()
    for s in source:
        t.append(s)
    positions = []
    current_pos = 0
    while text:
        out = t.match(text)
        if out: 
            positions.append(current_pos)
        text = text[1:]
        current_pos +=1
    return bio.io_utils.gen_array(positions)

bio.io_utils.generate_input_output(do_work, False)
