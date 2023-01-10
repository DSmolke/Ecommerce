import os
from dotenv import load_dotenv
from typing import Final

import logging


def main() -> None:
    logging.basicConfig(
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler()
        ]
    )

    load_dotenv()
    ORDERS_FILE_PATH: Final = os.getenv('ORDERS_FILE_PATH')
