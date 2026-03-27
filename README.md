<h1 align="center">
Chriesibaum's JEP106 Tool Box

[![pypi](https://img.shields.io/pypi/v/cb_jep106.svg)](https://pypi.org/project/cb_jep106/)
[![python](https://img.shields.io/pypi/pyversions/cb_jep106.svg)](https://pypi.org/project/cb_jep106/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cb_jep106)](https://pypi.org/project/cb_jep106/)
[![GitHub stars](https://img.shields.io/github/stars/chriesibaum/cb_jep106.svg)](https://github.com/smarie/python-genbadge/stargazers)
<br>
[![Tests Status](https://raw.githubusercontent.com/chriesibaum/cb_jep106/refs/heads/main/doc/tests-badge.svg)]()
[![Coverage Status](https://raw.githubusercontent.com/chriesibaum/cb_jep106/refs/heads/main/doc/coverage-badge.svg)]()

</h1>

A python library and toolbox that parses the Standard Manufacturer’s
Identification Code (JEP106) and converts the content into a machine-readable file like a CSV or JSON.

The data can also be easily used in Python projects by utilizing the Python class Jep106Db()

It is entirely written in Python.

# Installation
```bash
pip install -e .
```

# Example
```python
from cb_jep106 import Jep106Db

jep106 = Jep106Db()
print(jep106.get_manufacturer(0x001))
print(jep106.get_manufacturer(0x020))
print(jep106.get_manufacturer(0x23b))
```

This outputs the following text:
```bash
AMD
STMicroelectronics
ARM Ltd
```

# CLI Usage
```bash
cb_jep106_converter -i <JEP106xx.pdf> -j <JEP106xx.json>
```

```bash
cb_jep106_converter --help
usage: cb_jep106_converter [-h] [-i <JEP106xx.pdf>] [-c <csv file>] [-j <json file>]

Decode the Standard Manufacturer’s Identification Code PDF file (JEP106xx.pdf)
and generate machine readable output like a CSV or JSON file.

Note:
As the JEP106xx.pdf is not free to use, it is not included in the repository but
can be used by downloading the JEP106xx.pdf from JEDEC and running this script locally.
At the time of writing, the actual JEP106BN.pdf can be found at
https://www.jedec.org/standards-documents/docs/jep-106ab.

Finally, have fun with the JEP106 data! :)

options:
  -h, --help            show this help message and exit
  -i <JEP106xx.pdf>, --pdf <JEP106xx.pdf>
                        Path to input JEP106 PDF file (default: ./JEP106/JEP106BN.pdf)
  -c <csv file>, --csv <csv file>
                        Path to output CSV file
  -j <json file>, --json <json file>
                        Path to output JSON file

  At least one output must be provided: `-c/--csv` or `-j/--json`.
```


