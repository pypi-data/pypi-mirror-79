# -*- coding: utf-8 -*-
r"""
The class ``FinitelyGeneratedSubgroup`` is meant to represent finitely generated subgroups of free groups

The representation of a ``FinitelyGeneratedSubgroup`` is a tuple of partial injections on a set of the form `[0..(n-1)]` (one for each generator of the ambient free group), which represent the Stallings graph of the subgroup, with base vertex 0.

Methods implemented in this file:

- definition of a ``FinitelyGeneratedSubgroup`` from a list of generators (``Words``)

- definition of a ``FinitelyGeneratedSubgroup`` from a ``DiGraph`` (by folding and pruning)

- random instance

- ``ambient_group_rank``, to compute the rank of the ambient free group

- ``stallings_graph_size``

- ``rank``, to compute the rank of the subgroup

- ``stallings_graph``, to compute the Stallings graph of the subgroup

- ``show_Stallings_graph``, to visualize the Stallings graph

- ``is_valid``, to check the necessary properties of connectedness and trimness

- ``eq``, to check whether two objects represent the same finitely generated subgroup

- ``basis``

- ``contains_element``, to check whether the subgroup contains a given word

- ``contains_subgroup``, to check whether the subgroup contains a given subgroup

- ``intersection``

- ``has_index``, to compute the index of the subgroup

- ``conjugated_by``, to compute the conjugate of a subgroup by a given word

- ``is_conjugated_to``, to check whether two subgroups are conjugated and, optionally, compute a conjugating word

- ``is_malnormal``, to check whether the subgroup is malnormal and, optionally, compute a witness of its non-malnormality

- ``is_free_factor_of_ambient``, to check whether the subgroup is a free factor of the ambient group and, optionally, to compute a complement

- ``is_free_factor_of_``, to check whether the subgroup is a free factor of another and, optionally, to compute a complement



EXAMPLES::

    sage: from stallings_graphs import FinitelyGeneratedSubgroup
    sage: gens = ['ab','ba']
    sage: G = FinitelyGeneratedSubgroup.from_generators(gens, alphabet_type='abc')
    sage: G
    A subgroup of the free group of rank 2, whose Stallings graph has 3 vertices
    
::

    sage: gens = [[1,2,5,-1,-2,2,1],[-1,-2,2,3],[1,2,3]]
    sage: G = FinitelyGeneratedSubgroup.from_generators(gens)
    sage: G
    A subgroup of the free group of rank 5, whose Stallings graph has 3 vertices
    
::

    sage: from stallings_graphs import FinitelyGeneratedSubgroup
    sage: from stallings_graphs.about_words import random_reduced_word
    sage: from stallings_graphs.about_automata import bouquet
    sage: L = [random_reduced_word(100,2) for _ in range(10)]
    sage: G = bouquet(L)
    sage: H = FinitelyGeneratedSubgroup.from_digraph(G)
    sage: H    # random
    A subgroup of the free group of rank 2, whose Stallings graph has 965 vertices
    
::
    
    sage: H = FinitelyGeneratedSubgroup.random_instance(15)
    sage: H
    A subgroup of the free group of rank 2, whose Stallings graph has 15 vertices
    
AUTHORS:

- Pascal WEIL (2018-04-26): initial version

CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr>


"""

from sage.structure.sage_object import SageObject
from sage.rings.integer_ring import ZZ
from sage.graphs.digraph import DiGraph
from sage.misc.cachefunc import cached_function
from sage.misc.latex import LatexExpr

from stallings_graphs.partial_injections import PartialInjection
from stallings_graphs.about_words import *
from stallings_graphs.about_automata import *
from stallings_graphs.about_bases import *
from stallings_graphs.about_folding import *
# remplacer * par le nom des fonctions utilisées


class FinitelyGeneratedSubgroup(SageObject):
    r"""
    Define the class ``FinitelyGeneratedSubgroup``, which represents subgroups of free groups.
    
    The representation of a finitely generated subgroup is by means of the partial
    injections (on a set of the form `[0..n-1]`, one per generator of the ambient free group)
    which describes its Stallings graph, with base vertex 0. The Stallings graph of a subgroup is
    a uniquely defined finite directed graph,
    whose edges are labeled by positive letters, rooted in a designated
    vertex, subject to three conditions: it must be connected, folded (no two edges
    with the same label share the same initial (resp. terminal) vertex),
    and every vertex must have valency 2 (in the underlying non-directed graph),
    except possibly for the root (also known as base vertex). That is: a subgroup is represented by
    a tuple of partial injections on `[0..n-1]`, up to a relabeling of the elements of `[0..n-1]`
    fixing the base vertex (namely 0).

    A ``FinitelyGeneratedSubgroup`` can be created from:
    
    - a list of objects of the class ``PartialInjection``, all of the same size;
    
    or

    - a list of ``Words`` on a symmetrical alphabet: either `a`:`z` / `A`:`Z` (upper case is the inverse of lower case), so-called ``alphabet_type='abc'`` ; or `[-r..-1,1..r]`, so-called ``alphabet_type='123'``.
    
    or
    
    - a labeled ``DiGraph`` with vertex set `[0..(n-1)]` and edge labels in a positive alphabet (`a`:`z` if ``alphabet_type='abc'`` or `[1..r]` if ``alphabet_type='123'``). The ``DiGraph`` is considered to be rooted at vertex 0.
    
    or
    
    - a random instance.
    
    """

    def __init__(self, partial_injections):
        r"""
        Create a ``FinitelyGeneratedSubgroup`` by specifying the list of objects of the
        class ``PartialInjection``, which determines its Stallings graph.
        
        The ``PartialInjection``objects are expected to have the same size, and their graph of
        transitions must be connected, with every vertex except possibly 0 of valency at least 2.
        NB - The first property is verified in ``__init__``, the other properties are not verified.
        
        INPUT:

        - ``partial_injections`` -- list of objects from the class ``PartialInjection``.

        OUTPUT:

        - an object of class ``FinitelyGeneratedSubgroup``.

        EXAMPLES::
            
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [[0,3,None,4,None,2],[None,2,3,None,1,0]]
            sage: L = [PartialInjection(x) for x in L]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 6 vertices
            
            ::
            
            sage: H = FinitelyGeneratedSubgroup([])
            sage: H
            A subgroup of the free group of rank 0, whose Stallings graph has 1 vertices
            
            ::
            
            sage: H = FinitelyGeneratedSubgroup([PartialInjection([None]),PartialInjection([None])])
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 1 vertices
            
        .. WARNING::

            An exception will be raised if the input is not a list or if the ``PartialInjection`` objects
            in that list do not have the same size. There will be trouble if the input is a list
            of other objects than ``PartialInjection``.
            A list of `r` PartialInjections of the form `[``None``]` yields the trivial subgroup
            in the rank `r` free group (including if `r = 0`).
            If the graph defined by the input list of ``PartialInjection`` is not connected or if a
            vertex other than the base vertex 0 has valency 1, the definition will go through
            but the object will not represent a subgroup of a free group.
            
        """

        if not isinstance(partial_injections, list):
            raise TypeError('partial_injections(={}) must be of type list'.format(partial_injections))
        if (partial_injections and any(partial_injections[0].size() != p.size() for p in partial_injections)):
            raise ValueError('all partial injections must have the same length')
