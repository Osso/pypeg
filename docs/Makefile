# put the path to your local YML 2 compiler and processor here

YML2C=yml2c
YML2PROC=yml2proc

# for validating documentation (optional)
# see http://xmlstar.sourceforge.net/

XMLSTARLET=xmlstarlet
XHTML1_DTD=/opt/local/share/xml/html/4/xhtml1-transitional.dtd
XHTML_VALIDATOR=$(XMLSTARLET) val -e -d $(XHTML1_DTD)

YHTML=$(wildcard *.en.yhtml2)
HTML=$(subst en.yhtml2,html,$(YHTML))
XML=$(subst en.yhtml2,xml,$(YHTML))
YINC=$(wildcard *.en.yinc2)

documentation: $(HTML)

%.xml: %.en.yhtml2 gen_contents.ysl2
	$(YML2PROC) -y gen_contents.ysl2 -s 'dict(file="$(subst .xml,,$@)")' -o $@ $<

%.html: %.en.yhtml2 $(YINC) $(XML)
	$(YML2C) -o $@ ./homepage.en.yinc2 $<

.PHONY: test clean

test: $(subst .html,.test,$(HTML))

%.test: %.html
	$(XHTML_VALIDATOR) $<

clean:
	rm -f *.html *.xml
