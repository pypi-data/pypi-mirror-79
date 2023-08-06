# -*- coding: utf-8 -*-
r"""
The methods for the class ``FinitelyGeneratedSubgroup`` use a number of ancillary functions. These are the functions which deal with words (actually, objects of class ``Word``) in the context of group theory.

A word is a string of characters from either a numerical or an alphabetical set
of letters: ``alphabet_type='123'`` or ``'abc'``

``alphabet_type='123'``: The positive letters form an interval `[1,r]`. Their inverses (aka
negative letters) are the corresponding negative integers. The symmetrized
alphabet is the union of positive and negative letters (zero is NOT a letter).
The `\textit{rank}` of a word is the maximal absolute value of a letter occurring in the word.
When represented in a (say LaTeX) file (``.tex``, ``.pdf``), the letters are written
`a_i`.

``alphabet_type='abc'``: positive letters are lower case (at most 26 letters, `a`:`z`)
and their inverses are the corresponding upper case letters (`A`:`Z`).

We have functions to:

- translate a word or a list of words from one ``alphabet_type`` to the other

- test whether a word of ``alphabet_type '123'`` is (freely) reduced or cyclically reduced

- freely reduce a word of ``alphabet_type '123'``

- computes the cyclic reduction of a word of ``alphabet_type '123'``

- produce a random word of ``alphabet_type '123'`` of given length on an alphabet of given rank (given a positive integer `r`).

EXAMPLES::

    sage: from stallings_graphs.about_words import group_inverse
    sage: w = Word('aBabbaBA')
    sage: group_inverse(w,alphabet_type='abc')
    word: abABBAbA
    
    sage: from stallings_graphs.about_words import free_group_reduction
    sage: w = Word([3,1,-2,-2,2,1,-1,2,5,-3])
    sage: free_group_reduction(w)
    word: 3,1,5,-3

    sage: from stallings_graphs.about_words import random_reduced_word
    sage: w = random_reduced_word(7,3)   #random
    Word([2,-1,3,-1,-1,2,-3])


AUTHOR:

- Pascal WEIL, CNRS, Univ. Bordeaux, LaBRI <pascal.weil@cnrs.fr> (2018-06-09): initial version.

"""

from sage.misc.prandom import randint
from sage.combinat.words.word import Word
#from sage.graphs.digraph import DiGraph
#from sage.sets.disjoint_set import DisjointSet
#from sage.misc.latex import LatexExpr
#
#from partial_injections import PartialInjection



def positive_letters(r):
    r"""
    Return the set of positive (numerical) letters up to `r`.
    
    `r` is expected to be positive.
    
    INPUT:

        - ``r`` -- integer

    OUTPUT:

        - the list ``range(r)``
        
    EXAMPLES::

        sage: from stallings_graphs.about_words import positive_letters
        sage: positive_letters(6)
        [1, 2, 3, 4, 5, 6]

    """
    return range(1,r + 1)

def negative_letters(r):
    r"""
    Return the set of negative (numerical) letters up to `-r`.
    
    `r` is expected to be positive.
    
    INPUT:

        - ``r`` -- integer

    OUTPUT:

        - the list of integers from `-1` to `-r`
        
    EXAMPLES::

        sage: from stallings_graphs.about_words import negative_letters
        sage: negative_letters(6)
        [-1, -2, -3, -4, -5, -6]

    """
    return range(-1,-r-1,-1)

def symmetric_alphabet(r):
    r"""
    Return the full symmetric (numerical) alphabet.
    
    `r` is expected to be positive.
    
    INPUT:

        - ``r`` -- integer

    OUTPUT:

        - the list of integers from `1` to `r` and from `-1` to `-r`
        
    EXAMPLES::

        sage: from stallings_graphs.about_words import symmetric_alphabet
        sage: symmetric_alphabet(6)
        [1, 2, 3, 4, 5, 6, -1, -2, -3, -4, -5, -6]
    
    """
    L = positive_letters(r)
    L.extend(negative_letters(r))
    return L

def inverse_letter(i):
    r"""
    Return the inverse of this (numerical) letter.
    
    `i` is expected to be a non-zero integer.
    
    INPUT:

        - ``i`` -- integer

    OUTPUT:

        - integer
        
    EXAMPLES::

        sage: from stallings_graphs.about_words import inverse_letter
        sage: inverse_letter(3)
        -3
        sage: inverse_letter(-4)
        4
        
    """
    return -i

