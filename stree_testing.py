from suffix_tree_builder import SuffixTree, SuffixBuilder
from suffix_tree_graph import SuffixGraph

if __name__ == '__main__':
    dna = 'ABCABXABCD'
    
    #Build tree
    s_builder = SuffixBuilder(dna)
    s_tree = s_builder.build_tree()

    #Create graphing object
    s_graph = SuffixGraph()
    s_graph.gen_suffix_graph(s_tree)
    s_graph.view()
