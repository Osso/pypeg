import unittest
import pyPEG2
import re

class ParserTestCase(unittest.TestCase): pass

class TypeErrorTestCase(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(pyPEG2.GrammarTypeError):
            parser.parse("hello, world", 23)

class ParseTerminalStringTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", "hello")
        self.assertEqual(r, (", world", None))

class ParseTerminalStringTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", "world")

class ParseKeywordTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hallo, world", pyPEG2.K("hallo"))
        self.assertEqual(r, (", world", pyPEG2.Keyword("hallo")))
        pyPEG2.Keyword.table[pyPEG2.K("hallo")]

class ParseKeywordTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", pyPEG2.K("werld"))
        pyPEG2.Keyword.table[pyPEG2.K("werld")]

class ParseKeywordTestCase3(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse(", world", pyPEG2.K("hallo"))
        pyPEG2.Keyword.table[pyPEG2.K("hallo")]

class ParseRegexTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", re.compile(r"h.[lx]l\S"))
        self.assertEqual(r, (", world", "hello"))

class ParseRegexTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", re.compile(r"\d"))

class ParseSymbolTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", pyPEG2.Symbol)
        self.assertEqual(r, (", world", pyPEG2.Symbol("hello")))

class ParseSymbolTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse(", world", pyPEG2.Symbol)

class ParseAttributeTestCase(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", pyPEG2.attr("some", pyPEG2.Symbol))
        self.assertEqual(
            r,
            (
                ', world',
                pyPEG2.attr.Class(name='some', thing=pyPEG2.Symbol('hello'),
                    subtype=None)
            )
        )

class ParseTupleTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", (pyPEG2.name(), ",", pyPEG2.name()))
        self.assertEqual(
            r,
            (
                '',
                [
                    pyPEG2.attr.Class(name='name',
                        thing=pyPEG2.Symbol('hello'), subtype=None),
                    pyPEG2.attr.Class(name='name',
                        thing=pyPEG2.Symbol('world'), subtype=None)
                ]
            )
        )

class ParseTupleTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(ValueError):
            parser.parse("hello, world", (-23, "x"))

class ParseSomeTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", pyPEG2.some(re.compile(r"\w")))
        self.assertEqual(r, (', world', ['h', 'e', 'l', 'l', 'o']))

class ParseSomeTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", pyPEG2.some(re.compile(r"\d")))

class ParseMaybeSomeTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", pyPEG2.maybe_some(re.compile(r"\w")))
        self.assertEqual(r, (', world', ['h', 'e', 'l', 'l', 'o']))

class ParseMaybeSomeTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", pyPEG2.maybe_some(re.compile(r"\d")))
        self.assertEqual(r, ('hello, world', []))

class ParseCardinalityTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", (5, re.compile(r"\w")))
        self.assertEqual(r, (', world', ['h', 'e', 'l', 'l', 'o']))

class ParseCardinalityTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", (6, re.compile(r"\w")))

class ParseOptionsTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", [re.compile(r"\d+"), pyPEG2.word])
        self.assertEqual(r, (', world', 'hello'))

class ParseOptionsTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", ["x", "y"])

class ParseListTestCase1(ParserTestCase):
    class Chars(pyPEG2.List):
        grammar = pyPEG2.some(re.compile(r"\w")), pyPEG2.attr("comma", ",")

    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", ParseListTestCase1.Chars)
        self.assertEqual(r, (
            'world',
            ParseListTestCase1.Chars(['h', 'e', 'l', 'l', 'o']))
        )
        self.assertEqual(r[1].comma, None)

class ParseListTestCase2(ParserTestCase):
    class Digits(pyPEG2.List):
        grammar = pyPEG2.some(re.compile(r"\d"))

    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", ParseListTestCase2.Digits)

class ParseClassTestCase1(ParserTestCase):
    class Word(str):
        grammar = pyPEG2.word
 
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", ParseClassTestCase1.Word)
        self.assertEqual(type(r[1]), ParseClassTestCase1.Word)
        self.assertEqual(r[1], "hello")

class ParseClassTestCase2(ParserTestCase):
    class Word(str):
        grammar = pyPEG2.word, pyPEG2.attr("comma", ",")
        def __init__(self, data):
            self.polished = False
        def polish(self):
            self.polished = True
 
    def runTest(self):
        parser = pyPEG2.Parser()
        r = parser.parse("hello, world", ParseClassTestCase2.Word)
        self.assertEqual(type(r[1]), ParseClassTestCase2.Word)
        self.assertEqual(r[1], "hello")
        self.assertTrue(r[1].polished)
        self.assertEqual(r[1].comma, None)

class Parm:
    grammar = pyPEG2.name(), "=", pyPEG2.attr("value", int)

class Parms(pyPEG2.Namespace):
    grammar = (pyPEG2.csl(Parm), pyPEG2.flag("fullstop", "."),
            pyPEG2.flag("semicolon", ";"))

class ParseNLTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        parser.comment = pyPEG2.comment_c
        t, parms = parser.parse("x=23 /* Illuminati */, y=42 /* the answer */;", Parms)
        self.assertEqual(parms["x"].value, 23)
        self.assertEqual(parms["y"].value, 42)
        self.assertEqual(parms.fullstop, False)
        self.assertEqual(parms.semicolon, True)

class EnumTest(pyPEG2.Symbol):
    grammar = pyPEG2.Enum( pyPEG2.K("int"), pyPEG2.K("long") )

class ParseEnumTestCase1(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        t, r = parser.parse("int", EnumTest)
        self.assertEqual(r, "int")

class ParseEnumTestCase2(ParserTestCase):
    def runTest(self):
        parser = pyPEG2.Parser()
        with self.assertRaises(SyntaxError):
            t, r = parser.parse("float", EnumTest)

class ComposeTestCase(unittest.TestCase): pass

class ComposeString:
    grammar = "something"

class ComposeStringTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeString()
        t = pyPEG2.compose(x)
        self.assertEqual(t, "something")

class ComposeRegex(str):
    grammar = pyPEG2.word

class ComposeRegexTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeRegex("something")
        t = pyPEG2.compose(x)
        self.assertEqual(t, "something")

class ComposeKeyword:
    grammar = pyPEG2.K("hallo")

class ComposeKeywordTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeKeyword()
        t = pyPEG2.compose(x)
        self.assertEqual(t, "hallo")

class ComposeSymbol(str):
    grammar = pyPEG2.Symbol

class ComposeSymbolTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeSymbol("hello")
        t = pyPEG2.compose(x)
        self.assertEqual(t, "hello")

class ComposeAttribute:
    grammar = pyPEG2.name()

class ComposeAttributeTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeAttribute()
        x.name = "hello"
        t = pyPEG2.compose(x)
        self.assertEqual(t, "hello")

class ComposeFlag:
    grammar = pyPEG2.flag("mark", "MARK")

class ComposeFlagTestCase1(ComposeTestCase):
    def runTest(self):
        x = ComposeFlag()
        x.mark = True
        t = pyPEG2.compose(x)
        self.assertEqual(t, "MARK")

class ComposeFlagTestCase2(ComposeTestCase):
    def runTest(self):
        x = ComposeFlag()
        x.mark = False
        t = pyPEG2.compose(x)
        self.assertEqual(t, "")

class ComposeTuple(pyPEG2.List):
    grammar = pyPEG2.csl(pyPEG2.word)

class ComposeTupleTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeTuple(["hello", "world"])
        t = pyPEG2.compose(x)
        self.assertEqual(t, "hello, world")

class ComposeList(str):
    grammar = [ re.compile(r"\d+"), pyPEG2.word ]

class ComposeListTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeList("hello")
        t = pyPEG2.compose(x)
        self.assertEqual(t, "hello")

if __name__ == '__main__':
    unittest.main()
