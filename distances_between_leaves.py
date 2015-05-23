"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils
import bio.triee

def gen_matrix(data, N):
    for i in xrange(N):
        yield bio.io_utils.stringify_array(data[i][:N])

def do_work(source):
    N = int(source.next())
#    print 'N', N
    al = bio.io_utils.read_adjacency_list_with_weight(source)
    P = max(al.keys())
    result = a=[[None]*(P+1) for i in range(P+1)]
    for parent, children in al.iteritems():
#        print parent, children
        for child, weight in children.iteritems(): result[parent][child] = weight
    for i in xrange(P+1): result[i][i] = 0
    empty = 0
    for i in xrange(P+1):
        for j in xrange(P+1):
            if result[i][j] is None: empty +=1
    while empty>0:
        for i in xrange(P, -1, -1):
            for j1 in xrange(P+1):
                for j2 in xrange(j1+1, P+1):
                    if result[i][j1] and result[i][j2] and not result[j1][j2]:
                        empty-=2
                        dist = result[i][j1]+result[i][j2]
                        result[j1][j2] = dist
                        result[j2][j1] = dist
    return gen_matrix(result, N)
#    paths = bio.triee.non_branching_paths(al)
#    return bio.io_utils.gen_lines(paths, lambda p: ' -> '.join([str(pp) for pp in p]))

bio.io_utils.generate_input_output(do_work, False, False)
