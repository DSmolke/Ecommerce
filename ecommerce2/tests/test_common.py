import pytest

from decimal import Decimal

from ecommerce2.common import first_elements_having_same_value, matches_regex, is_dict_structure_correct


class TestFirstElementsHavingSameValue:
    def test_with_one_highest(self):
        assert first_elements_having_same_value([3, 2, 1]) == [3]

    def test_with_two_highest(self):
        assert first_elements_having_same_value([2, 2, 1]) == [2, 2]

    def test_with_all_highest(self):
        assert first_elements_having_same_value([3, 3, 3]) == [3, 3, 3]

    def test_with_one_lowest(self):
        assert first_elements_having_same_value([1, 2, 3]) == [1]

    def test_with_two_lowest(self):
        assert first_elements_having_same_value([1, 1, 2]) == [1, 1]

    def test_when_elements_are_empty_list(self):
        assert first_elements_having_same_value([]) == []

    def test_when_elements_have_one_value(self):
        assert first_elements_having_same_value([1]) == [1]

    def test_when_invalid_type_element_occur(self):
        with pytest.raises(TypeError) as e:
            first_elements_having_same_value([1, 2, '3'])
        assert e.value.args[0] == "Elements list containing invalid type elements"

    @pytest.mark.parametrize(("elements",), [
        (5,),
        ((1, 2, 3),),
        ({1: 1, 2: 2, 3: 3},)
    ])
    def test_when_invalid_type_of_elements_occur(self, elements):
        with pytest.raises(TypeError) as e:
            first_elements_having_same_value(5)
        assert e.value.args[0] == "Argument named 'elements' has invalid type"


class TestMatchingRegex:
    def test_for_expression_matching_regex(self):
        assert matches_regex('ABC', r'^ABC$')

    def test_for_expression_not_matching_regex(self):
        assert not matches_regex('123', r'^12$')

    @pytest.mark.parametrize(('expression',), [
        (1,),
        (1.1,),
        ((1,),),
        ([1],),
        (Decimal("1"),),
    ])
    def test_for_invalid_expression_type(self, expression):
        with pytest.raises(TypeError) as err:
            matches_regex(expression, r'^1$')
        assert err.value.args[0] == f"Invalid expression type: {type(expression)}"

    @pytest.mark.parametrize(('regex',), [
        (1,),
        (1.1,),
        ((1,),),
        ([1],),
        (Decimal("1"),),
    ])
    def test_for_invalid_regex_type(self, regex):
        with pytest.raises(TypeError) as err:
            matches_regex("ABC", regex)
        assert err.value.args[0] == f"Invalid regex type: {type(regex)}"

class TestIsDictStructureCorrect:
    def test_when_valid_dict(self):
        assert is_dict_structure_correct({'A': 1, "B": 1}, 'DATA', {'A', 'B'})

    def test_when_invalid_data(self):
        with pytest.raises(TypeError) as e:
            is_dict_structure_correct([1, 2, 3], 'DATA', {'A', 'B'})
        assert e.value.args[0] == f"Invalid DATA type"

    def test_when_empty_data(self):
        with pytest.raises(ValueError) as e:
            is_dict_structure_correct({}, 'DATA', {'A', 'B'})
        assert e.value.args[0] == f"DATA cannot be an empty dict"

    def test_when_key_not_matching(self):
        with pytest.raises(KeyError) as e:
            is_dict_structure_correct({'A': 1, "B": 1}, 'DATA', {'A', 'B', 'C'})
        assert e.value.args[0] == f"DATA is not valid due to different keys than desired"

# TODO dorobic funkcje ktora sprawdza czy integer jest w przedziale
