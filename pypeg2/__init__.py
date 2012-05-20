"""
pyPEG parsing framework

pyPEG offers a packrat parser as well as a framework to parse and output
languages for Python 3. See http://fdik.org/pyPEG2

Copyleft 2012, Volker Birk.
This program is under GNU General Public License 2.0.
"""

__version__ = 2.0
__author__ = "Volker Birk"
__license__ = "This program is under GNU General Public License 2.0."
__url__ = "http://fdik.org/pyPEG"

import re
import collections
import sys
import weakref
from functools import reduce
from types import FunctionType


word = re.compile(r"\w+")
"""Regular expression for scanning a word."""

RegEx = type(word)
"""Type of compiled regex."""

restline = re.compile(r".*")
"""Regular expression for rest of line."""

whitespace = re.compile("(?m)\s+")
"""Regular expression for scanning whitespace."""

comment_sh  = re.compile(r"\#.*")
"""Shell script style comment."""

comment_cpp = re.compile(r"//.*")
"""C++ style comment."""

comment_c   = re.compile(r"(?m)/\*.*?\*/")
"""C style comment without nesting comments."""

comment_pas = re.compile(r"(?m)\(\*.*?\*\)")
"""Pascal style comment without nesting comments."""


def _card(n, thing):
    # Reduce unnecessary recursions
    if len(thing) == 1:
        return n, thing[0]
    else:
        return n, thing


def some(*thing):
    """At least one occurrence of thing, + operator.
    Inserts -2 as cardinality before thing.
    """
    return _card(-2, thing)


def maybe_some(*thing):
    """No thing or some of them, * operator.
    Inserts -1 as cardinality before thing.
    """
    return _card(-1, thing)


def optional(*thing):
    """Thing or no thing, ? operator.
    Inserts 0 as cardinality before thing.
    """
    return _card(0, thing)


def csl(*thing):
    """Generate a grammar for a simple comma separated list."""
    # reduce unnecessary recursions
    if len(thing) == 1:
        L = [thing[0]]
        L.extend(maybe_some(",", blank, thing[0]))
        return tuple(L)
    else:
        L = list(thing)
        L.append(-1)
        L2 = [",", blank]
        L2.extend(tuple(thing))
        L.append(tuple(L2))
        return tuple(L)


def attr(name, thing=word, subtype=None):
    """Generate an Attribute with that name, referencing the thing.

    Instance variables:
        Class       reference to Attribute class generated by namedtuple()
    """
    return attr.Class(name, thing, subtype)

attr.Class = collections.namedtuple("Attribute", ("name", "thing", "subtype"))


def flag(name, thing):
    """Generate an Attribute with that name which is valued True or False."""
    return attr(name, thing, "Flag")


def attributes(grammar):
    """Iterates all attributes of a grammar."""
    if type(grammar) == attr.Class:
        yield grammar
    elif type(grammar) == tuple:
        for e in grammar:
            for a in attributes(e):
                yield a


class List(list):
    """A List of things."""

    def __init__(self, L=[], **kwargs):
        """Construct a List, and construct its attributes from keyword
        arguments.
        """
        super().__init__(L)
        for k, v in kwargs:
            setattr(self, k, v)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return ''.join((type(self).__name__, "(", super().__repr__(), ")"))


class Namespace(collections.UserDict):
    """A dictionary of things, indexed by their name."""

    def __init__(self, *args, **kwargs):
        """Initialize an OrderedDict containing the data of the Namespace.
        Arguments are being put into the Namespace, keyword arguments give the
        attributes of the Namespace.
        """
        self.data = collections.OrderedDict(args)
        for k, v in kwargs:
            setattr(self, k, v)

    def __setitem__(self, key, value):
        """x.__setitem__(i, y) <==> x[i]=y"""
        value.name = key
        try:
            value.namespace
        except AttributeError:
            value.namespace = weakref.ref(self)
        else:
            if not(value.namespace):
                value.namespace = weakref.ref(self)
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """x.__delitem__(y) <==> del x[y]"""
        self[key].namespace = None
        super().__delitem__(key)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return type(self).__name__ + repr(self.data)[11:]


