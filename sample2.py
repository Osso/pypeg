"""
Ini file sample (see end of file for the content of the ini file)

To parse an ini file we use the grammar below. Comments in ini files are
starting with a semicolon ";".

>>> ini_file = parse(ini_file_text, IniFile, comment=(";", restline))

Because IniFile and Section are Namespaces, we can access their content by
name.

>>> ini_file["Number 1"]["that"]
'something else'

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
<BLANKLINE>
"""

from pyPEG2 import *
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
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