def positive_value(i):
    r"""
    Return the positive value of a (numerical) letter.
    
    `i` is expected to be a non-zero integer.
    
    INPUT:

        - ``i`` -- integer

    OUTPUT:

        - integer
        
    EXAMPLES::

        sage: from stallings_graphs.about_words import positive_value
        sage: positive_value(3)
        3
        sage: positive_value(-4)
        4

    """
    if i < 0:
        return inverse_letter(i)
    else:
        return i

def translate_character_to_numeric(x):
    r"""
    Return the numeric equivalent of a character in `a`:`z` or `A`:`Z`.
    
    `x` is expected to be a character in `a`:`z` or `A`:`Z`. The numeric equivalent is
    1-26 for `a`:`z` and the opposite for `A`:`Z`.
    
    INPUT:

        - ``x`` -- character

    OUTPUT:

        - integer
            
    EXAMPLES::

        sage: from stallings_graphs.about_words import translate_character_to_numeric
        sage: translate_character_to_numeric('b')
        2
        sage: translate_character_to_numeric('D')
        -4

    """
    if ord(x) in range(65,91):
        return -(ord(x) - 64)
    elif ord(x) in range(97,123):
        return ord(x) - 96
    else:
        raise ValueError('the argument must be a letter in a:z or A:Z')

def translate_numeric_to_character(x):
    r"""
    Return the character equivalent of a numerical letter.
    
    `x` is expected to be a non-zero integer in the interval `[-26;26]`. A
    ValueError is raised otherwise. The numeric equivalent is a lower case character
    if `x > 0` and an upper case character otherwise.
    
    INPUT:

        - ``x`` -- integer

    OUTPUT:

        - character
            
    EXAMPLES::

        sage: from stallings_graphs.about_words import translate_numeric_to_character
        sage: translate_numeric_to_character(16)
        'p'
        sage: translate_numeric_to_character(-10)
        'J'
    
    """
    if x in range(-26,0):
        return chr(- x + 64)
    elif x in range(1,27):
        return chr(x + 96)
    else:
        raise ValueError('the argument must be a non-zero integer between -26 and 26')

def alphabetic_inverse(x):
    r"""
    Return the inverse of an alphabetic letter.
    
    `x` is expected to be a character in `a`:`z` or `A`:`Z`. Taking the inverse toggles between
    upper and lower case letters.
    
    INPUT:

        - ``x`` -- character

    OUTPUT:

        - character
                
    EXAMPLES::

        sage: from stallings_graphs.about_words import alphabetic_inverse
        sage: alphabetic_inverse('b')
        'B'
        sage: alphabetic_inverse('D')
        'd'
        
    """
    return translate_numeric_to_character(-translate_character_to_numeric(x))

### Words and lists of Words ###

def translate_alphabetic_Word_to_numeric(w):
    r"""
    Return the numerical equivalent of a ``Word`` of ``alphabet_type = 'abc'``.
    
    `w` is expected to be a ``Word`` on alphabet `a`:`z` `+` `A`:`Z`. The output is a ``Word``
    on alphabet `\{\pm 1, ..., \pm 26\}`.
    
    INPUT:

        - ``w`` -- Word

    OUTPUT:

        - Word
                    
    EXAMPLES::

        sage: from stallings_graphs.about_words import translate_alphabetic_Word_to_numeric
        sage: translate_alphabetic_Word_to_numeric(Word('aBBaAc'))
        word: 1,-2,-2,1,-1,3
        
    """
    if len(w) == 0:
        return Word([])
    u = [translate_character_to_numeric(x) for x in w]
    return Word(u)

def translate_numeric_Word_to_alphabetic(w):
    r"""
    Return the alphabetic equivalent of a numeric word.
    
    `w` is expected to be a ``Word`` on a numerical alphabet `\{\pm 1, \dots, \pm 26\}`. The output
    is a ``Word`` on alphabet  `a`:`z` `+` `A`:`Z`.
    
    INPUT:

        - ``w`` -- Word

    OUTPUT:

        - Word
    
    EXAMPLES::

        sage: from stallings_graphs.about_words import translate_numeric_Word_to_alphabetic
        sage: translate_numeric_Word_to_alphabetic(Word([2,-1,-2,3,1,3]))
        word: bABcac
        
    """
    if len(w) == 0:
        return Word([])
    u = [translate_numeric_to_character(x) for x in w]
    return Word(u)


