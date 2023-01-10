import pytest

from enum import Enum

from ecomerceapp.common.validator import is_enum_name, is_default_isoformat, matches_regex


class TestIsEnumName:
    class BasicEnum(Enum):
        ONE = 1

    correct_name = 'ONE'
    incorrect_name = 'FOUR'

    def test_correct_enum_name(self):
        assert is_enum_name(self.BasicEnum, self.correct_name)

    def test_incorrect_enum_name(self):
        assert is_enum_name(self.BasicEnum, self.incorrect_name) is False

    def test_with_different_object_than_enum(self):
        with pytest.raises(TypeError) as e:
            not_an_enum_obj = 0
            name = 'ONE'
            is_enum_name(not_an_enum_obj, name)
        assert ("Object is not an Enum",) == e.value.args


class TestIsoformatValidator:
    correct_value = "2022-12-20T00:00:00+00:00"
    incorrect_value = "20:11:2020"

    def test_correct_isoformat(self):
        assert is_default_isoformat(self.correct_value)

    def test_incorrect_isoformat(self):
        assert is_default_isoformat(self.incorrect_value) is False


class TestMatchesRegex:
    example_regex = r'^[A-Z]*$'
    correct_expression = 'ABCD'
    incorrect_expression = 'ABCd'

    def test_with_value_matching_regex(self):
        assert matches_regex(self.example_regex, self.correct_expression)

    def test_with_value_not_matching_regex(self):
        assert matches_regex(self.example_regex, self.incorrect_expression) is False
