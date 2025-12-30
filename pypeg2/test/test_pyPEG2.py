import re
import unittest

import pypeg2


class GrammarTestCase1(unittest.TestCase):
    def runTest(self):
        x = pypeg2.some("thing")
        y = pypeg2.maybe_some("thing")
        z = pypeg2.optional("hello", "world")
        self.assertEqual(x, (-2, "thing"))
        self.assertEqual(y, (-1, "thing"))
        self.assertEqual(z, (0, ("hello", "world")))


class GrammarTestCase2(unittest.TestCase):
    def runTest(self):
        L1 = pypeg2.csl("thing")
        L2 = pypeg2.csl("hello", "world")
        self.assertEqual(L1, ("thing", -1, (",", pypeg2.blank, "thing")))
        self.assertEqual(L2, ("hello", "world", -1, (",", pypeg2.blank, "hello", "world")))


class ParserTestCase(unittest.TestCase):
    pass


class TypeErrorTestCase(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(pypeg2.GrammarTypeError):
            parser.parse("hello, world", 23)


class ParseTerminalStringTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", "hello")
        self.assertEqual(r, (", world", None))


class ParseTerminalStringTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", "world")


class ParseKeywordTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hallo, world", pypeg2.K("hallo"))
        self.assertEqual(r, (", world", None))
        pypeg2.Keyword.table[pypeg2.K("hallo")]


class ParseKeywordTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", pypeg2.K("werld"))
        pypeg2.Keyword.table[pypeg2.K("werld")]


class ParseKeywordTestCase3(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse(", world", pypeg2.K("hallo"))
        pypeg2.Keyword.table[pypeg2.K("hallo")]


class ParseRegexTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", re.compile(r"h.[lx]l\S", re.U))
        self.assertEqual(r, (", world", "hello"))


class ParseRegexTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", re.compile(r"\d", re.U))


class ParseSymbolTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.Symbol)
        self.assertEqual(r, (", world", pypeg2.Symbol("hello")))


class ParseSymbolTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse(", world", pypeg2.Symbol)


class ParseAttributeTestCase(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.attr("some", pypeg2.Symbol))
        self.assertEqual(
            r,
            (", world", pypeg2.attr.Class(name="some", thing=pypeg2.Symbol("hello"), subtype=None)),
        )


class ParseTupleTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", (pypeg2.name(), ",", pypeg2.name()))
        self.assertEqual(
            r,
            (
                "",
                [
                    pypeg2.attr.Class(name="name", thing=pypeg2.Symbol("hello"), subtype=None),
                    pypeg2.attr.Class(name="name", thing=pypeg2.Symbol("world"), subtype=None),
                ],
            ),
        )


class ParseTupleTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(ValueError):
            parser.parse("hello, world", (-23, "x"))


class ParseSomeTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.some(re.compile(r"\w", re.U)))
        self.assertEqual(r, (", world", ["h", "e", "l", "l", "o"]))


class ParseSomeTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", pypeg2.some(re.compile(r"\d", re.U)))


class ParseMaybeSomeTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.maybe_some(re.compile(r"\w", re.U)))
        self.assertEqual(r, (", world", ["h", "e", "l", "l", "o"]))


class ParseMaybeSomeTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.maybe_some(re.compile(r"\d", re.U)))
        self.assertEqual(r, ("hello, world", []))


class ParseCardinalityTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", (5, re.compile(r"\w", re.U)))
        self.assertEqual(r, (", world", ["h", "e", "l", "l", "o"]))


class ParseCardinalityTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", (6, re.compile(r"\w", re.U)))


class ParseOptionsTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", [re.compile(r"\d+", re.U), pypeg2.word])
        self.assertEqual(r, (", world", "hello"))


class ParseOptionsTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", ["x", "y"])


class ParseListTestCase1(ParserTestCase):
    class Chars(pypeg2.List):
        grammar = pypeg2.some(re.compile(r"\w", re.U)), pypeg2.attr("comma", ",")

    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", ParseListTestCase1.Chars)
        self.assertEqual(r, ("world", ParseListTestCase1.Chars(["h", "e", "l", "l", "o"])))
        self.assertEqual(r[1].comma, None)


class ParseListTestCase2(ParserTestCase):
    class Digits(pypeg2.List):
        grammar = pypeg2.some(re.compile(r"\d", re.U))

    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", ParseListTestCase2.Digits)


class ParseClassTestCase1(ParserTestCase):
    class Word(str):
        grammar = pypeg2.word

    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", ParseClassTestCase1.Word)
        self.assertEqual(type(r[1]), ParseClassTestCase1.Word)
        self.assertEqual(r[1], "hello")


