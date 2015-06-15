"""
Solve the Non Branching Paths Construction Problem.
"""
import bio.io_utils
import bio.triee
from copy import deepcopy

def swap(al, node_1, node_2, child_1, child_2):
    al[node_1].remove(child_1)
    al[child_1].remove(node_1)
    al[node_2].remove(child_2)
    al[child_2].remove(node_2)
    al[node_1].append(child_2)
    al[child_2].append(node_1)
    al[node_2].append(child_1)
    al[child_1].append(node_2)

def emit_lists(al1, al2):
    for node in al1:
        for child in al1[node]:
            yield "%s->%s" % (node, child)
    yield ""
    for node in al2:
        for child in al2[node]:
            yield "%s->%s" % (node, child)


def do_work(source):
    node_1, node_2, = [int(i) for i in source.next().split()]
    al = bio.io_utils.read_adjacency_list(source)
    al1 = deepcopy(al)
    al2 = deepcopy(al)
    children_1 = deepcopy(al[node_1])
    children_2 = deepcopy(al[node_2])
    children_1.remove(node_2)
    children_2.remove(node_1)
    swap(al1, node_1, node_2, children_1[1], children_2[0])
    swap(al2, node_1, node_2, children_1[1], children_2[1])

    return emit_lists(al1, al2)

bio.io_utils.generate_input_output(do_work, True, False)
