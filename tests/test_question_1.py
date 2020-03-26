import pytest
from tests.conftest import create_params_from_yaml

from questions.question_1 import solution


@pytest.mark.parametrize(*create_params_from_yaml())
def test_solution(test_input, expected_output):
    # When
    actual_output = solution(test_input)

    # Then
    assert expected_output == actual_output
