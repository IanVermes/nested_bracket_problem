import pytest
from tests.conftest import create_params_from_yaml

from questions.question_1 import IsValid, BracketGroup, BracketState, is_odd


@pytest.mark.parametrize(
    "test_input,expected", [(IsValid.YES, 1), (IsValid.NO, 0)],
)
def test_IsValid_can_be_cast_to_expected_int(test_input, expected):
    # When
    actual = int(test_input)

    # Then
    assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("{", BracketGroup.CURLY),
        ("}", BracketGroup.CURLY),
        ("[", BracketGroup.SQUARE),
        ("]", BracketGroup.SQUARE),
        ("(", BracketGroup.ROUND),
        (")", BracketGroup.ROUND),
        ("a", BracketGroup.UNKNOWN),
        ("x", BracketGroup.UNKNOWN),
        ("<", BracketGroup.UNKNOWN),
        ("", BracketGroup.UNKNOWN),
    ],
)
def test_Bracket_method_from_char(test_input, expected):
    # Given
    char = test_input

    # When
    actual = BracketGroup.from_char(char)

    # Then
    assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("{", BracketState.OPEN),
        ("}", BracketState.CLOSED),
        ("[", BracketState.OPEN),
        ("]", BracketState.CLOSED),
        ("(", BracketState.OPEN),
        (")", BracketState.CLOSED),
    ],
)
def test_BracketState_method_from_char(test_input, expected):
    # Given
    char = test_input

    # When
    actual = BracketState.from_char(char)

    # Then
    assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected_bool",
    [("e" * i, False) for i in range(0, 10, 2)]
    + [("o" * i, True) for i in range(1, 10, 2)],
)
def test_is_odd(test_input, expected_bool):
    # When
    actual_bool = is_odd(test_input)

    # Then
    assert actual_bool == expected_bool