class Enum(Namespace):
    """A Namespace which is being treated as an Enum.
    Enums can only contain Keywords or Symbols."""

    def __init__(self, *things):
        """Construct an Enum using a tuple of things."""
        self.data = collections.OrderedDict()
        for thing in things:
            if type(thing) == str:
                thing = Symbol(thing)
            if not isinstance(thing, Symbol):
                raise TypeError(repr(thing) + " is not a Symbol")
            super().__setitem__(thing.name, thing)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        v = [e for e in self.values()]
        return type(self).__name__ + "(" + repr(v) + ")"

    def __setitem__(self, key, value):
        """x.__setitem__(i, y) <==> x[i]=y"""
        if not isinstance(value, Keyword) and not isinstance(value, Symbol):
            raise TypeError("Enums can only contain Keywords or Symbols")
        raise ValueError("Enums cannot be modified after creation.")


class Symbol(str):
    """Use to scan Symbols.

    Class variables:
        regex               regular expression to scan, default r"\w+"
        check_keywords      flag if a Symbol is checked for not being a Keyword
                            default: False
    """

    regex = word
    check_keywords = False

    def __init__(self, name, namespace=None):
        """Construct a Symbol with that name in Namespace namespace.

        Raises:
            ValueError      if check_keywords is True and value is identical to
                            a Keyword
            TypeError       if namespace is given and not a Namespace
        """

        if Symbol.check_keywords and name in Keyword.table:
            raise ValueError(repr(name)
                    + " is a Keyword, but is used as a Symbol")
        if namespace:
            if isinstance(namespace, Namespace):
                namespace[name] = self
            else:
                raise TypeError(repr(namespace) + " is not a Namespace")
        else:
            self.name = name
            self.namespace = None

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return type(self).__name__ + "(" + str(self).__repr__() + ")"


class Keyword(Symbol):
    """Use to access the keyword table.

    Class variables:
        regex   regular expression to scan, default r"\w+"
        table   Namespace with keyword table
    """

    regex = word
    table = Namespace()

    def __init__(self, keyword):
        """Adds keyword to the keyword table."""
        Keyword.table[keyword] = self

K = Keyword
"""Shortcut for Keyword."""


def name():
    """Generate a grammar for a symbol with name."""
    return attr("name", Symbol)


class _Ignore:
    pass


def ignore(*grammar):
    """Ignore what matches to the grammar."""

    try:
        ignore.serial += 1
    except AttributeError:
        ignore.serial = 1
    return type("_Ignore" + str(ignore.serial), (_Ignore,),
            dict(grammar=optional(grammar)))


def indent(*thing):
    """Indent thing by one level.
    Inserts -3 as cardinality before thing.
    """
    return _card(-3, thing)


def endl(thing, parser):
    """End of line marker for composing text."""
    return "\n"


def blank(thing, parser):
    """Space marker for composing text."""
    return " "


class GrammarTypeError(TypeError):
    """Raised if grammar contains an object of unkown type."""


def how_many(grammar):
    """Determines the possibly parsed objects of grammar.

    Returns:
        0 if there will be no objects
        1 if there will be a maximum of one object
        2 if there can be more than one object
    """

    if type(grammar) == list:
        return reduce(lambda a, b: max(how_many(a), how_many(b)), grammar)

    elif type(grammar) == tuple:
        length, card = 0, 1
        for e in grammar:
            if type(e) == int:
                if e < -3:
                    raise ValueError(
                        "illegal cardinality value in grammar: " + str(e))
                if e in (-1, -2):
                    card = 2
                elif e in (-3, 0):
                    card = 1
                else:
                    card = min(e, 2)
            else:
                length += card * how_many(e)
                if length >= 2:
                    return 2
        return length

    elif type(grammar) == str or isinstance(grammar, Keyword):
        return 0

    elif isinstance(grammar, Symbol) or isinstance(grammar, RegEx):
        return 1

    elif isinstance(grammar, attr.Class):
        return 0

    elif _issubclass(grammar, _Ignore) or type(grammar) == FunctionType:
        return 0

    elif _issubclass(grammar, object):
        try:
            grammar.grammar
        except AttributeError:
            if subclass(grammar, list) or subclass(grammar, Namespace):
                return 2
            else:
                return 1
        else:
            return how_many(grammar.grammar)

    else:
        raise GrammarTypeError("grammar contains an illegal type: "
                + type(grammar).__name__)


