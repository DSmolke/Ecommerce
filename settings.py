import os
from os.path import join, dirname
from dotenv import load_dotenv
from typing import Final

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class TestSettings:
    VALID_FILEPATH: Final = os.getenv('VALID_FILEPATH')
    INVALID_FILEPATH: Final = str(os.getenv('INVALID_FILEPATH'))
    FILEPATH_HAVING_INVALID_TYPE: Final = str(os.getenv('FILEPATH_HAVING_INVALID_TYPE'))


class ValidatorSettings:
    CLIENT_NAME_REGEX = fr"{os.getenv('CLIENT_NAME_REGEX')}"
    CLIENT_SURNAME_REGEX = fr"{os.getenv('CLIENT_SURNAME_REGEX')}"
    CLIENT_BALANCE_REGEX = fr"{os.getenv('CLIENT_BALANCE_REGEX')}"
    CLIENT_AGE_RANGE_MIN = int(os.getenv('CLIENT_AGE_RANGE_MIN'))
    PRODUCT_NAME_REGEX = fr"{os.getenv('PRODUCT_NAME_REGEX')}"
    PRODUCT_CATEGORY_REGEX = fr"{os.getenv('PRODUCT_CATEGORY_REGEX')}"
    PRODUCT_PRICE_REGEX = fr"{os.getenv('PRODUCT_PRICE_REGEX')}"
