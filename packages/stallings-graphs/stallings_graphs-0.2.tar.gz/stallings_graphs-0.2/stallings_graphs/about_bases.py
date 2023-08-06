# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions. These are the functions which deal with bases: determining one, parsing a word along a given basis.

A word is a string of characters from either a numerical or an alphabetical set
of letters: ``alphabet_type='123'`` or ``'abc'``.

``alphabet_type='123'``: The positive letters form an interval `[1,r]`. Their inverses (aka
negative letters) are the corresponding negative integers. The symmetrized
alphabet is the union of positive and negative letters (zero is NOT a letter).
The `\textit{rank}` of a word is the maximal absolute value of a letter occurring in the word.
When represented in a (say LaTeX) file (``.tex``, ``.pdf``), the letters are written
`a_i`.

``alphabet_type='abc'``: positive letters are lower case (at most 26 letters, `a`:`z`)
and their inverses are the corresponding upper case letters (`A`:`Z`).

Automata are objects of class ``DiGraph`` whose edge labels are positive letters (always numerical).
When automata are visualized, the value of ``alphabet_type`` determines how these edge labels will appear. In most cases, the vertex set of a ``DiGraph`` is a set of integers, usually of the form `[0..n]`.

We have functions to:

- compute a spanning tree

- compute a basis specified by a spanning tree

- express a Word in a basis specified by a spanning tree

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

- Pascal WEIL (2018-06-09): initial version
  CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr>