#            
        self._partial_injections = partial_injections
    
    def __repr__(self):
        r"""
        Describe a ``FinitelyGeneratedSubgroup``.
        
        The description consists in giving the rank of the ambient free group, that is,
        the length of the list of ``PartialInjection`` objects which define the ``FinitelyGeneratedSubgroup``;
        and the size of the Stallings graph, that is, the length of the partial injections.
        
        INPUT:

        - ``self`` -- an object of the class ``FinitelyGeneratedSubgroup``.

        OUTPUT:

        - a sentence describing the corresponding subgroup of a free group.

        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [[0,3,None,4,None,2],[None,2,3,None,1,0]]
            sage: M = [PartialInjection(x) for x in L]
            sage: H = FinitelyGeneratedSubgroup(M)
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 6 vertices
            
        """

        return 'A subgroup of the free group of rank {}, whose Stallings graph has {} vertices'.format(self.ambient_group_rank(), self.stallings_graph_size())


    @staticmethod
    def random_instance(size, ambient_rank=2, verbose=False):
        r"""
        Return a randomly chosen ``FinitelyGeneratedSubgroup``.
        
        ``size`` is expected to be at least 1 and ``ambient_rank`` is expected to be
        at least 0 (a ``ValueError`` will be raised otherwise).
        The ``FinitelyGeneratedSubgroup`` is picked uniformly at random among those
        of the given size and with the same ambient free group rank.
        
        If the option ``verbose`` is set to ``True``, also prints the number of attempts in the
        rejection algorithm.
        
        INPUT:

        - ``size`` -- integer
        - ``ambient_rank`` -- integer, default value 2
        - ``verbose`` -- a boolean, default value False

        OUTPUT:

        - an object of the class ``FinitelyGeneratedSubgroup`` if ``verbose = False``,
          and a tuple of an object of the class ``FinitelyGeneratedSubgroup`` and an integer otherwise

        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: H = FinitelyGeneratedSubgroup.random_instance(12)
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 12 vertices
            
        ::
            
            sage: H = FinitelyGeneratedSubgroup.random_instance(2, ambient_rank = 0)
            sage: H
            A subgroup of the free group of rank 0, whose Stallings graph has 1 vertices
            
        ::
            
            sage: H,c = FinitelyGeneratedSubgroup.random_instance(12,3,verbose=True)
            sage: H
            A subgroup of the free group of rank 3, whose Stallings graph has 12 vertices
            
        ::
            
            sage: c #random
            1
            
            
        ALGORITHM:
        
        This uses a rejection algorithm. It consists in drawing uniformly at random
        a tuple of ``ambient_rank`` partial injections, each of size ``size`` and testing
        whether they define a valid ``FinitelyGeneratedSubgroup``. If they do not, the tuple
        is tossed and another is drawn.
        
        For a justification, see [BNW2008]_.
        

        """
        if size < 1:
            raise ValueError('the first (size) argument must be at least 1')
        if ambient_rank < 0:
            raise ValueError('the second (ambient_rank) argument must be at least 0')
        counter = 0
        while True:
            partial_injections = [PartialInjection.random_instance(size) for _ in range(ambient_rank)]
            H = FinitelyGeneratedSubgroup(partial_injections)
            counter +=1 
            if H.is_valid():
                return (H,counter) if verbose == True else H
            

    @staticmethod
    def from_digraph(G):
        r"""
        Return the ``FinitelyGeneratedSubgroup`` specified by a ``DiGraph``.
        
        ``G`` is expected to be a ``DiGraph`` with edge labels in `[1..r]`, whose vertices are a
        set of non-negative integers including 0 (no verification is made). In particular,
        the empty graph with no vertices is not admissible.        
        The Stallings graph of the finitely generated subgroup produced is obtained by choosing
        0 as the base vertex, folding and pruning `G`.
        
        INPUT:

        - ``G`` -- ``DiGraph``
        
        OUTPUT:

        - an object of the class ``FinitelyGeneratedSubgroup``
        
        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = ['abaBa', 'BaBaB', 'cacBac', 'AbAbb']
            sage: from stallings_graphs.about_automata import bouquet
            sage: G = bouquet(L, alphabet_type='abc')
            sage: H = FinitelyGeneratedSubgroup.from_digraph(G)
            sage: H
            A subgroup of the free group of rank 3, whose Stallings graph has 14 vertices
            
        ::
            
            sage: V = [0]
            sage: E = []
            sage: G = DiGraph([V,E], format='vertices_and_edges', loops=True, multiedges=True)
            sage: H = FinitelyGeneratedSubgroup.from_digraph(G)
            sage: H
            A subgroup of the free group of rank 0, whose Stallings graph has 1 vertices
            
        ::
            
            sage: V = [0]
            sage: E = [(0,0,1)]
            sage: G = DiGraph([V,E], format='vertices_and_edges', loops=True, multiedges=True)
            sage: H = FinitelyGeneratedSubgroup.from_digraph(G)
            sage: H
            A subgroup of the free group of rank 1, whose Stallings graph has 1 vertices

        ::
            
            sage: V = [0]
            sage: E = [(0,0,3)]
            sage: G = DiGraph([V,E], format='vertices_and_edges', loops=True, multiedges=True)
            sage: H = FinitelyGeneratedSubgroup.from_digraph(G)
            sage: H
            A subgroup of the free group of rank 3, whose Stallings graph has 1 vertices
            
        .. WARNING::

            No exception will be raised if the input is not of the expected type.
        
        """
        GG = NT_fold(G)
        GGG = pruning(GG)
        partial_injections = DiGraph_to_list_of_PartialInjection(GGG)
        return FinitelyGeneratedSubgroup(partial_injections)
    

    @staticmethod
    def from_generators(generators, alphabet_type = '123'):
        r"""
        Return the ``FinitelyGeneratedSubgroup`` specified by a set of generators.
        
        ``generators`` is expected to be a list of valid ``Word`` objects, either numerical or
        alphabetical, in accordanc with the value of ``alphabet_type``.
        The ``FinitelyGeneratedSubgroup`` produced represents the subgroup generated by these words.
        It is computed by operating a free group reduction on the elements of generators, computing the
        bouquet of these words and then creating the ``FinitelyGeneratedSubgroup`` specified by the bouquet.
        
        INPUT:

        - ``generators`` -- a tuple of ``Word`` objects
        
        OUTPUT:

        - an object of the class ``FinitelyGeneratedSubgroup``

        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: gens = ['ab','ba']
            sage: H = FinitelyGeneratedSubgroup.from_generators(gens, alphabet_type='abc')
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 3 vertices
            
        ::
            
            sage: gens = [[1,2,5,-1,-2,2,1],[-1,-2,2,3],[1,2,3]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(gens)
            sage: H
            A subgroup of the free group of rank 5, whose Stallings graph has 3 vertices
            
        ::
            
            sage: L = []
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H
            A subgroup of the free group of rank 0, whose Stallings graph has 1 vertices
            
        ::
            
            sage: L = [[2]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 1 vertices

        .. WARNING::

            No exception will be raised if the input is not of the expected type. Also:
            ``generators`` can be an empty list.


        """
        
        if alphabet_type == 'abc':
            gens = [translate_alphabetic_Word_to_numeric(w) for w in generators]
        elif alphabet_type == '123':
            gens = generators
        else:
            raise ValueError('last argument must be "abc" or "123" (default)')
        reduced_gens = [free_group_reduction(w) for w in gens]
        G = bouquet(reduced_gens)
        return FinitelyGeneratedSubgroup.from_digraph(G)


    def ambient_group_rank(self):
        r"""
        Return the rank of the ambient free group of this ``FinitelyGeneratedSubgroup`` object.
        
        Exploits the fact that the rank of the ambient free group is the number of partial
        injections which specify this ``FinitelyGeneratedSubgroup``.
        
        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        
        OUTPUT:

        - an integer
        
        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: H.ambient_group_rank()
            2
            
        ::
            
            sage: L = []
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H.ambient_group_rank()
            0

        """
        return len(self._partial_injections)
    
    def stallings_graph_size(self):
        r"""
        Return the size of this ``FinitelyGeneratedSubgroup``.
        
        The size of the ``FinitelyGeneratedSubgroup`` is the number of vertices of the Stallings
        graph of the subgroup it represents. It is equal to the (common) length of the partial
        injections defining it.
        
        INPUT:

        - ``self`` -- ``FinitelyGeneratedSubgroup``
        
        OUTPUT:

        - an integer
        
        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: H.stallings_graph_size()
            6
            
        ::
            
            sage: L = []
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H.stallings_graph_size()
            1

        """
        if self._partial_injections:
            return self._partial_injections[0].size()
        else:
            return 1
    
    def rank(self):
        r"""
        Return the rank of this ``FinitelyGeneratedSubgroup``.
        
        The rank of this ``FinitelyGeneratedSubgroup`` is equal to ``edges`` - ``vertices`` + 1,
        where ``vertices`` and ``edges`` refer to the number of vertices and edges of the Stallings
        graph of the corresponding subgroup. In particular ``vertices`` is ``stallings_graph_size``
        and ``edges`` is the sum of the domain sizes of the partial injections.
        
        INPUT:

        - ``self`` -- ``FinitelyGeneratedSubgroup``
        
        OUTPUT:

        - an integer
        
        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: H.rank()
            3
            
        :
            
            sage: L = []
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H.rank()
            0
        
        """
        number_of_edges = sum([p.domain_size() for p in self._partial_injections])
        rank = number_of_edges - self.stallings_graph_size() + 1
        return rank
    
    def stallings_graph(self):
        r"""
        Return the Stallings ``DiGraph`` of this ``FinitelyGeneratedSubgroup``.
        
        The Stallings graph of the subgroup of a free group represented
        by this ``FinitelyGeneratedSubgroup`` is an edge-labeled ``DiGraph``. The vertex set
        is `[0..(n-1)]`, where `n` is the ``size`` of the input. The base vertex is 0. If `r` is
        the ``ambient_group_rank`` of the input, each of the `r` partial injections defining the
        ``FinitelyGeneratedSubgroup`` specifies the edges labeled by that particular letter.
        
        INPUT:

        - ``self`` -- ``FinitelyGeneratedSubgroup``
        
        OUTPUT:

        - a DiGraph


        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: G = H.stallings_graph()
            sage: G
            Looped multi-digraph on 6 vertices
            
            ::
            
            sage: L = []
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: G = H.stallings_graph()
            sage: G
            Looped multi-digraph on 1 vertex

        """
        edges = []
        vertices = [0]
        if self._partial_injections:
            vertices = range(self.stallings_graph_size())
            partial_injections_as_lists = [pinj._list_of_images for pinj in self._partial_injections]
            for i,p in enumerate(partial_injections_as_lists):
                edges.extend([(j,image_j,i + 1) for (j,image_j) in enumerate(p)
                                            if not image_j is None])
        G = DiGraph([vertices, edges], format='vertices_and_edges', loops=True, multiedges=True)
        return G
    

    def show_Stallings_graph(self,alphabet_type='abc',visu_tool='plot'):
        r"""
        
        Show the Stallings graph of this ``FinitelyGeneratedSubgroup``.
        
        Edge labels can be of the form `a_1,...,a_r` (``alphabet_type='123'``) or of the form
        `a,b,c,...,z` (``alphabet_type='abc'``). The visualization tool can be ``graph.plot``
        (with a color coding for the base vertex) or Sébastien Labbé's ``TikzPicture``
        `method <http://www.slabbe.org/Sage>`_. 

        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        
        - ``alphabet_type`` -- a string which is either ``'abc'`` or ``'123'``
        
        - ``visu_tool`` -- a string which is either ``'plot'`` or ``'tikz'``
        
        OUTPUT:

        - a visualization of the Stallings graph using ``graph.plot`` or using ``TikzPicture``,
          according to the value of ``visu_tool``. In the ``'tikz'`` case, the output can be saved
          as a ``.png``, ``.pdf`` or ``.tex`` file        

        EXAMPLES ::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: H.show_Stallings_graph(alphabet_type='abc',visu_tool='plot')
            Graphics object consisting of 28 graphics primitives
            
        ::
            
            sage: t = H.show_Stallings_graph(alphabet_type='abc',visu_tool='tikz')
            sage: # one can then type t.png, t.tex, t.pdf
        
        """
        G = self.stallings_graph()
        GG = prepare4visualization_graph(G,alphabet_type=alphabet_type,visu_tool=visu_tool)
        if visu_tool == 'plot':
            return show_rooted_graph(GG,0)
        elif visu_tool == 'tikz':
            from slabbe import TikzPicture
            return TikzPicture.from_graph(GG, merge_multiedges=False, edge_labels=True, color_by_label=False, prog='dot')


    def is_valid(self, verbose=False):
        r"""
        Return whether this ``FinitelyGeneratedSubgroup`` input really defines a subgroup.
        
        If ``verbose`` is set to ``True``, indications are given if the input is not valid, on
        the first reason encountered why it is the case. In order: not all elements of
        ``partial_injections`` are actually partial injections; the graph is not
        connected; some vertex other than 0 has degree less than 2.

        INPUT:

        - ``self`` -- ``FinitelyGeneratedSubgroup``
        - ``verbose`` -- boolean
        
        OUTPUT:
        
        - a boolean if ``verbose`` is set to ``False``; a pair of a boolean and a string otherwise

        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H = FinitelyGeneratedSubgroup(L)
            sage: H.is_valid()
            True
            
        ::
            
            sage: M = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,2,1,None,4,3])]
            sage: K = FinitelyGeneratedSubgroup(M)
            sage: K.is_valid()
            False
            
        ALGORITHM:
        
        The first verification is whether every element of the input's constitutive list of
        partial injections is indeed a valid partial injection. The fact that these partial
        injections all have the same size was checked when this list was made into a
        ``FinitelyGeneratedSubgroup``. The next steps are to verify whether the graph
        induced by these partial injections is connected, and that all the vertices except
        for the base vertex (vertex 0) have degree at least 2.
        
        .. WARNING::
        
            It is not checked whether the input is of the correct type.

        """
        
        from stallings_graphs.partial_injections import is_valid_partial_injection
        b1 = all(is_valid_partial_injection(p._list_of_images) for p in self._partial_injections)
        if verbose:
            if not b1:
                print('not all given partial injections are truly partial injections')
            else:
                print('all given partial injections are okay')
        if b1:        
            G = self.stallings_graph()
            b1 = b1 and G.is_connected()
            if verbose:
                if not b1:
                    print('the resulting graph is not connected')
                else:
                    print('the graph is connected')
        if b1:
            b2 = True
            for v in G.vertices():
                if not(v == 0) and G.degree(v) < 2:
                    b2 = False
                    v_exceptional = v
            b1 = b1 and b2
            if verbose:
                if not b1:
                    print('vertex {} has degree less than 2'.format(v_exceptional))
                else:
                    print('all vertices other than the base vertex (#0) have degree at least 2')
        return b1
    
    
    def __eq__(self, other):
        r"""
        Return whether these two FinitelyGeneratedSubgroup s represent the same subgroup.
        
        Both arguments are expected to be objects of class FinitelyGeneratedSubgroup. A ValueError
        is raised if other is not a FinitelyGeneratedSubgroup. The two objects
        represent the same subgroup if the Stallings graphs (or the tuple of PartialInjection s)
        coincide up to a relabeling of the vertices that fixes the base vertex (vertex 0).
        
        INPUT:

        - ``self`` -- a FinitelyGeneratedSubgroup
        - ``other`` -- a FinitelyGeneratedSubgroup
        
        OUTPUT:
        
        - a boolean

        EXAMPLES ::
            
            sage: from stallings_graphs import FinitelyGeneratedSubgroup, PartialInjection
            sage: L1 = [PartialInjection([1,2,None,4,5,3]), PartialInjection([0,3,4,None,None,None])]
            sage: H1 = FinitelyGeneratedSubgroup(L1)
            sage: L2 = [PartialInjection([1,2,None,5,3,4]), PartialInjection([0,3,5,None,None,None])]
            sage: H2 = FinitelyGeneratedSubgroup(L2)
            sage: gens = ['baaaB','aabAB']
            sage: H3 = FinitelyGeneratedSubgroup.from_generators(gens, alphabet_type='abc')
            sage: othergens = ['b','aabaaBA','abaBAA']
            sage: H4 = FinitelyGeneratedSubgroup.from_generators(othergens, alphabet_type='abc')
            sage: H1 == H2
            True
            
            ::
            
            sage: H2 == H3
            False
            
            ::
            
            sage: H1 == H4
            True
            
            ::
            
            sage: H = FinitelyGeneratedSubgroup.from_generators([])
            sage: K = FinitelyGeneratedSubgroup([])
            sage: H == K
            True
        
        ALGORITHM:
        
        The verification of equality is delegated to the is_the_same method.

        """
        b = isinstance(other, FinitelyGeneratedSubgroup)
        if not b:
            print('the second argument is not a FinitelyGeneratedSubgroup')
            return False
        else:
            G = self.stallings_graph()
            H = other.stallings_graph()
            return are_equal_as_rooted_unlabeled(G,H)
