# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions. These are the functions which deal with graphs and automata, in the context of group theory.

A word is a string of characters from either a numerical or an alphabetical set
of letters: ``alphabet_type='123'`` or ``'abc'``.

``alphabet_type='123'``: The positive letters form an interval `[1,r]`. Their inverses (a.k.a.
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

- compute the bouquet of a list of ``Word`` (of ``alphabet_type`` ``'123'`` or ``'abc'``)

- extract from a ``DiGraph`` the list of its transitions (one for each letter labeling an edge)

- determine whether a ``DiGraph`` is deterministic and in that case, compute the transition functions (one for each letter labeling an edge)

- determine whether a ``DiGraph`` is folded and in that case, compute the corresponding tuple of partial injections (objects of class ``PartialInjection``)

- relabel vertices

- permute the names of two vertices

- normalize its vertex set (so it is `[0..n]`)

- compute the image of a word in a ``DiGraph``

- prune a ``DiGraph``

- cyclically reduce a ``DiGraph``

- compute the fibered product of two objects of class ``DiGraph``

- prepare a rooted ``DiGraph`` to be visualized using ``TikzPicture`` with ``alphabet_type`` ``'123'`` or ``'abc'``

- show a rooted ``DiGraph`` (using ``graph.plot``), with the root in a different color

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
from sage.misc.latex import LatexExpr
#
from stallings_graphs.partial_injections import PartialInjection
from stallings_graphs.partial_injections_misc import *
from stallings_graphs.about_words import *


def bouquet(list_of_Words, alphabet_type='123', check=False):
    r"""
    Return the bouquet of loops labeled by this list of words.
    
    ``list_of_Words`` is expected to be a List of objects of class ``Word`` on a symmetric alphabet which is
    numerical (``alphabet_type = '123'``) or consists of letters (``alphabet_type = 'abc'``).
    The option ``check = True`` verifies that this argument is a valid list of ``Word`` over the
    given ``alphabet_type``.
    The bouquet in question is a ``DiGraph`` with vertex set of the form `[0..n]`, where every
    word in ``list_of_Words`` labels a loop at vertex 0. The edges are labeled by letters from
    the symmetric alphabet.
    
    INPUT:

        - ``list_of_Words`` -- List of ``Word``
        
        - ``alphabet_type`` -- string, which is either ``'123'`` or ``'abc'``
        
        - ``check`` -- boolean

    OUTPUT:

        - ``DiGraph``
                
    EXAMPLES::

        sage: from stallings_graphs.about_automata import bouquet, transitions
        sage: L = [[4,1,1,-4], [-4, -2, -1, 2, -1],[4]]
        sage: G = bouquet(L)
        sage: G
        Looped multi-digraph on 8 vertices
        
    ::

        sage: GG = bouquet([[-1]])
        sage: GG
        Looped multi-digraph on 1 vertex
        
    """
    if check:
        if not is_valid_list_of_Words(list_of_Words,alphabet_type):
            raise ValueError('the first argument is not a valid list of words, with respect to the alphabet type.')
    if alphabet_type == 'abc':
        new_list_of_Words = [translate_alphabetic_Word_to_numeric(w) for w in list_of_Words]
    else:
        new_list_of_Words = list_of_Words
    edge_list = []
    m = 0
    for u in new_list_of_Words:
        new_edge_list = []
        if len(u) == 1:
            if u[0] > 0:
                new_edge_list.append([0,0,u[0]])
            else:
                new_edge_list.append([0,0,inverse_letter(u[0])])
        elif len(u) > 1:
            if u[0] > 0:
                new_edge_list.append([0,m + 1,u[0]])
            else:
                new_edge_list.append([m + 1,0,inverse_letter(u[0])])
            for i in range(1,len(u) - 1):
                if u[i] > 0:
                    new_edge_list.append([m + i,m + i + 1,u[i]])            
                else:
                    new_edge_list.append([m + i + 1,m + i,inverse_letter(u[i])])
            if u[-1] >0:
                new_edge_list.append([m + len(u) - 1,0,u[-1]])
            else:
                new_edge_list.append([0, m + len(u) - 1,inverse_letter(u[-1])])
        edge_list.extend(new_edge_list)
        m = m + len(u) - 1
    
    vertex_list = range(m + 1)

    G = DiGraph([vertex_list, edge_list], format='vertices_and_edges',
                loops=True, multiedges=True)
    return G 

def transitions(digr):
    r"""
    Return a dictionary of the transitions (edges) of this ``DiGraph``, organized by edge labels.
    
    ``digr`` is expected to be a ``DiGraph``, with labeled edges and with vertex set of
    the form `[0..n]`. The output dictionary maps each edge label to a list of sets:
    the image of edge label `a` is a list indexed by the vertex set, where
    the `v`-entry is the set of end vertices of `a`-labeled edges out of `v`, or
    ``None`` if that set is empty.
    
    INPUT:

        - ``digr`` -- ``DiGraph``

    OUTPUT:

        - dictionary
                
    EXAMPLES::

        sage: from stallings_graphs.about_automata import bouquet, transitions
        sage: L = [[4,1,1,-4], [-4, -2, -1, 2, -1]]
        sage: G = bouquet(L)
        sage: transitions(G)
        {1: [{7}, {2}, {3}, None, None, None, {5}, None],
         2: [None, None, None, None, None, {4}, {7}, None],
         4: [{1, 3}, None, None, None, {0}, None, None, None]}
    """
    alphabet = set()
    for x in digr.edge_labels():
        alphabet.add(x)
    emptyset = set()
    transitions_dict = {}
    for x in alphabet:
        transitions_dict[x] = [set() for _ in digr.vertices()]
    for e in digr.edges():
        transitions_dict[e[2]][e[0]].add(e[1])
    for x in alphabet:
        for v in digr.vertices():
            if len(transitions_dict[x][v]) == 0:
                transitions_dict[x][v] = None
    return transitions_dict

def is_deterministic(digr):
    r"""
    Return whether this ``DiGraph`` is deterministic.
    
    ``digr`` is expected to be a ``DiGraph`` with labeled edges and with vertex set of
    the form `[0..n]`. It is said to be deterministic if for each vertex `v` and each
    label `a`, there is at most one `a`-labeled edge out of `v`.
    
    INPUT:

        - ``digr`` -- ``DiGraph``

    OUTPUT:

        - boolean
                
    EXAMPLES ::
        
        sage: from stallings_graphs.about_automata import bouquet, is_deterministic
        sage: L = [[3,1,1,-3], [-3, -2, -1, 2, -1]]
        sage: digr = bouquet(L)
        sage: is_deterministic(digr)
        False
    """
#    all(all(len(x) == 1 for x in L if x != None) for L in transitions(digr).values())
    determin = True
    for L in transitions(digr).values():
        for x in L:
            if x != None and len(x) > 1:
                determin = False
    return determin
    
def transition_function(digr):
    r"""
    Return a dictionary of the transitions (edges) of this ``DiGraph``.
    
    ``digr`` is expected to be a deterministic ``DiGraph`` (a ``ValueError`` is raised otherwise),
    with edge labels positive integers. The output dictionary maps each edge label to a list:
    the image of edge label `a` is a list indexed by the vertex set, where
    the `v`-entry is ``None`` if one cannot read `a` from `v`, and the result of the
    `a`-transition from `v` otherwise.
    
    INPUT:

        - ``digr`` -- ``DiGraph``

    OUTPUT:

        - dictionary
                
    EXAMPLES ::

        sage: from stallings_graphs.about_automata import bouquet, transition_function
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[-1,2,-3,-3,1]]
        sage: digr = bouquet(L)
        sage: transition_function(digr)
        {1: [5, 2, None, None, 3, None, None, 6, 9, None, 0, None, None, 0],
         2: [None, None, None, 2, None, 6, None, None, 7, 0, 11, None, None, None],
         3: [1, None, None, None, 0, None, None, None, None, None, None, None, 11, 12]}
         """
    if not is_deterministic(digr):
        raise ValueError('the argument is not a deterministic DiGraph')
    D = transitions(digr)
    E = {}
    for a in D.keys():
        M = [None for _ in D[a]]
        for i,x in enumerate(D[a]):
            if x != None:
                M[i] = x.pop()
        E[a] = M
    return E

def is_folded(G):
    r"""
    Return whether this ``DiGraph`` is folded (deterministic and co-deterministic).
    
    ``G`` is expected to be a ``DiGraph`` with labeled edges and with vertex set of
    the form `[0..n]`. It is said to be deterministic if for each vertex `v` and each
    label `a`, there is at most one `a`-labeled edge out of `v`; and co-deterministic if
    for each vertex `v` and label `a`, there is at most one `a`-labeled edge into `v`.
    
    INPUT:

        - ``G`` -- ``DiGraph``

    OUTPUT:

        - boolean
                
    EXAMPLES ::
        
        sage: from stallings_graphs.about_automata import bouquet, is_folded
        sage: L = [[-3,1,2,1], [3,2,1]]
        sage: G = bouquet(L)
        sage: is_folded(G)
        False
    """
    
    if is_deterministic(G)==False:
        return False
    L = transition_function(G)
    return all(is_valid_partial_injection(L[a]) for a in L.keys())
    

def DiGraph_to_list_of_PartialInjection(G):
    r"""
    Return the list of partial injections (in fact: objects of class ``PartialInjection``)
    on the set of vertices of this graph.
    
    ``G`` is expected to be a folded ``DiGraph`` (a ``ValueError`` is raised otherwise)
    with edge labels in `[1..r]` and vertex set equal to `[0..n-1]` (`r` and `n` not given).
    Folded means that the graph is deterministic and co-deterministic or, equivalently,
    that every edge label defines a partial injection on the vertex set. The list returned
    has size `r`, and represents the partial injections (from the class ``PartialInjection``)
    induced by edge labels `1, 2, \dots, r`, respectively.
    
    INPUT:

        - ``G`` -- ``DiGraph``

    OUTPUT:

        - List of lists
                
    EXAMPLES ::
    
        sage: from stallings_graphs import PartialInjection
        sage: from stallings_graphs.about_automata import bouquet, DiGraph_to_list_of_PartialInjection
        sage: from stallings_graphs.about_folding import NT_fold
        sage: from stallings_graphs import PartialInjection
        sage: L = [[3,1,-2,-1,-3],[-1,2,-1,-2,1,2],[3,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: GG = NT_fold(G)
        sage: DiGraph_to_list_of_PartialInjection(GG)
        [A partial injection of size 10, whose domain has size 4,
         A partial injection of size 10, whose domain has size 5,
         A partial injection of size 10, whose domain has size 3]
         
    ::
        
        sage: L = [[3,1,-2,-1,-3],[-1,2,-1,-2,1,2],[3,2,-3,-3,1],[5]]
        sage: G = bouquet(L)
        sage: GG = NT_fold(G)
        sage: DiGraph_to_list_of_PartialInjection(GG)
        [A partial injection of size 10, whose domain has size 4,
         A partial injection of size 10, whose domain has size 5,
         A partial injection of size 10, whose domain has size 3,
         A partial injection of size 10, whose domain has size 0,
         A partial injection of size 10, whose domain has size 1]
    
    """
    if not is_folded(G):
        raise ValueError('the argument is not a folded DiGraph')
    EL = set(G.edge_labels())
    if G.edges():
        r = max(EL)
    else:
        r = 0
    NV = len(G.vertices())
    pinj = [[None for _ in range(NV)] for _ in range(r)]
    for a in EL:
        pinj[a-1] = transition_function(G)[a]
    pinj = [PartialInjection(pinj[x]) for x in range(r)]
    return pinj


def image_of_word(G,w,qinitial=0,trace=False):
    r"""
    Return the vertex reached after reading this word in this graph (``None`` if it cannot be read).
    
    ``G`` is expected to be a ``DiGraph`` whose edges are labeled deterministically and
    codeterministically (folded ``DiGraph``) by a numerical alphabet (typically, ``G`` is a Stallings
    graph) [not verified], ``w`` is a ``Word`` on a numerical alphabet and ``qinitial``
    is a vertex of ``G``. If one can read ``w`` from ``qinitial`` in ``G``, the output is the vertex
    reached. If one cannot, the output is ``None``. The option ``trace=True`` documents
    the situation if ``w`` cannot be read in ``G``: the output is the triple
    (``None``, ``length_read``, ``last_vertex_visited``) where ``length_read`` is the length
    of the longest prefix ``u`` of ``w`` which can be read in ``G`` starting at ``qinitial`` and
    ``last_vertex_visited`` is the vertex reached after reading ``u``.
    
    INPUT:

        - ``G`` -- ``DiGraph``

        - ``w`` -- ``Word``

        - ``qinitial`` -- integer (state of ``G``)
        
        - ``trace`` -- boolean

    OUTPUT: 

        - integer or ``None`` if ``trace=False``; and if ``trace=True``, a triple consisting of three integers or ``None`` and two integers

    EXAMPLES ::

        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_automata import image_of_word
        sage: L = ['ab','ba', 'aBaa']
        sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
        sage: G = H.stallings_graph()
        sage: w = Word([1,-2,1,-1,1])
        sage: image_of_word(G,w, qinitial = 0,trace = True)
        (2, 5, 2)

    ::

        sage: image_of_word(G,w)
        2

    ::

        sage: ww = Word([1,2,-1,-2])
        sage: image_of_word(G,ww)
        0

    ::

        sage: w = Word([2,2,-1])
        sage: image_of_word(G,w, qinitial = 0,trace = True)
        (None, 1, 2)

    ::

        sage: image_of_word(G,w) is None
        True

    ::

        sage: w = Word()
        sage: image_of_word(G,w, qinitial = 0,trace = True)
        (0, 0, 0)

    ::

        sage: H = FinitelyGeneratedSubgroup([])
        sage: G = H.stallings_graph()
        sage: w = Word([2,2,-1])
        sage: image_of_word(G,w, qinitial = 0,trace = True)
        (None, 0, 0)

    ::

        sage: w = Word()
        sage: image_of_word(G,w, qinitial = 0,trace = True)
        (0, 0, 0)

    """
    PI = transition_function(G)
    if not PI:
        if len(w) == 0:
            return (qinitial, 0, qinitial) if trace else qinitial
        else:
            return (None, 0, qinitial) if trace else None
    # now if prePI is not the empty list
    for a in range(1,rank(w)+1):
        if a not in PI.keys():
            PI[a] = [None for _ in G.vertices()]
    PIinv = {}
    for a in PI.keys():
        pinj1 = PartialInjection(PI[a])
        pinj2 = pinj1.inverse_partial_injection()        
        PIinv[a] = pinj2._list_of_images
    q = qinitial
    length_read = 0
    last_vertex_visited = qinitial
    for a in w:
        if a > 0:
            nextq = PI[a][q]
        elif a < 0:
            nextq = PIinv[-a][q]
        else:
            raise ValueError('the word w contains 0, an illegal character')
        if nextq == None:
            return (None, length_read, last_vertex_visited) if trace else None
        else:
            q = nextq
            last_vertex_visited = q
            length_read += 1
    return (q, len(w), q) if trace else q


#######################################
### Equality as rooted unlabeled graphs
#######################################

def are_equal_as_rooted_unlabeled(G, H, certificate=False, verbose=False):
    r"""
    Return whether two folded ``DiGraph`` are the Stallings graphs of the same subgroup, possibly with different vertex labels.

    The two first arguments are expected to be folded ``DiGraph``. They represent the same subgroup if
    the corresponding tuples of ``PartialInjection`` coincide, up to a relabeling of the vertices which
    fixes the base vertex (vertex 0). That is: if the partial injections defining the second
    argument are obtained by conjugating the partial injections defining the first argument
    by a permutation which fixes 0.
    In ``verbose`` mode: details are given as to why the graphs do not represent the same subgroup or, if they
    do, which permutation fixing 0 maps one to the other.
    In ``certificate`` mode: if the subgroups are the same, the output is ``(True,sigma)``
    where ``sigma`` is a conjugating permutation; otherwise the output is ``(False,None)``.

    INPUT:

    - ``G`` -- ``DiGraph``

    - ``H`` -- ``DiGraph``

    - ``certificate`` -- boolean

    - ``verbose`` -- boolean

    OUTPUT: If ``certificate`` is set to ``False``:

    - a boolean, if ``certificate`` is set to ``False``; and if ``certificate`` is set to ``True``, 
      a tuple of the form ``(False,None)`` or ``(True,sigma)`` where ``sigma`` is the
      conjugating permutation

    EXAMPLES ::

        sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
        sage: from stallings_graphs.about_automata import are_equal_as_rooted_unlabeled
        sage: L1 = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
        sage: H1 = FinitelyGeneratedSubgroup(L1)
        sage: G1 = H1.stallings_graph()
        sage: L2 = [PartialInjection([1,2,None,5,4,3]), PartialInjection([0,3,5,None,None,None])]
        sage: H2 = FinitelyGeneratedSubgroup(L2)
        sage: G2 = H2.stallings_graph()
        sage: L3 = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,5,3,None,None,None])]
        sage: H3 = FinitelyGeneratedSubgroup(L3)
        sage: G3 = H3.stallings_graph()
        sage: are_equal_as_rooted_unlabeled(G1,G2)
        False

    ::

        sage: are_equal_as_rooted_unlabeled(G1,G3)
        True

    ::

        sage: (b, tau) = are_equal_as_rooted_unlabeled(G1,G3,certificate=True)
        sage: tau
        [0, 1, 2, 5, 3, 4]

    ::

        sage: H = FinitelyGeneratedSubgroup([])
        sage: G1 = H.stallings_graph()
        sage: K = FinitelyGeneratedSubgroup.from_generators([])
        sage: G2 = K.stallings_graph()
        sage: b,tau = are_equal_as_rooted_unlabeled(G1,G2,certificate=True)
        sage: (b,tau)
        (True, [0])
        
    ::
        
        sage: H1 = FinitelyGeneratedSubgroup.from_generators(['a','b'],alphabet_type='abc')
        sage: G1 = H1.stallings_graph()
        sage: H2 = FinitelyGeneratedSubgroup.from_generators(['ab','ba','aba'],alphabet_type='abc')
        sage: G2 = H2.stallings_graph()
        sage: are_equal_as_rooted_unlabeled(G1,G2)
        True

    ALGORITHM:

    One first checks whether both inputs represent subgroups in the same free group (same maximum
    value of a label) and have the same size (number of vertices). Then whether there is a
    permutation of the vertices other than the base
    vertex (vertex 0) which maps each transition (a partial injection) of the first argument to the
    corresponding partial injection of the second. Since a ``True`` output is least
    likely, the algorithm eliminates the most common and superficial reason for
    not being the same: different profiles of partial injections (ordered lists of lengths
    of sequences, resp. cycles, in the two subgroups. Then the algorithm attempts to build
    a conjugating permutation (unique if it exists).        
    This results in a long code,  experimentally much faster to run (on randomly generated
    subgroups constructed to be conjugated) than the shorter code relying on
    labeled graph isomorphism. 

    """
    if (not is_folded(G)) or (not is_folded(H)):
        raise ValueError('both arguments must be folded')
    if G.edges():
        rG = max(G.edge_labels())
    else:
        rG = 0
    if H.edges():
        rH = max(H.edge_labels())
    else:
        rH = 0
    if rG != rH:
        if verbose:
            print('the ambient free groups of the arguments are different.')        
        return (False,None) if (certificate == True) else False
    if len(G.vertices()) != len(H.vertices()):
        if verbose:
            print('the Stallings graphs of the subgroups have different sizes.')
        return (False,None) if (certificate == True) else False
    if len(G.edges()) != len(H.edges()):
        if verbose:
            print('the Stallings graphs of the subgroups have different numbers of edges.')
        return (False,None) if (certificate == True) else False
    #
    # Now self and other are FinitelyGeneratedSubgroup, with the same ambient_group_rank,
    # the same stallings_graph_size and the same number of edges.
    # A common reason for not being identical subgroups is that the partial 
    # injections cannot be translated to one another because they
    # have different orbit profiles (lists of lengths of sequences and of cycles).       
    ambient_rank = rG
    size = len(G.vertices())
    PIG = DiGraph_to_list_of_PartialInjection(G)
    PIH = DiGraph_to_list_of_PartialInjection(H)
    s_list1 = [None for _ in range(ambient_rank)]
    c_list1 = [None for _ in range(ambient_rank)]
    s_list2 = [None for _ in range(ambient_rank)]
    c_list2 = [None for _ in range(ambient_rank)]
    for i in range(ambient_rank):
        s_list1[i],c_list1[i] = PIG[i].orbit_decomposition()
        s_list2[i],c_list2[i] = PIH[i].orbit_decomposition()
    #
    c_lengths1 = [sorted([len(s) for s in c_list1[i]]) for i in range(ambient_rank)]
    s_lengths1 = [sorted([len(s) for s in s_list1[i]]) for i in range(ambient_rank)]
    c_lengths2 = [sorted([len(s) for s in c_list2[i]]) for i in range(ambient_rank)]
    s_lengths2 = [sorted([len(s) for s in s_list2[i]]) for i in range(ambient_rank)]
    #
    if (c_lengths1 != c_lengths2) or (s_lengths1 != s_lengths2):
        if verbose:
            print('the orbit profiles of the partial injections are different.')
        return (False,None) if (certificate == True) else False
    #
    # now try to build a permutation sigma, fixing 0 (the base vertex),
    # which maps (conjugates) each partial injection of self to the
    # corresponding partial injection of other
    #
    # first locate every point in the orbit decompositions of the
    # partial injections of self and other.
    type1 = [[None for _ in range(size)] for _ in range(ambient_rank)]
    type2 = [[None for _ in range(size)] for _ in range(ambient_rank)]
    orbit1 = [[None for _ in range(size)] for _ in range(ambient_rank)]
    orbit2 = [[None for _ in range(size)] for _ in range(ambient_rank)]
    location1 = [[None for _ in range(size)] for _ in range(ambient_rank)]
    location2 = [[None for _ in range(size)] for _ in range(ambient_rank)]
    for i in range(ambient_rank):
        for h in range(len(s_list1[i])):
            for k in range(len(s_list1[i][h])):
                type1[i][s_list1[i][h][k]] = 'seq'
                orbit1[i][s_list1[i][h][k]] = h
                location1[i][s_list1[i][h][k]] = k
        for h in range(len(c_list1[i])):
            for k in range(len(c_list1[i][h])):
                type1[i][c_list1[i][h][k]] = 'cyc'
                orbit1[i][c_list1[i][h][k]] = h
                location1[i][c_list1[i][h][k]] = k
    for i in range(ambient_rank):
        for h in range(len(s_list2[i])):
            for k in range(len(s_list2[i][h])):
                type2[i][s_list2[i][h][k]] = 'seq'
                orbit2[i][s_list2[i][h][k]] = h
                location2[i][s_list2[i][h][k]] = k
        for h in range(len(c_list2[i])):
            for k in range(len(c_list2[i][h])):
                type2[i][c_list2[i][h][k]] = 'cyc'
                orbit2[i][c_list2[i][h][k]] = h
                location2[i][c_list2[i][h][k]] = k
    # now attempt to construct the conjugation permutation (unique if
    # it exists): start with sigma[0] = 0, and then explore along the
    # orbits of 0 under the partial injections of self, to extend the
    # domain of sigma. Every new element of the domain of sigma is
    # added to new_domain, and elements of new_domain are popped one at
    # a time to explore their own orbits and further extend the domain.
    # Since the Stallings graphs of self and other are connected, this 
    # results in exploring all vertices and, either finding a contradiction
    # or constructing a permutation
    sigma = [0]
    sigma.extend([None for _ in range(1,size)])
    new_domain = set()
    new_domain.add(0)
    while new_domain:        
        x = new_domain.pop()
        for i in range(ambient_rank):
            if type1[i][x] == 'seq':
                if type2[i][sigma[x]] == 'cyc':
                    if verbose:
                        print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                    return (False,None) if (certificate == True) else False
                if len(s_list1[i][orbit1[i][x]]) != len(s_list2[i][orbit2[i][sigma[x]]]):
                    if verbose:
                        print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                    return (False,None) if (certificate == True) else False
                if location1[i][x] != location2[i][sigma[x]]:
                    if verbose:
                        print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                    return (False,None) if (certificate == True) else False
                # now these causes for failure are eliminated
                for y in range(len(s_list1[i][orbit1[i][x]])):
                    if sigma[s_list1[i][orbit1[i][x]][y]] != None:
                        if sigma[s_list1[i][orbit1[i][x]][y]] != s_list2[i][orbit2[i][sigma[x]]][y]:
                            if verbose:
                                print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                            return (False,None) if (certificate == True) else False
                    else:
                        sigma[s_list1[i][orbit1[i][x]][y]] = s_list2[i][orbit2[i][sigma[x]]][y]
                        new_domain.add(s_list1[i][orbit1[i][x]][y])
            #                    
            if type1[i][x] == 'cyc':
                if type2[i][sigma[x]] == 'seq':
                    if verbose:
                        print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                    return (False,None) if (certificate == True) else False
                if len(c_list1[i][orbit1[i][x]]) != len(c_list2[i][orbit2[i][sigma[x]]]):
                    if verbose:
                        print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                    return (False,None) if (certificate == True) else False
                if location1[i][x] > location2[i][sigma[x]]:
                    cycle3 = [c_list2[i][orbit2[i][sigma[x]]][z] for z in range(location2[i][sigma[x]] - location1[i][x], len(c_list1[i][orbit1[i][x]]) + location2[i][sigma[x]] - location1[i][x])]
                else:
                    cycle3 = [c_list2[i][orbit2[i][sigma[x]]][z] for z in range(location2[i][sigma[x]] - location1[i][x] - len(c_list1[i][orbit1[i][x]]), location2[i][sigma[x]] - location1[i][x])]
                for y in range(len(c_list1[i][orbit1[i][x]])):
                    if sigma[c_list1[i][orbit1[i][x]][y]] != None:
                        if sigma[c_list1[i][orbit1[i][x]][y]] != cycle3[y]:
                            if verbose:
                                print('ambient group rank, Stallings graph size and orbit profiles are the same, but there is no conjugating permutation.')
                            return (False,None) if (certificate == True) else False
                    else:
                        sigma[c_list1[i][orbit1[i][x]][y]] = cycle3[y]
                        new_domain.add(c_list1[i][orbit1[i][x]][y])
#
    if verbose:
        print('The permutation {} conjugates H1 to H2.'.format(sigma))
    return (True,sigma) if (certificate == True) else True



################################################################
### Misc graphs and automata: relabeling, normalize vertex names
################################################################

def relabeling(G, R):
    r"""
    Relabels this ``DiGraph`` using the given permutation.
    
    ``G`` is expected to a ``DiGraph`` with vertices labeled in `[0..n]`. ``R`` is expected to be
    a permutation of `[0..n]`. (No verification is made of that fact.) The output ``DiGraph`` is
    obtained from ``G`` by relabeling the vertices of ``G`` using the permutation ``R``. 
            
    INPUT:

        - ``G`` -- ``DiGraph``

        - ``R`` -- List

    OUTPUT: 

        - ``DiGraph``

    EXAMPLES::
    
        sage: from stallings_graphs.about_automata import relabeling
        sage: G = DiGraph([[0,1,2,3,4],[(0,0,1), (0,1,2), (0,4,3), (1,0,2), (1,2,1), (1,2,3), (2,3,2), (2,3,3), (4,3,1)]], format='vertices_and_edges', loops=True, multiedges=True)
        sage: R = [4,1,0,3,2]
        sage: GG = relabeling(G,R)
        sage: GG
        Looped multi-digraph on 5 vertices
                
    """
    
    new_edges = [(R[u],R[v],x) for (u,v,x) in G.edges()]
    return DiGraph([G.vertices(), new_edges], format='vertices_and_edges', loops=True, multiedges=True)

def exchange_labels(G,i,j):
    r"""
    Exchanges the given vertex names in this ``DiGraph``.
    
    ``G`` is expected to be a ``DiGraph`` with vertices `0,\dots,n-1`, and ``i``, ``j``
    are expected to be vertices of `G`. Outputs an isomorphic ``DiGraph``, where the names of the vertices
    `i` and `j` have been exchanged.
    
    INPUT:

        - ``G`` -- ``DiGraph``
        
        - ``i`` -- integer
        
        - ``j`` -- integer

    OUTPUT: 

        - ``DiGraph``

    EXAMPLES::
    
        sage: from stallings_graphs.about_automata import exchange_labels
        sage: G = DiGraph([[0,1,2,3,4],[(0,0,1), (0,1,2), (0,4,3), (1,0,2), (1,2,1), (1,2,3), (2,3,2), (2,3,3), (4,3,1)]], format='vertices_and_edges', loops=True, multiedges=True)
        sage: G = exchange_labels(G,0,3)
        sage: G
        Looped multi-digraph on 5 vertices
        
    """
    if i == j:
        return G
    u = min(i,j)
    v = max(i,j)
    R = list(range(u)) + [v] + list(range(u + 1,v)) + [u] + list(range(v + 1,len(G.vertices())))
    return relabeling(G,R)
    

def normalize_vertex_names(G):
    r"""
    Rename the vertices of this ``DiGraph`` so they are of the form `[0..n-1]`.
    
    ``G`` is expected to be a ``DiGraph`` with vertex set a set of integers (or at least
    sortable elements). The output ``DiGraph`` is isomorphic to ``G``, with vertices labeled
    `[0..n-1]`, where the new vertex names respect the original order on vertex identifiers.
            
    INPUT:

        - ``G`` -- ``DiGraph``

    OUTPUT: 

        - ``DiGraph``

    EXAMPLES::
    
        sage: from stallings_graphs.about_automata import normalize_vertex_names
        sage: G = DiGraph([[1,3,7,10,11],[(1,1,1), (1,3,2), (1,11,3), (3,1,2), (3,7,1), (3,7,3), (7,10,2), (7,10,3), (11,10,1)]], format='vertices_and_edges', loops=True, multiedges=True)
        sage: GG = normalize_vertex_names(G)
        sage: GG.vertices()
        [0, 1, 2, 3, 4]
        
    """
    V = G.vertices()
    V.sort()
    D = dict()
    for i,p in enumerate(V):
        D[p] = i
    newedgelist = [(D[p],D[q],i) for (p,q,i) in G.edges()]
    return DiGraph([range(len(V)),newedgelist], format='vertices_and_edges', loops=True, multiedges=True)




################################
### pruning, cyclically reducing
################################

def pruning(G):
    r"""
    Prune a ``DiGraph``, by iteratively removing degree 1 vertices other than the base vertex (vertex 0).
    
    ``G`` is expected to be a ``DiGraph`` with numerical edge labels, with vertex set of
    the form `[0..n]`. The output is another ``DiGraph``, obtained from `G` by iteratively
    removing the degree 1 vertices other than vertex 0 -- and relabeling the vertices other than 0
    so that the vertex set is of the form `[0..m]`.
    
    INPUT:

        - ``G`` -- ``DiGraph``

    OUTPUT: 

        - ``DiGraph``

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import bouquet, pruning
        sage: from stallings_graphs.about_folding import NT_fold
        sage: L = [[2,1,-2,2,1,-2], [2,3,1,-3,3,1,-2]]
        sage: G = bouquet(L)
        sage: GG = NT_fold(G)
        sage: GG
        Looped multi-digraph on 5 vertices
        
    ::
        
        sage: GGG = pruning(GG)
        sage: GGG
        Looped multi-digraph on 3 vertices
    
    """
    from stallings_graphs.about_bases import spanning_tree_and_paths
    T,list_of_leaves,D = spanning_tree_and_paths(G, root = 0)
    if len(G.vertices()) > 1:
        while list_of_leaves:
            v = list_of_leaves.pop()
#            if len(G.neighbors_in(v)) + len(G.neighbors_out(v)) == 1:
            if G.in_degree(v) + G.out_degree(v) == 1:
                w = T.neighbors(v)[0]
                G.delete_vertex(v)
                T.delete_vertex(v)
                if w != 0 and T.in_degree(w) + T.out_degree(w) == 1:
                    list_of_leaves.append(w)
    GG = normalize_vertex_names(G)
    return GG
        
def cyclic_reduction(G,trace=False):
    r"""
    Return the cyclic reduction of this ``DiGraph``.
    
    ``G`` is expected to be a ``DiGraph`` with numerical edge labels and vertex set of the
    form `[0..n]`.
    The cyclic reduction is obtained by iteratively deleting vertices of degree 1 (including the
    base vertex -- that is the difference with the ``prune`` method). Its vertex set is
    normalized to be of the form `[0..m]`. Note that the vertex labeled `0` in the cyclic
    reduction need not be the same as in the ``G`` (but it will be the same if the base vertex
    of `G` belongs to the cyclic reduction). If ``trace`` is set to ``True``, the output includes,
    in addition to the cyclic reduction of ``G``, the Word which labels the 
    shortest path from vertex 0 to a vertex that is preserved in the algorithm. 
    
    INPUT:
    
    - ``G``-- ``DiGraph``
    
    - ``trace``-- boolean
      
    OUTPUT: 
    
    - a ``Digraph`` if ``trace`` is set to ``False``; and a pair ``(GG, w)`` of a ``DiGraph``
      and a ``Word`` otherwise.
    
    EXAMPLES::
    
        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_automata import cyclic_reduction, pruning, normalize_vertex_names
        sage: L = ['ababA', 'aBabbabA', 'aababABAA']
        sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type='abc')
        sage: G = H.stallings_graph()
        sage: G
        Looped multi-digraph on 6 vertices
        
    ::
        
        sage: G2 = cyclic_reduction(G)
        sage: G2
        Looped multi-digraph on 5 vertices
        
    ::
        
        sage: G2,w = cyclic_reduction(G,trace=True)
        sage: w
        word: 1
        
    """
    if len(G.vertices()) > 1:
        GG = pruning(G)
        extremity = 0
        w = Word()
        while len(GG.neighbors_in(extremity)) + len(GG.neighbors_out(extremity)) == 1:
            vv = GG.neighbors(extremity)[0]
            if vv in GG.neighbors_in(extremity):
                a = GG.edge_label(vv,extremity)
                ww = group_inverse(Word(a))
            else:
                a = GG.edge_label(extremity,vv)
                ww = Word(a)
            GG.delete_vertex(extremity)
            extremity = vv
            w = w + ww
    GGG = normalize_vertex_names(GG)
    return (GGG,w) if trace else GGG


###############################
### Operations: fibered product
###############################

def fibered_product(G1,G2):
    r"""
    Compute the fibered product (a.k.a. direct product) of two edge-labeled graphs.
    
    ``G1`` and ``G2`` are assumed to be of class ``DiGraph``, with edges labeled by positive integers.
    Their fibered product is the ``DiGraph`` whose vertex set is the Cartesian product of the sets of
    vertices of ``G1`` and ``G2`` and whose edges are as follows:
    there is an `a`-labeled edge from `(u_1,u_2)` to `(v_1,v_2)` if and only if ``G1`` has an
    `a`-labeled edge from `u_1` to `v_1` and ``G2`` has an `a`-labeled edge from `u_2` to `v_2`.
    
    INPUT:

        - ``G1`` -- ``DiGraph``

        - ``G2`` -- ``DiGraph``

    OUTPUT: 

        - ``DiGraph``

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import fibered_product
        sage: V1 = range(3)
        sage: E1 = [(i,j,abs(i-j)) for i in V1 for j in V1]
        sage: G1 = DiGraph([V1,E1], format='vertices_and_edges', loops=True, multiedges=True)
        sage: V2 = range(3)
        sage: E2 = [(i,j,abs(i-j+1)) for i in V2 for j in V2]
        sage: G2 = DiGraph([V2,E2], format='vertices_and_edges', loops=True, multiedges=True)
        sage: G12 = fibered_product(G1,G2)
        sage: G12.vertices()
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        
    ::
        
        sage: len(G12.edges())
        26
    
    """
    if G1.edges():
        r1 = max(G1.edge_labels())
    else:
        r1 = 0
    if G2.edges():
        r2 = max(G2.edge_labels())
    else:
        r2 = 0
    vertices = [(u1,u2) for u1 in G1.vertices() for u2 in G2.vertices()]
    edges = []
    for (u1,v1,i) in G1.edges():
        for  (u2,v2,j) in G2.edges():
            if i == j:
                edges.append(((u1,u2),(v1,v2),i))
    return DiGraph([vertices,edges], format='vertices_and_edges', loops=True, multiedges=True)


############################
### Displaying an automaton
############################

def prepare4visualization_graph(G,alphabet_type='abc',visu_tool='tikz'):
    r"""
    Return a ``DiGraph`` ready for visualization, with good-looking edge labels.
    
    ``G`` is expected to be a ``DiGraph`` with numerical edge labels. The value of
    ``alphabet_type`` decides whether these labels will appear as `a_1,...,a_r`
    (``alphabet_type='123'``) or as `a,b,c,...,z` (``alphabet_type='abc'``)`. The argument
    ``visu_tool`` prepares the usage of the ``plot`` method for graphs (``visu_tool='plot'``) or of Sébastien Labbé's
    ``TikzPicture`` method (``visu_tool='tikz'``). 
        
    INPUT:

        - ``G`` -- ``DiGraph``

        - ``alphabet_type`` -- string, which can be either ``'abc'`` or ``'123'``

        - ``visu_tool`` -- string, which can be either ``'plot'`` or ``'tikz'``

    OUTPUT: 

        - ``DiGraph``

    EXAMPLES::
    
        sage: from stallings_graphs.about_automata import prepare4visualization_graph, bouquet, show_rooted_graph
        sage: from stallings_graphs.about_folding import NT_fold
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: GG = NT_fold(G)
        sage: GGG = prepare4visualization_graph(GG,alphabet_type='abc',visu_tool='plot')
        sage: show_rooted_graph(GGG,0)
        Graphics object consisting of 41 graphics primitives
        
    ::
    
        sage: GGG = prepare4visualization_graph(GG,alphabet_type='abc',visu_tool='tikz')
        sage: from slabbe import TikzPicture
        sage: t = TikzPicture.from_graph(GGG, merge_multiedges=False, edge_labels=True, color_by_label=False, prog='dot')
        sage: t.tex()         # not tested
        sage: t.pdf()         # not tested
        sage: t.png()         # not tested
    
    TESTS:

    Dear User, we made sure that production of images works::
    
        sage: _ = t.tex()
        sage: _ = t.pdf(view=False)
        sage: _ = t.png(view=False)
    
    """
    if alphabet_type == '123':
        if visu_tool == 'plot':
            edges = [(a,b,'$a_{}$'.format(c)) for (a,b,c) in G.edges()]
        elif visu_tool == 'tikz':
            edges = [(a,b,LatexExpr('a_{}'.format(c))) for (a,b,c) in G.edges()]
        else:
            raise ValueError('the 3rd argument must be "plot" or "tikz"')
    elif alphabet_type == 'abc':
        if visu_tool == 'plot':
            edges = [(a,b,translate_numeric_to_character(c)) for (a,b,c) in G.edges()]
        elif visu_tool == 'tikz':
            edges = [(a,b,LatexExpr(translate_numeric_to_character(c))) for (a,b,c) in G.edges()]
        else:
            raise ValueError('the 3rd argument must be "plot" or "tikz"')
    else:
        raise ValueError('the 2rd argument must be "123" or "abc"')
    return DiGraph([G.vertices(),edges], format='vertices_and_edges', loops=True, multiedges=True)

def show_rooted_graph(G,base_vertex=0):
    r"""
    Show this rooted ``DiGraph``, emphasizing its base vertex, using the ``graph.plot`` method.
    
    ``G`` is expected to be a ``DiGraph`` with at least one vertex, with a distinguished
    ``base_vertex``. The ``graph.plot`` function is used to show ``G``.
    The declared ``base_vertex`` is colored green, the other vertices are colored white.
        
    INPUT:

        - ``G`` -- ``DiGraph``

        - ``base_vertex`` -- an object which is a vertex of ``G``

    OUTPUT: 

        - A ``graphics`` object

    EXAMPLES ::
    
        sage: from stallings_graphs.about_automata import prepare4visualization_graph, bouquet, show_rooted_graph
        sage: from stallings_graphs.about_folding import NT_fold
        sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
        sage: G = bouquet(L)
        sage: GG = NT_fold(G)
        sage: show_rooted_graph(GG, base_vertex=0)
        Graphics object consisting of 41 graphics primitives

    """
    V = G.vertices()
    V.remove(base_vertex)
    return G.plot(vertex_colors = {"green" : [base_vertex], "white" : V}, edge_labels=True, spring = True)




