"""
Contains a small utility for opening json files.
"""

from typing import Any
import json


def open_json(file: str) -> Any:
    """Opens a .json file"""
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        return json_file