def parse(text, thing, filename=None, whitespace=whitespace, comment=None):
    """Parse text following thing.grammar and return the resulting things or
    raise an error.

    Arguments:
        text        text to parse
        thing       grammar for things to parse
        filename    filename where text is origin from
        whitespace  regular expression to _skip whitespace
                    default: regex "(?m)\s+"
        comment     grammar to parse comments
                    default: None

    Returns generated objects.

    Raises:
        SyntaxError if text does not match the grammar in thing
        ValueError  if input does not match types
        TypeError   if output classes have wrong syntax for __init__()
        GrammarTypeError
                    if grammar contains an object of unkown type
    """

    parser = Parser()
    parser.whitespace = whitespace
    parser.comment = comment
    parser.text = text
    parser.filename = filename

    t, r = parser.parse(text, thing)
    if t:
        raise parser.last_error
    return r


def compose(thing, grammar=None, indent="    "):
    """Compose text using thing with grammar.

    Arguments:
        thing           thing containing other things with grammar
        grammar         grammar to use to compose thing
                        default: thing.grammar
        indent          string to use to indent while composing
                        default: four spaces

    Returns text
    """

    parser = Parser()
    parser.indent = indent
    return parser.compose(thing, grammar)


def _issubclass(obj, cls):
    # If obj is not a class, just return False
    try:
        return issubclass(obj, cls)
    except TypeError:
        return False


