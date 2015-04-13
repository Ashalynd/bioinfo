class trie_node():
    def __init__(self, payload):
        self.payload = payload
        self.node_id = len(self.payload)
        self.children = {} # symbol -> child_id
        self.payload.append(self)
    def child(self, symbol): return self.payload[self.children[symbol]]
    def is_leaf(self): return not self.children
    def ensure_child(self, symbol):
        if symbol not in self.children:
            new_node = self.__class__(self.payload)
            self.children[symbol] = new_node.node_id
        return self.child(symbol)
    def append(self, line):
        if not line: return self.node_id
        symbol = line[0]
        return self.ensure_child(symbol).append(line[1:])
    def match(self, line):
        if not line: return True
        symbol = line[0]
        return symbol in self.children and self.child(symbol).match(line[1:])
    def emit_edges(self):
        return ['%s->%s:%s'%(self.node_id, child_id, key) for (key, child_id) in self.children.iteritems()]
    def emit(self):
        return 'id: %s, children: %s' % (self.node_id, self.children)

class trie():
    def new_node_class(self):
        return trie_node(self.payload)
    def __init__(self):
        self.payload = []
        self.root = self.new_node_class()
    def append(self, line): 
        self.count = self.root.append(line)
        return self.count
    def add(self, lines): 
        map(lambda line:self.append(line), lines)
        return self.count
    def match(self, text): return self.root.match(text)
    # return itself as a list of [num_p->num_c:C] lines
    def emit_edges(self):
        for node in self.payload: 
            for line in node.emit_edges():
                yield line
    def emit(self):
        for node in self.payload:
            yield node.emit()

class suffix_trie_node(trie_node):
    def __init__(self, payload):
        trie_node.__init__(self, payload)
        self.label = None
    def set_label(self, label): self.label = label
    def emit(self):
        return 'id: %s, label: %s, children: %s' % (self.node_id, self.label, self.children)

class suffix_trie(trie):
    def new_node_class(self):
        return suffix_trie_node(self.payload)
    def append_suffix(self, i):
        node_id = self.append(self.text[i:])
        last_node = self.payload[node_id]
        if last_node.is_leaf(): last_node.set_label(i)
    def construct(self, text):
        self.text = text
        len_text = len(text)
        for i in xrange(len_text):
            self.append_suffix(i)


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