class ParseClassTestCase2(ParserTestCase):
    class Word(str):
        grammar = pypeg2.word, pypeg2.attr("comma", ",")

        def __init__(self, data):
            self.polished = False

        def polish(self):
            self.polished = True

    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", ParseClassTestCase2.Word)
        self.assertEqual(type(r[1]), ParseClassTestCase2.Word)
        self.assertEqual(r[1], "hello")
        self.assertTrue(r[1].polished)
        self.assertEqual(r[1].comma, None)


class Parm(object):
    grammar = pypeg2.name(), "=", pypeg2.attr("value", int)


class Parms(pypeg2.Namespace):
    grammar = (pypeg2.csl(Parm), pypeg2.flag("fullstop", "."), pypeg2.flag("semicolon", ";"))


class ParseNLTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        parser.comment = pypeg2.comment_c
        t, parms = parser.parse("x=23 /* Illuminati */, y=42 /* the answer */;", Parms)
        self.assertEqual(parms["x"].value, 23)
        self.assertEqual(parms["y"].value, 42)
        self.assertEqual(parms.fullstop, False)
        self.assertEqual(parms.semicolon, True)


class EnumTest(pypeg2.Symbol):
    grammar = pypeg2.Enum(pypeg2.K("int"), pypeg2.K("long"))


class ParseEnumTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        t, r = parser.parse("int", EnumTest)
        self.assertEqual(r, "int")


class ParseEnumTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            t, r = parser.parse("float", EnumTest)


class ParseInvisibleTestCase(ParserTestCase):
    class C1(str):
        grammar = pypeg2.ignore("!"), pypeg2.restline

    def runTest(self):
        r = pypeg2.parse("!all", type(self).C1)
        self.assertEqual(str(r), "all")
        self.assertEqual(r._ignore1, None)


class ParseOmitTestCase(ParserTestCase):
    def runTest(self):
        r = pypeg2.parse("hello", pypeg2.omit(pypeg2.word))
        self.assertEqual(r, None)


class ComposeTestCase(unittest.TestCase):
    pass


class ComposeString(object):
    grammar = "something"


class ComposeStringTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeString()
        t = pypeg2.compose(x)
        self.assertEqual(t, "something")


class ComposeRegex(str):
    grammar = pypeg2.word


class ComposeRegexTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeRegex("something")
        t = pypeg2.compose(x)
        self.assertEqual(t, "something")


class ComposeKeyword(object):
    grammar = pypeg2.K("hallo")


class ComposeKeywordTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeKeyword()
        t = pypeg2.compose(x)
        self.assertEqual(t, "hallo")


class ComposeSymbol(pypeg2.Symbol):
    pass


class ComposeSymbolTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeSymbol("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")


class ComposeAttribute(object):
    grammar = pypeg2.name()


class ComposeAttributeTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeAttribute()
        x.name = pypeg2.Symbol("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")


class ComposeFlag(object):
    grammar = pypeg2.flag("mark", "MARK")


class ComposeFlagTestCase1(ComposeTestCase):
    def runTest(self):
        x = ComposeFlag()
        x.mark = True
        t = pypeg2.compose(x)
        self.assertEqual(t, "MARK")


class ComposeFlagTestCase2(ComposeTestCase):
    def runTest(self):
        x = ComposeFlag()
        x.mark = False
        t = pypeg2.compose(x)
        self.assertEqual(t, "")


class ComposeTuple(pypeg2.List):
    grammar = pypeg2.csl(pypeg2.word)


class ComposeTupleTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeTuple(["hello", "world"])
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello, world")


class ComposeList(str):
    grammar = [re.compile(r"\d+", re.U), pypeg2.word]


class ComposeListTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeList("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")


class ComposeIntTestCase(ComposeTestCase):
    def runTest(self):
        x = pypeg2.compose(23, int)
        self.assertEqual(x, "23")


class C2(str):
    grammar = pypeg2.attr("some", "!"), pypeg2.restline


class ComposeInvisibleTestCase(ParserTestCase):
    def runTest(self):
        r = pypeg2.parse("!all", C2)
        self.assertEqual(str(r), "all")
        self.assertEqual(r.some, None)
        t = pypeg2.compose(r, C2)
        self.assertEqual(t, "!all")


class ComposeOmitTestCase(ParserTestCase):
    def runTest(self):
        t = pypeg2.compose("hello", pypeg2.omit(pypeg2.word))
        self.assertEqual(t, "")


class CslPython32Compatibility(ParserTestCase):
    def runTest(self):
        try:
            g = eval("pypeg2.csl('hello', 'world', separator=';')")
        except TypeError:
            return
        self.assertEqual(g, ("hello", "world", -1, (";", pypeg2.blank, "hello", "world")))


