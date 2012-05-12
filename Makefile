# put the path to your local Python 3 interpreter here

PYTHON=python3.2

# put the path to your local YML 2 compiler and processor here

YML2C=yml2c
YML2PROC=yml2proc

documentation: index.html

contents.xml: index.en.yhtml2 gen_contents.ysl2
	$(YML2PROC) -y gen_contents.ysl2 -o $@ $<

%.html: %.en.yhtml2 homepage.en.yhtml2 heading.en.yhtml2 contents.xml
	$(YML2C) -o $@ ./homepage.en.yhtml2 $<

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg

test:
	$(PYTHON) test_xmlast2.py
	$(PYTHON) test_pyPEG2.py
	$(PYTHON) sample1.py
	$(PYTHON) sample2.py

clean:
	rm -f index.html contents.xml
