# put the path to your local YML 2 compiler and processor here

YML2C=yml2c
YML2PROC=yml2proc

documentation: index.html features.html

contents.xml: index.en.yhtml2 gen_contents.ysl2
	$(YML2PROC) -y gen_contents.ysl2 -o $@ $<

%.html: %.en.yhtml2 homepage.en.yhtml2 heading.en.yhtml2 contents.xml
	$(YML2C) -o $@ ./homepage.en.yhtml2 $<

clean:
	rm -f index.html contents.xml
