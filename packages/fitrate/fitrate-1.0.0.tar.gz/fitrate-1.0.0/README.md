<p align="center">
  <img width="420px" src="https://raw.githubusercontent.com/suzukey/fitrate/main/docs/img/fitrate.png" alt='fitrate'>
</p>

<p align="center">
  <em>Calculate the length of the sides that fit into the limited volume</em>
</p>

<p align="center">
  <a href="https://github.com/suzukey/fitrate/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/suzukey/fitrate/workflows/Test/badge.svg" alt="Test">
  </a>

  <a href="https://codecov.io/gh/suzukey/fitrate" target="_blank">
    <img src="https://img.shields.io/codecov/c/gh/suzukey/fitrate" alt="Coverage">
  </a>

  <a href="https://pypi.org/project/fitrate/" target="_blank">
    <img src="https://img.shields.io/pypi/v/fitrate?color=blue" alt="Package version">
  </a>
</p>

---

**Documentation**:

**Demo**:

---

# fitrate

## Requirements

Python 3.6+

## Installation

```shell
$ pip3 install fitrate
```

## Example

```python
from fitrate import contain

print(contain((200, 200), 60000))
# (244, 244)

print(contain((400, 300), 60000))
# (282, 212)

# -----------

from fitrate import scale-down

print(scale-down((200, 200), 60000))
# (200, 200)

print(scale-down((400, 300), 60000))
# (282, 212)
```

<p align="center">&mdash; 🎞️ &mdash;</p>

<p align="center">
  <i>fitrate is licensed under the terms of the <a href="https://github.com/suzukey/fitrate/blob/main/LICENSE">MIT license</a>.</i>
</p>
