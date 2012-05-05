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

from pyPEG2 import List, Namespace, attributes


def thing2xml(thing, parent=None):
    """Create an XML etree from a thing."""

    if not grammar:
        try:
            grammar = type(thing).grammar
        except AttributeError:
            if isinstance(thing, List):
                grammar = csl(name())
            else:
                grammar = word

    attrib = { e.name: e.thing for e in attributes(grammar) }

    if not parent:
        tree = etree.ElementTree(Element(type(thing).__name__, attrib))
    else:
        tree.SubElement(parent, type(thing).__name__, attrib)


def xml2thing(xml):
    """Create things from an XML etree."""
