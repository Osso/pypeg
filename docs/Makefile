# put the path to your local YML 2 compiler and processor here

YML2C=yml2c
YML2PROC=yml2proc

YHTML=$(wildcard *.en.yhtml2)
HTML=$(subst en.yhtml2,html,$(YHTML))
XML=$(subst en.yhtml2,xml,$(YHTML))
YINC=$(wildcard *.en.yinc2)

documentation: $(HTML)

%.xml: %.en.yhtml2 gen_contents.ysl2
	$(YML2PROC) -y gen_contents.ysl2 -s 'dict(file="$(subst .xml,,$@)")' -o $@ $<

%.html: %.en.yhtml2 $(YINC) $(XML)
	$(YML2C) -o $@ ./homepage.en.yinc2 $<

clean:
	rm -f *.html *.xml
