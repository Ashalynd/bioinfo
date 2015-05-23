"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils
import bio.triee

def read_list(source):
    result = []
    for line in source:
        row = tuple([float(elem) for elem in line.split()])
        result.append(row)
    return result

def distance(p1, p2):
    return sum([(i1-i2)**2 for (i1, i2) in zip(p1, p2)])**0.5

def do_work(source):
    (k, m) = [int(p) for p in source.next().split()]
    data = read_list(source)
#    print "data", data
    len_data = len(data)
    centers = set([0])
    while len(centers)<k:
        current_dist = -1
        next_center = None
        for d in xrange(len_data):
            if d in centers: continue
            dist = min([distance(data[ci], data[d]) for ci in centers])
            if dist>current_dist: 
                next_center = d
                current_dist = dist
#            print "dist", dist, "current_dist", current_dist, "next_center", next_center
        centers.add(next_center)
#        print "centers", centers
    return bio.io_utils.gen_lines([data[ci] for ci in centers], bio.io_utils.stringify_array)

bio.io_utils.generate_input_output(do_work, True, True)
