.PHONY: docs test push clean

docs:
	$(MAKE) -C docs

test:
	$(MAKE) -C test

push:
	hg push ssh://hg@bitbucket.org/fdik/pypeg

clean:
	$(MAKE) -C docs clean
