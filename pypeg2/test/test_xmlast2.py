import unittest
import re, sys
import pypeg2, pypeg2.xmlast2

class Another:
    grammar = pypeg2.name(), "=", pypeg2.attr("value")

class Something(pypeg2.List):
    grammar = pypeg2.name(), pypeg2.some(Another), str

class Thing2etreeTestCase1(unittest.TestCase):
    def runTest(self):
        s = Something()
        s.name = "hello"
        a1 = Another()
        a1.name = "bla"
        a1.value = "blub"
        a2 = Another()
        a2.name = "foo"
        a2.value = "bar"
        s.append(a1)
        s.append(a2)
        s.append("hello, world")

        root = pypeg2.xmlast2.create_tree(s)

        self.assertEqual(root.tag, "Something")
        self.assertEqual(root.attrib["name"], "hello")
 
        try:
            import lxml
        except ImportError:
            self.assertEqual(pypeg2.xmlast2.etree.tostring(root), b'<Something name="hello"><Another name="bla" value="blub" /><Another name="foo" value="bar" />hello, world</Something>')
        else:
            self.assertEqual(pypeg2.xmlast2.etree.tostring(root), b'<Something name="hello"><Another name="bla" value="blub"/><Another name="foo" value="bar"/>hello, world</Something>')

class SomethingElse(pypeg2.Namespace):
    grammar = pypeg2.name(), pypeg2.some(Another)

class Thing2etreeTestCase2(unittest.TestCase):
    def runTest(self):
        s = SomethingElse()
        s.name = "hello"
        a1 = Another()
        a1.name = "bla"
        a1.value = "blub"
        a2 = Another()
        a2.name = "foo"
        a2.value = "bar"
        s[a1.name] = a1
        s[a2.name] = a2

        root = pypeg2.xmlast2.create_tree(s)

        self.assertEqual(root.tag, "SomethingElse")
        self.assertEqual(root.attrib["name"], "hello")
 
        try:
            import lxml
        except ImportError:
            self.assertEqual(pypeg2.xmlast2.etree.tostring(root), b'<SomethingElse name="hello"><Another name="bla" value="blub" /><Another name="foo" value="bar" /></SomethingElse>')
        else:
            self.assertEqual(pypeg2.xmlast2.etree.tostring(root), b'<SomethingElse name="hello"><Another name="bla" value="blub"/><Another name="foo" value="bar"/></SomethingElse>')

class XML2ThingTestCase(unittest.TestCase): pass

if __name__ == '__main__':
    unittest.main()
