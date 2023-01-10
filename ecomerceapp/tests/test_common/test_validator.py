from decimal import Decimal

import pytest

from ecomerceapp.common.validator import is_enum_name, is_unstandardized_decimal_grater_or_equal_to, matches_regex, \
    is_default_isoformat, is_integer_grater_equal_to

from ecomerceapp.tests.test_common.common_fixtures import enum_with_red, empty_enum, correct_regex_exp_pairs, \
    incorrect_regex_exp_pairs, correct_iso_strings, incorrect_iso_strings


class TestIsEnumName:

    def test_with_correct_enum(self, enum_with_red):
        assert is_enum_name(enum_with_red, 'RED')

    def test_with_empty_enum(self, empty_enum):
        assert not is_enum_name(empty_enum, 'RED')

    def test_with_argument_different_than(self, enumerator='Enum'):
        with pytest.raises(TypeError) as e:
            is_enum_name(enumerator, 'RED')
        assert e.value.args[0] == "Object is not an Enum"

    def test_with_valid_enum_but_invalid_name(self, enum_with_red):
        with pytest.raises(TypeError) as e:
            is_enum_name(enum_with_red, 255)
        assert e.value.args[0] == "Name is not a string"


class TestIsUnstandardizedDecimalGraterOrEqualTo:
    @pytest.mark.parametrize(('comp_value', 'value'), [
        (Decimal('0'), '0.1'),
        (Decimal('0'), '0.0'),
    ])
    def test_when_compare_value_lower_or_equal_than_value(self, comp_value, value):
        assert is_unstandardized_decimal_grater_or_equal_to(comp_value, value)

    def test_when_when_compare_value_higher_than_value(self):
        assert is_unstandardized_decimal_grater_or_equal_to(Decimal('1'), '0') is False

    def test_when_compare_value_not_decimal(self):
        with pytest.raises(TypeError) as e:
            is_unstandardized_decimal_grater_or_equal_to(0, '1')
        assert e.value.args[0] == 'Compare value has invalid type'

    def test_when_value_not_str(self):
        with pytest.raises(TypeError) as e:
            is_unstandardized_decimal_grater_or_equal_to(1, '1')
        assert e.value.args[0] == 'Compare value has invalid type'

    def test_when_value_is_not_unstandardized_decimal(self):
        with pytest.raises(TypeError) as e:
            is_unstandardized_decimal_grater_or_equal_to(Decimal('0'), 1)
        assert e.value.args[0] == 'Value argument has invalid type'

    def test_when_value_has_wrong_formatting(self):
        with pytest.raises(ValueError) as e:
            is_unstandardized_decimal_grater_or_equal_to(Decimal('0'), '1$')
        assert e.value.args[0] == 'Value argument has invalid formatting'


class TestIsIntegerGraterEqualTo:
    def test_when_is_grater(self):
        assert is_integer_grater_equal_to(0, 1)

    def test_when_is_not_grater(self):
        assert is_integer_grater_equal_to(1, 0) is False

    def test_when_invalid_compare_value_type(self):
        with pytest.raises(TypeError) as e:
            is_integer_grater_equal_to(1.1, 0)
        assert e.value.args[0] == 'Compare value has invalid type'

    def test_when_invalid_value_type(self):
        with pytest.raises(TypeError) as e:
            is_integer_grater_equal_to(0, 1.1)
        assert e.value.args[0] == 'Value argument has invalid type'


class TestMatchesRegex:
    def test_with_correct_regex_exp_pairs(self, correct_regex_exp_pairs):
        assert matches_regex(*correct_regex_exp_pairs)

    def test_with_incorrect_regex_exp_pairs(self, incorrect_regex_exp_pairs):
        assert not matches_regex(*incorrect_regex_exp_pairs)

    def test_with_expression_not_being_string(self):
        with pytest.raises(TypeError) as e:
            matches_regex(r'', 1)
        assert e.value.args[0] == 'Expression should be string'


class TestIsDefaultIsoFormat:
    def test_with_correct_iso_strings(self, correct_iso_strings):
        assert is_default_isoformat(correct_iso_strings)

    def test_with_incorrect_iso_strings(self, incorrect_iso_strings):
        assert not is_default_isoformat(incorrect_iso_strings)

    def test_with_expression_not_being_string(self):
        with pytest.raises(TypeError) as e:
            is_default_isoformat(("2022-11-24T00:10:50+00:00",))
        assert e.value.args[0] == 'Expression should be string'
