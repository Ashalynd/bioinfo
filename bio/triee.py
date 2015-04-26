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
        if not line: return self.node_id
        key, rest = self.split_key(line)
        return self.ensure_child(key, {'position':position}).append(rest, position+1)
    def set_label(self, label): self.label = label
    def emit(self):
        return 'id: %s, label: %s, position: %s, children: %s' % (self.node_id, self.label, self.position, self.children)

# trie that stores all suffixes for the given text
class suffix_trie(trie):
    def new_node_class(self):
        return suffix_trie_node(self.payload)
    def append_suffix(self, i):
        node_id = self.root.append(self.text[i:], i)
        last_node = self.payload[node_id]
        if last_node.is_leaf(): last_node.set_label(i)
    def construct(self, text):
        self.text = text
        len_text = len(text)
        for i in xrange(len_text):
            self.append_suffix(i)

#converts the adjacent list (ad dictionary) into dictionary of parents per node
def parents_from_children(nodes):
    parents = {}
    for k, values in nodes.iteritems():
        for v in values:
            if not v in parents: parents[v] = set()
            parents[v].add(k)
    return parents


#receives edges as adjacency list
def non_branching_paths(edges):
    from copy import deepcopy
    indices = set()
    # we need to find out if a node has more than one parent
    parents = parents_from_children(edges)
    # consider only keys which are not 1-1 nodes
    keys = filter(lambda key: len(edges[key])>1 or ((not key in parents) or len(parents[key])>1), edges.keys())
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
                if len(parents[next_index])>1: break
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
    cycles_keys = set(edges.keys()).difference(passed_keys)
    for index in cycles_keys:
        traverse_subpath(index, True, cycles)
        
    return sorted(list(paths)) + sorted(list(cycles))


class suffix_tree_node(base_triee_node):
    def __init__(self, payload, old_position = 0):
        base_triee_node.__init__(self, payload)
        self.label = None
        self.old_position = old_position
    def set_label(self, label): self.label = label
    def emit(self):
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
    def longest_repeat(self, start_pos = None):
        if self.is_leaf():
#            print "leaf", start_pos
            return start_pos, -1
        else:
            max_length = 0
            max_pos = start_pos
            for ((pos, length), child_id) in self.children.iteritems():
#                print "pos", pos, "length", length
                child_pos, child_length = self.payload[child_id].longest_repeat(pos)
#                print "child_pos", child_pos, "child_length", child_length
                if child_length>=0 and (length + child_length > max_length):
                    max_length = length + child_length
                    max_pos = start_pos or child_pos
            return max_pos, max_length


class suffix_tree(base_triee):
    def new_node_class(self):
        return suffix_tree_node(self.payload)
    def emit_edges_with_text(self): return self.emit_edges({'text': self.text})
    def emit_edges_as_text(self): return self.emit_edges({'text': self.text, 'compact': True})
    def from_trie(self, source):
        # builds a suffix tree from suffix trie
        # 1. generates non branching paths
        # 2. finds out all nodes which are either in the beginning or at the end of the nbp
        # 3. adds all of them to payload, notes the new position <=> old position
        # 4. iterate over all nodes which made it to suffix tree and add the children (end nodes)
        self.text = source.text
        nb_paths = non_branching_paths(source.to_edges())
        new_kids = dict([(path[1], path) for path in nb_paths]) # used to map the paths from the trie to tree
        remaining_nodes = set()
        map(lambda path: remaining_nodes.update(set([path[0], path[-1]])), nb_paths)
        old_to_new = {0:0}
        # relationships between old and new positions
        for index, old_position in enumerate(sorted(list(remaining_nodes))[1:]): # 0 is already there
            new_node = suffix_tree_node(self.payload, old_position)
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
    def longest_repeat(self):
        max_pos, max_length = self.root.longest_repeat()
        return self.text[max_pos:(max_pos+max_length)]

