import pytest
from tests.conftest import create_params_from_yaml

from questions.question_1 import Bracket, BracketType


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("{", Bracket.CURLY),
        ("}", Bracket.CURLY),
        ("[", Bracket.SQUARE),
        ("]", Bracket.SQUARE),
        ("(", Bracket.ROUND),
        (")", Bracket.ROUND),
    ],
)
def test_Bracket_method_from_char(test_input, expected):
    # Given
    char = test_input

    # When
    actual = Bracket.from_char(char)

    # Then
    assert actual == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("{", BracketType.OPEN),
        ("}", BracketType.CLOSED),
        ("[", BracketType.OPEN),
        ("]", BracketType.CLOSED),
        ("(", BracketType.OPEN),
        (")", BracketType.CLOSED),
    ],
)
def test_BracketType_method_from_char(test_input, expected):
    # Given
    char = test_input

    # When
    actual = BracketType.from_char(char)

    # Then
    assert actual == expected
