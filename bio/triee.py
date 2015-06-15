class constants():
    RED = 1
    BLUE = 2
    PURPLE = 3
    GRAY = 0
    to_string = {RED:'red', BLUE:'blue', PURPLE:'purple', GRAY:'gray'}
    to_key = {v:k for (k,v) in to_string.iteritems()}

class base_triee_node():
    def __init__(self, payload, args = None):
        # parameters:
        # payload - a list where i-th element stores reference to i-th node
        self.payload = payload
        self.node_id = len(self.payload)
        self.children = {} # key -> child_id
        self.payload.append(self)
    def child(self, key): return self.payload[self.children[key]]
    def is_leaf(self): return not self.children
    def ensure_child(self, key, args = None):
        # return a child corresponding to a given key. Creates one if key is not present.
        if key not in self.children:
            new_node = self.__class__(self.payload, args)
            self.children[key] = new_node.node_id
        return self.child(key)
    def emit_edges(self, args = None):
        # pretty-prints the parent-child connections
        return ['%s->%s:%s'%(self.node_id, child_id, key) for (key, child_id) in self.children.iteritems()]
    def emit(self):
        # pretty-prints own + children ids
        return 'id: %s, children: %s' % (self.node_id, self.children)

class base_triee():
    def new_node_class(self):
        return base_triee_node(self.payload)
    def __init__(self):
        # always creates a root node
        self.payload = []
        self.root = self.new_node_class()
    def get_node(self, node_id): return self.payload[node_id]
    def to_edges(self):
        # returns a dictionary that contains only the links between the nodes
        return dict(map(lambda item: (item.node_id, item.children.values()), self.payload))
    def emit_edges(self, args = None):
        # return itself as a list of [num_p->num_c:C] lines
        for node in self.payload: 
            for line in node.emit_edges(args):
                yield line
    def emit(self):
        for node in self.payload:
            yield node.emit()
    def adjacency_list(self):
        return dict([(index, node.children.values()) for (index, node) in enumerate(self.payload)])


class trie_node(base_triee_node):
    def split_key(self, line): return (line[0], line[1:])
    def append(self, line):
        # recursively add a new line of text to the suffix tree
        if not line: return self.node_id
        key, rest = self.split_key(line)
        return self.ensure_child(key).append(rest)
    def match(self, line):
        # recursively looks for a match of the given line
        if not line: return True
        key, rest = self.split_key(line)
        return key in self.children and self.child(key).match(rest)

class trie(base_triee):
    def new_node_class(self):
        return trie_node(self.payload)
    def append(self, line): 
        self.count = self.root.append(line)
        return self.count
    def add(self, lines): 
        map(lambda line:self.append(line), lines)
        return self.count
    def match(self, text): return self.root.match(text)
    def adjacency_list(self):
        return dict([(index, node.children.values()) for (index, node) in enumerate(self.payload)])

class suffix_trie_node(trie_node):
    def __init__(self, payload, args = None):
        trie_node.__init__(self, payload)
        self.label = None
        self.position = args['position'] if args else None
    def append(self, line, position = 0):
        if not line: 
            return self.node_id, None
        else:
            key, rest = self.split_key(line)
            return self.ensure_child(key, {'position':position}).node_id, rest
    def set_label(self, label): self.label = label
    def emit(self):
        return 'id: %s, label: %s, position: %s, children: %s' % (self.node_id, self.label, self.position, self.children)

# trie that stores all suffixes for the given text
class suffix_trie(trie):
    def new_node_class(self):
        return suffix_trie_node(self.payload)
    def append_suffix(self, i, color = None):
        position = i
        node_id = 0
        rest = self.text[position:]
        while True:
            node_id, rest = self.payload[node_id].append(rest, position)
#            print "node_id", node_id, "rest", rest
            if not rest: break
            position +=1
        last_node = self.payload[node_id]
        if last_node.is_leaf(): 
            last_node.set_label(i)
            if color: last_node.color = color
    def construct(self, text, color = None):
        self.text = text
        len_text = len(text)
        for i in xrange(len_text):
            self.append_suffix(i, color)

#converts the adjacent list (ad dictionary) into dictionary of parents per node
def parents_from_children(nodes):
    parents = {}
    for k in nodes:
        for v in nodes[k]:
            if not v in parents: parents[v] = set()
            parents[v].add(k)
    return parents