"""

class suffix_node():
    def __init__(self, parent, position = None):
        self.parent = parent
        self.children = {}
        self.position = position
        self.label = None
    def has_child(self, symbol): return symbol in self.children
    def get_index(self, symbol): return self.children[symbol]
    def get(self, symbol): return self.parent[self.children[symbol]]
    def head_index(self): return self.children.itervalues().next()
    def add(self, symbol, position):
        self.children[symbol] = len(self.parent)
        self.parent.append(suffix_node(self.parent, position))
        return self.get(symbol)
    def is_leaf(self): return not self.children
    def set_label(self, new_label): self.label = new_label
    def out_degree(self): return len(self.children)
    def keys(self): return self.children.keys()
    def emit(self): return "(%s, %s, %s)" % (self.position, self.label, self.children)

class suffix_trie():
    def __init__(self):
        self.children = []
        self.children.append(suffix_node(self.children))
    def preconstruct(self, text):
        self.text = text
        #print "text", self.text
        len_text = len(text)
        for i in xrange(len_text):
            current_node = self.children[0]
            for j in xrange(i, len_text):
                current_symbol = text[j]
                if current_node.has_child(current_symbol):
                    current_node = current_node.get(current_symbol)
                else:
                    current_node = current_node.add(current_symbol, j)
            if current_node.is_leaf(): current_node.set_label(i)
    def emit(self):
        for index, child in enumerate(self.children):
            for key in child.keys():
                child_index = child.get_index(key)
                yield '%s->%s:%s,%s' %(index, child_index, key, self.children[child_index].position)
    def non_branching_paths(self):
        paths = set()
        indices = set([0])
        while indices:
            index = indices.pop()
            node = self.children[index] 
            for child in node.children:
                start = node.get_index(child)
#                print "child:", child, "start:", start
                end = start
                next_end = start
                degree = self.children[end].out_degree()
#                print "end 0", end, "degree", degree
                while degree==1:
                    end = self.children[end].head_index()
                    degree=self.children[end].out_degree()
#                    print "end", end, "degree", degree
                paths.add((index, start, end))
                if degree>1: indices.add(next_end)
        return paths
    def emit_paths(self, paths, details = False):
        for (index, start, end) in paths:
            start_pos, end_pos = self.children[start].position, self.children[end].position
            if not details:
                yield self.text[start_pos:(end_pos+1)]
            else:
                label = self.children[end].label or '-'
                yield (self.text[start_pos:(end_pos+1)], start_pos, end_pos+1-start_pos, label)

class st_node():
    def __init__(self, parent):
        self.parent = parent
        self.label = None
        self.children = {}
    def is_leaf(self): return self.label is not None
    def get(self, key): return self.parent[self.children[key]]
    def longest_repeat(self, start = None, length = 0):
        if self.is_leaf():
#            print "leaf", start, length
            return (start, 0)
        else:
            max_length = 0
            max_position = None
#            print "children", [key for key in self.children]
            for key in self.children:
                (child_position, child_length) = key
                child = self.get(key)
                (new_child_position, new_child_length) = child.longest_repeat(child_position, child_length)
#                print "child", child, "pos", new_child_position, "len", new_child_length
                if new_child_length > max_length:
                    max_length = new_child_length
                    max_position = new_child_position
            start = start or max_position
#            print "start", start, "length", length + max_length
            return (start, length + max_length)
    def all_repeats(self, aggregator, start = None, length = 0):
        if self.is_leaf():
            return
        else:
            if (start and length): aggregator.add((start, length))
            for key in self.children:
                (child_position, child_length) = key
                child = self.get(key)
                child.all_repeats(aggregator, start or child_position, length + child_length)


class suffix_tree():
    def __init__(self):
        self.children={}
    #st: suffix_trie
    def from_trie(self, st):
        self.text = st.text
        paths = st.non_branching_paths()
#        print "paths", list(st.emit_paths(paths, True))
        hubs = set([hub for (hub,first,last) in paths])
        stretches = dict([(first, last) for (hub,first,last) in paths])
        nodes = set([last for (hub,first,last) in paths])
        nodes.add(0)
        #enumerate tree nodes
        for (index, node) in enumerate(st.children):
            if index in nodes:
                new_node=st_node(self.children)
                new_node.label = node.label
                #enumerate node children
                for (child, ch_index) in node.children.iteritems():
                    #find stretch
                    end_index = stretches[ch_index]
                    start_pos = st.children[ch_index].position
                    end_pos = st.children[end_index].position
                    new_node.children[(start_pos, end_pos+1-start_pos)] = end_index
#                print "index", index, "label", new_node.label, "children", len(new_node.children)
                self.children[index] = new_node
    
    def longest_repeat(self):
        (position, length) = self.children[0].longest_repeat()
        return self.text[position:position+length]

    def all_repeats(self):
        aggregator = set()
        self.children[0].all_repeats(aggregator)
        return set([self.text[start:(start+length)] for (start,length) in aggregator])

    def emit(self):
        for (key, value) in self.children.iteritems():
            for child, child_value in value.children:
                yield (key, value.label, child, child_value)

"""
