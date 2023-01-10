import os

from decimal import Decimal
from dotenv import load_dotenv
from typing import Final

class AppData:
    """ Class AppData is created to distribute data stored in .env file  """
    load_dotenv()
    MINIMAL_CUSTOMER_AGE: Final = int(os.getenv('MINIMAL_CUSTOMER_AGE'))
    DISCOUNT_RATE_FOR_DATE = Decimal(os.getenv('DISCOUNT_RATE_FOR_DATE'))
    DISCOUNT_RATE_FOR_CUSTOMER_AGE = Decimal(os.getenv('DISCOUNT_RATE_FOR_CUSTOMER_AGE'))
    DISCOUNT_AGE_CAP = int(os.getenv('DISCOUNT_AGE_CAP'))