def is_valid_Word(w, alphabet_type='123'):
    r"""
    Return whether a ``Word`` is valid, in the sense of having a consistent alphabet.
    
    `w` is expected to be a ``Word``. It is `\textit{valid}` if all its letters are non-zero integers
    if ``alphabet_type='123'``; or are in `a`:`z` `+` `A`:`Z` if ``alphabet_type='abc'``.
    
    INPUT:

        - ``w`` -- ``Word``
        - ``alphabet_type`` -- string, which must be either ``'abc'`` or ``'123'``

    OUTPUT:

        - boolean
    
    EXAMPLES::

        sage: from stallings_graphs.about_words import is_valid_Word
        sage: w = Word([2,-1,-2,3,1,3])
        sage: is_valid_Word(w)
        True
        
        ::
        
        sage: is_valid_Word(Word('bABcac'), alphabet_type='abc')
        True
        
        ::
        
        sage: is_valid_Word(Word([2,-1,-2,0,1,3]))
        False
        
    """
    from sage.rings.integer_ring import ZZ
    if (alphabet_type != '123') and (alphabet_type != 'abc'):
        raise ValueError('the second argument is neither "123" nor "abc".')
    if len(w) == 0:
        return True
    if alphabet_type == '123':
        return all((x in ZZ and x != 0) for x in w)
    L = range(65,91) + range(97,123)
    return all(isinstance(x,str) for x in w) and all(ord(x) in L for x in w)

def is_valid_list_of_Words(L,alphabet_type='123'):
    r"""
    Return whether a list of ``Word``s is valid, in the sense of ``is_valid_Word``.
    
    `L` is expected to be a list of objects of class ``Word``. It is valid if all its components satisfy
    ``is_valid_Word``.
    
    INPUT:

        - ``L`` -- ``List``

        - ``alphabet_type`` -- string, which must be either ``'abc'`` or ``'123'``

    OUTPUT:

        - boolean
        
    EXAMPLES::

        sage: from stallings_graphs.about_words import is_valid_list_of_Words
        sage: L = [Word([2,-1,-2,3,1,3]), Word([1,2,-3,1,-1])]
        sage: is_valid_list_of_Words(L)
        True
        sage: L = [Word('bABcac'),'abcBA','baaCB']
        sage: is_valid_list_of_Words(L, alphabet_type='abc')
        True
        
    """
    if (alphabet_type != '123') and (alphabet_type != 'abc'):
        raise ValueError('the second argument is neither "123" nor "abc".')
    return all(is_valid_Word(w, alphabet_type) for w in L)
        

def rank(w,check=False):
    r"""
    Return the least rank of a free group containing this ``Word``.
    
    `w` is expected to be a ``Word`` on a numerical alphabet. The least rank of a free group
    containing `w` is the max of the positive values of its letters. If ``check`` is ``True``,
    ``is_valid_Word(w,alphabet_type='123')`` is run.
    
    INPUT:

        - ``w`` -- ``Word``
        - ``alphabet_type`` -- string, which must be either ``'abc'`` or ``'123'``

    OUTPUT:

        - integer
                
    EXAMPLES ::
        sage: from stallings_graphs.about_words import rank
        sage: w = Word([3,1,-2,-2,5,-3])
        sage: rank(w)
        5
        
    """
    if check == True:
        if not(is_valid_Word(w,alphabet_type='123')):
            raise ValueError('the argument is not a valid (numerical) Word: probably contains 0, which is not a letter, or is of type "abc".')
    if len(w) == 0:
        return 0
    else:
        return max([positive_value(x) for x in w])

##############################################
## group properties: inverting, reducing, etc.
##############################################

