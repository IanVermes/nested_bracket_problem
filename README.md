# informetis_tech_exam

Parse a string with nested brackets.

Tested on Python 3.8.2

The function `solution` is found in `questions/question_1.py`

## Setup

`questions/question_1.py` just uses the standard library, no other dependencies
necessary.

Running the tests does need `pytest` and `pyyaml` dependencies. This is most
easily done by using [Poetry](https://python-poetry.org/docs/#installation)

## Setup my dev environment

1) Install `pyenv` & `poetry`
2) Clone repo and cd into the repo
3) `pyenv install 3.8.2`, unless you already have a Python 3.8 runtime environment
4) `pyenv local 3.8.2` to set repo env to Python 3.8
5) `poetry shell` will create (and activate) a Poetry managed virtual env but
   `python -m venv .venv && .venv/bin/activate` will do much the same
6) `poetry install` will install the dependencies to the environment
7) Some times after a clean installation the shell needs to be restarted if the
   commands `pytest` or `mypy` cannot be found. Or you can do `python -m
   pytest`.


## Functional testing

I used the script `build_nested_strings.py` to create a battery of valid and
invalid test-strings. These are found in `big_strings.yaml` & `strings.yaml`.
They could be all in one file but it makes it difficult to browse the smaller
(more interesting) strings.

## Static typing

Functions and classes are type hinted. `mypy` was used to type check (hence no
type checking related unit tests).

## Code style

`black` was used to auto-format the repo. I didn't use any special linting.


## Notes about exercise

* Calls of `len(string)` are O(1)
* I call `queue.empty()` for every character in the iteration - this seems to be
  an O(1) operation after some testing
  ```python
  In [50]: %timeit lifo_q_small.empty()  # queue is full and has size 1_000
  582 ns ± 1.88 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

  In [51]: %timeit lifo_q_big.empty()  # queue is full and has size 10_000_000
  606 ns ± 2.64 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
  ```
  I also considered catching `queue.Empty` exceptions instead of checking if the
  queue was empty all the time. I decided that it was less readable to split up
  the conditional logic (`if/elif/else`) into both a `try/except` block and an
  `if/elif` block. Also there was little change in performance when parsing big
  strings (though I didn't profile this).
