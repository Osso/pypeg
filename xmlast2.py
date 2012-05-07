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


def create_tree(thing, object_tree=False, parent=None):
    """Create an XML etree from a thing.

    Arguments:
        thing       thing to interpret
        parent      etree.Element to put subtree into
                    default: create a new Element tree
    """

    try:
        grammar = type(thing).grammar
    except AttributeError:
        if isinstance(thing, pyPEG2.List):
            grammar = pyPEG2.csl(name())
        else:
            grammar = pyPEG2.word

    name = type(thing).__name__

    if object_tree:
        try:
            name = str(thing.name)
            name = name.replace(" ", "_")
        except AttributeError:
            pass

    if parent is None:
        me = etree.Element(name)
    else:
        me = etree.SubElement(parent, name)

    for e in pyPEG2.attributes(grammar):
        if object_tree and e.name == "name":
            if name != type(thing).__name__:
                continue
        key, value = e.name, getattr(thing, e.name)
        found = False
        for tp in (str, int, float, complex, bool, bytes):
            if isinstance(value, tp):
                me.set(key, str(value))
                found = True
                break
        if not found:
            create_tree(value, object_tree, me)

    if isinstance(thing, list):
        things = thing
    elif isinstance(thing, pyPEG2.Namespace):
        things = thing.values()
    else:
        things = []

    last = None
    for t in things:
        if type(t) == str:
            if last is not None:
                last.tail = str(t)
            else:
                me.text = str(t)
        else:
            last = create_tree(t, object_tree, me)

    if isinstance(thing, str):
        me.text = str(thing)

    return me


def thing2xml(thing, pretty=False, object_tree=False):
    """Create XML text from a thing.

    Arguments:
        thing       thing to interpret
        pretty      True if xml should be indented
                    False if xml should be plain
    """

    tree = create_tree(thing, object_tree)
    return etree.tostring(tree, pretty_print=pretty)

