"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils
import bio.triee

def read_matrix(source):
    result = []
    for line in source:
        row = [int(elem) for elem in line.split()]
        result.append(row)
    return result

def do_work(source):
    N = int(source.next())
    j = int(source.next())
    data = read_matrix(source)
    min_length = max(data[j]) # initialize with something reasonable
    i = 0 if j>0 else 1
#    for i in xrange(N):
#        if i==j: continue
    for k in xrange(i+1, N):
        if k==j: continue
        cur_length = (data[j][i]+data[j][k]-data[i][k])/2
        if cur_length<min_length: min_length=cur_length

    return bio.io_utils.gen(min_length)

bio.io_utils.generate_input_output(do_work, False, True)
