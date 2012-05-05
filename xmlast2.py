"""
XML AST generator

pyPEG parsing framework

Copyleft 2012, Volker Birk.
This program is under GNU General Public License 2.0.
"""

__version__ = 2.0

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

import pyPEG2


def create_tree(thing, parent=None):
    """Create an XML etree from a thing."""

    try:
        grammar = type(thing).grammar
    except AttributeError:
        if isinstance(thing, pyPEG2.List):
            grammar = pyPEG2.csl(name())
        else:
            grammar = pyPEG2.word

    if parent is None:
        me = etree.Element(type(thing).__name__)
    else:
        me = etree.SubElement(parent, type(thing).__name__)

    for e in pyPEG2.attributes(grammar):
        me.set(e.name, str(getattr(thing, e.name)))

    if isinstance(thing, pyPEG2.List):
        things = thing
    elif isinstance(thing, pyPEG2.Namespace):
        things = thing.values()
    else:
        things = []

    last = None
    for t in things:
        if isinstance(t, str):
            if last is not None:
                last.tail = str(t)
            else:
                me.text = str(t)
        else:
            last = create_tree(t, me)

    return me


def thing2xml(thing):
    """Create XML text from a thing."""

    tree = create_tree(thing)
    return etree.tostring(tree)

