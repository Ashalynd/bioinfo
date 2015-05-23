def limb_length(j, data):
    # data is an additive matrix N x N
    # j < 0
    min_length = max(data[j]) # initialize with something reasonable
    N = len(data)
    i = 0 if j>0 else 1
    for k in xrange(i+1, N):
        if k==j: continue
        cur_length = (data[j][i]+data[j][k]-data[i][k])/2
        if cur_length<min_length: min_length=cur_length
    return min_length

def neighbour_joining_matrix(data):
    from copy import deepcopy
    total_distance = [0]*len(data)
    result = deepcopy(data)
    len_data = len(data)
    coef = len_data-2
    for index, row in enumerate(data):
        total_distance[index] = sum(row)
    for row in xrange(len_data):
        for col in xrange(len_data):
            if row==col: continue
            result[row][col] = coef*result[row][col]-total_distance[row]-total_distance[col]
    return result

class philo_tree():
    def __init__(self, N, one, two, distance):
        self.next_index = N
        self.links = {one:{two:distance}, two:{one:distance}}
    def find_path(self, start, finish):
        nodes = set([(start,)])
#        print "nodes", nodes
        while nodes:
            current = nodes.pop()
#            print "current", current
            last = current[-1]
            if last==finish: return current
            children = self.links[last].keys()
            for c in children:
                if c in current: continue
                nodes.add(current+(c,))
        return None
    def add_limb(self, start, limb, finish, distance, length):
        path = self.find_path(start, finish)
        current_distance = 0
        current_index = 0
        len_path = len(path)
        while current_distance<distance and current_index+1<len(path):
            current_distance+=self.links[path[current_index]][path[current_index+1]]
            current_index+=1
        if current_distance>distance: # insert new node then between path[current_index] and path[current_index+1]
            new_index = self.next_index
            self.links[new_index]={}
            self.next_index+=1
            first_node, second_node = path[current_index-1], path[current_index]
            old_distance = self.links[first_node][second_node]
            diff = current_distance - distance
            del self.links[first_node][second_node]
            del self.links[second_node][first_node]
            self.links[new_index][second_node] = diff
            self.links[second_node][new_index] = diff
            self.links[new_index][first_node] = old_distance-diff
            self.links[first_node][new_index] = old_distance-diff
        else:
            new_index = path[current_index]
        self.links[new_index][limb] = length
        if not limb in self.links: self.links[limb] = {}
        self.links[limb][new_index] = length


