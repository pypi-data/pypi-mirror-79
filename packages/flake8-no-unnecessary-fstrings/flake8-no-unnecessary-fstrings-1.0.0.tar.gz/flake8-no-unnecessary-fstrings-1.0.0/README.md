flake8-no-unnecessary-fstrings
==============================

[![PyPI](https://img.shields.io/pypi/v/flake8-no-unnecessary-fstrings.svg)](https://pypi.python.org/pypi/flake8-no-unnecessary-fstrings)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
![Upload Python Package](https://github.com/NorthIsUp/flake8-no-unecessary-fstrings/workflows/Upload%20Python%20Package/badge.svg)

A [flake8](https://flake8.readthedocs.io/en/latest/index.html>) plugin to detect
f-strings that don't actually do any interpolation.

Installation
------------

Install from ``pip`` with:

```sh
python -m pip install flake8-no-unnecessary-fstrings
```

Python 3.6+ supported.

When installed it will automatically be run as part of ``flake8``; you can
check it is being picked up with:

```sh
$ flake8 --version
3.7.9 (flake8-no-unnecessary-fstrings: 1.0.0, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.8.0 on Darwin
```

Rules
-----
- **NUF001**: No unecessary f-strings
