"""
XML AST generator

pyPEG parsing framework

Copyleft 2012, Volker Birk.
This program is under GNU General Public License 2.0.
"""


from __future__ import unicode_literals
try:
    str = unicode
except NameError:
    pass


__version__ = 2.7
__author__ = "Volker Birk"
__license__ = "This program is under GNU General Public License 2.0."
__url__ = "http://fdik.org/pyPEG"


try:
    import lxml
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

if __debug__:
    import warnings
import pypeg2


def create_tree(thing, parent=None, object_names=False):
    """Create an XML etree from a thing.

    Arguments:
        thing           thing to interpret
        parent          etree.Element to put subtree into
                        default: create a new Element tree
        object_names    experimental feature: if True tag names are object
                        names instead of types

    Returns:
        etree.Element instance created
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
            create_tree(value, me, object_names)

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
            last = create_tree(t, me, object_names)

    if isinstance(thing, str):
        me.text = str(thing)

    return me


def thing2xml(thing, pretty=False, object_names=False):
    """Create XML text from a thing.

    Arguments:
        thing           thing to interpret
        pretty          True if XML should be indented
                        False if XML should be plain
        object_names    experimental feature: if True tag names are object
                        names instead of types

    Returns:
        bytes with encoded XML 
    """

    tree = create_tree(thing, None, object_names)
    try:
        if lxml:
            return etree.tostring(tree, pretty_print=pretty)
    except NameError:
        if __debug__:
            if pretty:
                warnings.warn("lxml is needed for pretty printing",
                        ImportWarning)
        return etree.tostring(tree)


def create_thing(element, symbol_table):
    """Create thing from an XML element.

    Arguments:
        element         etree.Element instance to read
        symbol_table    symbol table where the classes can be found

    Returns:
        thing created
    """

    C = symbol_table[element.tag]
    if element.text:
        thing = C(element.text)
    else:
        thing = C()
    
    subs = iter(element)

    try:
        grammar = C.grammar
    except AttributeError:
        pass
    else:
        for e in pypeg2.attributes(grammar):
            key = e.name
            try:
                value = element.attrib[e.name]
            except KeyError:
                sub = next(subs)
                t = create_thing(sub, symbol_table)
                setattr(thing, key, t)
            else:
                setattr(thing, key, e.thing(value))

    if issubclass(C, list) or issubclass(C, pypeg2.Namespace):
        try:
            while True:
                sub = next(subs)
                t = create_thing(sub, symbol_table)
                if isinstance(thing, pypeg2.List):
                    thing.append(t)
                else:
                    thing[t.name] = t
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

