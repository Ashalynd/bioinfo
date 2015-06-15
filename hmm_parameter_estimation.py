"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils as io
import bio.triee
import bio.cluster as cl
import math

def gen_matrices(states, external_states, transition_probs, emission_probs, delim = '\t'):
    yield delim+ io.stringify_array(states, delim)
    for i, s in enumerate(states):
        yield s+delim+ io.stringify_array_format(transition_probs[i], concat=delim, format='%.3f')
    yield('--------')
    yield delim + io.stringify_array(external_states, delim)
    for i, s in enumerate(states):
        yield s+ delim + io.stringify_array_format(emission_probs[i], concat=delim, format='%.3f')



def do_work(source):
    output = source.next()
    print "output", output
    io.eat_line(source)
    external_states = io.read_elements(source)
    print "external_states", external_states
    io.eat_line(source)
    hidden = source.next()
    print "hidden", hidden
    io.eat_line(source)
    states = io.read_elements(source)
    print "states", states
    transition_counts = {s:{ss:0.0 for ss in states} for s in states}
    emission_counts = {s:{es:0.0 for es in external_states} for s in states}

    print "transition_counts", transition_counts
    print "emission_counts", emission_counts

    transition_probs = [[0.0]*len(states) for s in states]
    emission_probs = [[0.0]*len(external_states) for s in states]
    prev_state = ''


    for (s, es) in zip(hidden, output):
        if es not in emission_counts[s]: emission_counts[s][es]=0
        emission_counts[s][es]+=1
        if prev_state in transition_counts: 
            if s not in transition_counts[prev_state]: transition_counts[prev_state][s] = 0
            transition_counts[prev_state][s]+=1
        prev_state = s

    print "transition_counts", transition_counts
    print "emission_counts", emission_counts

    for (i, s1) in enumerate(states):
        s_sum = sum([c for c in transition_counts[s1].values()])
        print "i",i, "s1", s1, "s_sum", s_sum
        if not s_sum:
            prob = 1./len(states)
            for (j, s2) in enumerate(states):
                transition_probs[i][j] = prob
        else:
            for (j, s2) in enumerate(states):                
                prob = transition_counts[s1][s2]
                s1_to_s2 = prob*1.0/s_sum
                transition_probs[i][j] = s1_to_s2

    for(i, s1) in enumerate(states):
        s_sum = sum([c for c in emission_counts[s1].values()])
        if not s_sum:
            prob = 1./len(external_states)
            for (j, o2) in enumerate(sorted(external_states)):
                emission_probs[i][j] = prob
        else:
            for (j, o2) in enumerate(sorted(external_states)):
                prob = emission_counts[s1][o2]
                s1_to_o2 = prob*1.0/s_sum
                emission_probs[i][j] = s1_to_o2

    print "transition_probs", transition_probs
    print "emission_probs", emission_probs

    return gen_matrices(states, external_states, transition_probs, emission_probs, ' ')

io.generate_input_output(do_work, False, True)