#receives edges as adjacency list
def non_branching_paths(edges, check_parents = True, check_cycles = True):
    from copy import deepcopy
    indices = set()
    parents = {}
    if check_parents:
        # we need to find out if a node has more than one parent
        parents = parents_from_children(edges)
        # consider only keys which are not 1-1 nodes
        keys = filter(lambda key: len(edges[key])>1 or ((not key in parents) or len(parents[key])>1), edges.keys())
    else:
        keys = [0] + filter(lambda key: len(edges[key])>1, edges.keys())
    #find non-cyclic non-branching paths
    passed_keys = set()

    def traverse_subpath(index, check_passed, aggregator):
        # index - active index to check for non-branching paths
        # check_passed - whether to check if index has been considered yet (only important for isolated cycles)
        # aggregator - where to put the found paths
        if check_passed and index in passed_keys: return
        subnodes = edges[index] # index -> {0,1,2,3,...}
        if not subnodes: return
        for next_index in subnodes:
            path = [index] # start with parent
            while(True):
                path.append(next_index) # at least 2 nodes in every non-breakable path
                passed_keys.add(next_index)
                # check whether the cycle has closed
                if next_index==index: break
                # every internal node in non-breakable path should be 1-in 1-out node
                if check_parents and len(parents[next_index])>1: break
                next_node = edges.get(next_index) # set of children for the given index
                if not(next_node) or len(next_node)>1: break
                next_index = list(next_node)[0]
            aggregator.add(tuple(path))
        passed_keys.add(index)

    paths = set()
    for index in keys:
        traverse_subpath(index, False, paths)
    #find cycles
    cycles = set()
    if check_cycles:
        cycles_keys = set(edges.keys()).difference(passed_keys)
        for index in cycles_keys:
            traverse_subpath(index, True, cycles)
        
    return sorted(list(paths)) + sorted(list(cycles))

def tree_coloring(edges, input_leaves):
    ct = constants
    leaves = {key:(input_leaves[key] if key in input_leaves else ct.GRAY) for key in edges.keys()}
    # receives edges and colors of leaves, returns list containing all edges and their colors
    def is_ripe(node_id): return all(leaves[child_id]!=ct.GRAY for child_id in edges[node_id])
    def has_child_color(node_id, color): return any(leaves[child_id]==color for child_id in edges[node_id])
    def has_color(node_id): return leaves[node_id]!=ct.GRAY
    uncolored = edges.keys()
    while uncolored:
        next_uncolored = []
        for node_id in uncolored:
            if has_color(node_id): continue
            if not is_ripe(node_id):
                next_uncolored.append(node_id)
            else:
                color = leaves[node_id]
#                print node_id, color, ','.join([str(leaves[child_id]) for child_id in edges[node_id]])
                has_blue = has_child_color(node_id, ct.BLUE)
                has_red = has_child_color(node_id, ct.RED)
                has_purple = has_child_color(node_id, ct.PURPLE)
                if has_purple or (has_blue and has_red):
                    color = ct.PURPLE
                else:
                    if has_blue:
                        color = ct.BLUE
                    else:
                        assert(has_red)
                        color = ct.RED
                leaves[node_id] = color
#                print "!", node_id, color
        uncolored = next_uncolored
    return leaves


class suffix_tree_node(base_triee_node):
    def __init__(self, payload, args = None):
        base_triee_node.__init__(self, payload)
        self.label = None
    def set_label(self, label): self.label = label
    def set_color(self, color): self.color = color
    def emit(self):
        if hasattr(self, 'color'):
            return 'id: %s, label: %s, color: %s, children: %s' % (self.node_id, self.label, self.color, self.children)   
        else: 
            return 'id: %s, label: %s, children: %s' % (self.node_id, self.label, self.children)
    def emit_edges(self, args = None):
        # pretty-prints the parent-child connections
        if not args:
            result = ['%s->%s:%s'%(self.node_id, child_id, key) for (key, child_id) in self.children.iteritems()]
        else:
            if not 'compact' in args: # full info
                result = ['%s->%s:%s(%s)'%(self.node_id, child_id, (start, length), args['text'][start:(start+length)]) for ((start, length), child_id) in self.children.iteritems()]
            else:
                result = [args['text'][start:(start+length)] for (start, length) in self.children]
        return result
    def longest_repeat(self, start_pos = None, start_length = 0, common = False):
        # if common = True, it assumes that nodes have colors
        if self.is_leaf() or (common and self.color!=constants.PURPLE):
