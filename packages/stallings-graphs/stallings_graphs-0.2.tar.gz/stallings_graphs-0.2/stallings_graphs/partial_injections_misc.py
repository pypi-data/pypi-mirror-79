# -*- coding: utf-8 -*-
r"""
The methods for the class ``PartialInjection`` use a number of ancillary functions.

We have the functions

- ``is_valid_partial_injection``, to check whether a list represents a valid partial injection

- ``number_of_partial_injections_list``, to compute the number of partial injections of a given size.


AUTHOR:

- Pascal WEIL, CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr> (2018-06-09): initial version

"""

from sage.rings.integer_ring import ZZ
from sage.misc.cachefunc import cached_function

def is_valid_partial_injection(L):
    r"""
    Return whether a list represents a ``PartialInjection``.
    
    ``L`` is expected to be a list. It properly defines a ``PartialInjection`` if its entries are
    either ``None`` or in `[0..n-1]`, where `n` is the length of ``L``, and if none of the integer entries is repeated.
    
    INPUT:

        - ``L`` -- List

    OUTPUT:

        - boolean
        
    EXAMPLES::

        sage: from stallings_graphs.partial_injections_misc import is_valid_partial_injection
        sage: L = [3,1,4,None,2]
        sage: is_valid_partial_injection(L)
        True
        
    ::
        
        sage: L = [3,1,5,None,None,1]
        sage: is_valid_partial_injection(L)
        False 
        
    .. WARNING::
    
        This test is performed when a ``PartialInjection`` is defined. As a stand-alone function,
        this is intended to be used when one does not want to attempt to define a
        ``PartialInjection`` if the list is not valid.
    
    """
    q = L[:]
    n = len(q)
    b1 = all((0 <= i) and (i < n) for i in q if not (i==None))
    for i in range(n):
        if q[i] == None:
            q[i] = -1
#
    q.sort()
    b2 = all((q[i] == -1) or not (q[i] == q[i+1]) for i in range(n-1))
    return b1 and b2
        
@cached_function
def number_of_partial_injections_list(n):
    r"""
    Return the list of the numbers of partial injections on `0, 1, 2,..., n-1`.
    
    The input integer is expected to be positive. A ``ValueError`` is raised otherwise.
    
    INPUT:

        - ``n`` -- integer

    OUTPUT:

        - a List of length `n`
        
    EXAMPLES::
    
        sage: from stallings_graphs.partial_injections_misc import number_of_partial_injections_list
        sage: number_of_partial_injections_list(7)
        [1, 2, 7, 34, 209, 1546, 13327]
    
    ALGORITHM:
    
        The algorithm implements a recurrence relation described in [BNW2008]_.
        
    """
    
    if n == 0:
        raise ValueError("the argument must be greater than 0")
    elif n == 1:
        P = [ZZ(1)]
    elif n == 2:
        P = [ZZ(1),ZZ(2)]
    else:
        P = [ZZ(1),ZZ(2)]
        for t in range(2, n):
            P.append(2 * t * P[-1] - (t - 1)**2 * P[-2])
    return P




