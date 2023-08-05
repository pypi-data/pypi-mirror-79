# fdbk_mongodb_plugin

[![Build Status](https://travis-ci.org/kangasta/fdbk_mongodb_plugin.svg?branch=master)](https://travis-ci.org/kangasta/fdbk_mongodb_plugin)

MongoDB wrapper for fdbk.

## Installation

Run:

```bash
pip install fdbk_mongodb_plugin
```

to install from [PyPI](https://pypi.org/project/fdbk_mongodb_plugin/) or download this repository and run

```bash
python setup.py install
```

to install from sources.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle fdbk_mongodb_plugin
autopep8 -aaar --in-place fdbk_mongodb_plugin
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance fdbk_mongodb_plugin
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source fdbk_mongodb_plugin/ -m unittest discover -s tst/
coverage report -m
```