# === Tests for __repr__ methods ===


class RegExReprTestCase(unittest.TestCase):
    def runTest(self):
        r = pypeg2.RegEx(r"\w+")
        self.assertEqual(repr(r), r"RegEx('\\w+')")

    def test_with_name(self):
        r = pypeg2.RegEx(r"\d+", name="digits")
        self.assertIn("name='digits'", repr(r))


class LiteralReprTestCase(unittest.TestCase):
    def runTest(self):
        lit = pypeg2.Literal("hello")
        self.assertEqual(repr(lit), "Literal('hello')")

    def test_str(self):
        lit = pypeg2.Literal("hello")
        self.assertEqual(str(lit), "hello")


class LiteralEqTestCase(unittest.TestCase):
    def runTest(self):
        lit1 = pypeg2.Literal("hello")
        lit2 = pypeg2.Literal("hello")
        lit3 = pypeg2.Literal("world")
        self.assertEqual(lit1, lit2)
        self.assertNotEqual(lit1, lit3)


class SymbolReprTestCase(unittest.TestCase):
    def runTest(self):
        sym = pypeg2.Symbol("hello")
        self.assertEqual(repr(sym), "Symbol('hello')")


class ListReprTestCase(unittest.TestCase):
    def runTest(self):
        lst = pypeg2.List(["a", "b"])
        self.assertIn("List(", repr(lst))

    def test_with_name(self):
        lst = pypeg2.List(["a"])
        lst.name = "mylist"
        self.assertIn("name=", repr(lst))


class ListEqTestCase(unittest.TestCase):
    def runTest(self):
        lst1 = pypeg2.List(["a", "b"])
        lst2 = pypeg2.List(["a", "b"])
        self.assertEqual(lst1, lst2)


class NamespaceReprTestCase(unittest.TestCase):
    def runTest(self):
        ns = pypeg2.Namespace()
        self.assertIn("Namespace(", repr(ns))

    def test_with_name(self):
        ns = pypeg2.Namespace()
        ns.name = "myns"
        self.assertIn("name=", repr(ns))


class EnumReprTestCase(unittest.TestCase):
    def runTest(self):
        e = pypeg2.Enum("a", "b", "c")
        self.assertIn("Enum(", repr(e))


# === Tests for Plain class ===


class PlainTestCase(unittest.TestCase):
    def runTest(self):
        p = pypeg2.Plain()
        self.assertIn("Plain()", repr(p))

    def test_with_name(self):
        p = pypeg2.Plain("myname")
        self.assertIn("name=", repr(p))


# === Tests for Namespace operations ===


