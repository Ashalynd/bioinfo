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
    centers = cl.fft_centers(k, data)
    return io.gen_lines([data[ci] for ci in centers], io.stringify_array)

io.generate_input_output(do_work, True, True)
