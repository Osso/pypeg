PYTHON=python3.2

.PHONY: docs test_docs clean push dist test register deploy

docs:
	$(MAKE) -C docs
	zip -j docs.zip docs/*.html docs/format.css LICENSE.txt

deploy: dist
	rm -f pyPEG2.tar.gz
	ln -s `ls dist/pyPEG2-*.tar.gz | tail -n1` pyPEG2.tar.gz
	scp docs/*.html docs/format.css pyPEG2.tar.gz *.txt samples/* dragon:fdik.org/pyPEG2/
	make register

register:
	$(PYTHON) setup.py check
	$(PYTHON) setup.py register

test_docs:
	$(MAKE) -C docs test

clean:
	$(MAKE) -C docs clean
	rm -Rf dist MANIFEST docs.zip pyPEG2.tar.gz

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg

dist: docs
	$(PYTHON) setup.py sdist

test:
	PYTHONPATH=`pwd` $(PYTHON) pypeg2/test/test_pypeg2.py
	PYTHONPATH=`pwd` $(PYTHON) pypeg2/test/test_xmlast.py
	PYTHONPATH=`pwd` $(PYTHON) samples/sample1.py
	PYTHONPATH=`pwd` $(PYTHON) samples/sample2.py

install: dist
	$(PYTHON) setup.py install --user
