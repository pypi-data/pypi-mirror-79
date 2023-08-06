# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions. These are the functions which deal with morphisms between free groups.

More precisely, morphisms and automorphisms are handled by Thierry Coulbois's ``train_track`` package. Here we provide mutual translations between objects of class ``Word``, as used in ``stallings_graphs``, and words as used in the ``train_track`` package. Specifically, we stick to words on a numerical alphabet (``alphabet_type='123'``) and to the ``train_track`` format ``type='x0'``.

The translation is as follows: if `i` is a positive integer, the corresponding letter is ``xj`` with `j = i-1`; if `i` is a negative integer, the corresponding letter is ``Xj`` with `j = -i-1`.


We have functions to:

- translate a character, or a word, from one of the formats to the other

- define a ``FGendomorphism``(this is a ``FreeGroupMorphism`` from ``train_track``), by giving the list of images of the ambient free group basis

- compute the image of a word (alphabetic or numeric) by a ``FGendomorphism``

We inherit the methods from ``train_track``, to compose morphisms, to check whether they are invertible and, if so, to compute their inverse.

EXAMPLES::

    sage: from stallings_graphs.about_TC_morphisms import FGendomorphism
    sage: L = ['ab','a']
    sage: phi = FGendomorphism(L,alphabet_type='abc')
    sage: phi
    Morphism from Free Group on generators {x0, x1} to Free Group on generators {x0, x1}: x0->x0*x1,x1->x0
    
::
    
    sage: from stallings_graphs.about_TC_morphisms import image_of_Word_by_endomorphism
    sage: w = 'abAbA'
    sage: image_of_Word_by_endomorphism(phi, w, alphabet_type='abc')
    word: abaBBA


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


def translate_numeric_Word_to_x0_list(w):
    r"""
    Return the corresponding word in Thierry Coulbois's ``x0`` format.

    ``w`` is expected to be a ``Word`` on a numerical alphabet.
    
    INPUT:

    - ``w`` -- Word

    OUTPUT: 

    - list

    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import translate_numeric_Word_to_x0_list
        sage: translate_numeric_Word_to_x0_list([7,1,-2,3,-3])
        ['x6', 'x0', 'X1', 'x2', 'X2']


    """
    if len(w) == 0:
        return []
    u = [translate_numeric_to_x0_character(x) for x in w]
    return u


def translate_x0_word_to_numeric_Word(u):
    r"""
    Return the corresponding numeric Word.

    ``u`` is expected to be a ``FreeGroup`` element in the sense of the ``train_track`` package, written with
    letters of the form ``xj`` or ``Xj``, where ``j`` is a non-negative integer in decimal expansion.
    
    INPUT:

    - ``u`` -- element of type ``train_track.free_group.FreeGroup_class_with_category.element_class`` (the free group elements in the ``train_track`` package)

    OUTPUT: 

    - ``Word``

    EXAMPLES::
    
        sage: from train_track import FreeGroupMorphism
        sage: D = {'x0':['x0','x1'],'x1':['X0']}
        sage: phi = FreeGroupMorphism(D)
        sage: print(phi)
        x0->x0*x1,x1->x0^-1
        sage: w = phi(['X0','x1','x0'])
        sage: from stallings_graphs.about_TC_morphisms import translate_x0_word_to_numeric_Word
        sage: translate_x0_word_to_numeric_Word(w)
        word: -2,-1,2

    ::

        sage: w = phi([])
        sage: translate_x0_word_to_numeric_Word(w)
        word:

    """
    if len(u) == 0:
        return Word([])
    v = u.to_word()
    w = []
    for i in range(len(v)):
        a,b = (v[i][0],int(v[i][1:]))
        if a == 'x':
            w = w + [b+1]
        elif a == 'X':
            w = w + [-b-1]
        else:
            raise ValueError('Something went wrong: the letters of this x0-word should be strings starting with "x" or "X".')
    return Word(w)

def FGendomorphism(L, alphabet_type='abc'):
    r"""
    Return a ``FreeGroupMorphism`` in the sense of the ``train_track`` package, defined
    by the given list.
    
    ``L`` is expected to be a list of objects of class Word, on a numerical or letter alphabet
    according to the value of ``alphabet_type``.
    
    INPUT:
    
    - ``L`` -- list of objects of class Word    
    - ``alphabet_type`` -- string, which is either ``'123'`` or ``'abc'``
        
    OUTPUT:
    
    - ``FreeGroupMorphism``
        
    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import FGendomorphism
        sage: L = ['ab','a']
        sage: phi = FGendomorphism(L,alphabet_type='abc')
        sage: phi
        Morphism from Free Group on generators {x0, x1} to Free Group on generators {x0, x1}: x0->x0*x1,x1->x0
    
    """
    from train_track import FreeGroupMorphism
    from stallings_graphs.about_words import translate_alphabetic_Word_to_numeric
    if alphabet_type == 'abc':
        numerical_list = [translate_alphabetic_Word_to_numeric(w) for w in L]
    elif alphabet_type == '123':
        numerical_list = L
    else:
        raise ValueError('the "alphabet_type" argument is neither "123" nor "abc".')
    #
    translated_list = [translate_numeric_Word_to_x0_list(w) for w in numerical_list]
    prepare_phi = {}
    for i in range(len(L)):
        prepare_phi['x%s' % i] = translated_list[i]
    #
    return FreeGroupMorphism(prepare_phi)

def image_of_Word_by_endomorphism(phi, w, alphabet_type='abc'):
    r"""
    Return the image of the second argument by the first.

    INPUT:
    
    - ``phi`` -- ``FreeGroupMorphism``    
    - ``w`` -- a ``Word`` on a numeric or letter alphabet, depending on the value of ``alphabet_type``
    - ``alphabet_type`` -- string, which is either ``'123'`` or ``'abc'``
        
    OUTPUT:
    
    - ``Word``
        
    EXAMPLES::
    
        sage: from stallings_graphs.about_TC_morphisms import image_of_Word_by_endomorphism 
        sage: from stallings_graphs.about_TC_morphisms import FGendomorphism
        sage: L = ['ab','a']
        sage: phi = FGendomorphism(L,alphabet_type='abc')
        sage: w = 'abAbA'
        sage: image_of_Word_by_endomorphism(phi, w, alphabet_type='abc')
        word: abaBBA
    
    """
    
    from stallings_graphs.about_words import translate_alphabetic_Word_to_numeric, translate_numeric_Word_to_alphabetic
    if alphabet_type == 'abc':
        numerical_word = translate_alphabetic_Word_to_numeric(w)
    elif alphabet_type == '123':
        numerical_word = w
    else:
        raise ValueError('the "alphabet_type" argument must be either "123" or "abc" (and is not).')
    #
    translated_word = translate_numeric_Word_to_x0_list(numerical_word)
    image_to_be_translated = phi(translated_word)
    image = translate_x0_word_to_numeric_Word(image_to_be_translated)
    if alphabet_type == 'abc':
        image = translate_numeric_Word_to_alphabetic(image)
    return image