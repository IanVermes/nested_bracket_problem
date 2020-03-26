#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Question 1: parse a string of brackets, validating its structure"""

from queue import LifoQueue
import typing as t

import enum


_ENCODED_BRACKET_GROUP_MAP: t.Dict[str, int] = {
    "(": 1,
    ")": 1,
    "[": 2,
    "]": 2,
    "{": 3,
    "}": 3,
}
_ENCODED_BRACKET_STATE_MAP: t.Dict[str, int] = {
    # 1 - OPEN, 2 - CLOSED
    "(": 1,
    "{": 1,
    "[": 1,
    "]": 2,
    ")": 2,
    "}": 2,
}


class BracketGroup(enum.Enum):
    UNKNOWN = 0
    ROUND = 1
    SQUARE = 2
    CURLY = 3

    @classmethod
    def from_char(cls, char: str):
        """Get the BracketGroup enum corresponding to the char."""
        init_val: int = _ENCODED_BRACKET_GROUP_MAP.get(char, 0)
        return cls(init_val)


class BracketState(enum.Enum):
    OPEN = 1
    CLOSED = 2

    @classmethod
    def from_char(cls, char: str):
        """Get the BracketState enum corresponding to the char."""
        init_val: int = _ENCODED_BRACKET_STATE_MAP[char]
        return cls(init_val)


def is_odd(string: str) -> bool:
    return len(string) % 2 == 1


def solution(string: str) -> int:
    """Parse a structured string & return 0 if the string is properly nested, otherwise 1."""

    if is_odd(string):  # A structured string should have an even number of brackets.
        return 1

    queue: LifoQueue[BracketGroup] = LifoQueue(maxsize=len(string))
    for bracket_char in string:
        bracket_group = BracketGroup.from_char(bracket_char)
        if bracket_group is BracketGroup.UNKNOWN:
            result = 1
            break
        bracket_state = BracketState.from_char(bracket_char)

        # We don't need to allow for waiting and timeouts as the queue is a private
        # property of this function.
        if bracket_state is BracketState.OPEN:
            queue.put_nowait(bracket_group)
        elif bracket_state is BracketState.CLOSED:
            bracket_group_from_q = queue.get_nowait()
            if bracket_group_from_q == bracket_group:
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
