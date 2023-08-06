# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions.
These are the functions which deal with free factors: determining whether a subgroup is a
free factor of the ambient group of another subgroup, deciding primitivity of a word, computing the
lattice of algebraic extensions of a subgroup.

We have the following functions:

- ``SilvaWeil_free_factor_of_ambient``: to decide whether a given subgroup is a free factor of
  the ambient group and, possibly give a basis of its complement

- ``SilvaWeil_free_factor_of``: to decide whether a given subgroup is a free factor of another and,
  possibly, give a basis of its complement

The algorithm implemented in ``SilvaWeil_free_factor_of_ambient`` and ``SilvaWeil_free_factor_of``
is from [SW2008]_. The worst-case complexity
is polynomial in the size of the subgroups considered but exponential in the rank difference
between them.

- ``set_of_possible_additional_generators``: an ancillary function to find the additional generators
  that will lead to the overgroups of a subgroup obtained by identifying two vertices of the
  Stallings graph

- ``compute_algebraic_extensions``: computes the semilattice of algebraic extensions of a subgroup
  noting those that are elementary algebraic and some of their inclusion relation (sufficiently many
  to include a Hasse diagram)

The algorithm implemented in ``compute_algebraic_extensions``  is from [MVW2007]_. It requires
verifying whether certain subgroups are free factors of others. This is done using the Silva Weil algorithm.

EXAMPLES::

    sage: from stallings_graphs import FinitelyGeneratedSubgroup
    sage: from stallings_graphs.about_free_factors import SilvaWeil_free_factor_of_ambient, SilvaWeil_free_factor_of
    sage: L1 = ['ac','bacd','ed']
    sage: H1 = FinitelyGeneratedSubgroup.from_generators(L1, alphabet_type='abc')
    sage: SilvaWeil_free_factor_of_ambient(H1, maxletter = 0, complement = True)
    (True, [word: 2,1,-5, word: -2])
    
::
    
    sage: LH = [[-3,1,-2,-1,-1,-3,2,2,3], [-3,-1,-1,3,1,1,-3,-1,3,1,3,3], [-3,1,3,-1,-1,-3,1,1,1,3,-1,-1], [1,1,-3,1,3,1,1,-3,-1,3]]
    sage: LK = [[1,1,2,-1,3], [1,1,3,-1], [-3,1,3,-1,-1], [-3,1,1,3], [-3,2,3], [1,3,3]]
    sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
    sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
    sage: SilvaWeil_free_factor_of(H, K, complement = True)
    (False, 'the 1st argument is not a free factor of the second')

::

    sage: LH = [[3,1,-2,-1,-1,-3,2,2,3], [-3,-1,-1,3,1,1,-3,-1,3,1,3,3], [-3,1,3,-1,-1,-3,1,1,1,3,-1,-1], [1,1,-3,1,3,1,1,-3,-1,3]]
    sage: LK = [[1,1,2,-1,3], [1,1,3,-1], [-3,1,3,-1,-1], [-3,1,1,3], [-3,2,3], [1,3,3]]
    sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
    sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
    sage: SilvaWeil_free_factor_of(H, K, complement = True)
    (False, '1st argument not contained in 2nd')

::

    sage: H = FinitelyGeneratedSubgroup.from_generators(['bba','bAbaB'], alphabet_type='abc')
    sage: K = FinitelyGeneratedSubgroup.from_generators(['a', 'bb', 'bAbaB'], alphabet_type='abc')
    sage: SilvaWeil_free_factor_of(H, K, complement = True)
    (True, [word: -2,-2])
    
::
    
    sage: from stallings_graphs.about_free_factors import compute_algebraic_extensions
    sage: testgens = ['aba','bab']
    sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
    sage: compute_algebraic_extensions(testH)
    {0: [set(),
      {1},
      [],
      {word: -1, word: -1,2, word: 1,-2, word: 11, word: 22},
      True,
      False],
     1: [{0}, set(), [word: -1], set(), True, False]}


AUTHOR:

- Pascal WEIL (2020-05-11): initial version
  CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr>