#            print "id", self.node_id, "leaf", self.is_leaf(), "color", self.color
            return start_pos, 0
        else:
            max_length = 0
            max_pos = (start_pos if start_pos else 0) + start_length
            for ((pos, length), child_id) in self.children.iteritems():
                if common and self.payload[child_id].color != constants.PURPLE: continue
#                print "pos", pos, "length", length
                child_pos, child_length = self.payload[child_id].longest_repeat(pos, length, common)
#                print "child_pos", child_pos, "child_length", child_length
                if child_length>0 and (child_length > max_length):
                    max_length = child_length
                    max_pos = child_pos
#            print "id", self.node_id, "color", self.color, "pos", max_pos - start_length, "length", max_length+start_length, "common", common
            return max_pos - start_length, max_length + start_length


class suffix_tree(base_triee):
    def new_node_class(self):
        return suffix_tree_node(self.payload)
    def emit_edges_with_text(self): return self.emit_edges({'text': self.text})
    def emit_edges_as_text(self): return self.emit_edges({'text': self.text, 'compact': True})
    def to_text(self, pos, length): return self.text[pos:pos+length]

    def acc_to_text(self, acc):
        # converts accelerator (a sequence of lists of (pos, length) tuples) into a set of strings
        return set(map(lambda seq: ''.join(map(lambda elem: self.to_text(elem[0],elem[1]), seq)), acc))    

    def from_trie(self, source):
        # builds a suffix tree from suffix trie
        # 1. generates non branching paths
        # 2. finds out all nodes which are either in the beginning or at the end of the nbp
        # 3. adds all of them to payload, notes the new position <=> old position
        # 4. iterate over all nodes which made it to suffix tree and add the children (end nodes)
        self.text = source.text
        nb_paths = non_branching_paths(source.to_edges(), check_parents = False, check_cycles = False)
        new_kids = dict([(path[1], path) for path in nb_paths]) # used to map the paths from the trie to tree
        remaining_nodes = set()
        map(lambda path: remaining_nodes.update(set([path[0], path[-1]])), nb_paths)
        old_to_new = {0:0}
        # relationships between old and new positions
        for index, old_position in enumerate(sorted(list(remaining_nodes))[1:]): # 0 is already there
            new_node = suffix_tree_node(self.payload)
            old_to_new[old_position] = new_node.node_id # translating position in trie to position in tree
        for node in remaining_nodes:
            # get the old node and a node to which it will be converted
            old_node = source.get_node(node)
            new_node = self.get_node(old_to_new[node])
#            print "old_node", old_node.emit(), "new_node", new_node.emit()
            if old_node.is_leaf():
                # if it's a leaf, only copy the label (start position of the text from which this branch was created)
                new_node.label = old_node.label
            else: # there are children - iterate over them
                for subnode_id in old_node.children.values():
                    # find corresponding node in the trie
                    subnode = source.get_node(subnode_id)
                    # find the corresponding non branching path
                    nb_path = new_kids[subnode_id]
                    assert(nb_path[0] == node) # paranoiac check
                    # find the node in the new tree, corresponding to last path element
                    end_node = source.get_node(nb_path[-1])
                    new_end_node = old_to_new[end_node.node_id]
                    # find start and end positions for the chunk of text related to this path
                    start_pos = subnode.position
                    end_pos = end_node.position
                    # add the new link
                    new_node.children[(start_pos, 1+end_pos-start_pos)] = new_end_node

    def longest_repeat(self, common = False):
#        print "longest_repeat", common
        if common: self.color()
        max_pos, max_length = self.root.longest_repeat(None, 0, common)
        return self.to_text(max_pos,max_length)

    def all_repeats(self, common = False):
        if common: self.color()
        acc = set()
        pool = {self.root.node_id:[]}
        while pool:
            node_id, chains = pool.popitem()
            node = self.payload[node_id]
            if node.is_leaf() or (common and node.color!=constants.PURPLE): continue
            for i in xrange(len(chains)): 
                acc.add(tuple(chains[i:])) # not really necessary at this step?
            for ((pos, length), child_id) in node.children.iteritems():
                pool[child_id] = chains + [(pos,length)]
        return self.acc_to_text(acc)

    def all_uniques(self, the_color = constants.BLUE):
        self.color()
        acc = set()
        pool = {self.root.node_id:[]}
        while pool:
            node_id, chains = pool.popitem()
#            print "acc", acc
            node = self.payload[node_id]
            if node.color not in (constants.PURPLE, the_color): continue
            has_color = node.color == the_color
