# This Makefile is for convenience as a reminder and shortcut for the most used commands

# Package folder
PACKAGE = stallings_graphs

# change to your sage command if needed
# SAGE = sage
SAGE = /Applications/SageMath-8.6.app/sage

all: install test

install:
	$(SAGE) -pip install --upgrade --no-index -v .

install-with-internet:
	$(SAGE) -pip install --upgrade -v .

installdependencies:
	$(SAGE) -i dot2tex
	$(SAGE) -i openssl
	$(SAGE) -f python2
	$(SAGE) -i pyopenssl

uninstall:
	$(SAGE) -pip uninstall .

develop:
	$(SAGE) -pip install --upgrade -e .

test:
	$(SAGE) setup.py test

coverage:
	$(SAGE) -coverage $(PACKAGE)/*

doc:
	cd docs && $(SAGE) -sh -c "make html"

doc-pdf:
	cd docs && $(SAGE) -sh -c "make latexpdf"

clean: clean-doc

clean-doc:
	cd docs && $(SAGE) -sh -c "make clean"
    
dist:
	$(SAGE) -python setup.py sdist

upload: dist
	VERSION=`cat VERSION`; $(SAGE) -sh -c "twine upload dist/$(PACKAGE)-$$VERSION.tar.gz"


.PHONY: all install develop test coverage clean clean-doc doc doc-pdf