"""

#from sage.misc.prandom import randint
from sage.combinat.words.word import Word
from sage.graphs.digraph import DiGraph
#from sage.sets.disjoint_set import DisjointSet
#from sage.misc.latex import LatexExpr
#
from stallings_graphs.partial_injections import PartialInjection
#from stallings_graphs.partial_injections_misc import *
#from about_words import *


def spanning_tree_and_paths(G,root=0):
    r"""
    Return a spanning tree `T` of this ``DiGraph``, a list of the leaves of `T`, and shortest paths in `T`, from the root to each vertex.
    
    ``G`` is expected to be a ``DiGraph`` with numerical edge labels. Computes a spanning tree `T`
    (also a ``DiGraph``) by `\textit{breadth first search}` starting at vertex ``root`` --, along with a list of the non-root
    leaves of `T`, and a dictionary associating with each vertex `v` the word labeling the geodesic path in `T`
    from ``root`` to `v`.
    
    INPUT:

    - ``G`` -- ``DiGraph``
    - ``root`` -- a vertex of ``G``

    OUTPUT: 

    - a triple consisting of a ``DiGraph``, a list and a dictionary

    EXAMPLES::
    
        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_bases import spanning_tree_and_paths
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: H = FinitelyGeneratedSubgroup.from_generators(L)
        sage: G = H.stallings_graph()
        sage: T,list_of_leaves,path_in_tree = spanning_tree_and_paths(G)
        sage: T
        Multi-digraph on 12 vertices
        
    ::
        
        sage: list_of_leaves
        [2, 10, 3, 6, 5]
        
    ::
        
        sage: path_in_tree
        {0: word: ,
         1: word: 3,
         2: word: 31,
         3: word: -3,1,
         4: word: -3,
         5: word: 1,2,-1,
         6: word: -2,-1,
         7: word: -2,
         8: word: 1,
         9: word: 12,
         10: word: -1,3,
         11: word: -1}
        
    """
    to_be_handled = []
    to_be_handled.append(root)
    visited_vertices = set()
    visited_edges = []
    list_of_leaves = []
    path_in_tree = {}
    path_in_tree[root] = Word()
    from stallings_graphs.about_words import inverse_letter
    while to_be_handled:
        v = to_be_handled[0]
        to_be_handled[:1] = []
        visited_vertices.add(v)
        is_leaf = True
        if v == root:
            is_leaf = False
        for w in G.neighbors_out(v):
            if w != v and w not in visited_vertices:
                visited_vertices.add(w)
                to_be_handled.append(w)
                x = G.edge_label(v,w)[0]
                visited_edges.append((v,w,x))
                path_in_tree[w] = path_in_tree[v] + Word([x])
                is_leaf = False
        for w in G.neighbors_in(v):
            if w != v and w not in visited_vertices:
                visited_vertices.add(w)
                to_be_handled.append(w)
                x = G.edge_label(w,v)[0]
                visited_edges.append((w,v,x))
                path_in_tree[w] = path_in_tree[v] + Word([inverse_letter(x)])
                is_leaf = False
        if is_leaf:
            list_of_leaves.append(v)
    return DiGraph(visited_edges,multiedges = True), list_of_leaves, path_in_tree

def basis_from_spanning_tree(G, T, D, root=0,alphabet_type='abc'):
    r"""
    Return the basis (of the space of loops of ``G``at the ``root`` vertex) specified by the spanning tree ``T``.

    ``G`` is expected to be a folded ``DiGraph`` with numerical edge labels. ``T`` (also a ``DiGraph``)
    is expected to be a spanning tree of ``G``. ``D`` is expected to be a dictionary associating with each
    vertex `v` of ``G`` (and ``T``) the word labeling the geodesic path in ``T``
    from ``root`` to `v`. The output basis is a list of objects of class ``Word`` on a numerical alphabet, one
    for each edge of ``G`` that is not in ``T``.
    
    INPUT:

    - ``G`` -- ``DiGraph``
    - ``T`` -- ``DiGraph``       
    - ``D`` -- dictionary (the keys are the vertices of ``G`` and the values are of class ``Word``)
    - ``root`` -- a vertex of ``G``

    OUTPUT: 

    - a list of objects of class ``Word`` (in numerical or alphabetic form)

    EXAMPLES::
    
        sage: from stallings_graphs.about_automata import bouquet
        sage: from stallings_graphs.about_bases import spanning_tree_and_paths, basis_from_spanning_tree
        sage: from stallings_graphs.about_folding import NT_fold
        sage: generators = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = NT_fold(bouquet(generators))
        sage: T,L,D = spanning_tree_and_paths(G)
        sage: basis_from_spanning_tree(G,T,D,alphabet_type='123')
        [word: -3,1,2,-1,-3, word: -2,-1,2,1,-2,-1, word: -1,3,3,-2,-1]

    ::

        sage: basis_from_spanning_tree(T,T,D)
        []

    """
    basis = []
    edge_set = set(G.edges()).difference(set(T.edges()))
    from stallings_graphs.about_words import group_inverse
    for e in G.edges():
        if e not in T.edges():
            w = D[e[0]] + Word([e[2]]) + group_inverse(D[e[1]])
            basis.append(w)
    if alphabet_type == 'abc':
        from stallings_graphs.about_words import translate_numeric_Word_to_alphabetic
        basis = [translate_numeric_Word_to_alphabetic(w) for w in basis]
    return basis

def tree_based_interpreter(w, G, T, root=0, alphabet_type = 'abc'):
    r"""
    Return the expression of the Word ``w`` in the basis (of the space of loops
    of ``G``at the ``root`` vertex) specified by the spanning tree ``T``.

    ``w`` is expected to be a Word in alphabetic or numerical form, depending on
    ``alphabet_type''. In addition, ``w``is expected to label a loop at vertex
    ``root`` in the folded ``DiGraph`` ``G`` (with numerical edge labels).
    ``T`` (also a ``DiGraph``) is expected to be a spanning tree of ``G``.
    The output is a numerical Word which is the translation of ``w`` in the alphabet
    of the basis defined by ``T``.
    
    INPUT:

    - ``G`` -- ``DiGraph``
    - ``T`` -- ``DiGraph``        
    - ``w`` -- ``Word``        
    - ``root`` -- a vertex of ``G``
    - ``alphabet_type`` -- string, which can be either ``'abc'`` or ``'123'``

    OUTPUT: 

    - ``Word`` (in numerical form)

    EXAMPLES::
    
        sage: from stallings_graphs.about_automata import bouquet
        sage: from stallings_graphs.about_bases import spanning_tree_and_paths, basis_from_spanning_tree, tree_based_interpreter
        sage: from stallings_graphs.about_folding import NT_fold
        sage: generators = ['abaa','ababb','ababab']
        sage: G = NT_fold(bouquet(generators,alphabet_type = 'abc'))
        sage: T,L,D = spanning_tree_and_paths(G)
        sage: basis_from_spanning_tree(G,T,D)
        [word: abaa, word: Abb, word: Bab]

    ::

        sage: w = Word('AbaabAABABab')
        sage: tree_based_interpreter(w,G,T)
        word: 2,3,3,-1,3


    """
    if alphabet_type == 'abc':
        from stallings_graphs.about_words import translate_alphabetic_Word_to_numeric
        u = translate_alphabetic_Word_to_numeric(w)
    else:
        u = w
    from stallings_graphs.about_automata import DiGraph_to_list_of_PartialInjection
    PI = DiGraph_to_list_of_PartialInjection(G)
    PIinv = [p.inverse_partial_injection() for p in PI]
    translated = []
    basis_list = []
    for e in G.edges():
        if e not in T.edges():
            basis_list.append(e)
    current_state = root
    for a in u:
        if current_state == None:
            raise ValueError('the 1st argument does not label a loop at the root')
        if a > 0:
            mapping = PI[a-1]
            next_state = mapping._list_of_images[current_state]
            current_transition = (current_state,next_state,a)
            if current_transition in basis_list:
                next_letter = 1 + basis_list.index(current_transition)
                translated.append(next_letter)
        elif a < 0:
            mapping = PIinv[-a-1]            
            next_state = mapping._list_of_images[current_state]
            current_transition = (next_state,current_state,-a)
            if current_transition in basis_list:
                next_letter = 1 + basis_list.index(current_transition)
                translated.append(-next_letter)
        elif a == 0:
            raise ValueError('the 1st argument is not a proper numerical Word (contains a non acceptable character')
        current_state = next_state
    if current_state != root:
        raise ValueError('the 1st argument does not label a loop at the root')
    return Word(translated)


def basis_interpreter(L, C, alphabet_type = 'abc', check = False):
    r"""
    Returns the translations of a list of words into words (in numerical form) on basis ``C``.

    ``L``and ``C`` are expected to be lists of words in the same format, alphabetic
    or numerical, specified by ``alphabet_type''. Each word in ``L`` is expected to be in
    the subgroup generated by ``C``. This is verified if ``check`` is set to ``True``.
    
    INPUT:

    - ``L`` -- list of objects of type ``Word``
    - ``C`` -- list of objects of type ``Word``
    - ``alphabet_type`` -- string, which can be either ``'abc'`` or ``'123'``
    - ``check``-- boolean

    OUTPUT: 

    - list of objects of type ``Word`` (in numerical form)

    EXAMPLES::
    
        sage: from stallings_graphs.finitely_generated_subgroup import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_bases import basis_interpreter
        sage: generators = ['abbC','aabCa','aaCBA','cBa']
        sage: w = Word('abcbCbCabcAA')
        sage: basis_interpreter([Word([])], generators, alphabet_type = 'abc', check = False)
        [word: ]
        
    ::
        
        sage: basis_interpreter([w], generators, alphabet_type = 'abc', check = False)
        [word: -3,2,-4,-3]
        
    ::
        
        sage: ww = Word('abcbCcBabcAA')
        sage: basis_interpreter([w,Word([])], generators, alphabet_type = 'abc', check = False)
        [word: -3,2,-4,-3, word: ]


    """
    from stallings_graphs.finitely_generated_subgroup import FinitelyGeneratedSubgroup
    H = FinitelyGeneratedSubgroup.from_generators(C,alphabet_type=alphabet_type)
    if check:
        if len(C) != H.rank():
            raise ValueError('the 2nd argument is not a basis of the subgroup it generates')
        if not all(H.contains_element(x,alphabet_type=alphabet_type) for x in L):
            raise ValueError('the 1st argument is not a list of elements of the subgroup generated by the 2nd argument')
#        
    G = H.stallings_graph()
#    r = H.rank()
    T,Leaves,D = spanning_tree_and_paths(G)
    B = basis_from_spanning_tree(G, T, D, root=0,alphabet_type=alphabet_type)
    LB = [tree_based_interpreter(x, G, T, root=0, alphabet_type=alphabet_type) for x in L]
#    if alphabet_type == 'abc':
#        from stallings_graphs.about_words import translate_alphabetic_Word_to_numeric
#        B = [translate_alphabetic_Word_to_numeric(w) for w in B]
    TrC = [tree_based_interpreter(c, G, T, root=0, alphabet_type=alphabet_type) for c in C]
#    for i in range(r):
#        value = tree_based_interpreter(B[i], G, T, root=0, alphabet_type=alphabet_type)
#        TrB["x%s" % i] = translate_numeric_Word_to_x0_list(value)
    from stallings_graphs.about_TC_morphisms import FGendomorphism, image_of_Word_by_endomorphism
    psiC = FGendomorphism(TrC, alphabet_type='123')
#    phiB = FGendomorphism(B, alphabet_type=alphabet_type)
#    TrC = {}
#    for i in range(r):
#        value = tree_based_interpreter(C[i], G, T, root=0, alphabet_type=alphabet_type)
    
#    phi = FGendomorphism(B, alphabet_type='123')
#    chi = psiC.inverse()*phi
    chi = psiC.inverse()
#    
    return [image_of_Word_by_endomorphism(chi, x, alphabet_type = '123') for x in LB]




