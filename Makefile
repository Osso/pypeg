.PHONY: docs clean push

docs:
	$(MAKE) -C docs

clean:
	$(MAKE) -C docs clean

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg
