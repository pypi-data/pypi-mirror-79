## -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests


# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib stallings_graphs")
        if errno != 0:
            sys.exit(1)

setup(
    name = "stallings_graphs",
    version = readfile("VERSION"), # the VERSION file is shared with the documentation
    description='Stallings graph representation of finitely generated subgroups of free groups',
    long_description = readfile("README.rst"), # get the long description from the README
    long_description_content_type='text/x-rst',
    url='https://plmlab.math.cnrs.fr/pascalweil/stallings_graphs',
    author='Pascal Weil',
    author_email='pascal.weil@cnrs.fr', # choose a main contact email
    license='GPLv2+', # This should be consistent with the LICENCE file
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'Topic :: Software Development :: Build Tools',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
      'Programming Language :: Python :: 2.7',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "SageMath Stallings Graphs Finitely Generated Subgroups Free Groups",
    packages = ['stallings_graphs'],
    install_requires = ['slabbe','train_track'],
    cmdclass = {'test': SageTest} # adding a special setup command for tests
)

