PYTHON=python3.2

.PHONY: docs test_docs clean push dist test register

docs:
	$(MAKE) -C docs
	zip -j docs.zip docs/*.html docs/format.css LICENSE.txt

register:
	$(PYTHON) setup.py register

test_docs:
	$(MAKE) -C docs test

clean:
	$(MAKE) -C docs clean
	rm -Rf dist MANIFEST docs.zip

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg2

dist: docs
	$(PYTHON) setup.py sdist

test:
	PYTHONPATH=`pwd` $(PYTHON) pypeg2/test/test_pypeg2.py
	PYTHONPATH=`pwd` $(PYTHON) pypeg2/test/test_xmlast.py
	PYTHONPATH=`pwd` $(PYTHON) samples/sample1.py
	PYTHONPATH=`pwd` $(PYTHON) samples/sample2.py