#            return self.is_the_same_as(other)


    def has_index(self):
        r"""
        Return the index of this subgroup if it is finite, ``+Infinity`` otherwise.
        
        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        
        OUTPUT:
        
        - an integer or ``+Infinity``
        
    
        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H.has_index()
            +Infinity
            
        ::
            
            sage: H = FinitelyGeneratedSubgroup([])
            sage: H.has_index()
            1
            
        ::
            
            sage: HH = FinitelyGeneratedSubgroup.from_generators(['ab', 'ba', 'Abab'], alphabet_type = 'abc')
            sage: HH.has_index()
            2
            
            
        """
        if all(p.is_permutation() for p in self._partial_injections):
            return self.stallings_graph_size()
        else:
            from sage.rings.infinity import Infinity as oo
            return oo

    def basis(self, alphabet_type = 'abc'):
        r"""
        Return a basis of this subgroup.
        
        The input is expected to be an object of the class ``FinitelyGeneratedSubgroup``.
        The variable ``alphabet_type`` determines whether the words in the output
        are numerical or alphabetic.
        
        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        - ``alphabet_type`` -- a string, which is either ``'abc'`` or ``'123'``
        
        OUTPUT: A list of objects of the class ``Word``
        
    
        EXAMPLES::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = [[3,1,-2,-1,3],[1,2,-1,-2,1,2],[1,2,-3,-3,1]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H.basis(alphabet_type = '123')
            [word: -3,1,2,-1,-3, word: -2,-1,2,1,-2,-1, word: -1,3,3,-2,-1]
            
        ::
            
            sage: H.basis()
            [word: CabAC, word: BAbaBA, word: AccBA]
            
        ::
            
            sage: H = FinitelyGeneratedSubgroup([])
            sage: H.basis()
            []
            
        ::
            
            sage: H = FinitelyGeneratedSubgroup.from_generators(['A'],alphabet_type = 'abc')
            sage: H.basis()
            [word: a]
            
        """
        G = self.stallings_graph()
        T,L,D = spanning_tree_and_paths(G)
        B = basis_from_spanning_tree(G, T, D,alphabet_type=alphabet_type)
