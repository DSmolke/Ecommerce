import json
from typing import Any


def load_file(filepath: str) -> Any:
    """ Basic json file loader """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Invalid filepath")
