"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils as io
import bio.triee
import bio.cluster as cl

def eat_line(source):
    source.next()

def read_elements(source):
    return [p for p in source.next().split()]

def read_state_matrix(source):
    row_states = read_elements(source)
    probs = {state:{} for state in row_states}
    for line in source:
        elements = line.split()
        state, state_probs = elements[0], [float(p) for p in elements[1:]]
        probs[state] = {state:prob for (state, prob) in zip(row_states, state_probs)}
    return probs

def do_work(source):
    text = source.next()
    eat_line(source)
    states = read_elements(source)
    eat_line(source)
    probs = read_state_matrix(source)
    assert(probs.keys() == states)
    probs[''] = {state:0.5 for state in states}
    result = 1
    prev_state = ''
    for s in text:
        result *= probs[prev_state][s]
        prev_state = s

    return io.gen(result)

io.generate_input_output(do_work, False, True)
