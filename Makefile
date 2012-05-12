PYTHON=python3.2

.PHONY: docs clean push

docs:
	$(MAKE) -C docs

clean:
	$(MAKE) -C docs clean
	rm -Rf dist

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg

dist: docs
	$(PYTHON) setup.py sdist