#            print "node_id", node_id, "chains", chains, "color", node.color
            if has_color:
                for i in xrange(len(chains)):
                    if not i or chains[i][2]: acc.add(tuple([item[:-1] for item in chains[i:]]))
            if node.is_leaf(): continue
            for ((pos, length), child_id) in node.children.iteritems():
                pool[child_id] = chains + [(pos,length, has_color)]
        return self.acc_to_text(acc)

    def color(self):
        color_pos = self.text.find('#')+1
        if color_pos<=0: raise ValueError('No delimiter to set color position!')
        # make edges and leaves for coloring procedure
        node_ids = xrange(len(self.payload))
        edges = {node_id:self.payload[node_id].children.values() for node_id in node_ids}
        def assign_color(node, color_pos):
            if not node.is_leaf(): return constants.GRAY
            return constants.BLUE if node.label < color_pos else constants.RED
        leaves = {node_id:assign_color(self.payload[node_id], color_pos) for node_id in node_ids}
        colored_leaves = tree_coloring(edges, leaves)
        # reassign colors
        map (lambda node_id: self.payload[node_id].set_color(colored_leaves[node_id]), colored_leaves.keys())

    def to_suffix_array(self):
        result = [self.root.node_id]
        next_result = []
        has_children = True
        #first initialization: all children of the root node (all possible first letters)
        while has_children:
            next_result = []
            has_children = False
            # the result nodes should be lexicographically sorted automatically
            for node_id in result:
                node = self.get_node(node_id)
                has_children = has_children or node.children
                if node.is_leaf():
                    # just add the leaf and continue
                    next_result.append(node_id)
                    continue
                print "keys", node.children.keys()
                for child_key in sorted(node.children.keys(), key = lambda (pos,len):self.text[pos]):
                    # add children for the next round
                    next_result.append(node.children[child_key])
            print "next_result", next_result
            pos_result = map(lambda node_id: self.get_node(node_id).label, next_result)
            print "pos_result", pos_result
            result = next_result
        # hopefully, we get out of the cycle with the array, containing node_ids of sorted suffixes
        # now, convert them into starting positions
        pos_result = map(lambda node_id: self.get_node(node_id).label, result)
        return pos_result

    def from_suffix_array(self, text, suffix_array, lcp):
        # keep only the root node
#        assert(len(self.payload)==1, "The tree is already initialized")
        self.text = text
        self.root.children = {}
        len_text = len(text)
        last_path = [(0, 0)] # index, descend
        for (suffix, prefix) in zip(suffix_array, lcp):
#            print "!", suffix, prefix, text[suffix:suffix+prefix+1]
            last_node_key = None
#            print "last_path", last_path, "payload_len", len(self.payload)
            while last_path[-1][1]>prefix: last_node_key = last_path.pop(-1)
            index, descend = last_path[-1]
            node = self.get_node(index)
            if descend == prefix: # just add the new node
                key = (suffix + prefix, len_text-(suffix + prefix))
#                print "new key", key
                child = node.ensure_child(key)
                child.label = suffix
                last_path.append((child.node_id, descend + key[1]))
#                print "new node: last_path", last_path, "payload_len", len(self.payload)
            else:
#                print "last_node_key", last_node_key
                next_index, next_descend = last_node_key
                next_node = self.get_node(next_index)
                #should replace the key leading to this node, remove the label and add two new leavs
#                assert(next_index==len(self.payload)-1)
                next_key = None
                # arghh no other way to find that child
                for (key, value) in node.children.iteritems():
                    if value == next_index:
                        next_key = key
                        break
                assert(next_key is not None)
                removed_index = node.children.pop(next_key)
                assert(removed_index==next_index)
                # now, create the new hub and add it to last_path
                diff = prefix - descend
                hub_key = (next_key[0], diff)
#                print "hub key", hub_key
                hub_child = node.ensure_child(hub_key)
                last_path.append((hub_child.node_id, prefix))
                # add the old node to the hub
                old_child_key = (next_key[0] + diff, next_key[1] - diff)
#                print "old child key", old_child_key
                hub_child.children[old_child_key] = next_index
                # add the new node to the hub and to the last_path
                new_child_key = (suffix + prefix, len_text - (suffix + prefix))
#                print "new child key", new_child_key
                new_child = hub_child.ensure_child(new_child_key)
                new_child.label = suffix
                last_path.append((new_child.node_id, descend + new_child_key[1]))
#                print "extra node: last_path", last_path, "payload_len", len(self.payload)







