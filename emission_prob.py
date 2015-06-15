"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils as io
import bio.triee
import bio.cluster as cl

def do_work(source):
    output = source.next()
    io.eat_line(source)
    external_states = io.read_elements(source)
    io.eat_line(source)
    text = source.next()
    io.eat_line(source)
    states = io.read_elements(source)
    io.eat_line(source)
    probs = io.read_state_matrix(source)
    print "probs", probs
    assert(probs.keys() == states)
    probs[''] = {state:0.5 for state in states}
    result = 1
    for (state, output) in zip(text, output):
        print state, output, probs[state][output], result
        result *= probs[state][output]

    return io.gen(result)

io.generate_input_output(do_work, False, True)
