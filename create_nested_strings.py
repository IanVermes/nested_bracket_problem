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


def truncate(string: str, by: int) -> str:
    """Truncate end of string by a specific number of characters."""
    negative_index = abs(by) * -1
    return string[:negative_index]


if __name__ == "__main__":
    DATA: t.Dict[str, t.List[str]] = {}
    step = 4
    assert step % 2 == 0
    max_length = 40

    # Add valid strings
    DATA["valid"] = [build_string(l) for l in range(0, max_length, step)]
    DATA["valid"].append("{[()()]}")  # Valid example from exam question PDF

    # Add invalid strings
    DATA["invalid"] = [build_string(l, True) for l in range(2, max_length, step)]
    more_invalids = [
        truncate(s, 1)
        for s in (build_string(l, True) for l in range(2, max_length, step))
    ]
    DATA["invalid"].extend(list(more_invalids))  # Add strings with odd number of chars
    DATA["invalid"].extend(["([)()]"])  # Invalid example from exam question PDF

    # # Add big strings # TODO UNCOMMENT THIS BLOCK
    # big_length = 200_000
    # DATA["valid"].append(build_string(big_length))
    # DATA["invalid"].append(build_string(big_length, False))

    with open("strings.yaml", "w") as handle:
        yaml.safe_dump(DATA, handle)
