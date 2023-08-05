# raise_assert

A short way to check for conditions and raise if it fails, in Python.

## Motivation

I get annoyed to need writing all the time variations around:

```python
if not isinstance(my_bool, bool):
    raise ValueError("my_bool should be a bool")
```

And as pointed several places on the net, ```assert``` cannot really be trusted for performing this sort of checks, as asserts can be disabled with the ```-O``` flag, see for example: https://stackoverflow.com/questions/1273211/disable-assertions-in-python .

## Solution

The raise_assert package contains a single function that allows writing:

```python
from raise_assert import ras

ras(isinstance(my_bool, bool))
```

or, if you want an error message (but this is usually not needed, as the stack trace is usually explicit enough):

```python
from raise_assert import ras

ras(isinstance(my_bool, bool), "my_bool must be a bool")
```

## Installation

```pip install raise_assert```

## Why ras?

The word ```ras``` is shortland for both raise_assert and 'rien à signaler', 'nothing to signal' in French.
