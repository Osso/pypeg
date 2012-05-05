import unittest
import re, sys
import pyPEG2, xmlast2
import lxml

class Text(str): pass

class Another:
    grammar = pyPEG2.name(), "=", pyPEG2.attr("value")

class Something(pyPEG2.List):
    grammar = pyPEG2.name(), pyPEG2.some(Another), Text

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
        t = Text("hello, world")
        s.append(t)

        root = xmlast2.create_tree(s)

        self.assertEqual(root.tag, "Something")
        self.assertEqual(root.attrib["name"], "hello")
        
        self.assertEqual(xmlast2.etree.tostring(root), b'<Something name="hello"><Another name="bla" value="blub"/><Another name="foo" value="bar"/>hello, world</Something>')

class SomethingElse(pyPEG2.Namespace):
    grammar = pyPEG2.name(), pyPEG2.some(Another)

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

        root = xmlast2.create_tree(s)

        self.assertEqual(root.tag, "SomethingElse")
        self.assertEqual(root.attrib["name"], "hello")
        
        self.assertTrue(
            xmlast2.etree.tostring(root) == b'<SomethingElse name="hello"><Another name="bla" value="blub"/><Another name="foo" value="bar"/></SomethingElse>' or xmlast2.etree.tostring(root) == b'<SomethingElse name="hello"><Another name="bla" value="blub" /><Another name="foo" value="bar" /></SomethingElse>'
        )

class XML2ThingTestCase(unittest.TestCase): pass

if __name__ == '__main__':
    unittest.main()
