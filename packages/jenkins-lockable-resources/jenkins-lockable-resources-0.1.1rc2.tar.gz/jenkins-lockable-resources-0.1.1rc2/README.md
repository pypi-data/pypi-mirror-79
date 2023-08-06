# Jenkins Lockable Resources Plugin Library

![Pipeline Status](https://gitlab.com/alexandre-perrin1/jenkins-lockable-resources/badges/master/pipeline.svg)

## About the library

This library and CLI utility was developped to access and control
[Jenkins Lockable-Resources plugin](https://plugins.jenkins.io/lockable-resources/)
because the current version of the plugin does not provide REST APIs.

## Prerequisite

As python2 is on its way to be deprecated, this tool was designed for python3
only.

The command line interface has been written with click package.
An optionnal `click-completion` package can also be installed in order to give
shell completion feature.

## Install

The tool may be installed from sources with pip package manager from PyPi.

```
pip3 install jenkins-lockable-resources
```

## Testing

This package is tested using `pytest` framework. See `requirements-test.txt` for the
list of required packages.

Install requirements for testing:

```
pip3 install -r requirements-test.txt
```

The tests are held in `tests` directory.
Simply execute pytest from command line:

```
pytest tests
```

## Development

For development, install as editable:

```
pip3 install -e .
```

## License

The MIT License (MIT): Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.