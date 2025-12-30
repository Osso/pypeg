# pyPEG 2

[![CI](https://github.com/osso/pypeg/actions/workflows/test.yml/badge.svg)](https://github.com/osso/pypeg/actions/workflows/test.yml)

Python is a nice scripting language. It even gives you access to its own parser
and compiler. It also gives you access to different other parsers for special
purposes like XML and string templates.

But sometimes you may want to have your own parser. This is what's pyPEG for.
And pyPEG supports Unicode.

## Installation

```bash
pip install git+https://github.com/osso/pypeg.git
```

Or for development:

```bash
git clone https://github.com/osso/pypeg.git
cd pypeg
uv sync
```

## Requirements

- Python 3.12+
- lxml (optional, for XML AST support)

## Documentation

See http://fdik.org/pyPEG2 for the original documentation.

## License

GNU General Public License v2 (GPLv2)
