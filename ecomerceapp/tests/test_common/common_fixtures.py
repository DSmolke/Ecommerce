import pytest

from enum import Enum
# -----------------------------------------------------------------------
# ENUM
# -----------------------------------------------------------------------
@pytest.fixture
def enum_with_red():
    class Colors(Enum):
        RED = 1
        BLACK = 2
        WHITE = 3

    return Colors


@pytest.fixture
def empty_enum():
    class Colors(Enum):
        pass

    return Colors


# -----------------------------------------------------------------------
# STRING VALUES
# -----------------------------------------------------------------------

@pytest.fixture(params=[
    (r'^[A-Z]+$', "ALA"), (r'^\d+$', '01234'), (r'', '')
])
def correct_regex_exp_pairs(request):
    return request.param


@pytest.fixture(params=[
    (r'^[A-Z]+$', "AaA"), (r'^\d+$', '012b34'), (r'^$', '01aA')
])
def incorrect_regex_exp_pairs(request):
    return request.param

# -----------------------------------------------------------------------
# ISO DATES VALUES
# -----------------------------------------------------------------------
@pytest.fixture(params=[
    "2022-11-24T00:10:50+00:00", "2022-09-20T00:00:00+08:00", "2023-11-20T00:00:00+00:00"
])
def correct_iso_strings(request):
    return request.param

@pytest.fixture(params=[
    "2022-11-24", "2022-09-20T00:00:00", "abc"
])
def incorrect_iso_strings(request):
    return request.param
