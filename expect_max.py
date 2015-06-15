"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils as io
import bio.triee
import bio.cluster as cl

def do_work(source):
    (k, m) = [int(p) for p in source.next().split()]
    beta = float(source.next())
    data = io.read_float_list(source)
#    print "data", data
    centers = cl.expect_max(k, m, data, beta, epsilon = 1e-6)
    return io.gen_lines_format(centers, format='%.3f')

io.generate_input_output(do_work, False, True)
