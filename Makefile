PYTHON=python3.2

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg

test:
	$(PYTHON) test_pyPEG2.py
	@echo testing sample1.py...
	$(PYTHON) sample1.py
	@echo testing sample2.py...
	$(PYTHON) sample2.py
	$(PYTHON) test_xmlast2.py

