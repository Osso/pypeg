# put the path to your local Python 3 interpreter here

PYTHON=python3.2

# put the path to your local YML 2 compiler here

YMLC=yml2c


documentation: index.html

%.html: %.en.yhtml2 homepage.en.yhtml2 heading.en.yhtml2
	$(YMLC) -o index.html index.en.yhtml2

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg

test:
	$(PYTHON) test_xmlast2.py
	$(PYTHON) test_pyPEG2.py
	$(PYTHON) sample1.py
	$(PYTHON) sample2.py

clean:
	rm -f index.html