def group_inverse(w,alphabet_type='123',check=False):
    r"""
    Return the (free group) inverse of a word.
    
    `w` is expected to be a ``Word`` on a numerical or letter alphabet, depending on the value
    of ``alphabet_type``. Its inverse is obtained in reading `w` in reverse order and replacing
    each letter by its inverse. If ``check`` is set to ``True``, ``is_valid_Word`` is run on `w`.
    
    INPUT:

        - ``w`` -- ``Word``
        - ``alphabet_type`` -- string, which must be either ``'abc'`` or ``'123'``

    OUTPUT:

        - Word
            
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import group_inverse
        sage: w = Word([3,1,-9,-2,5])
        sage: group_inverse(w)
        word: -5,2,9,-1,-3
        
        ::
        
        sage: w = Word([-1,1,2,-2])
        sage: group_inverse(w)
        word: 2,-2,-1,1
        
        ::
        
        sage: w = Word([1])
        sage: group_inverse(w)
        word: -1
        
        ::
        
        sage: w = Word()
        sage: group_inverse(w)
        word: 
        
    """
    if check == True:
        if not(is_valid_Word(w,alphabet_type)):
            raise ValueError('the first argument is not a valid Word of the given alphabet_type')
    if alphabet_type == 'abc':
        w1 = translate_alphabetic_Word_to_numeric(w)
    else:
        w1 = w
    v = [inverse_letter(x) for x in w1]
    v.reverse()
    v1 = Word(v)
    if alphabet_type == 'abc':
        v1 = translate_numeric_Word_to_alphabetic(v1)
    return v1


def is_reduced(w,check=False):
    r"""
    Return whether this word is a reduced.
    
    `w` is expected to be a ``Word`` on a numerical alphabet. A word `w` is reduced (in the
    group-theoretic sense) if it does not contain consecutive letters which are
    mutually inverse. The option ``check`` verifies whether `w` is a valid Word.
    
    INPUT:

        - ``w`` -- ``Word``
        - ``check`` -- boolean

    OUTPUT:

        - boolean
                
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import is_reduced
        sage: w = Word([3,1,-2,-2,5,-3])
        sage: is_reduced(w)
        True
        
        ::
        
        sage: u = Word([3,1,-2,2,5,-3])
        sage: is_reduced(u)
        False
        
    """
    if check == True:
        if not(is_valid_Word(w,alphabet_type='123')):
            raise ValueError('the argument is not a valid (numerical) Word: probably contains 0, which is not a letter')
    if len(w) < 2:
        return True
    else:
        return all(inverse_letter(w[i]) != w[i+1] for i in range(len(w) - 1))


def free_group_reduction(w,check=False):
    r"""
    Return the reduced word that is equivalent to this word.
    
    `w` is expected to be a ``Word`` on a numerical alphabet. The option ``check = True``
    verifies that this is the case. The reduced word equivalent to a word `w` is obtained
    from `w` by repeatedly deleting pairs of consecutive letters which are mutually
    inverse.
    
    INPUT:

        - ``w`` -- ``Word``
        - ``check`` -- boolean

    OUTPUT:

        - ``Word``
                
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import free_group_reduction
        sage: w = Word([3,1,-2,-2,2,1,-1,2,5,-3])
        sage: free_group_reduction(w)
        word: 3,1,5,-3
    
    ALGORITHM:
    
    This method implements the classical algorithm, based on the usage of a pushdown
    automaton.
            
    """
    if check == True:
        if not(is_valid_Word(w,alphabet_type='123')):
            raise ValueError('the argument is not a valid (numerical) Word: probably contains 0, which is not a letter')
    if len(w) < 2:
        return w
    else:
        stack = []
        for i in range(len(w)):
            if stack == []:
                stack.append(w[i])
            elif stack[-1] != inverse_letter(w[i]):
                stack.append(w[i])
            else:
                stack = stack[:-1]
        return Word(stack)

                
def is_cyclically_reduced(w,check=False):
    r"""
    Return whether this word is cyclically reduced.
    
    `w` is expected to be a ``Word`` on a numerical alphabet. The option ``check`` verifies
    that it is the case. A word is cyclically reduced if it is reduced and its first and
    last letters are not mutually inverse.
    
    INPUT:

        - ``w`` -- ``Word``
        - ``check`` -- boolean

    OUTPUT:

        - boolean
                
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import is_cyclically_reduced
        sage: w = Word([3,1,-2,-2,5,-3])
        sage: is_cyclically_reduced(w)
        False
        
        ::
        
        sage: u = Word([3,1,-2,-2,5,3])
        sage: is_cyclically_reduced(u)
        True
        
    """
    if check == True:
        if not(is_valid_Word(w,alphabet_type='123')):
            raise ValueError('the argument is not a valid (numerical) Word. Common mistake: it contains 0, which is not a letter')
    if len(w) < 2:
        return True
    else:
        return is_reduced(w) and inverse_letter(w[0]) != w[-1]


