"""
Solve the Suffix Tree Construction Problem.
"""
import bio.io_utils
import bio.triee

def read_edges(source):
    edges = {}
    STOP_SIGN = '-'
    NO_CHILDREN = '{}'
    for s in source:
        if s==STOP_SIGN: break
        key, arrow, rest = [ss.strip() for ss in s.split()]
        key = int(key)
        edges[key] = []
        if rest!=NO_CHILDREN: edges[key] = [int(i) for i in rest.split(',')]
    return edges

def read_leaves(source):
    leaves = {}
    to_key = bio.triee.constants.to_key
    for s in source:
        key, value = [ss.strip() for ss in s.split()]
        key = int(key[:-1])
        leaves[key] = to_key[value]
    return leaves

def yield_result(result):
    # yield every entry as key: value
    to_string = bio.triee.constants.to_string
    for key in sorted(result.keys()):
        yield "%s: %s" % (key, to_string[result[key]])

def do_work(source):
    edges = read_edges(source)
    leaves = read_leaves(source)
    for s in source: pass # eat source
    result = bio.triee.tree_coloring(edges, leaves)
    return yield_result(result)

bio.io_utils.generate_input_output(do_work, True)
