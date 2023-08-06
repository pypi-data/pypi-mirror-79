# -*- coding: utf-8 -*-
r"""
The class ``PartialInjection`` is meant to represent partial injections on a set of the form `[0..(n-1)]`.

The representation of a ``PartialInjection`` is the list of images of `0,\dots,n-1`, in that order, with ``None`` in places where the partial injection is not defined.

Methods implemented in this file:

- definition of a ``PartialInjection`` from its list of images

- random instance

- ``size`` -- the length of the list of images (that is, the integer `n` mentioned above)

- ``domain_size`` -- the number of entries different from ``None``

- ``inverse_partial_injection``

- ``is_permutation``

- ``orbit_decomposition``



EXAMPLES::

    sage: from stallings_graphs import PartialInjection
    sage: L = [0,3,None,2,4,None,5,1]
    sage: p = PartialInjection(L)
    sage: p
    A partial injection of size 8, whose domain has size 6
    
    ::
    
    sage: pinj = PartialInjection.random_instance(10)
    sage: pinj # random
    A partial injection of size 10, whose domain has size 7
    

AUTHOR:

- Pascal WEIL (2018-11-26): initial version
  CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr>


"""

from sage.structure.sage_object import SageObject
from sage.misc.prandom import shuffle, randint
from random import randrange
import itertools
from partial_injections_misc import *

class PartialInjection(SageObject):
    r"""
    Define the class ``PartialInjection``.
    
    The representation of a ``PartialInjection`` is a list of length `n`, whose entries are either elements of
    `range(n)` without any repetition, or ``None`` (the list of images of the elements of ``range(n)``). The integer `n` is
    seen as the size of the ``PartialInjection``.
    
    A ``PartialInjection`` can be created from
    
    - a list (its list of images)
    
    or
    
    - a random instance.
    
    EXAMPLES ::
        
        sage: from stallings_graphs import PartialInjection
        sage: L = [0,3,None,2,4,None]
        sage: p = PartialInjection(L)
        sage: p
        A partial injection of size 6, whose domain has size 4
        
        ::
        
        sage: PartialInjection.random_instance(1000)   # random
        A partial injection of size 1000, whose domain has size 969

    
    """

    def __init__(self, list_of_images, check=False):
        r"""
        Create a ``PartialInjection`` by specifying the list of images of `[0..n-1]`.
        
        This list ``list_of_images``, if it has length `n`, is expected to have entries that are either
        elements of `[0..n-1]`, without any repetition, or ``None``. This property is verified
        in ``__init__`` if ``check`` is set to ``True``.
        The empty list is acceptable: it represents the (unique) map from the empty
        set into itself.
    
        INPUT:

        - ``list_of_images`` -- list
        
        -  ``check``-- boolean
        

        OUTPUT:

        - an object of class ``PartialInjection``

        EXAMPLES::
            
            sage: from stallings_graphs import PartialInjection
            sage: L = [0,3,None,2,4,None]
            sage: p = PartialInjection(L)
            sage: p
            A partial injection of size 6, whose domain has size 4
            
            ::
            
            sage: L = []
            sage: p = PartialInjection(L)
            sage: p
            A partial injection of size 0, whose domain has size 0
            
        """

        if check == True:
            if not isinstance(list_of_images, list):
                raise TypeError('list_of_images(={}) must be of type list'.format(list_of_images))
            if not is_valid_partial_injection(list_of_images):
                raise ValueError('list_of_images(={}) does not represent a partial injection from [0..{}] into itself'.format(list_of_images, len(list_of_images) - 1))
