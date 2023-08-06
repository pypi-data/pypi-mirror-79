# polf

[![PyPI][pypi-image]][pypi-link]
[![PyPI Python versions][pypi-versions-image]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]
[![Coverage status][coverage-image]][coverage-link]
[![Documentation status][doc-image]][doc-link]

Simple library written with the Python C API to calculate points on lines.
It does not perform any checks on the passed data, but rather follows the
GIGO processing pattern.

I have written it with the main purpose of learning, but it may be useful in
some situation or it can serve as a reference to get you started in the
Python C API. If it has been useful to you, do not hesitate to leave a star.

## Install

```
pip install polf
```

## Useful links

- [Documentation on ReadTheDocs][doc-link]
- [Issue tracker][issue-tracker-link]

## Contributing (Linux)

First, create a virtual environment and initialize it with:

```
python3 -m virtualenv venv
source venv/bin/activate
```

I usually run these commands to develop:

- Rebuild source code and build documentation: `make docs`
- Rebuild source code and run tests: `make tests`
- Rebuild source code and lint: `make lint`

[doc-link]: https://polf.readthedocs.io
[issue-tracker-link]: https://github.com/mondeja/cpolf/issues

