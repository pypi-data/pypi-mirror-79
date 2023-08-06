# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions. These are the functions which deal with the crucial operation of folding a ``DiGraph``.

The algorithm used here is based on an
article by Nicholas Touikan, Intern. J. Algebra and Computation, vol 16, 2006,
pages 1031--1045], and it ought to have time complexity `O(n\ \log^*n)` -- that is: very
efficient. It uses in a crucial way the Union-Find algorithm, implemented in the
``DisjointSet`` class.

The ``DiGraph`` to be folded is expected to have numerical edge labels and to have a
vertex set of the form `[0..n]`.


EXAMPLES::

    sage: from stallings_graphs.about_words import random_reduced_word
    sage: L = ['aBABBaaaab', 'BBAbbABABA', 'bbAbAbaabb']
    sage: from stallings_graphs.about_automata import bouquet
    sage: G = bouquet(L, alphabet_type='abc')
    sage: from stallings_graphs.about_folding import NT_fold
    sage: GG = NT_fold(G)
    sage: GG
    Looped multi-digraph on 23 vertices


AUTHOR:

- Pascal WEIL, CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr>: initial version (2018-06-09)

"""

#from sage.misc.prandom import randint
#from sage.combinat.words.word import Word
from sage.graphs.digraph import DiGraph
from sage.sets.disjoint_set import DisjointSet
#from sage.misc.latex import LatexExpr
#
#from partial_injections import PartialInjection
from about_words import *
from about_automata import *

    
def NT_data_structures_initialization(digr):
    r"""
    Return the necessary data to initiate the folding of a labeled ``DiGraph``.
    
    ``digr`` is expected to be a labeled ``DiGraph``, with vertex set of the form `[0..n-1]`
    and edges labeled by integers in `[1..r]`. In this preliminary step of the folding
    algorithm, the edges of ``digr`` are organized in a dictionary of dictionaries
    and the vertices of ``digr`` are organized in a ``DisjointSet`` structure (to later use
    the union-find algorithm). The dictionary of dictionaries is a variant of the data
    structure used by Nicholas Touikan in his folding algorithm.
    
    INPUT:

        - ``digr`` -- ``DiGraph``

    OUTPUT: 

        - A tuple consisting of a dictionary of dictionaries and a ``DisjointSet`` object

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import bouquet
        sage: from stallings_graphs.about_folding import NT_data_structures_initialization
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: NT_data_structures_initialization(G)
        ({{0}, {10}, {11}, {12}, {13}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}},
         {1: {0: [{13}, {5, 10}],
           1: [set(), {2}],
           2: [{1}, set()],
           3: [{4}, set()],
           4: [set(), {3}],
           5: [{0}, set()],
           6: [{7}, set()],
           7: [set(), {6}],
           8: [set(), {9}],
           9: [{8}, set()],
           10: [{0}, set()],
           11: [set(), set()],
           12: [set(), set()],
           13: [set(), {0}]},
          2: {0: [{9}, set()],
           1: [set(), set()],
           2: [{3}, set()],
           3: [set(), {2}],
           4: [set(), set()],
           5: [set(), {6}],
           6: [{5}, set()],
           7: [{8}, set()],
           8: [set(), {7}],
           9: [set(), {0}],
           10: [set(), {11}],
           11: [{10}, set()],
           12: [set(), set()],
           13: [set(), set()]},
          3: {0: [{4}, {1}],
           1: [{0}, set()],
           2: [set(), set()],
           3: [set(), set()],
           4: [set(), {0}],
           5: [set(), set()],
           6: [set(), set()],
           7: [set(), set()],
           8: [set(), set()],
           9: [set(), set()],
           10: [set(), set()],
           11: [{12}, set()],
           12: [{13}, {11}],
           13: [set(), {12}]}})
    
    """
    # r is the maximum (numeric) value of the edge labels of digr.
    if digr.edges():
        r = max(digr.edge_labels())
    else:
        r = 0
    # NT_vertices initially holds the partition of the vertex set of digr,
    # each in its own singleton
    NT_vertices = DisjointSet(digr.vertices())
    ### NT_rank maps every vertex to an integer, its depth in the tree
    ### underlying the DisjointSet (union-find) data structure NT_vertices
    ### NT_rank = [0 for _ in digr.vertices()]
    # NT_edge_structure is a dictionary, whose keys are the alphabet letters.
    # The i-entry is a dictionary whose keys are the vertices.
    # NT_edge_structure[i][u] is a list [incoming,outgoing], where incoming is 
    # the set of initial vertices of i-labeled edges ending at u; and
    # outgoing is the set of terminal vertices of i-labeled edges starting at u.
    NT_edge_structure = {i:{u: [set(),set()] for u in digr.vertices()} for i in positive_letters(r)}
    for e in digr.edges():
        NT_edge_structure[e[2]][e[1]][0].add(e[0])
        NT_edge_structure[e[2]][e[0]][1].add(e[1])

    return NT_vertices,NT_edge_structure

def NT_is_vertex_unfolded(v,NT_vertices,NT_edge_structure):
    r"""
    Return whether this vertex is unfolded in the given ``DisjointSet`` structure.
    
    ``v`` is expected to be an element of the vertex set `V` of a graph, ``NT_vertices``
    is a ``DisjointSet`` object based on `V` and ``NT_edge_structure`` is a dictionary of dictionaries.
    The method detects whether the root of `v` in ``NT_vertices`` is unfolded, that is,
    whether for some letter `i`, ``NT_edge_structure[i][w][0]`` or
    ``NT_edge_structure[i][w][1]`` has at least 2 elements --- after updating
    these sets using the ``NT_vertices.find`` operator.
    
    INPUT:

        - ``digr`` -- ``DiGraph``

        - ``NT_vertices`` -- ``DisjointSet``

        - ``NT_edge_structure`` -- dictionary of dictionaries

    OUTPUT: 

        - boolean

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import bouquet
        sage: from stallings_graphs.about_folding import NT_data_structures_initialization, NT_is_vertex_unfolded
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: NT_vertices,NT_edge_structure = NT_data_structures_initialization(G)
        sage: NT_is_vertex_unfolded(0,NT_vertices,NT_edge_structure)
        True
        
        ::
        
        sage: NT_is_vertex_unfolded(2,NT_vertices,NT_edge_structure)
        False
    
    """
    answer = False
    w = NT_vertices.find(v)
    for i in NT_edge_structure.keys():
        NT_edge_structure[i][w][0] = set([NT_vertices.find(u) for u in NT_edge_structure[i][w][0]])
        NT_edge_structure[i][w][1] = set([NT_vertices.find(u) for u in NT_edge_structure[i][w][1]])
        if (len(NT_edge_structure[i][w][0]) > 1) or (len(NT_edge_structure[i][w][1]) > 1):
            answer = True
    return answer
        
def NT_initially_unfolded_construction(digr,NT_vertices,NT_edge_structure):
    r"""
    Returns the set of unfolded vertices in this ``DiGraph`` at the beginning of the folding algorithm.
    
    ``digr`` is expected to be a ``DiGraph``, ``NT_vertices`` is a ``DisjointSet`` structure based
    on the vertices of ``digr`` and ``NT_edge_structure`` is a dictionary based on the edges of ``digr``.
    This method is meant to be used once, when the input defining a subgroup is a NFA with
    one initial-final state. (If the ``DiGraph`` is a bouquet of freely reduced words,
    then ``NT_initially_unfolded`` could be set immediately to ``set([0])``.)
    
    INPUT:

        - ``digr`` -- ``DiGraph``

        - ``NT_vertices`` -- ``DisjointSet``

        - ``NT_edge_structure`` -- dictionary of dictionaries

    OUTPUT: 

        - set

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import bouquet
        sage: from stallings_graphs.about_folding import NT_data_structures_initialization, NT_initially_unfolded_construction
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: NT_vertices,NT_edge_structure = NT_data_structures_initialization(G)
        sage: NT_initially_unfolded_construction(G,NT_vertices,NT_edge_structure)
        {0}
        
    """
    NT_initially_unfolded = set()
    for v in digr.vertices():
        if NT_is_vertex_unfolded(v,NT_vertices,NT_edge_structure):
            NT_initially_unfolded.add(v)
    return NT_initially_unfolded


def NT_fold_edge(NT_vertices,NT_edge_structure,NT_unfolded,u,v1,v2):
    r"""
    Performs the crucial step of folding two edges.
    
    ``NT_vertices``, ``NT_edge_structure`` are expected to be the data structures
    (see ``NT_data_structures_initialization``) associated with a ``DiGraph``.
    ``NT_unfolded`` is the current set of unfolded vertices, ``u`` sits in that set,
    ``v1`` and ``v2`` are distinct vertices such that, for some letter `a` (a key in
    ``NT_edge_structure``), ``v1`` and ``v2``  are both in ``NT_edge_structure[a][u][0]``
    (outgoing edges) or both in ``NT_edge_structure[a][u][1]`` (incoming edges).
    The method returns updated versions of ``NT_vertices``, ``NT_edge_structure``,
    ``NT_unfolded`` after the `a`-labeled edges out of ``u`` and into ``v1`` and ``v2`` (resp.
    into ``u`` out of ``v1`` and ``v2``) are merged.
    
    INPUT:

        - ``NT_vertices`` -- `DisjointSet`

        - ``NT_edge_structure`` -- dictionary of dictionaries
        
        - ``NT_unfolded`` -- set
        
        - ``u`` -- element
        
        - ``v1`` -- element
        
        - ``v2`` -- element

    OUTPUT: 

        - the input objects ``NT_vertices``, ``NT_edge_structure`` and ``NT_unfolded`` are modified in place

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import bouquet
        sage: from stallings_graphs.about_folding import NT_data_structures_initialization, NT_initially_unfolded_construction, NT_fold_edge
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: NT_vertices,NT_edge_structure = NT_data_structures_initialization(G)
        sage: NT_unfolded = set([0])
        sage: NT_fold_edge(NT_vertices,NT_edge_structure,NT_unfolded,0,5,10)
        
    """
    # the vertices to be merged are in fact the roots of v1 and v2
    # in the NT_vertices DisjointSet
    r1 = NT_vertices.find(v1)
    r2 = NT_vertices.find(v2)
    NT_vertices.union(r1,r2)
    s = NT_vertices.find(r1)
    # updating the data structure by merging the incoming and outgoing sets
    # of vertices adjacent to r1 and r2, for each letter (that the purpose
    # of NT_edge_structure); removing r2 from the set of unfolded vertices
    # (in case it was there); adding r1 and u to the set of unfolded
    # vertices if they are still unfolded (note that u was noted as unfolded
    # at the start, but was popped out of that set (in function NT_fold) when
    # launching this function).
    for i in NT_edge_structure.keys():
        NT_edge_structure[i][s][0] = set(NT_vertices.find(x) for x in NT_edge_structure[i][r1][0].union(NT_edge_structure[i][r2][0]))
        NT_edge_structure[i][s][1] = set(NT_vertices.find(x) for x in NT_edge_structure[i][r1][1].union(NT_edge_structure[i][r2][1]))
    NT_unfolded.discard(r1)
    NT_unfolded.discard(r2)
    if NT_is_vertex_unfolded(s,NT_vertices,NT_edge_structure):
        NT_unfolded.add(s)
    if NT_is_vertex_unfolded(u,NT_vertices,NT_edge_structure):
        NT_unfolded.add(NT_vertices.find(u))

def NT_fold(digr):
    r"""
    Returns the folded version of this ``DiGraph`` (with base vertex 0).
    
    ``digr`` is expected to be a ``DiGraph`` with vertex set of the form `[0..n]`. The base
    vertex after folding is still called 0. The set of vertices of the output ``DiGraph``
    is of the form `[0..n]`: this is not reflecting the name of vertices in the original
    ``DiGraph`` -- except for the base vertex.
    
    INPUT:

        - ``digr`` -- ``DiGraph``

    OUTPUT: 

        - ``DiGraph``

    EXAMPLE ::
        
        sage: from stallings_graphs.about_words import translate_alphabetic_Word_to_numeric
        sage: from stallings_graphs.about_automata import show_rooted_graph, bouquet
        sage: from stallings_graphs.about_folding import NT_fold
        sage: L1 = ['bABcac','abcBA','baaCB','abABcaCA']
        sage: L2 = [translate_alphabetic_Word_to_numeric(w) for w in L1]
        sage: G = bouquet(L2)
        sage: GG = NT_fold(G)
        sage: show_rooted_graph(GG, base_vertex=0)
        Graphics object consisting of 62 graphics primitives
    
    """
    NT_vertices,NT_edge_structure = NT_data_structures_initialization(digr)
    NT_unfolded = NT_initially_unfolded_construction(digr,NT_vertices,NT_edge_structure)
    while NT_unfolded:
#        print 'NT_unfolded is', NT_unfolded
        u = NT_unfolded.pop()
#        print 'I popped {} from NT_unfolded'.format(u)
        if NT_is_vertex_unfolded(u,NT_vertices,NT_edge_structure):            
            a = 1
            while len(NT_edge_structure[a][u][0]) < 2 and len(NT_edge_structure[a][u][1]) < 2:
                a = a + 1
            if len(NT_edge_structure[a][u][0]) > 1:
                i = 0
            else:
                i = 1
            v1 = NT_edge_structure[a][u][i].pop()
            v2 = NT_edge_structure[a][u][i].pop()
#            print 'it turns out I need to merge {} and {}'.format(v1,v2)
#            print '{} is a root right now?'.format(v1),v1 == NT_vertices.find(v1)
#            print '{} is a root right now?'.format(v2),v2 == NT_vertices.find(v2)
            NT_edge_structure[a][u][i].add(v1)
            NT_edge_structure[a][u][i].add(v2)
            NT_fold_edge(NT_vertices,NT_edge_structure,NT_unfolded,u,v1,v2)
 #       else:
 #           print 'I found a case where a registered unfolded vertex was in fact folded'
    folded_vertices = NT_vertices.root_to_elements_dict().keys()
  #  print 'folded_vertices is', folded_vertices
    folded_edges_temp = set()
    for a in NT_edge_structure.keys():
        for u in folded_vertices:
            for v in NT_edge_structure[a][u][0]:
                #[0] is incoming
                folded_edges_temp.add((NT_vertices.find(v),u,a))
            for v in NT_edge_structure[a][u][1]:
                #[1] is outgoing
                folded_edges_temp.add((u,NT_vertices.find(v),a))
    folded_edges = [x for x in folded_edges_temp]
#
# now make sure that the base vertex is still called 0
    r = NT_vertices.find(0)
    if r != 0:
        for i in range(len(folded_edges)):
            if folded_edges[i][0] == r:
                folded_edges[i] = (0,folded_edges[i][1],folded_edges[i][2])
            if folded_edges[i][1] == r:
                folded_edges[i] = (folded_edges[i][0],0,folded_edges[i][2])
        folded_vertices.remove(r)
        folded_vertices.append(0)
#
# now rename the vertices so that they form an initial segment [0..n]
    GG = DiGraph([folded_vertices,folded_edges], format='vertices_and_edges', loops=True, multiedges=True)
    GGG = normalize_vertex_names(GG)
#
    return GGG


