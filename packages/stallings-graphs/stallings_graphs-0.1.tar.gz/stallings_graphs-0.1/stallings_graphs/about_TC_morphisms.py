# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions. These are the functions which deal with morphisms between ambient free groups.

More precisely, morphisms and automorphisms are handled by Thierry Coulbois's ``train_track`` package. Here we provide mutual translations between objects of class ``Word``, as used in ``stallings_graphs``, and words as used in the ``train_track`` package. Specifically, we stick to words on a numerical alphabet (``alphabet_type='123'``) and to the ``train_track`` format ``type='x0'``.

The translation is as follows: if `i` is a positive integer, the corresponding letter is ``xj`` with `j = i-1`; if `i` is a negative integer, the corresponding letter is ``Xj`` with `j = -i-1`.


We have functions to:

- translate a character, or a word, from one of the formats to the other

EXAMPLES::

    sage: from stallings_graphs.about_TC_morphisms import translate_numeric_Word_to_x0_word
    sage: translate_numeric_Word_to_x0_word([7,1,-2,3,-3])
    ['x6', 'x0', 'X1', 'x2', 'X2']
    
    sage: from stallings_graphs.about_TC_morphisms import translate_x0_word_to_numeric_Word
    sage: translate_x0_word_to_numeric_Word(['x1','X0','x2','X1'])
    word: 2,-1,3,-2


AUTHOR:

- Pascal WEIL, CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr> (2019-04-04): initial version.

"""

# from sage.misc.prandom import randint
from sage.combinat.words.word import Word
#from sage.graphs.digraph import DiGraph
#from sage.sets.disjoint_set import DisjointSet
#from sage.misc.latex import LatexExpr
#
#from partial_injections import PartialInjection

def translate_numeric_to_x0_character(i):
    r"""
    Return the corresponding character in Thierry Coulbois's ``x0`` format.

    ``i`` is expected to be a non-zero integer. An exception is raised if that is not the case.
    
    INPUT:

        - ``i`` -- integer

    OUTPUT: 

        - string

    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import translate_numeric_to_x0_character
        sage: translate_numeric_to_x0_character(7)
        'x6'

        ::

        sage: translate_numeric_to_x0_character(-7)
        'X6'


    """
    if i > 0:
        return "x%s" % (i-1)
    elif i < 0:
        return "X%s" % (-i-1)
    else:
        raise ValueError('the argument is not a proper numerical character')


def translate_x0_character_to_numeric(letter):
    r"""
    Return the corresponding numeric.

    ``letter`` is expected to be a string of the form ``xj`` or ``Xj``, where ``j`` is a non-negative integer
    in decimal expansion.
    
    INPUT:

        - ``letter`` -- string

    OUTPUT: 

        - integer

    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import translate_x0_character_to_numeric
        sage: translate_x0_character_to_numeric('x100')
        101

        ::

        sage: translate_x0_character_to_numeric('X100')
        -101


    """
    i = int(letter[1:])
    if letter[0] == 'x':
        return i + 1
    elif letter[0] == 'X':
        return -i-1
    else:
        raise ValueError('the argument is not a proper letter')


def translate_numeric_Word_to_x0_word(w):
    r"""
    Return the corresponding word in Thierry Coulbois's ``x0`` format.

    ``w`` is expected to be a ``Word`` on a numerical alphabet.
    
    INPUT:

        - ``w`` -- Word

    OUTPUT: 

        - list

    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import translate_numeric_Word_to_x0_word
        sage: translate_numeric_Word_to_x0_word([7,1,-2,3,-3])
        ['x6', 'x0', 'X1', 'x2', 'X2']


    """
    if len(w) == 0:
        return []
    u = [translate_numeric_to_x0_character(x) for x in w]
    return u


def translate_x0_word_to_numeric_Word(u):
    r"""
    Return the corresponding numeric Word.

    ``u`` is expected to be a list of strings of the form ``xj`` or ``Xj``, where ``j`` is a non-negative integer in decimal expansion.
    
    INPUT:

        - ``u`` -- list

    OUTPUT: 

        - ``Word``

    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import translate_x0_word_to_numeric_Word
        sage: translate_x0_word_to_numeric_Word(['x1','X0','x2','X1'])
        word: 2,-1,3,-2

        ::

        sage: translate_x0_word_to_numeric_Word([])
        word:


    """
    if len(u) == 0:
        return Word([])
    v = [translate_x0_character_to_numeric(y) for y in u]
    return Word(v)


