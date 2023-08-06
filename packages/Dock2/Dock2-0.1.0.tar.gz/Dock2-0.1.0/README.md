# Dock2

This is a simple wrapper for interacting with h2cs drivers (HTTP2 ClearText)

## Installation

Run the following to install:

```python
pip install Dock2
```

You need to download the h2cs driver in order for this to work.

Supported Drivers

| Driver | Download                                                                                  |
| ------ | ----------------------------------------------------------------------------------------- |
| H2CS   | [Download](https://raw.githubusercontent.com/BishopFox/h2csmuggler/master/h2csmuggler.py) |

## Usage

```python
import Dock2

#  Upgrade function
result = Dock2.upgrade('www.example.com', 'driver.py')
print(result)

# Do anything else, pass arguments h2cs returns byte string
 result =  Dock2.cmd('-x https://edgeserver -i dirs.txt http://localhost/', 'driver')
 print(result)
```

# Developing Dock2

To install Dock2, along with all the tools you need to develop and run tests,
run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```