"""

from sage.combinat.words.word import Word
from stallings_graphs import FinitelyGeneratedSubgroup
from stallings_graphs.about_words import rank, positive_alphabetic_content, group_inverse
from stallings_graphs.about_bases import spanning_tree_and_paths, basis_interpreter
from stallings_graphs.about_TC_morphisms import FGendomorphism, image_of_Word_by_endomorphism
                

def SilvaWeil_free_factor_of_ambient(H, maxletter = 0, complement = True):
    r"""
    If ``complement`` is set to ``False``, returns whether `H`is a free factor of the ambient
    free group (a boolean). If ``complement`` is set to ``True``, returns a pair of a boolean
    as above, and a string explaining why `H` is not a free factor, or a basis for a complement
    of `H` if `H` is a free factor (in numerical form). In that case, the ambient free group
    is understood to be of rank the maximal letter occurring in `H` if ``maxletter`` is set
    to 0, of rank ``maxletter`` otherwise.
    
    ``H`` is expected to be a ``FinitelyGeneratedSubgroup``; ``maxletter`` is expected to be a
    non-negative integer, equal to 0 or greater than or equal to the maximal letter occurring in
    ``H``; ``complement`` is expected to be a Boolean.
    
    INPUT:

    - ``H`` -- ``FinitelyGeneratedSubgroup``
    - ``maxletter`` -- integer
    - ``complement`` -- boolean

    OUTPUT: 

    - a boolean if ``complement`` is set to ``False``, and a pair consisting of a boolean and
      either a string or a list of ``Words`` in numerical form otherwise
    
    ALGORITHM:
    
        The algorithm implemented is from [P. Silva, P. Weil. On an algorithm to decide whether
        a free group is a free factor of another, Theoretical Informatics and Applications 42
        (2008) 395-414]. Be aware that the worst-case complexity is polynomial in the size of `H`
        but exponential in the rank difference between `H` and the ambient group.

    EXAMPLES::
    
        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_free_factors import SilvaWeil_free_factor_of_ambient
        sage: L1 = ['ac','bacd','ed']
        sage: H1 = FinitelyGeneratedSubgroup.from_generators(L1, alphabet_type='abc')
        sage: SilvaWeil_free_factor_of_ambient(H1, maxletter = 0, complement = True)
        (True, [word: 2,1,-5, word: -2])
        
    ::
        
        sage: SilvaWeil_free_factor_of_ambient(H1, maxletter = 0, complement = False)
        True
        
    ::
        
        sage: L2 = ['acac','bacd','ed']
        sage: H2 = FinitelyGeneratedSubgroup.from_generators(L2, alphabet_type='abc')
        sage: SilvaWeil_free_factor_of_ambient(H2, maxletter = 0, complement = True)
        (False, 'the 1st argument is not a free factor of the second')
        
    ::
        
        sage: SilvaWeil_free_factor_of_ambient(H2, maxletter = 0, complement = False)
        False
        
    ::
        
        sage: H = FinitelyGeneratedSubgroup.from_generators(['A','d'], alphabet_type='abc')
        sage: SilvaWeil_free_factor_of_ambient(H, complement = True)
        (True, [word: 2, word: 3])
        
    ::
        
        sage: SilvaWeil_free_factor_of_ambient(H, complement = False)
        True
                
    """
    original_graph = H.stallings_graph()
    original_basis = H.basis(alphabet_type = '123')
    if maxletter > 0:
        deficit = set(range(1,maxletter + 1))
    else:
        maxrank = max([rank(x) for x in original_basis])
        deficit = set(range(1,maxrank + 1))
    for x in original_basis:
        deficit = deficit.difference(positive_alphabetic_content(x))
    #
    if H.stallings_graph_size() == 1:
        if complement == True:
            return (True,[Word([x]) for x in deficit])
        else:
            return True
    # now H has size at least 2        
    if H.rank() >= H.ambient_group_rank():
        if complement == True:
            return (False,'the 1st argument has too large a rank')
        else:
            return False
    # now H has size at least 2 and rank of H < rank of the ambient group
    current_list = [(original_graph,[])]
    while current_list:
        (G,B) = current_list[-1]
        temporary_list = []
        still_good = True
        T,L,D = spanning_tree_and_paths(G)
        for p in G.vertices():
            for q in G.vertices():
                if still_good and q > p:
                    w = D[p]+group_inverse(D[q])
                    newgens = original_basis + B + [w]
                    newH = FinitelyGeneratedSubgroup.from_generators(newgens,alphabet_type = '123')
                    if newH.rank() == len(G.edges()) - len(G.vertices()) + 2:
                        if newH.stallings_graph_size() == 1:
                            if complement:
                                return (True,B+[w]+[Word([x]) for x in deficit])
                            else:
                                return True
                        # now newH has size at least 2
                        newG = newH.stallings_graph()
                        temporary_list.append((newG,w))
                    else:
                        still_good = False
        current_list = current_list[:-1]
        if still_good:
            current_list = current_list + [(newG,B + [w]) for (newG,w) in temporary_list]
    if complement:
        return (False,'the 1st argument is not a free factor of the second')
    else:
        return False

def SilvaWeil_free_factor_of(H, K, complement = True):
    r"""
    If ``complement`` is set to ``False``, returns whether `H`is a free factor of ``K``
    (a boolean). If ``complement`` is set to ``True``, returns a pair of a boolean
    as above, and a string explaining why `H` is not a free factor, or a basis for a complement
    of `H` in `K` (in numerical form) if `H` is a free factor.
    
    ``H`` and ``K`` are expected to be of type ``FinitelyGeneratedSubgroup``; ``complement``
    is expected to be a Boolean.
    
    INPUT:

    - ``H`` -- ``FinitelyGeneratedSubgroup``
    - ``K`` -- ``FinitelyGeneratedSubgroup``
    - ``complement`` -- boolean

    OUTPUT: 

    - a boolean if ``complement`` is set to ``False``, and a pair consisting of a boolean and
      either a string or a list of ``Words`` in numerical form otherwise
    
    ALGORITHM:
    
        The algorithm implemented is from [P. Silva, P. Weil. On an algorithm to decide whether
        a free group is a free factor of another, Theoretical Informatics and Applications 42
        (2008) 395-414]. Be aware that the worst-case complexity is polynomial in the size of `H`
        and `K` but exponential in the rank difference between `H` and `K`.

    EXAMPLES::
    
        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_free_factors import SilvaWeil_free_factor_of
        sage: LH = [[2,-3,1,3,2,3,-2,-1,2,-3,-1], [3,1,1,1,-3,-1], [1,3,-2,-1,2,-1,2], [3,2,3,-1,2,-1]]
        sage: LK = [[2,-3], [1,1], [1,3,-2,1,2,-3,-1], [3,2], [3,1,-3,-1], [1,3,2,-1], [1,3,3,-1], [1,3,1,-3]]
        sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
        sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
        sage: SilvaWeil_free_factor_of(H, K, complement = True)
        (True, [word: 3,2,3,1,2,-1, word: 32, word: 3,1,3,-1, word: 11])
        
    ::
        
        sage: SilvaWeil_free_factor_of(H, K, complement = False)
        True
        
    ::
        
        sage: LH = [[-3,1,-2,-1,-1,-3,2,2,3], [-3,-1,-1,3,1,1,-3,-1,3,1,3,3], [-3,1,3,-1,-1,-3,1,1,1,3,-1,-1], [1,1,-3,1,3,1,1,-3,-1,3]]
        sage: LK = [[1,1,2,-1,3], [1,1,3,-1], [-3,1,3,-1,-1], [-3,1,1,3], [-3,2,3], [1,3,3]]
        sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
        sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
        sage: SilvaWeil_free_factor_of(H, K, complement = True)
        (False, 'the 1st argument is not a free factor of the second')
        
    ::
        
        sage: SilvaWeil_free_factor_of(H, K, complement = False)
        False
        
    ::
        
        sage: LH = [[3,1,-2,-1,-1,-3,2,2,3], [-3,-1,-1,3,1,1,-3,-1,3,1,3,3], [-3,1,3,-1,-1,-3,1,1,1,3,-1,-1], [1,1,-3,1,3,1,1,-3,-1,3]]
        sage: LK = [[1,1,2,-1,3], [1,1,3,-1], [-3,1,3,-1,-1], [-3,1,1,3], [-3,2,3], [1,3,3]]
        sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
        sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
        sage: SilvaWeil_free_factor_of(H, K, complement = True)
        (False, '1st argument not contained in 2nd')
        
    ::
        
        sage: SilvaWeil_free_factor_of(H, K, complement = False)
        False
        
    ::
        
        sage: H = FinitelyGeneratedSubgroup.from_generators(['bba','bAbaB'], alphabet_type='abc')
        sage: K = FinitelyGeneratedSubgroup.from_generators(['a', 'bb', 'bAbaB'], alphabet_type='abc')
        sage: SilvaWeil_free_factor_of(H, K, complement = True)
        (True, [word: -2,-2])
        
    ::
        
        sage: SilvaWeil_free_factor_of(H, K, complement = False)
        True
        
    ::
        
        sage: H = FinitelyGeneratedSubgroup.from_generators(['a','B'], alphabet_type='abc')
        sage: K = FinitelyGeneratedSubgroup.from_generators(['a','b','d'], alphabet_type='abc')
        sage: SilvaWeil_free_factor_of(H, K, complement = True)
        (True, [word: 4])
        
    ::
        
        sage: SilvaWeil_free_factor_of(H, K, complement = False)
        True

        
    """
    basisK = K.basis(alphabet_type = '123')
    rK = len(basisK)
    basisH = H.basis(alphabet_type = '123')
    if all(K.contains_element(x) for x in basisH):
        translatedbasisH = basis_interpreter(basisH, basisK, alphabet_type = '123')
        translatedH = FinitelyGeneratedSubgroup.from_generators(translatedbasisH,alphabet_type = '123')
        if complement:
            (valeur,base) = SilvaWeil_free_factor_of_ambient(translatedH, maxletter = rK, complement = complement)
            if valeur:
                phi = FGendomorphism(basisK, alphabet_type = '123')
                translatedbase = [image_of_Word_by_endomorphism(phi, w, alphabet_type='123') for w in base]
                return (valeur,translatedbase)
            else:
                return (valeur,base)
        else:
            return SilvaWeil_free_factor_of_ambient(translatedH, maxletter = rK, complement = complement)
    else:
        if complement:
            return(False,'1st argument not contained in 2nd')
        else:
            return False      

        
def set_of_possible_additional_generators(G):
    r"""
    ``G`` is expected to be the Stallings graph of a finitely generated subgroup of
    a free group. The function returns a set of Words of the form `u_pu_q^{-1}`, where
    `u_p`(resp. `u_q`) is a path from the root vertex 0 to vertex `p`(resp. `q`).
    
    INPUT:

    - ``G`` -- ``DiGraph``

    OUTPUT: 

    - a set of objects of type ``Word``
    
    EXAMPLE::
    
        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_free_factors import set_of_possible_additional_generators
        sage: testgens = ['aba','bab']
        sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
        sage: testG = testH.stallings_graph()
        sage: set_of_possible_additional_generators(testG)
        {word: -1, word: -1,2, word: 1,-2, word: 11, word: 22}

    """
    # should return the empty set if G has a single vertex
    S = set()
    from stallings_graphs.about_automata import fibered_product
    T,L,D = spanning_tree_and_paths(G)
    GG = fibered_product(G,G)
    CC = GG.connected_components()
    baseCC = GG.connected_component_containing_vertex((0,0))
    CC.remove(baseCC)
    for C in CC:
        (p,q) = C[0]
        additional_generator = D[p]+group_inverse(D[q])
        if group_inverse(additional_generator) not in S:
            S.add(D[p]+group_inverse(D[q]))
    return S

    

def compute_algebraic_extensions(H):
    r"""
    Returns detailed information on the semilattice of algebraic extensions of the subgroup
    ``H``: a dictionary whose keys are integers (without any particular meaning, except key
    0 corresponds to ``H`` itself) and whose entries are a list of information on algebraic extensions:
    sets of parents and children (not a Hasse diagram of the containment relation, but including
    such a diagram), list of generators to be added to those of ``H`` to generate that particular
    extension, a set of words which help compute the immediate overgroups of this extension,
    and two boolean flags expressing, respectively, that the extension is e-algebraic and that it is
    *not* algebraic.
    
    ``H`` is expected to be a ``FinitelyGeneratedSubgroup``
    
    INPUT:

    - ``H`` -- ``FinitelyGeneratedSubgroup``

    OUTPUT: 

    - a dictionary whose keys are integers and whose entries are lists of two sets of keys, a list
      of ``Words``, a set of ``Words`` and two booleans
    
    EXAMPLES::

        sage: from stallings_graphs import FinitelyGeneratedSubgroup
        sage: from stallings_graphs.about_free_factors import compute_algebraic_extensions
        sage: testgens = ['aba','bab']
        sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
        sage: compute_algebraic_extensions(testH)
        {0: [set(),
          {1},
          [],
          {word: -1, word: -1,2, word: 1,-2, word: 11, word: 22},
          True,
          False],
         1: [{0}, set(), [word: -1], set(), True, False]}
    
    ::
    
        sage: testgens = ['ab','cd']
        sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
        sage: compute_algebraic_extensions(testH)
        {0: [set(), set(), [], {word: -3, word: -1, word: 1,-3}, True, False]}
    
    ::
    
        sage: testgens = ['ABBaaBABa','Baba','Abababba','AbabbABa','ABabAba']
        sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
        sage: compute_algebraic_extensions(testH)
        {0: [set(),
          {3, 6, 11},
          [],
          {word: -2,-1,-2,1,
           word: -1,-2,-2,1,-2,-1,-2,1,
           word: -1,-2,-2,1,-2,1,
           word: -1,-2,-2,1,-1,-2,1,
           word: -1,-2,-2,1,1,
           word: -1,-2,1,
           word: -1,2,2,1,
           word: 1,
           word: 2,
           word: 21,
           word: 221},
          True,
          False],
         3: [{0, 6, 11}, set(), [word: -1,-2,1], set(), True, False],
         6: [{0, 11}, {3}, [word: 21], {word: -1}, True, False],
         11: [{0},
          {3, 6},
          [word: -1,-2,-2,1,-2,1],
          {word: -1,-2,1, word: -1,2, word: 2},
          True,
          False]}

    """
    original_graph = H.stallings_graph()
    original_basis = H.basis(alphabet_type = '123')
    original_possible_additional_generators = set_of_possible_additional_generators(original_graph)
    #
    # semilattice_AE is a dictionary.
    # Keys are integers, managed by keycounter
    # semilattice_AE entries are of the form
    # [(0)set of parent keys, (1)set of children keys, (2)list of generators beyond original_basis,
    # (3)set of possible additional generators, (4)flag_ealgebraic, (5)flag_guaranteed_non_algebraic)
    #
    # Note that the set of possible additional generators is empty iff the entry has size 1
    #
    # flag_ealgebraic is True if I have found a witness: a sequence of elementary algebraic
    # extensions
    #
    # flag_guaranteed_non_algebraic is True if I have found a free factor 
    #
    # The construction is in phases. Note that semilattice_AE is first constructed as a
    # tree (Phases I and II) where subgroups can have several occurrences, in different branches.
    # In Phase I, the tree of overgroups is constructed with some information about
    # e-algebraicity and non-algebraicity. At the end of this phase, every e-algebraic overgroup
    # is tagged as such in at least one of its occurrences.
    # In Phase II, free factors are systematically located within the tree structure. At the end
    # of this phase, every non-algebraic overgroup is tagged as such in at least one of its
    # occurrences.
    # In Phase III, overgroups along different branches are compared, and merged if they
    # are equal: the tree becomes a dag. One takes the disjunction of the ealgebraic and
    # guaranteed_non_algebraic tags of merged vertices (+ bookkeeping about their parents and
    # children. At the end of this phase, every overgroup has a single occurrence, and
    # flag_ealgebraic and flag_guaranteed_non_algebraic mean 'ealgebraic' and
    #'not algebraic'.
    # In Phase IV, non algebraic overgroups are eliminated.
    #
    semilattice_AE = {}
    #
    # Phase I: construct semilattice_AE, as a tree.
    #
    # keys_to_visit keeps track of the entries created but whose own overgroups (children)
    # have not yet been computed
    #
    keys_to_visit = [0]
    semilattice_AE[0] = [set(),set(),[],original_possible_additional_generators,True,False]
    keycounter = 1
    #
    while keys_to_visit:
        current_key = keys_to_visit.pop()
        current_entry = semilattice_AE[current_key]
        current_generators = original_basis + current_entry[2]
        current_subgroup = FinitelyGeneratedSubgroup.from_generators(current_generators,alphabet_type='123')
        #
        # if currently_entry has size greater than 1 (non-empty list of possible
        # additional generators), append new quotients to the dictionary, increment keys_to_visit
        if len(current_entry[3]) != 0:
            newparent = set()
            newparent.add(current_key)
            for u in current_entry[3]:
                newgenerators = original_basis + current_entry[2] + [u]
                newH = FinitelyGeneratedSubgroup.from_generators(newgenerators,alphabet_type='123')
                newG = newH.stallings_graph()
                if newH.rank() <= current_subgroup.rank():
                    if current_entry[4]:
                        flag_ealgebraic = True
                        flag_guaranteed_non_algebraic = False
                    else:
                        flag_ealgebraic = False
                        flag_guaranteed_non_algebraic = False
                else:
                    flag_ealgebraic = False
                    flag_guaranteed_non_algebraic = True
                #
                semilattice_AE[keycounter] = [newparent, set(), current_entry[2] + [u], set_of_possible_additional_generators(newG),flag_ealgebraic,flag_guaranteed_non_algebraic]
                # add this new entry to children of its antecedent, and to keys_to_visit
                # (even if it is known to not be algebraic: we still need to take its quotients
                # and the same subgroup may occur elsewhere, without a witness of it being
                # non algebraic).
                current_entry[1].add(keycounter)
                keys_to_visit.append(keycounter)
                keycounter +=1
        #
    # Phase I over
    #
    # Phase II. Process the entries of the **tree** semilattice_AE, starting
    # with the largest keyvalues, seeking an ancestral free factor. If one is found, 
    # say K free factor of current_subgroup, flag_guaranteed_non_algebraic is set to True
    # for all the keys between K (excluded) and the currently processed key.
    # One may skip the overgroups tagged ealgebraic (no free factor will be found) or
    # flag_guaranteed_non_algebraic (the existence of a free factor was already established). 
    #
    keys_to_be_processed = list(semilattice_AE.keys())
    keys_to_be_processed.sort()
    while keys_to_be_processed:
        processed_key = keys_to_be_processed.pop()
        processed_entry = semilattice_AE[processed_key]
        if not(processed_entry[4] or processed_entry[5]):
            # processed_entry is neither known to be e-algebraic nor to be non-algebraic
            processed_generators = original_basis + processed_entry[2]
            processed_subgroup = FinitelyGeneratedSubgroup.from_generators(processed_generators,alphabet_type='123')
            intermediate_keys = [processed_key]
            no_free_factor = True
            # check current_predecessor: if it is guaranteed_non_algebraic, go to next;
            # if it is not guaranteed_non_algebraic, check whether it is a free factor
            # of processed_key;
            # if it is not, add to intermediate_keys and go to next predecessor;
            # if it is, stop and change all intermediate_keys to guaranteed_non_algebraic,
            # we're finished with this processed_key.
            # When I run out of predecessors, I am finished with this processed_key.
            current_predecessor_key = processed_key
            current_predecessor_entry = semilattice_AE[current_predecessor_key]
            while no_free_factor and current_predecessor_key != 0:
                copyset = current_predecessor_entry[0].copy()
                current_predecessor_key = copyset.pop()
                current_predecessor_entry = semilattice_AE[current_predecessor_key]
                if current_predecessor_entry[5]:
                    continue
                # now I know that current_predecessor_entry[5] is False
                current_predecessor_generators = original_basis + current_predecessor_entry[2]
                current_predecessor_subgroup = FinitelyGeneratedSubgroup.from_generators(current_predecessor_generators,alphabet_type='123')
                if current_predecessor_subgroup.SW_is_free_factor_of(processed_subgroup, complement = False, alphabet_type = '123'):
                    no_free_factor = False
                else:
                    intermediate_keys.append(current_predecessor_key)
            # At the end of this while loop, either I found a free factor, and I tag
            # intermediate vertices, or I reached the root. In either case, I am done with
            # processed_key.
            if not no_free_factor:
                for x in intermediate_keys:
                    semilattice_AE[x][5] = True
        # no 'else': if processed_entry[4] or processed_entry[5], we do nothing
    # Phase II over
    #
    # Phase III. Explore the tree to spot equal subgroups, starting with the largest key and
    # comparing it with keys that are not in its ancestry (well, if they are, it will be quickly
    # handled by _eq_ because the Stallings graphs will have different sizes). When I find equal
    # subgroups, I merge their entries: bookkeeping of parents and children + following remark:
    # 
    # if an occurrence of a subgroup is marked ealgebraic, the subgroup is indeed ealgebraic
    # if an occurrence of a subgroup is marked flag_guaranteed_non_algebraic, then the subgroup
    # is not algebraic
    # 
    # Don't eliminate any entry because information is needed about every occurrence of
    # every overgroup
    #
    pairs_to_be_compared = [(p,q) for p in semilattice_AE.keys() for q in semilattice_AE.keys() if q < p and not(q in semilattice_AE[p][0] or p in semilattice_AE[q][0])]
    while pairs_to_be_compared:
        (key1,key2) = pairs_to_be_compared.pop()
        entry1 = semilattice_AE[key1]
        entry2 = semilattice_AE[key2]
        generators1 = original_basis + entry1[2]
        generators2 = original_basis + entry2[2]
        subgroup1 = FinitelyGeneratedSubgroup.from_generators(generators1,alphabet_type='123')
        subgroup2 = FinitelyGeneratedSubgroup.from_generators(generators2,alphabet_type='123')
        if subgroup1 == subgroup2:
            # je veux supprimer subgroup1:
            # les parents de 1 perdent 1 et gagnent 2 parmi leurs enfants,
            # les enfants de 1 perdent 1 et gagnent 2 parmi leurs parents,
            # l'ensemble des parents de 2 accueille les parents de 1,
            # l'ensemble des enfants de 2 accueille les enfants de 1,
            # key1 est retiré de semilattice_AE
            # toutes les paires à comparer contenant key1 sont supprimées
            for x in entry1[0]:
                semilattice_AE[x][1].discard(key1)
                semilattice_AE[x][1].add(key2)
            for y in entry1[1]:
                semilattice_AE[y][0].discard(key1)
                semilattice_AE[y][0].add(key2)
            entry2[0] = entry2[0].union(entry1[0])
            entry2[1] = entry2[1].union(entry1[1])
            entry2[4] = entry1[4] or entry2[4]
            entry2[5] = entry1[5] or entry2[5]
            for p in semilattice_AE.keys():
                if p > key1 and (p,key1) in pairs_to_be_compared:
                    pairs_to_be_compared.remove((p,key1))
                elif p < key1 and (key1,p) in pairs_to_be_compared:
                    pairs_to_be_compared.remove((key1,p))
            semilattice_AE.pop(key1)
    # Now all pairs of entries have been compared, they are all distinct and those not
    # flagged guaranteed_not_algebraic are actually algebraic.
    #
    # Phase III over
    #
    # Phase IV. Remove the non algebraic entries
    #
    remaining_keys = list(semilattice_AE.keys())
    while remaining_keys:
        key = remaining_keys.pop()
        entry = semilattice_AE[key]
        if entry[5]:
            # non algebraic overgroup; attach its children to its parents,
            # update its parents' list of children
            # eliminate entry
            for parent in entry[0]:
                semilattice_AE[parent][1].discard(key)
            for child in entry[1]:
                semilattice_AE[child][0].discard(key)
            for parent in entry[0]:
                for child in entry[1]:
                    semilattice_AE[child][0].add(parent)
                    semilattice_AE[parent][1].add(child)                
            semilattice_AE.pop(key)
    #
    # End of Phase IV
    #
    return semilattice_AE