#        if alphabet_type == 'abc':
#            B = [translate_numeric_Word_to_alphabetic(w) for w in B]
        return B
    
    def intersection(self, K):
        r"""
        Return the intersection of two subgroups.
        
        Both inputs are expected to be objects of class ``FinitelyGeneratedSubgroup``. We
        understand both to be subgroups of the rank `r` free group, where `r` is the maximum
        of the ambient group ranks of the input subgroups. The intersection is also
        understood to be a subgroup of the same rank `r` free group.
        
        INPUT:

        - ``self`` -- ``FinitelyGeneratedSubgroup``
        - ``other`` -- ``FinitelyGeneratedSubgroup``
        
        OUTPUT: 
        
        - ``FinitelyGeneratedSubgroup``
        
        EXAMPLES ::
        
            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = [[2,1,-2,2,1,-2], [2,3,1,-3,3,1,-2]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: M = ['ab','ba', 'bdaB']
            sage: K = FinitelyGeneratedSubgroup.from_generators(M, alphabet_type = 'abc')
            sage: H.intersection(K)
            A subgroup of the free group of rank 4, whose Stallings graph has 1 vertices
            
        ::
            
            sage: L = ['ab', 'aaBa', 'bbAb']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
            sage: M = ['ab', 'bbbb', 'baba', 'aa']
            sage: K = FinitelyGeneratedSubgroup.from_generators(M, alphabet_type = 'abc')
            sage: S = H.intersection(K)
            sage: S.basis()
            [word: baba, word: baBaBB, word: ab, word: AbAA]
    
        """
        r = max(self.ambient_group_rank(),K.ambient_group_rank())
        GH = self.stallings_graph()
        GK = K.stallings_graph()
        GHK = fibered_product(GH,GK)
        V = GHK.connected_component_containing_vertex((0,0))
        G = GHK.subgraph(V)
        G = normalize_vertex_names(G)
        G = pruning(G)
        n = len(G.vertices())
        pinj = [PartialInjection([None for _ in range(n)]) for _ in range(r)]
        if G.edges():
            PI = DiGraph_to_list_of_PartialInjection(G)
            for a in range(len(PI)):
                pinj[a] = PI[a]
        return FinitelyGeneratedSubgroup(pinj)

    def is_malnormal(self, alphabet_type='123', witness=False):
        r"""
        Return whether this subgroup is malnormal.
        
        The first argument is assumed to be an object of class ``FinitelyGeneratedSubgroup``.
        The second argument determines whether words are to be represented numerically or
        alphabetically. This makes a difference only if ``witness`` is set to ``True``. In that
        case, the output includes witness words `s,t` such that `s` belongs to the intersection
        of `H` and `t^{-1} H t`.

        INPUT:

        - ``self`` -- ``FinitelyGeneratedSubgroup``
        - ``alphabet_type`` -- a string which is either ``'abc'`` or ``'123'``
        - ``witness`` -- a boolean
        
        OUTPUT: 
        
        - a boolean if ``witness`` is set to ``False``; and if ``witness`` is set to ``True``, then
          a tuple of the form ``(True, None, None)`` if the subgroup is malnormal, and of the form
          ``(False,s,t)`` if it is not, where `s` and `t` are of the class ``Word``.

        EXAMPLES ::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = [[2,1,-2,2,1,-2], [2,3,1,-3,3,1,-2]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(L)
            sage: H.is_malnormal()
            False

        ::

            sage: L = ['ab', 'aaBa', 'bbAb']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
            sage: H.is_malnormal()
            False

        ::

            sage: L = ['baB', 'ababa', 'aababbb']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
            sage: H.is_malnormal()
            True

        ::

            sage: M = ['ab', 'bbbb', 'baba', 'aa']
            sage: K = FinitelyGeneratedSubgroup.from_generators(M, alphabet_type = 'abc')
            sage: K.is_malnormal()
            False

        ::

            sage: H = FinitelyGeneratedSubgroup.from_generators(['a'], alphabet_type = 'abc')
            sage: H.is_malnormal()
            True

        ::

            sage: H = FinitelyGeneratedSubgroup([])
            sage: H.is_malnormal()
            True

        ::
        
            sage: L = ['aba', 'abb', 'aBababA']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type='abc')
            sage: H.is_malnormal(alphabet_type='abc', witness=True)
            (False, word: aba, word: aB)
            
        TODO :        
        The algorithm is quadratic and that is rather inefficient for large instances. One would probably gain significant time if, after verifying non malnormality, one could explore the (non-diagonal) connnected components starting with the smaller ones.

        """
        G = self.stallings_graph()
        GG = fibered_product(G,G)
        CC = GG.connected_components()
        # Let baseCC be the connected component containing vertex (0,0): it is isomorphic to G.
        # The number E of edges of GG outside baseCC is len(GG.edges()) - len(G.edges())
        # and the corresponding number of vertices V is len(GG.vertices()) - len(G.vertices()).
        # The connected components of GG other than baseCC are all trees if and only if
        # V - E = number of (non-base) connected components.
        # All together, the formula to verify is
        # len(GG.vertices()) + len(G.edges()) - len(G.vertices()) - len(GG.edges()) =
        # len(CC) - 1
        if len(GG.vertices()) + len(G.edges()) - len(G.vertices()) - len(GG.edges()) == len(CC) - 1:
            return True if witness == False else (True,None,None)
        # now the subgroup is not malnormal
        if witness == False:
            return False
        # now the subgroup is not malnormal and we need a witness
        baseCC = GG.connected_component_containing_vertex((0,0))
        CC.remove(baseCC)
        look_for_non_trivial_CC = True
        i = 0
        while look_for_non_trivial_CC:
            GGX = GG.subgraph(vertices=CC[i])
            if len(GGX.edges()) > len(CC[i]) - 1:
                look_for_non_trivial_CC = False
            else:
                i += 1
        X = CC[i]
        # now X is an interesting connected component
        T,L,P = spanning_tree_and_paths(GGX,root=X[0])
        E = list(GGX.edges())
        F = T.edges()
        for e in F:
            E.remove(e)
        (p,q,a) = E[0]
        u = P[p] + Word([a]) + group_inverse(P[q])
        TG,LG,PG = spanning_tree_and_paths(G)
        s = free_group_reduction(PG[X[0][0]] + u + group_inverse(PG[X[0][0]]))
        t = free_group_reduction(PG[X[0][1]] + group_inverse(PG[X[0][0]]))
        return (False, s, t) if alphabet_type=='123' else (False, translate_numeric_Word_to_alphabetic(s),translate_numeric_Word_to_alphabetic(t))

    
    def contains_element(self, w, alphabet_type = '123'):
        r"""
        Return whether the subgroup contains the word `w`.
        
        ``w`` is expected to be a ``Word`` on a numerical alphabet (``alphabet_type = '123'``) or
        on a letter alphabet (``alphabet_type = 'abc'``).
        
        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        - ``w`` -- a ``Word``
        - ``alphabet_type`` -- a string which is either ``'abc'`` or ``'123'``
        
        OUTPUT:
        
        - a boolean

        EXAMPLES ::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = ['ab','ba', 'aBaa']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
            sage: w = Word([1,-2,-2])
            sage: H.contains_element(w)
            False

        ::

            sage: w = Word('abba')
            sage: H.contains_element(w, alphabet_type = 'abc')
            True

        ::

            sage: w = Word()
            sage: H.contains_element(w)
            True

        ::

            sage: H = FinitelyGeneratedSubgroup([])
            sage: w = Word()
            sage: H.contains_element(w)
            True

        ::

            sage: w = Word([1,2,1])
            sage: H.contains_element(w)
            False

        """
        if alphabet_type == 'abc' and len(w) > 0:
            w = translate_alphabetic_Word_to_numeric(w)
        G = self.stallings_graph()
        return (image_of_word(G,w) == 0)


    def contains_subgroup(self, other):
        r"""
        Return whether the subgroup contains another subgroup.
        
        ``other`` is expected to be an object of class ``FinitelyGeneratedSubgroup``.
        
        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        - ``other`` -- a ``FinitelyGeneratedSubgroup``
        
        OUTPUT:
        
        - a boolean

        EXAMPLES ::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = ['ab','ba', 'aBaa']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
            sage: M = ['ab','ba']
            sage: K = FinitelyGeneratedSubgroup.from_generators(M, alphabet_type = 'abc')
            sage: H.contains_subgroup(K)
            True

        ::

            sage: LL = ['abba','bAbA']
            sage: K = FinitelyGeneratedSubgroup.from_generators(LL, alphabet_type = 'abc')
            sage: H.contains_subgroup(K)
            True

        ::

            sage: H = FinitelyGeneratedSubgroup([])
            sage: H.contains_subgroup(K)
            False
            
        ::

            sage: K.contains_subgroup(H)
            True

        """
        B = other.basis(alphabet_type='123')
        return all(self.contains_element(b) for b in B)

    def conjugated_by(self, w, alphabet_type = '123'):
        r"""
        Return the conjugate of this subgroup by the given word.
        
        ``w`` is expected to be a Word, on a numerical or letter alphabet, depending
        on the value of ``alphabet_type``. The conjugate of a subgroup `H` by a word `w`
        is the subgroup `w^{-1} H w`.
        
        INPUT:

        - ``self`` -- a ``FinitelyGeneratedSubgroup``
        - ``w`` -- a Word
        - ``alphabet_type`` -- a string which can be either ``'abc'`` or ``'123'``
        
        OUTPUT:
        
        - a ``FinitelyGeneratedSubgroup``

        EXAMPLES ::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L = ['ab','ba', 'aBaa']
            sage: H = FinitelyGeneratedSubgroup.from_generators(L, alphabet_type = 'abc')
            sage: H
            A subgroup of the free group of rank 2, whose Stallings graph has 4 vertices
            
        ::
        
            sage: w1 = Word('bA')
            sage: K1 = H.conjugated_by(w1, alphabet_type='abc')
            sage: K1
            A subgroup of the free group of rank 2, whose Stallings graph has 4 vertices
            
        ::
        
            sage: w2 = Word('bAA')
            sage: K2 = H.conjugated_by(w2, alphabet_type='abc')
            sage: K2
            A subgroup of the free group of rank 2, whose Stallings graph has 5 vertices
            
        ::
        
            sage: w = Word('abba')
            sage: K3 = H.conjugated_by(w, alphabet_type='abc')
            sage: H == K3
            True
        



        """
        n = self.stallings_graph_size()
        lenw = len(w)
        if alphabet_type == 'abc':
            w = translate_alphabetic_Word_to_numeric(w)
        G = self.stallings_graph()
        (q,m,qq) = image_of_word(G, w, qinitial = 0, trace = True)
        if q is None:
            G.add_vertices(range(n, n + lenw - m))
            if w[m] > 0:
                G.add_edge((qq, n, w[m]))
            else:
                G.add_edge((n, qq, -w[m]))
            for i in range(m + 1, lenw):
                if w[i] > 0:
                    G.add_edge((n + i - m - 1, n + i - m, w[i]))
                else:
                    G.add_edge((n + i - m, n + i - m - 1, - w[i]))
            future_base_vertex = n + lenw - m - 1
        else:
            future_base_vertex = q
