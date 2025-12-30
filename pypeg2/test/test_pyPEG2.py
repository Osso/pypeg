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


if __name__ == "__main__":
    unittest.main()