class NamespaceOperationsTestCase(unittest.TestCase):
    def test_setitem(self):
        ns = pypeg2.Namespace()
        ns["key"] = pypeg2.Symbol("value")
        self.assertIn("key", ns)

    def test_delitem(self):
        ns = pypeg2.Namespace()
        ns["key"] = pypeg2.Symbol("value")
        del ns["key"]
        self.assertNotIn("key", ns)

    def test_len(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        ns["b"] = pypeg2.Symbol("b")
        self.assertEqual(len(ns), 2)

    def test_iter(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        keys = list(ns.keys())
        self.assertEqual(len(keys), 1)

    def test_values(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        vals = list(ns.values())
        self.assertEqual(len(vals), 1)

    def test_items(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        items = list(ns.items())
        self.assertEqual(len(items), 1)

    def test_clear(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        ns.clear()
        self.assertEqual(len(ns), 0)

    def test_copy(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        copied = ns.copy()
        self.assertIn(pypeg2.Symbol("a"), copied.values())


# === Tests for Enum operations ===


class EnumOperationsTestCase(unittest.TestCase):
    def test_creation(self):
        e = pypeg2.Enum("alpha", "beta")
        self.assertIn(pypeg2.Symbol("alpha"), e)
        self.assertIn(pypeg2.Symbol("beta"), e)

    def test_immutable(self):
        e = pypeg2.Enum("alpha")
        with self.assertRaises(ValueError):
            e["beta"] = pypeg2.Symbol("beta")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            pypeg2.Enum(123)


# === Tests for IKeyword (case-insensitive) ===


class IKeywordTestCase(unittest.TestCase):
    def test_parse_uppercase(self):
        parser = pypeg2.Parser()
        t, r = parser.parse("HELLO world", pypeg2.IK("hello"))
        # Parser skips whitespace, so remaining text is "world"
        self.assertEqual(t, "world")

    def test_parse_lowercase(self):
        parser = pypeg2.Parser()
        t, r = parser.parse("hello world", pypeg2.IK("HELLO"))
        self.assertEqual(t, "world")

    def test_parse_mixedcase(self):
        parser = pypeg2.Parser()
        t, r = parser.parse("HeLLo world", pypeg2.IK("hello"))
        self.assertEqual(t, "world")

    def test_parse_fail(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            parser.parse("world", pypeg2.IK("hello"))

    def test_parse_fail_no_match(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            parser.parse("123", pypeg2.IK("hello"))


# === Tests for Symbol with check_keywords ===


class SymbolCheckKeywordsTestCase(unittest.TestCase):
    def test_check_keywords(self):
        pypeg2.Keyword("reserved_word")
        old_check = pypeg2.Symbol.check_keywords
        try:
            pypeg2.Symbol.check_keywords = True
            with self.assertRaises(ValueError):
                pypeg2.Symbol("reserved_word")
        finally:
            pypeg2.Symbol.check_keywords = old_check

    def test_symbol_invalid_namespace(self):
        with self.assertRaises(TypeError):
            pypeg2.Symbol("mysym", namespace="not_a_namespace")


# === Tests for how_many function ===


class HowManyTestCase(unittest.TestCase):
    def test_none(self):
        self.assertEqual(pypeg2.how_many(None), 0)

    def test_int(self):
        self.assertEqual(pypeg2.how_many(5), 5)

    def test_string(self):
        self.assertEqual(pypeg2.how_many("hello"), 0)

    def test_symbol(self):
        self.assertEqual(pypeg2.how_many(pypeg2.Symbol), 1)

    def test_regex(self):
        self.assertEqual(pypeg2.how_many(re.compile(r"\w+")), 1)

    def test_tuple_single(self):
        self.assertEqual(pypeg2.how_many((pypeg2.Symbol,)), 1)

    def test_tuple_multiple(self):
        self.assertEqual(pypeg2.how_many((pypeg2.Symbol, pypeg2.Symbol)), 2)

    def test_list(self):
        self.assertEqual(pypeg2.how_many([pypeg2.Symbol, "x"]), 1)

    def test_function(self):
        self.assertEqual(pypeg2.how_many(lambda x, y: None), 0)

    def test_invalid_cardinality(self):
        with self.assertRaises(pypeg2.GrammarValueError):
            pypeg2.how_many((-10, "x"))


# === Tests for attributes function ===


class AttributesTestCase(unittest.TestCase):
    def test_single_attr(self):
        a = pypeg2.attr("name", pypeg2.Symbol)
        attrs = list(pypeg2.attributes(a))
        self.assertEqual(len(attrs), 1)

    def test_tuple_attrs(self):
        grammar = (pypeg2.attr("a", pypeg2.Symbol), pypeg2.attr("b", pypeg2.Symbol))
        attrs = list(pypeg2.attributes(grammar))
        self.assertEqual(len(attrs), 2)

    def test_invisible_attr(self):
        a = pypeg2.attr("_hidden", pypeg2.Symbol)
        attrs = list(pypeg2.attributes(a))
        self.assertEqual(len(attrs), 0)
        attrs = list(pypeg2.attributes(a, invisible=True))
        self.assertEqual(len(attrs), 1)


# === Tests for compose with indentation ===


class ComposeIndent(pypeg2.List):
    grammar = (
        "begin",
        pypeg2.endl,
        pypeg2.indent(pypeg2.some(pypeg2.word, pypeg2.endl)),
        "end",
    )


class ComposeIndentTestCase(unittest.TestCase):
    def runTest(self):
        x = ComposeIndent(["hello", "world"])
        t = pypeg2.compose(x)
        self.assertIn("begin", t)
        self.assertIn("end", t)
        self.assertIn("    hello", t)  # indented


# === Tests for contiguous and separated ===


class ContiguousTestCase(unittest.TestCase):
    def test_contiguous(self):
        grammar = pypeg2.contiguous(pypeg2.word, pypeg2.word)
        self.assertEqual(grammar[0], -4)

    def test_separated(self):
        grammar = pypeg2.separated(pypeg2.word, pypeg2.word)
        self.assertEqual(grammar[0], -5)


# === Tests for compose with Enum ===


class ComposeEnumTestCase(unittest.TestCase):
    def runTest(self):
        e = pypeg2.Enum("alpha", "beta")
        sym = pypeg2.Symbol("alpha")
        t = pypeg2.compose(sym, e)
        self.assertEqual(t, "alpha")

    def test_not_in_enum(self):
        e = pypeg2.Enum("alpha", "beta")
        sym = pypeg2.Symbol("gamma")
        with self.assertRaises(ValueError):
            pypeg2.compose(sym, e)


# === Tests for compose error cases ===


class ComposeErrorTestCase(unittest.TestCase):
    def test_regex_no_match(self):
        with self.assertRaises(ValueError):
            pypeg2.compose("hello", re.compile(r"\d+"))

    def test_not_instance(self):
        class MyClass:
            grammar = pypeg2.word

        with self.assertRaises(ValueError):
            pypeg2.compose(123, MyClass)


# === Tests for List initialization ===


class ListInitTestCase(unittest.TestCase):
    def test_string_init(self):
        lst = pypeg2.List("hello")
        self.assertIn("hello", lst)

    def test_invalid_init(self):
        with self.assertRaises(ValueError):
            pypeg2.List(123)


# === Tests for clear_memory ===


class ClearMemoryTestCase(unittest.TestCase):
    def test_clear_all(self):
        parser = pypeg2.Parser()
        parser.parse("hello", pypeg2.word)
        parser.clear_memory()
        self.assertEqual(parser._memory, {})

    def test_clear_specific(self):
        parser = pypeg2.Parser()
        parser.parse("hello", pypeg2.word)
        parser.clear_memory(pypeg2.word)
        # Should not raise


# === Tests for keep_feeble_things ===


class KeepFeebleThingsTestCase(unittest.TestCase):
    def test_keeps_whitespace(self):
        parser = pypeg2.Parser()
        parser.keep_feeble_things = True
        t, r = parser.parse("  hello", pypeg2.word)
        self.assertEqual(r, "hello")


# === Tests for RegEx class ===


class RegExMethodsTestCase(unittest.TestCase):
    def test_search(self):
        r = pypeg2.RegEx(r"\d+")
        m = r.search("abc123def")
        self.assertEqual(m.group(), "123")

    def test_findall(self):
        r = pypeg2.RegEx(r"\d+")
        matches = r.findall("a1b2c3")
        self.assertEqual(matches, ["1", "2", "3"])

    def test_sub(self):
        r = pypeg2.RegEx(r"\d+")
        result = r.sub("X", "a1b2c3")
        self.assertEqual(result, "aXbXcX")

    def test_split(self):
        r = pypeg2.RegEx(r"\d+")
        result = r.split("a1b2c3")
        self.assertEqual(result, ["a", "b", "c", ""])


# === Tests for Concat class ===


class ConcatTestCase(unittest.TestCase):
    def runTest(self):
        c = pypeg2.Concat(["a", "b", "c"])
        self.assertEqual(list(c), ["a", "b", "c"])


# === Tests for compose with options ===


class ComposeOptionsTestCase(unittest.TestCase):
    def test_compose_first_option(self):

        class MyClass(str):
            grammar = [re.compile(r"\d+"), pypeg2.word]

        x = MyClass("42")
        t = pypeg2.compose(x)
        self.assertEqual(t, "42")

    def test_compose_second_option(self):

        class MyClass(str):
            grammar = [re.compile(r"^[A-Z]+$"), pypeg2.word]

        x = MyClass("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")


# === Tests for Whitespace class ===


class WhitespaceTestCase(unittest.TestCase):
    def runTest(self):
        self.assertTrue(issubclass(pypeg2.Whitespace, str))
        self.assertEqual(pypeg2.Whitespace.grammar, pypeg2.whitespace)


# === Tests for endl and blank ===


class EndlBlankTestCase(unittest.TestCase):
    def test_endl(self):
        result = pypeg2.endl(None, None)
        self.assertEqual(result, "\n")

    def test_blank(self):
        result = pypeg2.blank(None, None)
        self.assertEqual(result, " ")


# === Tests for flag function ===


class FlagFunctionTestCase(unittest.TestCase):
    def test_flag_default(self):
        f = pypeg2.flag("myflag")
        self.assertEqual(f.name, "myflag")
        self.assertEqual(f.subtype, "Flag")

    def test_flag_custom_thing(self):
        f = pypeg2.flag("myflag", "MARK")
        self.assertEqual(f.thing, "MARK")


# === Tests for RegEx pattern ===


class RegExPatternTestCase(unittest.TestCase):
    def test_regex_match(self):
        r = re.compile(r"\d+")
        self.assertIsNotNone(r.match("123"))

    def test_regex_no_match(self):
        r = re.compile(r"\d+")
        self.assertIsNone(r.match("abc"))


# === Tests for Enum with kwargs ===


class EnumKwargsTestCase(unittest.TestCase):
    def test_enum_with_name(self):
        e = pypeg2.Enum("a", "b", name="myenum")
        self.assertEqual(e.name, "myenum")


# === Tests for List with tuple init ===


class ListTupleInitTestCase(unittest.TestCase):
    def test_list_with_tuple(self):
        lst = pypeg2.List(["item1", "item2"])
        self.assertIn("item1", lst)
        self.assertIn("item2", lst)


# === Tests for Parser with filename ===


class ParserFilenameTestCase(unittest.TestCase):
    def test_parse_with_filename(self):
        parser = pypeg2.Parser()
        t, r = parser.parse("hello", pypeg2.word, filename="test.txt")
        self.assertEqual(parser.filename, "test.txt")

    def test_syntax_error_includes_filename(self):
        parser = pypeg2.Parser()
        try:
            parser.parse("123", pypeg2.word, filename="test.txt")
        except SyntaxError as e:
            self.assertEqual(e.filename, "test.txt")


# === Tests for comments in parsing ===


class ParseWithCommentsTestCase(unittest.TestCase):
    def test_skip_comments_after_word(self):
        # Comment after parsing first word - remainder has the comment
        comment = re.compile(r"#[^\n]*")
        result = pypeg2.parse("# comment\nhello", pypeg2.word, comment=comment)
        self.assertEqual(result, "hello")


# === Tests for Symbol with Enum grammar ===


class SymbolEnumGrammarTestCase(unittest.TestCase):
    def test_symbol_with_enum_restriction(self):
        class Color(pypeg2.Symbol):
            grammar = pypeg2.Enum("red", "green", "blue")

        result = pypeg2.parse("red", Color)
        self.assertEqual(result, "red")

    def test_symbol_enum_restriction_fails(self):
        class Color(pypeg2.Symbol):
            grammar = pypeg2.Enum("red", "green", "blue")

        with self.assertRaises(SyntaxError):
            pypeg2.parse("yellow", Color)


# === Tests for Symbol grammar error ===


class SymbolBadGrammarTestCase(unittest.TestCase):
    def test_symbol_non_enum_grammar(self):
        class BadSymbol(pypeg2.Symbol):
            grammar = "not an enum"

        with self.assertRaises(pypeg2.GrammarValueError):
            pypeg2.parse("hello", BadSymbol)


# === Tests for thing.compose method ===


class ThingComposeMethodTestCase(unittest.TestCase):
    def test_thing_with_compose_method(self):
        class Greeting(pypeg2.List):
            grammar = pypeg2.word

            def compose(self, parser, attr_of=None):
                return "HELLO"

        g = Greeting(["hi"])
        result = pypeg2.compose(g)
        self.assertEqual(result, "HELLO")


# === Tests for compose with Symbol list grammar ===


class ComposeSymbolListTestCase(unittest.TestCase):
    def test_compose_list_without_grammar(self):
        lst = pypeg2.List([pypeg2.Symbol("a"), pypeg2.Symbol("b")])
        result = pypeg2.compose(lst)
        self.assertIn("a", result)
        self.assertIn("b", result)


# === Tests for parse with List returning thing ===


class ParseListClassTestCase(unittest.TestCase):
    def test_parse_list_class(self):
        class Items(pypeg2.List):
            grammar = pypeg2.some(pypeg2.word)

        result = pypeg2.parse("hello world", Items)
        self.assertIsInstance(result, Items)
        self.assertIn("hello", result)
        self.assertIn("world", result)


# === Tests for Namespace class parsing ===


class ParseNamespaceTestCase(unittest.TestCase):
    def test_parse_namespace_class(self):
        class Entry(str):
            grammar = pypeg2.name(), "=", pypeg2.word

        class Config(pypeg2.Namespace):
            grammar = pypeg2.some(Entry)

        result = pypeg2.parse("foo = bar baz = qux", Config)
        self.assertIsInstance(result, Config)
        self.assertIn("foo", result)
        self.assertIn("baz", result)


# === Tests for parse with attr returning single result ===


class ParseAttrSingleTestCase(unittest.TestCase):
    def test_parse_attr_single(self):
        class Item(str):
            grammar = pypeg2.attr("label", pypeg2.word)

        result = pypeg2.parse("hello", Item)
        self.assertEqual(result.label, "hello")


# === Tests for List kwargs ===


class ListKwargsTestCase(unittest.TestCase):
    def test_list_with_kwargs(self):
        lst = pypeg2.List(name="mylist")
        self.assertEqual(lst.name, "mylist")


# === Tests for Plain with kwargs ===


class PlainKwargsTestCase(unittest.TestCase):
    def test_plain_with_extra_kwargs(self):
        # Plain accepts **kwargs in tuple form
        p = pypeg2.Plain(name="myplain")
        self.assertEqual(p.name, "myplain")


# === Tests for clear_memory with non-existent thing ===


class ClearMemoryNonExistentTestCase(unittest.TestCase):
    def test_clear_nonexistent_thing(self):
        parser = pypeg2.Parser()
        # Parsing something to populate memory
        parser.parse("hello", pypeg2.word)
        # Clear for a thing that was never parsed - should not raise
        parser.clear_memory(str)


# === Tests for grammar function in how_many ===


class HowManyFunctionTestCase(unittest.TestCase):
    def test_function_returns_zero(self):
        def my_func():
            pass

        self.assertEqual(pypeg2.how_many(my_func), 0)


# === Tests for cardinality values in how_many ===


class HowManyCardinalityTestCase(unittest.TestCase):
    def test_omit_cardinality(self):
        # -6 is omit() cardinality
        self.assertEqual(pypeg2.how_many((-6, pypeg2.word)), 0)

    def test_negative_five(self):
        # -5 is separated()
        self.assertEqual(pypeg2.how_many((-5, pypeg2.word)), 1)

    def test_negative_four(self):
        # -4 is contiguous()
        self.assertEqual(pypeg2.how_many((-4, pypeg2.word)), 1)

    def test_zero_cardinality(self):
        # 0 is optional()
        self.assertEqual(pypeg2.how_many((0, pypeg2.word)), 1)


# === Tests for compose with autoblank ===


class ComposeAutoblankTestCase(unittest.TestCase):
    def test_compose_no_autoblank(self):
        class Words(pypeg2.List):
            grammar = pypeg2.word, pypeg2.word

        w = Words(["hello", "world"])
        result = pypeg2.compose(w, autoblank=False)
        self.assertEqual(result, "helloworld")


# === Tests for contiguous marker ===


class ContiguousMarkerTestCase(unittest.TestCase):
    def test_contiguous_marker(self):
        # Test the contiguous tuple structure
        c = pypeg2.contiguous()
        self.assertEqual(c[0], -4)


# === Tests for syntax error with newlines ===


class SyntaxErrorNewlineTestCase(unittest.TestCase):
    def test_syntax_error_multiline(self):
        try:
            pypeg2.parse("line1\nline2\n123invalid", pypeg2.word)
        except SyntaxError as e:
            self.assertIsNotNone(e.lineno)


# === Tests for _issubclass with non-class ===


class IsSubclassTestCase(unittest.TestCase):
    def test_non_class(self):
        self.assertFalse(pypeg2._issubclass("not a class", str))

    def test_with_class(self):
        self.assertTrue(pypeg2._issubclass(pypeg2.Symbol, str))


# === Tests for compose with list options ===


class ComposeListOptionsTestCase(unittest.TestCase):
    def test_compose_list_first_match(self):
        grammar = [re.compile(r"\d+"), pypeg2.word]
        result = pypeg2.compose("hello", grammar)
        self.assertEqual(result, "hello")

    def test_compose_list_second_match(self):
        grammar = [re.compile(r"[A-Z]+"), pypeg2.word]
        result = pypeg2.compose("hello", grammar)
        self.assertEqual(result, "hello")


# === Tests for parse with options fallback ===


class ParseOptionsTestCase(unittest.TestCase):
    def test_parse_options_fallback(self):
        class First:
            grammar = re.compile(r"\d+")

        result = pypeg2.parse("hello", [First, pypeg2.word])
        self.assertEqual(result, "hello")


# === Tests for Namespace repr without name ===


class NamespaceReprNoNameTestCase(unittest.TestCase):
    def test_repr_no_name(self):
        ns = pypeg2.Namespace()
        ns["a"] = pypeg2.Symbol("a")
        r = repr(ns)
        self.assertIn("Namespace", r)
        self.assertNotIn("name=", r)


# === Tests for compose returning already matching type ===


class ParseReturnsMatchingTypeTestCase(unittest.TestCase):
    def test_parse_returns_same_type(self):
        class MyList(pypeg2.List):
            grammar = pypeg2.word

        result = pypeg2.parse("hello", MyList)
        self.assertIsInstance(result, MyList)


# === Tests for Symbol with grammar None ===


class SymbolNoneGrammarTestCase(unittest.TestCase):
    def test_symbol_with_none_grammar(self):
        class MySymbol(pypeg2.Symbol):
            grammar = None

        result = pypeg2.parse("hello", MySymbol)
        self.assertEqual(result, "hello")


# === Tests for compose with None grammar ===


class ComposeNoneGrammarTestCase(unittest.TestCase):
    def test_compose_none_grammar(self):
        class Item:
            grammar = None

        i = Item()
        result = pypeg2.compose(i)
        self.assertEqual(result, "")


# === Tests for compose with Keyword ===


class ComposeKeywordTestCase(unittest.TestCase):
    def test_compose_keyword_grammar(self):
        kw = pypeg2.Keyword("hello")
        result = pypeg2.compose("x", kw)
        self.assertEqual(result, "hello")


# === Tests for compose with Enum containing Keyword ===


class ComposeEnumKeywordTestCase(unittest.TestCase):
    def test_compose_enum_with_keyword(self):
        kw = pypeg2.Keyword("hello")
        e = pypeg2.Enum(kw)
        result = pypeg2.compose(kw, e)
        self.assertEqual(result, "hello")


# === Tests for compose with Flag ===


class ComposeFlagTestCase(unittest.TestCase):
    def test_compose_flag_true(self):
        class Item:
            grammar = pypeg2.flag("active", "ACTIVE")

        i = Item()
        i.active = True
        result = pypeg2.compose(i)
        self.assertEqual(result, "ACTIVE")

    def test_compose_flag_false(self):
        class Item:
            grammar = pypeg2.flag("active", "ACTIVE")

        i = Item()
        i.active = False
        result = pypeg2.compose(i)
        self.assertEqual(result, "")


# === Tests for compose with attr ===


class ComposeAttrTestCase(unittest.TestCase):
    def test_compose_attr(self):
        class Item:
            grammar = pypeg2.attr("label", pypeg2.word)

        i = Item()
        i.label = "hello"
        result = pypeg2.compose(i)
        self.assertEqual(result, "hello")


# === Tests for compose with indent ===


class ComposeIndentFunctionTestCase(unittest.TestCase):
    def test_indent_function(self):
        # Test indent returns the correct cardinality tuple
        i = pypeg2.indent()
        self.assertEqual(i[0], -3)


# === Tests for compose with endl ===


class ComposeEndlTestCase(unittest.TestCase):
    def test_compose_with_endl(self):
        class Lines(pypeg2.List):
            grammar = pypeg2.word, pypeg2.endl, pypeg2.word

        lines = Lines(["hello", "world"])
        result = pypeg2.compose(lines)
        self.assertIn("\n", result)


# === Tests for compose with blank ===


class ComposeBlankTestCase(unittest.TestCase):
    def test_compose_with_blank(self):
        class Spaced:
            grammar = pypeg2.word, pypeg2.blank, pypeg2.word

        s = Spaced()
        result = pypeg2.compose(["hello", "world"], (pypeg2.word, pypeg2.blank, pypeg2.word))
        self.assertIn(" ", result)


# === Tests for compose with function grammar ===


class ComposeFunctionGrammarTestCase(unittest.TestCase):
    def test_compose_function_grammar(self):
        def my_grammar(thing, parser):
            return pypeg2.word

        result = pypeg2.compose("hello", my_grammar)
        self.assertEqual(result, "hello")


# === Tests for class with polish method ===


class ClassPolishTestCase(unittest.TestCase):
    def test_class_with_polish(self):
        class Item(str):
            grammar = pypeg2.word

            def polish(self):
                self.polished = True

        result = pypeg2.parse("hello", Item)
        self.assertTrue(result.polished)


# === Tests for class with multiple attrs ===


class ClassMultipleAttrsTestCase(unittest.TestCase):
    def test_class_with_multiple_attrs(self):
        class Item:
            grammar = pypeg2.attr("first", pypeg2.word), pypeg2.attr("second", pypeg2.word)

        result = pypeg2.parse("hello world", Item)
        self.assertEqual(result.first, "hello")
        self.assertEqual(result.second, "world")


# === Tests for List class with grammar returning list ===


class ListClassWithGrammarTestCase(unittest.TestCase):
    def test_list_with_grammar_returning_list(self):
        class Items(pypeg2.List):
            grammar = pypeg2.some(pypeg2.word)

        result = pypeg2.parse("one two three", Items)
        self.assertEqual(len(result), 3)


# === Tests for compose with int grammar ===


class ComposeIntGrammarTestCase(unittest.TestCase):
    def test_compose_int_grammar(self):
        result = pypeg2.compose("x", 5)
        self.assertEqual(result, "5")


# === Tests for omit in grammar ===


class OmitTestCase(unittest.TestCase):
    def test_omit_in_parse(self):
        grammar = (pypeg2.omit(pypeg2.Keyword("start")), pypeg2.word)
        result = pypeg2.parse("start hello", grammar)
        self.assertEqual(result, "hello")


# === Tests for RegEx class (public wrapper) ===


class RegExClassTestCase(unittest.TestCase):
    def test_regex_class(self):
        r = pypeg2.RegEx(r"\d+", name="number")
        self.assertEqual(r.name, "number")
        self.assertEqual(r.pattern, r"\d+")


if __name__ == "__main__":
    unittest.main()
