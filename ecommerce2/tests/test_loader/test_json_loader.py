import pytest

from typing import Final

from ecommerce2.loader.json_loader import load_file
from ecommerce2.settings import TestSettings


class TestLoadFile:
    VALID_FILEPATH: Final = TestSettings.VALID_FILEPATH
    INVALID_FILEPATH: Final = TestSettings.INVALID_FILEPATH
    FILEPATH_HAVING_INVALID_TYPE: Final = TestSettings.FILEPATH_HAVING_INVALID_TYPE

    @pytest.mark.xfail(reason="If pytest is run from different directory than /tests it might cause error")
    def test_with_valid_filepath(self):
        assert load_file(self.VALID_FILEPATH) == [{"A": 1, "B": 2}]

    def test_with_invalid_filepath(self):
        with pytest.raises(ValueError) as er:
            load_file(self.INVALID_FILEPATH)
        assert er.value.args[0] == "Invalid filepath"

    def test_with_filepath_having_invalid_type(self):
        with pytest.raises(ValueError) as e:
            load_file(self.FILEPATH_HAVING_INVALID_TYPE)
        assert e.value.args[0] == "Invalid filepath"