def cyclic_reduction_of_a_word(u):
    r"""
    Return the elements of the cyclically reduced decomposition of this word.
    
    `u` is expected to be a ``Word`` on a numerical alphabet. The cyclically reduced
    decomposition of `u` is the pair of Words `(v,w)` such that `v` is cyclically reduced,
    and `u = w^{-1}vw`.

    INPUT:

        - ``w`` -- ``Word``
        - ``check`` -- boolean

    OUTPUT:

        - pair of objects of class ``Word``
                
    EXAMPLES ::

        sage: from stallings_graphs.about_words import cyclic_reduction_of_a_word
        sage: u = Word([1,-2,-2,-1,1])
        sage: cyclic_reduction_of_a_word(u)
        (word: 1,-2,-2, word: )

    ::

        sage: u = Word([1,-2,1,-2,1,2,-1])
        sage: cyclic_reduction_of_a_word(u)
        (word: 1,-2,1, word: 2,-1)

    ::

        sage: u = Word([1,-2,1,-1,1])
        sage: cyclic_reduction_of_a_word(u)
        (word: 1,-2,1, word: )

    ::

        sage: u = Word([1,2,-2,-1,2,2,1,-1,-2])
        sage: cyclic_reduction_of_a_word(u)
        (word: 2, word: )

    ::

        sage: u = Word()
        sage: cyclic_reduction_of_a_word(u)
        (word: , word: )

    """
    v = free_group_reduction(u)
    if len(v) <= 1:
        return (v,Word())
    w = Word()
    while v[0] == inverse_letter(v[-1]):
        w = Word([v[-1]]) + w
        v = v[1:-1]
    return (v,w)

#################
## random objects 
#################

def random_letter(r):
    r"""
    Return a random letter in the symmetric alphabet of this size.
    
    `r` is expected to be a positive integer. The symmetric alphabet of size `r`
    is the set of non-zero integers between `-r` and `r`. The probability distribution is
    uniform.
    
    INPUT:

        - ``r`` -- integer

    OUTPUT:

        - integer
                
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import random_letter
        sage: random_letter(4)   # random
        2
        
    """
    a = randint(0,2 * r - 1)
    return symmetric_alphabet(r)[a]

def random_word(n,r):
    r"""
    Return a random word of length `n` in the symmetric alphabet of size `r`.
    
    `n` is expected to be a non-negative integer and `r` is expected to be a positive
    integer. The word produced on the symmetric alphabet of size `r` is not necessarily
    reduced. The probability distribution is uniform.
    
    INPUT:

        - ``n`` -- integer
        - ``r`` -- integer

    OUTPUT:

        - ``Word``
                
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import random_word
        sage: random_word(4,5)   # random
        Word([2,-1,3,-4,-1])
        
    """
    if n == 0:
        return []
    else:
        return Word([random_letter(r) for _ in range(n)])

def random_reduced_word(n,r):
    r"""
    Return a random reduced word of length `n` in the symmetric alphabet of size `r`.
    
    `n` is expected to be a non-negative integer and `r` is expected to be a positive
    integer. A word is reduced if it does not contain consecutive letters which are mutually
    inverse. The probability distribution is uniform.
    
    INPUT:

        - ``n`` -- integer
        - ``r`` -- integer

    OUTPUT:

        - ``Word``
                
    EXAMPLES ::
    
        sage: from stallings_graphs.about_words import random_reduced_word
        sage: random_reduced_word(4,5)   # random
        Word([2,-1,3,-4,-1])
    

    """
    if n == 0:
        return []
    else:
        v = [random_letter(r)]
        for i in range(1,n):
            k = symmetric_alphabet(r).index(inverse_letter(v[-1]))
            x = randint(0,2 * r - 2)
            if x < k:
                v.append(symmetric_alphabet(r)[x])
            else:
                v.append(symmetric_alphabet(r)[x + 1])
    return Word(v)





