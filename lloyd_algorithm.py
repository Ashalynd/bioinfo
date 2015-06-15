"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils as io
import bio.triee
import bio.cluster as cl

def do_work(source):
    (k, m) = [int(p) for p in source.next().split()]
    data = io.read_float_list(source)
#    print "data", data
    centers = cl.lloyd_kmeans(k, m, data, with_fft = False, epsilon = 1e-6, randomStart = True)
    return io.gen_lines_format(centers, format='%.3f')

io.generate_input_output(do_work, False, False)
