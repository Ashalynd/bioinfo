"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils as io
import bio.triee
import bio.cluster as cl
import math

def do_work(source):
    output = source.next()
    print "output", output
    io.eat_line(source)
    external_states = io.read_elements(source)
    print "external_states", external_states
    io.eat_line(source)
    states = io.read_elements(source)
    print "states", states
    io.eat_line(source)
    transition_probs = io.read_state_matrix(source)
    print "transition probs", transition_probs
#    assert(transition_probs.keys() == states)
    transition_probs[''] = {state:0.5 for state in states}
#    io.eat_line(source) - already done while reading transition probs
    emission_probs = io.read_state_matrix(source)
    print "emission probs", emission_probs
#    assert(emission_probs.keys() == states)

    matrix = [[None]*len(output) for s in states]
    text = ''

    for i, symbol in enumerate(output):
        print "matrix", matrix
        for j, s in enumerate(states):
            if i==0:
                matrix[j][i] = (math.log(transition_probs[''][s]) + math.log(emission_probs[s][symbol]),None)
            else:
                max_val = None
                max_state = None
                for (k,ks) in enumerate(states):
                    next_val = matrix[k][i-1][0]+math.log(transition_probs[ks][s])
                    if max_val is None or next_val>max_val:
                        max_val = next_val
                        max_state = k
                matrix[j][i] = (max_val + math.log(emission_probs[s][symbol]),max_state)

    max_val = None
    max_state = None
    last_val, last_state = max([(m[i], index) for (index, m) in enumerate(matrix)], key = lambda mm:mm[0][0])
    while i>=0:
        print "i", i, "last_val", last_val, "last_state", last_state
        text = states[last_state] + text
        last_val, last_state = matrix[last_state][i]
        i-=1

    return io.gen(text)

io.generate_input_output(do_work, False, True)
