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
                matrix[j][i] = transition_probs[''][s]*emission_probs[s][symbol]
            else:
                sum_val = sum([matrix[k][i-1]*transition_probs[ks][s] for (k,ks) in enumerate(states)])
                matrix[j][i] = sum_val*emission_probs[s][symbol]

    sum_val = sum([matrix[k][i] for (k,s) in enumerate(states)])

    return io.gen(sum_val)

io.generate_input_output(do_work, False, True)