#
        G = exchange_labels(G,0,future_base_vertex)
        return FinitelyGeneratedSubgroup.from_digraph(G)


    def is_conjugated_to(self, other, conjugator=False, alphabet_type = '123'):
        r"""
        Return whether self and other are conjugated.

        If ``conjugator`` is set to ``True``, the output will also include a conjugator (``None`` if
        the two subgroups are not conjugated). A word `w` is a conjugator of `H` into `K` if
        `w^{-1} H w = K`. 

        INPUT:

        - ``other`` -- ``FinitelyGeneratedSubgroup``
        - ``conjugator`` -- boolean
        - ``alphabet_type`` -- a string which can be either ``'abc'`` or ``'123'``

        OUTPUT: 
        
        - a boolean or, if ``conjugator`` is ``True``, a tuple consisting of a boolean and a
          ``Word`` or ``None``.

        EXAMPLES::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: generators = ['abCA', 'abbaBA', 'aCacA', 'abbbcA']
            sage: H = FinitelyGeneratedSubgroup.from_generators(generators, alphabet_type='abc')
            sage: other_gens = ['ba', 'bbcb', 'bbcc', 'bbaBB']
            sage: K = FinitelyGeneratedSubgroup.from_generators(other_gens, alphabet_type='abc')
            sage: H.is_conjugated_to(K)
            True
            
        ::
            
            sage: b,w = H.is_conjugated_to(K,conjugator=True,alphabet_type = 'abc')
            sage: w
            word: ac

        """
        GH = self.stallings_graph()
        if conjugator:
            CRGH,w1 = cyclic_reduction(GH,trace=True)
        else:
            CRGH = cyclic_reduction(GH)
        vCRGH = len(CRGH.vertices())
        #
        GK = other.stallings_graph()
        if conjugator:
            CRGK,w3 = cyclic_reduction(GK,trace=True)
        else:
            CRGK = cyclic_reduction(GK)
        vCRGK = len(CRGK.vertices())
        #
        if vCRGH != vCRGK:
            return (False, None) if conjugator else False
        #
        KK = FinitelyGeneratedSubgroup.from_digraph(CRGK)
        for v in CRGH.vertices():
            modifiedCRGH = exchange_labels(CRGH,0,v)
            HH = FinitelyGeneratedSubgroup.from_digraph(modifiedCRGH)
            if HH == KK:
                if conjugator:
                    T,list_of_leaves,path_in_tree = spanning_tree_and_paths(CRGH)
                    w2 = path_in_tree[v]
                    w = w1 + w2 + group_inverse(w3)
                    w = free_group_reduction(w)
                    if alphabet_type == 'abc':
                        w = translate_numeric_Word_to_alphabetic(w)
                    return (True,w)
                else:
                    return True
        return (False, None) if conjugator else False

    def SW_is_free_factor_of_ambient(self, complement = True, alphabet_type = '123'):
        r"""
        Return whether ``self`` is a free factor of the ambient group and, if ``complement`` is
        set to ``True``, gives either a statement about it not being a free factor, or if it is,
        a basis of a complement of ``self`` (in numerical or in alphabetic form depending on
        ``alphabet_type``).

        INPUT:

        - ``complement``-- boolean
        - ``alphabet_type`` -- a string which can be either ``'abc'`` or ``'123'``

        OUTPUT: 
        
        - a boolean if ``complement`` is ``False`` and a pair of a boolean and either a string of a list of objects of type ``Word`` otherwise

        EXAMPLES::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: L1 = ['ac','bacd','ed']
            sage: H1 = FinitelyGeneratedSubgroup.from_generators(L1, alphabet_type='abc')
            sage: H1.SW_is_free_factor_of_ambient(complement = True, alphabet_type = 'abc')
            (True, [word: baE, word: B])

        ::

            sage: L2 = ['acac','bacd','ed']
            sage: H2 = FinitelyGeneratedSubgroup.from_generators(L2, alphabet_type='abc')
            sage: H2.SW_is_free_factor_of_ambient(complement = True, alphabet_type='abc')
            (False, 'the 1st argument is not a free factor of the second')

        ::

            sage: H = FinitelyGeneratedSubgroup.from_generators(['A','d'], alphabet_type='abc')
            sage: H.SW_is_free_factor_of_ambient(complement = True, alphabet_type='abc')
            (True, [word: b, word: c])
        
        ALGORITHM:
    
            The algorithm implemented is from [SW2008]_. Be aware that the worst-case complexity
            is polynomial in the size of the argument subgroup but exponential in the rank
            difference between that subgroup and the ambient group.
        """
        from stallings_graphs.about_free_factors import SilvaWeil_free_factor_of_ambient
        if complement:
            (valeur,base) = SilvaWeil_free_factor_of_ambient(self, maxletter = 0, complement = True)
            if alphabet_type == 'abc' and valeur == True:
                base = [translate_numeric_Word_to_alphabetic(w) for w in base]
            return (valeur,base)
        else:
            return SilvaWeil_free_factor_of_ambient(self, maxletter = 0, complement = False)
    
    
    def SW_is_free_factor_of(self, other, complement = True, alphabet_type = '123'):
        r"""
        Return whether ``self`` is a free factor of ``other`` and, if ``complement`` is
        set to ``True``, gives either a statement about it not being a free factor, or if it is,
        a basis of a complement of ``self`` in ``other`` (in numerical or in alphabetic form
        depending on ``alphabet_type``).
        
        ``other`` is expected to be a ``FinitelyGeneratedSubgroup``

        INPUT:

        - ``other`` -- ``FinitelyGeneratedSubgroup``
        - ``complement`` -- boolean
        - ``alphabet_type`` -- a string which can be either ``'abc'`` or ``'123'``

        OUTPUT: 
        
        - a boolean if ``complement`` is ``False``, and a pair of a boolean and either a string or a list of objects of type ``Word`` otherwise

        EXAMPLES::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: LH = [[2,-3,1,3,2,3,-2,-1,2,-3,-1], [3,1,1,1,-3,-1], [1,3,-2,-1,2,-1,2], [3,2,3,-1,2,-1]]
            sage: LK = [[2,-3], [1,1], [1,3,-2,1,2,-3,-1], [3,2], [3,1,-3,-1], [1,3,2,-1], [1,3,3,-1], [1,3,1,-3]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
            sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
            sage: H.SW_is_free_factor_of(K, complement = True)
            (True, [word: 3,2,3,1,2,-1, word: 32, word: 3,1,3,-1, word: 11])
        
        ::
        
            sage: H.SW_is_free_factor_of(K, complement = False)
            True
        
        ::
        
            sage: LH = [[-3,1,-2,-1,-1,-3,2,2,3], [-3,-1,-1,3,1,1,-3,-1,3,1,3,3], [-3,1,3,-1,-1,-3,1,1,1,3,-1,-1], [1,1,-3,1,3,1,1,-3,-1,3]]
            sage: LK = [[1,1,2,-1,3], [1,1,3,-1], [-3,1,3,-1,-1], [-3,1,1,3], [-3,2,3], [1,3,3]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
            sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
            sage: H.SW_is_free_factor_of(K, complement = True)
            (False, 'the 1st argument is not a free factor of the second')
        
        ::
        
            sage: H.SW_is_free_factor_of(K, complement = False)
            False
        
        ::
        
            sage: LH = [[3,1,-2,-1,-1,-3,2,2,3], [-3,-1,-1,3,1,1,-3,-1,3,1,3,3], [-3,1,3,-1,-1,-3,1,1,1,3,-1,-1], [1,1,-3,1,3,1,1,-3,-1,3]]
            sage: LK = [[1,1,2,-1,3], [1,1,3,-1], [-3,1,3,-1,-1], [-3,1,1,3], [-3,2,3], [1,3,3]]
            sage: H = FinitelyGeneratedSubgroup.from_generators(LH, alphabet_type='123')
            sage: K = FinitelyGeneratedSubgroup.from_generators(LK, alphabet_type='123')
            sage: H.SW_is_free_factor_of(K, complement = True)
            (False, '1st argument not contained in 2nd')
        
        ::
        
            sage: H.SW_is_free_factor_of(K, complement = False)
            False
        
        ::
        
            sage: H = FinitelyGeneratedSubgroup.from_generators(['bba','bAbaB'], alphabet_type='abc')
            sage: K = FinitelyGeneratedSubgroup.from_generators(['a', 'bb', 'bAbaB'], alphabet_type='abc')
            sage: H.SW_is_free_factor_of(K, complement = True, alphabet_type = 'abc')
            (True, [word: BB])
        
        ::
        
            sage: H.SW_is_free_factor_of(K, complement = False, alphabet_type = 'abc')
            True
        
        ::
        
            sage: H = FinitelyGeneratedSubgroup.from_generators(['a','B'], alphabet_type='abc')
            sage: K = FinitelyGeneratedSubgroup.from_generators(['a','b','d'], alphabet_type='abc')
            sage: H.SW_is_free_factor_of(K, complement = True, alphabet_type = 'abc')
            (True, [word: d])
        
        ::
        
            sage: H.SW_is_free_factor_of(K, complement = False, alphabet_type = 'abc')
            True

        
        ALGORITHM:
    
            The algorithm implemented is from [SW2008]_. Be aware that the worst-case complexity
            is polynomial in the size of the two argument subgroups, but exponential in the
            difference between their ranks.
        """

        from stallings_graphs.about_free_factors import SilvaWeil_free_factor_of
        if complement:
            (valeur,base) = SilvaWeil_free_factor_of(self, other, complement = True)
            if alphabet_type == 'abc' and valeur == True:
                base = [translate_numeric_Word_to_alphabetic(w) for w in base]
            return (valeur,base)
        else:
            return SilvaWeil_free_factor_of(self, other, complement = False)


    def algebraic_extensions(self):
        r"""
        Return a dictionary listing the algebraic extensions of ``self``. The keys are integers
        without any particular meaning, except key 0 corresponds to ``H`` itself. The entries are
        lists of an algebraic extension, sets of keys corresponding to parents and children
        of this extension (not a Hasse diagram of the containment relation, but including such
        a diagram), and a boolean indicating whether the extension is e-algebraic.
        
        For a definition of algebraic and e-algebraic extensions, see [MVW2007]_.
        
        INPUT:

        - ``self`` -- an object of the class ``FinitelyGeneratedSubgroup``.

        OUTPUT: 
        
        - a dictionary whose keys are integers and whose entries are lists of an object of type
          ``FinitelyGeneratedSubgroup``, two sets of keys, and a boolean

        EXAMPLES::

            sage: from stallings_graphs import FinitelyGeneratedSubgroup
            sage: from stallings_graphs.about_free_factors import compute_algebraic_extensions
            sage: testgens = ['aba','bab']
            sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
            sage: testH.algebraic_extensions()
            {0: [A subgroup of the free group of rank 2, whose Stallings graph has 5 vertices,
              set(),
              {1},
              True],
             1: [A subgroup of the free group of rank 2, whose Stallings graph has 1 vertices,
              {0},
              set(),
              True]}

        ::

            sage: testgens = ['ab','cd']
            sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
            sage: testH.algebraic_extensions()
            {0: [A subgroup of the free group of rank 4, whose Stallings graph has 3 vertices,
              set(),
              set(),
              True]}

        ::

            sage: testgens = ['ABBaaBABa','Baba','Abababba','AbabbABa','ABabAba']
            sage: testH = FinitelyGeneratedSubgroup.from_generators(testgens,alphabet_type='abc')
            sage: testH.algebraic_extensions()
            {0: [A subgroup of the free group of rank 2, whose Stallings graph has 10 vertices,
              set(),
              {3, 6, 11},
              True],
             3: [A subgroup of the free group of rank 2, whose Stallings graph has 1 vertices,
              {0, 6, 11},
              set(),
              True],
             6: [A subgroup of the free group of rank 2, whose Stallings graph has 3 vertices,
              {0, 11},
              {3},
              True],
             11: [A subgroup of the free group of rank 2, whose Stallings graph has 8 vertices,
              {0},
              {3, 6},
              True]}

        """

        original_basis = self.basis(alphabet_type='123')
        from stallings_graphs.about_free_factors import compute_algebraic_extensions
        semilattice_AE = compute_algebraic_extensions(self)
        semilattice = {}
        for key in semilattice_AE.keys():
            newgenerators = original_basis + semilattice_AE[key][2]
            newextension = FinitelyGeneratedSubgroup.from_generators(newgenerators, alphabet_type='123')
            semilattice[key] = [newextension, semilattice_AE[key][0], semilattice_AE[key][1], semilattice_AE[key][4]]
        return semilattice
                                
            


