"""
XML AST generator

pyPEG parsing framework

Copyleft 2012, Volker Birk.
This program is under GNU General Public License 2.0.
"""

__version__ = 2.0
__author__ = "Volker Birk"
__license__ = "This program is under GNU General Public License 2.0."
__url__ = "http://fdik.org/pyPEG"

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

import pypeg2


def create_tree(thing, object_names=False, parent=None):
    """Create an XML etree from a thing.

    Arguments:
        thing           thing to interpret
        parent          etree.Element to put subtree into
                        default: create a new Element tree

    Returns:
        etree object created
    """

    try:
        grammar = type(thing).grammar
    except AttributeError:
        if isinstance(thing, pypeg2.List):
            grammar = pypeg2.csl(name())
        else:
            grammar = word

    name = type(thing).__name__

    if object_names:
        try:
            name = str(thing.name)
            name = name.replace(" ", "_")
        except AttributeError:
            pass

    if parent is None:
        me = etree.Element(name)
    else:
        me = etree.SubElement(parent, name)

    for e in pypeg2.attributes(grammar):
        if object_names and e.name == "name":
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
            create_tree(value, object_names, me)

    if isinstance(thing, list):
        things = thing
    elif isinstance(thing, pypeg2.Namespace):
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
            last = create_tree(t, object_names, me)

    if isinstance(thing, str):
        me.text = str(thing)

    return me


def thing2xml(thing, pretty=False, object_names=False):
    """Create XML text from a thing.

    Arguments:
        thing           thing to interpret
        pretty          True if xml should be indented
                        False if xml should be plain

    Returns:
        bytes with encoded XML 
    """

    tree = create_tree(thing, object_names)
    return etree.tostring(tree, pretty_print=pretty)


def create_thing(element, symbol_table):
    """Create thing from an XML eelement.

    Arguments:
        element         Element instance to read
        symbol_table    symbol table where the classes can be found

    Returns:
        things created
    """

    C = symbol_table[element.tag]
    if element.text:
        thing = C(element.text)
    else:
        thing = C()
    
    subs = iter(list(element))
    try:
        sub = next(subs)
    except StopIteration:
        pass

    try:
        grammar = C.grammar
    except AttributeError:
        if isinstance(C, pypeg2.List) or isinstance(C, pypeg2.Namespace):
            grammar = pypeg2.csl(pypeg2.word)
        else:
            grammar = pypeg2.word

    for e in pypeg2.attributes(grammar):
        key = e.name
        try:
            value = element.attrib[e.name]
        except KeyError:
            t = create_thing(sub, symbol_table)
            setattr(thing, key, t)
            sub = next(subs)
        else:
            setattr(thing, key, e.thing(value))

    if isinstance(thing, pypeg2.List) or isinstance(thing, pypeg2.Namespace):
        try:
            while True:
                t = create_thing(sub, symbol_table)
                if isinstance(thing, pypeg2.List):
                    thing.append(t)
                else:
                    thing[t.name] = t
                sub = next(subs)
        except StopIteration:
            pass
    
    return thing

def xml2thing(xml, symbol_table):
    """Create thing from XML text.

    Arguments:
        xml             bytes with encoded XML
        symbol_table    symbol table where the classes can be found

    Returns:
        created thing
    """

    element = etree.fromstring(xml)
    return create_thing(element, symbol_table)

