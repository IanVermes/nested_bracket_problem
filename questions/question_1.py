#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Question 1: parse a string of brackets, validating its structure"""

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


def solution(string: str) -> int:
    """Parse a structured string & return 0 if the string is properly nested, otherwise 1."""
    return None
