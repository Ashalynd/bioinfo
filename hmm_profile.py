"""
Solve the Profile HMM Problem.
"""

import bio.io_utils as io
import bio.triee
import bio.cluster as cl
import math

def choose_state(symbol, prev_index, index):
    if symbol=='-':
        return '' if index==prev_index else 'D%s' % index
    else:
        return 'I%s' % index if index==prev_index else 'M%s' % index

def do_work(source):
    # read input
    theta = float(source.next())
    io.eat_line(source)
    external_states = io.read_elements(source)
    io.eat_line(source)
    items = [item for item in source]
    num_items = len(items)
    threshold = theta * num_items
    prof_len = len(items[0])
    # filter out columns with too many deletions
    col_nums = []
    for i in xrange(prof_len):
        col = [item[i] for item in items]
        num_del = col.count('-')
        if num_del<threshold: col_nums.append(i)
    filtered_len = len(col_nums)
    # initialize states
    states = ['S', 'I0']
    for i in xrange(filtered_len):
        states+=['M%s' % (i+1), 'D%s' % (i+1), 'I%s' % (i+1)]
    states +=['E']

    # precalculate indices
    states_indices = {s:i for (i,s) in enumerate(states)}
    external_states_indices = {s:i for (i,s) in enumerate(external_states)}

    transition_counts = [[0]*len(states) for s in states]
    emission_counts = [[0]*len(external_states) for s in states]
    transition_probs = [[0.0]*len(states) for s in states]
    emission_probs = [[0.0]*len(external_states) for s in states]
    prev_col_state = ['S' for item in xrange(num_items)]
    index = 0
    prev_index = 0
    for i in xrange(prof_len):
        next_col = [item[i] for item in items]
        if index<filtered_len and col_nums[index]==i: index+=1
        next_col_state = map(lambda x:choose_state(x, prev_index, index), next_col)
        for (prev, next) in zip(prev_col_state, next_col_state):
            if next in states_indices:
                transition_counts[states_indices[prev]][states_indices[next]]+=1
        prev_index = index
        prev_col_state = [next if next in states_indices else prev for (prev, next) in zip(prev_col_state, next_col_state)]
        # use this to get emission counts
        for (state, emission) in zip(prev_col_state, next_col): 
            if emission in external_states_indices: emission_counts[states_indices[state]][external_states_indices[emission]]+=1
    # the last one
    next_col_state = ['E' for item in xrange(num_items)]
    for (prev, next) in zip(prev_col_state, next_col_state):
        if next in states_indices:
            transition_counts[states_indices[prev]][states_indices[next]]+=1


    for index, cnt in enumerate(transition_counts):
        the_sum = sum(cnt)
        if not the_sum: continue
        transition_probs[index] = [cnt*1.0/the_sum for cnt in transition_counts[index]]

    for index, cnt in enumerate(emission_counts):
        the_sum = sum(cnt)
        if not the_sum: continue
        emission_probs[index] = [cnt*1.0/the_sum for cnt in emission_counts[index]]

    return io.gen_matrices(states, external_states, transition_probs, emission_probs, '\t', io.prob_format)

io.generate_input_output(do_work, False, True)