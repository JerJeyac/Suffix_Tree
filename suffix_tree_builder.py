#Tree builder class
class SuffixNode():
    '''Suffix Node object of Suffix Tree'''

    leaf_pos = 0
    _curr_ind = 0

    def __init__(self):

        #Key node variables
        self.children = {}
        self._s_link = []
        self._start, self._end = 0, 0

        #Keep track of leaf nodes for visualization
        self._curr_ind += 1
        self._total_nodes =+ 1
        self.suffix_index = self._curr_ind #Root, leaf, internal

    #Logging
    def __repr__(self):

        #Root case, only root has (-) start, -2 is only for root
        if (self.suffix_index ==-2):
            return 'Root_Node(start: %d end: %d ID: %d)' % (self.start,self.end,self.node_id)
        #Internal case
        elif (self.suffix_index < 0) and (self.start >= 0):
            return 'Internal_Node(start: %d end: %d ID: %d)' % (self.start,self.end,self.node_id)
        #Leaf case
        else: return 'Leaf(start: %d end: %d ID: %d)' % (self.start, self.end, self.node_id)

    #Convert into root
    def instantiate_as_root(self):
        #Establish the current node as a root
        self.start, self._end = 0,0
        #By definition an internal node
        self.suffix_index = -2
        #Decrement _curr_ind
        self._curr_ind -= 1

    #Internalize node
    def make_internal(self):
        self.suffix_index = -1

    #Add baby
    def add_child(self,child_node,base):
        self.children[base] = child_node

    #Compute length of incoming edge
    def edge_distance(self):
        return self.end-self.start

    ##Properties

    @property
    def end(self):
        if self.suffix_index >= 0:
            return self.leaf_pos
        else:
            return self._end
    @end.setter
    def end(self, end):
        self._end = end

    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, start):
        self._start = start

    @property
    def s_link(self):
        if self._s_link is not None:
            return self._s_link
        else: return []
    @s_link.setter
    def s_link(self, suffix_link):
        self._s_link = suffix_link

    @property
    def node_id(self):
        return id(self)

#Builder returns Suffix_Tree class
class SuffixBuilder():

    def __init__(self,dna):
        self.string = dna + '$' #string sequence

    #Ukkonen's algorithm
    def build_tree(self):

        root = SuffixNode()
        root.instantiate_as_root()

        r = 0
        ap = {'node': root, 'edge': None, 'length' : 0}
        step = -1

        #Iterate input string
        while SuffixNode.leaf_pos < len(self.string):

            base = self.string[SuffixNode.leaf_pos]
            SuffixNode.leaf_pos += 1
            r += 1
            step += 1
            jump_node = [None]

            print('Phase # {0}'.format(self.string[0:SuffixNode.leaf_pos]))

            while r > 0:

                #Conflict routine
                if self.compare_base_ap(ap,base):
                    if ap['edge'] is None: ap['edge'] = base
                    ap['length'] += 1

                    overhang = ap['length'] - ap['node'].children[ap['edge']].edge_distance()
                    if overhang >= 0:
                        ap['node'] = ap['node'].children[ap['edge']]
                        ap['length'] = 0
                        ap['edge'] = None
                    break #end phase

                #Insertion routine
                if ap['edge'] is None:
                    new_leaf = SuffixNode()
                    new_leaf.start = step
                    ap['node'].add_child(new_leaf,base)

                #Edge split routine
                else:
                    self.split_edge(ap,base)

                    if (jump_node[0] is not None) and (jump_node[0] is not ap['node'].children[ap['edge']]):
                        jump_node[0].s_link.append(ap['node'].children[ap['edge']])
                    jump_node[0] = ap['node'].children[ap['edge']]

                if (ap['node'] == root) and (ap['edge'] is not None):
                    ap['length'] -= 1
                    self.correct_edge(ap)
                else:
                    if ap['node'].s_link:
                        ap['node'] = ap['node'].s_link[0]
                        self.canonize(ap)
                    else:
                         ap['node'] = root
                         self.correct_edge(ap)

                r -= 1

            print('Letters Stored: ' + self.string[SuffixNode.leaf_pos-r:SuffixNode.leaf_pos])

        return SuffixTree(root,self.string)

    #Skip/count trick
    def correct_edge(self,ap):
        if ap['length'] == 0:
            ap['edge'] = None
            return

        sc_length = ap['length']
        sc_substring = self.string[SuffixNode.leaf_pos - sc_length - 1]
        overhang = sc_length - ap['node'].children[sc_substring].edge_distance()

        #If overhang is 0 then just move to next edge
        if overhang == 0:
            ap['node'] = ap['node'].children[sc_substring]
            ap['edge'] = None
            ap['length'] = 0
            return

        while overhang > 0:

            ap['node'] = ap['node'].children[sc_substring]
            sc_length = overhang
            sc_substring = self.string[SuffixNode.leaf_pos - sc_length - 1]
            overhang = sc_length - ap['node'].children[sc_substring].edge_distance()

        #Post traversal clean-up
        ap['length'] = sc_length
        if ap['length'] == 0:
            ap['edge'] = None
        else: ap['edge'] = sc_substring

    #TODO: Test canonize explicitly
    def canonize(self,ap):
        if ap['length'] == 0: return

        start = ap['node'].children[ap['edge']].start
        delta = ap['length'] - ap['node'].children[ap['edge']].edge_distance()
        while delta > 0:
            ap['node'] = ap['node'].children[ap['edge']]
            ap['length'] = delta
            start += ap['node'].edge_distance()
            delta = ap['length'] - ap['node'].children[ap['edge']].edge_distance()
        if ap['length'] == 0: ap['edge'] = None

    #Injects node at active point
    def split_edge(self,ap,base):

        split_node = SuffixNode()
        split_node.make_internal()
        split_node.start = ap['node'].children[ap['edge']].start
        split_node.end = ap['node'].children[ap['edge']].start + ap['length']
        split_key = self.string[split_node.start + ap['length']]

        new_leaf = SuffixNode()
        new_leaf.start = SuffixNode.leaf_pos - 1
        new_key = base

        ap['node'].children[ap['edge']].start += ap['length']

        split_node.children[split_key] = ap['node'].children[ap['edge']]
        split_node.children[new_key] = new_leaf

        ap['node'].children[ap['edge']] = split_node

    #Compares base to children
    def compare_base_ap(self,ap,base):

        if (ap['edge'] in ap['node'].children):
            return base == self.string[ap['node'].children[ap['edge']].start + ap['length']]
        elif(base in ap['node'].children):
            return base == self.string[ap['node'].children[base].start + ap['length']]

        return False

    #Debugging func
    def get_edge(self,node):
        return self.string[node.start:node.end]


#TODO: Implement generalization of tree routine, implicit representation, and querying for LCS
class SuffixTree():
    def __init__(self,root,dna):
        self.root = root
        self.dna = dna

    #Stack depth-first traversal
    def traverse_tree(self):
        stack = [self.root]

        while stack:
            node = stack.pop()
            edge_tups = []
            for _,child in node.children.items():

                stack.append(child)
                edge_tups.append((
                node.node_id,
                child.node_id,
                self.dna[child.start:child.end]
                ))

            yield node,edge_tups,node.s_link
