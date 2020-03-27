#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Create valid and invalid nested strings. Persist them in a *.yaml file"""
import random
import typing as t

import yaml


import itertools

t_BracketPairs = t.List[t.Tuple[str, str]]


def __make_invalid_bracket_pairs(pairs: t_BracketPairs) -> t_BracketPairs:
    """Take the valid paired brackets and return invalid pairs.

    Most Python functions should be defined after the classes, but this function is used
    to setup the module, as it would be beneficial to pick from the cached
    INVALID_BRACKET_PAIRS rather than calculate a new mismatched pair everytime a
    mistake is needed.
    """
    opens: t.List[str] = []
    closes: t.List[str] = []
    valid_pairs = set(pairs)
    for open_br, close_br in valid_pairs:
        opens.append(open_br)
        closes.append(close_br)
    all_bracket_pairs = set(itertools.product(opens, closes))
    # Discard the valid pairs
    invalid_pairs = all_bracket_pairs - valid_pairs
    return list(invalid_pairs)


__BRACKETS = "{}[]()"
VALID_BRACKET_PAIRS: t_BracketPairs = [
    (br_open, br_close) for br_open, br_close in zip(__BRACKETS[::2], __BRACKETS[1::2])
]
INVALID_BRACKET_PAIRS: t_BracketPairs = __make_invalid_bracket_pairs(
    VALID_BRACKET_PAIRS
)
__SORTING_INDEX_BY_GROUP: t.Dict[str, int] = {
    char: i for i, char in enumerate("{}[]()")
}
__SORTING_INDEX_BY_STATE: t.Dict[str, int] = {
    char: i for i, char in enumerate("}]){[(")
}
__REFLECT_MAP: t.Dict[str, str] = {
    "{": "}",
    "}": "{",
    "[": "]",
    "]": "[",
    "(": ")",
    ")": "(",
}


class StringStrategy:
    """Programmatically build valid and invalid strings with nested brackets"""

    def __init__(self, allow_mistakes: bool):
        self.allow_mistakes = allow_mistakes
        self._mistake_choices = [True, False]
        self._mistake_made = False

    def _get_bracket_pair(self) -> t.Tuple[str, str]:
        if self.allow_mistakes:
            make_mistake = random.choice(self._mistake_choices)
        else:
            make_mistake = False
        if make_mistake:
            bracket_pair = random.choice(INVALID_BRACKET_PAIRS)
            self._mistake_made = True
        else:
            bracket_pair = random.choice(VALID_BRACKET_PAIRS)
        return bracket_pair

    def nest_string(self, string: str) -> str:
        """Helper method for rule 2 - nesting

        Rule 2: S has the form "(U)" or "[U]" or "{U}" where U is a properly nested string
        """
        open_bracket, close_bracket = self._get_bracket_pair()
        nested = open_bracket + string + close_bracket
        return nested

    def append_string(self, string: str) -> str:
        """Helper method for rule 3 - W then V

        Rule 3: S has the form "WV" where V and W are properly nested strings.
        """
        open_bracket, close_bracket = self._get_bracket_pair()
        string = string + open_bracket + close_bracket
        return string

    def prepend_string(self, string: str) -> str:
        """Helper method for rule 3 - V then W

        Rule 3: S has the form "VW" where V and W are properly nested strings.
        """
        open_bracket, close_bracket = self._get_bracket_pair()
        string = open_bracket + close_bracket + string
        return string

    def next_action(self) -> t.Callable[[str], str]:
        """The next action with which to build a random valid or invalid string.

        Decision making and mistake inclusion into the string abstracted away.
        """
        string_func = random.choice(
            [self.append_string, self.prepend_string, self.nest_string]
        )
        return string_func

    @property
    def mistake_made(self) -> bool:
        return self._mistake_made