#                
        self._list_of_images = list_of_images
            

    
    def __repr__(self):
        r"""
        Return a description of this ``PartialInjection``.
        
        The description consists of its size and the size of its domain (that is:
        the number of entries different from ``None``).
        
        INPUT:

        - ``self`` -- an object of class ``PartialInjection``.

        OUTPUT:

        - a sentence describing the corresponding partial injection.
        
        EXAMPLES::
        
            sage: from stallings_graphs import PartialInjection
            sage: L = [0,3,None,2,4,None]
            sage: p = PartialInjection(L)
            sage: p
            A partial injection of size 6, whose domain has size 4
            
        """

        return 'A partial injection of size {}, whose domain has size {}'.format(self.size(), self.domain_size())
    
    
    def __eq__(self, other):
        r"""
        Return whether these two ``PartialInjection`` objects are equal.
        
        ``other`` is expected to be, like ``self``, an object of class ``PartialInjection``, a ``ValueError``is raised
        if that is not the case. Two ``PartialInjection``objects are equal when their ``list_of_images`` are equal

        INPUT:

        - ``self`` -- ``PartialInjection``

        - ``other`` -- `PartialInjection``
        
        OUTPUT:

        - boolean
        
        EXAMPLES ::
            
            sage: from stallings_graphs import PartialInjection
            sage: p1 = PartialInjection([1,2,None,4,5,3])
            sage: p2 = PartialInjection([0,3,4,None,None,None])
            sage: p1 == p2
            False
            
            ::
            
            sage: p1 = PartialInjection([])
            sage: p2 = PartialInjection([None])
            sage: p1 == p2
            False

            ::
            
            sage: p1 = PartialInjection([None])
            sage: p2 = PartialInjection([None,None])
            sage: p1 == p2
            False


        """
        b = isinstance(other, PartialInjection)
        if not b:
            print 'the second argument is not a PartialInjection'
            return False
        return (self._list_of_images == other._list_of_images)


    def size(self):
        r"""
        Return the size of this ``PartialInjection``.
        
        The size of a ``PartialInjection`` is the length of the list that represents it.
    
        INPUT:

        - ``self`` -- ``PartialInjection``
        
        OUTPUT:

        - integer
        
        EXAMPLES::
        
            sage: from stallings_graphs import PartialInjection
            sage: L = [0,3,None,2,4,None]
            sage: p = PartialInjection(L)
            sage: p.size()
            6
            
        """
        return len(self._list_of_images)
    
    
    def domain_size(self):
        r"""
        Return the size of the domain of this ``PartialInjection``.
        
        Computes the size of the domain of this partial injection. If it has size `n`, its domain size
        is the number of elements of `range(n)` with an image, that is, `n - \ell`, where `\ell` is the number of ``None``.
        
        INPUT:

        - ``self`` -- ``PartialInjection``
        
        OUTPUT:

        - integer
        
        EXAMPLES::
        
            sage: from stallings_graphs import PartialInjection
            sage: L = [0,3,None,2,4,None]
            sage: p = PartialInjection(L)
            sage: p.domain_size()
            4
            
        """
        p = self._list_of_images
        return len(p) - p.count(None)
    

    def inverse_partial_injection(self):
        r"""
        Return the inverse of a ``PartialInjection``.
    
        INPUT:

        - ``self`` -- ``PartialInjection``
        
        OUTPUT:

        - a ``PartialInjection``
        
        EXAMPLES::
        
            sage: from stallings_graphs import PartialInjection
            sage: p = PartialInjection([6, None, 5, 0, 11, 2, None, 3, 9, 1, 7, 10])
            sage: q = p.inverse_partial_injection()
            sage: q._list_of_images
            [3, 9, 5, 7, None, 2, 0, 10, None, 8, 11, 4]
    
        """
        p = self._list_of_images
        q = [None for _ in range(len(p))]
        for i,j in enumerate(p):
            if j != None:
                q[j] = i
        return PartialInjection(q)
    

    def is_permutation(self):
        r"""
        Return whether whether a ``PartialInjection`` is a permutation.
        
        A partial injection is a permutation if and only if its domain size is equal to its size.

        INPUT:

        - ``self`` -- ``PartialInjection``
        
        OUTPUT:

        - boolean
        
        EXAMPLES::
        
            sage: from stallings_graphs import PartialInjection
            sage: p = PartialInjection([6, None, 5, 0, 11, 2, None, 3, 9, 1, 7, 10])
            sage: p.is_permutation()
            False
            
            ::
    
            sage: p = PartialInjection([6, 4, 5, 0, 11, 2, 8, 3, 9, 1, 7, 10])
            sage: p.is_permutation()
            True
        
        """
        return self.size() == self.domain_size()
    
    def orbit_decomposition(self):
        r"""
        Return the orbit decomposition of a ``PartialInjection``.
        
        A partial injection admits a unique decomposition into its `\textit{maximal orbits}`: a list of sequences
        and a list of cycles. The particular case of a permutation is that where each orbit is a cycle.
            
        INPUT:

        - ``self`` -- ``PartialInjection``
        
        OUTPUT:

        - List of Lists
        
        EXAMPLES::
            
            sage: from stallings_graphs import PartialInjection
            sage: p = PartialInjection([6, None, 5, 0, 11, 2, None, 3, 9, 1, 7, 10])
            sage: p.orbit_decomposition()
            ([[8, 9, 1], [4, 11, 10, 7, 3, 0, 6]], [[2, 5]])
        
        """
        p = self._list_of_images
        sequence_list = []
        cycle_list = []
        d = {}
        deja_vus = set()
        for i in range(len(p)):
            if not (i in deja_vus):
                d[i] = [i]
                deja_vus.add(i)
                j = p[i]
                while (j != None) and not (j in d.keys()):
                    d[i].append(j)
                    deja_vus.add(j)
                    j = p[j]
                if j == i:
                    cycle_list.append(d[i])
                    del d[i]
                else:
                    if j in d.keys():
                        d[i].extend(d[j])
                        del d[j]
        sequence_list = [d[i] for i in d.keys()]
        return sequence_list, cycle_list

    @staticmethod
    def random_instance(size,statistics=False):
        r"""
        Returns a randomly chosen ``PartialInjection`` of given ``size``.
        
        ``size`` is expected to be a positive integer. If ``statistics`` is set to ``True``,
        the method also returns the number of orbits of the partial injection that are sequences.
        This number is expected to be asymptotically equivalent to `\sqrt n`, with standard deviation `o(\sqrt n)`, where `n` is equal to ``size``.
    
        INPUT:

        - ``size`` -- integer

        - ``statistics`` -- boolean

        OUTPUT: if ``statistics = False``:

        - an object of the class ``PartialInjection``
        
        otherwise:
        
        - a pair of an integer and an object of class ``PartialInjection``

        EXAMPLES::
        
            sage: from stallings_graphs import PartialInjection
            sage: rand_inj = PartialInjection.random_instance(10)
            sage: rand_inj._list_of_images   # random
            [0, 4, 2, None, 3, 9, 7, 8, 6, None]
            
            ::
            
            sage: rand_inj = PartialInjection.random_instance(10)
            sage: rand_inj._list_of_images   # random
            [2, 4, 6, 0, 3, None, 9, 5, None, None]
            
        ALGORITHM:
        
            Tha algorithm implemented here is that in [Bassino, Nicaud, Weil. Random generation of finitely
            generated subgroups of a free group, International Journal of Algebra and Computation 18 (2008) 1-31].
            It performs in linear time, except for a preprocessing which is cached.
        """
        
    # first: produce two lists, namely the list of sizes of cycle
    # components and the list of sizes of stick components
        n0 = size
        cycles = []
        sticks = []
        Inj = number_of_partial_injections_list(size + 1)
        while size > 0:
            # compute the size k of a component
            dice = randint(1,Inj[size])
            k = 1
            T = 1
            S = 2 * Inj[size - 1]
            while dice > S:
                T = T * (size - k)
                k = k + 1
                S = S + (k + 1) * T * Inj[size - k]
            new_dice = randrange(k + 1)
            if new_dice == k:
                cycles.append(k)
            else:
                sticks.append(k)
            size = size - k
        # when the while loop is over, we have two lists: the sizes of cycle components and the sizes of stick components.
        
    # Now turn the lists of sizes of cycles and sticks to a scheme of a permutation
        schema_of_rand_inj = []
        it = itertools.count(0)
        b = next(it)
        for a in cycles:
            for _ in range(a-1):
                schema_of_rand_inj.append(next(it))
            schema_of_rand_inj.append(b)
            b = next(it)
        for a in sticks:
            for _ in range(a-1):
                schema_of_rand_inj.append(next(it))
            schema_of_rand_inj.append(None)
            b = next(it)
    
    # Finally, randomly label the places in this partial injection
        R = range(n0)
        shuffle(R)
        rand_inj = [0 for _ in range(n0)]
        for i,a in enumerate(schema_of_rand_inj):
            if a is None:
                rand_inj[R[i]] = None
            else:
                rand_inj[R[i]] = R[a]
        if statistics:
            return len(sticks), rand_inj
        else:
            return PartialInjection(rand_inj)
    
    


