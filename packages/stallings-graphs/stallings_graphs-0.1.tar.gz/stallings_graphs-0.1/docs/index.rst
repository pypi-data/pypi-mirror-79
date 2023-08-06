==============================
Stallings Graphs Research Code
==============================

This is the reference manual for `Pascal Weil <http://www.labri.fr/perso/weil/>`_'s  ``stallings_graphs`` Research Code extension to the `Sage <http://sagemath.org/>`_ mathematical software system.  Sage is free open source math software that supports research and teaching in algebra, geometry, number theory, cryptography, and related areas.  


``stallings_graphs`` Research Code implements tools to experiment with finitely generated subgroups of infinite groups in Sage, via a set of new Python classes. Many of the modules correspond to research code written for published articles (random generation, decision for various properties, etc). It is meant to be reused and reusable (full documentation including doctests).
Comments are welcome.

[BNW02008]_

To install this module, you do::

    sage -pip install http://www.labri.fr/perso/weil/software/stallings_graphs-0.1.tar.gz

and eventually::

    sage -pip install stallings_graphs
    
.. Install latest development version::
    replace the url by the mathrice url for the git repository once it is public

    sage -pip install http://www.labri.fr/perso/weil/stallings_graphs-0.1.tar.gz

To use this module, you need to import it:: 

    from stallings_graphs import *

This reference manual contains many examples that illustrate the usage of
``stallings_graphs``. The examples are all tested with each release of ``stallings_graphs``, and
should produce exactly the same output as in this manual, except for line
breaks.

This work is licensed under a `Creative Commons Attribution-Share Alike
3.0 License`__.

__ https://creativecommons.org/licenses/by-sa/3.0/


Finitely generated subgroups of free groups
===========================================

.. toctree::
   :maxdepth: 2
   
   finitely_generated_subgroup
   about_words
   about_automata
   about_folding
   about_TC_morphisms


Partial injections
==================

.. toctree::
   :maxdepth: 2
   
   partial_injections
   partial_injections_misc




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
