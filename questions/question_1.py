#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Question 1: parse a string of brackets, validating its structure"""

from queue import LifoQueue
import typing as t

import enum


_ENCODED_BRACKET_MAP: t.Dict[str, int] = {
    "(": 1,
    ")": 1,
    "[": 2,
    "]": 2,
    "{": 3,
    "}": 3,
}
_ENCODED_BRACKET_TYPE_MAP: t.Dict[str, int] = {
    "(": 1,
    "{": 1,
    "[": 1,
    "]": 2,
    ")": 2,
    "}": 2,
}


class Bracket(enum.Enum):
    ROUND = 1
    SQUARE = 2
    CURLY = 3

    @classmethod
    def from_char(cls, char: str):
        """Get the Bracket enum corresponding to the char."""
        init_val: int = _ENCODED_BRACKET_MAP[char]
        return cls(init_val)


class BracketType(enum.Enum):
    OPEN = 1
    CLOSED = 2

    @classmethod
    def from_char(cls, char: str):
        """Get the BracketType enum corresponding to the char."""
        init_val: int = _ENCODED_BRACKET_TYPE_MAP[char]
        return cls(init_val)


def is_odd(string: str) -> bool:
    return len(string) % 2 == 1


def solution(string: str) -> int:
    """Parse a structured string & return 0 if the string is properly nested, otherwise 1."""

    if is_odd(string):  # A structured string should have an even number of brackets.
        return 1

    queue: LifoQueue[Bracket] = LifoQueue(maxsize=len(string))
    for bracket_char in string:
        bracket_from_str = Bracket.from_char(bracket_char)
        bracket_type = BracketType.from_char(bracket_char)

        # We don't need to allow for waiting and timeouts as the queue is a private
        # property of this function.
        if bracket_type is BracketType.OPEN:
            queue.put_nowait(bracket_from_str)
        elif bracket_type is BracketType.CLOSED:
            bracket_from_q = queue.get_nowait()
            if bracket_from_q == bracket_from_str:
                continue
            else:
                result = 1
                break
    else:
        # If the string is well structured then the queue will have emptied.
        if queue.empty():
            result = 0
        else:
            result = 1

    return result