class Parser:
    """Offers parsing and composing capabilities. Implements a Packrat parser.
    
    Instance variables:
        whitespace      regular expression to scan whitespace
                        default: "(?m)\s+"
        comment         grammar to parse comments
        last_error      syntax error which ended parsing
        indent          string to use to indent while composing
                        default: four spaces
        indention_level level to indent to
                        default: 0
        text            original text to parse; set for decorated syntax errors
        filename        filename where text is origin from
    """

    def __init__(self):
        """Initialize instance variables to their defaults."""
        self.whitespace = whitespace
        self.comment = None
        self.last_error = None
        self.indent = "    "
        self.indention_level = 0
        self.text = None
        self.filename = None
        self._memory = {}
        self._got_endl = False

    def parse(self, text, thing, filename=None):
        """Parse text following thing.grammar and return the resulting things
        or raise an error.

        Arguments:
            text        text to parse
            thing       grammar for things to parse
            filename    filename where text is origin from

        Returns (text, result) with:
            text        unparsed text
            result      generated objects

        Raises:
            ValueError  if input does not match types
            TypeError   if output classes have wrong syntax for __init__()
            GrammarTypeError
                        if grammar contains an object of unkown type
        """

        self.text = text
        if filename:
            self.filename = filename
        pos = [1, 0]
        t = self._skip(text, pos)
        t, r = self._parse(t, thing, pos)
        if type(r) == SyntaxError:
            raise r
        else:
            return t, r

    def _skip(self, text, pos=None):
        # Skip whitespace and comments from input text
        t2 = None
        t = text
        while t2 != t:
            if self.whitespace:
                t, r = self._parse(t, self.whitespace, pos)
            t2 = t
            if self.comment:
                t, r = self._parse(t, self.comment, pos)
        return t

    def _parse(self, text, thing, pos=[1, 0]):
        # Parser implementation

        def update_pos(text, t, pos):
            # Calculate where we are in the text
            if not pos:
                return
            if text == t:
                return
            d_text = text[:len(text) - len(t)]
            pos[0] += d_text.count("\n")
            pos[1] += len(d_text)

        try:
            return self._memory[(text, id(thing))]
        except KeyError:
            pass

        if pos: 
            current_pos = tuple(pos)
        else:
            current_pos = None

        def syntax_error(msg):
            # Create a syntax error construct with sensible attributes
            result = SyntaxError(msg)
            if pos:
                result.lineno = pos[0]
                start = max(pos[1] - 19, 0)
                end   = min(pos[1] + 20, len(self.text))
                result.text = self.text[start:end]
                result.offset = pos[1] - start + 1
                while "\n" in result.text:
                    lf = result.text.find("\n")
                    if lf >= result.offset:
                        result.text = result.text[:result.offset-1]
                        break;
                    else:
                        L = len(result.text)
                        result.text = result.text[lf+1:]
                        result.offset -= L - len(result.text)
                if self.filename:
                    result.filename = self.filename
            return result

        # terminal symbols

        if thing is None or type(thing) == FunctionType:
            result = text, None

        elif type(thing) == str:
            if text.startswith(thing):
                t, r = text[len(thing):], None
                t = self._skip(t)
                result = t, r
                update_pos(text, t, pos)
            else:
                result = text, syntax_error("expecting " + repr(thing))

        elif isinstance(thing, RegEx):
            m = thing.match(text)
            if m:
                t, r = text[len(m.group(0)):], m.group(0)
                t = self._skip(t)
                result = t, r
                update_pos(text, t, pos)
            else:
                result = text, syntax_error("expecting match on "
                        + thing.pattern)

        elif isinstance(thing, Keyword):
            m = type(thing).regex.match(text)
            if m and m.group(0) == str(thing):
                t, r = text[len(thing):], None
                t = self._skip(t)
                result = t, r
                update_pos(text, t, pos)
            else:
                result = text, syntax_error("expecting " + repr(thing))

        elif _issubclass(thing, Symbol):
            m = thing.regex.match(text)
            if m:
                result = None
                try:
                    thing.grammar
                except AttributeError:
                    pass
                else:
                    if isinstance(thing.grammar, Enum):
                        if not m.group(0) in thing.grammar:
                            result = text, syntax_error(repr(m.group(0))
                                + " is not a member of " + repr(thing.grammar))
                    else:
                        raise TypeError(
                            "only an Enum is allowed as a grammar of a Symbol")
                if not result:
                    t, r = text[len(m.group(0)):], thing(m.group(0))
                    t = self._skip(t)
                    result = t, r
                    update_pos(text, t, pos)
            else:
                result = text, syntax_error("expecting " + type(thing).__name__)

        # non-terminal constructs

        elif type(thing) == attr.Class:
            t, r = self._parse(text, thing.thing, pos)
            if type(r) == SyntaxError:
                if thing.subtype == "Flag":
                    result = t, attr(thing.name, False)
                else:
                    result = text, r
            else:
                if thing.subtype == "Flag":
                    result = t, attr(thing.name, True)
                else:
                    result = t, attr(thing.name, r)

        elif type(thing) == tuple:
            L = []
            t = text
            flag = True
            _min, _max = 1, 1
            for e in thing:
                if type(e) == int:
                    if e < -3:
                        raise ValueError(
                            "illegal cardinality value in grammar: " + str(e))
                    if e == -3:
                        _min, _max = 1, 1
                    elif e == -2:
                        _min, _max = 1, sys.maxsize
                    elif e == -1:
                        _min, _max = 0, sys.maxsize
                    elif e ==  0:
                        _min, _max = 0, 1
                    else:
                        _min, _max = e, e
                    continue
                for i in range(_max):
                    t2, r = self._parse(t, e, pos)
                    if type(r) == SyntaxError:
                        i -= 1
                        break
                    else:
                        t = t2
                        if r != None:
                            if type(r) is list:
                                L.extend(r)
                            else:
                                L.append(r)
                if i+1 < _min:
                    if type(r) != SyntaxError:
                        r = syntax_error("expecting " + str(_min)
                                + " occurrence(s) of " + repr(e)
                                + " (" + str(i+1) + " found)")
                    flag = False
                    break
                _min, _max = 1, 1
            if flag:
                result = t, L
            else:
                result = text, r

        elif type(thing) == list:
            found = False
            for e in thing:
                t, r = self._parse(text, e, pos)
                if type(r) != SyntaxError:
                    found = True
                    break
            if found:
                result = t, r
            else:
                result = text, syntax_error("expecting one of " + repr(thing))

        elif _issubclass(thing, list):
            try:
                g = thing.grammar
            except AttributeError:
                g = csl(name())
            t, r = self._parse(text, g, pos)
            if type(r) != SyntaxError:
                obj = thing()
                for e in r:
                    if type(e) == attr.Class:
                        setattr(obj, e.name, e.thing)
                    else:
                        obj.append(e)
                try:
                    obj.polish()
                except AttributeError:
                    pass
                result = t, obj
            else:
                result = text, r

        elif _issubclass(thing, Namespace):
            t, r = self._parse(text, thing.grammar, pos)
            if type(r) != SyntaxError:
                obj = thing()
                for e in r:
                    if type(e) == attr.Class:
                        setattr(obj, e.name, e.thing)
                    else:
                        obj[e.name] = e
                try:
                    obj.polish()
                except AttributeError:
                    pass
                result = t, obj
            else:
                result = text, r

        elif _issubclass(thing, _Ignore):
            t, r = self._parse(text, thing.grammar, pos)
            if type(r) == SyntaxError:
                result = t, r
            else:
                result = t, None

        elif _issubclass(thing, object):
            try:
                g = thing.grammar
            except AttributeError:
                g = word
            t, r = self._parse(text, g, pos)
            if type(r) != SyntaxError:
                if isinstance(r, list):
                    L, a = [], []
                    for e in r:
                        if type(e) == attr.Class:
                            a.append(e)
                        else:
                            L.append(e)
                    if L:
                        lg = how_many(thing.grammar)
                        if lg == 0:
                            obj = None
                        elif lg == 1:
                            obj = thing(L[0])
                        else:
                            obj = thing(L)
                    else:
                        obj = thing()
                    for e in a:
                        setattr(obj, e.name, e.thing)
                else:
                    if type(r) == attr.Class:
                        obj = thing()
                        setattr(obj, r.name, r.thing)
                    else:
                        if r is None:
                            obj = thing()
                        else:
                            obj = thing(r)
                try:
                    obj.polish()
                except AttributeError:
                    pass
                result = t, obj
            else:
                result = text, r

        else:
            raise GrammarTypeError("in grammar: " + repr(thing))

        if pos:
            if type(result[1]) == SyntaxError:
                pos[0] = current_pos[0]
                pos[1] = current_pos[1]
                self.last_error = result[1]
            else:
                try:
                    result[1].position_in_text = current_pos
                except AttributeError:
                    pass

        self._memory[(text, id(thing))] = result
        return result

    def compose(self, thing, grammar=None):
        """Compose text using thing with grammar.

        Arguments:
            thing           thing containing other things with grammar
            grammar         grammar to use to compose thing
                            default: thing.grammar

        Returns text
        """
 
        def terminal_indent():
            if self._got_endl:
                result = self.indent * self.indention_level
                self._got_endl = False
                return result
            else:
                return ""

        if not grammar:
            try:
                grammar = type(thing).grammar
            except AttributeError:
                if isinstance(thing, list):
                    grammar = csl(name())
                else:
                    grammar = word

        if grammar is None:
            result = ""

        elif type(grammar) == FunctionType:
            if grammar == endl:
                result = "\n"
                self._got_endl = True
            else:
                result = self.compose(thing, grammar(thing, self))

        elif isinstance(grammar, (str, int, float, complex, bool, bytes)):
            result = terminal_indent() + str(grammar)

        elif isinstance(grammar, RegEx):
            m = grammar.match(str(thing))
            if m:
                result = terminal_indent() + str(thing)
            else:
                raise ValueError(repr(thing) + " does not match " + grammar.pattern)

        elif isinstance(grammar, Enum):
            if thing in grammar:
                result = terminal_indent() + str(thing)
            else:
                raise ValueError(repr(thing) + " is not in " + repr(grammar))

        elif type(grammar) == attr.Class:
            if grammar.subtype == "Flag":
                if getattr(thing, grammar.name):
                    result = terminal_indent() + str(grammar.thing)
                else:
                    result = ""
            else:
                result = self.compose(getattr(thing, grammar.name))

        elif type(grammar) == list:
            found = False
            for g in grammar:
                try:
                    result = self.compose(thing, g)
                    found = True
                    break
                except GrammarTypeError:
                    raise
                except AttributeError:
                    pass
                except KeyError:
                    pass
                except TypeError:
                    pass
                except ValueError:
                    pass
            if not found:
                raise ValueError("none of the options in " + repr(grammar)
                        + " found")

        elif type(grammar) == tuple:
            def compose_tuple(thing, things, grammar):
                text = []
                multiple, card = 1, 1
                indenting = 0
                for g in grammar:
                    if type(g) == int:
                        if g < -3:
                            raise ValueError(
                                "illegal cardinality value in grammar: " +
                                str(g)
                            )
                        card = g
                        if g in (-2, -1):
                            multiple = sys.maxsize
                        elif g in (-3, 0):
                            multiple = 1
                            if g == -3:
                                self.indention_level += 1
                                indenting = 1
                        else:
                            multiple = g
                    else:
                        if indenting == 1:
                            indenting = 2
                        elif indenting == 2:
                            self.indention_level -= 1
                            indenting = 0
                        if type(g) == attr.Class:
                            text.append(self.compose(thing, g))
                        elif type(g) == str or isinstance(g, Keyword):
                            if card > 0:
                                for i in range(multiple):
                                    text.append(terminal_indent() + str(g))
                            elif card == -2:
                                text.append(terminal_indent() + str(g))
                        else:
                            for j in range(multiple):
                                if type(g) == tuple:
                                    if not things:
                                        return ''.join(text)
                                    text.append(compose_tuple(thing, things, g))
                                else:
                                    if g is None:
                                        pass
                                    elif type(g) == FunctionType:
                                        text.append(self.compose(things, g))
                                    elif type(g) == str or isinstance(g,
                                            Keyword):
                                        text.append(self.compose(things, g))
                                    elif type(things) == list:
                                        if not things:
                                            return ''.join(text)
                                        text.append(self.compose(things[0], g))
                                        del things[0]
                                    else:
                                        text.append(self.compose(things, g))
                        multiple = 1
                    if indenting == 2:
                        self.indention_level -= 1
                        indenting = 0
                return ''.join(text)

            if isinstance(thing, Namespace):
                L = [e for e in thing.values()]
                result = compose_tuple(thing, L, grammar)
            elif isinstance(thing, list):
                result = compose_tuple(thing, thing[:], grammar)
            else:
                result = compose_tuple(thing, thing, grammar)

        elif _issubclass(grammar, _Ignore):
            result = ""

        elif _issubclass(grammar, object):
            if isinstance(thing, grammar):
                try:
                    grammar.grammar
                except AttributeError:
                    if isinstance(grammar, list):
                        result = self.compose(thing, csl(word))
                    else:
                        result = self.compose(thing, word)
                else:
                    result = self.compose(thing, grammar.grammar)
            else:
                raise ValueError(repr(thing) + " is not a " + repr(grammar))

        else:
            raise GrammarTypeError("in grammar: " + repr(grammar))

        return result
