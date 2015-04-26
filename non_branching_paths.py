"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils
import bio.triee

def do_work(source):
    al = bio.io_utils.read_adjacency_list(source)
    paths = bio.triee.non_branching_paths(al)
    return bio.io_utils.gen_lines(paths, lambda p: ' -> '.join([str(pp) for pp in p]))

bio.io_utils.generate_input_output(do_work, True, False)