def build_string(length: int, allow_mistakes: bool = False) -> str:
    """Build a structured string of specific length.

    By default do not include structural mistakes.
    """
    if length % 2 == 1:
        raise ValueError(f"Lengths of strings must be even. Got {length}")

    strategy = StringStrategy(allow_mistakes)

    # If mistakes are requested when building an invalid string, there is a decent
    # statistical chance that a short string it could still be valid. This chance is
    # inversely proportional to string length. We can significantly reduce that chance
    # by discarding strings where no mistake was made and try again.
    loops = 0
    while True:
        loops += 1
        string = ""
        for _ in range(length // 2):
            do_build_string = strategy.next_action()
            string = do_build_string(string)

        if not allow_mistakes:
            break
        elif allow_mistakes and strategy.mistake_made:
            break
        elif loops > 10:
            raise ValueError("Infinite loop avoided")
        else:
            continue
    return string


def reverse(string: str) -> str:
    """Reverse a string."""
    return string[::-1]


def reflect(string: str) -> str:
    new_string = []
    for char in reverse(string):
        reflected_char = __REFLECT_MAP[char]
        new_string.append(reflected_char)
    return "".join(new_string)


def truncate(string: str, by: int) -> str:
    """Truncate end of string by a specific number of characters."""
    negative_index = abs(by) * -1
    return string[:negative_index]


def substitute(string: str) -> str:
    """Substitute a single character at random for an invalid character."""
    index = random.randint(0, len(string) - 1)
    if len(string) >= 1:
        new_string = string[0:index] + "X" + string[index + 1 :]
        return new_string
    else:
        return string


def sort_by_state(string: str) -> str:
    """Sort all brackets in a string by their open/closed state, de-structuring the string."""
    indexed_string: t.List[t.Tuple[int, str]] = []
    for char in string:
        index = __SORTING_INDEX_BY_STATE.get(char, -1)
        indexed_char: t.Tuple[int, str] = (index, char)
        indexed_string.append(indexed_char)
    indexed_string.sort()
    sorted_string = "".join([char for _, char in indexed_string])
    return sorted_string


def sort_by_group(string: str) -> str:
    """Sort all brackets in a string by their group."""
    indexed_string: t.List[t.Tuple[int, str]] = []
    for char in string:
        index = __SORTING_INDEX_BY_GROUP.get(char, -1)
        indexed_char: t.Tuple[int, str] = (index, char)
        indexed_string.append(indexed_char)
    indexed_string.sort()
    sorted_string = "".join([char for _, char in indexed_string])
    return sorted_string


if __name__ == "__main__":
    DATA: t.Dict[str, t.List[t.Tuple[str, str]]] = {}
    step = 4
    assert step % 2 == 0
    max_length = 40

    # Add valid strings
    valids: t.List[t.Tuple[str, str]] = []
    for valid in (build_string(l) for l in range(0, max_length, step)):
        basic_valid = (valid, "BASIC")
        sorted_valid = (sort_by_group(valid), "GROUP_SORT")
        reflected_valid = (reflect(valid), "REFLECT")
        valids.extend([basic_valid, sorted_valid, reflected_valid])
    DATA["valid"] = valids
    DATA["valid"].append(("{[()()]}", "PDF"))  # Valid example from exam question PDF

    # Add invalid strings
    invalids: t.List[t.Tuple[str, str]] = []
    for invalid in (build_string(l, True) for l in range(2, max_length, step)):
        invalids.append((invalid, "BASIC"))
    for valid in (build_string(l) for l in range(2, max_length, step)):
        odd_length_invalid = (truncate(valid, 1), "ODD")
        substituted_invalid = (substitute(valid), "SUB")
        sorted_invalid = (sort_by_state(valid), "STATE_SORT")
        reversed_invalid = (reverse(valid), "REVERSE")
        invalids.extend(
            [substituted_invalid, odd_length_invalid, sorted_invalid, reversed_invalid]
        )

    DATA["invalid"] = invalids
    DATA["invalid"].append(("([)()]", "PDF"))  # Invalid example from exam question PDF

    with open("strings.yaml", "w") as handle:
        yaml.safe_dump(DATA, handle)

    # Add big strings to separate file
    BIGDATA: t.Dict[str, t.List[t.Tuple[str, str]]] = {"valid": [], "invalid": []}
    big_length = 200_000
    BIGDATA["valid"].append((build_string(big_length), "BIG"))
    BIGDATA["invalid"].append((build_string(big_length + 2), "TOO_BIG"))
    BIGDATA["invalid"].append((build_string(big_length, True), "BIG"))
    BIGDATA["invalid"].append(("{" * big_length, "BIG"))

    with open("big_strings.yaml", "w") as handle:
        yaml.safe_dump(BIGDATA, handle)
