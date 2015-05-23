"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils
import bio.triee

def read_list(source, size = None):
    result = []
    counter = 0
    for line in source:
        row = tuple([float(elem) for elem in line.split()])
        result.append(row)
        counter +=1
        if size is not None and counter==size: break
    return result

def distance(p1, p2):
    return sum([(i1-i2)**2 for (i1, i2) in zip(p1, p2)])**0.5

def do_work(source):
    (k, m) = [int(p) for p in source.next().split()]
    centers = set()

    centers = set(read_list(source, k))
    source.next() # eat --------
    data = read_list(source)
#    print "data", data
    len_data = len(data)
    distortion = 0.0
    for d in data:
        dist = min([distance(d, c) for c in centers])
        distortion += dist*dist
    distortion /=len_data
    return bio.io_utils.gen(distortion)

bio.io_utils.generate_input_output(do_work, True, True)
