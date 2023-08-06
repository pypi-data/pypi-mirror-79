# This Makefile is for convenience as a reminder and shortcut for the most used commands

# Package folder
PACKAGE = stallings_graphs

# change to your sage command if needed
SAGEROOT = /Applications/SageMath-9.0.app
SAGE = $(SAGEROOT)/sage

all: install test

install:
	$(SAGE) -pip install --upgrade --no-index -v .

install-with-internet:
	$(SAGE) -pip install --upgrade -v .

installdependencies-old:
	$(SAGE) -i dot2tex
	$(SAGE) -i openssl
	$(SAGE) -f python2
	$(SAGE) -i pyopenssl

# additional XCode command line tool for MacOSX
install-command-line-tools:
	xcode-select --install   

installdependencies:
	$(SAGE) -i openssl
	$(SAGE) -f python3
	cd $(SAGE_ROOT) && make ssl
	$(SAGE) -i dot2tex
    
uninstall:
	$(SAGE) -pip uninstall .

develop:
	$(SAGE) -pip install --upgrade -e .

test:
	$(SAGE) setup.py test

coverage:
	$(SAGE) -coverage $(PACKAGE)/*

doc:install
	cd docs && $(SAGE) -sh -c "make html"

doc-pdf:install
	cd docs && $(SAGE) -sh -c "make latexpdf"

clean: clean-doc

clean-doc:
	cd docs && $(SAGE) -sh -c "make clean"
    
dist:
	$(SAGE) -python setup.py sdist

check: dist
	VERSION=`cat VERSION`; $(SAGE) -sh -c "twine check dist/$(PACKAGE)-$$VERSION.tar.gz"

upload: dist
	VERSION=`cat VERSION`; $(SAGE) -sh -c "twine upload dist/$(PACKAGE)-$$VERSION.tar.gz"


.PHONY: all install develop test coverage clean clean-doc doc doc-pdf dist upload
