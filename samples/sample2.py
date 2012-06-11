"""
Ini file sample (see end of file for the content of the ini file)

To parse an ini file we use the grammar below. Comments in ini files are
starting with a semicolon ";".

>>> ini_file = parse(ini_file_text, IniFile, comment=(";", restline))

Because IniFile and Section are Namespaces, we can access their content by
name.

>>> print("found: " + repr(ini_file["Number 1"]["that"]))
found: ...'something else'

pyPEG is measuring the position of each object in the input text with a
tuple (line_number, offset).

>>> ini_file["Number 1"]["that"].position_in_text
(3, 26)
>>> ini_file["Number 2"].position_in_text
(6, 85)

pyPEG can also do the reverse job, composing a text of an object tree.

>>> ini_file["Number 1"]["that"] = Key("new one")
>>> ini_file["Number 3"] = Section()
>>> print(compose(ini_file))
[Number 1]
this=something
that=new one
[Number 2]
once=anything
twice=goes
[Number 3]
...

pyPEG contains an XML backend, too:

>>> from pypeg2.xmlast import thing2xml
>>> print(thing2xml(ini_file, pretty=True).decode())
<IniFile>
  <Section name="Number 1">
    <Key name="this">something</Key>
    <Key name="that">new one</Key>
  </Section>
  <Section name="Number 2">
    <Key name="once">anything</Key>
    <Key name="twice">goes</Key>
  </Section>
  <Section name="Number 3"/>
</IniFile>
...

In this sample the tree contains named objects only. Then we can output object
names as tag names. Spaces in names will be translated into underscores.

>>> print(thing2xml(ini_file, pretty=True, object_names=True).decode())
<IniFile>
  <Number_1>
    <this>something</this>
    <that>new one</that>
  </Number_1>
  <Number_2>
    <once>anything</once>
    <twice>goes</twice>
  </Number_2>
  <Number_3/>
</IniFile>
...
"""

from __future__ import unicode_literals, print_function
from pypeg2 import *
import re

# ini file parser

# symbols in ini files can include spaces
Symbol.regex = re.compile(r"[\w\s]+")

class Key(str):
    grammar = name(), "=", restline, endl

class Section(Namespace):
    grammar = "[", name(), "]", endl, maybe_some(Key)

class IniFile(Namespace):
    grammar = some(Section)

if __name__ == "__main__":
    ini_file_text = """[Number 1]
this=something
that=something else

; now for something even more useless
[Number 2]
once=anything
twice=goes
"""
    import doctest
    doctest.testmod(optionflags=(doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE))
