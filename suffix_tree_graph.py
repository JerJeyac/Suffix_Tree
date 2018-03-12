
from suffix_tree_builder import SuffixNode, SuffixTree
from graphviz import Digraph

#Visualization class for plotting Suffix tree
class SuffixGraph():

    def __init__(self):
        #Default style settings
        self._styles = {
            'graph': {
                'rankdir' : 'LR',
                'label' : '',
                'fontsize' : '16',
                'size' : '5',
                'fixedsize' : 'true'
            },
            'nodes' : {
                'fontcolor': 'red',
                'label': '',
                'style': 'filled',
                'fillcolor': 'red',
                'fontsize': '1',
                'shape' : 'circle',
                'width' : '0.25'
            }
        }

        self.graph = []

    #Credit : http://matthiaseisen.com/articles/graphviz/
    #Applies style dictionary to Graph object
    def apply_styles(self):
            self.graph.graph_attr.update(
                ('graph' in self.styles and self.styles['graph']) or {}
            )
            self.graph.node_attr.update(
                ('nodes' in self.styles and self.styles['nodes']) or {}
            )
            self.graph.edge_attr.update(
                ('edges' in self.styles and self.styles['edges']) or {}
            )

    #Generates Graphviz DiGraph object
    def gen_suffix_graph(self,suffix_tree, **kwargs):

        #TODO: Implement **kwargs structure
        '''kwargs guide:
            @filename: filename for graphviz visualization
            @name: name of graph '''

        dna = suffix_tree.dna
        self._styles['graph']['label'] = dna
        traversal = suffix_tree.traverse_tree()

        self.graph = Digraph(filename='./graphs/'+dna+'_stree',name=dna+'_stree')

        #Perform traversal and output tree shape
        for _,edges,s_links in traversal:
            if edges:
                for edge in edges:
                    self.graph.edge(str(edge[0]),str(edge[1]),label=(edge[2]))
            if s_links:
                self.graph.edge(str(edge[0]),str(s_links[0].node_id),style='dotted')

    def view(self):
        self.apply_styles()
        self.graph.view()

    ## Properties

    @property
    def styles(self):
        return self._styles
    @styles.setter
    def styles(self,styles):
        self._styles = styles
